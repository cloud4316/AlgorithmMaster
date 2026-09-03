"""python manage.py seed_theory_oaip — модули 21-30 (ОАИП расширенный)"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject


def tip(text):
    return f'<div class="tip">💡 {text}</div>'

def warn(text):
    return f'<div class="warning">⚠️ {text}</div>'

def info(text):
    return f'<div class="tip" style="background:#e0f2fe;border-color:#0284c7">ℹ️ {text}</div>'

def table(headers, rows):
    th = ''.join(f'<th>{c}</th>' for c in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def diagram(inner_svg, w=600, h=300, caption=''):
    return (
        f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
        f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;'
        f'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">'
        f'{inner_svg}</svg>'
        f'<p style="text-align:center;color:#64748b;font-size:13px">{caption}</p></div>'
    )


MODULES = [

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 21 — COMPREHENSIONS И LAMBDA
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Comprehensions и lambda',
'icon': 'fas fa-filter',
'order': 21,
'description': 'List/dict/set comprehensions, generator expressions, lambda-функции, map, filter, reduce.',
'lessons': [
{
'title': 'List comprehensions',
'order': 1,
'estimated_minutes': 55,
'content': '''
<h2>List Comprehensions — компактные списки</h2>
<p><strong>List comprehension</strong> — это краткий синтаксис для создания нового списка путём преобразования или фильтрации элементов другого итерируемого объекта. Это одна из самых любимых возможностей Python, делающая код одновременно короче и читаемее.</p>
''' + diagram(
    '<rect x="20" y="30" width="560" height="60" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>'
    '<text x="300" y="55" text-anchor="middle" font-size="15" fill="#1e40af" font-family="monospace">[  выражение  for  переменная  in  последовательность  if  условие  ]</text>'
    '<text x="80" y="85" text-anchor="middle" font-size="11" fill="#64748b">результат</text>'
    '<text x="230" y="85" text-anchor="middle" font-size="11" fill="#64748b">итерация</text>'
    '<text x="420" y="85" text-anchor="middle" font-size="11" fill="#64748b">фильтр (опционально)</text>'
    '<line x1="80" y1="90" x2="80" y2="92" stroke="#64748b" stroke-width="1"/>'
    '<rect x="20" y="120" width="120" height="30" rx="5" fill="#dbeafe"/>'
    '<text x="80" y="140" text-anchor="middle" font-size="12" fill="#1e40af">квадраты чисел</text>'
    '<rect x="160" y="120" width="160" height="30" rx="5" fill="#dcfce7"/>'
    '<text x="240" y="140" text-anchor="middle" font-size="12" fill="#166534">фильтрация чётных</text>'
    '<rect x="340" y="120" width="180" height="30" rx="5" fill="#fef9c3"/>'
    '<text x="430" y="140" text-anchor="middle" font-size="12" fill="#854d0e">преобразование строк</text>'
    '<text x="80" y="175" text-anchor="middle" font-size="11" fill="#1e40af" font-family="monospace">[x**2 for x in range(10)]</text>'
    '<text x="240" y="175" text-anchor="middle" font-size="11" fill="#166534" font-family="monospace">[x for x in lst if x%2==0]</text>'
    '<text x="430" y="175" text-anchor="middle" font-size="11" fill="#854d0e" font-family="monospace">[s.upper() for s in words]</text>',
    w=600, h=190, caption='Синтаксис list comprehension и примеры'
) + '''
<h3>Базовый синтаксис</h3>
<p>Общая форма: <code>[выражение for элемент in итерируемое if условие]</code></p>
<p>Часть <code>if условие</code> — необязательная. Без неё берутся все элементы.</p>
''' + table(
    ['Обычный цикл', 'List comprehension'],
    [
        ['result = []<br>for x in range(5):<br>&nbsp;&nbsp;result.append(x**2)', '[x**2 for x in range(5)]'],
        ['result = []<br>for x in lst:<br>&nbsp;&nbsp;if x > 0:<br>&nbsp;&nbsp;&nbsp;&nbsp;result.append(x)', '[x for x in lst if x > 0]'],
        ['result = []<br>for s in words:<br>&nbsp;&nbsp;result.append(s.upper())', '[s.upper() for s in words]'],
    ]
) + tip('List comprehension всегда возвращает новый список. Исходный объект не изменяется.') + '''
<h3>Вложенные comprehensions</h3>
<p>Можно использовать несколько <code>for</code> — вложенные циклы в одной строке:</p>
<pre><code># Декартово произведение
pairs = [(x, y) for x in [1, 2, 3] for y in ['a', 'b']]
# [(1,'a'), (1,'b'), (2,'a'), (2,'b'), (3,'a'), (3,'b')]

# Разворот матрицы (транспонирование)
matrix = [[1,2,3],[4,5,6],[7,8,9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
</code></pre>
''' + warn('Вложенные comprehensions читаются справа налево по циклам. Более двух уровней вложенности обычно снижают читаемость — тогда лучше явные циклы.') + '''
<h3>Comprehension с условием else (тернарный оператор)</h3>
<p>Если нужно задать два варианта результата (не фильтрацию), используется тернарный оператор ПЕРЕД for:</p>
<pre><code># Заменить отрицательные на 0
result = [x if x > 0 else 0 for x in numbers]

# Классификация
labels = ['чётное' if x % 2 == 0 else 'нечётное' for x in range(8)]
</code></pre>
''' + info('Важно: <code>[x if cond else y for x in seq]</code> — тернарный оператор (преобразование всех элементов). <code>[x for x in seq if cond]</code> — фильтрация (некоторые элементы отбрасываются).') + '''
<h3>Практические применения</h3>
<ul>
  <li><strong>Очистка данных:</strong> <code>[s.strip().lower() for s in lines if s.strip()]</code></li>
  <li><strong>Извлечение полей:</strong> <code>[person['name'] for person in people]</code></li>
  <li><strong>Числовые преобразования:</strong> <code>[round(x * 1.2, 2) for x in prices]</code></li>
  <li><strong>Проверка условий:</strong> <code>[x for x in nums if 10 <= x <= 100]</code></li>
</ul>
''',
'code_example': '''# List comprehensions — практика

# 1. Квадраты нечётных чисел от 1 до 20
odd_squares = [x**2 for x in range(1, 21) if x % 2 != 0]
print("Квадраты нечётных:", odd_squares)

# 2. Слова длиннее 4 букв в верхнем регистре
words = ["python", "is", "great", "for", "data", "science"]
long_words = [w.upper() for w in words if len(w) > 4]
print("Длинные слова:", long_words)

# 3. Таблица умножения через вложенный comprehension
mult_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
for row in mult_table:
    print(row)

# 4. Разворот матрицы
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print("Транспонированная:", transposed)

# 5. Фильтрация и преобразование словаря
students = [
    {"name": "Иван", "grade": 85},
    {"name": "Мария", "grade": 92},
    {"name": "Пётр", "grade": 60},
]
honor_roll = [s["name"] for s in students if s["grade"] >= 80]
print("Отличники:", honor_roll)
'''
},

{
'title': 'Dict/set comprehensions и генераторы',
'order': 2,
'estimated_minutes': 50,
'content': '''
<h2>Dict и Set Comprehensions</h2>
<p>Аналогично list comprehension, Python поддерживает создание словарей и множеств компактным синтаксисом.</p>
<h3>Dict comprehension</h3>
<p>Форма: <code>{ключ: значение for элемент in итерируемое if условие}</code></p>
<pre><code># Квадраты чисел в словаре
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Инвертировать словарь
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Слова → их длины
words = ['python', 'java', 'go']
lengths = {w: len(w) for w in words}
</code></pre>
<h3>Set comprehension</h3>
<p>Форма: <code>{выражение for элемент in итерируемое}</code> — возвращает <strong>множество</strong> (уникальные элементы, без порядка).</p>
<pre><code># Уникальные длины слов
lengths = {len(w) for w in ['cat', 'dog', 'elephant', 'ox', 'ant']}
# {2, 3, 8} (порядок может отличаться)

# Уникальные первые буквы
initials = {name[0].upper() for name in names if name}
</code></pre>
''' + tip('Фигурные скобки <code>{}</code> с одним выражением — set comprehension. С двумя через двоеточие <code>key: val</code> — dict comprehension. Пустые <code>{}</code> — это dict, не set! Пустое множество: <code>set()</code>.') + '''
<h2>Generator Expressions — ленивые вычисления</h2>
<p><strong>Generator expression</strong> (генераторное выражение) — это как list comprehension, но в круглых скобках. Разница фундаментальная: list comprehension создаёт весь список сразу в памяти, а генератор вычисляет элементы <em>по одному, по мере необходимости</em>.</p>
''' + diagram(
    '<rect x="10" y="20" width="270" height="120" rx="8" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5"/>'
    '<text x="145" y="45" text-anchor="middle" font-size="13" fill="#991b1b" font-weight="bold">List Comprehension</text>'
    '<text x="145" y="65" text-anchor="middle" font-size="11" fill="#7f1d1d">[x**2 for x in range(1000)]</text>'
    '<rect x="30" y="75" width="230" height="55" rx="4" fill="#fca5a5"/>'
    '<text x="145" y="95" text-anchor="middle" font-size="11" fill="#7f1d1d">Память: все 1000 значений</text>'
    '<text x="145" y="112" text-anchor="middle" font-size="11" fill="#7f1d1d">сразу в списке ~8 КБ</text>'
    '<rect x="320" y="20" width="270" height="120" rx="8" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>'
    '<text x="455" y="45" text-anchor="middle" font-size="13" fill="#14532d" font-weight="bold">Generator Expression</text>'
    '<text x="455" y="65" text-anchor="middle" font-size="11" fill="#14532d">(x**2 for x in range(1000))</text>'
    '<rect x="340" y="75" width="230" height="55" rx="4" fill="#86efac"/>'
    '<text x="455" y="95" text-anchor="middle" font-size="11" fill="#14532d">Память: только один</text>'
    '<text x="455" y="112" text-anchor="middle" font-size="11" fill="#14532d">объект-генератор ~120 байт</text>'
    '<text x="300" y="170" text-anchor="middle" font-size="12" fill="#475569">Результат одинаковый, но генератор экономит память в 60+ раз</text>',
    w=600, h=190, caption='List vs Generator: потребление памяти'
) + '''
<h3>Когда использовать генераторы</h3>
''' + table(
    ['Ситуация', 'Используй', 'Почему'],
    [
        ['Нужен список для нескольких обращений', 'List comprehension', 'Генератор можно пройти только раз'],
        ['Большие данные (100к+ элементов)', 'Generator expression', 'Экономия памяти'],
        ['Передать в sum(), max(), any()', 'Generator expression', 'Они принимают любой итерируемый'],
        ['Нужна индексация result[3]', 'List comprehension', 'Генератор не поддерживает индексы'],
        ['Pipeline обработка данных', 'Generator expression', 'Ленивые вычисления'],
    ]
) + warn('Генератор можно пройти только один раз! После исчерпания он пуст. Если нужно несколько проходов — используй list.') + '''
<h3>Передача в функции</h3>
<pre><code># Если передаёшь генератор единственным аргументом — можно убрать одну скобку
total = sum(x**2 for x in range(100))  # не sum((x**2 for x in range(100)))
maximum = max(len(word) for word in text.split())
exists = any(grade > 90 for grade in grades)
</code></pre>
''',
'code_example': '''import sys

# Dict comprehension
squares_dict = {x: x**2 for x in range(1, 8)}
print("Квадраты:", squares_dict)

inverted = {v: k for k, v in squares_dict.items()}
print("Инвертированный:", inverted)

# Set comprehension — уникальные длины
words = ["apple", "bee", "cat", "door", "elk", "frog"]
unique_lengths = {len(w) for w in words}
print("Уникальные длины:", unique_lengths)

# Сравнение памяти: list vs generator
n = 100_000
list_comp = [x**2 for x in range(n)]
gen_exp   = (x**2 for x in range(n))

print(f"Список:   {sys.getsizeof(list_comp):,} байт")
print(f"Генератор:{sys.getsizeof(gen_exp):,} байт")

# Практический pipeline с генераторами
data = ["  3.14 ", "error", "  2.71 ", "N/A", "  1.41 "]

def safe_float(s):
    try:
        return float(s.strip())
    except ValueError:
        return None

numbers = (safe_float(s) for s in data)
valid   = (x for x in numbers if x is not None)
result  = sum(valid)
print(f"Сумма валидных: {result}")
'''
},

{
'title': 'lambda, map, filter, reduce',
'order': 3,
'estimated_minutes': 55,
'content': '''
<h2>Lambda-функции</h2>
<p><strong>Lambda</strong> — анонимная функция, которая определяется в одном выражении. Синтаксис: <code>lambda параметры: выражение</code>.</p>
<pre><code># Обычная функция vs lambda
def square(x):
    return x ** 2

square_lambda = lambda x: x ** 2

# Несколько параметров
add = lambda x, y: x + y
clamp = lambda x, lo, hi: max(lo, min(x, hi))
</code></pre>
''' + table(
    ['Характеристика', 'def', 'lambda'],
    [
        ['Имя', 'Обязательно', 'Нет (анонимная)'],
        ['Тело', 'Любые операторы', 'Одно выражение'],
        ['return', 'Явный', 'Неявный (само выражение)'],
        ['Документация (docstring)', 'Да', 'Нет'],
        ['Типичное применение', 'Переиспользуемые функции', 'Короткие колбэки'],
    ]
) + tip('Лямбды чаще всего передают как аргумент в другую функцию — сортировку, map, filter и т.д. Если функция нужна в нескольких местах — лучше написать def.') + '''
<h2>map() и filter()</h2>
<p><strong><code>map(func, iterable)</code></strong> — применяет функцию к каждому элементу. Возвращает объект-итератор (не список!).</p>
<p><strong><code>filter(func, iterable)</code></strong> — оставляет только элементы, для которых функция вернула <code>True</code>.</p>
<pre><code>numbers = [1, -2, 3, -4, 5, -6]

# map — применить abs к каждому
absolutes = list(map(abs, numbers))          # [1, 2, 3, 4, 5, 6]

# filter — только положительные
positives = list(filter(lambda x: x > 0, numbers))  # [1, 3, 5]

# Эквиваленты через comprehension (часто предпочтительнее)
absolutes2 = [abs(x) for x in numbers]
positives2 = [x for x in numbers if x > 0]
</code></pre>
''' + diagram(
    '<rect x="20" y="20" width="80" height="30" rx="5" fill="#dbeafe"/>'
    '<text x="60" y="40" text-anchor="middle" font-size="11" fill="#1e40af">[1,-2,3,-4]</text>'
    '<rect x="140" y="15" width="80" height="40" rx="5" fill="#ede9fe"/>'
    '<text x="180" y="38" text-anchor="middle" font-size="12" fill="#5b21b6">map(abs)</text>'
    '<line x1="100" y1="35" x2="138" y2="35" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>'
    '<rect x="260" y="20" width="80" height="30" rx="5" fill="#dcfce7"/>'
    '<text x="300" y="40" text-anchor="middle" font-size="11" fill="#166534">[1,2,3,4]</text>'
    '<line x1="220" y1="35" x2="258" y2="35" stroke="#94a3b8" stroke-width="1.5"/>'
    '<rect x="380" y="15" width="80" height="40" rx="5" fill="#fef9c3"/>'
    '<text x="420" y="38" text-anchor="middle" font-size="12" fill="#854d0e">filter(&gt;2)</text>'
    '<line x1="340" y1="35" x2="378" y2="35" stroke="#94a3b8" stroke-width="1.5"/>'
    '<rect x="500" y="20" width="80" height="30" rx="5" fill="#fee2e2"/>'
    '<text x="540" y="40" text-anchor="middle" font-size="11" fill="#991b1b">[3,4]</text>'
    '<line x1="460" y1="35" x2="498" y2="35" stroke="#94a3b8" stroke-width="1.5"/>'
    '<text x="300" y="80" text-anchor="middle" font-size="11" fill="#64748b">Pipeline: источник → map → filter → результат</text>',
    w=600, h=100, caption='Цепочка: источник → map → filter'
) + '''
<h2>functools.reduce()</h2>
<p><strong><code>reduce(func, iterable)</code></strong> — сворачивает список к одному значению, применяя функцию попарно: сначала к первым двум элементам, затем к результату и третьему и т.д.</p>
<pre><code>from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Сумма через reduce
total = reduce(lambda acc, x: acc + x, numbers)  # 15

# Произведение
product = reduce(lambda acc, x: acc * x, numbers)  # 120

# Максимум без встроенной функции
maximum = reduce(lambda a, b: a if a > b else b, numbers)  # 5
</code></pre>
''' + warn('reduce() не является встроенной — нужен <code>from functools import reduce</code>. В большинстве случаев проще использовать sum(), max(), min() или цикл.') + '''
<h3>Практический совет</h3>
<p>В современном Python comprehensions обычно читаются лучше, чем map/filter с lambda. Выбор зависит от контекста:</p>
<ul>
<li><code>sorted(data, key=lambda x: x['score'])</code> — лямбда незаменима как key-функция</li>
<li><code>[x*2 for x in data]</code> — comprehension читается лучше чем <code>map(lambda x: x*2, data)</code></li>
<li><code>map(str, numbers)</code> — map с готовой функцией (без lambda) лаконичен</li>
</ul>
''',
'code_example': '''from functools import reduce

# Lambda как key для сортировки
students = [
    {"name": "Анна", "grade": 88, "age": 20},
    {"name": "Борис", "grade": 95, "age": 19},
    {"name": "Вера", "grade": 88, "age": 21},
]

by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
by_grade_then_age = sorted(students, key=lambda s: (-s["grade"], s["age"]))
print([s["name"] for s in by_grade_then_age])

# map с готовой функцией
numbers = [1, 4, 9, 16, 25]
roots = list(map(float.__pow__, [1.0]*5, [0.5]*5))  # нет, используем:
roots = list(map(lambda x: x**0.5, numbers))
print("Корни:", roots)

# filter: только простые числа
def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

primes = list(filter(is_prime, range(2, 30)))
print("Простые до 30:", primes)

# reduce: факториал
factorial = lambda n: reduce(lambda a, b: a * b, range(1, n+1), 1)
print("10! =", factorial(10))
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 22 — СЛОЖНОСТЬ АЛГОРИТМОВ (BIG O)
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Сложность алгоритмов (Big O)',
'icon': 'fas fa-chart-line',
'order': 22,
'description': 'Нотация Big O, анализ временной и пространственной сложности, сравнение алгоритмов.',
'lessons': [
{
'title': 'Что такое Big O: O(1), O(n), O(log n)',
'order': 1,
'estimated_minutes': 60,
'content': '''
<h2>Зачем нужна нотация Big O?</h2>
<p>Когда мы пишем алгоритм, нас интересует: как изменится время его работы при увеличении входных данных? Ответ даёт <strong>нотация Big O</strong> — математический способ описания роста числа операций в зависимости от размера задачи <em>n</em>.</p>
<p>Big O описывает <strong>верхнюю границу</strong> роста — наихудший сценарий. Константные множители и несущественные слагаемые отбрасываются: <code>O(2n + 5)</code> → <code>O(n)</code>.</p>
''' + diagram(
    '<rect x="10" y="10" width="580" height="240" rx="8" fill="#f8fafc"/>'
    '<line x1="50" y1="220" x2="570" y2="220" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="50" y1="220" x2="50" y2="20" stroke="#94a3b8" stroke-width="1.5"/>'
    '<text x="310" y="248" text-anchor="middle" font-size="12" fill="#64748b">Размер входных данных (n)</text>'
    '<text x="20" y="120" text-anchor="middle" font-size="12" fill="#64748b" transform="rotate(-90,20,120)">Операции</text>'
    '<line x1="50" y1="200" x2="550" y2="200" stroke="#16a34a" stroke-width="2.5"/>'
    '<text x="555" y="204" font-size="11" fill="#16a34a">O(1)</text>'
    '<line x1="50" y1="200" x2="550" y2="90" stroke="#2563eb" stroke-width="2.5"/>'
    '<text x="555" y="94" font-size="11" fill="#2563eb">O(n)</text>'
    '<path d="M50,200 Q180,180 300,140 Q420,100 550,70" stroke="#f59e0b" stroke-width="2.5" fill="none"/>'
    '<text x="555" y="74" font-size="11" fill="#f59e0b">O(log n)</text>'
    '<path d="M50,200 Q150,150 250,100 Q350,60 450,30" stroke="#ef4444" stroke-width="2" fill="none" stroke-dasharray="5,3"/>'
    '<text x="455" y="28" font-size="11" fill="#ef4444">O(n²)</text>',
    w=600, h=260, caption='Рост числа операций для разных сложностей'
) + '''
<h3>O(1) — константная сложность</h3>
<p>Время выполнения не зависит от размера данных. Сколько бы элементов ни было — операция выполняется за одно и то же время.</p>
<pre><code>def get_first(lst):
    return lst[0]         # O(1) — прямой доступ по индексу

def is_empty(lst):
    return len(lst) == 0  # O(1) — Python хранит длину отдельно

d = {1: 'a', 2: 'b'}
value = d[1]              # O(1) — доступ к словарю (хэш-таблица)
</code></pre>
''' + tip('Доступ к элементу списка по индексу, добавление в конец списка (append), операции со словарём — всё это O(1) в Python.') + '''
<h3>O(n) — линейная сложность</h3>
<p>Время растёт пропорционально размеру данных. В два раза больше данных → в два раза дольше.</p>
<pre><code>def linear_search(lst, target):
    for item in lst:      # перебираем все n элементов
        if item == target:
            return True
    return False

def total(lst):
    s = 0
    for x in lst:         # один проход = O(n)
        s += x
    return s
</code></pre>
<h3>O(log n) — логарифмическая сложность</h3>
<p>При каждом шаге задача уменьшается вдвое. Для 1 000 000 элементов нужно всего ~20 шагов (log₂ 1 000 000 ≈ 20)!</p>
<pre><code>def binary_search(sorted_lst, target):
    lo, hi = 0, len(sorted_lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_lst[mid] == target:
            return mid
        elif sorted_lst[mid] < target:
            lo = mid + 1  # отбрасываем левую половину
        else:
            hi = mid - 1  # отбрасываем правую половину
    return -1
</code></pre>
''' + table(
    ['n (размер)', 'O(1)', 'O(log n)', 'O(n)', 'O(n²)'],
    [
        ['10', '1', '3', '10', '100'],
        ['100', '1', '7', '100', '10 000'],
        ['1 000', '1', '10', '1 000', '1 000 000'],
        ['1 000 000', '1', '20', '1 000 000', '10¹²'],
    ]
) + warn('O(n²) для 1 миллиона элементов — 10¹² операций. При 10⁹ операций/сек компьютеру потребуется ~16 минут. O(log n) для тех же данных — 20 операций, мгновенно!'),
'code_example': '''import timeit
import random

# Сравнение O(1) vs O(n) поиска
n = 100_000
data_list = list(range(n))
data_set  = set(range(n))
target = n - 1  # худший случай — ищем последний элемент

time_list = timeit.timeit(lambda: target in data_list, number=1000)
time_set  = timeit.timeit(lambda: target in data_set,  number=1000)

print(f"Поиск в list (O(n)):  {time_list:.4f} сек за 1000 раз")
print(f"Поиск в set  (O(1)):  {time_set:.6f} сек за 1000 раз")
print(f"Set быстрее в {time_list/time_set:.0f} раз")

# Бинарный поиск O(log n)
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    steps = 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, steps

arr = list(range(1_000_000))
idx, steps = binary_search(arr, 999_999)
print(f"Нашли {idx} за {steps} шагов (из 1 000 000 элементов!)")
'''
},
{
'title': 'Таблица сложностей структур данных Python',
'order': 2,
'estimated_minutes': 55,
'content': '''
<h2>Сложность операций в структурах данных Python</h2>
<p>Понимание сложности операций помогает выбирать правильную структуру данных для задачи. Вот полная таблица для основных типов Python:</p>
''' + table(
    ['Структура', 'Операция', 'Средняя', 'Худший случай'],
    [
        ['list', 'Индексирование lst[i]', 'O(1)', 'O(1)'],
        ['list', 'Добавление в конец append()', 'O(1) аморт.', 'O(n)'],
        ['list', 'Вставка в начало insert(0,x)', 'O(n)', 'O(n)'],
        ['list', 'Удаление из середины del lst[i]', 'O(n)', 'O(n)'],
        ['list', 'Поиск x in lst', 'O(n)', 'O(n)'],
        ['list', 'Сортировка sort()', 'O(n log n)', 'O(n log n)'],
        ['dict', 'Получение d[k]', 'O(1)', 'O(n)'],
        ['dict', 'Запись d[k]=v', 'O(1)', 'O(n)'],
        ['dict', 'Удаление del d[k]', 'O(1)', 'O(n)'],
        ['dict', 'k in d', 'O(1)', 'O(n)'],
        ['set', 'Добавление add()', 'O(1)', 'O(n)'],
        ['set', 'Удаление remove()', 'O(1)', 'O(n)'],
        ['set', 'x in s', 'O(1)', 'O(n)'],
        ['set', 'Пересечение s & t', 'O(min(len,len))', 'O(n*m)'],
        ['deque', 'appendleft / popleft', 'O(1)', 'O(1)'],
        ['deque', 'Индексирование d[i]', 'O(n)', 'O(n)'],
    ]
) + warn('У dict и set «худший случай O(n)» — это теоретическая ситуация коллизий хэшей. На практике для стандартных типов (str, int) это практически никогда не происходит.') + '''
<h3>O(n log n) — сложность сортировок</h3>
<p>Алгоритм Timsort (используемый в Python) гарантирует O(n log n) в худшем случае. Это оптимально для сортировок на основе сравнений — доказано математически, что лучше не получится.</p>
''' + table(
    ['Алгоритм сортировки', 'Лучший', 'Средний', 'Худший', 'Память'],
    [
        ['Пузырьковая', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)'],
        ['Вставками', 'O(n)', 'O(n²)', 'O(n²)', 'O(1)'],
        ['Слиянием (merge sort)', 'O(n log n)', 'O(n log n)', 'O(n log n)', 'O(n)'],
        ['Быстрая (quicksort)', 'O(n log n)', 'O(n log n)', 'O(n²)', 'O(log n)'],
        ['Timsort (Python sort)', 'O(n)', 'O(n log n)', 'O(n log n)', 'O(n)'],
    ]
) + tip('Timsort хорош тем, что имеет O(n) для уже отсортированных или почти отсортированных данных — это частый случай в реальных программах.'),
'code_example': '''import time, random

# Демонстрация: list vs set для поиска
def benchmark_search(n):
    data = list(range(n))
    data_set = set(data)
    target = n // 2

    start = time.perf_counter()
    for _ in range(10000):
        _ = target in data
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(10000):
        _ = target in data_set
    set_time = time.perf_counter() - start

    return list_time, set_time

for size in [100, 1000, 10000]:
    lt, st = benchmark_search(size)
    print(f"n={size:6d}: list={lt:.4f}s  set={st:.6f}s  ratio={lt/st:.0f}x")

# Сортировка: built-in vs пузырьковая
def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

data = random.sample(range(10000), 500)
start = time.perf_counter(); bubble_sort(data); bt = time.perf_counter() - start
start = time.perf_counter(); sorted(data);      pt = time.perf_counter() - start
print(f"Пузырьковая: {bt:.4f}s, Python sort: {pt:.6f}s, ratio: {bt/pt:.0f}x")
'''
},
{
'title': 'Анализ сложности кода',
'order': 3,
'estimated_minutes': 50,
'content': '''
<h2>Как анализировать сложность своего кода</h2>
<p>Научившись определять Big O вашего кода, вы сможете заранее предсказывать проблемы с производительностью. Есть несколько простых правил.</p>
<h3>Правила подсчёта</h3>
<p><strong>Правило 1: Последовательные блоки — складываются</strong></p>
<pre><code>for x in arr:    # O(n)
    process(x)

for x in arr:    # O(n)
    other(x)

# Итого: O(n) + O(n) = O(2n) = O(n)
</code></pre>
<p><strong>Правило 2: Вложенные циклы — перемножаются</strong></p>
<pre><code>for i in arr:        # O(n)
    for j in arr:    # O(n) для каждого i
        print(i, j)

# Итого: O(n) × O(n) = O(n²)
</code></pre>
<p><strong>Правило 3: Берём доминирующий член</strong></p>
<pre><code>for x in arr:              # O(n)
    for y in arr:          # O(n²) в сумме
        process(x, y)

for x in arr:              # O(n)
    print(x)

# O(n²) + O(n) → O(n²)  (n² растёт быстрее)
</code></pre>
''' + table(
    ['Код', 'Сложность', 'Объяснение'],
    [
        ['x = arr[0]', 'O(1)', 'Прямой доступ'],
        ['for x in arr: print(x)', 'O(n)', 'Один проход'],
        ['for i in arr:\n  for j in arr: ...', 'O(n²)', 'Два вложенных цикла'],
        ['while n > 1: n //= 2', 'O(log n)', 'Делим пополам'],
        ['sorted(arr)', 'O(n log n)', 'Встроенная сортировка'],
        ['x in some_dict', 'O(1)', 'Хэш-таблица'],
        ['x in some_list', 'O(n)', 'Линейный поиск'],
    ]
) + '''
<h3>Оптимизация: замена O(n²) на O(n)</h3>
<p>Частый случай — поиск пар. Наивное решение O(n²), оптимизированное через словарь — O(n):</p>
<pre><code># Задача: найти два числа в массиве, дающие в сумме target
# O(n²) — перебор всех пар
def two_sum_slow(arr, target):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == target:
                return i, j

# O(n) — через словарь дополнений
def two_sum_fast(arr, target):
    seen = {}
    for i, x in enumerate(arr):
        complement = target - x
        if complement in seen:   # O(1) lookup
            return seen[complement], i
        seen[x] = i
</code></pre>
''' + tip('Почти любой O(n²) алгоритм поиска/проверки можно улучшить до O(n) или O(n log n), используя словарь (хэш-таблицу) или предварительную сортировку.') + warn('Пространственная сложность тоже важна. Ускорив алгоритм через словарь, вы тратите O(n) дополнительной памяти. Это часто выгодный обмен, но не всегда.'),
'code_example': '''import time

# Сравнение O(n²) vs O(n) для задачи Two Sum
def two_sum_slow(arr, target):
    """O(n²): перебор всех пар"""
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None

def two_sum_fast(arr, target):
    """O(n): хэш-таблица"""
    seen = {}
    for i, x in enumerate(arr):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None

import random
arr = random.sample(range(100_000), 10_000)
arr.append(42); arr.append(58)  # гарантируем решение
target = 100

t = time.perf_counter(); r1 = two_sum_slow(arr, target); slow_t = time.perf_counter() - t
t = time.perf_counter(); r2 = two_sum_fast(arr, target); fast_t = time.perf_counter() - t

print(f"O(n²): {slow_t:.4f}с, результат: {r1}")
print(f"O(n):  {fast_t:.6f}с, результат: {r2}")
print(f"Ускорение: {slow_t/fast_t:.0f}x")
'''
},
]
},


# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 23 — СТЕК, ОЧЕРЕДЬ, ДЕК
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Стек, очередь, дек',
'icon': 'fas fa-layer-group',
'order': 23,
'description': 'Линейные структуры данных: стек LIFO, очередь FIFO, двусторонняя очередь и приоритетная очередь.',
'lessons': [
{
'title': 'Стек (LIFO): принцип и реализация',
'order': 1,
'estimated_minutes': 65,
'content': '''
<h2>Стек — структура данных «последний пришёл, первый ушёл»</h2>
<p><strong>Стек (Stack)</strong> — линейная структура данных, работающая по принципу <strong>LIFO</strong> (Last In, First Out — последний вошёл, первый вышел). Представьте стопку тарелок: вы кладёте тарелку сверху и берёте тоже сверху.</p>
''' + diagram(
    '<rect x="200" y="20" width="120" height="240" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>'
    '<rect x="210" y="170" width="100" height="35" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>'
    '<text x="260" y="193" text-anchor="middle" font-size="12" fill="#1e40af">Элемент 1</text>'
    '<rect x="210" y="130" width="100" height="35" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>'
    '<text x="260" y="153" text-anchor="middle" font-size="12" fill="#1e40af">Элемент 2</text>'
    '<rect x="210" y="90" width="100" height="35" rx="4" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>'
    '<text x="260" y="113" text-anchor="middle" font-size="12" fill="#5b21b6" font-weight="bold">Элемент 3 ← top</text>'
    '<text x="350" y="108" font-size="11" fill="#16a34a">← push()</text>'
    '<text x="350" y="125" font-size="11" fill="#dc2626">← pop()</text>'
    '<line x1="340" y1="108" x2="315" y2="108" stroke="#16a34a" stroke-width="1.5"/>'
    '<line x1="340" y1="122" x2="315" y2="108" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4,2"/>'
    '<text x="260" y="270" text-anchor="middle" font-size="11" fill="#64748b">← дно стека (bottom)</text>'
    '<text x="260" y="15" text-anchor="middle" font-size="13" fill="#374151" font-weight="bold">СТЕК (LIFO)</text>',
    w=500, h=280, caption='Стек: push добавляет сверху, pop убирает сверху'
) + '''
<h3>Основные операции</h3>
''' + table(
    ['Операция', 'Описание', 'Сложность', 'Python (list)'],
    [
        ['push(x)', 'Добавить элемент на вершину', 'O(1)', 'stack.append(x)'],
        ['pop()', 'Убрать и вернуть вершину', 'O(1)', 'stack.pop()'],
        ['peek() / top()', 'Посмотреть вершину без удаления', 'O(1)', 'stack[-1]'],
        ['is_empty()', 'Проверить, пуст ли стек', 'O(1)', 'len(stack) == 0'],
        ['size()', 'Размер стека', 'O(1)', 'len(stack)'],
    ]
) + tip('В Python обычный list отлично работает как стек: append() — это push, pop() без аргументов — это pop. Это O(1) операции.') + '''
<h3>Реализация стека</h3>
<pre><code>class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data})"
</code></pre>
<h3>Применения стека</h3>
''' + table(
    ['Применение', 'Как используется стек', 'Пример'],
    [
        ['История браузера', 'Каждая страница push, «назад» — pop', 'Chrome, Firefox «Back»'],
        ['Undo/Redo в редакторах', 'Действия в стек, Ctrl+Z — pop', 'VS Code, Word'],
        ['Вычисление выражений', 'Операнды в стек, операторы применяются', 'Калькулятор с ОПЗ'],
        ['Обход дерева (DFS)', 'Соседние узлы push, обрабатываем pop', 'Поиск в глубину'],
        ['Проверка скобок', 'Открывающая — push, закрывающая — pop и проверка', 'Компиляторы, линтеры'],
        ['Рекурсия', 'Call stack — неявный стек вызовов', 'Стек вызовов Python'],
    ]
) + '''
<h3>Задача: проверка правильности скобок</h3>
<p>Классическое применение стека — проверка, правильно ли расставлены скобки в строке. Правило: каждая закрывающая скобка должна соответствовать последней незакрытой открывающей.</p>
<pre><code>def is_balanced(s):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack[-1] != matching[ch]:
                return False
            stack.pop()

    return len(stack) == 0  # стек должен быть пуст

print(is_balanced("({[]})"))   # True
print(is_balanced("([)]"))     # False — неправильный порядок
print(is_balanced("{[}"))      # False — незакрытая {
</code></pre>
''' + warn('Не забывайте проверять <code>is_empty()</code> перед pop()! Попытка pop из пустого стека — это ошибка. Всегда обрабатывайте этот случай.'),
'code_example': '''class Stack:
    def __init__(self):
        self._data = []
    def push(self, item): self._data.append(item)
    def pop(self):
        if not self._data: raise IndexError("empty stack")
        return self._data.pop()
    def peek(self): return self._data[-1] if self._data else None
    def is_empty(self): return len(self._data) == 0
    def __len__(self): return len(self._data)
    def __repr__(self): return f"Stack{self._data}"

# Проверка скобок
def is_balanced(s):
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.push(ch)
        elif ch in ')]}':
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()

tests = ["({[]})", "([)]", "{{}}", "((())", ""]
for t in tests:
    print(f"  '{t}': {is_balanced(t)}")

# Вычисление постфиксного выражения (ОПЗ)
def eval_postfix(expr):
    stack = Stack()
    ops = {'+': lambda a,b: a+b, '-': lambda a,b: a-b,
           '*': lambda a,b: a*b, '/': lambda a,b: a/b}
    for token in expr.split():
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.push(ops[token](a, b))
        else:
            stack.push(float(token))
    return stack.pop()

print(eval_postfix("3 4 + 2 *"))   # (3+4)*2 = 14
print(eval_postfix("5 1 2 + 4 * + 3 -"))  # 14
'''
},
{
'title': 'Очередь (FIFO) и collections.deque',
'order': 2,
'estimated_minutes': 60,
'content': '''
<h2>Очередь — структура данных «первый пришёл, первый ушёл»</h2>
<p><strong>Очередь (Queue)</strong> работает по принципу <strong>FIFO</strong> (First In, First Out). Как очередь в магазине: первый встал — первый обслужен. Новые элементы добавляются в <em>конец (rear/tail)</em>, извлекаются из <em>начала (front/head)</em>.</p>
''' + diagram(
    '<rect x="10" y="80" width="480" height="80" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>'
    '<rect x="20" y="90" width="90" height="60" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>'
    '<text x="65" y="115" text-anchor="middle" font-size="11" fill="#14532d" font-weight="bold">front</text>'
    '<text x="65" y="135" text-anchor="middle" font-size="10" fill="#14532d">dequeue() ←</text>'
    '<rect x="120" y="90" width="80" height="60" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>'
    '<text x="160" y="125" text-anchor="middle" font-size="11" fill="#1e40af">A</text>'
    '<rect x="210" y="90" width="80" height="60" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>'
    '<text x="250" y="125" text-anchor="middle" font-size="11" fill="#1e40af">B</text>'
    '<rect x="300" y="90" width="80" height="60" rx="4" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>'
    '<text x="340" y="125" text-anchor="middle" font-size="11" fill="#1e40af">C</text>'
    '<rect x="390" y="90" width="90" height="60" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>'
    '<text x="435" y="115" text-anchor="middle" font-size="11" fill="#991b1b" font-weight="bold">rear</text>'
    '<text x="435" y="135" text-anchor="middle" font-size="10" fill="#991b1b">→ enqueue()</text>'
    '<text x="250" y="40" text-anchor="middle" font-size="13" fill="#374151" font-weight="bold">ОЧЕРЕДЬ (FIFO)</text>'
    '<text x="250" y="200" text-anchor="middle" font-size="11" fill="#64748b">Направление движения: → (от rear к front)</text>',
    w=500, h=220, caption='Очередь: enqueue добавляет в конец, dequeue берёт из начала'
) + '''
<h3>Почему list — плохой выбор для очереди</h3>
<p>Можно реализовать очередь через list, но это неэффективно: <code>list.pop(0)</code> — операция O(n), так как все элементы сдвигаются влево. Правильный инструмент — <code>collections.deque</code>.</p>
''' + table(
    ['Операция', 'list', 'collections.deque'],
    [
        ['enqueue (добавить в конец)', 'append() — O(1)', 'append() — O(1)'],
        ['dequeue (убрать из начала)', 'pop(0) — O(n) ⚠️', 'popleft() — O(1) ✓'],
        ['peek (посмотреть начало)', 'lst[0] — O(1)', 'dq[0] — O(1)'],
        ['Доступ по индексу', 'lst[i] — O(1)', 'dq[i] — O(n) ⚠️'],
        ['Добавить в начало', 'insert(0,x) — O(n) ⚠️', 'appendleft() — O(1) ✓'],
    ]
) + tip('<code>collections.deque</code> (Double-Ended Queue) — двусторонняя очередь, реализованная как двусвязный список. Операции с обоих концов O(1). Идеальна для очередей и стеков при большом объёме данных.') + '''
<h3>Реализация очереди через deque</h3>
<pre><code>from collections import deque

class Queue:
    def __init__(self, maxlen=None):
        self._data = deque(maxlen=maxlen)  # maxlen — ограничение размера (опц.)

    def enqueue(self, item):
        self._data.append(item)     # добавляем в конец

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()  # берём из начала O(1)!

    def peek(self):
        return self._data[0] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
</code></pre>
<h3>Применения очереди</h3>
''' + table(
    ['Применение', 'Описание'],
    [
        ['BFS (поиск в ширину)', 'Вершины графа добавляются в очередь при обнаружении'],
        ['Планировщик задач ОС', 'Процессы ждут своей очереди на процессор'],
        ['Буфер печати', 'Документы печатаются в порядке отправки'],
        ['Кэш (LRU Cache)', 'deque с maxlen вытесняет старые элементы автоматически'],
        ['Потоковая обработка', 'Задачи передаются между потоками через Queue'],
        ['Симуляции', 'Очередь клиентов, пакетов в сети и т.д.'],
    ]
) + warn('Для многопоточного кода используйте <code>queue.Queue</code> из стандартной библиотеки — она потокобезопасна. <code>collections.deque</code> не гарантирует атомарность операций при параллельном доступе.'),
'code_example': '''from collections import deque

# Базовая очередь
q = deque()
for item in ["задача_1", "задача_2", "задача_3"]:
    q.append(item)
    print(f"  Добавлено: {item}, очередь: {list(q)}")

while q:
    task = q.popleft()
    print(f"  Обработано: {task}")

# Симуляция банковской очереди
import random

class BankSimulation:
    def __init__(self):
        self.queue = deque()
        self.time = 0

    def arrive(self, client):
        self.queue.append((client, self.time))
        print(f"  t={self.time:2d}: {client} встал в очередь (длина: {len(self.queue)})")

    def serve(self):
        if self.queue:
            client, arrived = self.queue.popleft()
            wait = self.time - arrived
            print(f"  t={self.time:2d}: {client} обслужен (ждал {wait} ед.)")

    def tick(self):
        self.time += 1

bank = BankSimulation()
events = [(1,"Иван"),(2,"Мария"),(2,None),(3,"Пётр"),(4,None),(5,None),(6,"Анна")]
for t, event in events:
    while bank.time < t: bank.tick()
    if event: bank.arrive(event)
    else: bank.serve()
'''
},
{
'title': 'Дек и приоритетная очередь (heapq)',
'order': 3,
'estimated_minutes': 65,
'content': '''
<h2>Дек — двусторонняя очередь</h2>
<p><strong>Дек (Deque, Double-Ended Queue)</strong> — структура данных, которая объединяет возможности стека и очереди: элементы можно добавлять и удалять с <em>обоих</em> концов за O(1).</p>
''' + table(
    ['Операция', 'Описание', 'Метод deque', 'Сложность'],
    [
        ['Добавить справа', 'Стандартное добавление', 'append(x)', 'O(1)'],
        ['Добавить слева', 'Добавить в начало', 'appendleft(x)', 'O(1)'],
        ['Убрать справа', 'Как pop() стека', 'pop()', 'O(1)'],
        ['Убрать слева', 'Как dequeue() очереди', 'popleft()', 'O(1)'],
        ['Повернуть', 'Сдвиг всех элементов на k позиций', 'rotate(k)', 'O(k)'],
        ['Ограничить размер', 'При maxlen старые вытесняются', 'deque(maxlen=n)', 'O(1)'],
    ]
) + tip('deque с maxlen — готовый скользящий буфер (sliding window). Когда добавляется новый элемент при заполненном deque, самый старый автоматически удаляется.') + '''
<pre><code>from collections import deque

# Скользящее среднее (sliding window)
def moving_average(data, window):
    buf = deque(maxlen=window)
    result = []
    for x in data:
        buf.append(x)
        result.append(sum(buf) / len(buf))
    return result

temps = [20, 22, 19, 25, 28, 30, 27, 24]
print(moving_average(temps, 3))  # среднее за 3 дня

# rotate: круговой буфер
d = deque([1, 2, 3, 4, 5])
d.rotate(2)   # [4, 5, 1, 2, 3] — сдвиг вправо
d.rotate(-1)  # [5, 1, 2, 3, 4] — сдвиг влево
</code></pre>
<h2>Приоритетная очередь и модуль heapq</h2>
<p><strong>Приоритетная очередь (Priority Queue)</strong> — очередь, в которой элемент с наибольшим (или наименьшим) приоритетом извлекается первым, независимо от порядка добавления.</p>
<p>В Python приоритетная очередь реализована через <strong>минимальную двоичную кучу (min-heap)</strong> из модуля <code>heapq</code>.</p>
''' + diagram(
    '<circle cx="300" cy="40" r="25" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>'
    '<text x="300" y="46" text-anchor="middle" font-size="14" fill="#1e40af" font-weight="bold">1</text>'
    '<line x1="280" y1="60" x2="220" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="320" y1="60" x2="380" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="200" cy="120" r="25" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>'
    '<text x="200" y="126" text-anchor="middle" font-size="14" fill="#5b21b6" font-weight="bold">3</text>'
    '<circle cx="400" cy="120" r="25" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>'
    '<text x="400" y="126" text-anchor="middle" font-size="14" fill="#5b21b6" font-weight="bold">2</text>'
    '<line x1="182" y1="140" x2="140" y2="175" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="218" y1="140" x2="260" y2="175" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="120" cy="195" r="20" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>'
    '<text x="120" y="201" text-anchor="middle" font-size="13" fill="#166534">6</text>'
    '<circle cx="280" cy="195" r="20" fill="#f0fdf4" stroke="#16a34a" stroke-width="1"/>'
    '<text x="280" y="201" text-anchor="middle" font-size="13" fill="#166534">5</text>'
    '<text x="300" y="250" text-anchor="middle" font-size="11" fill="#64748b">Свойство кучи: каждый родитель ≤ потомков</text>'
    '<text x="300" y="270" text-anchor="middle" font-size="11" fill="#64748b">Минимум всегда в корне → извлечение O(log n)</text>',
    w=600, h=285, caption='Min-heap: наименьший элемент всегда в корне'
) + '''
<h3>Операции heapq</h3>
''' + table(
    ['Функция', 'Описание', 'Сложность'],
    [
        ['heapq.heappush(h, x)', 'Добавить элемент, сохранить свойство кучи', 'O(log n)'],
        ['heapq.heappop(h)', 'Извлечь и вернуть минимальный элемент', 'O(log n)'],
        ['heapq.heapify(lst)', 'Превратить список в кучу на месте', 'O(n)'],
        ['heapq.nlargest(k, it)', 'k наибольших элементов', 'O(n log k)'],
        ['heapq.nsmallest(k, it)', 'k наименьших элементов', 'O(n log k)'],
        ['h[0]', 'Посмотреть минимум без извлечения', 'O(1)'],
    ]
) + warn('heapq реализует МИНИМАЛЬНУЮ кучу. Для максимальной кучи — вставляйте отрицательные значения: <code>heappush(h, -x)</code>, при извлечении: <code>-heappop(h)</code>.'),
'code_example': '''import heapq
from collections import deque

# --- Приоритетная очередь задач ---
tasks = []
heapq.heappush(tasks, (3, "Написать отчёт"))
heapq.heappush(tasks, (1, "Критический баг"))
heapq.heappush(tasks, (2, "Код-ревью"))
heapq.heappush(tasks, (1, "Сервер упал"))

print("Задачи по приоритету:")
while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"  [{priority}] {task}")

# --- Top-K элементов ---
scores = [45, 92, 67, 88, 33, 95, 72, 81]
top3 = heapq.nlargest(3, scores)
bottom3 = heapq.nsmallest(3, scores)
print(f"Топ-3: {top3}, Нижние-3: {bottom3}")

# --- Скользящее среднее через deque ---
def moving_avg(data, k):
    window = deque(maxlen=k)
    result = []
    for x in data:
        window.append(x)
        result.append(round(sum(window) / len(window), 2))
    return result

data = [10, 20, 30, 40, 50, 60, 70]
print("Скользящее среднее (k=3):", moving_avg(data, 3))

# --- Слияние k отсортированных массивов ---
arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
merged = list(heapq.merge(*arrays))
print("Слияние:", merged)
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 24 — СВЯЗНЫЙ СПИСОК
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Связный список',
'icon': 'fas fa-link',
'order': 24,
'description': 'Однонаправленный и двунаправленный связный список: узлы, указатели, вставка, удаление, обход.',
'lessons': [
{
'title': 'Узел и однонаправленный связный список',
'order': 1,
'estimated_minutes': 70,
'content': '''
<h2>Что такое связный список?</h2>
<p><strong>Связный список (Linked List)</strong> — линейная структура данных, в которой элементы (<em>узлы</em>) хранятся не в смежных ячейках памяти, а рассеяны по ней. Каждый узел содержит данные и <em>указатель (ссылку)</em> на следующий узел.</p>
''' + diagram(
    '<rect x="30" y="80" width="100" height="60" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>'
    '<text x="80" y="105" text-anchor="middle" font-size="12" fill="#1e40af" font-weight="bold">data: 10</text>'
    '<text x="80" y="125" text-anchor="middle" font-size="11" fill="#3b82f6">next →</text>'
    '<line x1="130" y1="110" x2="160" y2="110" stroke="#374151" stroke-width="2" marker-end="url(#arr)"/>'
    '<rect x="170" y="80" width="100" height="60" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>'
    '<text x="220" y="105" text-anchor="middle" font-size="12" fill="#1e40af" font-weight="bold">data: 20</text>'
    '<text x="220" y="125" text-anchor="middle" font-size="11" fill="#3b82f6">next →</text>'
    '<line x1="270" y1="110" x2="300" y2="110" stroke="#374151" stroke-width="2"/>'
    '<rect x="310" y="80" width="100" height="60" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>'
    '<text x="360" y="105" text-anchor="middle" font-size="12" fill="#1e40af" font-weight="bold">data: 30</text>'
    '<text x="360" y="125" text-anchor="middle" font-size="11" fill="#3b82f6">next →</text>'
    '<line x1="410" y1="110" x2="440" y2="110" stroke="#374151" stroke-width="2"/>'
    '<rect x="450" y="90" width="60" height="40" rx="4" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>'
    '<text x="480" y="115" text-anchor="middle" font-size="12" fill="#94a3b8">None</text>'
    '<text x="80" y="165" text-anchor="middle" font-size="11" fill="#64748b">head</text>'
    '<line x1="80" y1="155" x2="80" y2="145" stroke="#64748b" stroke-width="1.5"/>'
    '<text x="360" y="165" text-anchor="middle" font-size="11" fill="#64748b">tail</text>'
    '<line x1="360" y1="155" x2="360" y2="145" stroke="#64748b" stroke-width="1.5"/>',
    w=560, h=180, caption='Однонаправленный связный список: каждый узел указывает на следующий'
) + '''
<h3>Сравнение с массивом (list)</h3>
''' + table(
    ['Характеристика', 'Массив (list)', 'Связный список'],
    [
        ['Хранение в памяти', 'Смежные ячейки', 'Произвольное расположение'],
        ['Доступ по индексу', 'O(1) — прямой', 'O(n) — нужен обход'],
        ['Вставка в начало', 'O(n) — сдвиг элементов', 'O(1) — меняем head'],
        ['Вставка в конец', 'O(1) амортизированно', 'O(1) если есть tail'],
        ['Вставка в середину', 'O(n) — сдвиг', 'O(1) после нахождения позиции'],
        ['Удаление', 'O(n) — сдвиг', 'O(1) если известен предыдущий'],
        ['Память', 'Только данные', 'Данные + указатели'],
        ['Динамический размер', 'Перевыделение памяти', 'Идеально подходит'],
    ]
) + '''
<h3>Реализация класса Node и LinkedList</h3>
<pre><code>class Node:
    """Узел связного списка"""
    def __init__(self, data):
        self.data = data
        self.next = None   # указатель на следующий узел

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    def __init__(self):
        self.head = None   # указатель на первый узел
        self._size = 0

    def append(self, data):
        """Добавить в конец — O(n), если нет tail"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:    # идём до последнего
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        """Добавить в начало — O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def display(self):
        """Вывести все элементы"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " → ".join(elements) + " → None"

    def __len__(self):
        return self._size
</code></pre>
''' + tip('Добавление tail-указателя (ссылки на последний узел) ускоряет append() с O(n) до O(1). Для коротких списков разница незначительна, но при тысячах добавлений — существенна.') + warn('При обходе связного списка всегда проверяйте <code>current is not None</code> перед доступом к <code>current.data</code> или <code>current.next</code>!'),
'code_example': '''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        node = Node(data)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def prepend(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def __len__(self): return self._size
    def __repr__(self): return " → ".join(map(str, self.to_list())) + " → None"

ll = LinkedList()
for v in [10, 20, 30, 40, 50]:
    ll.append(v)
print(f"После append: {ll}")

ll.prepend(5)
print(f"После prepend(5): {ll}")
print(f"Длина: {len(ll)}")

# Нахождение середины (алгоритм двух указателей)
def find_middle(ll):
    slow = fast = ll.head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.data if slow else None

print(f"Середина: {find_middle(ll)}")

# Разворот связного списка
def reverse(ll):
    prev, cur = None, ll.head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    ll.head = prev

reverse(ll)
print(f"После разворота: {ll}")
'''
},
{
'title': 'Вставка, удаление, поиск в связном списке',
'order': 2,
'estimated_minutes': 65,
'content': '''
<h2>Операции над связным списком</h2>
<p>Основная сложность работы со связным списком — все операции требуют обхода от головы. Зато вставка и удаление (после нахождения позиции) выполняются за O(1) без сдвига памяти.</p>
<h3>Вставка</h3>
<p>Три случая вставки: в начало, в конец, в произвольную позицию.</p>
''' + diagram(
    '<text x="300" y="20" text-anchor="middle" font-size="13" fill="#374151" font-weight="bold">Вставка узла C между A и B</text>'
    '<rect x="50" y="50" width="80" height="50" rx="5" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>'
    '<text x="90" y="80" text-anchor="middle" font-size="13" fill="#1e40af" font-weight="bold">A</text>'
    '<line x1="130" y1="75" x2="170" y2="75" stroke="#94a3b8" stroke-width="2"/>'
    '<rect x="180" y="50" width="80" height="50" rx="5" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>'
    '<text x="220" y="80" text-anchor="middle" font-size="13" fill="#1e40af" font-weight="bold">B</text>'
    '<line x1="260" y1="75" x2="300" y2="75" stroke="#94a3b8" stroke-width="2"/>'
    '<rect x="310" y="50" width="60" height="50" rx="4" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>'
    '<text x="340" y="80" text-anchor="middle" font-size="11" fill="#94a3b8">None</text>'
    '<rect x="180" y="150" width="80" height="50" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>'
    '<text x="220" y="180" text-anchor="middle" font-size="13" fill="#14532d" font-weight="bold">C (new)</text>'
    '<line x1="130" y1="75" x2="180" y2="165" stroke="#dc2626" stroke-width="2" stroke-dasharray="5,3"/>'
    '<text x="150" y="130" font-size="10" fill="#dc2626">1. A.next = C</text>'
    '<line x1="260" y1="175" x2="220" y2="105" stroke="#16a34a" stroke-width="2" stroke-dasharray="5,3"/>'
    '<text x="285" y="150" font-size="10" fill="#16a34a">2. C.next = B</text>',
    w=600, h=220, caption='Вставка: 1) новый узел указывает на B; 2) A указывает на новый узел'
) + '''
<pre><code>def insert_after(self, target_data, new_data):
    """Вставить new_data после узла с target_data"""
    current = self.head
    while current:
        if current.data == target_data:
            new_node = Node(new_data)
            new_node.next = current.next  # шаг 2: C → B
            current.next = new_node       # шаг 1: A → C
            self._size += 1
            return True
        current = current.next
    return False  # элемент не найден
</code></pre>
<h3>Удаление</h3>
<p>При удалении нужен доступ к <em>предыдущему</em> узлу. Именно поэтому для удаления произвольного узла нужен обход O(n).</p>
<pre><code>def delete(self, target_data):
    """Удалить первый узел с данным значением"""
    if self.head is None:
        return False

    # Особый случай: удаляем голову
    if self.head.data == target_data:
        self.head = self.head.next
        self._size -= 1
        return True

    # Ищем предшественника
    prev = self.head
    while prev.next:
        if prev.next.data == target_data:
            prev.next = prev.next.next  # перепрыгиваем узел
            self._size -= 1
            return True
        prev = prev.next
    return False
</code></pre>
''' + table(
    ['Операция', 'Сложность', 'Примечание'],
    [
        ['Вставка в начало', 'O(1)', 'Меняем head'],
        ['Вставка в конец (с tail)', 'O(1)', 'Меняем tail.next и tail'],
        ['Вставка в конец (без tail)', 'O(n)', 'Нужен обход до конца'],
        ['Вставка после узла', 'O(1)*', '*O(n) на поиск + O(1) на вставку'],
        ['Удаление головы', 'O(1)', 'Меняем head'],
        ['Удаление по значению', 'O(n)', 'Нужен обход + предшественник'],
        ['Поиск по значению', 'O(n)', 'Линейный обход'],
        ['Доступ по индексу', 'O(n)', 'Нет прямого доступа'],
    ]
) + tip('Два классических алгоритма для связных списков: <strong>алгоритм двух указателей</strong> (быстрый и медленный) — находит середину, k-й с конца, цикл. Используйте его в задачах на собеседованиях.'),
'code_example': '''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node; return
        cur = self.head
        while cur.next: cur = cur.next
        cur.next = node

    def delete(self, val):
        if not self.head: return False
        if self.head.data == val:
            self.head = self.head.next; return True
        prev = self.head
        while prev.next:
            if prev.next.data == val:
                prev.next = prev.next.next; return True
            prev = prev.next
        return False

    def has_cycle(self):
        """Алгоритм Флойда: обнаружение цикла"""
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def kth_from_end(self, k):
        """k-й элемент с конца за один проход"""
        ahead = behind = self.head
        for _ in range(k):
            if not ahead: return None
            ahead = ahead.next
        while ahead:
            ahead = ahead.next
            behind = behind.next
        return behind.data if behind else None

    def __repr__(self):
        parts, cur = [], self.head
        while cur:
            parts.append(str(cur.data)); cur = cur.next
        return " → ".join(parts)

ll = LinkedList()
for v in [1, 2, 3, 4, 5, 6, 7]:
    ll.append(v)
print(f"Список: {ll}")
print(f"3-й с конца: {ll.kth_from_end(3)}")
ll.delete(4)
print(f"После удаления 4: {ll}")
'''
},
{
'title': 'Двунаправленный связный список',
'order': 3,
'estimated_minutes': 60,
'content': '''
<h2>Двунаправленный (двусвязный) список</h2>
<p>В отличие от однонаправленного, каждый узел двунаправленного списка хранит <strong>два указателя</strong>: на следующий (<code>next</code>) и на предыдущий (<code>prev</code>) узлы. Это позволяет обходить список в обоих направлениях и удалять узел за O(1) при наличии на него ссылки.</p>
''' + diagram(
    '<text x="300" y="22" text-anchor="middle" font-size="13" fill="#374151" font-weight="bold">Двусвязный список</text>'
    '<rect x="10" y="40" width="50" height="40" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>'
    '<text x="35" y="65" text-anchor="middle" font-size="10" fill="#94a3b8">None</text>'
    '<line x1="60" y1="60" x2="90" y2="60" stroke="#374151" stroke-width="1.5"/>'
    '<rect x="90" y="35" width="110" height="50" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>'
    '<text x="110" y="57" font-size="9" fill="#64748b">prev←</text>'
    '<text x="145" y="57" text-anchor="middle" font-size="13" fill="#1e40af" font-weight="bold">A</text>'
    '<text x="165" y="57" font-size="9" fill="#64748b">→next</text>'
    '<line x1="200" y1="55" x2="230" y2="55" stroke="#374151" stroke-width="1.5"/>'
    '<line x1="200" y1="65" x2="230" y2="65" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="4,2"/>'
    '<rect x="230" y="35" width="110" height="50" rx="6" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>'
    '<text x="250" y="57" font-size="9" fill="#64748b">prev←</text>'
    '<text x="285" y="57" text-anchor="middle" font-size="13" fill="#5b21b6" font-weight="bold">B</text>'
    '<text x="305" y="57" font-size="9" fill="#64748b">→next</text>'
    '<line x1="340" y1="55" x2="370" y2="55" stroke="#374151" stroke-width="1.5"/>'
    '<line x1="340" y1="65" x2="370" y2="65" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="4,2"/>'
    '<rect x="370" y="35" width="110" height="50" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>'
    '<text x="390" y="57" font-size="9" fill="#64748b">prev←</text>'
    '<text x="425" y="57" text-anchor="middle" font-size="13" fill="#1e40af" font-weight="bold">C</text>'
    '<text x="445" y="57" font-size="9" fill="#64748b">→next</text>'
    '<line x1="480" y1="60" x2="510" y2="60" stroke="#374151" stroke-width="1.5"/>'
    '<rect x="510" y="40" width="50" height="40" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>'
    '<text x="535" y="65" text-anchor="middle" font-size="10" fill="#94a3b8">None</text>'
    '<text x="300" y="110" text-anchor="middle" font-size="11" fill="#374151">→ прямые ссылки (next)     - - - обратные ссылки (prev)</text>',
    w=580, h=130, caption='Двусвязный список: каждый узел знает своего предшественника и преемника'
) + '''
<h3>Преимущества двунаправленного списка</h3>
''' + table(
    ['Операция', 'Однонаправленный', 'Двунаправленный'],
    [
        ['Обход вперёд', 'O(n)', 'O(n)'],
        ['Обход назад', 'Невозможно / O(n) разворот', 'O(n) напрямую'],
        ['Удаление узла (есть ссылка)', 'O(n) — нужен предшественник', 'O(1) — есть prev'],
        ['Вставка перед узлом', 'O(n)', 'O(1)'],
        ['Память', 'data + next', 'data + next + prev'],
    ]
) + '''
<pre><code>class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        node = DNode(data)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def delete_node(self, node):
        """Удалить конкретный узел за O(1)"""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next  # удаляем голову

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # удаляем хвост

        self._size -= 1
</code></pre>
''' + tip('Двусвязный список лежит в основе <code>collections.deque</code> в Python — именно поэтому все операции с обоих концов выполняются за O(1). Также он используется в реализации LRU Cache (Least Recently Used).'),
'code_example': '''class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = self.tail = None
        self._size = 0

    def append(self, data):
        node = DNode(data)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def delete_node(self, node):
        if node.prev: node.prev.next = node.next
        else: self.head = node.next
        if node.next: node.next.prev = node.prev
        else: self.tail = node.prev
        self._size -= 1

    def forward(self):
        result, cur = [], self.head
        while cur: result.append(cur.data); cur = cur.next
        return result

    def backward(self):
        result, cur = [], self.tail
        while cur: result.append(cur.data); cur = cur.prev
        return result

# LRU Cache через двусвязный список + словарь
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}  # key -> node
        self.dll = DoublyLinkedList()

    def get(self, key):
        if key not in self.cache: return -1
        node = self.cache[key]
        self.dll.delete_node(node)
        self.dll.append(node.data)
        self.cache[key] = self.dll.tail
        return node.data[1]

    def put(self, key, value):
        if key in self.cache:
            self.dll.delete_node(self.cache[key])
        elif self._size() >= self.cap:
            lru = self.dll.head
            del self.cache[lru.data[0]]
            self.dll.delete_node(lru)
        self.dll.append((key, value))
        self.cache[key] = self.dll.tail

    def _size(self): return self.dll._size

lru = LRUCache(3)
for k, v in [(1,10),(2,20),(3,30)]: lru.put(k, v)
print(lru.get(1))  # 10, делает 1 самым свежим
lru.put(4, 40)     # вытесняет ключ 2 (давно не использовался)
print(lru.get(2))  # -1 (вытеснен)
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 25 — БИНАРНОЕ ДЕРЕВО ПОИСКА
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Бинарное дерево поиска (BST)',
'icon': 'fas fa-sitemap',
'order': 25,
'description': 'Деревья: терминология, бинарное дерево поиска, вставка, поиск, обходы, удаление узла.',
'lessons': [
{
'title': 'Деревья: терминология и структура',
'order': 1,
'estimated_minutes': 60,
'content': '''
<h2>Деревья в информатике</h2>
<p><strong>Дерево</strong> — иерархическая структура данных, состоящая из узлов, связанных рёбрами. В отличие от связного списка, у каждого узла может быть несколько потомков. Деревья моделируют иерархические отношения: файловая система, XML/HTML-документ, семейное дерево, структура компании.</p>
''' + diagram(
    '<circle cx="300" cy="30" r="22" fill="#667eea" stroke="#4f46e5" stroke-width="2"/>'
    '<text x="300" y="36" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">A</text>'
    '<text x="340" y="20" font-size="10" fill="#64748b">← корень (root)</text>'
    '<line x1="285" y1="50" x2="190" y2="90" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="315" y1="50" x2="410" y2="90" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="170" cy="110" r="22" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="170" y="116" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">B</text>'
    '<circle cx="430" cy="110" r="22" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="430" y="116" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">C</text>'
    '<line x1="158" y1="130" x2="100" y2="170" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="182" y1="130" x2="240" y2="170" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="418" y1="130" x2="360" y2="170" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="80" cy="190" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="80" y="196" text-anchor="middle" font-size="11" fill="#fff" font-weight="bold">D</text>'
    '<circle cx="260" cy="190" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="260" y="196" text-anchor="middle" font-size="11" fill="#fff" font-weight="bold">E</text>'
    '<circle cx="340" cy="190" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="340" y="196" text-anchor="middle" font-size="11" fill="#fff" font-weight="bold">F</text>'
    '<text x="60" y="240" font-size="10" fill="#64748b">D,E,F — листья</text>'
    '<text x="200" y="240" font-size="10" fill="#64748b">B,C — внутренние узлы</text>'
    '<text x="380" y="240" font-size="10" fill="#64748b">Высота дерева = 3</text>',
    w=560, h=255, caption='Дерево: иерархия узлов с одним корнем'
) + '''
<h3>Ключевая терминология</h3>
''' + table(
    ['Термин', 'Определение', 'В примере выше'],
    [
        ['Корень (root)', 'Единственный узел без родителя', 'A'],
        ['Лист (leaf)', 'Узел без потомков', 'D, E, F'],
        ['Внутренний узел', 'Узел с хотя бы одним потомком', 'A, B, C'],
        ['Родитель (parent)', 'Непосредственный предшественник', 'A — родитель B и C'],
        ['Потомок (child)', 'Непосредственный преемник', 'B и C — потомки A'],
        ['Высота дерева', 'Длина наидлиннейшего пути от корня до листа', '3 (A→B→D)'],
        ['Глубина узла', 'Расстояние от корня до узла', 'Глубина D = 2'],
        ['Поддерево', 'Дерево, образованное узлом и всеми потомками', 'B, D, E — поддерево'],
    ]
) + '''
<h3>Бинарное дерево</h3>
<p><strong>Бинарное дерево</strong> — дерево, в котором каждый узел имеет <em>не более двух</em> потомков: левый (<code>left</code>) и правый (<code>right</code>).</p>
''' + table(
    ['Вид бинарного дерева', 'Описание'],
    [
        ['Полное (full)', 'Каждый узел имеет 0 или 2 потомка'],
        ['Совершенное (perfect)', 'Все внутренние узлы имеют 2 потомка, все листья на одном уровне'],
        ['Сбалансированное', 'Высота левого и правого поддерева отличаются не более чем на 1'],
        ['Вырожденное (degenerate)', 'Каждый узел имеет только одного потомка (похоже на список)'],
    ]
) + tip('Высота сбалансированного бинарного дерева из n узлов — O(log n). Именно это обеспечивает эффективность BST, AVL и Red-Black деревьев.'),
'code_example': '''class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
    def __repr__(self): return f"TreeNode({self.val})"

# Ручное построение дерева
#       1
#      / \\
#     2   3
#    / \\
#   4   5
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

# Высота дерева
def height(node):
    if node is None: return 0
    return 1 + max(height(node.left), height(node.right))

# Количество узлов
def count_nodes(node):
    if node is None: return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

# Является ли деревом листом
def is_leaf(node):
    return node is not None and node.left is None and node.right is None

print(f"Высота: {height(root)}")
print(f"Узлов: {count_nodes(root)}")
print(f"Корень — лист? {is_leaf(root)}")
print(f"Узел 4 — лист? {is_leaf(root.left.left)}")

# Зеркальное отражение дерева
def mirror(node):
    if node is None: return
    node.left, node.right = node.right, node.left
    mirror(node.left)
    mirror(node.right)

mirror(root)
print(f"После зеркала: root.left = {root.left}, root.right = {root.right}")
'''
},
{
'title': 'BST: вставка и поиск',
'order': 2,
'estimated_minutes': 65,
'content': '''
<h2>Бинарное дерево поиска (Binary Search Tree)</h2>
<p><strong>BST</strong> — бинарное дерево со специальным свойством: для каждого узла <em>все элементы левого поддерева меньше</em> значения узла, а <em>все элементы правого поддерева больше</em>.</p>
''' + diagram(
    '<circle cx="300" cy="35" r="25" fill="#667eea" stroke="#4f46e5" stroke-width="2"/>'
    '<text x="300" y="41" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">8</text>'
    '<line x1="280" y1="55" x2="190" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="320" y1="55" x2="410" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="165" cy="120" r="22" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="165" y="126" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">3</text>'
    '<circle cx="435" cy="120" r="22" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="435" y="126" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">10</text>'
    '<line x1="150" y1="140" x2="100" y2="180" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="180" y1="140" x2="230" y2="180" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="448" y1="140" x2="480" y2="180" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="80" cy="200" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="80" y="206" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">1</text>'
    '<circle cx="250" cy="200" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="250" y="206" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">6</text>'
    '<circle cx="500" cy="200" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="500" y="206" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">14</text>'
    '<text x="100" y="255" font-size="10" fill="#dc2626">всё левое < 8</text>'
    '<text x="420" y="255" font-size="10" fill="#16a34a">всё правое > 8</text>',
    w=580, h=270, caption='BST: левое поддерево < корень < правое поддерево'
) + '''
<h3>Реализация BST</h3>
<pre><code>class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if node is None:
            return TreeNode(val)   # нашли место — создаём узел
        if val < node.val:
            node.left = self._insert(node.left, val)   # идём влево
        elif val > node.val:
            node.right = self._insert(node.right, val)  # идём вправо
        # val == node.val: дубликаты игнорируем (можно и обрабатывать)
        return node

    def search(self, val):
        return self._search(self.root, val)

    def _search(self, node, val):
        if node is None:
            return False       # дошли до None — не нашли
        if val == node.val:
            return True        # нашли!
        elif val < node.val:
            return self._search(node.left, val)
        else:
            return self._search(node.right, val)
</code></pre>
''' + table(
    ['Операция', 'Сбалансированное BST', 'Вырожденное BST (список)'],
    [
        ['Поиск', 'O(log n)', 'O(n)'],
        ['Вставка', 'O(log n)', 'O(n)'],
        ['Удаление', 'O(log n)', 'O(n)'],
        ['Min/Max', 'O(log n)', 'O(n)'],
        ['Обход inorder', 'O(n)', 'O(n)'],
    ]
) + warn('BST вырождается в список (O(n) операции), если вставлять элементы в отсортированном порядке: 1, 2, 3, 4... Для гарантированного O(log n) используют <strong>AVL-деревья</strong> или <strong>красно-чёрные деревья</strong> (dict в Python — именно хэш-таблица, не BST).'),
'code_example': '''class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

class BST:
    def __init__(self): self.root = None

    def insert(self, val):
        def _ins(node, v):
            if not node: return TreeNode(v)
            if v < node.val: node.left = _ins(node.left, v)
            elif v > node.val: node.right = _ins(node.right, v)
            return node
        self.root = _ins(self.root, val)

    def search(self, val):
        node = self.root
        while node:
            if val == node.val: return True
            node = node.left if val < node.val else node.right
        return False

    def min_val(self):
        node = self.root
        while node and node.left: node = node.left
        return node.val if node else None

    def max_val(self):
        node = self.root
        while node and node.right: node = node.right
        return node.val if node else None

    def height(self):
        def _h(n): return 0 if not n else 1 + max(_h(n.left), _h(n.right))
        return _h(self.root)

bst = BST()
values = [8, 3, 10, 1, 6, 14, 4, 7]
for v in values: bst.insert(v)

print(f"Поиск 6: {bst.search(6)}")
print(f"Поиск 5: {bst.search(5)}")
print(f"Min: {bst.min_val()}, Max: {bst.max_val()}")
print(f"Высота: {bst.height()}")

# Сравнение: отсортированный vs случайный порядок вставки
import random
bst_sorted = BST()
bst_random = BST()
data = list(range(1, 16))
for v in data: bst_sorted.insert(v)           # вырождение
random.shuffle(data)
for v in data: bst_random.insert(v)           # сбалансированное
print(f"Высота (отсортированный): {bst_sorted.height()}")  # ~15
print(f"Высота (случайный):       {bst_random.height()}")  # ~4-5
'''
},
{
'title': 'Обходы дерева: inorder, preorder, postorder',
'order': 3,
'estimated_minutes': 60,
'content': '''
<h2>Три классических обхода бинарного дерева</h2>
<p>Обход дерева — систематическое посещение всех узлов. Три основных порядка определяются <em>моментом обработки корневого узла</em> относительно поддеревьев.</p>
''' + table(
    ['Обход', 'Порядок', 'Применение'],
    [
        ['Inorder (симметричный)', 'Левое → Корень → Правое', 'BST: даёт отсортированный порядок'],
        ['Preorder (прямой)', 'Корень → Левое → Правое', 'Копирование дерева, сериализация'],
        ['Postorder (обратный)', 'Левое → Правое → Корень', 'Удаление дерева, вычисление выражений'],
        ['Level-order (BFS)', 'Уровень за уровнем', 'Поиск в ширину, минимальная высота'],
    ]
) + '''
<pre><code>def inorder(node, result=None):
    """Левое → Корень → Правое → для BST даёт отсортированный список"""
    if result is None: result = []
    if node:
        inorder(node.left, result)
        result.append(node.val)      # ← обработка в середине
        inorder(node.right, result)
    return result

def preorder(node, result=None):
    """Корень → Левое → Правое → структура дерева"""
    if result is None: result = []
    if node:
        result.append(node.val)      # ← обработка первым
        preorder(node.left, result)
        preorder(node.right, result)
    return result

def postorder(node, result=None):
    """Левое → Правое → Корень → подходит для удаления"""
    if result is None: result = []
    if node:
        postorder(node.left, result)
        postorder(node.right, result)
        result.append(node.val)      # ← обработка последним
    return result

from collections import deque
def level_order(root):
    """BFS: уровень за уровнем"""
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
</code></pre>
''' + tip('Запомнить порядки легко по положению корня: <strong>PRE</strong>order — корень <strong>первый</strong>, <strong>IN</strong>order — корень <strong>между</strong>, <strong>POST</strong>order — корень <strong>после</strong>.') + warn('Рекурсивные обходы используют стек вызовов. Для очень глубоких деревьев (n > 1000) возможна ошибка RecursionError. Используйте итеративные версии с явным стеком.'),
'code_example': '''from collections import deque

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def build_bst(values):
    def ins(root, v):
        if not root: return TreeNode(v)
        if v < root.val: root.left = ins(root.left, v)
        else: root.right = ins(root.right, v)
        return root
    root = None
    for v in values: root = ins(root, v)
    return root

root = build_bst([8, 3, 10, 1, 6, 14, 4, 7])

# Рекурсивные обходы
def inorder(n, r=None):
    r = r or []
    if n: inorder(n.left, r); r.append(n.val); inorder(n.right, r)
    return r

def preorder(n, r=None):
    r = r or []
    if n: r.append(n.val); preorder(n.left, r); preorder(n.right, r)
    return r

def postorder(n, r=None):
    r = r or []
    if n: postorder(n.left, r); postorder(n.right, r); r.append(n.val)
    return r

def level_order(root):
    if not root: return []
    res, q = [], deque([root])
    while q:
        lvl = []
        for _ in range(len(q)):
            n = q.popleft(); lvl.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        res.append(lvl)
    return res

print("Inorder   (сортировка):", inorder(root))
print("Preorder  (структура):", preorder(root))
print("Postorder (снизу вверх):", postorder(root))
print("По уровням:", level_order(root))

# Итеративный inorder (без рекурсии)
def inorder_iterative(root):
    result, stack, cur = [], [], root
    while cur or stack:
        while cur: stack.append(cur); cur = cur.left
        cur = stack.pop(); result.append(cur.val); cur = cur.right
    return result

print("Итеративный inorder:", inorder_iterative(root))
'''
},
{
'title': 'Удаление узла в BST',
'order': 4,
'estimated_minutes': 65,
'content': '''
<h2>Удаление узла из BST — три случая</h2>
<p>Удаление сложнее вставки, потому что нужно сохранить свойство BST. В зависимости от положения узла возникают три ситуации.</p>
''' + table(
    ['Случай', 'Описание', 'Решение'],
    [
        ['1. Узел — лист', 'Нет потомков', 'Просто удалить, обнулить ссылку родителя'],
        ['2. Один потомок', 'Есть только левый или только правый', 'Заменить узел его потомком'],
        ['3. Два потомка', 'Есть оба потомка', 'Заменить значением inorder-преемника (минимума правого поддерева), затем удалить преемника'],
    ]
) + diagram(
    '<text x="300" y="18" text-anchor="middle" font-size="12" fill="#374151" font-weight="bold">Случай 3: удаляем 3 (два потомка)</text>'
    '<circle cx="300" cy="50" r="20" fill="#667eea" stroke="#4f46e5" stroke-width="2"/>'
    '<text x="300" y="56" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">8</text>'
    '<line x1="283" y1="65" x2="210" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="190" cy="115" r="20" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>'
    '<text x="190" y="121" text-anchor="middle" font-size="13" fill="#991b1b" font-weight="bold">3</text>'
    '<text x="190" y="155" text-anchor="middle" font-size="10" fill="#dc2626">удаляем</text>'
    '<line x1="175" y1="133" x2="130" y2="165" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="205" y1="133" x2="250" y2="165" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="115" cy="180" r="18" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="115" y="186" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">1</text>'
    '<circle cx="265" cy="180" r="18" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>'
    '<text x="265" y="186" text-anchor="middle" font-size="12" fill="#166534" font-weight="bold">4</text>'
    '<text x="265" y="210" text-anchor="middle" font-size="10" fill="#16a34a">преемник!</text>'
    '<line x1="265" y1="162" x2="230" y2="133" stroke="#16a34a" stroke-width="2" stroke-dasharray="4,2"/>'
    '<text x="370" y="115" font-size="10" fill="#64748b">Шаги:</text>'
    '<text x="370" y="130" font-size="10" fill="#64748b">1. Найти min правого</text>'
    '<text x="370" y="145" font-size="10" fill="#64748b">   поддерева = 4</text>'
    '<text x="370" y="160" font-size="10" fill="#64748b">2. Копируем 4 в узел 3</text>'
    '<text x="370" y="175" font-size="10" fill="#64748b">3. Удаляем 4 из правого</text>',
    w=560, h=230, caption='Удаление узла с двумя потомками через inorder-преемника'
) + '''
<pre><code>def delete(self, val):
    self.root = self._delete(self.root, val)

def _delete(self, node, val):
    if node is None:
        return None                    # элемент не найден

    if val < node.val:
        node.left = self._delete(node.left, val)
    elif val > node.val:
        node.right = self._delete(node.right, val)
    else:
        # Нашли узел для удаления
        if node.left is None:          # Случай 1 и 2: нет левого
            return node.right
        elif node.right is None:       # Случай 2: нет правого
            return node.left
        else:                          # Случай 3: два потомка
            # Находим inorder-преемника (минимум правого поддерева)
            successor = self._min_node(node.right)
            node.val = successor.val   # копируем значение
            # Удаляем преемника из правого поддерева
            node.right = self._delete(node.right, successor.val)

    return node

def _min_node(self, node):
    while node.left:
        node = node.left
    return node
</code></pre>
''' + tip('Вместо inorder-преемника можно использовать inorder-предшественника (максимум левого поддерева) — оба подхода корректны. Некоторые реализации чередуют их для поддержания баланса.'),
'code_example': '''class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

class BST:
    def __init__(self): self.root = None

    def insert(self, val):
        def ins(n, v):
            if not n: return TreeNode(v)
            if v < n.val: n.left = ins(n.left, v)
            elif v > n.val: n.right = ins(n.right, v)
            return n
        self.root = ins(self.root, val)

    def delete(self, val):
        def _min(n):
            while n.left: n = n.left
            return n
        def _del(n, v):
            if not n: return None
            if v < n.val: n.left = _del(n.left, v)
            elif v > n.val: n.right = _del(n.right, v)
            else:
                if not n.left: return n.right
                if not n.right: return n.left
                succ = _min(n.right)
                n.val = succ.val
                n.right = _del(n.right, succ.val)
            return n
        self.root = _del(self.root, val)

    def inorder(self):
        def _in(n, r):
            if n: _in(n.left, r); r.append(n.val); _in(n.right, r)
            return r
        return _in(self.root, [])

bst = BST()
for v in [8, 3, 10, 1, 6, 14, 4, 7, 13]: bst.insert(v)
print("Начало:", bst.inorder())

# Удаление листа (1)
bst.delete(1); print("Удалили лист 1:", bst.inorder())

# Удаление узла с одним потомком (14 → остаётся 13)
bst.delete(14); print("Удалили 14 (один потомок):", bst.inorder())

# Удаление узла с двумя потомками (3 → преемник 4)
bst.delete(3); print("Удалили 3 (два потомка):", bst.inorder())

# Удаление корня (8)
bst.delete(8); print("Удалили корень 8:", bst.inorder())
'''
},
]
},


# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 26 — ГРАФЫ: BFS И DFS
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Графы: BFS и DFS',
'icon': 'fas fa-project-diagram',
'order': 26,
'description': 'Графы: представление, обход в ширину (BFS) и обход в глубину (DFS), применения.',
'lessons': [
{
'title': 'Введение в графы',
'order': 1,
'estimated_minutes': 65,
'content': '''
<h2>Что такое граф?</h2>
<p><strong>Граф G = (V, E)</strong> — набор <em>вершин</em> (vertices, V) и <em>рёбер</em> (edges, E), соединяющих пары вершин. Графы моделируют отношения между объектами: карты дорог, социальные сети, зависимости пакетов, схемы цепей.</p>
''' + table(
    ['Вид графа', 'Описание', 'Пример'],
    [
        ['Неориентированный', 'Рёбра без направления', 'Дружба в соцсети'],
        ['Ориентированный (диграф)', 'Рёбра со стрелками', 'Ссылки в интернете'],
        ['Взвешенный', 'Рёбра имеют вес/стоимость', 'Карта с расстояниями'],
        ['Ациклический (DAG)', 'Нет циклов (ориент.)', 'Зависимости задач, git commit graph'],
        ['Связный', 'Из любой вершины добраться до любой', 'Полноценная дорожная сеть'],
    ]
) + '''
<h3>Способы представления графа</h3>
<p><strong>Матрица смежности</strong>: двумерный массив adj[i][j] = 1, если есть ребро (i,j). Быстрая проверка наличия ребра O(1), но расходует O(V²) памяти.</p>
<p><strong>Список смежности</strong>: словарь/массив, где adj[v] — список соседей v. Экономична по памяти O(V+E), обход соседей O(degree(v)).</p>
''' + diagram(
    '<text x="140" y="20" text-anchor="middle" font-size="12" fill="#374151" font-weight="bold">Граф</text>'
    '<circle cx="140" cy="80" r="20" fill="#667eea" stroke="#4f46e5" stroke-width="2"/><text x="140" y="86" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">0</text>'
    '<circle cx="60" cy="160" r="20" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/><text x="60" y="166" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">1</text>'
    '<circle cx="220" cy="160" r="20" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/><text x="220" y="166" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">2</text>'
    '<circle cx="60" cy="240" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/><text x="60" y="246" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">3</text>'
    '<circle cx="220" cy="240" r="20" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/><text x="220" y="246" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">4</text>'
    '<line x1="125" y1="97" x2="75" y2="143" stroke="#374151" stroke-width="1.5"/>'
    '<line x1="155" y1="97" x2="205" y2="143" stroke="#374151" stroke-width="1.5"/>'
    '<line x1="60" y1="180" x2="60" y2="220" stroke="#374151" stroke-width="1.5"/>'
    '<line x1="80" y1="170" x2="200" y2="170" stroke="#374151" stroke-width="1.5"/>'
    '<line x1="220" y1="180" x2="220" y2="220" stroke="#374151" stroke-width="1.5"/>'
    '<rect x="310" y="40" width="260" height="200" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>'
    '<text x="440" y="60" text-anchor="middle" font-size="11" fill="#374151" font-weight="bold">Список смежности</text>'
    '<text x="320" y="80" font-size="10" fill="#374151" font-family="monospace">0: [1, 2]</text>'
    '<text x="320" y="100" font-size="10" fill="#374151" font-family="monospace">1: [0, 2, 3]</text>'
    '<text x="320" y="120" font-size="10" fill="#374151" font-family="monospace">2: [0, 1, 4]</text>'
    '<text x="320" y="140" font-size="10" fill="#374151" font-family="monospace">3: [1]</text>'
    '<text x="320" y="160" font-size="10" fill="#374151" font-family="monospace">4: [2]</text>',
    w=590, h=280, caption='Граф из 5 вершин и его список смежности'
) + tip('Для разреженных графов (E << V²) используйте список смежности — он экономнее. Для плотных графов (почти все пары соединены) матрица смежности может быть удобнее.'),
'code_example': '''# Представление графа через словарь (список смежности)
graph = {
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 4],
    3: [1],
    4: [2]
}

# Класс Graph
class Graph:
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v, weight=None):
        self.add_vertex(u); self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def neighbors(self, v): return self.adj.get(v, [])
    def vertices(self): return list(self.adj.keys())
    def degree(self, v): return len(self.adj.get(v, []))

g = Graph()
edges = [(0,1),(0,2),(1,2),(1,3),(2,4)]
for u, v in edges: g.add_edge(u, v)

for v in sorted(g.vertices()):
    print(f"  {v}: соседи={g.neighbors(v)}, степень={g.degree(v)}")
'''
},
{
'title': 'BFS — обход в ширину',
'order': 2,
'estimated_minutes': 70,
'content': '''
<h2>BFS — Breadth-First Search</h2>
<p>BFS (<strong>обход в ширину</strong>) посещает все вершины на расстоянии 1 от старта, затем на расстоянии 2, затем 3 и т.д. — как волна, расходящаяся по воде. Реализуется через <strong>очередь</strong>.</p>
''' + diagram(
    '<circle cx="300" cy="40" r="22" fill="#667eea" stroke="#4f46e5" stroke-width="2"/>'
    '<text x="300" y="46" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">S</text>'
    '<text x="330" y="30" font-size="10" fill="#64748b">уровень 0</text>'
    '<line x1="283" y1="58" x2="185" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="317" y1="58" x2="415" y2="100" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="165" cy="120" r="20" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="165" y="126" text-anchor="middle" font-size="12" fill="#fff">A</text>'
    '<circle cx="435" cy="120" r="20" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="435" y="126" text-anchor="middle" font-size="12" fill="#fff">B</text>'
    '<text x="490" y="112" font-size="10" fill="#64748b">уровень 1</text>'
    '<line x1="150" y1="138" x2="100" y2="178" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="180" y1="138" x2="260" y2="178" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="420" y1="138" x2="340" y2="178" stroke="#94a3b8" stroke-width="1.5"/>'
    '<circle cx="80" cy="198" r="18" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="80" y="204" text-anchor="middle" font-size="11" fill="#fff">C</text>'
    '<circle cx="280" cy="198" r="18" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="280" y="204" text-anchor="middle" font-size="11" fill="#fff">D</text>'
    '<circle cx="320" cy="198" r="18" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="320" y="204" text-anchor="middle" font-size="11" fill="#fff">E</text>'
    '<text x="490" y="192" font-size="10" fill="#64748b">уровень 2</text>',
    w=580, h=240, caption='BFS: сначала все соседи, потом их соседи'
) + '''
<h3>Алгоритм BFS</h3>
<pre><code>from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        vertex = queue.popleft()     # берём из начала очереди
        order.append(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # добавляем в конец

    return order

# Кратчайший путь в невзвешенном графе
def bfs_shortest_path(graph, start, end):
    if start == end: return [start]
    visited = {start}
    queue = deque([(start, [start])])  # (вершина, путь до неё)

    while queue:
        vertex, path = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path       # нашли!
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    return None  # пути нет
</code></pre>
''' + table(
    ['Характеристика BFS', 'Значение'],
    [
        ['Структура данных', 'Очередь (FIFO)'],
        ['Временная сложность', 'O(V + E)'],
        ['Пространственная сложность', 'O(V) — в очереди максимум V вершин'],
        ['Гарантия кратчайшего пути', 'Да — в невзвешенном графе'],
        ['Применения', 'Кратчайший путь, проверка связности, уровни дерева'],
    ]
) + warn('BFS находит кратчайший путь только в <strong>невзвешенном</strong> графе (или когда все рёбра одного веса). Для взвешенных графов используйте алгоритм Дейкстры.'),
'code_example': '''from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"]
}

def bfs(graph, start):
    visited, queue, order = {start}, deque([start]), []
    while queue:
        v = queue.popleft(); order.append(v)
        for nb in graph[v]:
            if nb not in visited:
                visited.add(nb); queue.append(nb)
    return order

def bfs_path(graph, start, end):
    q = deque([(start, [start])])
    visited = {start}
    while q:
        v, path = q.popleft()
        for nb in graph[v]:
            if nb == end: return path + [nb]
            if nb not in visited:
                visited.add(nb); q.append((nb, path + [nb]))
    return None

def bfs_distances(graph, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        v = q.popleft()
        for nb in graph[v]:
            if nb not in dist:
                dist[nb] = dist[v] + 1
                q.append(nb)
    return dist

print("BFS порядок от A:", bfs(graph, "A"))
print("Путь A→F:", bfs_path(graph, "A", "F"))
print("Расстояния от A:", bfs_distances(graph, "A"))
'''
},
{
'title': 'DFS — обход в глубину',
'order': 3,
'estimated_minutes': 65,
'content': '''
<h2>DFS — Depth-First Search</h2>
<p>DFS (<strong>обход в глубину</strong>) идёт как можно глубже по каждой ветке, прежде чем отступать назад. Реализуется через <strong>рекурсию</strong> (неявный стек) или явный <strong>стек</strong>.</p>
<pre><code># Рекурсивный DFS
def dfs_recursive(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    visited.add(vertex)
    print(vertex, end=" ")

    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# Итеративный DFS (явный стек)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        vertex = stack.pop()    # берём с верхушки стека
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            # Добавляем соседей (в обратном порядке для того же обхода)
            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order
</code></pre>
''' + table(
    ['', 'BFS', 'DFS'],
    [
        ['Структура данных', 'Очередь (FIFO)', 'Стек (LIFO) / рекурсия'],
        ['Порядок обхода', 'По уровням (ширина)', 'По веткам (глубина)'],
        ['Кратчайший путь', 'Да (невзвешенный)', 'Нет'],
        ['Сложность', 'O(V+E)', 'O(V+E)'],
        ['Применения', 'Кратчайший путь, уровни', 'Топологическая сортировка, циклы, компоненты'],
    ]
) + '''
<h3>Топологическая сортировка</h3>
<p>В ориентированном ациклическом графе (DAG) топологическая сортировка даёт порядок вершин, при котором для каждого ребра (u→v) вершина u стоит раньше v. Используется для порядка выполнения задач.</p>
<pre><code>def topological_sort(graph):
    visited = set()
    result = []

    def dfs(v):
        visited.add(v)
        for neighbor in graph.get(v, []):
            if neighbor not in visited:
                dfs(neighbor)
        result.append(v)   # добавляем ПОСЛЕ обхода всех потомков

    for v in graph:
        if v not in visited:
            dfs(v)

    return result[::-1]   # разворачиваем
</code></pre>
''' + tip('Топологическая сортировка применяется везде, где нужен порядок зависимостей: планировщики задач, системы сборки (make, gradle), порядок компиляции модулей, разрешение зависимостей пакетов (pip).'),
'code_example': '''graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": []
}

def dfs_recursive(graph, v, visited=None, order=None):
    if visited is None: visited, order = set(), []
    visited.add(v); order.append(v)
    for nb in graph[v]:
        if nb not in visited:
            dfs_recursive(graph, nb, visited, order)
    return order

def dfs_iterative(graph, start):
    visited, stack, order = set(), [start], []
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v); order.append(v)
            for nb in reversed(graph[v]):
                if nb not in visited: stack.append(nb)
    return order

print("DFS рекурсивный:", dfs_recursive(graph, "A"))
print("DFS итеративный:", dfs_iterative(graph, "A"))

# Поиск всех путей между двумя вершинами
def all_paths(graph, start, end, path=None):
    path = (path or []) + [start]
    if start == end: return [path]
    paths = []
    for nb in graph.get(start, []):
        if nb not in path:
            paths.extend(all_paths(graph, nb, end, path))
    return paths

print("Все пути A→F:", all_paths(graph, "A", "F"))

# Проверка наличия цикла (неориентированный граф)
def has_cycle(graph):
    visited = set()
    def dfs(v, parent):
        visited.add(v)
        for nb in graph[v]:
            if nb not in visited:
                if dfs(nb, v): return True
            elif nb != parent: return True
        return False
    for v in graph:
        if v not in visited:
            if dfs(v, None): return True
    return False
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 27 — ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Динамическое программирование',
'icon': 'fas fa-table',
'order': 27,
'description': 'Мемоизация, табуляция, классические задачи: Fibonacci, рюкзак, НОП, НОВ.',
'lessons': [
{
'title': 'Идея ДП: мемоизация и табуляция',
'order': 1,
'estimated_minutes': 70,
'content': '''
<h2>Что такое динамическое программирование?</h2>
<p><strong>Динамическое программирование (ДП)</strong> — метод оптимизации, применимый к задачам с двумя свойствами:</p>
<ul>
  <li><strong>Перекрывающиеся подзадачи</strong> — одна и та же подзадача решается многократно</li>
  <li><strong>Оптимальная подструктура</strong> — оптимальное решение задачи складывается из оптимальных решений подзадач</li>
</ul>
<p>Идея: <em>решать каждую подзадачу один раз и сохранять результат</em>.</p>
''' + diagram(
    '<text x="300" y="18" text-anchor="middle" font-size="12" fill="#374151" font-weight="bold">fib(5) без мемоизации: 15 вызовов</text>'
    '<rect x="260" y="30" width="80" height="28" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>'
    '<text x="300" y="49" text-anchor="middle" font-size="11" fill="#991b1b" font-weight="bold">fib(5)</text>'
    '<line x1="285" y1="58" x2="195" y2="82" stroke="#94a3b8" stroke-width="1"/>'
    '<line x1="315" y1="58" x2="405" y2="82" stroke="#94a3b8" stroke-width="1"/>'
    '<rect x="155" y="82" width="70" height="25" rx="3" fill="#fef9c3" stroke="#f59e0b" stroke-width="1"/>'
    '<text x="190" y="99" text-anchor="middle" font-size="10" fill="#854d0e">fib(4)</text>'
    '<rect x="370" y="82" width="70" height="25" rx="3" fill="#fef9c3" stroke="#f59e0b" stroke-width="1"/>'
    '<text x="405" y="99" text-anchor="middle" font-size="10" fill="#854d0e">fib(3)</text>'
    '<line x1="175" y1="107" x2="115" y2="131" stroke="#94a3b8" stroke-width="1"/>'
    '<line x1="205" y1="107" x2="265" y2="131" stroke="#94a3b8" stroke-width="1"/>'
    '<line x1="383" y1="107" x2="323" y2="131" stroke="#94a3b8" stroke-width="1"/>'
    '<line x1="418" y1="107" x2="478" y2="131" stroke="#94a3b8" stroke-width="1"/>'
    '<rect x="80" y="131" width="65" height="23" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>'
    '<text x="113" y="147" text-anchor="middle" font-size="10" fill="#166534">fib(3)★</text>'
    '<rect x="235" y="131" width="65" height="23" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>'
    '<text x="268" y="147" text-anchor="middle" font-size="10" fill="#166534">fib(2)★</text>'
    '<rect x="290" y="131" width="65" height="23" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>'
    '<text x="323" y="147" text-anchor="middle" font-size="10" fill="#166534">fib(2)★</text>'
    '<rect x="445" y="131" width="65" height="23" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>'
    '<text x="478" y="147" text-anchor="middle" font-size="10" fill="#166534">fib(1)</text>'
    '<text x="300" y="185" text-anchor="middle" font-size="10" fill="#dc2626">★ — повторные вычисления (fib(3) считается 2 раза, fib(2) — 3 раза!)</text>',
    w=580, h=200, caption='Дерево рекурсии fib(5): многие подзадачи решаются повторно'
) + '''
<h3>Подход 1: Мемоизация (top-down)</h3>
<p>Решаем рекурсивно, но сохраняем результаты в кэше. «Сверху вниз»: от большой задачи к маленьким.</p>
<pre><code>from functools import lru_cache

# С lru_cache (декоратор)
@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1: return n
    return fib_memo(n-1) + fib_memo(n-2)

# Вручную через словарь
def fib_dict(n, memo={}):
    if n in memo: return memo[n]     # уже посчитано!
    if n <= 1: return n
    memo[n] = fib_dict(n-1, memo) + fib_dict(n-2, memo)
    return memo[n]
</code></pre>
<h3>Подход 2: Табуляция (bottom-up)</h3>
<p>Строим таблицу с ответами, начиная от базовых случаев. «Снизу вверх»: от маленьких задач к большим. Итеративно, без рекурсии.</p>
<pre><code>def fib_tab(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Оптимизация памяти: нужны только два последних
def fib_opt(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
</code></pre>
''' + table(
    ['Характеристика', 'Мемоизация (top-down)', 'Табуляция (bottom-up)'],
    [
        ['Стиль', 'Рекурсивный', 'Итеративный'],
        ['Порядок решения', 'Только нужные подзадачи', 'Все подзадачи по порядку'],
        ['Стек вызовов', 'Использует (риск переполнения)', 'Не использует'],
        ['Скорость на практике', 'Немного медленнее', 'Немного быстрее'],
        ['Когда удобнее', 'Подзадачи сложно упорядочить', 'Порядок подзадач ясен'],
    ]
) + tip('Правило выбора: если граф подзадач — DAG с очевидным порядком (как массив), выбирайте табуляцию. Если граф сложный или не все подзадачи нужны — мемоизацию.'),
'code_example': '''import time
from functools import lru_cache

# Сравнение трёх подходов
def fib_naive(n):
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)

@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1: return n
    return fib_memo(n-1) + fib_memo(n-2)

def fib_tab(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n+1): a, b = b, a+b
    return b

# Замер времени
n = 35
t = time.perf_counter(); r = fib_naive(n); naive_t = time.perf_counter()-t
t = time.perf_counter(); r = fib_memo(n); memo_t  = time.perf_counter()-t
t = time.perf_counter(); r = fib_tab(n);  tab_t   = time.perf_counter()-t

print(f"fib({n}) = {r}")
print(f"Наивная рекурсия: {naive_t:.4f}с")
print(f"Мемоизация:       {memo_t:.6f}с  (быстрее в {naive_t/memo_t:.0f}x)")
print(f"Табуляция:        {tab_t:.6f}с")

# Число способов подняться по n ступенькам (1 или 2 шага за раз)
def climb_stairs(n):
    if n <= 2: return n
    dp = [0] * (n+1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n+1): dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

for n in [1, 5, 10, 20]:
    print(f"  Ступенек {n}: {climb_stairs(n)} способов")
'''
},
{
'title': 'Задача о рюкзаке (0-1 Knapsack)',
'order': 2,
'estimated_minutes': 75,
'content': '''
<h2>Задача о рюкзаке (0-1 Knapsack)</h2>
<p><strong>Постановка:</strong> есть рюкзак вместимостью W и n предметов, каждый с весом weights[i] и ценностью values[i]. Каждый предмет можно взять или не взять (0 или 1 раз). Найти максимальную суммарную ценность при суммарном весе ≤ W.</p>
''' + table(
    ['Предмет', 'Вес', 'Ценность', 'Ценность/Вес'],
    [
        ['Ноутбук', '3 кг', '4000 ₽', '1333'],
        ['Телефон', '1 кг', '3000 ₽', '3000'],
        ['Книги', '4 кг', '1000 ₽', '250'],
        ['Планшет', '2 кг', '2500 ₽', '1250'],
    ]
) + '''
<p>Жадный алгоритм (брать лучшее по отношению ценность/вес) не даёт оптимального ответа. Нужно ДП.</p>
<h3>DP-решение через 2D-таблицу</h3>
<p><code>dp[i][w]</code> = максимальная ценность при рассмотрении первых i предметов и ёмкости w.</p>
<p><strong>Переход:</strong> если weight[i] > w, предмет не берём: <code>dp[i][w] = dp[i-1][w]</code>. Иначе берём лучшее из двух: взять предмет или нет: <code>dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])</code>.</p>
<pre><code>def knapsack(weights, values, capacity):
    n = len(weights)
    # dp[i][w] — макс. ценность при i предметах и ёмкости w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i-1]
        v_i = values[i-1]
        for w in range(capacity + 1):
            # Не берём i-й предмет
            dp[i][w] = dp[i-1][w]
            # Берём i-й предмет (если помещается)
            if w_i <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - w_i] + v_i)

    return dp[n][capacity], dp  # ценность и таблица для восстановления
</code></pre>
''' + tip('Восстановление набора предметов: идём по таблице dp с позиции [n][W] назад. Если dp[i][w] != dp[i-1][w] — предмет i был взят, уменьшаем w на weight[i].') + warn('Сложность O(n×W) — это псевдополиномиальная сложность. При W = 10¹⁰ таблица не влезет в память. Для больших W используют другие подходы (например, перебор с отсечениями).'),
'code_example': '''def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0]*(capacity+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for w in range(capacity+1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])

    # Восстановление набора
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            chosen.append(i-1)
            w -= weights[i-1]

    return dp[n][capacity], chosen

weights = [3, 1, 4, 2]
values  = [4000, 3000, 1000, 2500]
names   = ["Ноутбук", "Телефон", "Книги", "Планшет"]
capacity = 5

max_val, items = knapsack(weights, values, capacity)
print(f"Максимальная ценность: {max_val} ₽")
print(f"Взять: {[names[i] for i in items]}")
print(f"Вес: {sum(weights[i] for i in items)} кг из {capacity} кг")

# Оптимизированная версия O(W) памяти
def knapsack_1d(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w_i, v_i in zip(weights, values):
        for w in range(capacity, w_i - 1, -1):  # обратный порядок!
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[capacity]

print(f"Оптимизированный ответ: {knapsack_1d(weights, values, capacity)} ₽")
'''
},
{
'title': 'НОП (LCS) и НОВ (LIS)',
'order': 3,
'estimated_minutes': 70,
'content': '''
<h2>Наибольшая общая подпоследовательность (LCS)</h2>
<p><strong>LCS (Longest Common Subsequence)</strong> — наибольшая подпоследовательность, которая встречается и в строке A, и в строке B. Подпоследовательность не обязана быть непрерывной.</p>
<p>Пример: LCS("ABCBDAB", "BDCAB") = "BCAB" или "BDAB" (длина 4).</p>
''' + table(
    ['Термин', 'Определение', 'Пример'],
    [
        ['Подстрока (substring)', 'Непрерывная часть строки', '"ABC" в "XABCDE"'],
        ['Подпоследовательность', 'Символы в исходном порядке, не обязательно рядом', '"ACD" в "ABCDE"'],
        ['LCS', 'Самая длинная общая подпоследовательность', 'LCS("AGGTAB","GXTXAYB")="GTAB"'],
    ]
) + '''
<p><strong>DP-переход:</strong> если A[i] == B[j]: <code>dp[i][j] = dp[i-1][j-1] + 1</code>, иначе: <code>dp[i][j] = max(dp[i-1][j], dp[i][j-1])</code></p>
<pre><code>def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Восстановление строки
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            result.append(a[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(result))
</code></pre>
<h2>Наибольшая возрастающая подпоследовательность (LIS)</h2>
<p><strong>LIS (Longest Increasing Subsequence)</strong> — наибольшая подпоследовательность, в которой каждый следующий элемент строго больше предыдущего.</p>
<p>Пример: LIS([10, 9, 2, 5, 3, 7, 101, 18]) = [2, 3, 7, 101] или [2, 5, 7, 101] (длина 4).</p>
<pre><code>def lis_dp(arr):
    """O(n²) DP"""
    n = len(arr)
    dp = [1] * n  # каждый элемент — подпоследовательность длины 1

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

def lis_binary(arr):
    """O(n log n) через бинарный поиск"""
    import bisect
    tails = []
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)
</code></pre>
''' + tip('LCS применяется в diff-утилитах (git diff), биоинформатике (сравнение ДНК). LIS — в задачах сортировки пакетов, планирования расписаний, биржевом анализе.'),
'code_example': '''import bisect

def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]+1
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    i, j, res = m, n, []
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]: res.append(a[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]: i -= 1
        else: j -= 1
    return dp[m][n], "".join(reversed(res))

def lis(arr):
    tails = []
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails): tails.append(x)
        else: tails[pos] = x
    return len(tails)

# LCS
s1, s2 = "ABCBDAB", "BDCAB"
length, seq = lcs(s1, s2)
print(f"LCS('{s1}', '{s2}') = '{seq}', длина {length}")

# Расстояние редактирования (edit distance) — смежная задача
def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

print(f"Edit distance('kitten','sitting') = {edit_distance('kitten','sitting')}")

# LIS
arr = [10, 9, 2, 5, 3, 7, 101, 18]
print(f"LIS({arr}) = {lis(arr)}")
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 28 — JSON, CSV, DATETIME
# ═══════════════════════════════════════════════════════════════════
{
'title': 'JSON, CSV, datetime',
'icon': 'fas fa-database',
'order': 28,
'description': 'Работа с форматами данных JSON и CSV, модуль datetime для работы с датами и временем.',
'lessons': [
{
'title': 'Работа с JSON',
'order': 1,
'estimated_minutes': 60,
'content': '''
<h2>JSON — универсальный формат обмена данными</h2>
<p><strong>JSON (JavaScript Object Notation)</strong> — текстовый формат для хранения и передачи структурированных данных. Стал стандартом в веб-разработке и API. Python-модуль <code>json</code> встроен в стандартную библиотеку.</p>
''' + table(
    ['Тип Python', 'Тип JSON', 'Пример'],
    [
        ['dict', 'object', '{"key": "value"}'],
        ['list, tuple', 'array', '[1, 2, 3]'],
        ['str', 'string', '"текст"'],
        ['int, float', 'number', '42, 3.14'],
        ['True / False', 'true / false', 'true'],
        ['None', 'null', 'null'],
        ['set, bytes, datetime', '❌ не поддерживается', 'Нужна кастомизация'],
    ]
) + '''
<h3>Основные функции</h3>
<pre><code>import json

# Сериализация: Python → JSON строка
data = {"name": "Иван", "grades": [85, 92, 78], "active": True}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# Десериализация: JSON строка → Python
restored = json.loads(json_str)
print(type(restored))  # dict

# Запись в файл
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Чтение из файла
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
</code></pre>
''' + tip('<code>ensure_ascii=False</code> — обязательно для кириллицы! Без него русские символы превратятся в \\uXXXX. <code>indent=2</code> — красивое форматирование с отступами.') + '''
<h3>Кастомная сериализация</h3>
<pre><code>from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()   # "2024-01-15T10:30:00"
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data = {"ts": datetime.now(), "tags": {"python", "json"}}
print(json.dumps(data, cls=CustomEncoder, ensure_ascii=False))
</code></pre>
''' + warn('json.loads() может бросить <code>json.JSONDecodeError</code> при невалидном JSON. Всегда оборачивайте в try/except при работе с внешними данными.'),
'code_example': '''import json
from pathlib import Path

# Сохранение и загрузка данных студентов
students = [
    {"id": 1, "name": "Анна Смирнова", "grades": {"math": 95, "python": 88}, "active": True},
    {"id": 2, "name": "Борис Козлов",  "grades": {"math": 72, "python": 91}, "active": True},
    {"id": 3, "name": "Вера Попова",   "grades": {"math": 88, "python": 79}, "active": False},
]

# Сохранить
path = Path("students.json")
path.write_text(json.dumps(students, ensure_ascii=False, indent=2), encoding="utf-8")
print("Сохранено:", path.stat().st_size, "байт")

# Загрузить и обработать
loaded = json.loads(path.read_text(encoding="utf-8"))

# Аналитика
active = [s for s in loaded if s["active"]]
avg_python = sum(s["grades"]["python"] for s in active) / len(active)
top_student = max(loaded, key=lambda s: sum(s["grades"].values()))

print(f"Активных студентов: {len(active)}")
print(f"Средняя оценка по Python: {avg_python:.1f}")
print(f"Лучший студент: {top_student['name']}")

# Обновить и пересохранить
for s in loaded:
    s["average"] = round(sum(s["grades"].values()) / len(s["grades"]), 1)
path.write_text(json.dumps(loaded, ensure_ascii=False, indent=2), encoding="utf-8")
print("Обновлено с полем average")
'''
},
{
'title': 'Работа с CSV',
'order': 2,
'estimated_minutes': 60,
'content': '''
<h2>CSV — табличные данные в текстовом формате</h2>
<p><strong>CSV (Comma-Separated Values)</strong> — простой формат таблиц: каждая строка — это запись, поля разделены запятой (или другим разделителем). Открывается в Excel, читается человеком. Модуль <code>csv</code> встроен в Python.</p>
''' + table(
    ['Метод', 'Описание', 'Когда использовать'],
    [
        ['csv.reader', 'Читает строки как списки строк', 'Простые данные без заголовка'],
        ['csv.writer', 'Записывает списки в CSV', 'Простой вывод'],
        ['csv.DictReader', 'Строки как словари {заголовок: значение}', 'Данные с заголовком'],
        ['csv.DictWriter', 'Записывает словари в CSV', 'Структурированный вывод'],
    ]
) + '''
<pre><code>import csv

# Запись через DictWriter
students = [
    {"имя": "Анна", "оценка": 95, "группа": "ИС-21"},
    {"имя": "Борис", "оценка": 88, "группа": "ИС-21"},
]
with open("grades.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["имя", "оценка", "группа"])
    writer.writeheader()      # строка заголовков
    writer.writerows(students)  # все строки

# Чтение через DictReader
with open("grades.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["имя"], row["оценка"])
</code></pre>
''' + tip('Всегда используйте <code>newline=""</code> при открытии CSV-файла в режиме записи — иначе Python добавит лишние пустые строки на Windows. Кодировка <code>utf-8-sig</code> (с BOM) для корректного открытия в Excel.') + warn('Значения с запятой или переносом строки в поле csv автоматически оборачиваются в кавычки. Не пытайтесь парсить CSV вручную через split(",") — это не работает в общем случае!'),
'code_example': '''import csv
from io import StringIO

# Создаём CSV в памяти (без файла)
output = StringIO()
writer = csv.DictWriter(output, fieldnames=["студент", "задание", "балл"])
writer.writeheader()
records = [
    {"студент": "Анна",  "задание": "Лаб1", "балл": 95},
    {"студент": "Борис", "задание": "Лаб1", "балл": 88},
    {"студент": "Анна",  "задание": "Лаб2", "балл": 92},
    {"студент": "Борис", "задание": "Лаб2", "балл": 75},
    {"студент": "Вера",  "задание": "Лаб1", "балл": 83},
]
writer.writerows(records)
csv_text = output.getvalue()
print("CSV содержимое:")
print(csv_text)

# Читаем обратно и строим сводку
reader = csv.DictReader(StringIO(csv_text))
by_student = {}
for row in reader:
    name = row["студент"]
    score = int(row["балл"])
    if name not in by_student:
        by_student[name] = []
    by_student[name].append(score)

print("Средние баллы:")
for student, scores in sorted(by_student.items()):
    avg = sum(scores) / len(scores)
    print(f"  {student}: {avg:.1f} ({len(scores)} работ)")
'''
},
{
'title': 'Модуль datetime: даты и время',
'order': 3,
'estimated_minutes': 65,
'content': '''
<h2>Работа с датами и временем в Python</h2>
<p>Модуль <code>datetime</code> предоставляет классы для работы с датами, временем и временными интервалами. Правильная обработка дат — критически важный навык, ведь ошибки здесь приводят к трудноуловимым багам.</p>
''' + table(
    ['Класс', 'Описание', 'Пример создания'],
    [
        ['date', 'Только дата (год, месяц, день)', 'date(2024, 1, 15)'],
        ['time', 'Только время (ч, мин, сек, мксек)', 'time(10, 30, 0)'],
        ['datetime', 'Дата + время', 'datetime(2024, 1, 15, 10, 30)'],
        ['timedelta', 'Интервал времени', 'timedelta(days=7, hours=2)'],
        ['timezone', 'Информация о часовом поясе', 'timezone.utc'],
    ]
) + '''
<pre><code>from datetime import datetime, date, timedelta

# Текущее время
now = datetime.now()           # локальное
utc = datetime.utcnow()        # UTC (устарело, лучше ниже)

# Создание
dt = datetime(2024, 3, 15, 14, 30, 0)
d  = date(2024, 3, 15)

# Форматирование
print(now.strftime("%d.%m.%Y %H:%M"))    # "15.03.2024 14:30"
print(now.strftime("%A, %B %d, %Y"))     # "Friday, March 15, 2024"

# Парсинг строки → datetime
s = "2024-03-15 14:30:00"
parsed = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
print(type(parsed))  # datetime

# Арифметика
deadline = datetime(2024, 12, 31)
days_left = (deadline - datetime.now()).days
print(f"До конца года: {days_left} дней")

yesterday = date.today() - timedelta(days=1)
next_week = date.today() + timedelta(weeks=1)
</code></pre>
''' + table(
    ['Директива strftime', 'Значение', 'Пример'],
    [
        ['%Y', 'Год 4 цифры', '2024'],
        ['%m', 'Месяц 01-12', '03'],
        ['%d', 'День 01-31', '15'],
        ['%H', 'Час 00-23', '14'],
        ['%M', 'Минуты 00-59', '30'],
        ['%S', 'Секунды 00-59', '00'],
        ['%A', 'Название дня недели', 'Friday'],
        ['%B', 'Название месяца', 'March'],
        ['%j', 'День года 001-366', '075'],
        ['%U', 'Номер недели 00-53', '11'],
    ]
) + tip('ISO формат: <code>datetime.isoformat()</code> → "2024-03-15T14:30:00". Удобен для JSON и БД. Обратно: <code>datetime.fromisoformat("2024-03-15T14:30:00")</code>.'),
'code_example': '''from datetime import datetime, date, timedelta

# Вычисление возраста
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

birthday = date(2000, 6, 15)
print(f"Возраст: {calculate_age(birthday)} лет")

# Дни до дедлайна
def days_until(target_date):
    delta = target_date - date.today()
    return delta.days

deadline = date(2024, 12, 31)
d = days_until(deadline)
print(f"До 31 декабря: {d} дней" if d >= 0 else "Дедлайн прошёл!")

# Парсинг различных форматов
formats = ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y %H:%M"]
strings = ["15.03.2024", "2024-03-15", "15/03/2024 14:30"]
for fmt, s in zip(formats, strings):
    dt = datetime.strptime(s, fmt)
    print(f"  '{s}' → {dt.strftime('%d %B %Y')}")

# Рабочие дни между датами (упрощённо, без праздников)
def working_days(start, end):
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # 0-4 = пн-пт
            count += 1
        current += timedelta(days=1)
    return count

d1, d2 = date(2024, 3, 1), date(2024, 3, 31)
print(f"Рабочих дней в марте: {working_days(d1, d2)}")
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 29 — ООП: НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'ООП: наследование и полиморфизм',
'icon': 'fas fa-cubes',
'order': 29,
'description': 'Наследование, super(), полиморфизм, dunder-методы, инкапсуляция, @property, ABC.',
'lessons': [
{
'title': 'Наследование и super()',
'order': 1,
'estimated_minutes': 70,
'content': '''
<h2>Наследование в Python</h2>
<p><strong>Наследование</strong> — механизм ООП, позволяющий создавать новый класс на основе существующего, расширяя или изменяя его поведение. Дочерний класс получает все атрибуты и методы родительского класса.</p>
''' + diagram(
    '<rect x="220" y="10" width="160" height="55" rx="8" fill="#667eea" stroke="#4f46e5" stroke-width="2"/>'
    '<text x="300" y="32" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Animal</text>'
    '<text x="300" y="52" text-anchor="middle" font-size="10" fill="#c7d2fe">name, speak(), move()</text>'
    '<line x1="255" y1="65" x2="175" y2="110" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="300" y1="65" x2="300" y2="110" stroke="#94a3b8" stroke-width="1.5"/>'
    '<line x1="345" y1="65" x2="425" y2="110" stroke="#94a3b8" stroke-width="1.5"/>'
    '<rect x="100" y="110" width="150" height="55" rx="7" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="175" y="132" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">Dog</text>'
    '<text x="175" y="152" text-anchor="middle" font-size="10" fill="#e0e7ff">breed, fetch(), speak()</text>'
    '<rect x="225" y="110" width="150" height="55" rx="7" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="300" y="132" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">Cat</text>'
    '<text x="300" y="152" text-anchor="middle" font-size="10" fill="#e0e7ff">indoor, purr(), speak()</text>'
    '<rect x="350" y="110" width="150" height="55" rx="7" fill="#818cf8" stroke="#4f46e5" stroke-width="1.5"/>'
    '<text x="425" y="132" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">Bird</text>'
    '<text x="425" y="152" text-anchor="middle" font-size="10" fill="#e0e7ff">wingspan, fly(), speak()</text>'
    '<line x1="150" y1="165" x2="130" y2="205" stroke="#94a3b8" stroke-width="1.5"/>'
    '<rect x="75" y="205" width="135" height="45" rx="6" fill="#a5b4fc" stroke="#818cf8" stroke-width="1"/>'
    '<text x="143" y="222" text-anchor="middle" font-size="11" fill="#fff" font-weight="bold">GoldenRetriever</text>'
    '<text x="143" y="239" text-anchor="middle" font-size="9" fill="#e0e7ff">color, guide()</text>',
    w=580, h=265, caption='Иерархия наследования: Animal → Dog/Cat/Bird → GoldenRetriever'
) + '''
<pre><code>class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        raise NotImplementedError("Подкласс должен реализовать speak()")

    def info(self):
        return f"{self.name} ({self.age} лет)"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)   # вызов конструктора родителя
        self.breed = breed

    def speak(self):
        return f"{self.name} говорит: Гав!"

    def fetch(self, item):
        return f"{self.name} принёс {item}"

    def info(self):
        return super().info() + f", порода: {self.breed}"  # расширение метода


class GoldenRetriever(Dog):
    def __init__(self, name, age, color="золотистый"):
        super().__init__(name, age, breed="Golden Retriever")
        self.color = color

    def guide(self):
        return f"{self.name} помогает хозяину ориентироваться"
</code></pre>
''' + table(
    ['Концепция', 'Описание', 'Синтаксис Python'],
    [
        ['Наследование', 'Дочерний класс получает методы родителя', 'class Child(Parent):'],
        ['Переопределение', 'Дочерний класс меняет реализацию метода', 'def method(self): ...'],
        ['Расширение', 'Дочерний класс добавляет к родительскому методу', 'super().method() + ...'],
        ['super()', 'Вызов метода родительского класса', 'super().__init__(...)'],
        ['isinstance()', 'Проверка типа с учётом наследования', 'isinstance(dog, Animal)'],
        ['issubclass()', 'Проверка отношения наследования', 'issubclass(Dog, Animal)'],
    ]
) + tip('MRO (Method Resolution Order) — порядок поиска метода при наследовании. Посмотреть: <code>ClassName.__mro__</code> или <code>ClassName.mro()</code>. Python использует алгоритм C3-линеаризации для корректной работы множественного наследования.'),
'code_example': '''class Animal:
    def __init__(self, name, age):
        self.name = name; self.age = age
    def speak(self): return f"{self.name}: ..."
    def info(self): return f"{self.name}, {self.age} лет"
    def __repr__(self): return f"{type(self).__name__}('{self.name}')"

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    def speak(self): return f"{self.name}: Гав!"
    def info(self): return super().info() + f", {self.breed}"

class Cat(Animal):
    def __init__(self, name, age, indoor=True):
        super().__init__(name, age)
        self.indoor = indoor
    def speak(self): return f"{self.name}: Мяу!"
    def purr(self): return f"{self.name}: Мурр..."

class GoldenRetriever(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, "Golden Retriever")
    def guide(self): return f"{self.name} — поводырь"

animals = [Dog("Бобик", 3, "Дворняга"), Cat("Мурка", 5), GoldenRetriever("Голди", 2)]

print("--- Полиморфизм ---")
for a in animals:
    print(f"  {a.speak()}")

print("--- isinstance ---")
for a in animals:
    print(f"  {a.name}: is Animal={isinstance(a, Animal)}, is Dog={isinstance(a, Dog)}")

print("--- MRO ---")
print("GoldenRetriever MRO:", [c.__name__ for c in GoldenRetriever.__mro__])
'''
},
{
'title': 'Dunder-методы и полиморфизм',
'order': 2,
'estimated_minutes': 65,
'content': '''
<h2>Dunder-методы (magic methods)</h2>
<p><strong>Dunder-методы</strong> (double underscore, «двойное подчёркивание») — специальные методы, которые Python вызывает автоматически в ответ на определённые операции: <code>+</code>, <code>len()</code>, <code>str()</code>, сравнения и т.д. Это основа <em>перегрузки операторов</em>.</p>
''' + table(
    ['Dunder-метод', 'Когда вызывается', 'Пример использования'],
    [
        ['__init__', 'Создание объекта', 'Инициализация атрибутов'],
        ['__repr__', 'repr(obj), в консоли', 'Однозначное текстовое представление'],
        ['__str__', 'str(obj), print(obj)', 'Читаемое строковое представление'],
        ['__len__', 'len(obj)', 'Длина коллекции'],
        ['__eq__', 'obj1 == obj2', 'Сравнение на равенство'],
        ['__lt__, __le__, __gt__', 'obj1 < obj2 и т.д.', 'Сравнение (для sorted())'],
        ['__add__', 'obj1 + obj2', 'Сложение'],
        ['__mul__', 'obj * n', 'Умножение'],
        ['__contains__', 'x in obj', 'Оператор in'],
        ['__iter__, __next__', 'for x in obj', 'Итерация'],
        ['__getitem__', 'obj[key]', 'Доступ по индексу/ключу'],
        ['__setitem__', 'obj[key] = val', 'Присваивание по индексу'],
        ['__enter__, __exit__', 'with obj:', 'Контекстный менеджер'],
    ]
) + '''
<h3>Пример: класс Vector с dunder-методами</h3>
<pre><code>import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):     # scalar * vector
        return self.__mul__(scalar)

    def __abs__(self):              # abs(v) — длина вектора
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):        # сравнение по длине
        return abs(self) < abs(other)

    def dot(self, other):           # скалярное произведение
        return self.x * other.x + self.y * other.y
</code></pre>
''' + tip('Реализуйте <code>__repr__</code> так, чтобы <code>eval(repr(obj))</code> воссоздавал объект. <code>__str__</code> — для пользователя. Если определён только <code>__repr__</code>, он используется и для <code>str()</code>.'),
'code_example': '''import math

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self): return f"Vector({self.x}, {self.y})"
    def __add__(self, o): return Vector(self.x+o.x, self.y+o.y)
    def __sub__(self, o): return Vector(self.x-o.x, self.y-o.y)
    def __mul__(self, s): return Vector(self.x*s, self.y*s)
    def __rmul__(self, s): return self.__mul__(s)
    def __abs__(self): return math.sqrt(self.x**2+self.y**2)
    def __eq__(self, o): return self.x==o.x and self.y==o.y
    def __lt__(self, o): return abs(self) < abs(o)
    def __iter__(self): yield self.x; yield self.y
    def dot(self, o): return self.x*o.x + self.y*o.y

v1, v2 = Vector(3, 4), Vector(1, 2)
print(f"v1 = {v1}, |v1| = {abs(v1)}")
print(f"v1 + v2 = {v1+v2}")
print(f"v1 * 3 = {v1*3}, 3 * v1 = {3*v1}")
print(f"v1 · v2 = {v1.dot(v2)}")
print(f"v1 == v2: {v1==v2}, v1 > v2: {v1>v2}")
print(f"sorted: {sorted([v1, v2, Vector(0,1)])}")
print(f"list(v1): {list(v1)}")

# Контекстный менеджер
class Timer:
    import time
    def __enter__(self):
        import time; self.start = time.perf_counter(); return self
    def __exit__(self, *args):
        import time; self.elapsed = time.perf_counter()-self.start
        print(f"Время: {self.elapsed:.4f}с")
    def __repr__(self): return f"Timer({self.elapsed:.4f}с)"

with Timer() as t:
    result = sum(x**2 for x in range(100000))
'''
},
{
'title': 'Инкапсуляция и @property',
'order': 3,
'estimated_minutes': 60,
'content': '''
<h2>Инкапсуляция в Python</h2>
<p><strong>Инкапсуляция</strong> — принцип ООП, предполагающий скрытие внутренних деталей объекта и предоставление контролируемого интерфейса доступа. В Python нет жёсткой приватности (как в Java), но есть соглашения.</p>
''' + table(
    ['Именование', 'Соглашение', 'Поведение', 'Пример'],
    [
        ['name', 'Публичный', 'Доступен всем', 'self.value'],
        ['_name', 'Защищённый', 'Не трогать снаружи (но можно)', 'self._cache'],
        ['__name', 'Приватный', 'Name mangling: _Class__name', 'self.__secret'],
    ]
) + '''
<pre><code>class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance     # приватный — извне не тронуть
        self._history = []           # защищённый

    @property
    def balance(self):
        """Геттер — читаем баланс"""
        return self.__balance

    @balance.setter
    def balance(self, value):
        """Сеттер — устанавливаем с проверкой"""
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self.__balance = value
        self._history.append(f"Установлен: {value}")

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.__balance += amount
        self._history.append(f"+{amount}")

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Недостаточно средств")
        self.__balance -= amount
        self._history.append(f"-{amount}")
</code></pre>
''' + tip('@property позволяет обращаться к методу как к атрибуту: <code>account.balance</code> — без скобок! Это главное преимущество: можно в любой момент добавить логику (валидацию, логирование) к существующему коду без изменения интерфейса.') + warn('Name mangling (__name) — это НЕ настоящая приватность. Доступ всё равно возможен через <code>obj._ClassName__name</code>. Python доверяет программисту и использует соглашения, а не жёсткие ограничения.'),
'code_example': '''class Temperature:
    """Температура с конвертацией между шкалами"""
    def __init__(self, celsius=0):
        self._celsius = celsius  # хранить в цельсиях

    @property
    def celsius(self): return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError(f"Ниже абсолютного нуля: {value}")
        self._celsius = value

    @property
    def fahrenheit(self): return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value): self.celsius = (value - 32) * 5/9

    @property
    def kelvin(self): return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value): self.celsius = value - 273.15

    def __repr__(self): return f"Temperature({self._celsius}°C)"

t = Temperature(100)
print(f"Кипение: {t.celsius}°C = {t.fahrenheit}°F = {t.kelvin}K")
t.fahrenheit = 32
print(f"Замерзание: {t.celsius}°C = {t.fahrenheit}°F")
t.kelvin = 0
print(f"Абсолютный ноль: {t.celsius}°C")

# Демонстрация name mangling
class Secret:
    def __init__(self):
        self.public = "публичный"
        self._protected = "защищённый"
        self.__private = "приватный"

s = Secret()
print(s.public)        # OK
print(s._protected)    # OK (но не рекомендуется)
# print(s.__private)   # AttributeError!
print(s._Secret__private)  # name mangling — всё же доступен
'''
},
{
'title': 'Абстрактные классы и Protocol',
'order': 4,
'estimated_minutes': 60,
'content': '''
<h2>Абстрактные классы (ABC)</h2>
<p><strong>Абстрактный класс</strong> — класс, который нельзя инстанцировать напрямую. Он определяет <em>интерфейс</em> — набор методов, которые обязаны реализовать все дочерние классы. Используется модуль <code>abc</code>.</p>
<pre><code>from abc import ABC, abstractmethod

class Shape(ABC):
    """Абстрактный класс фигуры"""

    @abstractmethod
    def area(self) -> float:
        """Площадь фигуры"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Периметр фигуры"""
        pass

    def describe(self):
        """Конкретный метод — не abstract"""
        return f"{self.__class__.__name__}: площадь={self.area():.2f}, периметр={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self): return 3.14159 * self.radius ** 2
    def perimeter(self): return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self): return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

# shape = Shape()  # TypeError: нельзя создать ABC!
circle = Circle(5)
print(circle.describe())
</code></pre>
''' + table(
    ['', 'Абстрактный класс (ABC)', 'typing.Protocol'],
    [
        ['Механизм', 'Явное наследование', 'Структурная типизация'],
        ['Проверка', 'Во время создания объекта', 'Статически (mypy) или явно'],
        ['Наследование', 'Обязательно (is-a)', 'Не требуется (duck typing)'],
        ['Общий код', 'Да, через конкретные методы', 'Нет'],
        ['Применение', 'Иерархии с общим поведением', 'Независимые классы с общим интерфейсом'],
    ]
) + tip('Используйте ABC, когда хотите: (1) запретить создание базового класса, (2) поделиться реализацией части методов, (3) документировать обязательный интерфейс в большой иерархии. Protocol подходит для независимых классов (duck typing).'),
'code_example': '''from abc import ABC, abstractmethod
import math
from typing import Protocol, runtime_checkable

# Абстрактный класс Shape
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: pass
    @abstractmethod
    def perimeter(self) -> float: pass
    def describe(self):
        return f"{type(self).__name__}: S={self.area():.2f}, P={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r**2
    def perimeter(self): return 2 * math.pi * self.r

class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
    def perimeter(self): return 2*(self.w+self.h)

class Triangle(Shape):
    def __init__(self, a, b, c): self.a, self.b, self.c = a, b, c
    def area(self):
        s = (self.a+self.b+self.c)/2
        return math.sqrt(s*(s-self.a)*(s-self.b)*(s-self.c))
    def perimeter(self): return self.a+self.b+self.c

shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
for s in shapes: print(s.describe())

total_area = sum(s.area() for s in shapes)
print(f"Суммарная площадь: {total_area:.2f}")

# Protocol (структурная типизация)
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Sprite:
    def draw(self): return "Рисую спрайт"

class Button:
    def draw(self): return "Рисую кнопку"

widgets = [Sprite(), Button()]
for w in widgets:
    if isinstance(w, Drawable):
        print(w.draw())
'''
},
]
},

# ═══════════════════════════════════════════════════════════════════
# МОДУЛЬ 30 — ЧИСЛОВЫЕ АЛГОРИТМЫ
# ═══════════════════════════════════════════════════════════════════
{
'title': 'Числовые алгоритмы',
'icon': 'fas fa-calculator',
'order': 30,
'description': 'НОД, НОК, быстрое возведение в степень, простые числа, решето Эратосфена, системы счисления.',
'lessons': [
{
'title': 'НОД, НОК и быстрое возведение в степень',
'order': 1,
'estimated_minutes': 65,
'content': '''
<h2>Наибольший общий делитель (алгоритм Евклида)</h2>
<p>НОД(a, b) — наибольшее число, на которое делятся и a, и b. Алгоритм Евклида (300 г. до н.э.) использует свойство: <strong>НОД(a, b) = НОД(b, a mod b)</strong>. Базовый случай: НОД(a, 0) = a.</p>
''' + diagram(
    '<text x="300" y="20" text-anchor="middle" font-size="13" fill="#374151" font-weight="bold">НОД(48, 18) — шаги алгоритма Евклида</text>'
    '<rect x="50" y="40" width="500" height="40" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>'
    '<text x="300" y="66" text-anchor="middle" font-size="12" fill="#1e40af">НОД(48, 18) → 48 = 2×18 + 12 → НОД(18, 12)</text>'
    '<rect x="80" y="90" width="440" height="40" rx="6" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>'
    '<text x="300" y="116" text-anchor="middle" font-size="12" fill="#5b21b6">НОД(18, 12) → 18 = 1×12 + 6 → НОД(12, 6)</text>'
    '<rect x="110" y="140" width="380" height="40" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>'
    '<text x="300" y="166" text-anchor="middle" font-size="12" fill="#166534">НОД(12, 6) → 12 = 2×6 + 0 → НОД(6, 0) = 6 ✓</text>'
    '<text x="300" y="210" text-anchor="middle" font-size="11" fill="#64748b">НОД(48, 18) = 6  |  Всего 3 шага (O(log min(a,b)))</text>',
    w=600, h=230, caption='Алгоритм Евклида: каждый шаг уменьшает числа примерно вдвое'
) + '''
<pre><code>def gcd(a, b):
    """Рекурсивный алгоритм Евклида"""
    return a if b == 0 else gcd(b, a % b)

def gcd_iter(a, b):
    """Итеративный вариант"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """НОК через НОД: НОК(a,b) = a*b / НОД(a,b)"""
    return abs(a * b) // gcd(a, b)

# В стандартной библиотеке:
import math
print(math.gcd(48, 18))   # 6
print(math.lcm(4, 6))     # 12
</code></pre>
<h3>Быстрое возведение в степень</h3>
<p>Наивный алгоритм: n умножений для aⁿ. Быстрый: используем <strong>бинарное возведение</strong> — O(log n) умножений.</p>
<p>Идея: <code>aⁿ = (a^(n/2))²</code> если n чётное; <code>aⁿ = a × a^(n-1)</code> если нечётное.</p>
<pre><code>def fast_pow(base, exp, mod=None):
    """Быстрое возведение в степень за O(log exp)"""
    result = 1
    base = base % mod if mod else base
    while exp > 0:
        if exp % 2 == 1:        # нечётный показатель
            result = (result * base) % mod if mod else result * base
        base = (base * base) % mod if mod else base * base
        exp //= 2
    return result

# Python: встроенный pow(base, exp, mod) делает то же самое!
print(pow(2, 100))             # встроенный, оптимизированный
print(pow(2, 100, 10**9+7))   # с модулем (для конкурсных задач)
</code></pre>
''' + table(
    ['Алгоритм', 'Сложность', 'Пример для a¹⁰⁰'],
    [
        ['Наивный (цикл a*a*a...)', 'O(n)', '100 умножений'],
        ['Быстрое возведение', 'O(log n)', '7 умножений (log₂100 ≈ 7)'],
        ['Python pow()', 'O(log n)', 'Встроенный, C-реализация'],
    ]
) + tip('В криптографии (RSA) вычисляют a^e mod n для чисел с тысячами знаков. Без быстрого возведения это было бы невозможно. Python встроенный pow(a, e, n) использует именно этот алгоритм.'),
'code_example': '''import math, time

def gcd(a, b):
    while b: a, b = b, a%b
    return a

def lcm(a, b): return abs(a*b)//gcd(a,b)

def fast_pow(base, exp, mod=None):
    result = 1
    if mod: base %= mod
    while exp > 0:
        if exp & 1:
            result = result*base%mod if mod else result*base
        base = base*base%mod if mod else base*base
        exp >>= 1
    return result

# НОД нескольких чисел
from functools import reduce
def gcd_multiple(*args): return reduce(gcd, args)
def lcm_multiple(*args): return reduce(lcm, args)

nums = [12, 18, 24, 36]
print(f"НОД{tuple(nums)} = {gcd_multiple(*nums)}")
print(f"НОК{tuple(nums)} = {lcm_multiple(*nums)}")

# Сравнение наивного и быстрого возведения
def naive_pow(base, exp):
    result = 1
    for _ in range(exp): result *= base
    return result

n = 10000
t1 = time.perf_counter(); naive_pow(2, n); slow = time.perf_counter()-t1
t1 = time.perf_counter(); fast_pow(2, n);  fast = time.perf_counter()-t1
print(f"Наивный: {slow:.4f}с, быстрый: {fast:.6f}с, ratio: {slow/fast:.0f}x")

# RSA-подобное: pow с большими числами
p, g, e = 10**9+7, 7, 12345678
print(f"7^12345678 mod (10⁹+7) = {pow(g, e, p)}")
'''
},
{
'title': 'Простые числа и решето Эратосфена',
'order': 2,
'estimated_minutes': 65,
'content': '''
<h2>Простые числа</h2>
<p><strong>Простое число</strong> — натуральное число > 1, делящееся только на 1 и на себя. Простые числа — строительные блоки всех натуральных чисел (Основная теорема арифметики): каждое число единственным образом разкладывается в произведение простых.</p>
<h3>Проверка числа на простоту</h3>
<pre><code>def is_prime_naive(n):
    """O(n) — перебор всех делителей"""
    if n < 2: return False
    for i in range(2, n):
        if n % i == 0: return False
    return True

def is_prime(n):
    """O(√n) — делители выше √n идут парами с делителями ниже √n"""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):  # только нечётные
        if n % i == 0: return False
    return True
</code></pre>
<h3>Решето Эратосфена</h3>
<p>Для нахождения ВСЕХ простых до N — используем <strong>решето</strong>: начинаем с 2, помечаем все его кратные как составные, переходим к следующему непомеченному числу.</p>
''' + diagram(
    '<text x="300" y="20" text-anchor="middle" font-size="12" fill="#374151" font-weight="bold">Решето Эратосфена: простые до 20</text>'
    '<rect x="20" y="40" width="560" height="60" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>'
    '<text x="50" y="65" text-anchor="middle" font-size="12" fill="#94a3b8" font-style="italic">1</text>'
    '<rect x="70" y="45" width="35" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/><text x="87" y="65" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">2</text>'
    '<rect x="110" y="45" width="35" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/><text x="127" y="65" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">3</text>'
    '<rect x="150" y="45" width="35" height="30" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/><text x="167" y="65" text-anchor="middle" font-size="13" fill="#dc2626" text-decoration="line-through">4</text>'
    '<rect x="190" y="45" width="35" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/><text x="207" y="65" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">5</text>'
    '<rect x="230" y="45" width="35" height="30" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/><text x="247" y="65" text-anchor="middle" font-size="13" fill="#dc2626" text-decoration="line-through">6</text>'
    '<rect x="270" y="45" width="35" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/><text x="287" y="65" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">7</text>'
    '<rect x="310" y="45" width="35" height="30" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/><text x="327" y="65" text-anchor="middle" font-size="13" fill="#dc2626" text-decoration="line-through">8</text>'
    '<rect x="350" y="45" width="35" height="30" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/><text x="367" y="65" text-anchor="middle" font-size="13" fill="#dc2626" text-decoration="line-through">9</text>'
    '<rect x="390" y="45" width="35" height="30" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/><text x="407" y="65" text-anchor="middle" font-size="13" fill="#dc2626" text-decoration="line-through">10</text>'
    '<rect x="430" y="45" width="35" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/><text x="447" y="65" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">11</text>'
    '<rect x="470" y="45" width="35" height="30" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1"/><text x="487" y="65" text-anchor="middle" font-size="13" fill="#dc2626" text-decoration="line-through">12</text>'
    '<rect x="510" y="45" width="35" height="30" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/><text x="527" y="65" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">13</text>'
    '<text x="300" y="125" text-anchor="middle" font-size="11" fill="#374151">Простые до 20: 2, 3, 5, 7, 11, 13, 17, 19</text>',
    w=580, h=140, caption='Решето Эратосфена: зелёные — простые, красные — составные'
) + '''
<pre><code>def sieve_of_eratosthenes(n):
    """Все простые числа от 2 до n включительно"""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Помечаем все кратные i (начиная с i²)
            for j in range(i*i, n+1, i):
                is_prime[j] = False

    return [i for i in range(2, n+1) if is_prime[i]]
</code></pre>
''' + tip('Решето Эратосфена имеет сложность O(n log log n) — почти линейное. Для n=10⁶ находит все простые за ~0.1 секунды. is_prime[i²] — оптимизация: все составные числа меньше i² уже помечены на предыдущих итерациях.'),
'code_example': '''import time

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def sieve(n):
    primes = [True]*(n+1)
    primes[0] = primes[1] = False
    for i in range(2, int(n**0.5)+1):
        if primes[i]:
            for j in range(i*i, n+1, i):
                primes[j] = False
    return [i for i in range(2, n+1) if primes[i]]

# Нахождение простых до миллиона
t = time.perf_counter()
primes = sieve(1_000_000)
elapsed = time.perf_counter() - t
print(f"Простых до 10⁶: {len(primes)}, за {elapsed:.3f}с")
print(f"Последние 5: {primes[-5:]}")

# Факторизация числа
def factorize(n):
    factors = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return factors

for n in [360, 1024, 997, 100]:
    f = factorize(n)
    print(f"{n} = {' × '.join(f'{p}^{e}' if e>1 else str(p) for p,e in f.items())}")

# Числа-близнецы (twin primes: p и p+2 — оба простые)
twins = [(p, p+2) for p in primes if p+2 in set(primes)][:10]
print(f"Первые 10 пар-близнецов: {twins}")
'''
},
{
'title': 'Системы счисления и битовые операции',
'order': 3,
'estimated_minutes': 60,
'content': '''
<h2>Системы счисления</h2>
<p>Компьютеры хранят данные в двоичной системе (основание 2). Программисты регулярно работают с двоичными (0b), восьмеричными (0o) и шестнадцатеричными (0x) числами.</p>
''' + table(
    ['Число', 'Десятичная (10)', 'Двоичная (2)', 'Восьмеричная (8)', '16-ричная (16)'],
    [
        ['0', '0', '0000', '0', '0'],
        ['5', '5', '0101', '5', '5'],
        ['10', '10', '1010', '12', 'A'],
        ['15', '15', '1111', '17', 'F'],
        ['16', '16', '0001 0000', '20', '10'],
        ['255', '255', '1111 1111', '377', 'FF'],
        ['256', '256', '0001 0000 0000', '400', '100'],
    ]
) + '''
<pre><code># Python: литералы разных систем
binary = 0b1010      # 10
octal  = 0o17        # 15
hexad  = 0xFF        # 255

# Перевод числа в строку
n = 42
print(bin(n))    # '0b101010'
print(oct(n))    # '0o52'
print(hex(n))    # '0x2a'
print(format(n, 'b'))   # '101010' (без префикса)
print(format(n, '08b')) # '00101010' (8 бит с нулями)
print(format(n, 'X'))   # '2A' (заглавные hex)

# Парсинг строк
print(int('101010', 2))  # 42 из двоичной
print(int('2a', 16))     # 42 из hex
print(int('52', 8))      # 42 из восьмеричной
</code></pre>
<h2>Битовые операции</h2>
''' + table(
    ['Операция', 'Символ', 'Описание', 'Пример (5=101, 3=011)'],
    [
        ['AND', '&', 'Бит 1 если оба 1', '5 & 3 = 001 = 1'],
        ['OR', '|', 'Бит 1 если хотя бы один 1', '5 | 3 = 111 = 7'],
        ['XOR', '^', 'Бит 1 если биты разные', '5 ^ 3 = 110 = 6'],
        ['NOT', '~', 'Инверсия всех битов', '~5 = -6 (дополн. код)'],
        ['Сдвиг влево', '<<', 'Умножение на 2ⁿ', '5 << 1 = 1010 = 10'],
        ['Сдвиг вправо', '>>', 'Деление на 2ⁿ', '5 >> 1 = 010 = 2'],
    ]
) + tip('Битовые операции используются для: флагов и масок (проверка и установка отдельных битов), оптимизации (n>>1 быстрее n//2), хэш-функций, сжатия данных, работы с пикселями (RGB). Проверка чётности: if n&1: — нечётное.'),
'code_example': '''# Конвертация систем счисления
def to_base(n, base):
    """Перевод n в систему счисления base (2-16)"""
    if n == 0: return "0"
    digits = "0123456789ABCDEF"
    result = ""
    negative = n < 0
    n = abs(n)
    while n > 0:
        result = digits[n % base] + result
        n //= base
    return ("-" if negative else "") + result

for n in [0, 10, 42, 255]:
    print(f"{n:4d} → bin:{to_base(n,2):>10} oct:{to_base(n,8):>5} hex:{to_base(n,16):>4}")

# Битовые трюки
def is_even(n): return not (n & 1)
def is_power_of_2(n): return n > 0 and (n & (n-1)) == 0
def set_bit(n, pos): return n | (1 << pos)
def clear_bit(n, pos): return n & ~(1 << pos)
def toggle_bit(n, pos): return n ^ (1 << pos)
def check_bit(n, pos): return bool(n & (1 << pos))

n = 0b10110  # 22
print(f"n = {n} = {format(n,'08b')}")
print(f"Установить бит 0: {format(set_bit(n, 0),'08b')} = {set_bit(n, 0)}")
print(f"Очистить бит 2:   {format(clear_bit(n, 2),'08b')} = {clear_bit(n, 2)}")
print(f"Инвертировать бит 1: {format(toggle_bit(n, 1),'08b')} = {toggle_bit(n, 1)}")

# Степени двойки
print("Степени двойки:", [2**i for i in range(10)])
print("Проверка:", [is_power_of_2(x) for x in [1,2,3,4,5,8,10,16]])
'''
},
]
},

]  # end MODULES


class Command(BaseCommand):
    help = 'Создать модули теории 21–30 (ОАИП расширенный)'

    def handle(self, *args, **options):
        try:
            subj = Subject.objects.get(slug='python')
        except Subject.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Subject "python" не найден. Запустите: python manage.py seed_subjects'
            ))
            return

        for mod_data in MODULES:
            lessons_data = mod_data.pop('lessons')
            mod_data['subject'] = subj
            mod, created = TheoryModule.objects.update_or_create(
                order=mod_data['order'], defaults=mod_data
            )
            action = 'Создан' if created else 'Обновлён'
            self.stdout.write(f'{action} модуль [{mod.order}]: {mod.title}')

            for les_data in lessons_data:
                les_data['module'] = mod
                _, lc = TheoryLesson.objects.update_or_create(
                    module=mod, order=les_data['order'], defaults=les_data
                )
                lbl = '+' if lc else '~'
                self.stdout.write(f'  {lbl} {les_data["title"]}')

        self.stdout.write(self.style.SUCCESS('Готово! Добавлены модули 21–30.'))
