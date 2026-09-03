import sys
import os
import shutil
import subprocess
import tempfile
import time
import requests as _requests
from .utils import is_valid_text, fix_corrupted_text

MAX_OUTPUT_SIZE = 10_000

# ── Wandbox API (облачный компилятор, fallback когда нет локальных тулов) ─────
# Бесплатно, без ключа. https://wandbox.org/
WANDBOX_URL = 'https://wandbox.org/api/compile.json'

WANDBOX_COMPILERS = {
    'cpp':  'gcc-head',
    'java': 'openjdk-jdk-21+35',
}

def run_via_wandbox(lang, code, input_data=None):
    """Запуск кода через бесплатный Wandbox API (без ключа)."""
    import re as _re
    compiler = WANDBOX_COMPILERS.get(lang)
    if not compiler:
        return {'status': 'error', 'output': f'Язык {lang} не поддерживается облачным компилятором.', 'via': 'wandbox'}

    send_code = code
    # Java: Wandbox называет файл prog.java, поэтому переименовываем public class
    if lang == 'java':
        m = _re.search(r'public\s+class\s+(\w+)', code)
        if m:
            cls = m.group(1)
            if cls != 'prog':
                send_code = code.replace(f'public class {cls}', 'public class prog', 1)
                # Replace ALL occurrences of the class name as a whole word
                send_code = _re.sub(rf'\b{_re.escape(cls)}\b', 'prog', send_code)

    payload = {'compiler': compiler, 'code': send_code}
    if input_data:
        payload['stdin'] = input_data

    try:
        resp = _requests.post(WANDBOX_URL, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        compiler_error = data.get('compiler_error', '')
        program_output = data.get('program_output', '')
        program_error  = data.get('program_error', '')
        status_code    = data.get('status', '0')

        if compiler_error:
            return {'status': 'error', 'output': compiler_error, 'via': 'wandbox'}
        output = program_output + program_error
        status = 'error' if str(status_code) != '0' else 'success'
        return {
            'status': status,
            'output': output.strip() or '(нет вывода)',
            'via': 'wandbox',
        }
    except _requests.exceptions.Timeout:
        return {'status': 'error', 'output': 'Превышено время ожидания облачного компилятора (20 с).', 'via': 'wandbox'}
    except _requests.exceptions.ConnectionError:
        return {'status': 'error', 'output': 'Нет соединения с облачным компилятором (wandbox.org). Проверьте интернет.', 'via': 'wandbox'}
    except Exception as e:
        return {'status': 'error', 'output': f'Ошибка облачного компилятора: {e}', 'via': 'wandbox'}


FORBIDDEN_IMPORTS = {"os", "sys", "subprocess", "socket", "shutil",
                     "ctypes", "multiprocessing", "threading", "importlib"}

FORBIDDEN_NAMES = {'exec', 'eval', '__import__', 'compile', 'open', 'breakpoint'}

def check_code_safety(code):
    """Возвращает (is_safe, reason)."""
    import ast as _ast
    try:
        tree = _ast.parse(code)
    except SyntaxError:
        return True, ""  # синтакс-ошибки поймает выполнение
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.Import, _ast.ImportFrom)):
            names = [a.name.split(".")[0] for a in node.names] if isinstance(node, _ast.Import) else [node.module.split(".")[0] if node.module else ""]
            for name in names:
                if name in FORBIDDEN_IMPORTS:
                    return False, f"Запрещённый модуль: {name}"
        # Ban dangerous builtins
        if isinstance(node, _ast.Call):
            func = node.func
            fname = ''
            if isinstance(func, _ast.Name): fname = func.id
            elif isinstance(func, _ast.Attribute): fname = func.attr
            if fname in FORBIDDEN_NAMES:
                return False, f"Запрещённая функция: {fname}"
    return True, ""

def run_python_code(code, input_data=None):
    safe, reason = check_code_safety(code)
    if not safe:
        return {'status': 'error', 'output': f'Запрещено: {reason}', 'error': reason}
    """
    Run Python code and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
        process = subprocess.Popen(
            [sys.executable, temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            env=env,
        )

        stdout, stderr = process.communicate(input=input_data, timeout=5)
        stdout = stdout[:MAX_OUTPUT_SIZE]
        stderr = stderr[:MAX_OUTPUT_SIZE]

        if process.returncode != 0:
            return {
                'status': 'error',
                'output': stderr,
                'error': stderr
            }

        return {
            'status': 'success',
            'output': stdout
        }
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        return {
            'status': 'error',
            'output': 'Execution timed out',
            'error': 'Execution timed out after 10 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'output': str(e),
            'error': str(e)
        }
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def run_java_code(code, input_data=None):
    """
    Run Java code and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    # Extract class name from code (safe regex, prevents path traversal)
    import re as _re
    class_name = "Main"
    m = _re.search(r'public\s+class\s+(\w+)', code)
    if m:
        class_name = m.group(1)
    # Safety: class_name must be a valid identifier only
    if not _re.match(r'^\w+$', class_name):
        class_name = "Main"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        java_file = os.path.join(temp_dir, f"{class_name}.java")
        
        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Compile Java code — если нет javac, используем Wandbox
        if not shutil.which('javac'):
            return run_via_wandbox('java', code, input_data)
        compile_process = subprocess.run(
            ['javac', '-encoding', 'UTF-8', java_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
        )

        if compile_process.returncode != 0:
            return {
                'status': 'error',
                'output': compile_process.stderr,
                'error': f"Compilation error: {compile_process.stderr}"
            }

        # Run Java code
        try:
            process = subprocess.Popen(
                ['java', '-Dfile.encoding=UTF-8', '-Dstdout.encoding=UTF-8', '-cp', temp_dir, class_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
            )

            stdout, stderr = process.communicate(input=input_data, timeout=5)

            if process.returncode != 0:
                return {
                    'status': 'error',
                    'output': stderr,
                    'error': stderr
                }

            return {
                'status': 'success',
                'output': stdout
            }
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return {
                'status': 'error',
                'output': 'Execution timed out',
                'error': 'Execution timed out after 10 seconds'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': str(e),
                'error': str(e)
            }

def run_cpp_code(code, input_data=None):
    """
    Run C++ code and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
        
    # Если g++ не установлен — используем Wandbox
    if not shutil.which('g++') and not shutil.which('g++.exe'):
        return run_via_wandbox('cpp', code, input_data)

    with tempfile.TemporaryDirectory() as temp_dir:
        cpp_file = os.path.join(temp_dir, "main.cpp")
        exe_file = os.path.join(temp_dir, "main.exe")

        with open(cpp_file, 'w', encoding='utf-8') as f:
            f.write(code)

        # Compile C++ code
        compile_process = subprocess.run(
            ['g++', cpp_file, '-o', exe_file, '-finput-charset=UTF-8', '-fexec-charset=UTF-8'],
            capture_output=True,
            text=True,
            encoding='utf-8',
        )

        if compile_process.returncode != 0:
            return {
                'status': 'error',
                'output': compile_process.stderr,
                'error': f"Compilation error: {compile_process.stderr}"
            }

        # Run C++ code
        try:
            env_cpp = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}
            process = subprocess.Popen(
                [exe_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                env=env_cpp,
            )

            stdout, stderr = process.communicate(input=input_data, timeout=5)

            if process.returncode != 0:
                return {
                    'status': 'error',
                    'output': stderr,
                    'error': stderr
                }

            return {
                'status': 'success',
                'output': stdout
            }
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return {
                'status': 'error',
                'output': 'Execution timed out',
                'error': 'Execution timed out after 10 seconds'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': str(e),
                'error': str(e)
            }

JS_FORBIDDEN = {'require', 'process', '__dirname', '__filename', 'fs', 'child_process', 'net', 'http', 'https', 'os', 'eval', 'Function'}

def run_javascript_code(code, input_data=None):
    """
    Run JavaScript code using Node.js and return the result
    """
    if not is_valid_text(code):
        code = fix_corrupted_text(code)
    # Basic safety: block dangerous Node.js APIs
    import re as _re
    for banned in JS_FORBIDDEN:
        # Check as whole word to avoid false positives
        if _re.search(rf'\b{_re.escape(banned)}\b', code):
            return {'status': 'error', 'output': f'Запрещено: использование {banned} не разрешено.', 'error': banned}

    with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name

    try:
        process = subprocess.Popen(
            ['node', temp_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
        )

        stdout, stderr = process.communicate(input=input_data, timeout=5)
        stdout = stdout[:MAX_OUTPUT_SIZE]
        stderr = stderr[:MAX_OUTPUT_SIZE]

        if process.returncode != 0:
            return {
                'status': 'error',
                'output': stderr,
                'error': stderr
            }

        return {
            'status': 'success',
            'output': stdout
        }
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        return {
            'status': 'error',
            'output': 'Execution timed out',
            'error': 'Execution timed out after 10 seconds'
        }
    except Exception as e:
        return {
            'status': 'error',
            'output': str(e),
            'error': str(e)
        }
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)