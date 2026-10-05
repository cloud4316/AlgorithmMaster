"""
Детектор схожести кода между решениями студентов.
Алгоритм: нормализация (AST для Python, токены для остальных) + SequenceMatcher.
"""
import ast
import re
import tokenize
import io
import difflib
import logging
from typing import NamedTuple

logger = logging.getLogger(__name__)

# Встроенные имена Python — не переименовываем
_BUILTINS = frozenset(dir(__builtins__) if isinstance(__builtins__, dict) else dir(__builtins__))
_KEYWORDS = frozenset([
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield', 'print', 'input', 'range', 'len', 'int',
    'str', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'type',
    'open', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'reversed',
    'sum', 'min', 'max', 'abs', 'round', 'isinstance', 'hasattr',
    'getattr', 'setattr', 'append', 'extend', 'insert', 'remove', 'pop',
    'keys', 'values', 'items', 'get', 'update', 'split', 'join', 'strip',
    'upper', 'lower', 'format', 'replace', 'find', 'count', 'index',
])
_SKIP_NAMES = _BUILTINS | _KEYWORDS


class _Renamer(ast.NodeTransformer):
    def __init__(self):
        self._map: dict[str, str] = {}
        self._counter = 0

    def _rename(self, name: str) -> str:
        if name in _SKIP_NAMES:
            return name
        if name not in self._map:
            self._map[name] = f'x{self._counter}'
            self._counter += 1
        return self._map[name]

    def visit_Name(self, node):
        node.id = self._rename(node.id)
        return node

    def visit_FunctionDef(self, node):
        node.name = self._rename(node.name)
        self.generic_visit(node)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        node.name = self._rename(node.name)
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        node.arg = self._rename(node.arg)
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node.value = 'S'
        elif isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            node.value = 0
        return node


def _normalize_python(code: str) -> str:
    """AST-нормализация Python: переименовать идентификаторы, заменить константы."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return _normalize_text(code)
    renamer = _Renamer()
    try:
        new_tree = renamer.visit(tree)
        ast.fix_missing_locations(new_tree)
        return ast.unparse(new_tree)
    except Exception:
        return _normalize_text(code)


def _normalize_text(code: str) -> str:
    """Текстовая нормализация для не-Python кода: убрать комментарии, схлопнуть пробелы."""
    # Убираем // ... и /* ... */ комментарии
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Убираем # ... комментарии
    code = re.sub(r'#[^\n]*', '', code)
    # Нормализуем строковые литералы
    code = re.sub(r'"[^"]*"', '"S"', code)
    code = re.sub(r"'[^']*'", "'S'", code)
    # Нормализуем числа
    code = re.sub(r'\b\d+\.?\d*\b', '0', code)
    # Схлопнуть пробелы
    code = re.sub(r'\s+', ' ', code).strip()
    return code


def normalize(code: str, lang: str = 'python') -> str:
    if not code or not code.strip():
        return ''
    if lang == 'python':
        return _normalize_python(code)
    return _normalize_text(code)


def similarity(code_a: str, code_b: str, lang: str = 'python') -> float:
    """Возвращает схожесть 0.0..1.0 между двумя кодами."""
    na = normalize(code_a, lang)
    nb = normalize(code_b, lang)
    if not na or not nb:
        return 0.0
    return difflib.SequenceMatcher(None, na, nb, autojunk=False).ratio()


class Match(NamedTuple):
    solution_id: int
    student_name: str
    score: float          # 0..100
    work_title: str


def check_solution(solution) -> list[Match]:
    """
    Сравнивает решение со всеми другими решениями той же работы.
    Возвращает список Match отсортированный по убыванию схожести.
    Учитывает только последнюю попытку каждого студента.
    """
    from works.models import Solution
    import os

    # Читаем код текущего решения
    try:
        with solution.code_file.open('rb') as f:
            my_code = f.read().decode('utf-8', errors='replace')
    except Exception as e:
        logger.warning('plagiarism: cannot read solution %s: %s', solution.id, e)
        return []

    if not my_code.strip():
        return []

    # Определяем язык по расширению
    ext = os.path.splitext(solution.code_file.name)[1].lower()
    lang_map = {'.py': 'python', '.cpp': 'cpp', '.c': 'cpp',
                '.java': 'java', '.js': 'javascript'}
    lang = lang_map.get(ext, 'python')

    # Берём все решения той же работы, кроме текущего студента
    others = (
        Solution.objects
        .filter(work=solution.work)
        .exclude(student=solution.student)
        .select_related('student')
        .order_by('student_id', '-submitted_at')
    )

    # Группируем: одна (последняя) попытка на студента
    seen_students: set[int] = set()
    unique: list = []
    for s in others:
        if s.student_id not in seen_students:
            seen_students.add(s.student_id)
            unique.append(s)

    matches: list[Match] = []
    for other in unique:
        try:
            with other.code_file.open('rb') as f:
                other_code = f.read().decode('utf-8', errors='replace')
        except Exception:
            continue
        if not other_code.strip():
            continue

        score = similarity(my_code, other_code, lang) * 100
        if score >= 40:   # порог: ниже 40% не интересно
            matches.append(Match(
                solution_id=other.id,
                student_name=f'{other.student.last_name} {other.student.first_name}',
                score=round(score, 1),
                work_title=other.work.title,
            ))

    matches.sort(key=lambda m: m.score, reverse=True)
    return matches
