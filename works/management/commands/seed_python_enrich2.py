# -*- coding: utf-8 -*-
"""
Вторая волна расширения тонких уроков Python.
Запуск: python manage.py seed_python_enrich2
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject

# ─── helpers ──────────────────────────────────────────────────────────────────
def tip(t): return f'<div class="tip">&#128161; {t}</div>'
def warn(t): return f'<div class="warning">&#9888; {t}</div>'
def info(t): return f'<div class="info">&#8505; {t}</div>'

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

def diagram(width, height, *items):
    inner = ''.join(items)
    return (f'<div style="overflow-x:auto;margin:1rem 0">'
            f'<svg viewBox="0 0 {width} {height}" style="max-width:100%;height:auto;display:block;margin:0 auto">'
            f'{inner}</svg></div>')

def arr(x1, y1, x2, y2, color='#64748b', label=''):
    dx = x2-x1; dy = y2-y1
    txt = f'<text x="{(x1+x2)//2}" y="{(y1+y2)//2-5}" text-anchor="middle" font-size="11" fill="{color}" font-family="sans-serif">{label}</text>' if label else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>' + txt

ARROW_DEF = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'


# ═══════════════════════════════════════════════════════════════════════════════
#  M3L1 — if / elif / else
# ═══════════════════════════════════════════════════════════════════════════════
M3L1 = (
    '<h2>if / elif / else — разветвление программы</h2>'
    '<p>Любая реальная программа принимает решения. Светофор включает красный или зелёный,'
    ' банкомат отказывает или выдаёт деньги, магазин применяет скидку или нет.</p>'
    + diagram(600, 180, ARROW_DEF,
        svg_box(20, 70, 100, 40, '#e0f2fe', '#0284c7', 'условие'),
        arr(120, 90, 200, 90, '#0284c7'),
        svg_box(200, 20, 100, 40, '#dcfce7', '#16a34a', 'True'),
        svg_box(200, 120, 100, 40, '#fee2e2', '#dc2626', 'False'),
        arr(300, 40, 380, 40, '#16a34a'),
        arr(300, 140, 380, 140, '#dc2626'),
        svg_box(380, 20, 120, 40, '#dcfce7', '#16a34a', 'блок True'),
        svg_box(380, 120, 120, 40, '#fee2e2', '#dc2626', 'блок False'),
    )
    + '<h3>Синтаксис и отступы</h3>'
    + code('python',
        'temperature = 36.6\n\n'
        'if temperature > 38:\n'
        '    print("Высокая температура — обратитесь к врачу")\n'
        'elif temperature < 35.5:\n'
        '    print("Пониженная температура")\n'
        'else:\n'
        '    print("Температура в норме")')
    + tip('Python определяет блоки отступами, а не фигурными скобками. '
          'Стандарт — 4 пробела.')
    + '<h3>Вложенные условия vs elif</h3>'
    + code('python',
        '# Плохо: лесенка из if\n'
        'if score >= 90:\n'
        '    if score >= 95:\n'
        '        grade = "A+"\n'
        '    else:\n'
        '        grade = "A"\n\n'
        '# Хорошо: плоская цепочка elif\n'
        'if score >= 95:   grade = "A+"\n'
        'elif score >= 90: grade = "A"\n'
        'elif score >= 80: grade = "B"\n'
        'elif score >= 70: grade = "C"\n'
        'else:             grade = "F"')
    + '<h3>Тернарный оператор</h3>'
    + code('python',
        '# value_if_true if condition else value_if_false\n'
        'label = "совершеннолетний" if age >= 18 else "несовершеннолетний"\n\n'
        '# Эквивалентно\n'
        'discount = 0.2 if is_member else 0.0')
    + '<h3>match/case (Python 3.10+)</h3>'
    + code('python',
        'status_code = 404\n\n'
        'match status_code:\n'
        '    case 200: print("OK")\n'
        '    case 404: print("Not Found")\n'
        '    case 500: print("Server Error")\n'
        '    case _:   print("Unknown")')
    + '<h3>Реальный кейс: тарифная сетка</h3>'
    + code('python',
        'def electricity_bill(kwh: float) -> float:\n'
        '    """Расчёт счёта по ступенчатому тарифу (как в реальных энергосбытах)."""\n'
        '    if kwh <= 150:\n'
        '        return kwh * 3.50\n'
        '    elif kwh <= 600:\n'
        '        return 150 * 3.50 + (kwh - 150) * 5.20\n'
        '    else:\n'
        '        return 150 * 3.50 + 450 * 5.20 + (kwh - 600) * 7.80\n\n'
        'print(electricity_bill(100))   # 350.0\n'
        'print(electricity_bill(300))   # 1305.0\n'
        'print(electricity_bill(700))   # 4083.0')
    + table(['Сценарий', 'Конструкция'],
        [['2 ветки', 'if / else'],
         ['3+ ветки', 'if / elif / elif / else'],
         ['Одна строка', 'x if cond else y'],
         ['Константы/паттерны', 'match / case (3.10+)']])
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M4L1 — while
# ═══════════════════════════════════════════════════════════════════════════════
M4L1 = (
    '<h2>while — цикл с условием</h2>'
    '<p>while выполняет блок кода <em>пока условие истинно</em>. '
    'Используется, когда число итераций неизвестно заранее: '
    'ввод данных от пользователя, ожидание ответа сервера, игровой цикл.</p>'
    + code('python',
        'attempts = 0\n'
        'max_attempts = 3\n\n'
        'while attempts < max_attempts:\n'
        '    password = input("Введите пароль: ")\n'
        '    if password == "secret":\n'
        '        print("Добро пожаловать!")\n'
        '        break\n'
        '    attempts += 1\n'
        '    print(f"Неверно. Осталось попыток: {max_attempts - attempts}")\n'
        'else:\n'
        '    print("Аккаунт заблокирован")  # else выполняется если цикл не прерван break')
    + tip('Конструкция <code>while/else</code> уникальна для Python. '
          'Блок <code>else</code> выполняется только если цикл завершился '
          'естественно (без <code>break</code>).')
    + '<h3>Бесконечный цикл с break</h3>'
    + code('python',
        '# Сервер обработки сообщений\n'
        'while True:\n'
        '    message = queue.get()       # блокирует до появления сообщения\n'
        '    if message is None:         # сигнал остановки\n'
        '        break\n'
        '    process(message)')
    + '<h3>Алгоритм Евклида — НОД</h3>'
    + code('python',
        'def gcd(a: int, b: int) -> int:\n'
        '    """Наибольший общий делитель через алгоритм Евклида."""\n'
        '    while b:\n'
        '        a, b = b, a % b\n'
        '    return a\n\n'
        'print(gcd(48, 18))   # 6\n'
        'print(gcd(100, 75))  # 25')
    + '<h3>Бинарный поиск через while</h3>'
    + code('python',
        'def binary_search(arr, target):\n'
        '    left, right = 0, len(arr) - 1\n'
        '    while left <= right:\n'
        '        mid = (left + right) // 2\n'
        '        if arr[mid] == target:\n'
        '            return mid\n'
        '        elif arr[mid] < target:\n'
        '            left = mid + 1\n'
        '        else:\n'
        '            right = mid - 1\n'
        '    return -1\n\n'
        'nums = [1, 3, 5, 7, 9, 11, 13]\n'
        'print(binary_search(nums, 7))   # 3\n'
        'print(binary_search(nums, 4))   # -1')
    + warn('Убедитесь, что тело цикла <em>изменяет</em> переменную условия. '
           'Иначе получите бесконечный цикл, который подвесит программу.')
    + '<h3>continue — пропустить итерацию</h3>'
    + code('python',
        'n = 0\n'
        'while n < 10:\n'
        '    n += 1\n'
        '    if n % 2 == 0:   # чётные пропускаем\n'
        '        continue\n'
        '    print(n)         # выводит 1 3 5 7 9')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M5L1 — for + range
# ═══════════════════════════════════════════════════════════════════════════════
M5L1 = (
    '<h2>for + range() — перебор последовательностей</h2>'
    '<p>for итерирует по любому <em>итерируемому</em> объекту: строке, списку, '
    'словарю, файлу, генератору. Это самый частый цикл в Python.</p>'
    + code('python',
        '# range(stop)          — 0..stop-1\n'
        '# range(start, stop)   — start..stop-1\n'
        '# range(start,stop,step)\n\n'
        'for i in range(5):           # 0,1,2,3,4\n'
        '    print(i)\n\n'
        'for i in range(1, 11, 2):    # нечётные 1..9\n'
        '    print(i)\n\n'
        'for i in range(10, 0, -1):   # обратный отсчёт\n'
        '    print(i)')
    + '<h3>Перебор с индексом: enumerate</h3>'
    + code('python',
        'fruits = ["яблоко", "банан", "вишня"]\n\n'
        '# Плохо (C-стиль)\n'
        'for i in range(len(fruits)):\n'
        '    print(i, fruits[i])\n\n'
        '# Хорошо (Pythonic)\n'
        'for i, fruit in enumerate(fruits, start=1):\n'
        '    print(f"{i}. {fruit}")\n'
        '# 1. яблоко\n'
        '# 2. банан\n'
        '# 3. вишня')
    + '<h3>Параллельный перебор: zip</h3>'
    + code('python',
        'names  = ["Alice", "Bob", "Carol"]\n'
        'scores = [92, 87, 95]\n\n'
        'for name, score in zip(names, scores):\n'
        '    grade = "A" if score >= 90 else "B"\n'
        '    print(f"{name}: {score} ({grade})")')
    + '<h3>List comprehension — компактный for</h3>'
    + code('python',
        '# Классика\n'
        'squares = []\n'
        'for x in range(1, 6):\n'
        '    squares.append(x**2)\n\n'
        '# List comprehension — в одну строку\n'
        'squares = [x**2 for x in range(1, 6)]\n\n'
        '# С условием\n'
        'evens = [x for x in range(20) if x % 2 == 0]\n\n'
        '# Вложенный (таблица умножения)\n'
        'mult = [(i, j, i*j) for i in range(1,4) for j in range(1,4)]')
    + tip('List comprehension в 2–3 раза быстрее обычного цикла с append, '
          'потому что интерпретатор специально оптимизирует эту конструкцию.')
    + '<h3>Реальный кейс: обработка данных</h3>'
    + code('python',
        '# Анализ продаж за неделю\n'
        'daily_sales = [15200, 18400, 12100, 21600, 19800, 24300, 17500]\n'
        'days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]\n\n'
        'total = sum(daily_sales)\n'
        'average = total / len(daily_sales)\n\n'
        'print(f"Итого за неделю: {total:,} руб.")\n'
        'print(f"Среднее в день: {average:,.0f} руб.")\n\n'
        'for day, sale in zip(days, daily_sales):\n'
        '    bar = "#" * (sale // 1000)\n'
        '    delta = sale - average\n'
        '    sign = "+" if delta >= 0 else ""\n'
        '    print(f"{day}: {bar} ({sign}{delta:,.0f})")')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M5L2 — break / continue / else
# ═══════════════════════════════════════════════════════════════════════════════
M5L2 = (
    '<h2>break, continue, else в циклах</h2>'
    + code('python',
        '# break  — прервать цикл полностью\n'
        '# continue — перейти к следующей итерации\n'
        '# else   — выполнить, если цикл не прерван через break')
    + '<h3>Поиск с break</h3>'
    + code('python',
        'numbers = [4, 7, 2, 9, 1, 5, 8]\n\n'
        'for i, num in enumerate(numbers):\n'
        '    if num > 8:\n'
        '        print(f"Первый >8 на позиции {i}: {num}")\n'
        '        break\n'
        'else:\n'
        '    print("Нет числа больше 8")')
    + '<h3>Фильтрация с continue</h3>'
    + code('python',
        '# Обработка строк, пропуская пустые и комментарии\n'
        'config_lines = [\n'
        '    "# Настройки базы данных",\n'
        '    "",\n'
        '    "host=localhost",\n'
        '    "port=5432",\n'
        '    "# Конец",\n'
        '    "name=mydb",\n'
        ']\n\n'
        'settings = {}\n'
        'for line in config_lines:\n'
        '    if not line or line.startswith("#"):\n'
        '        continue                 # пропускаем\n'
        '    key, value = line.split("=")\n'
        '    settings[key] = value\n\n'
        'print(settings)\n'
        '# {"host": "localhost", "port": "5432", "name": "mydb"}')
    + '<h3>for/else — проверка простоты числа</h3>'
    + code('python',
        'def is_prime(n: int) -> bool:\n'
        '    if n < 2: return False\n'
        '    for i in range(2, int(n**0.5) + 1):\n'
        '        if n % i == 0:\n'
        '            return False    # break\n'
        '    else:\n'
        '        return True         # цикл дошёл до конца — делителей нет\n\n'
        'primes = [n for n in range(2, 30) if is_prime(n)]\n'
        'print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]')
    + tip('<code>for/else</code> — идиома Python, которой нет в C/Java. '
          'Заменяет паттерн "found = False ... if found: ..." одной конструкцией.')
    + '<h3>Вложенные циклы: break прерывает только внутренний</h3>'
    + code('python',
        '# Найти пару (i,j) с i*j == target\n'
        'target = 12\n'
        'found = False\n\n'
        'for i in range(1, 10):\n'
        '    for j in range(1, 10):\n'
        '        if i * j == target:\n'
        '            print(f"Найдено: {i} * {j} = {target}")\n'
        '            found = True\n'
        '            break         # выходим из внутреннего\n'
        '    if found: break       # выходим из внешнего')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M6L1 — функции: определение и вызов
# ═══════════════════════════════════════════════════════════════════════════════
M6L1 = (
    '<h2>Функции: определение и вызов</h2>'
    '<p>Функция — <em>именованный блок кода</em>, который можно вызвать повторно. '
    'Без функций программа в 1000 строк превращается в лапшу. '
    'Функции — основа DRY (Don\'t Repeat Yourself).</p>'
    + diagram(700, 160, ARROW_DEF,
        svg_box(10, 60, 120, 40, '#e0f2fe', '#0284c7', 'def greet(name):'),
        arr(130, 80, 210, 80),
        svg_box(210, 30, 140, 40, '#fef9c3', '#ca8a04', 'параметры'),
        svg_box(210, 90, 140, 40, '#dcfce7', '#16a34a', 'тело функции'),
        arr(350, 80, 430, 80),
        svg_box(430, 60, 120, 40, '#f3e8ff', '#9333ea', 'return значение'),
        arr(550, 80, 630, 80),
        svg_box(630, 60, 60, 40, '#e0f2fe', '#0284c7', 'вызов'),
    )
    + '<h3>Параметры: позиционные, именованные, со значением по умолчанию</h3>'
    + code('python',
        'def send_email(to, subject, body="", html=False):\n'
        '    """Отправить письмо.\n\n'
        '    Args:\n'
        '        to: адрес получателя\n'
        '        subject: тема письма\n'
        '        body: текст (по умолчанию пустой)\n'
        '        html: если True — HTML-письмо\n'
        '    """\n'
        '    # ...\n'
        '    pass\n\n'
        '# Вызовы\n'
        'send_email("user@example.com", "Привет")\n'
        'send_email("boss@company.com", "Отчёт", body="Смотри файл", html=True)')
    + '<h3>*args и **kwargs</h3>'
    + code('python',
        'def log(*args, level="INFO", **kwargs):\n'
        '    """Логирование с произвольными аргументами."""\n'
        '    parts = " ".join(str(a) for a in args)\n'
        '    extra = " ".join(f"{k}={v}" for k,v in kwargs.items())\n'
        '    print(f"[{level}] {parts} {extra}")\n\n'
        'log("Запрос принят", "GET /api/users")\n'
        'log("Ошибка!", level="ERROR", code=500, path="/api")')
    + '<h3>Возвращаемое значение</h3>'
    + code('python',
        '# Несколько значений через tuple\n'
        'def divide(a, b):\n'
        '    if b == 0:\n'
        '        return None, "Деление на ноль"\n'
        '    return a / b, None\n\n'
        'result, error = divide(10, 3)\n'
        'if error:\n'
        '    print(f"Ошибка: {error}")\n'
        'else:\n'
        '    print(f"Результат: {result:.4f}")')
    + tip('Функция без <code>return</code> неявно возвращает <code>None</code>. '
          'Всегда документируйте что возвращается через docstring или аннотации типов.')
    + '<h3>Реальный кейс: конвертер валют</h3>'
    + code('python',
        'RATES = {"USD": 1.0, "EUR": 0.92, "RUB": 91.5, "GBP": 0.79}\n\n'
        'def convert(amount: float, from_cur: str, to_cur: str) -> float:\n'
        '    """Конвертировать сумму между валютами."""\n'
        '    if from_cur not in RATES or to_cur not in RATES:\n'
        '        raise ValueError(f"Неизвестная валюта")\n'
        '    usd = amount / RATES[from_cur]   # в доллары\n'
        '    return usd * RATES[to_cur]        # из долларов\n\n'
        'print(f"{convert(1000, \'RUB\', \'USD\'):.2f} USD")\n'
        'print(f"{convert(100, \'EUR\', \'RUB\'):.2f} RUB")')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M6L2 — рекурсия
# ═══════════════════════════════════════════════════════════════════════════════
M6L2 = (
    '<h2>Рекурсия: функция вызывает сама себя</h2>'
    '<p>Рекурсия — когда функция решает задачу, сводя её к уменьшенной версии той же задачи. '
    'Алгоритмы на деревьях, JSON с вложенными объектами, файловые системы — '
    'все это естественно выражается через рекурсию.</p>'
    + diagram(600, 180, ARROW_DEF,
        svg_box(10, 70, 120, 40, '#e0f2fe', '#0284c7', 'factorial(5)'),
        arr(130, 90, 200, 60),
        svg_box(200, 40, 120, 40, '#f3e8ff', '#9333ea', 'factorial(4)'),
        arr(320, 60, 390, 40),
        svg_box(390, 20, 110, 40, '#fef9c3', '#ca8a04', 'factorial(3)'),
        arr(390, 110, 320, 130),
        svg_box(200, 110, 120, 40, '#dcfce7', '#16a34a', '5 * 24 = 120'),
        svg_box(390, 100, 110, 40, '#dcfce7', '#16a34a', 'base: n<=1 ->1'),
    )
    + '<h3>Структура рекурсивной функции</h3>'
    + code('python',
        'def factorial(n: int) -> int:\n'
        '    # 1. Базовый случай (остановка рекурсии)\n'
        '    if n <= 1:\n'
        '        return 1\n'
        '    # 2. Рекурсивный случай (сводим к меньшей задаче)\n'
        '    return n * factorial(n - 1)\n\n'
        'print(factorial(5))  # 120 (5*4*3*2*1)\n'
        'print(factorial(10)) # 3628800')
    + warn('Python по умолчанию ограничивает глубину рекурсии 1000 вызовов '
           '(<code>sys.getrecursionlimit()</code>). '
           'Для глубоких деревьев или больших n используйте итеративный вариант.')
    + '<h3>Числа Фибоначчи и мемоизация</h3>'
    + code('python',
        '# Наивно: экспоненциальная сложность O(2^n)\n'
        'def fib_slow(n):\n'
        '    if n <= 1: return n\n'
        '    return fib_slow(n-1) + fib_slow(n-2)\n\n'
        '# С мемоизацией: O(n)\n'
        'from functools import lru_cache\n\n'
        '@lru_cache(maxsize=None)\n'
        'def fib(n):\n'
        '    if n <= 1: return n\n'
        '    return fib(n-1) + fib(n-2)\n\n'
        'print(fib(50))   # 12586269025  (мгновенно)\n'
        '# fib_slow(50) работал бы >20 минут')
    + '<h3>Реальный кейс: обход файловой системы</h3>'
    + code('python',
        'import os\n\n'
        'def count_py_files(directory: str) -> int:\n'
        '    """Рекурсивно считает .py файлы в папке."""\n'
        '    count = 0\n'
        '    for entry in os.scandir(directory):\n'
        '        if entry.is_file() and entry.name.endswith(".py"):\n'
        '            count += 1\n'
        '        elif entry.is_dir():\n'
        '            count += count_py_files(entry.path)  # рекурсия!\n'
        '    return count\n\n'
        'print(count_py_files("."))  # количество .py файлов в проекте')
    + '<h3>Реальный кейс: flatten вложенного списка</h3>'
    + code('python',
        'def flatten(lst):\n'
        '    """Разворачивает список любой глубины вложенности."""\n'
        '    result = []\n'
        '    for item in lst:\n'
        '        if isinstance(item, list):\n'
        '            result.extend(flatten(item))  # рекурсия\n'
        '        else:\n'
        '            result.append(item)\n'
        '    return result\n\n'
        'data = [1, [2, 3], [4, [5, 6]], [[[7]]]]\n'
        'print(flatten(data))  # [1, 2, 3, 4, 5, 6, 7]')
    + tip('JSON-данные из API часто приходят с произвольной вложенностью. '
          'Рекурсивный обход — стандартное решение для обработки таких структур.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M7L1 — списки
# ═══════════════════════════════════════════════════════════════════════════════
M7L1 = (
    '<h2>Списки (list) — динамические массивы Python</h2>'
    '<p>list — наиболее используемая структура данных в Python. '
    'Хранит элементы <em>любых типов</em> в порядке вставки, '
    'поддерживает дубликаты, изменяемый.</p>'
    + diagram(700, 120, ARROW_DEF,
        svg_box(10, 40, 60, 40, '#e0f2fe', '#0284c7', 'a[0]\n"Alice"'),
        svg_box(80, 40, 60, 40, '#dcfce7', '#16a34a', 'a[1]\n"Bob"'),
        svg_box(150, 40, 60, 40, '#fef9c3', '#ca8a04', 'a[2]\n"Carol"'),
        svg_box(220, 40, 60, 40, '#fee2e2', '#dc2626', 'a[3]\n42'),
        svg_box(290, 40, 60, 40, '#f3e8ff', '#9333ea', 'a[4]\nTrue'),
        '<text x="380" y="65" font-size="12" fill="#64748b" font-family="sans-serif">индексы: 0,1,2,3,4</text>',
        '<text x="380" y="85" font-size="12" fill="#64748b" font-family="sans-serif">или:    -5,-4,-3,-2,-1</text>',
    )
    + '<h3>Создание и срезы</h3>'
    + code('python',
        'nums = [10, 20, 30, 40, 50]\n\n'
        '# Индексация\n'
        'print(nums[0])    # 10  (первый)\n'
        'print(nums[-1])   # 50  (последний)\n\n'
        '# Срезы [start:stop:step]\n'
        'print(nums[1:4])   # [20, 30, 40]\n'
        'print(nums[::2])   # [10, 30, 50] (каждый второй)\n'
        'print(nums[::-1])  # [50, 40, 30, 20, 10] (обратный)')
    + '<h3>Основные методы</h3>'
    + table(['Метод', 'Описание', 'O(?)'],
        [['append(x)', 'Добавить в конец', 'O(1)'],
         ['insert(i, x)', 'Вставить по индексу', 'O(n)'],
         ['pop()', 'Удалить и вернуть последний', 'O(1)'],
         ['pop(i)', 'Удалить по индексу', 'O(n)'],
         ['remove(x)', 'Удалить первое вхождение', 'O(n)'],
         ['sort()', 'Сортировать на месте', 'O(n log n)'],
         ['index(x)', 'Найти индекс элемента', 'O(n)']])
    + '<h3>Стек и очередь на основе list</h3>'
    + code('python',
        '# Стек (LIFO) — push/pop с конца\n'
        'stack = []\n'
        'stack.append("задача1")\n'
        'stack.append("задача2")\n'
        'stack.append("задача3")\n'
        'print(stack.pop())   # "задача3" — последний вошёл, первый вышел\n\n'
        '# Очередь (FIFO) — для больших объёмов лучше collections.deque\n'
        'from collections import deque\n'
        'queue = deque()\n'
        'queue.append("клиент1")\n'
        'queue.append("клиент2")\n'
        'print(queue.popleft())  # "клиент1"')
    + '<h3>Реальный кейс: история браузера</h3>'
    + code('python',
        'class BrowserHistory:\n'
        '    def __init__(self, homepage: str):\n'
        '        self.history = [homepage]\n'
        '        self.current = 0\n\n'
        '    def visit(self, url: str):\n'
        '        # Обрезаем "будущее" при новом переходе\n'
        '        self.history = self.history[:self.current + 1]\n'
        '        self.history.append(url)\n'
        '        self.current = len(self.history) - 1\n\n'
        '    def back(self, steps: int) -> str:\n'
        '        self.current = max(0, self.current - steps)\n'
        '        return self.history[self.current]\n\n'
        '    def forward(self, steps: int) -> str:\n'
        '        self.current = min(len(self.history)-1, self.current+steps)\n'
        '        return self.history[self.current]\n\n'
        'b = BrowserHistory("google.com")\n'
        'b.visit("youtube.com")\n'
        'b.visit("github.com")\n'
        'print(b.back(1))     # "youtube.com"\n'
        'print(b.forward(1))  # "github.com"')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M7L2 — методы списков
# ═══════════════════════════════════════════════════════════════════════════════
M7L2 = (
    '<h2>Методы списков и эффективная работа</h2>'
    + code('python',
        'a = [3, 1, 4, 1, 5, 9, 2, 6]\n\n'
        'a.sort()                    # сортировка на месте\n'
        'a.sort(reverse=True)        # по убыванию\n\n'
        'b = sorted(a)               # новый список (a не изменяется)\n\n'
        '# Сортировка по ключу\n'
        'words = ["banana", "apple", "cherry", "date"]\n'
        'words.sort(key=len)         # по длине\n'
        'words.sort(key=str.lower)   # case-insensitive\n\n'
        'people = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]\n'
        'people.sort(key=lambda p: p["age"])')
    + '<h3>Копирование: shallow vs deep</h3>'
    + code('python',
        'import copy\n\n'
        'original = [[1, 2], [3, 4]]\n\n'
        '# Поверхностная копия — внутренние списки общие!\n'
        'shallow = original.copy()          # или original[:]\n'
        'shallow[0].append(99)\n'
        'print(original)  # [[1, 2, 99], [3, 4]] — ИЗМЕНИЛСЯ!\n\n'
        '# Глубокая копия — полностью независима\n'
        'deep = copy.deepcopy(original)\n'
        'deep[0].append(42)\n'
        'print(original)  # [[1, 2, 99], [3, 4]] — не изменился')
    + warn('Это частая ловушка! При копировании списка списков всегда используйте '
           '<code>copy.deepcopy()</code>, если нужна независимость.')
    + '<h3>Операции над списками</h3>'
    + code('python',
        '# Конкатенация\n'
        'a = [1, 2, 3]\n'
        'b = [4, 5, 6]\n'
        'c = a + b           # [1,2,3,4,5,6] — новый список\n'
        'a.extend(b)         # расширить a на месте\n\n'
        '# Повторение\n'
        'zeros = [0] * 10    # [0,0,0,0,0,0,0,0,0,0]\n\n'
        '# Проверка\n'
        'print(5 in [1, 3, 5, 7])     # True\n'
        'print([1,2] == [1,2])         # True (сравнение по содержимому)\n\n'
        '# Распаковка\n'
        'first, *rest = [10, 20, 30, 40]\n'
        'print(first)  # 10\n'
        'print(rest)   # [20, 30, 40]')
    + '<h3>zip, map, filter с списками</h3>'
    + code('python',
        'prices  = [100, 200, 150, 80]\n'
        'amounts = [3, 1, 2, 5]\n\n'
        '# zip — пары (price, amount)\n'
        'totals = [p * a for p, a in zip(prices, amounts)]\n'
        'print(totals)    # [300, 200, 300, 400]\n\n'
        '# filter — только дорогие\n'
        'expensive = list(filter(lambda p: p >= 150, prices))\n'
        'print(expensive) # [200, 150]\n\n'
        '# map — применить скидку\n'
        'discounted = list(map(lambda p: round(p * 0.9, 2), prices))\n'
        'print(discounted) # [90.0, 180.0, 135.0, 72.0]')
    + tip('В современном Python <code>filter()</code> и <code>map()</code> '
          'чаще заменяют list comprehension — они читаемее.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M8L1 — словарь
# ═══════════════════════════════════════════════════════════════════════════════
M8L1 = (
    '<h2>Словарь (dict) — хеш-таблица Python</h2>'
    '<p>dict — пары ключ→значение. Поиск и вставка за O(1). '
    'Один из самых мощных инструментов Python. '
    'С Python 3.7+ гарантируется порядок вставки.</p>'
    + code('python',
        '# Создание\n'
        'person = {"name": "Alice", "age": 30, "city": "Moscow"}\n'
        'empty = {}\n'
        'from_pairs = dict([("a", 1), ("b", 2)])\n\n'
        '# Доступ\n'
        'print(person["name"])              # "Alice"\n'
        'print(person.get("phone", "N/A")) # "N/A" (нет KeyError)\n\n'
        '# Изменение\n'
        'person["age"] = 31\n'
        'person.update({"city": "SPb", "email": "a@b.com"})')
    + '<h3>Методы и перебор</h3>'
    + code('python',
        'inventory = {"apple": 50, "banana": 30, "cherry": 10}\n\n'
        '# Ключи, значения, пары\n'
        'print(list(inventory.keys()))    # ["apple", "banana", "cherry"]\n'
        'print(list(inventory.values()))  # [50, 30, 10]\n\n'
        'for product, count in inventory.items():\n'
        '    status = "OK" if count > 20 else "МАЛО"\n'
        '    print(f"{product}: {count} шт. [{status}]")')
    + '<h3>defaultdict и Counter</h3>'
    + code('python',
        'from collections import defaultdict, Counter\n\n'
        '# defaultdict: нет KeyError при первом доступе\n'
        'groups = defaultdict(list)\n'
        'for student, grade in [("Alice","A"),("Bob","B"),("Carol","A"),("Dave","B")]:\n'
        '    groups[grade].append(student)\n'
        'print(dict(groups))\n'
        '# {"A": ["Alice", "Carol"], "B": ["Bob", "Dave"]}\n\n'
        '# Counter: подсчёт элементов\n'
        'text = "hello world"\n'
        'freq = Counter(text)\n'
        'print(freq.most_common(3))  # [("l",3),("o",2),("h",1)]')
    + '<h3>Реальный кейс: кеш результатов</h3>'
    + code('python',
        'import time\n\n'
        '_cache = {}\n\n'
        'def expensive_query(user_id: int) -> dict:\n'
        '    """Запрос к БД с кешем."""\n'
        '    if user_id in _cache:\n'
        '        return _cache[user_id]      # мгновенно из кеша\n\n'
        '    # Симуляция долгого запроса\n'
        '    time.sleep(0.1)\n'
        '    result = {"id": user_id, "name": f"User{user_id}", "score": 100}\n'
        '    _cache[user_id] = result        # сохраняем в кеш\n'
        '    return result\n\n'
        '# Первый вызов — медленно\n'
        'print(expensive_query(42))   # 0.1 сек\n'
        '# Второй вызов — мгновенно\n'
        'print(expensive_query(42))   # < 1 мс (из кеша)')
    + tip('Реальные кеши (Redis, Memcached) работают по тому же принципу. '
          'Словарь Python — это in-process кеш на один процесс.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M8L2 — множества
# ═══════════════════════════════════════════════════════════════════════════════
M8L2 = (
    '<h2>Множества (set) — математическое множество в Python</h2>'
    '<p>set хранит уникальные элементы, поиск за O(1). '
    'Используется для удаления дублей, проверки принадлежности, '
    'операций пересечения/объединения.</p>'
    + code('python',
        'a = {1, 2, 3, 4, 5}\n'
        'b = {4, 5, 6, 7, 8}\n\n'
        'print(a | b)   # объединение:   {1,2,3,4,5,6,7,8}\n'
        'print(a & b)   # пересечение:   {4, 5}\n'
        'print(a - b)   # разность:      {1, 2, 3}\n'
        'print(a ^ b)   # симм. разность:{1,2,3,6,7,8}\n\n'
        '# Проверка\n'
        'print(3 in a)          # True\n'
        'print(a.issubset({1,2,3,4,5,6}))   # True')
    + '<h3>Реальный кейс 1: удаление дублей</h3>'
    + code('python',
        '# Задача: найти пользователей, зашедших оба дня\n'
        'day1_visitors = ["alice", "bob", "charlie", "alice", "dave"]\n'
        'day2_visitors = ["bob", "eve", "alice", "frank", "dave"]\n\n'
        'both_days = set(day1_visitors) & set(day2_visitors)\n'
        'print(f"Пришли оба дня: {both_days}")\n'
        '# {"alice", "bob", "dave"}\n\n'
        'only_day1 = set(day1_visitors) - set(day2_visitors)\n'
        'print(f"Только в день 1: {only_day1}")\n'
        '# {"charlie"}')
    + '<h3>Реальный кейс 2: поиск анаграмм</h3>'
    + code('python',
        'def is_anagram(s1: str, s2: str) -> bool:\n'
        '    """Проверить, являются ли строки анаграммами."""\n'
        '    return Counter(s1.lower()) == Counter(s2.lower())\n\n'
        'from collections import Counter\n'
        'print(is_anagram("listen", "silent"))   # True\n'
        'print(is_anagram("hello", "world"))     # False')
    + '<h3>frozenset — неизменяемое множество</h3>'
    + code('python',
        '# frozenset можно использовать как ключ словаря\n'
        'permissions_map = {\n'
        '    frozenset({"read"}): "readonly",\n'
        '    frozenset({"read", "write"}): "editor",\n'
        '    frozenset({"read", "write", "delete"}): "admin",\n'
        '}\n\n'
        'user_perms = frozenset({"read", "write"})\n'
        'print(permissions_map[user_perms])  # "editor"')
    + table(['Операция', 'set', 'list', 'dict (ключи)'],
        [['Поиск x', 'O(1)', 'O(n)', 'O(1)'],
         ['Добавление', 'O(1)', 'O(1) конец', 'O(1)'],
         ['Удаление', 'O(1)', 'O(n)', 'O(1)'],
         ['Дубликаты', 'Нет', 'Да', 'Нет']])
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M9L1 — исключения
# ═══════════════════════════════════════════════════════════════════════════════
M9L1 = (
    '<h2>Исключения: try / except / else / finally</h2>'
    '<p>Исключения — механизм обработки ошибок во время выполнения. '
    'Без них программа падает при первой проблеме. '
    'С ними — корректно обрабатывает сбои и сообщает пользователю что произошло.</p>'
    + diagram(700, 160, ARROW_DEF,
        svg_box(10, 60, 80, 40, '#e0f2fe', '#0284c7', 'try'),
        arr(90, 80, 170, 80),
        svg_box(170, 30, 100, 40, '#dcfce7', '#16a34a', 'успех\n-> else'),
        svg_box(170, 90, 100, 40, '#fee2e2', '#dc2626', 'ошибка\n-> except'),
        arr(270, 50, 370, 50),
        arr(270, 110, 370, 110),
        svg_box(370, 20, 100, 40, '#dcfce7', '#16a34a', 'else'),
        svg_box(370, 80, 100, 40, '#fee2e2', '#dc2626', 'except'),
        arr(470, 50, 550, 80),
        arr(470, 110, 550, 80),
        svg_box(550, 60, 100, 40, '#fef9c3', '#ca8a04', 'finally\n(всегда)'),
    )
    + code('python',
        'def read_config(path: str) -> dict:\n'
        '    try:\n'
        '        with open(path) as f:\n'
        '            data = json.load(f)\n'
        '    except FileNotFoundError:\n'
        '        print(f"Файл {path} не найден, используем настройки по умолчанию")\n'
        '        return DEFAULT_CONFIG\n'
        '    except json.JSONDecodeError as e:\n'
        '        print(f"Ошибка в JSON: {e}")\n'
        '        raise   # пробрасываем дальше\n'
        '    else:\n'
        '        print(f"Конфиг загружен: {len(data)} параметров")\n'
        '        return data\n'
        '    finally:\n'
        '        print("read_config завершён")   # выполнится ВСЕГДА')
    + '<h3>Иерархия исключений Python</h3>'
    + table(['Класс', 'Когда возникает'],
        [['ValueError', 'Неверное значение: int("abc")'],
         ['TypeError', 'Неверный тип: "a" + 1'],
         ['KeyError', 'Ключ не найден в dict'],
         ['IndexError', 'Индекс за пределами списка'],
         ['FileNotFoundError', 'Файл не существует'],
         ['ZeroDivisionError', 'Деление на ноль'],
         ['AttributeError', 'Атрибут/метод не найден']])
    + '<h3>Собственные исключения</h3>'
    + code('python',
        'class InsufficientFundsError(ValueError):\n'
        '    def __init__(self, amount, balance):\n'
        '        self.amount = amount\n'
        '        self.balance = balance\n'
        '        super().__init__(f"Нужно {amount}, на счёте {balance}")\n\n'
        'class BankAccount:\n'
        '    def __init__(self, balance: float):\n'
        '        self.balance = balance\n\n'
        '    def withdraw(self, amount: float):\n'
        '        if amount > self.balance:\n'
        '            raise InsufficientFundsError(amount, self.balance)\n'
        '        self.balance -= amount\n\n'
        'acc = BankAccount(1000)\n'
        'try:\n'
        '    acc.withdraw(1500)\n'
        'except InsufficientFundsError as e:\n'
        '    print(f"Ошибка: {e}")   # Нужно 1500, на счёте 1000')
    + tip('Создавайте иерархии исключений для своих библиотек. '
          'Пользователи смогут ловить как конкретные ошибки, '
          'так и базовый класс — как в стандартной библиотеке Python.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M10L1 — lambda / map / filter / sorted
# ═══════════════════════════════════════════════════════════════════════════════
M10L1 = (
    '<h2>Lambda-функции и функции высшего порядка</h2>'
    '<p>lambda — однострочная анонимная функция. '
    'Передаётся как аргумент в <code>sorted()</code>, <code>map()</code>, <code>filter()</code>.</p>'
    + code('python',
        '# lambda аргументы: выражение\n'
        'double = lambda x: x * 2\n'
        'add    = lambda x, y: x + y\n\n'
        'print(double(5))    # 10\n'
        'print(add(3, 4))    # 7\n\n'
        '# Обычно лямбды не сохраняют в переменную — это анти-паттерн.\n'
        '# Используйте def для именованных функций.')
    + '<h3>sorted() с ключом</h3>'
    + code('python',
        'students = [\n'
        '    {"name": "Alice", "grade": 92, "age": 20},\n'
        '    {"name": "Bob",   "grade": 85, "age": 22},\n'
        '    {"name": "Carol", "grade": 92, "age": 19},\n'
        ']\n\n'
        '# По оценке убывая, при равных — по имени\n'
        'ranking = sorted(students, key=lambda s: (-s["grade"], s["name"]))\n'
        'for i, s in enumerate(ranking, 1):\n'
        '    print(f"{i}. {s[\'name\']}: {s[\'grade\']}")')
    + '<h3>map и filter</h3>'
    + code('python',
        'prices = [100.0, 200.50, 150.75, 80.25]\n\n'
        '# map: применить функцию к каждому элементу\n'
        'with_tax = list(map(lambda p: round(p * 1.2, 2), prices))\n'
        'print(with_tax)   # [120.0, 240.6, 180.9, 96.3]\n\n'
        '# filter: оставить только удовлетворяющие условию\n'
        'affordable = list(filter(lambda p: p < 150, prices))\n'
        'print(affordable) # [100.0, 80.25]')
    + '<h3>functools.reduce</h3>'
    + code('python',
        'from functools import reduce\n\n'
        '# reduce(f, [a,b,c,d]) = f(f(f(a,b),c),d)\n'
        'product = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])\n'
        'print(product)  # 120 (5!)\n\n'
        '# Нахождение максимума через reduce\n'
        'max_val = reduce(lambda a, b: a if a > b else b, [3, 1, 4, 1, 5, 9])\n'
        'print(max_val)  # 9')
    + tip('В Python 3 предпочтительнее list comprehension вместо map/filter. '
          'Они читаемее и быстрее. Lambda нужна в первую очередь для <code>sorted(key=...)</code>.')
    + '<h3>Реальный кейс: пайплайн обработки данных</h3>'
    + code('python',
        '# Обработка транзакций: валидация -> конвертация -> фильтрация\n'
        'raw_transactions = [\n'
        '    {"id": 1, "amount": "100.50", "currency": "USD", "valid": True},\n'
        '    {"id": 2, "amount": "invalid", "currency": "EUR", "valid": True},\n'
        '    {"id": 3, "amount": "200.00", "currency": "USD", "valid": False},\n'
        '    {"id": 4, "amount": "50.25", "currency": "EUR", "valid": True},\n'
        ']\n\n'
        'USD_ONLY = (\n'
        '    filter(lambda t: t["valid"],          raw_transactions)   # валидные\n'
        ')\n'
        '# Дальнейшая обработка пайплайном...')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M11L1 — декораторы
# ═══════════════════════════════════════════════════════════════════════════════
M11L1 = (
    '<h2>Декораторы: функции-обёртки</h2>'
    '<p>Декоратор — паттерн, который добавляет поведение функции '
    '<em>без изменения её кода</em>. '
    'Логирование, замер времени, кеширование, авторизация — всё это декораторы.</p>'
    + code('python',
        'import time\n\n'
        'def timer(func):\n'
        '    """Декоратор: замеряет время выполнения."""\n'
        '    def wrapper(*args, **kwargs):\n'
        '        start = time.perf_counter()\n'
        '        result = func(*args, **kwargs)     # вызываем оригинал\n'
        '        elapsed = time.perf_counter() - start\n'
        '        print(f"{func.__name__} выполнялась {elapsed:.4f} сек")\n'
        '        return result\n'
        '    return wrapper\n\n'
        '@timer\n'
        'def slow_function(n):\n'
        '    return sum(i**2 for i in range(n))\n\n'
        'result = slow_function(1_000_000)\n'
        '# slow_function выполнялась 0.0821 сек')
    + tip('Синтаксис <code>@timer</code> — это сокращение для '
          '<code>slow_function = timer(slow_function)</code>.')
    + '<h3>functools.wraps — сохранение метаданных</h3>'
    + code('python',
        'from functools import wraps\n\n'
        'def logger(func):\n'
        '    @wraps(func)   # сохраняет __name__, __doc__\n'
        '    def wrapper(*args, **kwargs):\n'
        '        print(f"Вызов {func.__name__}({args}, {kwargs})")\n'
        '        result = func(*args, **kwargs)\n'
        '        print(f"{func.__name__} вернула {result}")\n'
        '        return result\n'
        '    return wrapper\n\n'
        '@logger\n'
        'def add(x, y):\n'
        '    """Складывает два числа."""\n'
        '    return x + y\n\n'
        'add(3, 4)\n'
        '# Вызов add((3, 4), {})\n'
        '# add вернула 7\n'
        'print(add.__name__)  # "add" (без @wraps было бы "wrapper")')
    + '<h3>Декоратор с аргументами</h3>'
    + code('python',
        'def retry(max_attempts=3, delay=1.0):\n'
        '    """Повторить при ошибке."""\n'
        '    def decorator(func):\n'
        '        @wraps(func)\n'
        '        def wrapper(*args, **kwargs):\n'
        '            for attempt in range(max_attempts):\n'
        '                try:\n'
        '                    return func(*args, **kwargs)\n'
        '                except Exception as e:\n'
        '                    if attempt == max_attempts - 1:\n'
        '                        raise\n'
        '                    print(f"Попытка {attempt+1} неудачна: {e}, жду {delay}с")\n'
        '                    time.sleep(delay)\n'
        '        return wrapper\n'
        '    return decorator\n\n'
        '@retry(max_attempts=3, delay=0.5)\n'
        'def fetch_data(url: str):\n'
        '    # Может упасть при нестабильном интернете\n'
        '    response = requests.get(url, timeout=5)\n'
        '    response.raise_for_status()\n'
        '    return response.json()')
    + '<h3>Встроенные декораторы Python</h3>'
    + table(['Декоратор', 'Назначение'],
        [['@staticmethod', 'Статический метод (нет self)'],
         ['@classmethod', 'Метод класса (cls вместо self)'],
         ['@property', 'Геттер атрибута'],
         ['@lru_cache', 'Мемоизация (кеш результатов),functools'],
         ['@dataclass', 'Авто-генерация __init__ и др.']])
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M14L1 — классы и объекты
# ═══════════════════════════════════════════════════════════════════════════════
M14L1 = (
    '<h2>Классы и объекты — основа ООП</h2>'
    '<p>Класс — шаблон для создания объектов. '
    'Объект объединяет данные (атрибуты) и действия (методы). '
    'ООП позволяет моделировать реальный мир в коде.</p>'
    + diagram(650, 200, ARROW_DEF,
        svg_box(10, 80, 180, 120, '#e0f2fe', '#0284c7', 'class BankAccount\n\n  + balance: float\n  + owner: str\n\n  + deposit()\n  + withdraw()\n  + get_balance()'),
        arr(190, 120, 270, 80),
        arr(190, 140, 270, 160),
        svg_box(270, 50, 160, 60, '#dcfce7', '#16a34a', 'acc1 = BankAccount()\nbalance=1000\nowner="Alice"'),
        svg_box(270, 130, 160, 60, '#fef9c3', '#ca8a04', 'acc2 = BankAccount()\nbalance=500\nowner="Bob"'),
    )
    + code('python',
        'class BankAccount:\n'
        '    """Банковский счёт."""\n\n'
        '    bank_name = "PyBank"   # атрибут КЛАССА (общий)\n\n'
        '    def __init__(self, owner: str, balance: float = 0):\n'
        '        """Конструктор: вызывается при acc = BankAccount(...)"""\n'
        '        self.owner = owner         # атрибут ОБЪЕКТА\n'
        '        self._balance = balance    # _ = соглашение "приватный"\n'
        '        self._transactions = []\n\n'
        '    def deposit(self, amount: float) -> None:\n'
        '        if amount <= 0:\n'
        '            raise ValueError("Сумма должна быть положительной")\n'
        '        self._balance += amount\n'
        '        self._transactions.append(("deposit", amount))\n\n'
        '    def withdraw(self, amount: float) -> None:\n'
        '        if amount > self._balance:\n'
        '            raise ValueError("Недостаточно средств")\n'
        '        self._balance -= amount\n'
        '        self._transactions.append(("withdraw", amount))\n\n'
        '    @property\n'
        '    def balance(self) -> float:\n'
        '        return self._balance\n\n'
        '    def __repr__(self) -> str:\n'
        '        return f"BankAccount({self.owner!r}, balance={self._balance})"\n\n'
        '# Использование\n'
        'acc = BankAccount("Alice", 1000)\n'
        'acc.deposit(500)\n'
        'acc.withdraw(200)\n'
        'print(acc.balance)   # 1300\n'
        'print(acc)           # BankAccount("Alice", balance=1300)')
    + '<h3>Магические методы (__dunder__)</h3>'
    + table(['Метод', 'Когда вызывается'],
        [['__init__', 'Создание объекта: BankAccount()'],
         ['__repr__', 'repr(obj), отладчик'],
         ['__str__', 'str(obj), print()'],
         ['__len__', 'len(obj)'],
         ['__eq__', 'obj1 == obj2'],
         ['__lt__', 'obj1 < obj2 (и sorted())'],
         ['__add__', 'obj1 + obj2'],
         ['__enter__/__exit__', 'with obj as x:']])
    + tip('Первым параметром методов класса всегда идёт <code>self</code> — '
          'ссылка на текущий объект. Это соглашение (не ключевое слово), '
          'но его нарушение — плохой тон.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M14L2 — наследование
# ═══════════════════════════════════════════════════════════════════════════════
M14L2 = (
    '<h2>Наследование — переиспользование кода</h2>'
    '<p>Дочерний класс получает все атрибуты и методы родителя '
    'и может их переопределять или дополнять.</p>'
    + code('python',
        'class Animal:\n'
        '    def __init__(self, name: str, sound: str):\n'
        '        self.name = name\n'
        '        self.sound = sound\n\n'
        '    def speak(self) -> str:\n'
        '        return f"{self.name} говорит: {self.sound}!"\n\n'
        '    def __repr__(self):\n'
        '        return f"{type(self).__name__}({self.name!r})"\n\n'
        'class Dog(Animal):\n'
        '    def __init__(self, name: str, breed: str):\n'
        '        super().__init__(name, "Гав")   # вызываем родителя\n'
        '        self.breed = breed\n\n'
        '    def fetch(self) -> str:\n'
        '        return f"{self.name} принёс мяч!"\n\n'
        'class Cat(Animal):\n'
        '    def __init__(self, name: str):\n'
        '        super().__init__(name, "Мяу")\n\n'
        '    def speak(self) -> str:   # переопределение\n'
        '        return f"{self.name} говорит: {self.sound}~ (тихо)"\n\n'
        'dog = Dog("Rex", "Лабрадор")\n'
        'cat = Cat("Барсик")\n\n'
        'print(dog.speak())   # Rex говорит: Гав!\n'
        'print(cat.speak())   # Барсик говорит: Мяу~ (тихо)\n'
        'print(dog.fetch())   # Rex принёс мяч!')
    + '<h3>Полиморфизм</h3>'
    + code('python',
        '# Одна функция работает с разными типами\n'
        'animals = [Dog("Rex","Лабрадор"), Cat("Мурка"), Dog("Бобик","Дворняга")]\n\n'
        'for animal in animals:\n'
        '    print(animal.speak())   # каждый говорит по-своему')
    + '<h3>isinstance и issubclass</h3>'
    + code('python',
        'print(isinstance(dog, Dog))      # True\n'
        'print(isinstance(dog, Animal))   # True  (Dog — подкласс Animal)\n'
        'print(isinstance(dog, Cat))      # False\n'
        'print(issubclass(Dog, Animal))   # True')
    + '<h3>ABC — абстрактный базовый класс</h3>'
    + code('python',
        'from abc import ABC, abstractmethod\n\n'
        'class Shape(ABC):\n'
        '    @abstractmethod\n'
        '    def area(self) -> float: ...\n\n'
        '    @abstractmethod\n'
        '    def perimeter(self) -> float: ...\n\n'
        'class Circle(Shape):\n'
        '    def __init__(self, r): self.r = r\n'
        '    def area(self): return 3.14159 * self.r ** 2\n'
        '    def perimeter(self): return 2 * 3.14159 * self.r\n\n'
        'class Rectangle(Shape):\n'
        '    def __init__(self, w, h): self.w, self.h = w, h\n'
        '    def area(self): return self.w * self.h\n'
        '    def perimeter(self): return 2 * (self.w + self.h)\n\n'
        '# Shape() — ошибка: нельзя создать абстрактный класс\n'
        'shapes = [Circle(5), Rectangle(4, 6)]\n'
        'for s in shapes:\n'
        '    print(f"{type(s).__name__}: площадь={s.area():.2f}")')
    + tip('ABC гарантирует, что все подклассы реализуют обязательные методы. '
          'Это договор между автором базового класса и пользователями.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M28L1 — JSON
# ═══════════════════════════════════════════════════════════════════════════════
M28L1 = (
    '<h2>JSON — универсальный формат обмена данными</h2>'
    '<p>JSON (JavaScript Object Notation) используется в 99% REST API. '
    'Python автоматически конвертирует dict/list ↔ JSON.</p>'
    + code('python',
        'import json\n\n'
        '# Сериализация (Python -> JSON строка)\n'
        'data = {\n'
        '    "user": "Alice",\n'
        '    "age": 30,\n'
        '    "scores": [95, 87, 92],\n'
        '    "active": True,\n'
        '    "address": None\n'
        '}\n\n'
        'json_str = json.dumps(data, ensure_ascii=False, indent=2)\n'
        'print(json_str)\n\n'
        '# Десериализация (JSON строка -> Python)\n'
        'loaded = json.loads(json_str)\n'
        'print(loaded["user"])   # "Alice"')
    + table(['Python', 'JSON'],
        [['dict', 'object {}'],
         ['list, tuple', 'array []'],
         ['str', 'string'],
         ['int, float', 'number'],
         ['True/False', 'true/false'],
         ['None', 'null']])
    + '<h3>Чтение/запись JSON-файла</h3>'
    + code('python',
        '# Запись в файл\n'
        'config = {"host": "localhost", "port": 5432, "debug": False}\n\n'
        'with open("config.json", "w", encoding="utf-8") as f:\n'
        '    json.dump(config, f, indent=2, ensure_ascii=False)\n\n'
        '# Чтение из файла\n'
        'with open("config.json", encoding="utf-8") as f:\n'
        '    loaded_config = json.load(f)\n'
        'print(loaded_config["port"])  # 5432')
    + '<h3>Работа с реальным API</h3>'
    + code('python',
        'import json, urllib.request\n\n'
        'url = "https://jsonplaceholder.typicode.com/users/1"\n\n'
        'with urllib.request.urlopen(url) as response:\n'
        '    user = json.loads(response.read().decode())\n\n'
        'print(f"Имя: {user[\'name\']}")\n'
        'print(f"Email: {user[\'email\']}")\n'
        'print(f"Город: {user[\'address\'][\'city\']}")')
    + '<h3>JSONEncoder для своих типов</h3>'
    + code('python',
        'from datetime import datetime\n\n'
        'class DateTimeEncoder(json.JSONEncoder):\n'
        '    def default(self, obj):\n'
        '        if isinstance(obj, datetime):\n'
        '            return obj.isoformat()\n'
        '        return super().default(obj)\n\n'
        'data = {"created_at": datetime.now(), "name": "event"}\n'
        'print(json.dumps(data, cls=DateTimeEncoder))\n'
        '# {"created_at": "2025-01-15T14:30:00", "name": "event"}')
    + warn('Никогда не используйте <code>pickle</code> для данных из недоверенных источников '
           '(API, пользователи). Pickle выполняет произвольный код при десериализации. '
           'JSON — безопасная альтернатива.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M28L2 — CSV
# ═══════════════════════════════════════════════════════════════════════════════
M28L2 = (
    '<h2>CSV — табличные данные</h2>'
    '<p>CSV (Comma-Separated Values) — самый распространённый формат для таблиц: '
    'Excel, Google Sheets, базы данных экспортируют в CSV.</p>'
    + code('python',
        'import csv\n\n'
        '# Запись CSV\n'
        'students = [\n'
        '    ["Имя", "Оценка", "Предмет"],\n'
        '    ["Alice", 95, "Математика"],\n'
        '    ["Bob", 87, "Физика"],\n'
        '    ["Carol", 92, "Информатика"],\n'
        ']\n\n'
        'with open("students.csv", "w", newline="", encoding="utf-8") as f:\n'
        '    writer = csv.writer(f)\n'
        '    writer.writerows(students)\n\n'
        '# Чтение CSV\n'
        'with open("students.csv", encoding="utf-8") as f:\n'
        '    reader = csv.DictReader(f)\n'
        '    for row in reader:\n'
        '        print(f"{row[\'Имя\']}: {row[\'Оценка\']} ({row[\'Предмет\']})")')
    + '<h3>DictWriter — запись из словарей</h3>'
    + code('python',
        'employees = [\n'
        '    {"name": "Alice", "dept": "Eng", "salary": 150000},\n'
        '    {"name": "Bob",   "dept": "HR",  "salary": 90000},\n'
        ']\n\n'
        'with open("employees.csv", "w", newline="", encoding="utf-8") as f:\n'
        '    writer = csv.DictWriter(f, fieldnames=["name", "dept", "salary"])\n'
        '    writer.writeheader()\n'
        '    writer.writerows(employees)')
    + '<h3>Анализ CSV без Pandas</h3>'
    + code('python',
        'from collections import defaultdict\n\n'
        '# Агрегация продаж по отделу\n'
        'dept_sales = defaultdict(float)\n\n'
        'with open("sales.csv", encoding="utf-8") as f:\n'
        '    for row in csv.DictReader(f):\n'
        '        dept = row["department"]\n'
        '        amount = float(row["amount"])\n'
        '        dept_sales[dept] += amount\n\n'
        'for dept, total in sorted(dept_sales.items(), key=lambda x: -x[1]):\n'
        '    print(f"{dept}: {total:,.0f} руб.")')
    + tip('Параметр <code>newline=""</code> обязателен при открытии CSV на Windows — '
          'без него возникнут лишние пустые строки из-за CRLF.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M28L3 — datetime
# ═══════════════════════════════════════════════════════════════════════════════
M28L3 = (
    '<h2>datetime: дата и время в Python</h2>'
    + code('python',
        'from datetime import datetime, date, timedelta, timezone\n\n'
        '# Текущее время\n'
        'now = datetime.now()                   # локальное\n'
        'utc = datetime.now(timezone.utc)       # UTC (рекомендуется для серверов)\n\n'
        '# Создание\n'
        'birthday = date(1990, 5, 15)\n'
        'meeting = datetime(2025, 3, 20, 14, 30)  # 20 марта 14:30\n\n'
        '# Форматирование\n'
        'print(now.strftime("%d.%m.%Y %H:%M"))  # 29.05.2025 14:30\n\n'
        '# Парсинг строки\n'
        'dt = datetime.strptime("2025-01-15", "%Y-%m-%d")\n'
        'print(dt.year, dt.month, dt.day)       # 2025 1 15')
    + '<h3>timedelta — арифметика времени</h3>'
    + code('python',
        'from datetime import datetime, timedelta\n\n'
        'now = datetime.now()\n\n'
        '# Через 30 дней\n'
        'deadline = now + timedelta(days=30)\n'
        'print(deadline.strftime("%d.%m.%Y"))\n\n'
        '# Разница между датами\n'
        'start = datetime(2025, 1, 1)\n'
        'end   = datetime(2025, 5, 29)\n'
        'delta = end - start\n'
        'print(f"Прошло {delta.days} дней")    # 148 дней\n\n'
        '# Возраст человека\n'
        'birthday = date(1990, 5, 15)\n'
        'today = date.today()\n'
        'age = (today - birthday).days // 365\n'
        'print(f"Возраст: {age} лет")')
    + '<h3>Часовые пояса с zoneinfo (Python 3.9+)</h3>'
    + code('python',
        'from zoneinfo import ZoneInfo\n'
        'from datetime import datetime\n\n'
        'moscow = ZoneInfo("Europe/Moscow")\n'
        'ny     = ZoneInfo("America/New_York")\n\n'
        'meeting_moscow = datetime(2025, 6, 1, 15, 0, tzinfo=moscow)\n'
        'meeting_ny = meeting_moscow.astimezone(ny)\n\n'
        'print(f"Москва: {meeting_moscow.strftime(\"%H:%M\")}")  # 15:00\n'
        'print(f"Нью-Йорк: {meeting_ny.strftime(\"%H:%M\")}")    # 07:00')
    + warn('Всегда храните время в UTC в базе данных. '
           'Конвертируйте в локальный часовой пояс только при отображении. '
           'Смешивание aware и naive datetime вызовет TypeError.')
    + '<h3>Реальный кейс: SLA-мониторинг</h3>'
    + code('python',
        'from datetime import datetime, timedelta, timezone\n\n'
        'class Ticket:\n'
        '    def __init__(self, title: str, priority: str):\n'
        '        self.title = title\n'
        '        self.created_at = datetime.now(timezone.utc)\n'
        '        # SLA: критично=4ч, высокий=8ч, обычный=24ч\n'
        '        sla_hours = {"critical": 4, "high": 8, "normal": 24}\n'
        '        self.deadline = self.created_at + timedelta(\n'
        '            hours=sla_hours.get(priority, 24))\n\n'
        '    def is_overdue(self) -> bool:\n'
        '        return datetime.now(timezone.utc) > self.deadline\n\n'
        '    def time_left(self) -> str:\n'
        '        delta = self.deadline - datetime.now(timezone.utc)\n'
        '        if delta.total_seconds() < 0:\n'
        '            return f"Просрочено на {-delta}"\n'
        '        h, m = divmod(int(delta.total_seconds()) // 60, 60)\n'
        '        return f"Осталось {h}ч {m}м"')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M33L1 — аннотации типов
# ═══════════════════════════════════════════════════════════════════════════════
M33L1 = (
    '<h2>Аннотации типов: статическая типизация в Python</h2>'
    '<p>Python — динамически типизированный язык, но с версии 3.5+ поддерживает '
    'аннотации типов. Они не влияют на выполнение, но помогают IDE и линтерам '
    'находить ошибки до запуска.</p>'
    + code('python',
        'from typing import Optional, Union, List, Dict, Tuple\n\n'
        '# Базовые аннотации\n'
        'def greet(name: str, repeat: int = 1) -> str:\n'
        '    return (f"Hello, {name}! " * repeat).strip()\n\n'
        '# Optional[X] == Union[X, None]\n'
        'def find_user(user_id: int) -> Optional[dict]:\n'
        '    db = {1: {"name": "Alice"}, 2: {"name": "Bob"}}\n'
        '    return db.get(user_id)  # может вернуть None\n\n'
        '# Современный синтаксис (Python 3.10+)\n'
        'def process(value: int | str | None) -> str:\n'
        '    if value is None: return "empty"\n'
        '    return str(value)')
    + '<h3>Аннотации для коллекций</h3>'
    + code('python',
        'from typing import List, Dict, Set, Tuple\n\n'
        '# Python 3.9+: можно писать list[str] вместо List[str]\n'
        'def total_score(scores: list[int]) -> float:\n'
        '    return sum(scores) / len(scores)\n\n'
        'def group_by_grade(students: list[dict]) -> dict[str, list[str]]:\n'
        '    result: dict[str, list[str]] = {}\n'
        '    for s in students:\n'
        '        grade = s["grade"]\n'
        '        result.setdefault(grade, []).append(s["name"])\n'
        '    return result')
    + '<h3>TypeAlias и NewType</h3>'
    + code('python',
        'from typing import NewType\n\n'
        '# NewType создаёт "тип-обёртку" — предотвращает путаницу\n'
        'UserId  = NewType("UserId", int)\n'
        'OrderId = NewType("OrderId", int)\n\n'
        'def get_user(user_id: UserId) -> dict: ...\n\n'
        'uid = UserId(42)\n'
        'oid = OrderId(42)\n\n'
        '# mypy поймает: get_user(oid) — это ошибка!\n'
        '# get_user(oid)  # error: Argument 1 has incompatible type "OrderId"')
    + '<h3>Проверка через mypy</h3>'
    + code('bash',
        'pip install mypy\n'
        'mypy my_script.py\n'
        '# my_script.py:15: error: Argument 1 to "get_user" has incompatible type')
    + tip('Включите mypy в CI/CD пайплайн. Крупные компании (Dropbox, Google, '
          'Instagram) внедрили mypy и нашли тысячи скрытых багов в legacy-коде.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M36L2 — Mock, coverage, TDD
# ═══════════════════════════════════════════════════════════════════════════════
M36L2 = (
    '<h2>Mock, coverage и TDD</h2>'
    '<h3>Mock — заглушки для внешних зависимостей</h3>'
    '<p>Тест не должен зависеть от БД, API или файловой системы. '
    'Mock заменяет реальные зависимости контролируемыми объектами.</p>'
    + code('python',
        'from unittest.mock import Mock, patch, MagicMock\n'
        'import pytest\n\n'
        'class WeatherService:\n'
        '    def get_temperature(self, city: str) -> float:\n'
        '        # В реальности — HTTP-запрос\n'
        '        import requests\n'
        '        r = requests.get(f"https://api.weather.com/{city}")\n'
        '        return r.json()["temp"]\n\n'
        'def should_wear_coat(service, city: str) -> bool:\n'
        '    return service.get_temperature(city) < 10\n\n'
        '# Тест с Mock\n'
        'def test_should_wear_coat_cold():\n'
        '    mock_service = Mock()\n'
        '    mock_service.get_temperature.return_value = 5.0\n\n'
        '    assert should_wear_coat(mock_service, "Moscow") == True\n'
        '    mock_service.get_temperature.assert_called_once_with("Moscow")\n\n'
        'def test_should_wear_coat_warm():\n'
        '    mock_service = Mock()\n'
        '    mock_service.get_temperature.return_value = 25.0\n\n'
        '    assert should_wear_coat(mock_service, "Moscow") == False')
    + '<h3>patch — замена объектов в модуле</h3>'
    + code('python',
        '# Патчинг requests.get без изменения кода\n'
        '@patch("requests.get")\n'
        'def test_api_call(mock_get):\n'
        '    mock_response = Mock()\n'
        '    mock_response.json.return_value = {"temp": 3.5}\n'
        '    mock_response.status_code = 200\n'
        '    mock_get.return_value = mock_response\n\n'
        '    service = WeatherService()\n'
        '    temp = service.get_temperature("Moscow")\n\n'
        '    assert temp == 3.5\n'
        '    mock_get.assert_called_once()')
    + '<h3>pytest-cov — покрытие кода</h3>'
    + code('bash',
        'pip install pytest-cov\n\n'
        '# Запуск с отчётом покрытия\n'
        'pytest --cov=mymodule --cov-report=term-missing\n\n'
        '# -------- coverage: mymodule.py --------\n'
        '# Name          Stmts   Miss  Cover   Missing\n'
        '# mymodule.py      45      8    82%   12,25-30')
    + '<h3>TDD — разработка через тесты</h3>'
    + code('python',
        '# Шаг 1: RED — написать тест (он падает)\n'
        'def test_password_strength():\n'
        '    assert check_strength("abc") == "weak"\n'
        '    assert check_strength("Abc123") == "medium"\n'
        '    assert check_strength("Abc123!@#") == "strong"\n\n'
        '# Шаг 2: GREEN — написать минимальную реализацию\n'
        'def check_strength(password: str) -> str:\n'
        '    score = 0\n'
        '    if len(password) >= 8: score += 1\n'
        '    if any(c.isupper() for c in password): score += 1\n'
        '    if any(c.isdigit() for c in password): score += 1\n'
        '    if any(c in "!@#$%^&*" for c in password): score += 1\n'
        '    return ["weak","weak","medium","strong","strong"][score]\n\n'
        '# Шаг 3: REFACTOR — улучшить код, не сломав тесты')
    + info('Индустриальная норма: 80%+ покрытие тестами. '
           'Критичные модули (финансы, безопасность) — 90-100%.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M42L1 — logging
# ═══════════════════════════════════════════════════════════════════════════════
M42L1 = (
    '<h2>logging — профессиональные журналы событий</h2>'
    '<p>print() хорош для отладки, но в продакшене нужен logging: '
    'уровни важности, запись в файл, ротация логов, структурированный формат.</p>'
    + code('python',
        'import logging\n\n'
        '# Базовая настройка\n'
        'logging.basicConfig(\n'
        '    level=logging.DEBUG,\n'
        '    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",\n'
        '    datefmt="%Y-%m-%d %H:%M:%S"\n'
        ')\n\n'
        'logger = logging.getLogger(__name__)\n\n'
        'logger.debug("Детали для разработчика")\n'
        'logger.info("Сервер запущен на порту 8000")\n'
        'logger.warning("Высокая загрузка CPU: 85%")\n'
        'logger.error("Не удалось подключиться к БД")\n'
        'logger.critical("Диск заполнен на 100%!")\n\n'
        '# 2025-05-29 14:30:00 [INFO] __main__: Сервер запущен на порту 8000\n'
        '# 2025-05-29 14:30:00 [WARNING] __main__: Высокая загрузка CPU: 85%')
    + table(['Уровень', 'Значение', 'Использование'],
        [['DEBUG', '10', 'Отладочные детали'],
         ['INFO', '20', 'Штатные события'],
         ['WARNING', '30', 'Нештатные, но не критичные'],
         ['ERROR', '40', 'Ошибки, требующие внимания'],
         ['CRITICAL', '50', 'Катастрофические сбои']])
    + '<h3>Логирование в файл с ротацией</h3>'
    + code('python',
        'import logging\n'
        'from logging.handlers import RotatingFileHandler\n\n'
        'logger = logging.getLogger("myapp")\n'
        'logger.setLevel(logging.INFO)\n\n'
        '# Ротация: max 10MB, хранить 5 файлов\n'
        'handler = RotatingFileHandler(\n'
        '    "app.log",\n'
        '    maxBytes=10 * 1024 * 1024,\n'
        '    backupCount=5,\n'
        '    encoding="utf-8"\n'
        ')\n'
        'handler.setFormatter(logging.Formatter(\n'
        '    "%(asctime)s [%(levelname)s] %(message)s"\n'
        '))\n'
        'logger.addHandler(handler)')
    + '<h3>Логирование исключений</h3>'
    + code('python',
        'try:\n'
        '    result = risky_operation()\n'
        'except Exception as e:\n'
        '    logger.exception("Ошибка в risky_operation")  # логирует traceback!\n'
        '    # exc_info=True — автоматически добавляет traceback в лог\n\n'
        '# Добавление контекста\n'
        'logger.info("Пользователь вошёл", extra={"user_id": 42, "ip": "127.0.0.1"})')
    + tip('Никогда не логируйте пароли, токены и персональные данные. '
          'Используйте маскирование: <code>token[:4] + "****"</code>.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PATCHES dict
# ═══════════════════════════════════════════════════════════════════════════════
PATCHES = {
    (3, 1):  M3L1,
    (4, 1):  M4L1,
    (5, 1):  M5L1,
    (5, 2):  M5L2,
    (6, 1):  M6L1,
    (6, 2):  M6L2,
    (7, 1):  M7L1,
    (7, 2):  M7L2,
    (8, 1):  M8L1,
    (8, 2):  M8L2,
    (9, 1):  M9L1,
    (10, 1): M10L1,
    (11, 1): M11L1,
    (14, 1): M14L1,
    (14, 2): M14L2,
    (28, 1): M28L1,
    (28, 2): M28L2,
    (28, 3): M28L3,
    (33, 1): M33L1,
    (36, 2): M36L2,
    (42, 1): M42L1,
}


class Command(BaseCommand):
    help = 'Вторая волна расширения тонких уроков Python'

    def handle(self, *args, **options):
        try:
            subject = Subject.objects.get(slug='python')
        except Subject.DoesNotExist:
            self.stderr.write('Subject python not found')
            return

        modules = list(TheoryModule.objects.filter(subject=subject).order_by('order'))
        # first occurrence wins for duplicate orders
        mod_map = {}
        for m in modules:
            if m.order not in mod_map:
                mod_map[m.order] = m

        patched = 0
        results = []
        for (mo, lo), extra in PATCHES.items():
            if mo not in mod_map:
                results.append('M%dL%d: MODULE NOT FOUND' % (mo, lo))
                continue
            try:
                lesson = TheoryLesson.objects.filter(module=mod_map[mo], order=lo).order_by('id').first()
                if lesson is None:
                    raise TheoryLesson.DoesNotExist
            except TheoryLesson.DoesNotExist:
                results.append('M%dL%d: LESSON NOT FOUND' % (mo, lo))
                continue

            old_len = len(lesson.content)
            lesson.content += extra
            lesson.estimated_minutes = max(lesson.estimated_minutes or 0, 20)
            lesson.save()
            new_len = len(lesson.content)
            results.append('M%dL%d: %d -> %d ch (+%d)' % (mo, lo, old_len, new_len, new_len - old_len))
            patched += 1

        for r in results:
            self.stdout.write(r)
        self.stdout.write('Done: %d lessons enriched' % patched)
