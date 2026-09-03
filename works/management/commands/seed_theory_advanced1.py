"""
Модули 31–40: продвинутые темы Python (часть 1).
Запуск: python manage.py seed_theory_advanced1
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


def tip(text):
    return f'<div class="tip">💡 {text}</div>'

def warn(text):
    return f'<div class="warning">⚠️ {text}</div>'

def info(text):
    return f'<div class="tip" style="background:#e0f2fe;border-left-color:#0284c7">ℹ️ {text}</div>'

def table(headers, rows, caption=''):
    hdr = ''.join(f'<th>{h}</th>' for h in headers)
    body = ''
    for row in rows:
        body += '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
    cap = f'<caption style="font-weight:600;margin-bottom:.5rem">{caption}</caption>' if caption else ''
    return f'<div class="theory-table"><table>{cap}<thead><tr>{hdr}</tr></thead><tbody>{body}</tbody></table></div>'

def diagram(svg_inner, w=600, h=260, caption=''):
    cap = f'<p style="text-align:center;font-size:.82rem;color:#6b7280;margin-top:.4rem">{caption}</p>' if caption else ''
    return f'<div style="overflow-x:auto;margin:1rem 0"><svg viewBox="0 0 {w} {h}" style="max-width:100%;display:block;margin:0 auto">{svg_inner}</svg>{cap}</div>'


MODULES = [

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 31 — itertools и functools
# ════════════════════════════════════════════════════════════════
{
  'title': 'itertools и functools',
  'description': 'Стандартные библиотеки для работы с итераторами и функциями высшего порядка.',
  'icon': 'fas fa-infinity',
  'color': '#7c3aed',
  'order': 31,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'itertools: цепочки, комбинации, группировка',
      'order': 1,
      'estimated_minutes': 55,
      'content': '''<h2>Модуль itertools</h2>
<p><code>itertools</code> — стандартная библиотека Python с готовыми ленивыми итераторами.
Все функции возвращают <strong>итераторы</strong> (не списки), что экономит память.</p>

''' + table(
  ['Функция','Что делает','Пример'],
  [
    ['chain(*iters)','Склеивает несколько итерируемых','chain([1,2],[3,4]) → 1 2 3 4'],
    ['islice(it,n)','Срез итератора','islice(range(100),5) → 0..4'],
    ['count(start,step)','Бесконечный счётчик','count(10,2) → 10,12,14,…'],
    ['cycle(it)','Бесконечный цикл по элементам','cycle("AB") → A B A B…'],
    ['repeat(x,n)','Повторяет x ровно n раз','repeat(0,3) → 0 0 0'],
    ['product(*iters)','Декартово произведение','product("AB","12") → A1 A2 B1 B2'],
    ['permutations(it,r)','Перестановки','permutations([1,2,3],2) → 12 пар'],
    ['combinations(it,r)','Сочетания','combinations([1,2,3],2) → 3 пары'],
    ['groupby(it,key)','Группировка по ключу','groupby(sorted, key)'],
    ['takewhile(pred,it)','Берёт пока pred=True','takewhile(x<5, count())'],
    ['dropwhile(pred,it)','Пропускает пока pred=True','dropwhile(x<5, count())'],
  ],
  'Основные функции itertools'
) + '''
<h3>Практические примеры</h3>
<pre><code>import itertools

# chain — обход нескольких списков без копирования
students = list(itertools.chain(group1, group2, group3))

# islice — первые 10 простых чисел из бесконечного генератора
def primes():
    n = 2
    while True:
        if all(n % i != 0 for i in range(2, n)): yield n
        n += 1

first10 = list(itertools.islice(primes(), 10))

# product — все комбинации параметров
params = list(itertools.product([1,2,3], ['a','b']))
# → [(1,'a'),(1,'b'),(2,'a'),(2,'b'),(3,'a'),(3,'b')]

# groupby — нужна ПРЕДВАРИТЕЛЬНАЯ сортировка!
data = [('Alice','A'),('Bob','B'),('Charlie','A')]
data.sort(key=lambda x: x[1])
for key, group in itertools.groupby(data, key=lambda x: x[1]):
    print(key, list(group))
</code></pre>

''' + diagram('''
<rect x="10" y="20" width="120" height="40" rx="6" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>
<text x="70" y="44" text-anchor="middle" font-size="13" fill="#5b21b6">Итерируемые 1..N</text>
<text x="185" y="44" text-anchor="middle" font-size="22" fill="#7c3aed">→</text>
<rect x="220" y="20" width="120" height="40" rx="6" fill="#7c3aed" opacity=".25" stroke="#7c3aed"/>
<text x="280" y="44" text-anchor="middle" font-size="13" fill="#5b21b6">chain / product</text>
<text x="395" y="44" text-anchor="middle" font-size="22" fill="#7c3aed">→</text>
<rect x="430" y="20" width="140" height="40" rx="6" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>
<text x="500" y="44" text-anchor="middle" font-size="13" fill="#5b21b6">Ленивый итератор</text>
<text x="70" y="110" text-anchor="middle" font-size="12" fill="#374151">Не копирует данные</text>
<text x="280" y="110" text-anchor="middle" font-size="12" fill="#374151">Минимум памяти</text>
<text x="500" y="110" text-anchor="middle" font-size="12" fill="#374151">list() при нужде</text>
''', caption='Принцип работы itertools — ленивые итераторы') + tip('Функции itertools не выполняют вычисления сразу. Оберни в list() или for-цикл, чтобы получить результат.'),
      'code_example': '''import itertools

# 1. chain — соединить списки
a = [1, 2, 3]
b = [4, 5, 6]
print("chain:", list(itertools.chain(a, b)))

# 2. product — все пары (x, y)
print("product:", list(itertools.product([1,2], ['a','b'])))

# 3. combinations — сочетания по 2
print("C(3,2):", list(itertools.combinations([1,2,3], 2)))

# 4. permutations — перестановки
print("P(3,2):", list(itertools.permutations([1,2,3], 2)))

# 5. groupby — группировка (сначала сортировка!)
words = ['яблоко', 'апельсин', 'авокадо', 'банан', 'арбуз']
words.sort()
for letter, group in itertools.groupby(words, key=lambda w: w[0]):
    print(f"{letter}: {list(group)}")
'''
    },
    {
      'title': 'functools: lru_cache, partial, reduce, wraps',
      'order': 2,
      'estimated_minutes': 50,
      'content': '''<h2>Модуль functools</h2>
<p>Инструменты для работы с функциями: кэширование, частичное применение, свёртка.</p>

<h3>lru_cache — кэширование результатов</h3>
<pre><code>from functools import lru_cache

@lru_cache(maxsize=None)   # None = кэш без ограничений
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

print(fib(100))       # мгновенно!
print(fib.cache_info())  # CacheInfo(hits=98, misses=101, ...)
</code></pre>
''' + tip('lru_cache хранит результаты по аргументам. Аргументы должны быть хэшируемыми (числа, строки, кортежи — да; списки — нет).') + '''

<h3>partial — зафиксировать часть аргументов</h3>
<pre><code>from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)

print(square(5))  # 25
print(cube(3))    # 27

# Полезно для колбэков с параметрами
buttons = [partial(print, f"Button {i} clicked") for i in range(3)]
buttons[1]()  # Button 1 clicked
</code></pre>

<h3>reduce — свёртка (агрегация)</h3>
<pre><code>from functools import reduce
import operator

nums = [1, 2, 3, 4, 5]
product = reduce(operator.mul, nums)      # 120
total   = reduce(operator.add, nums, 0)   # 15 (0 — нач. значение)

# Найти максимум вручную через reduce
max_val = reduce(lambda a, b: a if a > b else b, nums)
</code></pre>

<h3>wraps — сохранение метаданных декоратора</h3>
<pre><code>from functools import wraps

def my_decorator(func):
    @wraps(func)           # без этого __name__ = 'wrapper'
    def wrapper(*args, **kwargs):
        print("До вызова")
        result = func(*args, **kwargs)
        print("После вызова")
        return result
    return wrapper

@my_decorator
def hello(name):
    """Приветствует пользователя."""
    print(f"Привет, {name}!")

print(hello.__name__)  # hello (а не wrapper!)
print(hello.__doc__)   # Приветствует пользователя.
</code></pre>
''' + table(
  ['Функция','Назначение','Когда использовать'],
  [
    ['lru_cache','Кэшировать вызовы функции','Рекурсия, дорогие вычисления'],
    ['cache','lru_cache без ограничений (3.9+)','Простое кэширование'],
    ['partial','Зафиксировать аргументы','Колбэки, pipeline'],
    ['reduce','Свернуть список в одно значение','Агрегация без циклов'],
    ['wraps','Сохранить __name__/__doc__','Внутри декораторов'],
    ['total_ordering','Дополнить операторы сравнения','Классы с __lt__'],
  ],
  'functools: ключевые инструменты'
),
      'code_example': '''from functools import lru_cache, partial, reduce

# lru_cache: фибоначчи без лишних вычислений
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
print("Кэш:", fib.cache_info())

# partial: степени
from functools import partial
power = lambda base, exp: base ** exp
square = partial(power, exp=2)
cube   = partial(power, exp=3)
print(list(map(square, [1, 2, 3, 4, 5])))
print(list(map(cube,   [1, 2, 3, 4, 5])))

# reduce: произведение списка
nums = [1, 2, 3, 4, 5]
product = reduce(lambda a, b: a * b, nums)
print("Произведение:", product)
'''
    },
    {
      'title': 'Цепочки обработки данных: pipe-style',
      'order': 3,
      'estimated_minutes': 45,
      'content': '''<h2>Функциональный стиль обработки данных</h2>
<p>Сочетание <code>map</code>, <code>filter</code>, <code>itertools</code> и <code>functools</code>
позволяет строить читаемые цепочки обработки данных без промежуточных переменных.</p>

<h3>Пример: обработка CSV-подобных данных</h3>
<pre><code>from itertools import islice, groupby
from functools import reduce

raw = [
    {'name': 'Alice', 'dept': 'IT',  'salary': 80000},
    {'name': 'Bob',   'dept': 'HR',  'salary': 60000},
    {'name': 'Carol', 'dept': 'IT',  'salary': 95000},
    {'name': 'Dave',  'dept': 'HR',  'salary': 70000},
    {'name': 'Eve',   'dept': 'IT',  'salary': 75000},
]

# Средняя зарплата по отделам
sorted_data = sorted(raw, key=lambda x: x['dept'])
for dept, group in groupby(sorted_data, key=lambda x: x['dept']):
    salaries = [e['salary'] for e in group]
    avg = reduce(lambda a, b: a + b, salaries) / len(salaries)
    print(f"{dept}: {avg:,.0f}")
</code></pre>

''' + tip('Используй sorted() перед groupby — groupby группирует только СОСЕДНИЕ одинаковые ключи!') + '''

<h3>Генераторные выражения в цепочках</h3>
<pre><code># Найти топ-3 слова по частоте в тексте
from itertools import islice
from collections import Counter

text = "python python java python java c++ java python"
words = text.split()
top3 = islice(Counter(words).most_common(), 3)
for word, count in top3:
    print(f"{word}: {count}")
</code></pre>

<h3>Ленивая цепочка без промежуточных списков</h3>
<pre><code>import itertools

# 10000 файлов — обрабатываем лениво, без загрузки в память
def read_lines(files):
    return itertools.chain.from_iterable(open(f) for f in files)

def filter_errors(lines):
    return (line for line in lines if 'ERROR' in line)

def take(n, iterable):
    return itertools.islice(iterable, n)

# Пайплайн: читать → фильтровать → взять первые 5
files = ['log1.txt', 'log2.txt']
# pipeline = take(5, filter_errors(read_lines(files)))
# for line in pipeline: print(line)
</code></pre>
''',
      'code_example': '''from itertools import groupby, islice
from functools import reduce
from collections import Counter

# Задача: аналитика продаж
sales = [
    ('Янв', 'Книги', 1500),
    ('Янв', 'Игры',  3200),
    ('Фев', 'Книги', 1800),
    ('Фев', 'Игры',  2900),
    ('Мар', 'Книги', 2100),
    ('Мар', 'Игры',  3800),
]

# Итого по категориям
by_cat = sorted(sales, key=lambda x: x[1])
for cat, group in groupby(by_cat, key=lambda x: x[1]):
    total = reduce(lambda a, b: a + b[2], group, 0)
    print(f"{cat}: {total:,} руб.")

# Топ-2 месяца по общей выручке
monthly = Counter()
for month, _, amount in sales:
    monthly[month] += amount
print("Топ месяцы:", list(islice(monthly.most_common(), 2)))
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 32 — Параллельность: threading и multiprocessing
# ════════════════════════════════════════════════════════════════
{
  'title': 'threading и multiprocessing',
  'description': 'Параллельное выполнение задач в Python: потоки, процессы и GIL.',
  'icon': 'fas fa-project-diagram',
  'color': '#dc2626',
  'order': 32,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'GIL и модуль threading',
      'order': 1,
      'estimated_minutes': 60,
      'content': '''<h2>GIL — Global Interpreter Lock</h2>
<p><strong>GIL</strong> (Глобальная блокировка интерпретатора) — механизм CPython,
который позволяет <strong>только одному потоку</strong> выполнять Python-байткод в каждый момент времени.</p>

''' + table(
  ['Задача','GIL мешает?','Инструмент'],
  [
    ['I/O: сеть, файлы, БД','НЕТ — поток освобождает GIL во время ожидания','threading'],
    ['CPU: математика, обработка','ДА — GIL не даёт реального параллелизма','multiprocessing'],
    ['Смешанные','Зависит от соотношения','concurrent.futures'],
  ],
  'GIL и выбор инструмента'
) + '''

<h3>threading.Thread — базовое использование</h3>
<pre><code>import threading
import time

def download(url, delay):
    print(f"Начало загрузки {url}")
    time.sleep(delay)          # I/O — GIL освобождается
    print(f"Готово: {url}")

# Последовательно: 3 + 2 + 1 = 6 сек
# Параллельно: max(3,2,1) = 3 сек

threads = [
    threading.Thread(target=download, args=(f"url{i}", 3-i))
    for i in range(3)
]
for t in threads: t.start()
for t in threads: t.join()    # ждём завершения всех
print("Все загрузки завершены")
</code></pre>

<h3>Lock — защита общих данных</h3>
<pre><code>import threading

counter = 0
lock = threading.Lock()

def increment(n):
    global counter
    for _ in range(n):
        with lock:      # только один поток в этом блоке
            counter += 1

threads = [threading.Thread(target=increment, args=(10000,)) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)  # всегда 50000 (без lock — нет гарантии)
</code></pre>
''' + warn('Без Lock при одновременном доступе к counter получим race condition — некорректный результат.') + '''

<h3>ThreadPoolExecutor — пул потоков</h3>
<pre><code>from concurrent.futures import ThreadPoolExecutor

def fetch(url):
    import time; time.sleep(0.5)
    return f"data from {url}"

urls = [f"https://api.example.com/{i}" for i in range(10)]

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch, urls))

print(results)
</code></pre>
''',
      'code_example': '''import threading
import time

# Демонстрация: параллельная загрузка vs последовательная
results = []
lock = threading.Lock()

def simulate_download(url, delay):
    time.sleep(delay)
    with lock:
        results.append(f"{url}: {delay}s")

urls = [("site1.com", 0.3), ("site2.com", 0.2), ("site3.com", 0.1)]

# Последовательно
start = time.time()
for url, delay in urls:
    simulate_download(url, delay)
print(f"Последовательно: {time.time()-start:.2f}s")

results.clear()

# Параллельно
start = time.time()
threads = [threading.Thread(target=simulate_download, args=(u, d)) for u, d in urls]
for t in threads: t.start()
for t in threads: t.join()
print(f"Параллельно: {time.time()-start:.2f}s")
print("Результаты:", results)
'''
    },
    {
      'title': 'multiprocessing: обход GIL для CPU-задач',
      'order': 2,
      'estimated_minutes': 55,
      'content': '''<h2>multiprocessing</h2>
<p>Модуль <code>multiprocessing</code> запускает <strong>отдельные процессы</strong>
(каждый со своим GIL), что даёт реальный параллелизм на CPU-bound задачах.</p>

<h3>Process — базовый запуск</h3>
<pre><code>from multiprocessing import Process

def heavy_task(n):
    """Тяжёлая CPU-работа."""
    result = sum(i*i for i in range(n))
    print(f"Сумма квадратов до {n}: {result}")

if __name__ == '__main__':   # ОБЯЗАТЕЛЬНО для Windows!
    processes = [
        Process(target=heavy_task, args=(10**7,))
        for _ in range(4)
    ]
    for p in processes: p.start()
    for p in processes: p.join()
</code></pre>

''' + warn('На Windows multiprocessing требует защиты точки входа: if __name__ == "__main__":') + '''

<h3>Pool.map — параллельный map</h3>
<pre><code>from multiprocessing import Pool

def square(x):
    return x * x

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        result = pool.map(square, range(100))
    print(result[:10])
</code></pre>

<h3>Queue — передача данных между процессами</h3>
<pre><code>from multiprocessing import Process, Queue

def producer(q):
    for i in range(5):
        q.put(i)
    q.put(None)   # сигнал завершения

def consumer(q):
    while True:
        item = q.get()
        if item is None: break
        print(f"Получено: {item}")

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    p1.start(); p2.start()
    p1.join();  p2.join()
</code></pre>
''' + table(
  ['Инструмент','Тип параллелизма','GIL','Подходит для'],
  [
    ['threading.Thread','Потоки','Один на всех','I/O-bound: сеть, файлы'],
    ['multiprocessing.Process','Процессы','У каждого свой','CPU-bound: матрица, шифрование'],
    ['concurrent.futures.ThreadPoolExecutor','Пул потоков','Один','I/O пул'],
    ['concurrent.futures.ProcessPoolExecutor','Пул процессов','Свой у каждого','CPU пул'],
  ],
  'Сравнение инструментов параллелизма'
),
      'code_example': '''# Сравнение: однопоточный vs multiprocessing

def count_primes(limit):
    """Подсчёт простых чисел — CPU-задача."""
    count = 0
    for n in range(2, limit):
        if all(n % i != 0 for i in range(2, int(n**0.5)+1)):
            count += 1
    return count

import time

# Однопоточно
start = time.time()
results = [count_primes(5000) for _ in range(4)]
print(f"Однопоточно: {time.time()-start:.2f}s, найдено: {results[0]}")

# С multiprocessing
# from multiprocessing import Pool
# if __name__ == "__main__":
#     start = time.time()
#     with Pool(4) as pool:
#         results = pool.map(count_primes, [5000]*4)
#     print(f"Параллельно: {time.time()-start:.2f}s")
'''
    },
    {
      'title': 'asyncio: асинхронное программирование',
      'order': 3,
      'estimated_minutes': 65,
      'content': '''<h2>asyncio — кооперативная многозадачность</h2>
<p><code>asyncio</code> — не потоки и не процессы. Это <strong>один поток</strong>,
который переключается между задачами в момент ожидания I/O (await).</p>

''' + diagram('''
<rect x="10" y="20" width="580" height="60" rx="8" fill="#f0fdf4" stroke="#16a34a"/>
<text x="300" y="45" text-anchor="middle" font-size="14" font-weight="600" fill="#15803d">Event Loop (один поток)</text>
<text x="300" y="65" text-anchor="middle" font-size="12" fill="#166534">Переключается на await; никогда не блокируется</text>
<rect x="20" y="110" width="120" height="45" rx="6" fill="#dcfce7" stroke="#16a34a"/>
<text x="80" y="130" text-anchor="middle" font-size="12" fill="#15803d">task1</text>
<text x="80" y="147" text-anchor="middle" font-size="11" fill="#166534">await sleep(1)</text>
<rect x="160" y="110" width="120" height="45" rx="6" fill="#dcfce7" stroke="#16a34a"/>
<text x="220" y="130" text-anchor="middle" font-size="12" fill="#15803d">task2</text>
<text x="220" y="147" text-anchor="middle" font-size="11" fill="#166534">await fetch(url)</text>
<rect x="300" y="110" width="120" height="45" rx="6" fill="#dcfce7" stroke="#16a34a"/>
<text x="360" y="130" text-anchor="middle" font-size="12" fill="#15803d">task3</text>
<text x="360" y="147" text-anchor="middle" font-size="11" fill="#166534">await read_db()</text>
<path d="M80,155 Q80,190 220,155" stroke="#16a34a" fill="none" stroke-dasharray="4,3"/>
<path d="M220,155 Q220,200 360,155" stroke="#16a34a" fill="none" stroke-dasharray="4,3"/>
''', caption='asyncio: один поток переключается между задачами') + '''

<h3>async/await — базовый синтаксис</h3>
<pre><code>import asyncio

async def greet(name, delay):
    await asyncio.sleep(delay)    # НЕ блокирует event loop!
    print(f"Привет, {name}!")

async def main():
    # Запуск нескольких корутин "одновременно"
    await asyncio.gather(
        greet("Алиса", 1),
        greet("Боб",   0.5),
        greet("Кэрол", 0.1),
    )

asyncio.run(main())
# Кэрол → Боб → Алиса  (в порядке задержек)
</code></pre>

<h3>asyncio.create_task — фоновые задачи</h3>
<pre><code>async def main():
    task1 = asyncio.create_task(greet("Алиса", 1))
    task2 = asyncio.create_task(greet("Боб", 0.5))

    # Делаем другую работу пока задачи выполняются
    print("Работаю...")
    await task1
    await task2
</code></pre>
''' + tip('asyncio не ускоряет CPU-задачи. Он нужен для I/O: HTTP, базы данных, файлы. Для CPU-задач — multiprocessing.'),
      'code_example': '''import asyncio

async def fetch_data(url, delay):
    """Симулируем HTTP запрос."""
    print(f"  → Запрос к {url}")
    await asyncio.sleep(delay)
    print(f"  ← Ответ от {url} ({delay}s)")
    return f"data:{url}"

async def main():
    import time
    urls = [
        ("api.example.com/users",    0.3),
        ("api.example.com/products", 0.5),
        ("api.example.com/orders",   0.2),
    ]

    start = time.time()

    # Параллельный запуск всех запросов
    results = await asyncio.gather(
        *[fetch_data(url, delay) for url, delay in urls]
    )

    print(f"Всего: {time.time()-start:.2f}s (vs {sum(d for _,d in urls):.1f}s синхронно)")
    return results

results = asyncio.run(main())
print("Получено:", results)
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 33 — Аннотации типов и dataclasses
# ════════════════════════════════════════════════════════════════
{
  'title': 'Type hints и dataclasses',
  'description': 'Аннотации типов делают код читаемым. Dataclasses избавляют от шаблонного кода.',
  'icon': 'fas fa-tag',
  'color': '#0369a1',
  'order': 33,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'Аннотации типов: int, str, list, Optional, Union',
      'order': 1,
      'estimated_minutes': 50,
      'content': '''<h2>Type Hints (PEP 484)</h2>
<p>Python динамически типизирован, но начиная с 3.5 поддерживает <strong>аннотации типов</strong>.
Python их не проверяет в runtime, но это делают IDE и инструменты (mypy, pyright).</p>

<h3>Базовые аннотации</h3>
<pre><code>def greet(name: str) -> str:
    return f"Привет, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# Переменные
age: int = 25
scores: list[float] = [9.5, 8.0, 7.5]   # Python 3.9+
mapping: dict[str, int] = {"one": 1}
</code></pre>

<h3>typing — расширенные типы</h3>
<pre><code>from typing import Optional, Union, List, Dict, Tuple, Any

# Optional[X] = X | None
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)   # может вернуть None

# Union[X, Y] — один из нескольких типов
def stringify(val: Union[int, float, str]) -> str:
    return str(val)

# Python 3.10+ — упрощённый синтаксис
def find(user_id: int) -> str | None: ...
def proc(val: int | float | str) -> str: ...
</code></pre>

''' + table(
  ['Аннотация','Значение','Пример'],
  [
    ['list[int]','Список целых','[1, 2, 3]'],
    ['dict[str, int]','Словарь str → int','{"a": 1}'],
    ['tuple[int, str]','Кортеж (int, str)','(1, "hi")'],
    ['Optional[str]','str или None','None / "text"'],
    ['Union[int, str]','int или str','1 / "one"'],
    ['Any','Любой тип','anything'],
    ['Callable[[int], str]','Функция int → str','lambda x: str(x)'],
    ['TypeVar("T")','Обобщённый тип','Для generic-функций'],
  ],
  'Основные аннотации типов'
) + tip('Аннотации — документация + подсказки IDE. Запусти mypy для статической проверки.'),
      'code_example': '''from typing import Optional, Union

def divide(a: int, b: int) -> Optional[float]:
    """Делит a на b. Возвращает None при делении на 0."""
    if b == 0:
        return None
    return a / b

def describe(value: Union[int, str, list]) -> str:
    if isinstance(value, int):
        return f"Число: {value}"
    elif isinstance(value, str):
        return f"Строка длиной {len(value)}"
    else:
        return f"Список из {len(value)} элементов"

# Проверка
print(divide(10, 3))    # 3.333...
print(divide(10, 0))    # None

for v in [42, "hello", [1, 2, 3]]:
    print(describe(v))
'''
    },
    {
      'title': 'dataclasses: автоматические __init__, __repr__, __eq__',
      'order': 2,
      'estimated_minutes': 55,
      'content': '''<h2>dataclasses (Python 3.7+)</h2>
<p>Декоратор <code>@dataclass</code> автоматически генерирует <code>__init__</code>,
<code>__repr__</code> и <code>__eq__</code> по объявленным полям.</p>

<h3>Без dataclass vs с dataclass</h3>
<pre><code># ❌ Без dataclass — много шаблонного кода
class PointOld:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# ✅ С dataclass
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
print(p1)           # Point(x=1.0, y=2.0)
print(p1 == p2)     # True
</code></pre>

<h3>Параметры dataclass</h3>
<pre><code>from dataclasses import dataclass, field
from typing import List

@dataclass(order=True, frozen=True)   # сравнение + неизменяемость
class Student:
    name: str
    grade: float
    courses: List[str] = field(default_factory=list)
    _id: int = field(default=0, repr=False)  # не в repr

s1 = Student("Alice", 4.5)
s2 = Student("Bob",   3.8)
print(sorted([s2, s1]))   # по grade (первое поле)

# frozen=True — нельзя изменить
# s1.grade = 5.0  → FrozenInstanceError
</code></pre>

<h3>post_init и вычисляемые поля</h3>
<pre><code>from dataclasses import dataclass
import math

@dataclass
class Circle:
    radius: float
    area: float = 0.0
    perimeter: float = 0.0

    def __post_init__(self):
        self.area = math.pi * self.radius ** 2
        self.perimeter = 2 * math.pi * self.radius

c = Circle(radius=5)
print(f"Площадь: {c.area:.2f}")      # 78.54
print(f"Периметр: {c.perimeter:.2f}")  # 31.42
</code></pre>
''' + table(
  ['Параметр','Что делает'],
  [
    ['eq=True (по умол.)','Генерирует __eq__'],
    ['order=False (по умол.)','Если True — генерирует __lt__,__gt__ и т.д.'],
    ['frozen=False (по умол.)','Если True — поля неизменяемы'],
    ['repr=True (по умол.)','Генерирует __repr__'],
    ['slots=False (3.10+)','Если True — использует __slots__ (быстрее)'],
  ],
  'Параметры @dataclass'
),
      'code_example': '''from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)

    def discounted(self, percent: float) -> float:
        return self.price * (1 - percent / 100)

@dataclass(order=True)
class Student:
    # order=True — сортировка по первому полю (gpa)
    gpa: float
    name: str
    courses: List[str] = field(default_factory=list, compare=False)

p = Product("Ноутбук", 75000, ["электроника", "компьютеры"])
print(p)
print(f"Скидка 10%: {p.discounted(10):,.0f} руб.")

students = [
    Student(3.5, "Боб",   ["Алгебра"]),
    Student(4.8, "Алиса", ["Python", "ML"]),
    Student(3.9, "Кэрол", ["Физика"]),
]
print("Рейтинг:", sorted(students, reverse=True))
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 34 — Контекстные менеджеры
# ════════════════════════════════════════════════════════════════
{
  'title': 'Контекстные менеджеры',
  'description': 'with-блоки, __enter__/__exit__, contextlib.contextmanager.',
  'icon': 'fas fa-lock',
  'color': '#b45309',
  'order': 34,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'with-блоки и протокол контекстного менеджера',
      'order': 1,
      'estimated_minutes': 50,
      'content': '''<h2>Контекстные менеджеры</h2>
<p>Конструкция <code>with</code> гарантирует выполнение завершающего кода (<code>__exit__</code>)
даже при исключении. Используется для: файлов, соединений с БД, блокировок, таймеров.</p>

<h3>Стандартное использование</h3>
<pre><code># Файл закроется автоматически даже при ошибке
with open("data.txt", "r") as f:
    content = f.read()

# Эквивалент без with:
f = open("data.txt", "r")
try:
    content = f.read()
finally:
    f.close()    # with делает это за нас
</code></pre>

<h3>Создание собственного менеджера: __enter__ / __exit__</h3>
<pre><code>import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self        # доступен через "as"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Время: {self.elapsed:.4f}s")
        return False       # False = не подавлять исключения

with Timer() as t:
    sum(range(1_000_000))
print(f"Зафиксировано: {t.elapsed:.4f}s")
</code></pre>

<h3>contextlib.contextmanager — через генератор</h3>
<pre><code>from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield                      # здесь выполняется тело with
    finally:
        print(f"Время: {time.perf_counter()-start:.4f}s")

with timer():
    [x**2 for x in range(100000)]
</code></pre>

<h3>Практический пример: транзакция БД</h3>
<pre><code>from contextlib import contextmanager

@contextmanager
def transaction(conn):
    """Автоматический commit или rollback."""
    try:
        yield conn
        conn.commit()
        print("Транзакция подтверждена")
    except Exception as e:
        conn.rollback()
        print(f"Откат транзакции: {e}")
        raise

# with transaction(db_conn) as conn:
#     conn.execute("INSERT ...")
</code></pre>
''' + tip('contextmanager упрощает создание менеджеров. Код до yield — __enter__, после — __exit__.'),
      'code_example': '''from contextlib import contextmanager
import time

@contextmanager
def timer(label=""):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        tag = f"[{label}] " if label else ""
        print(f"{tag}Время выполнения: {elapsed:.6f}s")

@contextmanager
def indent(level=1):
    """Менеджер для отступов в выводе."""
    prefix = "  " * level
    print(prefix + "┌─ Начало блока")
    try:
        yield prefix
    finally:
        print(prefix + "└─ Конец блока")

# Тест 1
with timer("список"):
    data = [i**2 for i in range(100_000)]

# Тест 2
with indent(1) as prefix:
    print(prefix + "  Строка 1")
    print(prefix + "  Строка 2")
    with indent(2) as prefix2:
        print(prefix2 + "  Вложенный блок")
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 35 — Паттерны проектирования
# ════════════════════════════════════════════════════════════════
{
  'title': 'Паттерны проектирования',
  'description': 'Singleton, Factory, Observer, Strategy и другие шаблоны на Python.',
  'icon': 'fas fa-shapes',
  'color': '#0f766e',
  'order': 35,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'Порождающие паттерны: Singleton, Factory, Builder',
      'order': 1,
      'estimated_minutes': 60,
      'content': '''<h2>Паттерны проектирования</h2>
<p>Паттерны — типовые решения частых проблем проектирования. Делятся на три группы.</p>

''' + table(
  ['Группа','Что решает','Примеры'],
  [
    ['Порождающие','Как создавать объекты','Singleton, Factory, Builder'],
    ['Структурные','Как компоновать объекты','Decorator, Adapter, Proxy'],
    ['Поведенческие','Как объекты взаимодействуют','Observer, Strategy, Command'],
  ],
  'Три категории паттернов'
) + '''

<h3>Singleton — единственный экземпляр</h3>
<pre><code>class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class Config(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.debug = False
            self.db_url = "sqlite:///app.db"
            self._initialized = True

c1 = Config()
c2 = Config()
print(c1 is c2)   # True — один и тот же объект
c1.debug = True
print(c2.debug)   # True
</code></pre>

<h3>Factory Method — создание без указания класса</h3>
<pre><code>from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...

class Dog(Animal):
    def speak(self): return "Гав!"

class Cat(Animal):
    def speak(self): return "Мяу!"

def animal_factory(kind: str) -> Animal:
    registry = {"dog": Dog, "cat": Cat}
    cls = registry.get(kind)
    if not cls:
        raise ValueError(f"Неизвестный вид: {kind}")
    return cls()

dog = animal_factory("dog")
print(dog.speak())   # Гав!
</code></pre>

<h3>Builder — пошаговое создание сложного объекта</h3>
<pre><code>class QueryBuilder:
    def __init__(self):
        self._table = ""
        self._conditions = []
        self._limit = None

    def from_table(self, table):
        self._table = table
        return self          # возвращаем self для цепочки

    def where(self, condition):
        self._conditions.append(condition)
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self):
        sql = f"SELECT * FROM {self._table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        if self._limit:
            sql += f" LIMIT {self._limit}"
        return sql

query = (QueryBuilder()
    .from_table("users")
    .where("age > 18")
    .where("active = 1")
    .limit(10)
    .build())
print(query)
</code></pre>
''',
      'code_example': '''# Factory + Builder комбинация

class Report:
    def __init__(self, title, data, format_):
        self.title = title
        self.data = data
        self.format_ = format_
    def render(self):
        if self.format_ == 'text':
            lines = [self.title, "-"*len(self.title)]
            lines += [f"  {k}: {v}" for k, v in self.data.items()]
            return "\n".join(lines)
        elif self.format_ == 'csv':
            header = ",".join(self.data.keys())
            row = ",".join(str(v) for v in self.data.values())
            return f"{header}\n{row}"
        return str(self.data)

class ReportBuilder:
    def __init__(self):
        self._title = "Отчёт"
        self._data = {}
        self._format = "text"
    def title(self, t):
        self._title = t; return self
    def add(self, key, value):
        self._data[key] = value; return self
    def format(self, f):
        self._format = f; return self
    def build(self):
        return Report(self._title, self._data, self._format)

# Создаём отчёт
r = (ReportBuilder()
     .title("Успеваемость")
     .add("Иванов", 85)
     .add("Петров", 72)
     .add("Сидоров", 91)
     .format("text")
     .build())
print(r.render())
print()

r2 = (ReportBuilder()
     .title("Успеваемость")
     .add("Иванов", 85)
     .add("Петров", 72)
     .format("csv")
     .build())
print(r2.render())
'''
    },
    {
      'title': 'Поведенческие паттерны: Observer, Strategy, Command',
      'order': 2,
      'estimated_minutes': 55,
      'content': '''<h2>Поведенческие паттерны</h2>

<h3>Observer — подписка на события</h3>
<pre><code>class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list] = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)
        return self

    def emit(self, event, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

emitter = EventEmitter()
emitter.on("login", lambda u: print(f"Пользователь вошёл: {u}"))
emitter.on("login", lambda u: print(f"Записываем в лог: {u}"))
emitter.emit("login", "alice")
</code></pre>

<h3>Strategy — взаимозаменяемые алгоритмы</h3>
<pre><code>from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data):
        a = data.copy()
        for i in range(len(a)):
            for j in range(len(a)-i-1):
                if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]
        return a

class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        if len(data) <= 1: return data
        pivot = data[len(data)//2]
        left   = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right  = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    def sort(self, data):
        return self.strategy.sort(data)

sorter = Sorter(QuickSortStrategy())
print(sorter.sort([3,1,4,1,5,9,2,6]))
</code></pre>

<h3>Command — инкапсуляция действия</h3>
<pre><code>from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class AddCommand(Command):
    def __init__(self, text_editor, text):
        self.editor = text_editor
        self.text = text
    def execute(self):
        self.editor.content += self.text
    def undo(self):
        self.editor.content = self.editor.content[:-len(self.text)]

class TextEditor:
    def __init__(self): self.content = ""
    def __str__(self): return f'"{self.content}"'

editor = TextEditor()
history = []

for text in ["Hello", " World", "!"]:
    cmd = AddCommand(editor, text)
    cmd.execute()
    history.append(cmd)
    print(editor)

# Undo последних 2 действий
for _ in range(2):
    history.pop().undo()
    print(editor)
</code></pre>
''',
      'code_example': '''# Strategy: выбор алгоритма скидки

class DiscountStrategy:
    def calculate(self, price: float) -> float:
        return price

class PercentDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent
    def calculate(self, price):
        return price * (1 - self.percent / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount):
        self.amount = amount
    def calculate(self, price):
        return max(0, price - self.amount)

class BuyTwoGetOneDiscount(DiscountStrategy):
    def calculate(self, price):
        # 3 за цену 2
        return price * 2 / 3

class Cart:
    def __init__(self, price, strategy: DiscountStrategy = None):
        self.price = price
        self.strategy = strategy or DiscountStrategy()
    def total(self):
        return self.strategy.calculate(self.price)

price = 1500
strategies = [
    ("Без скидки",      DiscountStrategy()),
    ("Скидка 20%",      PercentDiscount(20)),
    ("Скидка 300 руб.", FixedDiscount(300)),
    ("2+1",             BuyTwoGetOneDiscount()),
]
for name, s in strategies:
    cart = Cart(price, s)
    print(f"{name}: {cart.total():,.0f} руб.")
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 36 — pytest и тестирование
# ════════════════════════════════════════════════════════════════
{
  'title': 'Тестирование с pytest',
  'description': 'pytest, фикстуры, параметризация, mock-объекты, coverage.',
  'icon': 'fas fa-vial',
  'color': '#7c3aed',
  'order': 36,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'pytest: основы, assertions, fixtures',
      'order': 1,
      'estimated_minutes': 55,
      'content': '''<h2>pytest</h2>
<p>pytest — самый популярный фреймворк для тестирования Python. Проще, чем unittest.</p>

<h3>Установка и первый тест</h3>
<pre><code># pip install pytest

# файл: test_math.py
def add(a, b): return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

def test_add_floats():
    result = add(0.1, 0.2)
    assert abs(result - 0.3) < 1e-9   # float сравнение

# Запуск: pytest test_math.py -v
</code></pre>

<h3>Тестирование исключений</h3>
<pre><code>import pytest

def divide(a, b):
    if b == 0: raise ZeroDivisionError("делить на ноль нельзя")
    return a / b

def test_divide_ok():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="нельзя"):
        divide(10, 0)
</code></pre>

<h3>Фикстуры — подготовка данных</h3>
<pre><code>import pytest

@pytest.fixture
def sample_list():
    return [3, 1, 4, 1, 5, 9, 2, 6]

@pytest.fixture
def empty_list():
    return []

def test_max(sample_list):
    assert max(sample_list) == 9

def test_sorted(sample_list):
    assert sorted(sample_list) == [1, 1, 2, 3, 4, 5, 6, 9]

def test_empty_raises(empty_list):
    with pytest.raises(ValueError):
        max(empty_list)
</code></pre>

<h3>Параметризация</h3>
<pre><code>@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
</code></pre>
''' + tip('pytest.mark.parametrize позволяет запустить один тест с множеством входных данных — устраняет дублирование.'),
      'code_example': '''# Полный пример тестирования класса стека

class Stack:
    def __init__(self):
        self._data = []
    def push(self, item):
        self._data.append(item)
    def pop(self):
        if not self._data:
            raise IndexError("Стек пуст")
        return self._data.pop()
    def peek(self):
        if not self._data:
            raise IndexError("Стек пуст")
        return self._data[-1]
    def __len__(self):
        return len(self._data)
    def is_empty(self):
        return len(self._data) == 0

# Тесты (можно запустить через pytest)
def test_push_pop():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1

def test_lifo_order():
    s = Stack()
    for i in range(5):
        s.push(i)
    result = [s.pop() for _ in range(5)]
    assert result == [4, 3, 2, 1, 0]

def test_empty_pop():
    s = Stack()
    try:
        s.pop()
        assert False, "Должно быть исключение"
    except IndexError:
        pass

# Запуск тестов
for test in [test_push_pop, test_lifo_order, test_empty_pop]:
    test()
    print(f"✓ {test.__name__}")
'''
    },
    {
      'title': 'Mock, coverage и TDD',
      'order': 2,
      'estimated_minutes': 50,
      'content': '''<h2>Mock-объекты</h2>
<p>Mock позволяет заменить реальные зависимости (HTTP, БД, файлы) на объекты-заглушки.</p>

<pre><code>from unittest.mock import Mock, patch, MagicMock

# Создать mock
mock_db = Mock()
mock_db.get_user.return_value = {"id": 1, "name": "Alice"}
mock_db.save.return_value = True

print(mock_db.get_user(1))   # {"id": 1, "name": "Alice"}
mock_db.save.assert_called_once()  # проверяем что save был вызван
</code></pre>

<h3>patch — замена реального объекта</h3>
<pre><code>import requests
from unittest.mock import patch

def get_weather(city):
    resp = requests.get(f"https://api.weather.com/{city}")
    return resp.json()["temperature"]

def test_weather():
    mock_response = Mock()
    mock_response.json.return_value = {"temperature": 22}

    with patch("requests.get", return_value=mock_response):
        temp = get_weather("Moscow")

    assert temp == 22
</code></pre>

<h3>Coverage — покрытие кода</h3>
<pre><code># pip install pytest-cov
# pytest --cov=my_module --cov-report=html

# Показывает какие строки кода НЕ покрыты тестами:
# Name          Stmts  Miss  Cover
# my_module.py     45     3    93%
</code></pre>

<h3>TDD — разработка через тесты</h3>
''' + table(
  ['Шаг','Действие','Состояние'],
  [
    ['1. RED','Пишем тест → он падает','❌ FAIL'],
    ['2. GREEN','Пишем минимальный код → тест проходит','✅ PASS'],
    ['3. REFACTOR','Улучшаем код → тест должен остаться зелёным','✅ PASS'],
  ],
  'Цикл TDD: Red → Green → Refactor'
) + tip('TDD заставляет думать об интерфейсе ДО реализации. Код получается более тестируемым и чистым.'),
      'code_example': '''from unittest.mock import Mock, patch

# Пример: тестирование функции с зависимостью от времени
from datetime import datetime

def get_greeting(name: str, clock=None) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if clock is None:
        hour = datetime.now().hour
    else:
        hour = clock()

    if 6 <= hour < 12:
        period = "Доброе утро"
    elif 12 <= hour < 18:
        period = "Добрый день"
    elif 18 <= hour < 22:
        period = "Добрый вечер"
    else:
        period = "Доброй ночи"

    return f"{period}, {name}!"

# Тестируем с mock-часами
def test_morning():
    mock_clock = Mock(return_value=9)
    assert get_greeting("Алиса", mock_clock) == "Доброе утро, Алиса!"

def test_evening():
    mock_clock = Mock(return_value=20)
    assert get_greeting("Боб", mock_clock) == "Добрый вечер, Боб!"

def test_night():
    mock_clock = Mock(return_value=2)
    assert get_greeting("Кэрол", mock_clock) == "Доброй ночи, Кэрол!"

for t in [test_morning, test_evening, test_night]:
    t()
    print(f"✓ {t.__name__}")
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 37 — Работа с базами данных (SQLite)
# ════════════════════════════════════════════════════════════════
{
  'title': 'SQLite и работа с базами данных',
  'description': 'sqlite3, SQL-запросы, ORM-подход, безопасность запросов.',
  'icon': 'fas fa-database',
  'color': '#1e40af',
  'order': 37,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'sqlite3: CREATE, INSERT, SELECT, UPDATE, DELETE',
      'order': 1,
      'estimated_minutes': 60,
      'content': '''<h2>Встроенный модуль sqlite3</h2>
<p>SQLite — встроенная в Python база данных. Хранится в одном файле, не требует сервера.</p>

<h3>Создание таблицы и вставка данных</h3>
<pre><code>import sqlite3

# Подключение (создаёт файл если не существует)
conn = sqlite3.connect("school.db")
# conn = sqlite3.connect(":memory:")  # только в RAM

cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT NOT NULL,
        grade   REAL DEFAULT 0,
        group_  TEXT
    )
""")

# Вставка одной записи
cursor.execute(
    "INSERT INTO students (name, grade, group_) VALUES (?, ?, ?)",
    ("Иванов Иван", 4.5, "ИТ-21")
)

# Вставка нескольких
students = [
    ("Петров Пётр", 3.8, "ИТ-21"),
    ("Сидорова Анна", 4.9, "ИТ-22"),
]
cursor.executemany(
    "INSERT INTO students (name, grade, group_) VALUES (?, ?, ?)",
    students
)

conn.commit()   # ОБЯЗАТЕЛЬНО для сохранения изменений
conn.close()
</code></pre>

''' + warn('ВСЕГДА используй параметрические запросы (знак ?) — никогда не форматируй данные через f-string! Это защита от SQL-инъекций.') + '''

<h3>Выборка данных</h3>
<pre><code>conn = sqlite3.connect("school.db")
conn.row_factory = sqlite3.Row  # строки как словари

cursor = conn.cursor()

# SELECT
cursor.execute("SELECT * FROM students ORDER BY grade DESC")
rows = cursor.fetchall()

for row in rows:
    print(f"{row['name']}: {row['grade']}")

# WHERE с параметром
cursor.execute("SELECT * FROM students WHERE group_ = ?", ("ИТ-21",))
group_students = cursor.fetchall()

# Агрегация
cursor.execute("SELECT group_, AVG(grade) as avg FROM students GROUP BY group_")
for row in cursor.fetchall():
    print(f"{row['group_']}: средний балл {row['avg']:.2f}")

conn.close()
</code></pre>

<h3>Context manager</h3>
<pre><code>with sqlite3.connect("school.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET grade = ? WHERE name = ?",
                   (5.0, "Сидорова Анна"))
    # commit автоматически при выходе из with
</code></pre>
''',
      'code_example': '''import sqlite3

# Создаём базу в памяти
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

with conn:
    conn.execute("""
        CREATE TABLE products (
            id    INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            price REAL,
            stock INTEGER DEFAULT 0
        )
    """)
    conn.executemany(
        "INSERT INTO products (name, price, stock) VALUES (?,?,?)",
        [
            ("Ноутбук",  75000, 10),
            ("Мышь",     1500,  50),
            ("Клавиатура", 3200, 30),
            ("Монитор",  35000, 15),
            ("Наушники", 8000,  25),
        ]
    )

# Запросы
cursor = conn.cursor()

print("=== Все товары ===")
for row in cursor.execute("SELECT * FROM products ORDER BY price DESC"):
    print(f"  {row['name']}: {row['price']:,.0f} руб. (склад: {row['stock']} шт.)")

print("\\n=== Дорогие товары (>5000) ===")
for row in cursor.execute("SELECT name, price FROM products WHERE price > ?", (5000,)):
    print(f"  {row['name']}: {row['price']:,.0f}")

print("\\n=== Сумма инвентаря ===")
row = cursor.execute("SELECT SUM(price * stock) as total FROM products").fetchone()
print(f"  Итого: {row['total']:,.0f} руб.")

conn.close()
'''
    },
    {
      'title': 'ORM-подход и паттерн Repository',
      'order': 2,
      'estimated_minutes': 55,
      'content': '''<h2>ORM и паттерн Repository</h2>
<p>ORM (Object-Relational Mapping) — слой абстракции, который представляет строки таблицы как объекты Python.</p>

<h3>Простой ORM на dataclasses</h3>
<pre><code>import sqlite3
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Student:
    name: str
    grade: float
    group_: str
    id: int = 0   # 0 = не сохранён в БД

class StudentRepository:
    """Инкапсулирует всю работу с таблицей students."""

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, grade REAL, group_ TEXT
            )
        """)
        self.conn.commit()

    def save(self, student: Student) -> Student:
        if student.id == 0:
            cur = self.conn.execute(
                "INSERT INTO students (name,grade,group_) VALUES (?,?,?)",
                (student.name, student.grade, student.group_)
            )
            student.id = cur.lastrowid
        else:
            self.conn.execute(
                "UPDATE students SET name=?,grade=?,group_=? WHERE id=?",
                (student.name, student.grade, student.group_, student.id)
            )
        self.conn.commit()
        return student

    def find_all(self) -> List[Student]:
        rows = self.conn.execute("SELECT * FROM students").fetchall()
        return [Student(r["name"],r["grade"],r["group_"],r["id"]) for r in rows]

    def find_by_group(self, group: str) -> List[Student]:
        rows = self.conn.execute(
            "SELECT * FROM students WHERE group_=?", (group,)
        ).fetchall()
        return [Student(r["name"],r["grade"],r["group_"],r["id"]) for r in rows]

    def delete(self, student_id: int):
        self.conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()

# Использование
repo = StudentRepository(":memory:")
repo.save(Student("Иванов",  4.5, "ИТ-21"))
repo.save(Student("Петров",  3.8, "ИТ-21"))
repo.save(Student("Сидорова",4.9, "ИТ-22"))

for s in repo.find_all():
    print(s)
</code></pre>
''' + tip('В реальных проектах используют SQLAlchemy или Django ORM. Но понимание базового SQLite помогает разобраться в том, что происходит "под капотом".'),
      'code_example': '''import sqlite3
from dataclasses import dataclass

@dataclass
class Task:
    title: str
    done: bool = False
    id: int = 0

class TaskDB:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
            CREATE TABLE tasks (
                id    INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done  INTEGER DEFAULT 0
            )
        """)

    def add(self, task):
        cur = self.conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?,?)",
            (task.title, int(task.done))
        )
        self.conn.commit()
        task.id = cur.lastrowid
        return task

    def complete(self, task_id):
        self.conn.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
        self.conn.commit()

    def pending(self):
        rows = self.conn.execute("SELECT * FROM tasks WHERE done=0").fetchall()
        return [Task(r["title"], bool(r["done"]), r["id"]) for r in rows]

    def all(self):
        rows = self.conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [Task(r["title"], bool(r["done"]), r["id"]) for r in rows]

db = TaskDB()
t1 = db.add(Task("Изучить SQL"))
t2 = db.add(Task("Написать тесты"))
t3 = db.add(Task("Сдать лабораторную"))

db.complete(t1.id)

print("Все задачи:")
for t in db.all():
    status = "✓" if t.done else "○"
    print(f"  [{status}] {t.title}")

print(f"\\nОсталось: {len(db.pending())} задач")
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 38 — HTTP-запросы и REST API
# ════════════════════════════════════════════════════════════════
{
  'title': 'HTTP-запросы и REST API',
  'description': 'requests, работа с JSON API, обработка ошибок, rate limiting.',
  'icon': 'fas fa-globe',
  'color': '#0891b2',
  'order': 38,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'requests: GET, POST, заголовки, сессии',
      'order': 1,
      'estimated_minutes': 55,
      'content': '''<h2>Библиотека requests</h2>
<pre><code># pip install requests
import requests
</code></pre>

<h3>GET-запрос</h3>
<pre><code>import requests

# Простой GET
resp = requests.get("https://api.github.com/users/python")
print(resp.status_code)   # 200
data = resp.json()
print(data["name"])       # Python

# GET с параметрами
resp = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "python sort:stars", "per_page": 5},
    timeout=10             # секунды
)
for repo in resp.json()["items"]:
    print(f"{repo['name']}: ★{repo['stargazers_count']}")
</code></pre>

<h3>POST-запрос</h3>
<pre><code># POST с JSON
resp = requests.post(
    "https://httpbin.org/post",
    json={"name": "Alice", "score": 95},
    headers={"Authorization": "Bearer my-token"},
)
print(resp.json()["json"])   # наш payload

# POST с формой
resp = requests.post(
    "https://httpbin.org/post",
    data={"username": "alice", "password": "secret"},
)
</code></pre>

<h3>Обработка ошибок</h3>
<pre><code>import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

try:
    resp = requests.get("https://api.example.com/data", timeout=5)
    resp.raise_for_status()   # вызывает HTTPError для 4xx/5xx
    data = resp.json()
except Timeout:
    print("Сервер не ответил вовремя")
except ConnectionError:
    print("Нет соединения")
except HTTPError as e:
    print(f"HTTP ошибка: {e.response.status_code}")
</code></pre>

<h3>Session — переиспользование соединения</h3>
<pre><code>with requests.Session() as s:
    s.headers.update({"Authorization": "Bearer TOKEN"})
    s.headers.update({"Accept": "application/json"})

    users = s.get("/api/users").json()
    profile = s.get(f"/api/users/{users[0]['id']}").json()
    s.patch(f"/api/users/{profile['id']}", json={"active": True})
</code></pre>
''' + table(
  ['Метод','Назначение','Тело запроса'],
  [
    ['GET','Получить данные','Нет'],
    ['POST','Создать ресурс','JSON / Form'],
    ['PUT','Заменить ресурс целиком','JSON'],
    ['PATCH','Частично обновить','JSON'],
    ['DELETE','Удалить ресурс','Нет'],
  ],
  'HTTP методы REST API'
),
      'code_example': '''import urllib.request
import json

# Используем встроенный urllib (без pip install)
def get_json(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

# Публичные API
joke = get_json("https://official-joke-api.appspot.com/jokes/random")
if "error" not in joke:
    print(f"Анекдот: {joke.get('setup')}")
    print(f"         {joke.get('punchline')}")
else:
    print("Нет соединения с интернетом — демонстрационный режим")

    # Симулируем ответ API
    fake_data = {
        "users": [
            {"id": 1, "name": "Alice", "score": 95},
            {"id": 2, "name": "Bob",   "score": 87},
        ]
    }
    print("\\nДанные API (симуляция):")
    for user in fake_data["users"]:
        print(f"  {user['name']}: {user['score']} баллов")
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 39 — Регулярные выражения (продвинутый)
# ════════════════════════════════════════════════════════════════
{
  'title': 'Регулярные выражения: продвинутый уровень',
  'description': 'Группы захвата, lookahead/lookbehind, именованные группы, флаги.',
  'icon': 'fas fa-search',
  'color': '#be123c',
  'order': 39,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'Группы захвата, named groups, lookahead',
      'order': 1,
      'estimated_minutes': 55,
      'content': '''<h2>Продвинутые возможности регулярных выражений</h2>

<h3>Группы захвата</h3>
<pre><code>import re

# () — группа захвата
date = "2024-03-15"
m = re.match(r"(\\d{4})-(\\d{2})-(\\d{2})", date)
year, month, day = m.groups()
print(year, month, day)   # 2024 03 15

# Именованные группы (?P<name>...)
m = re.match(r"(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})", date)
print(m.group("year"))   # 2024
print(m.groupdict())     # {'year': '2024', 'month': '03', 'day': '15'}
</code></pre>

<h3>Lookahead и Lookbehind</h3>
<pre><code># Позитивный lookahead (?=...)
# Найти цены со знаком рубля
text = "Товар 1500₽, скидка 200₽, итого 1300₽"
prices = re.findall(r"\\d+(?=₽)", text)
print(prices)   # ['1500', '200', '1300']

# Негативный lookahead (?!...)
# Слова НЕ перед запятой
words = re.findall(r"\\w+(?!,)\\b", "apple, orange, banana")

# Позитивный lookbehind (?<=...)
# Числа после знака доллара
text = "$100 и €200 и £300"
usd = re.findall(r"(?<=\\$)\\d+", text)
print(usd)   # ['100']
</code></pre>

<h3>Замена с функцией</h3>
<pre><code>def censor_card(m):
    card = m.group(0)
    return "*" * 12 + card[-4:]   # скрыть первые 12 цифр

text = "Карта 4111111111111111 и 5500005555555559"
result = re.sub(r"\\d{16}", censor_card, text)
print(result)   # Карта ************1111 и ************5559
</code></pre>
''' + table(
  ['Конструкция','Что делает','Пример'],
  [
    ['(...)','Группа захвата','(\\d+) захватывает число'],
    ['(?:...)','Незахватывающая группа','(?:abc)+ — группа без захвата'],
    ['(?P<name>...)','Именованная группа','(?P<year>\\d{4})'],
    ['(?=...)','Позитивный lookahead','\\d+(?=₽) — число перед ₽'],
    ['(?!...)','Негативный lookahead','\\w+(?!\\.py) — не .py файл'],
    ['(?<=...)','Позитивный lookbehind','(?<=\\$)\\d+ — число после $'],
    ['(?<!...)','Негативный lookbehind','(?<!-)\\d+ — не после минуса'],
  ],
  'Продвинутые конструкции regex'
),
      'code_example': '''import re

# Задача: парсинг логов
log = """
2024-03-15 09:23:11 INFO  User alice logged in
2024-03-15 09:24:05 ERROR Failed to connect to db: timeout
2024-03-15 09:24:06 WARN  Retry attempt 1/3
2024-03-15 09:24:08 ERROR Failed to connect to db: timeout
2024-03-15 09:25:00 INFO  User bob logged in
"""

# Именованные группы
pattern = r"(?P<date>\\d{4}-\\d{2}-\\d{2}) (?P<time>\\d{2}:\\d{2}:\\d{2}) (?P<level>\\w+)\\s+(?P<message>.+)"

entries = []
for m in re.finditer(pattern, log):
    entries.append(m.groupdict())

# Статистика по уровням
from collections import Counter
levels = Counter(e["level"] for e in entries)
print("Статистика:", dict(levels))

# Все ERROR сообщения
errors = [e for e in entries if e["level"] == "ERROR"]
print("\\nОшибки:")
for e in errors:
    print(f"  [{e['time']}] {e['message']}")

# Извлечь email адреса
text = "Контакты: alice@example.com, bob.smith@corp.org, admin@test.ru"
emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", text)
print("\\nEmail:", emails)
'''
    },
  ]
},

# ════════════════════════════════════════════════════════════════
# МОДУЛЬ 40 — CLI-инструменты: argparse, pathlib, os
# ════════════════════════════════════════════════════════════════
{
  'title': 'CLI-инструменты: argparse и pathlib',
  'description': 'Создание командных утилит, работа с файловой системой через pathlib.',
  'icon': 'fas fa-terminal',
  'color': '#374151',
  'order': 40,
  'subject_slug': 'python',
  'lessons': [
    {
      'title': 'argparse: аргументы командной строки',
      'order': 1,
      'estimated_minutes': 50,
      'content': '''<h2>argparse</h2>
<p>Стандартная библиотека для создания CLI-утилит с аргументами, флагами и подкомандами.</p>

<h3>Базовое использование</h3>
<pre><code># script.py
import argparse

parser = argparse.ArgumentParser(description="Калькулятор сумм")
parser.add_argument("numbers", nargs="+", type=float, help="Числа для суммирования")
parser.add_argument("--multiply", "-m", action="store_true", help="Умножить вместо сложения")
parser.add_argument("--round", "-r", type=int, default=2, help="Знаков после запятой")

args = parser.parse_args()

if args.multiply:
    result = 1
    for n in args.numbers: result *= n
else:
    result = sum(args.numbers)

print(round(result, args.round))

# python script.py 1.5 2.3 3.1          → 6.9
# python script.py 2 3 4 --multiply     → 24.0
# python script.py 1.23456 --round 4    → 1.2346
</code></pre>

<h3>Подкоманды</h3>
<pre><code>parser = argparse.ArgumentParser(description="Утилита работы с файлами")
subparsers = parser.add_subparsers(dest="command")

# Подкоманда count
count_parser = subparsers.add_parser("count", help="Посчитать строки")
count_parser.add_argument("file", help="Путь к файлу")

# Подкоманда search
search_parser = subparsers.add_parser("search", help="Найти текст")
search_parser.add_argument("pattern", help="Шаблон поиска")
search_parser.add_argument("file", help="Файл")

args = parser.parse_args()
if args.command == "count":
    print(f"Строк: {sum(1 for _ in open(args.file))}")
elif args.command == "search":
    import re
    for i, line in enumerate(open(args.file), 1):
        if re.search(args.pattern, line):
            print(f"{i}: {line.rstrip()}")
</code></pre>
''',
      'code_example': '''# Симулируем argparse без реальных аргументов командной строки
import argparse
import sys

def create_cli():
    parser = argparse.ArgumentParser(description="Анализатор текста")
    parser.add_argument("text", help="Текст для анализа")
    parser.add_argument("--words", action="store_true", help="Показать статистику слов")
    parser.add_argument("--chars", action="store_true", help="Показать статистику символов")
    parser.add_argument("--top", type=int, default=5, help="Топ N слов")
    return parser

# Симулируем вызов: python script.py "hello world" --words --top 3
sys.argv = ["script.py", "the quick brown fox jumps over the lazy dog", "--words", "--top", "3"]
parser = create_cli()
args = parser.parse_args()

text = args.text
words = text.lower().split()

if args.words:
    from collections import Counter
    word_counts = Counter(words)
    print(f"Слов всего: {len(words)}, уникальных: {len(word_counts)}")
    print(f"Топ-{args.top}:")
    for word, cnt in word_counts.most_common(args.top):
        print(f"  {word!r}: {cnt}")

if args.chars:
    letters = [c for c in text.lower() if c.isalpha()]
    print(f"Символов: {len(text)}, букв: {len(letters)}")
'''
    },
    {
      'title': 'pathlib: современная работа с файловой системой',
      'order': 2,
      'estimated_minutes': 45,
      'content': '''<h2>pathlib (Python 3.4+)</h2>
<p>pathlib.Path — объектно-ориентированный способ работы с путями файловой системы.
Заменяет <code>os.path</code>.</p>

<h3>Основные операции</h3>
<pre><code>from pathlib import Path

# Создание пути
p = Path("/home/user/documents")
p = Path.home() / "documents" / "report.txt"   # / — оператор конкатенации!

# Свойства
print(p.name)       # report.txt
print(p.stem)       # report (без расширения)
print(p.suffix)     # .txt
print(p.parent)     # /home/user/documents
print(p.parts)      # ('/', 'home', 'user', 'documents', 'report.txt')

# Проверки
print(p.exists())   # True/False
print(p.is_file())
print(p.is_dir())

# Создание директорий
output = Path("output/reports")
output.mkdir(parents=True, exist_ok=True)   # -p аналог mkdir

# Запись и чтение
path = Path("data.txt")
path.write_text("Hello, World!", encoding="utf-8")
content = path.read_text(encoding="utf-8")

# Итерация по директории
for file in Path(".").iterdir():
    if file.is_file(): print(file.name)

# Поиск файлов (glob)
py_files = list(Path(".").glob("**/*.py"))   # рекурсивно
</code></pre>

''' + table(
  ['pathlib','os.path аналог','Что делает'],
  [
    ['Path(a) / Path(b)','os.path.join(a, b)','Склейка путей'],
    ['p.exists()','os.path.exists(p)','Проверка существования'],
    ['p.is_file()','os.path.isfile(p)','Это файл?'],
    ['p.parent','os.path.dirname(p)','Родительская директория'],
    ['p.name','os.path.basename(p)','Имя файла'],
    ['p.suffix','os.path.splitext(p)[1]','Расширение файла'],
    ['p.stat().st_size','os.path.getsize(p)','Размер файла'],
    ['p.rename(q)','os.rename(p, q)','Переименование'],
    ['p.unlink()','os.remove(p)','Удаление файла'],
  ],
  'pathlib vs os.path'
),
      'code_example': '''from pathlib import Path
import tempfile
import os

# Работаем во временной директории
with tempfile.TemporaryDirectory() as tmpdir:
    base = Path(tmpdir)

    # Создать структуру директорий
    (base / "src").mkdir()
    (base / "tests").mkdir()
    (base / "docs").mkdir()

    # Создать файлы
    files = {
        "src/main.py":    "print('hello')",
        "src/utils.py":   "def helper(): pass",
        "tests/test_main.py": "import pytest",
        "docs/README.md": "# Project",
    }

    for path, content in files.items():
        file = base / path
        file.write_text(content, encoding="utf-8")

    print("Структура проекта:")
    for p in sorted(base.rglob("*")):
        if p.is_file():
            rel = p.relative_to(base)
            size = p.stat().st_size
            print(f"  {rel} ({size} bytes)")

    # Поиск Python файлов
    py_files = list(base.rglob("*.py"))
    print(f"\\nPython файлов: {len(py_files)}")

    # Прочитать содержимое
    for f in py_files:
        print(f"  {f.name}: {f.read_text()!r}")
'''
    },
  ]
},

]  # end MODULES


class Command(BaseCommand):
    help = 'Seed theory modules 31-40 (itertools, threading, type hints, patterns, etc.)'

    def handle(self, *args, **options):
        try:
            subject = Subject.objects.get(slug='python')
        except Subject.DoesNotExist:
            subject = Subject.objects.create(
                slug='python', title='Python', icon='fab fa-python',
                color='#3b82f6', order=1,
            )
            self.stdout.write('  Subject python создан')

        total_modules = 0
        total_lessons = 0

        for mod_data in MODULES:
            module, created = TheoryModule.objects.update_or_create(
                order=mod_data['order'],
                subject=subject,
                defaults={
                    'title':       mod_data['title'],
                    'description': mod_data['description'],
                    'icon':        mod_data['icon'],
                    'is_active':   True,
                },
            )
            action = 'создан' if created else 'обновлён'
            self.stdout.write(f'  Модуль {mod_data["order"]}: {mod_data["title"]} — {action}')
            total_modules += 1

            for lesson_data in mod_data['lessons']:
                lesson, lc = TheoryLesson.objects.update_or_create(
                    module=module,
                    order=lesson_data['order'],
                    defaults={
                        'title':             lesson_data['title'],
                        'content':           lesson_data['content'],
                        'code_example':      lesson_data.get('code_example', ''),
                        'estimated_minutes': lesson_data.get('estimated_minutes', 45),
                    },
                )
                total_lessons += 1

        self.stdout.write(self.style.SUCCESS(
            f'seed_theory_advanced1: {total_modules} modul., {total_lessons} urokov'
        ))
