# -*- coding: utf-8 -*-
"""
Расширение тонких уроков Python реальными кейсами, диаграммами и практикой.
Запуск: python manage.py seed_python_enrich
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject

# ─── helpers ──────────────────────────────────────────────────────────────────
def tip(t): return f'<div class="tip">💡 {t}</div>'
def warn(t): return f'<div class="warning">⚠️ {t}</div>'
def info(t): return f'<div class="info">ℹ️ {t}</div>'

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def code(lang, src):
    return f'<pre><code class="language-{lang}">{src}</code></pre>'

def svg_box(x, y, w, h, fill, stroke, label, fs=12, tc='#1e293b'):
    lh = fs + 4
    lines = label.split('\n')
    y0 = y + h//2 - (lh*len(lines))//2 + fs
    spans = ''.join(f'<tspan x="{x+w//2}" dy="{0 if i==0 else lh}">{l}</tspan>'
                    for i, l in enumerate(lines))
    r = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    t = (f'<text x="{x+w//2}" y="{y0}" text-anchor="middle" font-size="{fs}" '
         f'fill="{tc}" font-family="sans-serif">{spans}</text>')
    return r + t

DEFS = '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'

def arr(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="1.5" marker-end="url(#a)"/>'

def diagram(inner, w=640, h=220, cap=''):
    return (f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;border-radius:12px;'
            f'filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">{inner}</svg>'
            f'<p style="text-align:center;color:#64748b;font-size:13px">{cap}</p></div>')

def bg(w, h, title):
    return (f'<rect width="{w}" height="{h}" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'
            f'<text x="{w//2}" y="24" text-anchor="middle" font-size="13" fill="#1e293b" '
            f'font-weight="bold" font-family="sans-serif">{title}</text>')

# ═══════════════════════════════════════════════════════════════════════════════
# Контент по урокам
# ═══════════════════════════════════════════════════════════════════════════════

# ── M2L1: Переменные ──────────────────────────────────────────────────────────
M2L1 = '''
<h2>Переменная — это ярлык, а не ящик</h2>
<p>В отличие от C/Java, переменная в Python — это <strong>имя, которое указывает на объект в памяти</strong>.
Один объект может иметь несколько имён, а имя в любой момент можно «переклеить» на другой объект.</p>
''' + diagram(
    DEFS + bg(640, 200, 'Переменная в Python: имя → объект в памяти') +
    svg_box(20, 50, 120, 40, '#dbeafe', '#3b82f6', 'Стек имён', 11, '#1e40af') +
    svg_box(20, 110, 120, 40, '(имя)', '#3b82f6', 'x', 13, '#1e40af') +
    svg_box(20, 160, 120, 40, '(имя)', '#3b82f6', 'y', 13, '#1e40af') +
    arr(140, 130, 250, 130) +
    arr(140, 180, 250, 130) +
    svg_box(250, 100, 180, 60, '#dcfce7', '#16a34a', 'Объект int\n42\nid=0x7f...', 11, '#14532d') +
    svg_box(460, 100, 160, 60, '#fef3c7', '#f59e0b', 'После: x = 99\nновый объект\nстарый не тронут', 10, '#92400e'),
    640, 200, 'x = 42; y = x  →  оба имени смотрят на один объект 42'
) + code('python', '''x = 42
y = x         # y тоже указывает на 42
print(id(x) == id(y))   # True — один объект!

x = 99        # x переклеен на новый объект
print(y)      # 42 — y не изменился

# Реальный кейс: баг в командах игры
score = 0
best = score   # best тоже 0, НЕ копия
score += 100   # int неизменяем → создаётся новый объект
print(best)    # 0 — всё верно для int

# Опасность со списками (изменяемые объекты):
a = [1, 2, 3]
b = a          # b смотрит на ТОТ ЖЕ список
b.append(4)
print(a)       # [1, 2, 3, 4] — сюрприз!''') + tip(
    'Неизменяемые типы (int, str, tuple) безопасны при присваивании. '
    'Изменяемые (list, dict) нужно копировать явно: <code>b = a.copy()</code>.'
) + '''
<h3>Кейс из жизни: NASA Mars Climate Orbiter (1999)</h3>
<p>Зонд стоимостью $327 млн сгорел в атмосфере Марса. Причина: одна команда передавала
данные <strong>в фунто-секундах</strong>, другая ожидала <strong>ньютон-секунды</strong>.
Переменная имела одно имя, но разный смысл в разных частях кода. Урок: <strong>называй
переменные ясно</strong> — <code>thrust_newton_seconds</code>, а не просто <code>thrust</code>.</p>
''' + table(
    ['Плохое имя', 'Хорошее имя', 'Почему'],
    [
        ('d', 'distance_km', 'Сразу ясны единицы'),
        ('t', 'timeout_seconds', 'Нет путаницы мс/с/мин'),
        ('flag', 'is_user_authenticated', 'bool-переменная начинается с is_/has_/can_'),
        ('data', 'raw_json_response', 'Видно откуда и в каком формате'),
        ('temp', 'temperature_celsius', 'Не путаем с "temporary"'),
    ]
) + tip('Правило: если через полгода незнакомый человек (или ты сам) не поймёт имя переменной — переименуй.')

# ── M2L2: int, float ──────────────────────────────────────────────────────────
M2L2 = '''
<h2>Числа в реальном коде: ловушки и трюки</h2>
<h3>Целочисленное деление и остаток</h3>
<p>Операторы <code>//</code> и <code>%</code> используются повсюду — в играх, банках, расписаниях.</p>
''' + code('python', '''# Кейс: разбить 100 монет между 7 игроками
coins = 100
players = 7
each = coins // players    # 14 монет каждому
leftover = coins % players  # 2 монеты в банк
print(f"Каждый получает {each}, остаток {leftover}")

# Кейс: часы → часы:минуты
total_minutes = 137
hours   = total_minutes // 60   # 2
minutes = total_minutes % 60    # 17
print(f"{hours}ч {minutes}мин")

# Кейс: каждый N-й элемент (логи, пагинация)
for i in range(20):
    if i % 5 == 0:
        print(f"Сохраняем checkpoint на шаге {i}")''') + '''
<h3>Проблема float: когда 0.1 + 0.2 ≠ 0.3</h3>
''' + code('python', '''print(0.1 + 0.2)          # 0.30000000000000004 — не баг, стандарт IEEE 754!
print(0.1 + 0.2 == 0.3)   # False

# Кейс: банковское ПО Knight Capital (2012)
# Потеряли $440 млн за 45 минут из-за ошибки округления float в торговой системе.
# Правильное решение для денег:
from decimal import Decimal
price = Decimal("0.1") + Decimal("0.2")
print(price)              # 0.3 — точно!

# Для сравнения float используй math.isclose:
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True''') + warn(
    'Никогда не используй <code>float</code> для хранения денег! '
    'Используй <code>decimal.Decimal</code> или храни суммы в копейках/центах как <code>int</code>.'
) + table(
    ['Тип', 'Диапазон/точность', 'Применение', 'Пример'],
    [
        ('int', 'Неограничен (bignum)', 'Счётчики, индексы, деньги в копейках', '100_000_000'),
        ('float', '~15 значимых цифр, IEEE 754', 'Физика, ML, координаты', '3.14159'),
        ('Decimal', 'Настраиваемая точность', 'Финансы, бухгалтерия', "Decimal('9.99')"),
        ('complex', 'a + bj', 'Сигналы, FFT, квантовые симуляции', '3+4j'),
    ]
) + tip('Python автоматически переключается на <code>bignum</code>: <code>2**1000</code> — работает без переполнения, в отличие от C/Java.')

# ── M2L3: str и input() ───────────────────────────────────────────────────────
M2L3 = '''
<h2>Строки: больше чем просто текст</h2>
<p>Строки в Python — <strong>неизменяемые</strong> последовательности Unicode-символов.
Это означает, что каждая «модификация» создаёт новый объект.</p>
''' + code('python', '''# f-строки (Python 3.6+) — лучший способ форматирования
name = "Алиса"
score = 1337
print(f"Игрок {name}, очки: {score:,}")   # "Игрок Алиса, очки: 1,337"
print(f"PI ≈ {3.14159:.2f}")              # "PI ≈ 3.14"
print(f"{'OK':>10}")                       # выравнивание вправо

# Кейс: безопасная обработка ввода пользователя
raw = input("Введи возраст: ").strip()
if raw.isdigit():
    age = int(raw)
    print(f"Через 10 лет тебе будет {age + 10}")
else:
    print("Это не число!")

# Кейс: парсинг CSV-строки вручную
line = "  Иванов,  Иван,   25   "
parts = [p.strip() for p in line.split(",")]
print(parts)  # ["Иванов", "Иван", "25"]''') + '''
<h3>Реальный баг: SQL-инъекция через конкатенацию строк</h3>
''' + code('python', '''# ❌ ОПАСНО — так делать нельзя никогда:
user_input = "'; DROP TABLE users; --"
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
# query = "SELECT * FROM users WHERE name = ''; DROP TABLE users; --'"
# Злоумышленник удалил всю таблицу!

# ✅ Правильно — параметризованные запросы:
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
# Библиотека экранирует ввод автоматически''') + warn(
    'SQL-инъекция входит в топ-1 OWASP уже более 15 лет. В 2017 утечка Equifax (143 млн человек) '
    'произошла частично из-за небезопасной обработки строк пользовательского ввода.'
) + table(
    ['Метод', 'Скорость', 'Читаемость', 'Когда использовать'],
    [
        ('f"..."', '★★★★★', '★★★★★', 'Python 3.6+, почти всегда'),
        ('"".format()', '★★★★', '★★★★', 'Шаблоны, совместимость с 2.7'),
        ('% форматирование', '★★★', '★★★', 'Логирование, legacy-код'),
        ('+ конкатенация', '★ (в цикле)', '★★', 'Никогда в цикле — O(n²)!'),
        ('"".join(list)', '★★★★★', '★★★', 'Сборка строки в цикле'),
    ]
)

# ── M2L4: bool и сравнения ────────────────────────────────────────────────────
M2L4 = '''
<h2>Истина и ложь в Python: нюансы, о которых молчат учебники</h2>
<h3>Что считается ложью (Falsy)?</h3>
''' + code('python', '''# Falsy-значения — всё, что bool() превращает в False:
falsy = [0, 0.0, 0j, "", [], {}, (), set(), None, False]
for v in falsy:
    print(f"bool({v!r:10}) = {bool(v)}")

# Типичный баг начинающих:
count = 0
if count:        # ← False! Даже если count существует
    print("Есть данные")
# Правильно:
if count is not None:   # явная проверка на None
    print(f"Данных: {count}")  # напечатает даже 0''') + '''
<h3>is vs ==: знаменитый баг Python</h3>
''' + code('python', '''# == сравнивает значения
# is  сравнивает объекты (один ли объект в памяти)

a = 1000
b = 1000
print(a == b)   # True (значения равны)
print(a is b)   # False (разные объекты) — НО!

a = 10
b = 10
print(a is b)   # True — Python кэширует int от -5 до 256!

# Кейс: баг в продакшне
def get_status():
    return None  # API вернул ошибку

status = get_status()
if status == None:    # ❌ работает, но не pythonic
    print("Ошибка")
if status is None:    # ✅ правильно: None — синглтон
    print("Ошибка")''') + tip(
    '<code>is None</code> и <code>is not None</code> — единственные правильные способы проверки на None. '
    'Никогда не пиши <code>== None</code>.'
) + '''
<h3>Короткое замыкание (short-circuit): оптимизация и баги</h3>
''' + code('python', '''# and возвращает первое ложное или последнее значение
# or  возвращает первое истинное или последнее значение
print(0 and 1/0)      # 0 — деление не вычисляется!
print(1 or 1/0)       # 1 — деление не вычисляется!

# Кейс: безопасное получение значения по умолчанию
config = {}
timeout = config.get("timeout") or 30   # если None или 0 → 30
# Но осторожно с нулём!
port = config.get("port") or 80         # если port=0 → 80 (баг!)
port = config.get("port") if config.get("port") is not None else 80  # правильно

# Кейс: однострочная инициализация
name = input("Имя: ").strip() or "Аноним"  # пустой ввод → "Аноним"
print(f"Привет, {name}!")''') + table(
    ['Выражение', 'Результат', 'Почему'],
    [
        ('True and "hello"', '"hello"', 'and возвращает последнее если всё True'),
        ('False and "hello"', 'False', 'Короткое замыкание на False'),
        ('None or "default"', '"default"', 'or возвращает первое True'),
        ('0 or [] or "ok"', '"ok"', 'Пропускает все Falsy'),
        ('"" or 0 or None', 'None', 'Возвращает последнее если всё Falsy'),
    ]
)

# ── M12L1: Файлы ──────────────────────────────────────────────────────────────
M12 = '''
<h2>Файлы в реальных проектах: паттерны и ловушки</h2>
<p>Работа с файлами — одна из самых частых задач: логи, конфиги, отчёты, обмен данными.
Ошибки здесь могут стоить дорого — от потери данных до утечки персональных сведений.</p>
''' + code('python', '''# ✅ Всегда используй контекстный менеджер with
# Он гарантирует закрытие файла даже при исключении

# Кейс 1: Атомарная запись (избегаем повреждённых файлов)
import os, tempfile

def safe_write(path, content):
    """Записываем во временный файл, потом атомарно переименовываем."""
    dir_ = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile("w", dir=dir_, delete=False,
                                     encoding="utf-8", suffix=".tmp") as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    os.replace(tmp_path, path)  # атомарная операция на Linux/Windows

# Кейс 2: Обработка большого файла построчно (не грузим всё в RAM)
def count_errors(log_path):
    errors = 0
    with open(log_path, encoding="utf-8") as f:
        for line in f:           # итерация, не readlines()!
            if "ERROR" in line:
                errors += 1
    return errors

# Кейс 3: Append-only лог (не перезаписываем, добавляем)
import datetime
def write_log(message):
    ts = datetime.datetime.now().isoformat()
    with open("app.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\\n")''') + warn(
    'В 2017 году облачный сервис GitLab потерял данные 300 000 пользователей: '
    'администратор запустил <code>rm -rf</code> не в той директории. '
    'Урок: всегда делай атомарные операции и храни бэкапы.'
) + table(
    ['Режим', 'Файл существует', 'Файл НЕ существует', 'Типичное применение'],
    [
        ("'r'", 'Читаем', 'FileNotFoundError', 'Чтение конфига, данных'),
        ("'w'", 'ПЕРЕЗАПИСЫВАЕМ', 'Создаём', 'Генерация отчёта'),
        ("'a'", 'Добавляем в конец', 'Создаём', 'Логирование'),
        ("'x'", 'FileExistsError', 'Создаём', 'Безопасное создание'),
        ("'r+'", 'Читаем и пишем', 'FileNotFoundError', 'Редактирование'),
        ("'rb'/'wb'", 'Бинарный режим', '—', 'Изображения, zip'),
    ]
) + code('python', '''# Кейс 4: Работа с путями (pathlib — современный способ)
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)   # создать папку если нет

# Безопасная работа с путями (защита от path traversal):
def read_user_file(filename: str) -> str:
    safe_dir = Path("uploads").resolve()
    file_path = (safe_dir / filename).resolve()
    if not str(file_path).startswith(str(safe_dir)):
        raise PermissionError("Доступ за пределы директории запрещён!")
    return file_path.read_text(encoding="utf-8")

# Найти все .py файлы рекурсивно:
py_files = list(Path(".").rglob("*.py"))
print(f"Python файлов: {len(py_files)}")''') + tip(
    'Используй <code>pathlib.Path</code> вместо <code>os.path</code> — '
    'код читабельнее, работает кроссплатформенно, есть удобные методы: '
    '<code>.read_text()</code>, <code>.write_text()</code>, <code>.exists()</code>.'
)

# ── M18L1: Поиск (бинарный, линейный) ────────────────────────────────────────
M18 = '''
<h2>Поиск в реальных системах: от списка до миллиардов записей</h2>
''' + diagram(
    DEFS + bg(640, 190, 'Линейный vs Бинарный поиск (n = 1 000 000)') +
    svg_box(30, 50, 260, 50, '#fee2e2', '#ef4444', 'Линейный O(n)\nДо 1 000 000 шагов', 11, '#7f1d1d') +
    svg_box(350, 50, 260, 50, '#dcfce7', '#16a34a', 'Бинарный O(log n)\nМаксимум 20 шагов!', 11, '#14532d') +
    arr(160, 115, 160, 145) + arr(480, 115, 480, 145) +
    svg_box(30, 145, 260, 35, '#fef3c7', '#f59e0b', 'Применимо к любому массиву', 10, '#92400e') +
    svg_box(350, 145, 260, 35, '#dbeafe', '#3b82f6', 'Только отсортированный массив!', 10, '#1e40af'),
    640, 190, 'log₂(1 000 000) ≈ 20 — бинарный поиск делает максимум 20 проверок из миллиона'
) + code('python', '''import bisect, time

# Линейный поиск — O(n)
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Бинарный поиск — O(log n) — только для отсортированного!
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Сравнение скорости
import random
data = sorted(random.randint(0, 10**9) for _ in range(10**6))
target = data[500_000]

t0 = time.perf_counter()
linear_search(data, target)
print(f"Линейный: {(time.perf_counter()-t0)*1000:.1f} мс")

t0 = time.perf_counter()
binary_search(data, target)
print(f"Бинарный: {(time.perf_counter()-t0)*1000:.3f} мс")

# В Python есть встроенный бинарный поиск через bisect:
idx = bisect.bisect_left(data, target)
print(f"bisect: индекс {idx}, значение {data[idx]}")''') + '''
<h3>Как поиск работает в реальных системах</h3>
''' + table(
    ['Система', 'Структура', 'Алгоритм поиска', 'Сложность'],
    [
        ('Python dict/set', 'Хеш-таблица', 'O(1) средний', 'lookup мгновенный'),
        ('PostgreSQL индекс', 'B-Tree', 'O(log n)', 'миллиарды строк за мс'),
        ('Git история', 'DAG', 'Обход графа BFS/DFS', 'O(n) коммитов'),
        ('Google Search', 'Инвертированный индекс', 'TF-IDF + BFS', 'трилл. страниц'),
        ('DNS lookup', 'Дерево доменов', 'O(уровней)', 'глубина ≤ 127'),
    ]
) + tip(
    'Знаменитая история: в 2015 году Facebook ускорил поиск по 1.5 млрд профилей, '
    'добавив многоуровневый индекс. Запросы к «Социальному графу» выполняются за &lt;10 мс. '
    'Секрет: никакого линейного поиска — только хеш-таблицы и B-деревья.'
)

# ── M32L1: GIL и потоки ───────────────────────────────────────────────────────
M32 = '''
<h2>GIL на практике: когда потоки помогают, а когда мешают</h2>
''' + diagram(
    DEFS + bg(640, 200, 'GIL: CPU-bound vs IO-bound задачи') +
    svg_box(20, 40, 280, 140, '#fee2e2', '#ef4444', '', 11, '#7f1d1d') +
    '<text x="160" y="65" text-anchor="middle" font-size="11" fill="#7f1d1d" font-weight="bold" font-family="sans-serif">CPU-bound (GIL мешает)</text>' +
    '<text x="160" y="85" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">Thread1: [===GIL===][wait][===GIL===]</text>' +
    '<text x="160" y="105" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">Thread2: [wait][===GIL===][wait]</text>' +
    '<text x="160" y="130" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">Хуже одного потока из-за</text>' +
    '<text x="160" y="148" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">overhead переключений!</text>' +
    svg_box(340, 40, 280, 140, '#dcfce7', '#16a34a', '', 11, '#14532d') +
    '<text x="480" y="65" text-anchor="middle" font-size="11" fill="#14532d" font-weight="bold" font-family="sans-serif">IO-bound (потоки помогают)</text>' +
    '<text x="480" y="85" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Thread1: [run][ IO wait    ][run]</text>' +
    '<text x="480" y="105" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Thread2:      [run][IO][run]</text>' +
    '<text x="480" y="130" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Во время IO другие потоки</text>' +
    '<text x="480" y="148" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">работают параллельно!</text>',
    640, 200, 'GIL освобождается во время IO — поэтому потоки полезны для сетевых запросов'
) + code('python', '''import threading, time, requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Кейс 1: IO-bound — потоки ускоряют в 10x
urls = [f"https://httpbin.org/delay/1" for _ in range(5)]

# Последовательно: ~5 секунд
t0 = time.perf_counter()
# results = [requests.get(u).status_code for u in urls]
# print(f"Последовательно: {time.perf_counter()-t0:.1f}s")

# Параллельно (потоки): ~1 секунда
with ThreadPoolExecutor(max_workers=5) as ex:
    futures = [ex.submit(requests.get, u) for u in urls]
    results = [f.result().status_code for f in futures]
print(f"Потоки: {time.perf_counter()-t0:.1f}s  ← ускорение в 5x!")

# Кейс 2: CPU-bound — процессы (обходят GIL)
def cpu_task(n):
    return sum(i*i for i in range(n))

with ProcessPoolExecutor() as ex:
    results = list(ex.map(cpu_task, [10**7]*4))

# Кейс 3: Race condition — классический баг
counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1  # НЕ атомарная операция!

threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)  # Ожидаем 200000, но получаем меньше!''') + warn(
    'Amazon в 2012 году получил известный race condition в системе заказов: '
    'из-за параллельных потоков один товар можно было купить дважды, '
    'уменьшая остаток на складе в обход проверки. Убытки — тысячи долларов. '
    'Решение: <code>threading.Lock()</code> или атомарные операции БД.'
) + table(
    ['Задача', 'Рекомендация', 'Почему'],
    [
        ('HTTP-запросы, API', 'threading или asyncio', 'IO-bound, GIL освобождается'),
        ('Обработка изображений', 'multiprocessing', 'CPU-bound, нужны реальные ядра'),
        ('ML/NumPy вычисления', 'Уже параллельно', 'NumPy освобождает GIL'),
        ('Парсинг сайтов', 'asyncio + aiohttp', '1000+ сайтов одновременно'),
        ('Видеокодирование', 'multiprocessing', 'CPU-bound, тяжёлые вычисления'),
    ]
)

# ── M36L1: pytest ─────────────────────────────────────────────────────────────
M36 = '''
<h2>Тестирование: почему это не скучно и как это спасает деньги</h2>
<p>В 2021 году баг в коде Robinhood заблокировал торги для миллионов пользователей
в самый активный день. Простой тест мог это предотвратить.</p>
''' + code('python', '''# Реальный кейс: функция расчёта скидки
def apply_discount(price: float, discount_pct: float) -> float:
    """Применяет скидку в % к цене. Возвращает итоговую цену."""
    if not 0 <= discount_pct <= 100:
        raise ValueError(f"Скидка {discount_pct}% вне диапазона 0-100")
    return round(price * (1 - discount_pct / 100), 2)

# test_discount.py — запуск: pytest test_discount.py -v
import pytest

class TestApplyDiscount:
    def test_no_discount(self):
        assert apply_discount(100.0, 0) == 100.0

    def test_full_discount(self):
        assert apply_discount(100.0, 100) == 0.0

    def test_partial_discount(self):
        assert apply_discount(200.0, 25) == 150.0

    def test_rounding(self):
        # 10.99 * 0.9 = 9.891 → должно округлиться до 9.89
        assert apply_discount(10.99, 10) == 9.89

    def test_invalid_negative(self):
        with pytest.raises(ValueError, match="вне диапазона"):
            apply_discount(100.0, -5)

    def test_invalid_over_100(self):
        with pytest.raises(ValueError):
            apply_discount(100.0, 101)

    @pytest.mark.parametrize("price,pct,expected", [
        (1000, 10, 900.0),
        (50,   50, 25.0),
        (0.01, 0,  0.01),
    ])
    def test_parametrized(self, price, pct, expected):
        assert apply_discount(price, pct) == expected''') + tip(
    'Правило пирамиды тестов: 70% unit-тестов (быстрые, изолированные), '
    '20% интеграционных (реальная БД/API), 10% E2E (браузер). '
    'Не наоборот — E2E тесты медленные и хрупкие.'
) + code('python', '''# Фикстуры — переиспользуемые тестовые данные
import pytest

@pytest.fixture
def sample_cart():
    return {"items": [{"name": "Книга", "price": 500},
                      {"name": "Ручка", "price": 50}]}

def test_cart_total(sample_cart):
    total = sum(i["price"] for i in sample_cart["items"])
    assert total == 550

def test_cart_count(sample_cart):
    assert len(sample_cart["items"]) == 2

# Временные файлы — pytest создаёт и удаляет автоматически:
def test_write_report(tmp_path):
    report = tmp_path / "report.txt"
    report.write_text("Итого: 550 руб.")
    assert report.read_text() == "Итого: 550 руб."''') + table(
    ['Команда', 'Что делает'],
    [
        ('pytest', 'Запустить все тесты'),
        ('pytest -v', 'Подробный вывод'),
        ('pytest -k "discount"', 'Только тесты с "discount" в имени'),
        ('pytest --tb=short', 'Короткий traceback'),
        ('pytest --cov=mymodule', 'Покрытие кода (нужен pytest-cov)'),
        ('pytest -x', 'Стоп после первого падения'),
    ]
)

# ── M40L1: argparse ────────────────────────────────────────────────────────────
M40 = '''
<h2>CLI-инструменты: скрипты, которые используют настоящие разработчики</h2>
<p>Большинство девопс-инструментов, скриптов обработки данных и утилит — это CLI-программы.
<code>argparse</code> — стандарт для Python.</p>
''' + code('python', '''#!/usr/bin/env python3
# resize_images.py — реальный CLI-инструмент
"""Конвертирует изображения в папке с изменением размера."""
import argparse
from pathlib import Path

def build_parser():
    parser = argparse.ArgumentParser(
        description="Пакетная обработка изображений",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir",
                        type=Path,
                        help="Папка с исходными изображениями")
    parser.add_argument("-o", "--output",
                        type=Path, default=Path("output"),
                        help="Папка для результата")
    parser.add_argument("-s", "--size",
                        type=int, nargs=2, default=[800, 600],
                        metavar=("WIDTH", "HEIGHT"),
                        help="Размер в пикселях")
    parser.add_argument("-q", "--quality",
                        type=int, default=85, choices=range(1, 101),
                        metavar="1-100",
                        help="Качество JPEG")
    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Показать что будет сделано, не делать")
    parser.add_argument("-v", "--verbose",
                        action="count", default=0,
                        help="Уровень логирования (-v, -vv, -vvv)")
    return parser

def main():
    args = build_parser().parse_args()

    if args.verbose >= 1:
        print(f"Входная папка: {args.input_dir}")
        print(f"Размер: {args.size[0]}x{args.size[1]}, качество: {args.quality}%")

    images = list(args.input_dir.glob("*.jpg")) + list(args.input_dir.glob("*.png"))
    print(f"Найдено изображений: {len(images)}")

    if args.dry_run:
        for img in images:
            print(f"  [dry-run] {img.name} → {args.output / img.name}")
        return

    args.output.mkdir(exist_ok=True)
    # ... обработка ...

if __name__ == "__main__":
    main()

# Использование:
# python resize_images.py photos/ -o web/ -s 1920 1080 -q 90 -vv
# python resize_images.py photos/ --dry-run''') + tip(
    'Добавляй <code>--dry-run</code> к любому скрипту, который меняет файлы или БД. '
    'Это спасёт тебя от случайного уничтожения данных.'
) + table(
    ['Параметр argparse', 'Что делает', 'Пример'],
    [
        ('positional', 'Обязательный аргумент', 'python script.py input.txt'),
        ('-f / --file', 'Опциональный с флагом', 'script.py -f data.csv'),
        ('action="store_true"', 'Флаг-переключатель', 'script.py --verbose'),
        ('action="count"', 'Счётчик повторений', 'script.py -vvv (→ 3)'),
        ('nargs="+"', 'Список аргументов', 'script.py a b c'),
        ('choices=[...]', 'Ограничить варианты', 'script.py --format json'),
        ('type=Path', 'Авто-конверсия типа', 'Сразу Path-объект'),
    ]
)

# ── M46L1: NumPy ───────────────────────────────────────────────────────────────
M46 = '''
<h2>NumPy: почему Python для науки быстрее C-кода на чистых циклах</h2>
<p>NumPy выполняет операции над массивами в <strong>скомпилированном C/Fortran коде</strong>
и использует <strong>SIMD-инструкции</strong> процессора — одновременная обработка 4-16 чисел за такт.</p>
''' + code('python', '''import numpy as np
import time

# Сравнение скорости: Python list vs NumPy array
n = 10_000_000
data_list = list(range(n))
data_np   = np.arange(n, dtype=np.float64)

# Python
t0 = time.perf_counter()
result = [x * 2 + 1 for x in data_list]
print(f"Python list: {time.perf_counter()-t0:.2f}s")

# NumPy
t0 = time.perf_counter()
result = data_np * 2 + 1   # векторизованная операция
print(f"NumPy array: {time.perf_counter()-t0:.3f}s")
# NumPy обычно в 50-200 раз быстрее!

# ── Реальный кейс: обработка RGB-изображения ──────────────────────────────
from PIL import Image
img = np.array(Image.open("photo.jpg"))  # shape: (H, W, 3)
print(img.shape, img.dtype)              # (1080, 1920, 3) uint8

# Яркость +50 за одну операцию (вместо тройного цикла):
brighter = np.clip(img.astype(np.int16) + 50, 0, 255).astype(np.uint8)

# Конвертация в оттенки серого (формула luminance):
gray = (0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]).astype(np.uint8)

# ── Кейс: анализ продаж за год ─────────────────────────────────────────
sales = np.random.randint(100, 1000, size=(12, 30))  # 12 месяцев × 30 дней
print(f"Лучший день: {sales.max():,} руб.")
print(f"Средние продажи: {sales.mean():.0f} руб./день")
print(f"Лучший месяц: {sales.sum(axis=1).argmax() + 1}")   # ось 1 = по дням
print(f"Дней с продажами >500: {(sales > 500).sum()}")''') + tip(
    'Правило NumPy: если есть цикл <code>for</code> по массиву — почти всегда '
    'его можно заменить векторной операцией. Ищи функции в документации: '
    '<code>np.where()</code>, <code>np.sum(axis=)</code>, <code>np.argsort()</code>.'
) + table(
    ['Операция', 'Без NumPy', 'С NumPy', 'Ускорение'],
    [
        ('Сумма 10M чисел', '~200 мс', '~5 мс', '40x'),
        ('Умножение матриц 1000×1000', '~300 с', '~0.01 с', '30000x'),
        ('Медиана 1M чисел', '~500 мс', '~2 мс', '250x'),
        ('Поиск максимума', '~100 мс', '~3 мс', '33x'),
    ]
)

# ── M47L1: Pandas ─────────────────────────────────────────────────────────────
M47 = '''
<h2>Pandas: инструмент анализа данных, которым пользуется весь мир</h2>
<p>Pandas используют Netflix (рекомендации), Airbnb (ценообразование),
Bloomberg (финансы). Это не просто таблица — это SQL + Excel + Python в одном.</p>
''' + code('python', '''import pandas as pd
import numpy as np

# ── Реальный кейс: анализ продаж интернет-магазина ──────────────────────
# Загрузка (CSV, Excel, SQL, JSON, Parquet — Pandas читает всё):
# df = pd.read_csv("orders.csv", parse_dates=["order_date"])

# Создадим тестовые данные:
np.random.seed(42)
df = pd.DataFrame({
    "order_id":   range(1000),
    "user_id":    np.random.randint(1, 200, 1000),
    "product":    np.random.choice(["Книга","Курс","Подписка","Девайс"], 1000),
    "price":      np.random.uniform(50, 5000, 1000).round(2),
    "date":       pd.date_range("2024-01-01", periods=1000, freq="6h"),
    "status":     np.random.choice(["paid","pending","refunded"], 1000, p=[.8,.15,.05]),
})

# ── Ключевые вопросы бизнеса: ─────────────────────────────────────────
# 1. Выручка по месяцам:
monthly = df[df.status=="paid"].groupby(df.date.dt.month)["price"].sum()
print("Выручка по месяцам:")
print(monthly.round(0))

# 2. Топ-5 клиентов:
top_customers = (df[df.status=="paid"]
                 .groupby("user_id")["price"]
                 .sum()
                 .nlargest(5))

# 3. Конверсия воронки продаж:
funnel = df.status.value_counts(normalize=True) * 100
print(f"Оплачено: {funnel.get('paid', 0):.1f}%")
print(f"Возвраты: {funnel.get('refunded', 0):.1f}%")

# 4. Средний чек по категориям:
avg_check = df[df.status=="paid"].groupby("product")["price"].agg(["mean","count","sum"])
print(avg_check.sort_values("sum", ascending=False))

# 5. Поиск аномалий (заказы >3σ от среднего):
mean, std = df.price.mean(), df.price.std()
outliers = df[df.price > mean + 3*std]
print(f"Аномальных заказов: {len(outliers)}")''') + tip(
    'Ключевые операции Pandas для работы с данными: <code>groupby()</code> — группировка, '
    '<code>merge()</code> — JOIN таблиц, <code>pivot_table()</code> — сводная таблица, '
    '<code>resample()</code> — агрегация по времени (как в SQL <code>DATE_TRUNC</code>).'
) + table(
    ['Задача', 'Pandas-операция', 'SQL-аналог'],
    [
        ('Фильтрация', 'df[df.price > 100]', 'WHERE price > 100'),
        ('Группировка', 'df.groupby("city")["sales"].sum()', 'GROUP BY city'),
        ('Соединение', 'pd.merge(df1, df2, on="id")', 'INNER JOIN'),
        ('Сортировка', 'df.sort_values("date", ascending=False)', 'ORDER BY date DESC'),
        ('Уникальные', 'df.drop_duplicates("user_id")', 'DISTINCT user_id'),
        ('Первые 5', 'df.head(5) / df.nlargest(5, "price")', 'LIMIT 5 / TOP 5'),
    ]
)

# ═══════════════════════════════════════════════════════════════════════════════
PATCHES = {
    # (module_order, lesson_order): extra_content
    (2, 1): M2L1,
    (2, 2): M2L2,
    (2, 3): M2L3,
    (2, 4): M2L4,
    (12, 1): M12,
    (18, 1): M18,
    (32, 1): M32,
    (36, 1): M36,
    (40, 1): M40,
    (46, 1): M46,
    (47, 1): M47,
}


class Command(BaseCommand):
    help = 'Enrich thin Python theory lessons with real-life cases'

    def handle(self, *args, **kwargs):
        subj = Subject.objects.filter(slug='python').first()
        if not subj:
            self.stdout.write('Subject python not found'); return

        mods = TheoryModule.objects.filter(subject=subj).order_by('order')
        mod_map = {}
        for m in mods:
            if m.order not in mod_map:
                mod_map[m.order] = m

        count = 0
        for (mo, lo), extra in PATCHES.items():
            mod = mod_map.get(mo)
            if not mod:
                self.stdout.write(f'Module M{mo} not found'); continue
            lesson = TheoryLesson.objects.filter(module=mod, order=lo).first()
            if not lesson:
                self.stdout.write(f'Lesson M{mo}L{lo} not found'); continue
            old = len(lesson.content)
            lesson.content += extra
            lesson.estimated_minutes = max(lesson.estimated_minutes or 0, 20)
            lesson.save()
            new = len(lesson.content)
            self.stdout.write(f'M{mo}L{lo}: {old} -> {new} ch (+{new-old})')
            count += 1

        self.stdout.write(f'Done: {count} lessons enriched')
