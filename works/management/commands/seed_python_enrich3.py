# -*- coding: utf-8 -*-
"""
Третья волна расширения тонких уроков Python.
Запуск: python manage.py seed_python_enrich3
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject

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

ARROW_DEF = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'

def arr(x1, y1, x2, y2, color='#64748b', label=''):
    txt = f'<text x="{(x1+x2)//2}" y="{(y1+y2)//2-5}" text-anchor="middle" font-size="11" fill="{color}" font-family="sans-serif">{label}</text>' if label else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>' + txt


# ═══════════════════════════════════════════════════════════════════════════════
#  M10L2 — генераторы и comprehensions
# ═══════════════════════════════════════════════════════════════════════════════
M10L2 = (
    '<h2>Генераторы и comprehensions</h2>'
    '<p>Comprehensions — компактный способ создавать коллекции. '
    'Генераторы — ленивые последовательности, не хранящие все элементы в памяти.</p>'
    + '<h3>Все виды comprehensions</h3>'
    + code('python',
        '# List comprehension\n'
        'squares = [x**2 for x in range(10)]\n\n'
        '# Dict comprehension\n'
        'word_len = {word: len(word) for word in ["apple", "banana", "cherry"]}\n'
        '# {"apple": 5, "banana": 6, "cherry": 6}\n\n'
        '# Set comprehension\n'
        'unique_len = {len(word) for word in ["hi", "hello", "hey", "howdy"]}\n'
        '# {2, 5}\n\n'
        '# Generator expression (не хранит в памяти)\n'
        'total = sum(x**2 for x in range(1_000_000))  # нет квадратных скобок!')
    + '<h3>Генераторы с yield</h3>'
    + code('python',
        'def fibonacci():\n'
        '    """Бесконечная последовательность Фибоначчи."""\n'
        '    a, b = 0, 1\n'
        '    while True:\n'
        '        yield a          # приостановить и вернуть\n'
        '        a, b = b, a + b  # возобновить отсюда\n\n'
        '# Взять первые 10\n'
        'fib = fibonacci()\n'
        'first_10 = [next(fib) for _ in range(10)]\n'
        'print(first_10)  # [0,1,1,2,3,5,8,13,21,34]\n\n'
        '# Или через itertools\n'
        'import itertools\n'
        'print(list(itertools.islice(fibonacci(), 10)))')
    + '<h3>Реальный кейс: чтение огромного файла</h3>'
    + code('python',
        '# Плохо: весь файл в памяти\n'
        'lines = open("big_log.txt").readlines()   # может быть 10GB!\n'
        'errors = [l for l in lines if "ERROR" in l]\n\n'
        '# Хорошо: генератор читает построчно\n'
        'def read_errors(path):\n'
        '    with open(path, encoding="utf-8") as f:\n'
        '        for line in f:                    # файл как итератор\n'
        '            if "ERROR" in line:\n'
        '                yield line.strip()\n\n'
        'for error in read_errors("big_log.txt"):\n'
        '    print(error)')
    + tip('Генераторы используют O(1) памяти независимо от размера данных. '
          'Сервис обработки логов Splunk обрабатывает терабайты именно так: '
          'поток данных, а не загрузка всего в RAM.')
    + '<h3>itertools — батарейки для генераторов</h3>'
    + code('python',
        'import itertools\n\n'
        '# chain: склеить итераторы\n'
        'combined = list(itertools.chain([1,2], [3,4], [5]))\n'
        '# [1, 2, 3, 4, 5]\n\n'
        '# groupby: группировка\n'
        'data = [("A","Alice"),("A","Bob"),("B","Carol"),("B","Dave")]\n'
        'for group, items in itertools.groupby(data, key=lambda x: x[0]):\n'
        '    print(group, [i[1] for i in items])\n'
        '# A [\'Alice\', \'Bob\']\n'
        '# B [\'Carol\', \'Dave\']\n\n'
        '# product: декартово произведение\n'
        'for suit, rank in itertools.product("HDSC", "AKQJ"):\n'
        '    print(f"{rank}{suit}", end=" ")  # AH AD AS AC KH KD...')
    + table(['Конструкция', 'Тип', 'Память'],
        [['[x for x in ...]', 'list', 'O(n)'],
         ['{x for x in ...}', 'set', 'O(n)'],
         ['{k:v for ...}', 'dict', 'O(n)'],
         ['(x for x in ...)', 'generator', 'O(1)']])
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M29L3 — @property
# ═══════════════════════════════════════════════════════════════════════════════
M29L3 = (
    '<h2>@property: управляемые атрибуты</h2>'
    '<p>@property позволяет добавить логику к чтению/записи атрибута, '
    'не меняя публичный интерфейс класса. '
    'Это важно: если сначала был просто атрибут, а потом понадобилась валидация — '
    'весь старый код продолжает работать.</p>'
    + code('python',
        'class Temperature:\n'
        '    def __init__(self, celsius: float = 0):\n'
        '        self._celsius = celsius   # приватное хранилище\n\n'
        '    @property\n'
        '    def celsius(self) -> float:\n'
        '        """Геттер: вызывается при чтении t.celsius"""\n'
        '        return self._celsius\n\n'
        '    @celsius.setter\n'
        '    def celsius(self, value: float):\n'
        '        """Сеттер: вызывается при t.celsius = 37"""\n'
        '        if value < -273.15:\n'
        '            raise ValueError(f"Температура {value} ниже абсолютного нуля")\n'
        '        self._celsius = value\n\n'
        '    @property\n'
        '    def fahrenheit(self) -> float:\n'
        '        """Вычисляемый атрибут — только чтение"""\n'
        '        return self._celsius * 9/5 + 32\n\n'
        '    @celsius.deleter\n'
        '    def celsius(self):\n'
        '        self._celsius = 0\n\n'
        't = Temperature(100)\n'
        'print(t.celsius)     # 100\n'
        'print(t.fahrenheit)  # 212.0\n'
        't.celsius = -300     # ValueError: ниже абсолютного нуля')
    + '<h3>Кешированное свойство</h3>'
    + code('python',
        'from functools import cached_property\n\n'
        'class DataProcessor:\n'
        '    def __init__(self, data: list):\n'
        '        self.data = data\n\n'
        '    @cached_property\n'
        '    def statistics(self) -> dict:\n'
        '        """Вычисляется один раз, потом берётся из кеша."""\n'
        '        n = len(self.data)\n'
        '        mean = sum(self.data) / n\n'
        '        variance = sum((x - mean)**2 for x in self.data) / n\n'
        '        return {\n'
        '            "mean": mean,\n'
        '            "variance": variance,\n'
        '            "std": variance**0.5,\n'
        '            "min": min(self.data),\n'
        '            "max": max(self.data),\n'
        '        }\n\n'
        'dp = DataProcessor([1, 2, 3, 4, 5])\n'
        'print(dp.statistics)   # вычисляется\n'
        'print(dp.statistics)   # из кеша, мгновенно')
    + tip('@cached_property — из functools, Python 3.8+. '
          'Идеально для дорогих вычислений: статистика, парсинг, запросы к БД.')
    + '<h3>Slots + property: оптимизация памяти</h3>'
    + code('python',
        'class Point:\n'
        '    __slots__ = ("_x", "_y")  # нет __dict__, меньше памяти\n\n'
        '    def __init__(self, x, y):\n'
        '        self._x, self._y = float(x), float(y)\n\n'
        '    @property\n'
        '    def x(self): return self._x\n\n'
        '    @property\n'
        '    def y(self): return self._y\n\n'
        '    @property\n'
        '    def magnitude(self):\n'
        '        return (self._x**2 + self._y**2)**0.5\n\n'
        '# 40-50% меньше памяти по сравнению с обычным классом\n'
        'points = [Point(i, i) for i in range(1_000_000)]')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M31L2 — functools
# ═══════════════════════════════════════════════════════════════════════════════
M31L2 = (
    '<h2>functools: инструменты функционального программирования</h2>'
    + '<h3>lru_cache — мемоизация</h3>'
    + code('python',
        'from functools import lru_cache\n\n'
        '@lru_cache(maxsize=128)\n'
        'def expensive(n: int) -> int:\n'
        '    """Дорогое вычисление, кешируем результаты."""\n'
        '    import time; time.sleep(0.1)  # симуляция\n'
        '    return n * n\n\n'
        'expensive(10)   # 0.1 сек\n'
        'expensive(10)   # мгновенно (из кеша)\n'
        'expensive(20)   # 0.1 сек\n\n'
        'print(expensive.cache_info())\n'
        '# CacheInfo(hits=1, misses=2, maxsize=128, currsize=2)')
    + '<h3>partial — частичное применение</h3>'
    + code('python',
        'from functools import partial\n\n'
        'def power(base, exp):\n'
        '    return base ** exp\n\n'
        'square = partial(power, exp=2)\n'
        'cube   = partial(power, exp=3)\n\n'
        'print(square(5))  # 25\n'
        'print(cube(3))    # 27\n\n'
        '# Реальный пример: заготовить функцию с фиксированными параметрами\n'
        'import json\n'
        'json_ru = partial(json.dumps, ensure_ascii=False, indent=2)\n'
        'print(json_ru({"имя": "Алиса", "возраст": 30}))')
    + '<h3>reduce — свёртка последовательности</h3>'
    + code('python',
        'from functools import reduce\n\n'
        '# Произведение списка\n'
        'product = reduce(lambda acc, x: acc * x, [1,2,3,4,5])\n'
        'print(product)  # 120\n\n'
        '# Построить URL из частей\n'
        'parts = ["https://api.example.com", "users", "42", "orders"]\n'
        'url = reduce(lambda a, b: f"{a}/{b}", parts)\n'
        'print(url)  # https://api.example.com/users/42/orders\n\n'
        '# Объединить словари\n'
        'dicts = [{"a": 1}, {"b": 2}, {"c": 3}]\n'
        'merged = reduce(lambda acc, d: {**acc, **d}, dicts)\n'
        'print(merged)  # {"a": 1, "b": 2, "c": 3}')
    + '<h3>wraps — сохранение метаданных декоратора</h3>'
    + code('python',
        'from functools import wraps\n\n'
        'def validate(func):\n'
        '    @wraps(func)  # копирует __name__, __doc__, __annotations__\n'
        '    def wrapper(*args, **kwargs):\n'
        '        # валидация...\n'
        '        return func(*args, **kwargs)\n'
        '    return wrapper\n\n'
        '@validate\n'
        'def create_user(name: str, age: int) -> dict:\n'
        '    """Создать пользователя."""\n'
        '    return {"name": name, "age": age}\n\n'
        'print(create_user.__name__)  # "create_user" (без @wraps было бы "wrapper")\n'
        'print(create_user.__doc__)   # "Создать пользователя."')
    + tip('functools — стандартная библиотека. '
          '<code>lru_cache</code> используется повсюду: Django ORM, '
          'Werkzeug routing, SQLAlchemy reflection.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M32L2 — multiprocessing
# ═══════════════════════════════════════════════════════════════════════════════
M32L2 = (
    '<h2>multiprocessing: обход GIL для CPU-задач</h2>'
    '<p>GIL (Global Interpreter Lock) запрещает нескольким потокам Python '
    'выполнять байткод одновременно. '
    'Для CPU-интенсивных задач — multiprocessing запускает отдельные процессы '
    'с независимыми GIL.</p>'
    + diagram(660, 160, ARROW_DEF,
        svg_box(10, 60, 120, 40, '#e0f2fe', '#0284c7', 'Главный процесс'),
        arr(130, 80, 210, 50),
        arr(130, 80, 210, 110),
        svg_box(210, 20, 140, 40, '#dcfce7', '#16a34a', 'Worker 1\n(ядро CPU 1)'),
        svg_box(210, 90, 140, 40, '#dcfce7', '#16a34a', 'Worker 2\n(ядро CPU 2)'),
        arr(350, 40, 430, 70),
        arr(350, 110, 430, 90),
        svg_box(430, 60, 120, 40, '#fef9c3', '#ca8a04', 'Pool.map\nрезультаты'),
    )
    + code('python',
        'from multiprocessing import Pool\nimport time\n\n'
        'def cpu_task(n: int) -> int:\n'
        '    """Тяжёлое вычисление (симуляция)."""\n'
        '    return sum(i*i for i in range(n))\n\n'
        'numbers = [10_000_000] * 8    # 8 одинаковых задач\n\n'
        '# Однопоточно\n'
        'start = time.perf_counter()\n'
        'results = [cpu_task(n) for n in numbers]\n'
        'print(f"Последовательно: {time.perf_counter()-start:.2f} сек")\n\n'
        '# Параллельно (по числу ядер CPU)\n'
        'start = time.perf_counter()\n'
        'with Pool() as pool:\n'
        '    results = pool.map(cpu_task, numbers)\n'
        'print(f"Параллельно: {time.perf_counter()-start:.2f} сек")\n'
        '# Параллельно: ~2x-8x быстрее (зависит от числа ядер)')
    + '<h3>ProcessPoolExecutor — современный API</h3>'
    + code('python',
        'from concurrent.futures import ProcessPoolExecutor\nimport os\n\n'
        'def process_image(filename: str) -> str:\n'
        '    """Обработка одного изображения."""\n'
        '    # resize, filter, compress...\n'
        '    return f"processed_{filename}"\n\n'
        'images = [f"img_{i:04d}.jpg" for i in range(100)]\n\n'
        'with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:\n'
        '    results = list(executor.map(process_image, images))\n\n'
        'print(f"Обработано: {len(results)} изображений")')
    + '<h3>Общая память и очереди</h3>'
    + code('python',
        'from multiprocessing import Process, Queue\n\n'
        'def worker(q: Queue, task: str):\n'
        '    result = task.upper()   # обработка\n'
        '    q.put(result)           # отправить результат\n\n'
        'queue = Queue()\n'
        'tasks = ["hello", "world", "python"]\n\n'
        'processes = [Process(target=worker, args=(queue, t)) for t in tasks]\n'
        'for p in processes: p.start()\n'
        'for p in processes: p.join()\n\n'
        'results = [queue.get() for _ in tasks]\n'
        'print(results)  # ["HELLO", "WORLD", "PYTHON"] (порядок может отличаться)')
    + warn('Не используйте multiprocessing для I/O-задач (HTTP-запросы, файлы, БД). '
           'Там лучше asyncio или threading — они дешевле по ресурсам.')
    + table(['Задача', 'Инструмент', 'Почему'],
        [['CPU-тяжёлые вычисления', 'multiprocessing', 'Обходит GIL'],
         ['I/O: HTTP, файлы, БД', 'asyncio / threading', 'Дешевле по памяти'],
         ['Простые скрипты', 'subprocess', 'Запустить другую программу']])
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M32L3 — asyncio
# ═══════════════════════════════════════════════════════════════════════════════
M32L3 = (
    '<h2>asyncio: асинхронное программирование</h2>'
    '<p>asyncio позволяет выполнять тысячи I/O-операций "одновременно" '
    'в одном потоке через кооперативную многозадачность. '
    'Discord, Telegram Bot API, FastAPI — все построены на asyncio.</p>'
    + code('python',
        'import asyncio\n\n'
        'async def fetch_user(user_id: int) -> dict:\n'
        '    """Симуляция HTTP-запроса."""\n'
        '    await asyncio.sleep(1)     # "жди 1 сек, пока другие работают"\n'
        '    return {"id": user_id, "name": f"User{user_id}"}\n\n'
        'async def main():\n'
        '    # Последовательно: 3 секунды\n'
        '    # u1 = await fetch_user(1)\n'
        '    # u2 = await fetch_user(2)\n'
        '    # u3 = await fetch_user(3)\n\n'
        '    # Параллельно: 1 секунда\n'
        '    users = await asyncio.gather(\n'
        '        fetch_user(1),\n'
        '        fetch_user(2),\n'
        '        fetch_user(3),\n'
        '    )\n'
        '    for user in users:\n'
        '        print(user)\n\n'
        'asyncio.run(main())')
    + '<h3>aiohttp — асинхронные HTTP-запросы</h3>'
    + code('python',
        'import asyncio, aiohttp\n\n'
        'async def fetch(session, url: str) -> str:\n'
        '    async with session.get(url) as resp:\n'
        '        return await resp.text()\n\n'
        'async def fetch_all(urls: list) -> list:\n'
        '    async with aiohttp.ClientSession() as session:\n'
        '        tasks = [fetch(session, url) for url in urls]\n'
        '        return await asyncio.gather(*tasks)\n\n'
        'urls = [\n'
        '    "https://jsonplaceholder.typicode.com/posts/1",\n'
        '    "https://jsonplaceholder.typicode.com/posts/2",\n'
        '    "https://jsonplaceholder.typicode.com/posts/3",\n'
        ']\n\n'
        '# 3 запроса за время одного!\n'
        'results = asyncio.run(fetch_all(urls))')
    + '<h3>Задачи и таймауты</h3>'
    + code('python',
        'import asyncio\n\n'
        'async def slow_operation():\n'
        '    await asyncio.sleep(10)\n'
        '    return "done"\n\n'
        'async def main():\n'
        '    try:\n'
        '        # Таймаут 3 секунды\n'
        '        result = await asyncio.wait_for(slow_operation(), timeout=3.0)\n'
        '    except asyncio.TimeoutError:\n'
        '        print("Превышено время ожидания!")\n\n'
        '    # Отменяемая задача\n'
        '    task = asyncio.create_task(slow_operation())\n'
        '    await asyncio.sleep(1)\n'
        '    task.cancel()    # отменить до завершения\n'
        '    try:\n'
        '        await task\n'
        '    except asyncio.CancelledError:\n'
        '        print("Задача отменена")')
    + tip('asyncio — не про параллелизм, а про конкурентность. '
          'Пока одна корутина ждёт I/O, другие работают. '
          'Один процесс, один поток, тысячи "параллельных" задач.')
    + diagram(620, 120, ARROW_DEF,
        svg_box(10, 40, 110, 40, '#e0f2fe', '#0284c7', 'Event Loop'),
        arr(120, 60, 180, 40),
        arr(120, 60, 180, 80),
        svg_box(180, 20, 130, 40, '#dcfce7', '#16a34a', 'coroutine 1\nawait sleep'),
        svg_box(180, 70, 130, 40, '#fef9c3', '#ca8a04', 'coroutine 2\nawait read'),
        arr(310, 40, 380, 60),
        arr(310, 90, 380, 60),
        svg_box(380, 40, 130, 40, '#f3e8ff', '#9333ea', 'I/O ready\n-> resume'),
    )
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M33L2 — dataclasses
# ═══════════════════════════════════════════════════════════════════════════════
M33L2 = (
    '<h2>dataclasses: автоматическая генерация __init__, __repr__, __eq__</h2>'
    '<p>dataclass — декоратор, который генерирует boilerplate-код класса. '
    'Python 3.7+. Замена NamedTuple для изменяемых данных.</p>'
    + code('python',
        'from dataclasses import dataclass, field\n\n'
        '@dataclass\n'
        'class Product:\n'
        '    name: str\n'
        '    price: float\n'
        '    quantity: int = 0\n'
        '    tags: list[str] = field(default_factory=list)\n\n'
        '# Автоматически генерируется:\n'
        '# __init__(self, name, price, quantity=0, tags=None)\n'
        '# __repr__\n'
        '# __eq__\n\n'
        'p1 = Product("Apple", 1.5, 100, ["fruit", "fresh"])\n'
        'p2 = Product("Apple", 1.5, 100, ["fruit", "fresh"])\n\n'
        'print(p1)          # Product(name=\'Apple\', price=1.5, ...)\n'
        'print(p1 == p2)    # True  (сравнение по полям)')
    + warn('Никогда не используйте изменяемый объект как default: '
           '<code>tags: list = []</code> — всем экземплярам достанется ОДИН и тот же список! '
           'Используйте <code>field(default_factory=list)</code>.')
    + '<h3>frozen=True — неизменяемый dataclass</h3>'
    + code('python',
        '@dataclass(frozen=True)  # как NamedTuple, но с наследованием\n'
        'class Point:\n'
        '    x: float\n'
        '    y: float\n\n'
        '    @property\n'
        '    def magnitude(self) -> float:\n'
        '        return (self.x**2 + self.y**2)**0.5\n\n'
        'p = Point(3.0, 4.0)\n'
        'print(p.magnitude)    # 5.0\n'
        'p.x = 10              # FrozenInstanceError!')
    + '<h3>order=True — сортировка</h3>'
    + code('python',
        '@dataclass(order=True)\n'
        'class Version:\n'
        '    major: int\n'
        '    minor: int\n'
        '    patch: int\n\n'
        'versions = [Version(1,2,3), Version(2,0,0), Version(1,10,0)]\n'
        'print(sorted(versions))\n'
        '# [Version(1,2,3), Version(1,10,0), Version(2,0,0)]')
    + '<h3>post_init — дополнительная инициализация</h3>'
    + code('python',
        'from dataclasses import dataclass\nfrom datetime import datetime\n\n'
        '@dataclass\n'
        'class Order:\n'
        '    customer: str\n'
        '    total: float\n'
        '    created_at: datetime = field(default_factory=datetime.now)\n'
        '    order_id: str = field(init=False)  # не в __init__\n\n'
        '    def __post_init__(self):\n'
        '        import uuid\n'
        '        self.order_id = str(uuid.uuid4())[:8]\n'
        '        if self.total < 0:\n'
        '            raise ValueError("Сумма не может быть отрицательной")\n\n'
        'o = Order("Alice", 299.99)\n'
        'print(o.order_id)  # например "a3f1c2d4"\n'
        'print(o.created_at.strftime("%H:%M:%S"))')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M34L1 — context managers
# ═══════════════════════════════════════════════════════════════════════════════
M34L1 = (
    '<h2>with-оператор и менеджеры контекста</h2>'
    '<p>Менеджер контекста гарантирует выполнение "завершающего" кода, '
    'даже если произошло исключение. '
    'Открыть файл → обработать → закрыть. Получить соединение → работать → вернуть в пул.</p>'
    + code('python',
        '# Без with — опасно (файл не закроется при исключении)\n'
        'f = open("data.txt")\n'
        'data = f.read()       # если здесь ошибка...\n'
        'f.close()             # ...это не выполнится!\n\n'
        '# С with — безопасно\n'
        'with open("data.txt", encoding="utf-8") as f:\n'
        '    data = f.read()   # файл закроется в любом случае')
    + '<h3>Свой менеджер контекста через __enter__/__exit__</h3>'
    + code('python',
        'import time\n\n'
        'class Timer:\n'
        '    """Измеряет время выполнения блока кода."""\n\n'
        '    def __enter__(self):\n'
        '        self.start = time.perf_counter()\n'
        '        return self  # доступен как `t` в `with Timer() as t`\n\n'
        '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
        '        self.elapsed = time.perf_counter() - self.start\n'
        '        print(f"Прошло: {self.elapsed:.4f} сек")\n'
        '        return False  # False = не подавлять исключение\n\n'
        'with Timer() as t:\n'
        '    result = sum(i**2 for i in range(1_000_000))\n'
        '# Прошло: 0.0823 сек\n'
        'print(t.elapsed)')
    + '<h3>contextlib.contextmanager — через генератор</h3>'
    + code('python',
        'from contextlib import contextmanager\nimport sqlite3\n\n'
        '@contextmanager\n'
        'def db_transaction(db_path: str):\n'
        '    """Менеджер транзакции БД."""\n'
        '    conn = sqlite3.connect(db_path)\n'
        '    try:\n'
        '        yield conn          # всё до yield — __enter__\n'
        '        conn.commit()       # успех\n'
        '    except Exception:\n'
        '        conn.rollback()     # откат при ошибке\n'
        '        raise\n'
        '    finally:\n'
        '        conn.close()\n\n'
        'with db_transaction("shop.db") as conn:\n'
        '    conn.execute("INSERT INTO orders VALUES (?,?,?)", (1,"Alice",299.99))\n'
        '    conn.execute("UPDATE stock SET qty=qty-1 WHERE id=?", (42,))\n'
        '    # Если второй запрос упадёт — первый тоже откатится')
    + '<h3>Вложенные и множественные менеджеры</h3>'
    + code('python',
        '# Python 3.10+: скобочный синтаксис\n'
        'with (\n'
        '    open("input.txt")  as fin,\n'
        '    open("output.txt", "w") as fout,\n'
        '):\n'
        '    for line in fin:\n'
        '        fout.write(line.upper())')
    + tip('Правило: всё, что нужно "освободить" после использования, '
          'должно быть менеджером контекста: файлы, соединения, '
          'блокировки, временные директории, сетевые сессии.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M37L1 — SQLite
# ═══════════════════════════════════════════════════════════════════════════════
M37L1 = (
    '<h2>sqlite3: встроенная база данных</h2>'
    '<p>SQLite — файловая SQL-база данных без сервера. '
    'Входит в стандартную библиотеку Python. '
    'Используется в браузерах, мобильных приложениях, Django (по умолчанию), '
    'встроена в iOS и Android.</p>'
    + code('python',
        'import sqlite3\n\n'
        '# Подключение (или создание файла)\n'
        'conn = sqlite3.connect("school.db")\n'
        'conn.row_factory = sqlite3.Row    # строки как dict-подобные объекты\n'
        'cur = conn.cursor()\n\n'
        '# Создание таблицы\n'
        'cur.execute("""\n'
        '    CREATE TABLE IF NOT EXISTS students (\n'
        '        id      INTEGER PRIMARY KEY AUTOINCREMENT,\n'
        '        name    TEXT NOT NULL,\n'
        '        grade   REAL,\n'
        '        subject TEXT\n'
        '    )\n'
        '""")\n\n'
        '# Вставка — ВСЕГДА параметры, никогда f-строки!\n'
        'students = [\n'
        '    ("Alice", 95.0, "Math"),\n'
        '    ("Bob",   87.5, "Physics"),\n'
        '    ("Carol", 91.0, "Math"),\n'
        ']\n'
        'cur.executemany("INSERT INTO students (name, grade, subject) VALUES (?,?,?)", students)\n'
        'conn.commit()')
    + warn('НИКОГДА не вставляйте данные через f-строку или %-форматирование: '
           '<code>f"INSERT INTO ... VALUES ({name})"</code> — это SQL-инъекция! '
           'Всегда используйте параметры <code>?</code>.')
    + '<h3>SELECT, UPDATE, DELETE</h3>'
    + code('python',
        '# Выборка\n'
        'cur.execute("SELECT * FROM students WHERE subject=?", ("Math",))\n'
        'math_students = cur.fetchall()\n'
        'for s in math_students:\n'
        '    print(f"{s[\'name\']}: {s[\'grade\']}")\n\n'
        '# Агрегация\n'
        'cur.execute("SELECT subject, AVG(grade) as avg FROM students GROUP BY subject")\n'
        'for row in cur.fetchall():\n'
        '    print(f"{row[\'subject\']}: средний балл {row[\'avg\']:.1f}")\n\n'
        '# Обновление\n'
        'cur.execute("UPDATE students SET grade=? WHERE name=?", (98.0, "Alice"))\n\n'
        '# Удаление\n'
        'cur.execute("DELETE FROM students WHERE grade < ?", (70.0,))\n'
        'conn.commit()\n'
        'conn.close()')
    + '<h3>Context manager для транзакций</h3>'
    + code('python',
        '# Рекомендуемый способ\n'
        'with sqlite3.connect("school.db") as conn:\n'
        '    conn.row_factory = sqlite3.Row\n'
        '    # автоматический commit/rollback\n'
        '    conn.execute("INSERT INTO students VALUES (?,?,?,?)", (None,"Dave",88,"CS"))\n'
        '    rows = conn.execute("SELECT COUNT(*) as n FROM students").fetchone()\n'
        '    print(f"Всего студентов: {rows[\'n\']}")')
    + '<h3>Индексы для производительности</h3>'
    + code('python',
        '# Без индекса: O(n) — полный перебор\n'
        '# С индексом: O(log n) — B-tree\n'
        'conn.execute("CREATE INDEX IF NOT EXISTS idx_subject ON students(subject)")\n\n'
        '# EXPLAIN покажет план запроса\n'
        'cur.execute("EXPLAIN QUERY PLAN SELECT * FROM students WHERE subject=?", ("Math",))\n'
        'print(cur.fetchone())')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M38L1 — requests HTTP
# ═══════════════════════════════════════════════════════════════════════════════
M38L1 = (
    '<h2>requests: HTTP-клиент для Python</h2>'
    '<p>requests — самая популярная библиотека Python (500M+ загрузок в месяц). '
    'Делает работу с HTTP API простой и человекочитаемой.</p>'
    + code('python',
        'import requests\n\n'
        '# GET-запрос\n'
        'response = requests.get(\n'
        '    "https://jsonplaceholder.typicode.com/users/1",\n'
        '    timeout=10  # всегда задавайте timeout!\n'
        ')\n\n'
        'response.raise_for_status()  # бросит HTTPError при 4xx/5xx\n\n'
        'user = response.json()\n'
        'print(f"{user[\'name\']} ({user[\'email\']})")\n'
        'print(f"Статус: {response.status_code}")  # 200')
    + '<h3>POST, заголовки, аутентификация</h3>'
    + code('python',
        '# POST с JSON-телом\n'
        'new_post = {\n'
        '    "title": "Тестовый пост",\n'
        '    "body": "Содержимое...",\n'
        '    "userId": 1\n'
        '}\n'
        'r = requests.post(\n'
        '    "https://jsonplaceholder.typicode.com/posts",\n'
        '    json=new_post,            # автоматически добавит Content-Type: application/json\n'
        '    headers={"X-Custom": "value"},\n'
        '    timeout=10\n'
        ')\n'
        'print(r.status_code)    # 201 Created\n'
        'print(r.json())         # {"id": 101, "title": ..., ...}\n\n'
        '# Bearer token авторизация\n'
        'token = "eyJhbGciOiJIUzI1NiIs..."\n'
        'r = requests.get(\n'
        '    "https://api.github.com/user",\n'
        '    headers={"Authorization": f"Bearer {token}"},\n'
        '    timeout=10\n'
        ')')
    + '<h3>Session — переиспользование соединений</h3>'
    + code('python',
        '# Session переиспользует TCP-соединение и куки\n'
        'with requests.Session() as session:\n'
        '    session.headers.update({"User-Agent": "MyApp/1.0"})\n'
        '    session.auth = ("username", "password")\n\n'
        '    # Все запросы используют одно соединение\n'
        '    for user_id in range(1, 11):\n'
        '        r = session.get(f"https://api.example.com/users/{user_id}", timeout=5)\n'
        '        print(r.json()["name"])')
    + '<h3>Обработка ошибок</h3>'
    + code('python',
        'from requests.exceptions import Timeout, ConnectionError, HTTPError\n\n'
        'def safe_get(url: str) -> dict | None:\n'
        '    try:\n'
        '        r = requests.get(url, timeout=5)\n'
        '        r.raise_for_status()   # 4xx/5xx -> HTTPError\n'
        '        return r.json()\n'
        '    except Timeout:\n'
        '        print(f"Таймаут: {url}")\n'
        '    except ConnectionError:\n'
        '        print(f"Нет соединения: {url}")\n'
        '    except HTTPError as e:\n'
        '        print(f"HTTP ошибка {e.response.status_code}: {url}")\n'
        '    return None')
    + tip('Всегда задавайте <code>timeout</code>. Без него запрос может висеть '
          'вечно и блокировать поток. '
          'Рекомендуемое значение: 5-30 секунд в зависимости от API.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M39L1 — regex
# ═══════════════════════════════════════════════════════════════════════════════
M39L1 = (
    '<h2>Регулярные выражения: мощный поиск в тексте</h2>'
    '<p>Regex — мини-язык для описания паттернов в строках. '
    'Валидация email/телефонов, парсинг логов, замена текста.</p>'
    + table(['Символ', 'Значение', 'Пример'],
        [[r'<code>.</code>', 'Любой символ (кроме \\n)', r'<code>a.c</code> → abc, a1c'],
         [r'<code>\d</code>', 'Цифра [0-9]', r'<code>\d{4}</code> → 2025'],
         [r'<code>\w</code>', 'Буква/цифра/_ ', r'<code>\w+</code> → hello'],
         [r'<code>\s</code>', 'Пробел/таб/\\n', r'<code>\s+</code> → пробелы'],
         [r'<code>*</code>', '0 или более', r'<code>go*gle</code>'],
         [r'<code>+</code>', '1 или более', r'<code>\d+</code>'],
         [r'<code>?</code>', '0 или 1', r'<code>colou?r</code>'],
         [r'<code>^...$</code>', 'Начало/конец', r'<code>^\d{5}$</code>']])
    + code('python',
        'import re\n\n'
        '# Основные функции\n'
        'text = "Звоните по +7 (999) 123-45-67 или +7-800-555-35-35"\n\n'
        '# search — найти первое совпадение\n'
        'match = re.search(r"\\+7[\\s\\-\\(]*\\d{3}[\\s\\-\\)]*\\d{3}[\\s\\-]\\d{2}[\\s\\-]\\d{2}", text)\n'
        'if match:\n'
        '    print(match.group())   # +7 (999) 123-45-67\n\n'
        '# findall — все совпадения\n'
        'phones = re.findall(r"\\+7[\\d\\s\\-\\(\\)]{10,14}", text)\n'
        'print(phones)\n\n'
        '# sub — замена\n'
        'clean = re.sub(r"[\\s\\-\\(\\)]", "", "+7 (999) 123-45-67")\n'
        'print(clean)  # +79991234567')
    + '<h3>Именованные группы</h3>'
    + code('python',
        '# Парсинг строки лога\n'
        'log_line = "2025-05-29 14:30:15 ERROR main: Connection refused"\n\n'
        'pattern = r"""(?P<date>\\d{4}-\\d{2}-\\d{2})\\ \n'
        '               (?P<time>\\d{2}:\\d{2}:\\d{2})\\ \n'
        '               (?P<level>\\w+)\\ \n'
        '               (?P<module>\\w+):\\ \n'
        '               (?P<message>.+)"""\n\n'
        'm = re.match(pattern, log_line, re.VERBOSE)\n'
        'if m:\n'
        '    print(m.group("level"))    # ERROR\n'
        '    print(m.group("message"))  # Connection refused\n'
        '    print(m.groupdict())       # весь словарь')
    + '<h3>Компиляция для производительности</h3>'
    + code('python',
        '# Если паттерн используется много раз — скомпилируйте\n'
        'EMAIL_RE = re.compile(\n'
        '    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"\n'
        ')\n\n'
        'emails = ["alice@example.com", "not-an-email", "bob@gmail.com"]\n'
        'valid = [e for e in emails if EMAIL_RE.fullmatch(e)]\n'
        'print(valid)  # ["alice@example.com", "bob@gmail.com"]')
    + tip('Используйте <a href="https://regex101.com" target="_blank">regex101.com</a> '
          'для тестирования паттернов с подсветкой и объяснениями.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M40L2 — pathlib
# ═══════════════════════════════════════════════════════════════════════════════
M40L2 = (
    '<h2>pathlib: объектная работа с путями</h2>'
    '<p>pathlib.Path — современная замена os.path. '
    'Читаемый синтаксис через оператор <code>/</code>, кроссплатформенный.</p>'
    + code('python',
        'from pathlib import Path\n\n'
        'p = Path("/home/user/projects/myapp")\n\n'
        '# Свойства пути\n'
        'print(p.name)        # "myapp"\n'
        'print(p.stem)        # "myapp" (без расширения)\n'
        'print(p.suffix)      # "" (нет расширения)\n'
        'print(p.parent)      # /home/user/projects\n'
        'print(p.parts)       # ("/", "home", "user", "projects", "myapp")\n\n'
        '# Конкатенация через /\n'
        'config = p / "config" / "settings.json"\n'
        'print(config)        # /home/user/projects/myapp/config/settings.json\n\n'
        '# Работа с текущей директорией\n'
        'cwd = Path.cwd()\n'
        'home = Path.home()\n'
        'print(home / "Downloads")')
    + '<h3>Поиск файлов</h3>'
    + code('python',
        'project = Path(".")\n\n'
        '# Все .py файлы в текущей папке\n'
        'py_files = list(project.glob("*.py"))\n\n'
        '# Рекурсивно все .py файлы\n'
        'all_py = list(project.rglob("*.py"))\n'
        'print(f"Python файлов: {len(all_py)}")\n\n'
        '# Фильтрация\n'
        'test_files = [f for f in project.rglob("test_*.py")]\n'
        'for f in test_files:\n'
        '    size = f.stat().st_size\n'
        '    print(f"{f.name}: {size} байт")')
    + '<h3>Чтение/запись через Path</h3>'
    + code('python',
        'config_path = Path("config.json")\n\n'
        '# Запись\n'
        'config_path.write_text(\'{"debug": true}\', encoding="utf-8")\n\n'
        '# Чтение\n'
        'import json\n'
        'config = json.loads(config_path.read_text(encoding="utf-8"))\n\n'
        '# Создание директорий\n'
        'logs_dir = Path("logs/2025/05")\n'
        'logs_dir.mkdir(parents=True, exist_ok=True)   # mkdir -p\n\n'
        '# Безопасное удаление\n'
        'temp = Path("temp_file.tmp")\n'
        'if temp.exists():\n'
        '    temp.unlink()')
    + '<h3>Безопасность: проверка выхода за пределы директории</h3>'
    + code('python',
        '# Защита от path traversal атаки: ../../etc/passwd\n'
        'BASE_DIR = Path("/var/www/uploads")\n\n'
        'def safe_path(filename: str) -> Path:\n'
        '    target = (BASE_DIR / filename).resolve()  # нормализация\n'
        '    if not target.is_relative_to(BASE_DIR):\n'
        '        raise ValueError(f"Путь {filename} выходит за пределы директории")\n'
        '    return target\n\n'
        'safe_path("image.jpg")     # OK\n'
        'safe_path("../../etc/passwd")  # ValueError!')
    + warn('Path traversal — реальная уязвимость. Всегда проверяйте, '
           'что итоговый путь находится внутри разрешённой директории.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M41L2 — BeautifulSoup
# ═══════════════════════════════════════════════════════════════════════════════
M41L2 = (
    '<h2>BeautifulSoup: парсинг HTML</h2>'
    '<p>BeautifulSoup парсит HTML/XML и предоставляет удобный API для навигации. '
    'Используется для веб-скрапинга, анализа данных с сайтов.</p>'
    + code('python',
        'from bs4 import BeautifulSoup\nimport requests\n\n'
        'html = """\n'
        '<html><body>\n'
        '  <h1 class="title">Каталог книг</h1>\n'
        '  <div class="book" data-id="1">\n'
        '    <h2>Python Crash Course</h2>\n'
        '    <span class="price">$29.99</span>\n'
        '    <span class="rating">4.8</span>\n'
        '  </div>\n'
        '  <div class="book" data-id="2">\n'
        '    <h2>Clean Code</h2>\n'
        '    <span class="price">$34.99</span>\n'
        '    <span class="rating">4.7</span>\n'
        '  </div>\n'
        '</body></html>\n'
        '"""\n\n'
        'soup = BeautifulSoup(html, "html.parser")\n\n'
        '# Найти один элемент\n'
        'title = soup.find("h1").text\n'
        'print(title)   # "Каталог книг"\n\n'
        '# Найти все элементы\n'
        'books = soup.find_all("div", class_="book")\n'
        'for book in books:\n'
        '    name  = book.find("h2").text\n'
        '    price = book.find("span", class_="price").text\n'
        '    bid   = book["data-id"]\n'
        '    print(f"[{bid}] {name}: {price}")')
    + '<h3>CSS-селекторы</h3>'
    + code('python',
        '# select — CSS-селекторы (мощнее find_all)\n'
        'prices = [s.text for s in soup.select(".book .price")]\n'
        'print(prices)   # ["$29.99", "$34.99"]\n\n'
        '# Атрибут\n'
        'ids = [b["data-id"] for b in soup.select("div[data-id]")]\n'
        'print(ids)      # ["1", "2"]')
    + '<h3>Реальный скрапинг с requests</h3>'
    + code('python',
        'import requests\nfrom bs4 import BeautifulSoup\n\n'
        'def scrape_quotes(url: str) -> list[dict]:\n'
        '    """Собрать цитаты с сайта."""\n'
        '    headers = {"User-Agent": "Mozilla/5.0"}\n'
        '    r = requests.get(url, headers=headers, timeout=10)\n'
        '    r.raise_for_status()\n\n'
        '    soup = BeautifulSoup(r.text, "html.parser")\n'
        '    quotes = []\n\n'
        '    for q in soup.select(".quote"):\n'
        '        text   = q.select_one(".text").text.strip()\n'
        '        author = q.select_one(".author").text.strip()\n'
        '        tags   = [t.text for t in q.select(".tag")]\n'
        '        quotes.append({"text": text, "author": author, "tags": tags})\n\n'
        '    return quotes\n\n'
        '# quotes = scrape_quotes("http://quotes.toscrape.com/")')
    + warn('Перед скрапингом проверяйте robots.txt и Terms of Service сайта. '
           'Делайте паузы между запросами (<code>time.sleep(1)</code>). '
           'Многие сайты блокируют агрессивные скрапперы.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  M43L1 — profiling
# ═══════════════════════════════════════════════════════════════════════════════
M43L1 = (
    '<h2>Профилирование: найти узкое место</h2>'
    '<p>Правило оптимизации: сначала измерь, потом оптимизируй. '
    '80% времени программа проводит в 20% кода (правило Парето). '
    'Профилировщик покажет где именно.</p>'
    + '<h3>timeit — точный замер маленьких фрагментов</h3>'
    + code('python',
        'import timeit\n\n'
        '# Сравниваем два способа склеить строки\n'
        'join_time = timeit.timeit(\n'
        '    \'"\".join(str(i) for i in range(100))\',\n'
        '    number=10_000\n'
        ')\n'
        'concat_time = timeit.timeit(\n'
        '    \'result = ""; [result := result + str(i) for i in range(100)]\',\n'
        '    number=10_000\n'
        ')\n'
        'print(f"join:   {join_time:.3f} сек")\n'
        'print(f"concat: {concat_time:.3f} сек")\n'
        '# join:   0.045 сек  <-- в 10x быстрее\n'
        '# concat: 0.410 сек')
    + '<h3>cProfile — полное профилирование</h3>'
    + code('python',
        'import cProfile, pstats, io\n\n'
        'def slow_sort(data):\n'
        '    """Пузырьковая сортировка для примера."""\n'
        '    n = len(data)\n'
        '    for i in range(n):\n'
        '        for j in range(0, n-i-1):\n'
        '            if data[j] > data[j+1]:\n'
        '                data[j], data[j+1] = data[j+1], data[j]\n\n'
        'def main():\n'
        '    import random\n'
        '    data = [random.randint(0, 10000) for _ in range(5000)]\n'
        '    slow_sort(data)\n\n'
        '# Профилирование\n'
        'pr = cProfile.Profile()\n'
        'pr.enable()\n'
        'main()\n'
        'pr.disable()\n\n'
        'stats = pstats.Stats(pr)\n'
        'stats.sort_stats("cumulative")\n'
        'stats.print_stats(10)  # топ 10 самых медленных функций')
    + '<h3>line_profiler — по строкам</h3>'
    + code('bash',
        'pip install line_profiler\n\n'
        '# Добавьте @profile к функции и запустите:\n'
        'kernprof -l -v my_script.py\n\n'
        '# Line #  Hits   Time   Per Hit   % Time  Line Contents\n'
        '# ======================================================\n'
        '#     5  4999  45234     9.0      72.3    if data[j] > data[j+1]:')
    + '<h3>memory_profiler — утечки памяти</h3>'
    + code('python',
        'from memory_profiler import profile\n\n'
        '@profile\n'
        'def leaky_function():\n'
        '    big_list = [i**2 for i in range(100_000)]  # 3.8 МБ\n'
        '    result = sum(big_list)\n'
        '    # big_list не освобождается до конца функции\n'
        '    return result\n\n'
        'leaky_function()\n'
        '# Line  Mem usage  Increment   Line Contents\n'
        '# 3     15.0 MiB    +3.8 MiB   big_list = [...]')
    + tip('Альтернатива memory_profiler: <code>tracemalloc</code> из стандартной библиотеки. '
          'Показывает топ N строк кода по выделению памяти.')
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PATCHES
# ═══════════════════════════════════════════════════════════════════════════════
PATCHES = {
    (10, 2):  M10L2,
    (29, 3):  M29L3,
    (31, 2):  M31L2,
    (32, 2):  M32L2,
    (32, 3):  M32L3,
    (33, 2):  M33L2,
    (34, 1):  M34L1,
    (37, 1):  M37L1,
    (38, 1):  M38L1,
    (39, 1):  M39L1,
    (40, 2):  M40L2,
    (41, 2):  M41L2,
    (43, 1):  M43L1,
}


class Command(BaseCommand):
    help = 'Третья волна расширения тонких уроков Python'

    def handle(self, *args, **options):
        try:
            subject = Subject.objects.get(slug='python')
        except Subject.DoesNotExist:
            self.stderr.write('Subject python not found')
            return

        modules = list(TheoryModule.objects.filter(subject=subject).order_by('order'))
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
            lesson = TheoryLesson.objects.filter(module=mod_map[mo], order=lo).order_by('id').first()
            if not lesson:
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
