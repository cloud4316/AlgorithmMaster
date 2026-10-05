"""
Проверка кода студентов.
AST-анализ + тест-кейсы + Ollama LLM (локальный, бесплатный).
"""
import ast as _ast
import os
import json
import threading
import requests
import logging

logger = logging.getLogger(__name__)

# ── Ollama ────────────────────────────────────────────────────────────────────

_OLLAMA_MODEL = 'qwen2.5:14b-instruct'
_ollama_available = None  # None=не проверено, True/False
_ollama_lock = threading.Lock()


def _check_ollama() -> bool:
    """Проверяет доступность Ollama сервера (кешируется)."""
    global _ollama_available
    if _ollama_available is not None:
        return _ollama_available
    with _ollama_lock:
        if _ollama_available is not None:
            return _ollama_available
        try:
            from django.conf import settings
            model = getattr(settings, 'OLLAMA_MODEL', _OLLAMA_MODEL)
            base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
            resp = requests.get(f'{base_url}/api/tags', timeout=3)
            models = [m['name'] for m in resp.json().get('models', [])]
            _ollama_available = any(model in m for m in models)
            if not _ollama_available:
                logger.warning('Ollama: модель %s не найдена. Доступны: %s', model, models)
        except Exception as e:
            logger.warning('Ollama недоступен: %s', e)
            _ollama_available = None  # не кэшируем False — перепроверим при следующем вызове
    return bool(_ollama_available)


def _ollama_request(prompt: str, num_predict: int = 400) -> str | None:
    """Отправляет запрос в Ollama и возвращает текст ответа или None."""
    from django.conf import settings
    model = getattr(settings, 'OLLAMA_MODEL', _OLLAMA_MODEL)
    base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
    try:
        resp = requests.post(
            f'{base_url}/v1/chat/completions',
            json={
                'model': model,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.1,
                'stream': False,
                'options': {'num_predict': num_predict},
            },
            timeout=360,
        )
        resp.raise_for_status()
        return resp.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.warning('Ollama request error: %s', e)
        return None


def _parse_json(text: str) -> dict | list | None:
    """Извлекает первый JSON-объект или массив из текста."""
    if not text:
        return None
    # ищем объект {...}
    s = text.find('{')
    e = text.rfind('}') + 1
    if s >= 0 and e > s:
        try:
            return json.loads(text[s:e])
        except Exception:
            pass
    # ищем массив [...]
    s = text.find('[')
    e = text.rfind(']') + 1
    if s >= 0 and e > s:
        try:
            return json.loads(text[s:e])
        except Exception:
            pass
    return None


def ai_generate_test_inputs(code: str, work_title: str) -> list[str]:
    """
    Просит LLM сгенерировать тестовые входные данные для кода с input().
    Возвращает список строк (каждая = одна сессия stdin, строки разделены \\n).
    """
    if not _check_ollama():
        return []

    prompt = (
        f'Task: "{work_title}"\n\n'
        f'Python code:\n{code[:2000]}\n\n'
        'This code uses input(). Generate 3 realistic test input sequences.\n'
        'Each sequence simulates one complete run (multiple input() calls = multiple lines).\n'
        'Respond ONLY with JSON array of strings. Each string = one test run inputs joined by newline.\n'
        'Example for a guessing game needing 3 guesses: ["5\\n3\\n7", "10\\n1\\n4", "2\\n8\\n6"]\n'
        'If code needs no input, return [].'
    )

    text = _ollama_request(prompt, num_predict=200)
    result = _parse_json(text)
    if isinstance(result, list):
        return [str(x) for x in result if x]
    return []


def ai_review_code(code: str, work_title: str, language: str = 'python',
                   run_results: list[dict] | None = None) -> dict | None:
    """
    ИИ-проверка кода через Ollama.
    run_results — список {'input': str, 'output': str, 'error': str} из реальных запусков.
    Возвращает dict: score, verdict, feedback, issues, suggestions.
    """
    if not _check_ollama():
        return None

    # Блок с реальными результатами запуска
    runs_block = ''
    if run_results:
        parts = []
        for i, r in enumerate(run_results, 1):
            inp = (r.get('input') or '').replace('\n', '↵')
            out = (r.get('output') or '').strip()[:300]
            err = (r.get('error') or '').strip()[:200]
            line = f'Run {i}: input="{inp}" → output="{out}"'
            if err:
                line += f' ERROR="{err}"'
            parts.append(line)
        runs_block = '\n\nActual execution results:\n' + '\n'.join(parts)

    prompt = (
        f'You are a programming teacher grading student code for task: "{work_title}".\n\n'
        'Grade 0-100:\n'
        '- 90-100: correct and clean code\n'
        '- 60-89: mostly correct, minor issues\n'
        '- 30-59: partial solution or style problems\n'
        '- 0-29: wrong answer, crashes, or does not run\n\n'
        'Respond ONLY with valid JSON (no markdown, nothing outside JSON).\n'
        'Write feedback, issues, suggestions in Russian.\n'
        'Example: {"score": 85, "verdict": "correct", "feedback": "Хорошее решение.", '
        '"issues": ["Нет комментариев"], "suggestions": ["Добавьте docstring"]}\n\n'
        f'Student code ({language}):\n{code[:3500]}'
        f'{runs_block}'
    )

    text = _ollama_request(prompt, num_predict=400)
    result = _parse_json(text)
    if isinstance(result, dict):
        result['score'] = max(0, min(100, int(result.get('score', 50))))
        if result['score'] >= 70:
            result['verdict'] = 'correct'
        elif result['score'] >= 40:
            result['verdict'] = 'partially_correct'
        else:
            result['verdict'] = 'incorrect'
        result.setdefault('issues', [])
        result.setdefault('suggestions', [])
        result.setdefault('feedback', '')
        return result
    logger.warning('Ollama review: не удалось разобрать JSON из ответа')
    return None


_LLAVA_MODEL = 'llava:7b'


def _check_llava() -> bool:
    """Проверяет доступность LLaVA в Ollama."""
    try:
        from django.conf import settings
        base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        model = getattr(settings, 'LLAVA_MODEL', _LLAVA_MODEL)
        resp = requests.get(f'{base_url}/api/tags', timeout=3)
        models = [m['name'] for m in resp.json().get('models', [])]
        return any(model in m for m in models)
    except Exception:
        return False


def _llava_request(prompt: str, image_b64: str) -> str | None:
    """Отправляет изображение + текст в LLaVA. Возвращает текстовый ответ."""
    from django.conf import settings
    base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
    model = getattr(settings, 'LLAVA_MODEL', _LLAVA_MODEL)
    try:
        resp = requests.post(
            f'{base_url}/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'images': [image_b64],
                'stream': False,
                'options': {'num_predict': 200, 'temperature': 0.1},
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get('response', '').strip()
    except Exception as e:
        logger.warning('LLaVA request error: %s', e)
        return None


def extract_images_from_file(file_path: str) -> list[str]:
    """Извлекает изображения из .docx или .pdf. Возвращает список base64-строк."""
    import base64
    ext = os.path.splitext(file_path)[1].lower()
    images = []
    try:
        if ext == '.docx':
            import docx as _docx
            doc = _docx.Document(file_path)
            for rel in doc.part.rels.values():
                if 'image' in rel.reltype:
                    blob = rel.target_part.blob
                    images.append(base64.b64encode(blob).decode('utf-8'))
        elif ext == '.pdf':
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    for img in (page.images or []):
                        try:
                            x0, top, x1, bot = img['x0'], img['top'], img['x1'], img['bottom']
                            crop = page.crop((x0, top, x1, bot))
                            pil_img = crop.to_image(resolution=100).original
                            import io
                            buf = io.BytesIO()
                            pil_img.save(buf, format='PNG')
                            images.append(base64.b64encode(buf.getvalue()).decode('utf-8'))
                        except Exception:
                            pass
    except Exception as e:
        logger.warning('extract_images_from_file %s: %s', file_path, e)
    return images[:10]  # не больше 10 изображений


def ai_review_images(images_b64: list[str], work_title: str) -> dict:
    """
    Проверяет изображения из отчёта через LLaVA.
    Возвращает: {'score': 0-30, 'found': int, 'feedback': str, 'issues': list}
    """
    if not images_b64 or not _check_llava():
        return {'score': 0, 'found': 0, 'feedback': 'Изображения не обнаружены или LLaVA недоступна.', 'issues': ['Рисунки/схемы/графики отсутствуют или не загружены']}

    prompt = (
        f'Это изображение из студенческого отчёта по практической работе "{work_title}" '
        f'по дисциплине "Автоматизация технологических процессов" (АСУТП).\n\n'
        f'Оцени изображение по следующим критериям (каждый пункт — да/нет):\n'
        f'1. Это технический рисунок, схема, график или диаграмма (не фото, не скриншот интерфейса)?\n'
        f'2. Подписаны ли оси (если это график) или элементы схемы?\n'
        f'3. Соответствует ли содержание теме АСУТП (объекты управления, ПИД-регуляторы, переходные характеристики, структурные схемы, таблицы данных)?\n'
        f'4. Качество исполнения приемлемое (читаемо, не размыто)?\n\n'
        f'Ответь кратко: перечисли да/нет по каждому пункту, затем одно предложение — общий вывод.'
    )

    results = []
    for i, img_b64 in enumerate(images_b64):
        answer = _llava_request(prompt, img_b64)
        if answer:
            results.append(answer)
        if i >= 4:  # максимум 5 изображений
            break

    if not results:
        return {'score': 0, 'found': 0, 'feedback': 'LLaVA не смогла обработать изображения.', 'issues': ['Проверьте изображения вручную']}

    # Считаем сколько изображений прошли проверку
    good = 0
    issues = []
    feedback_parts = []
    for i, res in enumerate(results, 1):
        lower = res.lower()
        yes_count = lower.count('да') + lower.count('yes')
        no_count  = lower.count('нет') + lower.count('no')
        if yes_count >= 2 and yes_count > no_count:
            good += 1
            feedback_parts.append(f'Рисунок {i}: принят ✓')
        else:
            issues.append(f'Рисунок {i}: не соответствует требованиям ({res[:100]})')
            feedback_parts.append(f'Рисунок {i}: замечания')

    total = len(results)
    ratio = good / total if total else 0
    score = round(ratio * 30)  # максимум 30 баллов за изображения

    feedback = (
        f'ИИ проверил {total} рис. — {good} приняты. '
        + ' '.join(feedback_parts)
    )
    return {'score': score, 'found': total, 'feedback': feedback, 'issues': issues}


def extract_text_from_file(file_path: str) -> str:
    """Извлекает текст из .docx или .pdf. Возвращает строку или ''."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.docx':
            import docx as _docx
            doc = _docx.Document(file_path)
            parts = []
            for para in doc.paragraphs:
                if para.text.strip():
                    parts.append(para.text.strip())
            for table in doc.tables:
                for row in table.rows:
                    row_text = ' | '.join(c.text.strip() for c in row.cells if c.text.strip())
                    if row_text:
                        parts.append(row_text)
            return '\n'.join(parts)
        elif ext == '.pdf':
            import pdfplumber
            parts = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        parts.append(text)
            return '\n'.join(parts)
    except Exception as e:
        logger.warning('extract_text_from_file %s: %s', file_path, e)
    return ''


def ai_review_report(report_text: str, work_title: str, work_description: str, file_path: str = '') -> dict | None:
    """
    Проверяет отчёт студента (Word/PDF) через Ollama.
    Возвращает dict: score, verdict, feedback, issues, suggestions.
    """
    if not _check_ollama():
        return None

    # Критерии оценки для промпта
    criteria = (
        'Критерии оценки отчёта:\n'
        '- 90-100 (отлично): все задания выполнены, таблицы заполнены корректно, '
        'графики/схемы присутствуют, выводы содержательные, оформление по ГОСТ.\n'
        '- 70-89 (хорошо): все задания выполнены с незначительными ошибками или пропусками, '
        'есть вывод.\n'
        '- 50-69 (удовлетворительно): выполнено 60%+ заданий, есть грубые ошибки '
        'или пропущены таблицы/схемы.\n'
        '- 0-49 (неудовлетворительно): менее 60% заданий выполнено, нет выводов, '
        'нет таблиц, работа скопирована без осмысления.\n'
    )

    import re

    # ── Python-проверки очевидных пунктов ──────────────────────────────────────
    txt = report_text.lower()

    def _found(*patterns):
        return any(re.search(p, txt, re.IGNORECASE) for p in patterns)

    checks = {
        'titulny':   _found(r'фио|выполнил|студент.{0,30}группы?|группа.{0,10}\d', r'специальност'),
        'goal':      _found(r'цель работы|цель\s*:', r'целью.{0,20}является'),
        'numbers':   _found(r'[kкKК]\s*=\s*\d', r'[tтTТ]\s*=\s*\d', r'τ\s*=\s*\d', r'tau\s*=\s*\d',
                            r'постоянн.{0,15}врем.{0,5}\d', r'коэффициент.{0,20}\d'),
        'conclusion_class': _found(r'статическ|астатическ|самовыравнивани', r'класс.{0,20}оу'),
        'conclusion_work':  _found(r'выво[дд].{0,5}работ|в ходе.{0,30}работ|таким образом', r'заключени'),
        'sources':   _found(r'список.{0,20}источник', r'использованн.{0,20}литератур',
                            r'гост\s+\d', r'учебник|пособие'),
    }

    # Таблица — проверяем есть ли строки с числами (не только заголовки)
    table_lines = [l for l in report_text.splitlines() if re.search(r'\d', l) and re.search(r'[|│\t]|\s{3,}', l)]
    checks['table_filled'] = len(table_lines) >= 1

    # Авто-баллы за подтверждённые пункты (max 60 из 70 — остальное модель)
    auto_score = sum([
        10 if checks['titulny'] else 0,
        5  if checks['goal'] else 0,
        10 if checks['numbers'] else 0,
        10 if checks['conclusion_class'] else 0,
        10 if checks['conclusion_work'] else 0,
        5  if checks['table_filled'] else 0,
    ])  # max 50 из 60

    # Сообщаем модели что уже проверено
    confirmed = []
    missing = []
    labels = {
        'titulny': 'Титульный лист (ФИО, группа, специальность)',
        'goal': 'Цель работы',
        'numbers': 'Числовые данные (K, T, τ)',
        'conclusion_class': 'Вывод о классе ОУ',
        'conclusion_work': 'Вывод по работе',
        'table_filled': 'Таблица свойств ОУ с числами',
        'sources': 'Список источников (книги/ГОСТы)',
    }
    for key, label in labels.items():
        (confirmed if checks.get(key) else missing).append(label)

    report_excerpt = report_text[:2000]
    task_clean = re.sub(r'<[^>]+>', ' ', work_description)
    task_clean = re.sub(r'\s+', ' ', task_clean).strip()[:600]

    prompt = (
        f'Отвечай только на русском языке.\n\n'
        f'Ты преподаватель дисциплины АСУТП. Автоматическая система уже проверила отчёт студента.\n\n'
        f'=== УЖЕ ПОДТВЕРЖДЕНО (не добавляй в issues) ===\n'
        f'{chr(10).join("✓ " + c for c in confirmed)}\n\n'
        f'=== НЕ НАЙДЕНО (вероятно отсутствует) ===\n'
        f'{chr(10).join("✗ " + m for m in missing) if missing else "— (все пункты найдены)"}\n\n'
        f'=== ЗАДАНИЕ ===\n{task_clean}\n\n'
        f'=== ФРАГМЕНТ ОТЧЁТА ===\n{report_excerpt}\n\n'
        f'Твоя задача — оценить КАЧЕСТВО содержания:\n'
        f'- Насколько содержательны выводы (не формальные)?\n'
        f'- Правильно ли описаны свойства ОУ и класс?\n'
        f'- Есть ли технические ошибки в числах или формулировках?\n'
        f'Добавь в issues только РЕАЛЬНЫЕ качественные недостатки из текста отчёта.\n'
        f'НЕ повторяй пункты из "Не найдено" — они уже будут добавлены автоматически.\n\n'
        f'Верни ТОЛЬКО JSON (без markdown), поля:\n'
        f'score: целое от 0 до 10 (только за качество содержания)\n'
        f'feedback: итоговый вывод об отчёте, 2-3 предложения, только русский язык\n'
        f'issues: массив строк — реальные качественные недостатки текста (пустой если нет)\n'
        f'suggestions: массив строк — конкретные советы по каждому недостатку'
    )

    text = _ollama_request(prompt, num_predict=400)
    result = _parse_json(text) or {}

    # quality_score от модели (0-10), auto_score уже подсчитан Python (0-50+)
    quality_score = max(0, min(10, int(result.get('score', 5))))
    text_score = min(70, auto_score + quality_score)

    # missing пункты → автоматически в issues
    missing_issues = [f'{m} — не обнаружено в отчёте' for m in missing]

    # Проверка изображений через LLaVA
    img_result = {'score': 0, 'found': 0, 'feedback': '', 'issues': []}
    if file_path:
        images = extract_images_from_file(file_path)
        img_result = ai_review_images(images, work_title)

    final_score = text_score + img_result['score']

    feedback_parts = []
    if result.get('feedback'):
        feedback_parts.append(result['feedback'])
    if img_result['found'] > 0:
        feedback_parts.append(img_result['feedback'])
    elif not file_path:
        feedback_parts.append('Изображения не проверялись (файл недоступен).')
    else:
        feedback_parts.append('Рисунки/схемы/графики в файле не обнаружены — проверит преподаватель.')

    all_issues = missing_issues + list(result.get('issues', [])) + img_result.get('issues', [])

    final_score = max(0, min(100, final_score))
    if final_score >= 70:
        verdict = 'correct'
    elif final_score >= 50:
        verdict = 'partially_correct'
    else:
        verdict = 'incorrect'

    return {
        'score': final_score,
        'verdict': verdict,
        'feedback': ' '.join(feedback_parts),
        'issues': all_issues,
        'suggestions': result.get('suggestions', []),
        'image_score': img_result['score'],
        'text_score': text_score,
        'images_found': img_result['found'],
    }


def analyze_code_quality(code: str) -> dict:
    """Анализирует качество Python кода через AST."""
    issues = []
    suggestions = []
    score = 100

    try:
        tree = _ast.parse(code)
    except SyntaxError as e:
        return {
            "score": 0,
            "issues": [f"Синтаксическая ошибка: {e}"],
            "suggestions": ["Исправьте синтаксические ошибки перед отправкой"],
            "passed": False,
        }

    # Проверка 1: Есть ли функции (хороший стиль)
    functions = [n for n in _ast.walk(tree) if isinstance(n, _ast.FunctionDef)]
    if not functions and len(code) > 200:
        issues.append("Код не разбит на функции")
        suggestions.append("Разбейте код на функции для лучшей читаемости")
        score -= 10

    # Проверка 2: Есть ли комментарии
    if "#" not in code and len(code) > 100:
        issues.append("Нет комментариев в коде")
        suggestions.append("Добавьте комментарии для пояснения логики")
        score -= 5

    # Проверка 3: Имена переменных (не одиночные буквы, кроме i, j, k, n, x, y)
    ok_single = {"i", "j", "k", "n", "x", "y", "a", "b", "c", "s"}
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Name) and isinstance(node.ctx, _ast.Store):
            if len(node.id) == 1 and node.id not in ok_single:
                issues.append(f"Однобуквенное имя переменной: '{node.id}'")
                score -= 3
                break

    # Проверка 4: Глобальные переменные
    globals_count = sum(1 for n in _ast.walk(tree) if isinstance(n, _ast.Global))
    if globals_count > 0:
        issues.append(f"Используются глобальные переменные ({globals_count} раз)")
        suggestions.append("Избегайте global — передавайте данные через параметры")
        score -= 5

    # Проверка 5: Вложенность
    max_depth = _get_max_depth(tree)
    if max_depth > 5:
        issues.append(f"Глубокая вложенность кода: {max_depth} уровней")
        suggestions.append("Уменьшите вложенность — разбейте на функции")
        score -= 10

    score = max(0, score)
    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "passed": score >= 60,
        "functions_count": len(functions),
        "lines_count": len(code.splitlines()),
        "max_depth": max_depth,
    }


def _get_max_depth(tree, depth=0):
    """Определяет максимальную глубину вложенности AST."""
    max_d = depth
    for child in _ast.iter_child_nodes(tree):
        if isinstance(child, (_ast.If, _ast.For, _ast.While, _ast.With, _ast.Try,
                               _ast.FunctionDef, _ast.ClassDef)):
            max_d = max(max_d, _get_max_depth(child, depth + 1))
    return max_d


def check_solution_with_tests(code: str, work_order: int) -> dict:
    """Проверяет код против тест-кейсов из auto_tests.json."""
    from works.code_runner import run_python_code

    tests_path = os.path.join(
        os.path.dirname(__file__), "test_data", "auto_tests.json"
    )
    if not os.path.exists(tests_path):
        return {"score": None, "status": "no_tests", "passed": 0, "total": 0}

    with open(tests_path, encoding="utf-8") as f:
        all_tests = json.load(f)

    work_tests = all_tests.get(str(work_order), [])
    if not work_tests:
        return {"score": None, "status": "no_tests", "passed": 0, "total": 0}

    passed = 0
    results = []
    for test in work_tests:
        result = run_python_code(code, input_data=test["input"])
        actual = (result.get("output") or "").strip()
        expected = test["expected"].strip()
        ok = expected in actual or actual == expected
        if ok:
            passed += 1
        results.append({
            "input": test["input"],
            "expected": expected,
            "actual": actual[:200],
            "passed": ok,
        })

    total = len(work_tests)
    score = round(passed * 100 / total) if total else 0
    return {
        "score": score,
        "status": "correct" if score >= 70 else "partially_correct" if score >= 40 else "incorrect",
        "passed": passed,
        "total": total,
        "results": results,
    }


class AICodeChecker:
    """Запускает автопроверку решения и сохраняет результат в CodeCheck."""

    def check_solution(self, solution_id: int, code_check_id: int) -> None:
        from django.utils import timezone
        from works.models import Solution, CodeCheck

        try:
            solution = Solution.objects.get(id=solution_id)
            code_check = CodeCheck.objects.get(id=code_check_id)
        except Exception:
            return

        try:
            file_path = solution.code_file.path
            ext = os.path.splitext(file_path)[1].lower()

            # ── Ветка: отчёт (docx/pdf) — проверяем как документ ──────────────
            if ext in ('.docx', '.pdf'):
                report_text = extract_text_from_file(file_path)
                if not report_text.strip():
                    raise ValueError('Не удалось извлечь текст из файла отчёта')

                work_description = getattr(solution.work, 'description', '') or ''
                ai_result = ai_review_report(report_text, solution.work.title, work_description, file_path=file_path)

                if ai_result:
                    final_score = ai_result['score']
                    verdict = ai_result['verdict']
                    feedback = ai_result.get('feedback', '')
                    issues = ai_result.get('issues', [])
                    suggestions = ai_result.get('suggestions', [])
                    meta = {
                        'text_score': ai_result.get('text_score', 0),
                        'image_score': ai_result.get('image_score', 0),
                        'images_found': ai_result.get('images_found', 0),
                    }
                else:
                    # Ollama недоступна — ставим "на ручную проверку"
                    final_score = 0
                    verdict = 'pending'
                    feedback = 'ИИ недоступен. Отчёт ожидает ручной проверки преподавателем.'
                    issues = []
                    suggestions = []
                    meta = {}

                code_check.status = 'completed'
                code_check.score = final_score
                code_check.feedback = feedback
                code_check.suggestions = suggestions
                code_check.errors = issues
                code_check.warnings = [meta] if meta else []
                code_check.completed_at = timezone.now()
                code_check.save()

                solution.status = verdict
                solution.score = final_score
                solution.save()
                return

            # ── Ветка: код (py, cpp, js …) ────────────────────────────────────
            with open(file_path, encoding='utf-8', errors='replace') as f:
                code = f.read()

            lang_map = {'py': 'python', 'cpp': 'c++', 'c': 'c', 'java': 'java',
                        'js': 'javascript', 'kt': 'kotlin', 'ino': 'arduino'}
            language = lang_map.get(ext.lstrip('.'), ext.lstrip('.') or 'python')

            # 1. Прогон против тест-кейсов из auto_tests.json (только Python)
            tests = check_solution_with_tests(code, solution.work.order)

            # 2. Если нет готовых тестов и код на Python — ИИ генерирует входные данные и запускает
            ai_run_results = []
            if language == 'python' and tests['status'] == 'no_tests' and 'input(' in code:
                from works.code_runner import run_python_code
                generated_inputs = ai_generate_test_inputs(code, solution.work.title)
                for inp in generated_inputs[:3]:
                    r = run_python_code(code, input_data=inp)
                    ai_run_results.append({
                        'input': inp,
                        'output': (r.get('output') or '').strip(),
                        'error': (r.get('error') or '').strip(),
                    })

            # 3. Ollama ИИ-проверка с реальными результатами запуска
            ai_result = ai_review_code(
                code, solution.work.title, language,
                run_results=ai_run_results or None,
            )

            # 3. AST-анализ (fallback или дополнение)
            quality = analyze_code_quality(code) if language == 'python' else {
                'score': 70, 'issues': [], 'suggestions': [], 'passed': True,
            }

            # Итоговая оценка
            if ai_result:
                # GigaChat доступен — его оценка главная
                ai_score = ai_result['score']
                if tests['status'] != 'no_tests':
                    # Комбинируем: 50% тесты + 50% ИИ
                    final_score = round(tests['score'] * 0.5 + ai_score * 0.5)
                else:
                    final_score = ai_score
                verdict = ai_result['verdict']
                feedback_lines = []
                if ai_result.get('feedback'):
                    feedback_lines.append(f"ИИ-оценка: {ai_result['feedback']}")
                if ai_run_results:
                    ok = sum(1 for r in ai_run_results if not r['error'])
                    feedback_lines.append(
                        f"Запуски с ИИ-данными: {ok}/{len(ai_run_results)} без ошибок"
                    )
                if tests['status'] != 'no_tests':
                    feedback_lines.append(
                        f"Тесты: {tests['passed']}/{tests['total']} пройдено ({tests['score']}%)"
                    )
                issues = ai_result.get('issues', [])
                suggestions = ai_result.get('suggestions', [])
            elif tests['status'] != 'no_tests':
                # Только тесты + AST
                final_score = round(tests['score'] * 0.6 + quality['score'] * 0.4)
                verdict = tests['status']
                feedback_lines = [f"Тесты: {tests['passed']}/{tests['total']} пройдено ({tests['score']}%)"]
                if quality['issues']:
                    feedback_lines.append("Замечания: " + "; ".join(quality['issues']))
                issues = quality['issues']
                suggestions = quality['suggestions']
            else:
                # Только AST
                final_score = quality['score']
                verdict = 'correct' if quality['passed'] else 'incorrect'
                feedback_lines = []
                if quality['issues']:
                    feedback_lines.append("Замечания: " + "; ".join(quality['issues']))
                issues = quality['issues']
                suggestions = quality['suggestions']

            code_check.status = 'completed'
            code_check.score = final_score
            code_check.feedback = "\n".join(feedback_lines) or "Проверка завершена."
            code_check.suggestions = suggestions
            code_check.errors = issues
            code_check.warnings = []
            code_check.completed_at = timezone.now()
            code_check.save()

            # Обновляем статус самого решения
            solution.status = verdict
            solution.score = final_score
            if tests['status'] != 'no_tests':
                solution.test_results = {
                    'tests': tests.get('results', []),
                    'passed': tests['passed'],
                    'total': tests['total'],
                }
            elif ai_run_results:
                solution.test_results = {
                    'tests': ai_run_results,
                    'passed': sum(1 for r in ai_run_results if not r['error']),
                    'total': len(ai_run_results),
                    'source': 'ai_generated',
                }
            solution.save()

        except Exception as e:
            try:
                code_check.status = 'failed'
                code_check.feedback = f"Ошибка проверки: {e}"
                code_check.completed_at = timezone.now()
                code_check.save()
            except Exception:
                pass
