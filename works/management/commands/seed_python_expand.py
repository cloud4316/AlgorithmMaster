# -*- coding: utf-8 -*-
"""
Расширение тонких Python-модулей: добавляет 2-3 урока в каждый модуль с 1-2 уроками.
Запуск: python manage.py seed_python_expand
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject


def tip(t):   return f'<div class="tip">&#128161; {t}</div>'
def warn(t):  return f'<div class="warning">&#9888; {t}</div>'
def info(t):  return f'<div class="info">&#8505; {t}</div>'

def code(lang, src):
    return f'<pre><code class="language-{lang}">{src}</code></pre>'

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def svg_box(x, y, w, h, fill, stroke, label, fs=12, tc='#1e293b'):
    lh = fs + 4
    lines = label.split('\n')
    y0 = y + h // 2 - (lh * len(lines)) // 2 + fs
    spans = ''.join(f'<tspan x="{x + w // 2}" dy="{0 if i == 0 else lh}">{l}</tspan>'
                    for i, l in enumerate(lines))
    r = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    t = (f'<text x="{x + w // 2}" y="{y0}" text-anchor="middle" font-size="{fs}" '
         f'fill="{tc}" font-family="sans-serif">{spans}</text>')
    return r + t

ARROW = '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'

def arr(x1, y1, x2, y2, color='#64748b', label=''):
    txt = (f'<text x="{(x1+x2)//2}" y="{(y1+y2)//2-5}" text-anchor="middle" '
           f'font-size="11" fill="{color}" font-family="sans-serif">{label}</text>') if label else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="1.5" marker-end="url(#ah)"/>' + txt)

def diagram(w, h, *items):
    inner = ''.join(items)
    return (f'<div style="overflow-x:auto;margin:1rem 0">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto">'
            f'{inner}</svg></div>')


# ── Данные уроков ────────────────────────────────────────────────────────────────
# Формат: (module_title_keyword, [( lesson_title, lesson_content ), ...])

LESSONS = []


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Словари
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('Словари', [

    ('Методы словарей и вложенные структуры',
     '<h2>Методы словарей и вложенные структуры</h2>'
     '<p>Словарь — самая важная структура данных Python. Здесь разбираем все ключевые методы '
     'и учимся работать с вложенными данными (JSON-подобные структуры).</p>'
     '<h3>Все методы словаря</h3>'
     + table(['Метод', 'Что делает', 'Пример'],
             [['d.get(k, default)', 'Значение по ключу без KeyError', 'd.get("x", 0)'],
              ['d.setdefault(k, v)', 'Добавить если нет ключа', 'd.setdefault("count", 0)'],
              ['d.update(other)', 'Обновить/добавить пары', 'd.update({"b": 2})'],
              ['d.pop(k, default)', 'Удалить и вернуть', 'd.pop("x", None)'],
              ['d.items()', 'Пары (ключ, значение)', 'for k, v in d.items()'],
              ['d.keys() / d.values()', 'Ключи / значения', 'list(d.keys())'],
              ['d | other', 'Слияние (Python 3.9+)', 'merged = a | b']])
     + '<h3>Вложенные словари (JSON)</h3>'
     + code('python',
            'student = {\n'
            '    "name": "Алиса",\n'
            '    "grades": {"math": 95, "python": 100, "english": 88},\n'
            '    "tags": ["отличник", "активист"]\n'
            '}\n\n'
            '# Обращение к вложенным данным\n'
            'print(student["grades"]["python"])    # 100\n'
            'print(student["tags"][0])             # отличник\n\n'
            '# Безопасное получение\n'
            'score = student.get("grades", {}).get("history", 0)\n'
            'print(score)  # 0 (нет такого предмета)\n\n'
            '# Перебор вложенного словаря\n'
            'for subject, score in student["grades"].items():\n'
            '    print(f"{subject}: {score}")')
     + '<h3>Счётчик слов через словарь</h3>'
     + code('python',
            'text = "яблоко банан яблоко вишня банан яблоко"\n'
            'words = text.split()\n\n'
            '# Способ 1: setdefault\n'
            'counter = {}\n'
            'for word in words:\n'
            '    counter.setdefault(word, 0)\n'
            '    counter[word] += 1\n\n'
            '# Способ 2: get (короче)\n'
            'counter2 = {}\n'
            'for word in words:\n'
            '    counter2[word] = counter2.get(word, 0) + 1\n\n'
            '# Способ 3: collections.Counter (лучший)\n'
            'from collections import Counter\n'
            'counter3 = Counter(words)\n'
            'print(counter3.most_common(2))  # [("яблоко", 3), ("банан", 2)]')
     + tip('Используй <code>d.get(key, default)</code> вместо <code>d[key]</code> когда ключ может отсутствовать — так избежишь KeyError.')),

    ('Словарные выражения и продвинутые техники',
     '<h2>Словарные выражения и продвинутые техники</h2>'
     '<p>Dict comprehension позволяет создавать словари в одну строку. '
     'Разберём паттерны, которые используются в реальном коде.</p>'
     '<h3>Dict Comprehension</h3>'
     + code('python',
            '# Базовый синтаксис\n'
            'squares = {x: x**2 for x in range(1, 6)}\n'
            '# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}\n\n'
            '# С условием (только чётные)\n'
            'even_sq = {x: x**2 for x in range(10) if x % 2 == 0}\n'
            '# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}\n\n'
            '# Инвертировать словарь (ключ ↔ значение)\n'
            'grades = {"math": 95, "python": 100}\n'
            'inverted = {v: k for k, v in grades.items()}\n'
            '# {95: "math", 100: "python"}\n\n'
            '# Фильтрация по значению\n'
            'high_grades = {k: v for k, v in grades.items() if v >= 95}\n'
            '# {"math": 95, "python": 100}')
     + '<h3>defaultdict — словарь с умолчанием</h3>'
     + code('python',
            'from collections import defaultdict\n\n'
            '# Группировка студентов по оценке\n'
            'students = [\n'
            '    ("Алиса", "A"), ("Боря", "B"), ("Вася", "A"),\n'
            '    ("Галя", "C"), ("Денис", "B"),\n'
            ']\n'
            'groups = defaultdict(list)   # при отсутствии ключа создаст []\n'
            'for name, grade in students:\n'
            '    groups[grade].append(name)\n\n'
            'print(dict(groups))\n'
            '# {"A": ["Алиса", "Вася"], "B": ["Боря", "Денис"], "C": ["Галя"]}')
     + '<h3>OrderedDict и последний элемент</h3>'
     + code('python',
            '# С Python 3.7 обычный dict сохраняет порядок вставки\n'
            'config = {"host": "localhost", "port": 8080, "debug": True}\n\n'
            '# Последний добавленный ключ\n'
            'last_key = list(config.keys())[-1]\n'
            'print(last_key)  # debug\n\n'
            '# Слияние нескольких словарей (Python 3.9+)\n'
            'defaults = {"theme": "dark", "lang": "ru"}\n'
            'user_prefs = {"lang": "en", "font_size": 14}\n'
            'result = defaults | user_prefs\n'
            '# {"theme": "dark", "lang": "en", "font_size": 14}  # user_prefs побеждает')
     + warn('Dict comprehension с изменением порядка ключ/значение — частая ошибка. '
            'Убедись что у тебя нет дублирующихся значений перед инверсией.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Обработка ошибок и исключения
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append((9, [  # Модуль order=9: Обработка ошибок

    ('Пользовательские исключения и иерархия ошибок',
     '<h2>Пользовательские исключения и иерархия ошибок</h2>'
     '<p>Стандартные исключения хороши, но для серьёзных программ нужны свои — '
     'они делают ошибки понятнее и позволяют обрабатывать их точечно.</p>'
     + diagram(600, 200,
               ARROW,
               svg_box(230, 20, 140, 36, '#dbeafe', '#3b82f6', 'BaseException', 12),
               arr(300, 56, 300, 84),
               svg_box(230, 84, 140, 36, '#ede9fe', '#7c3aed', 'Exception', 12),
               arr(230, 102, 130, 130, '#64748b'),
               arr(370, 102, 470, 130, '#64748b'),
               svg_box(50, 130, 120, 36, '#d1fae5', '#059669', 'ValueError\nTypeError', 11),
               svg_box(390, 130, 160, 36, '#fef9c3', '#d97706', 'МоеИсключение', 11))
     + code('python',
            '# Создаём иерархию своих исключений\n'
            'class AppError(Exception):\n'
            '    """Базовая ошибка приложения."""\n\n'
            'class ValidationError(AppError):\n'
            '    """Ошибка валидации данных."""\n'
            '    def __init__(self, field, message):\n'
            '        self.field = field\n'
            '        super().__init__(f"Поле {field!r}: {message}")\n\n'
            'class NetworkError(AppError):\n'
            '    """Ошибка сети."""\n'
            '    def __init__(self, url, code):\n'
            '        self.url = url\n'
            '        self.code = code\n'
            '        super().__init__(f"HTTP {code} при запросе {url}")\n\n'
            '# Использование\n'
            'def validate_age(age):\n'
            '    if not isinstance(age, int):\n'
            '        raise ValidationError("age", "должно быть целым числом")\n'
            '    if age < 0 or age > 150:\n'
            '        raise ValidationError("age", "недопустимый диапазон")\n\n'
            'try:\n'
            '    validate_age(-5)\n'
            'except ValidationError as e:\n'
            '    print(f"Ошибка: {e}")      # Поле "age": недопустимый диапазон\n'
            '    print(f"Поле: {e.field}")   # age\n'
            'except AppError as e:\n'
            '    print(f"Общая ошибка: {e}")')
     + tip('Наследуй свои исключения от <code>Exception</code>, а не от <code>BaseException</code>. '
           'BaseException — для системных исключений (KeyboardInterrupt, SystemExit).')),

    ('Контекстные менеджеры и with-блоки',
     '<h2>Контекстные менеджеры и with-блоки</h2>'
     '<p><code>with</code> гарантирует выполнение кода очистки даже если произошла ошибка — '
     'это основа безопасной работы с файлами, сетью, базами данных.</p>'
     '<h3>Как работает with</h3>'
     + diagram(640, 160,
               ARROW,
               svg_box(20, 60, 160, 40, '#dbeafe', '#3b82f6', '__enter__()\nоткрыть ресурс', 11),
               arr(180, 80, 240, 80),
               svg_box(240, 60, 140, 40, '#d1fae5', '#059669', 'тело блока\n(бизнес-логика)', 11),
               arr(380, 80, 440, 80),
               svg_box(440, 60, 180, 40, '#ede9fe', '#7c3aed', '__exit__()\nзакрыть ресурс\n(даже при ошибке)', 10))
     + code('python',
            '# Классический with для файлов\n'
            'with open("data.txt", "r", encoding="utf-8") as f:\n'
            '    content = f.read()\n'
            '# Файл закрыт автоматически — даже если было исключение\n\n'
            '# Несколько ресурсов в одном with\n'
            'with open("input.txt") as src, open("output.txt", "w") as dst:\n'
            '    dst.write(src.read().upper())\n\n'
            '# Создаём собственный контекстный менеджер\n'
            'class Timer:\n'
            '    import time\n'
            '    def __enter__(self):\n'
            '        import time\n'
            '        self.start = time.perf_counter()\n'
            '        return self        # это попадёт в "as timer"\n\n'
            '    def __exit__(self, exc_type, exc_val, exc_tb):\n'
            '        import time\n'
            '        self.elapsed = time.perf_counter() - self.start\n'
            '        print(f"Время: {self.elapsed:.4f} сек")\n'
            '        return False       # не подавляем исключение\n\n'
            'with Timer() as t:\n'
            '    total = sum(range(1_000_000))\n'
            'print(f"Сумма: {total}, заняло: {t.elapsed:.4f} сек")')
     + '<h3>contextlib.contextmanager — проще и чище</h3>'
     + code('python',
            'from contextlib import contextmanager\n\n'
            '@contextmanager\n'
            'def managed_connection(url):\n'
            '    print(f"Подключаемся к {url}")\n'
            '    conn = {"url": url, "open": True}  # симуляция соединения\n'
            '    try:\n'
            '        yield conn      # <-- сюда передаётся управление телу with\n'
            '    finally:\n'
            '        conn["open"] = False\n'
            '        print("Соединение закрыто")\n\n'
            'with managed_connection("db://localhost") as conn:\n'
            '    print(f"Работаем с: {conn}")')
     + info('Декоратор <code>@contextmanager</code> из <code>contextlib</code> — '
            'самый простой способ создать контекстный менеджер без класса.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Декораторы
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('Декораторы', [

    ('Декораторы с параметрами и functools.wraps',
     '<h2>Декораторы с параметрами и functools.wraps</h2>'
     '<p>Декоратор-фабрика — это функция, которая принимает аргументы и возвращает декоратор. '
     'Это мощный паттерн для конфигурируемого поведения.</p>'
     + code('python',
            '# Обычный декоратор (без параметров)\n'
            'def log(func):\n'
            '    def wrapper(*args, **kwargs):\n'
            '        print(f"Вызов {func.__name__}")\n'
            '        return func(*args, **kwargs)\n'
            '    return wrapper\n\n'
            '# Декоратор с параметрами (три уровня вложенности!)\n'
            'import functools\n\n'
            'def repeat(n):              # <-- принимает параметр n\n'
            '    def decorator(func):    # <-- настоящий декоратор\n'
            '        @functools.wraps(func)  # сохраняем имя и docstring\n'
            '        def wrapper(*args, **kwargs):\n'
            '            for _ in range(n):\n'
            '                result = func(*args, **kwargs)\n'
            '            return result\n'
            '        return wrapper\n'
            '    return decorator        # <-- возвращаем декоратор\n\n'
            '@repeat(3)                  # @repeat(3)(greet)\n'
            'def greet(name):\n'
            '    """Приветствует пользователя."""\n'
            '    print(f"Привет, {name}!")\n\n'
            'greet("Алиса")  # Привет, Алиса! (три раза)\n'
            'print(greet.__name__)   # greet (не wrapper, спасибо @wraps)')
     + warn('Без <code>@functools.wraps(func)</code> декоратор затирает имя функции и docstring. '
            'Это ломает отладку, документацию и некоторые фреймворки.')
     + '<h3>Декоратор кэширования (мемоизация)</h3>'
     + code('python',
            'import functools\n\n'
            'def memoize(func):\n'
            '    """Кэширует результаты вызовов функции."""\n'
            '    cache = {}\n'
            '    @functools.wraps(func)\n'
            '    def wrapper(*args):\n'
            '        if args not in cache:\n'
            '            cache[args] = func(*args)\n'
            '        return cache[args]\n'
            '    wrapper.cache = cache  # доступ к кэшу снаружи\n'
            '    return wrapper\n\n'
            '@memoize\n'
            'def fib(n):\n'
            '    if n < 2: return n\n'
            '    return fib(n-1) + fib(n-2)\n\n'
            'print(fib(50))         # мгновенно!\n'
            'print(len(fib.cache))  # 51 запомненных значений\n\n'
            '# Встроенный аналог из стандартной библиотеки:\n'
            'from functools import lru_cache\n\n'
            '@lru_cache(maxsize=128)\n'
            'def fib2(n):\n'
            '    return n if n < 2 else fib2(n-1) + fib2(n-2)')),

    ('Декораторы @property, @staticmethod, @classmethod',
     '<h2>Встроенные декораторы: @property, @staticmethod, @classmethod</h2>'
     '<p>Python предоставляет три важных встроенных декоратора для методов класса. '
     'Понимание их — ключ к написанию правильного Python-кода.</p>'
     + table(['Декоратор', 'Применение', 'self/cls'],
             [['@property', 'Атрибут с логикой вычисления', 'self'],
              ['@setter / @deleter', 'Запись/удаление свойства', 'self'],
              ['@staticmethod', 'Функция в пространстве класса', 'нет'],
              ['@classmethod', 'Метод, знающий о классе', 'cls']])
     + code('python',
            'class Circle:\n'
            '    def __init__(self, radius):\n'
            '        self._radius = radius   # _radius — "приватный"\n\n'
            '    @property\n'
            '    def radius(self):           # читать как атрибут\n'
            '        return self._radius\n\n'
            '    @radius.setter\n'
            '    def radius(self, value):    # устанавливать с валидацией\n'
            '        if value < 0:\n'
            '            raise ValueError("Радиус не может быть отрицательным")\n'
            '        self._radius = value\n\n'
            '    @property\n'
            '    def area(self):             # вычисляемое свойство (только чтение)\n'
            '        import math\n'
            '        return math.pi * self._radius ** 2\n\n'
            '    @staticmethod\n'
            '    def from_diameter(d):       # фабричный метод\n'
            '        return Circle(d / 2)\n\n'
            '    @classmethod\n'
            '    def unit(cls):              # создаёт единичный круг\n'
            '        return cls(1)\n\n'
            'c = Circle(5)\n'
            'print(c.area)          # 78.53...\n'
            'c.radius = 10          # вызывает setter\n'
            'c2 = Circle.from_diameter(8)   # radius = 4\n'
            'c3 = Circle.unit()             # radius = 1')
     + tip('Используй <code>@property</code> когда нужна валидация при установке атрибута '
            'или когда значение вычисляется на лету. Это делает API класса чище.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Регулярные выражения
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('Регулярные выражения', [

    ('Основы регулярных выражений в Python',
     '<h2>Основы регулярных выражений в Python</h2>'
     '<p>Регулярные выражения (regex) — язык поиска и замены в тексте. '
     'Модуль <code>re</code> — стандартный инструмент Python для работы с ними.</p>'
     '<h3>Базовые символы</h3>'
     + table(['Паттерн', 'Описание', 'Пример совпадения'],
             [[r'\d', 'Цифра [0-9]', '3, 7, 0'],
              [r'\w', 'Буква, цифра, _', 'a, Z, 5, _'],
              [r'\s', 'Пробельный символ', 'пробел, таб, \\n'],
              [r'.', 'Любой символ (кроме \\n)', 'a, 3, !'],
              ['[abc]', 'Один из символов', 'a, b или c'],
              ['^', 'Начало строки', '^Python'],
              ['$', 'Конец строки', 'world$'],
              ['*', '0 или более раз', 'ab* → a, ab, abb'],
              ['+', '1 или более раз', 'ab+ → ab, abb'],
              ['?', '0 или 1 раз', 'colou?r → color, colour'],
              ['{n,m}', 'От n до m раз', r'\d{2,4}']])
     + code('python',
            'import re\n\n'
            'text = "Телефон: +7 (916) 123-45-67 или 8-800-555-0100"\n\n'
            '# re.findall — все совпадения\n'
            r"phones = re.findall(r'[\d\-\s\(\)\+]{10,}', text)" + '\n'
            'print(phones)  # ["+7 (916) 123-45-67 ", "8-800-555-0100"]\n\n'
            '# re.search — первое совпадение (или None)\n'
            r"m = re.search(r'\d{3}', text)" + '\n'
            'if m:\n'
            '    print(m.group())   # 916\n'
            '    print(m.start())   # позиция в строке\n\n'
            '# re.sub — замена\n'
            r"clean = re.sub(r'[\s\-\(\)]', '', '+7 (916) 123-45-67')" + '\n'
            'print(clean)  # +79161234567')
     + tip('Всегда используй сырые строки <code>r"паттерн"</code> для regex. '
            'Это избавляет от двойного экранирования (\\\\d вместо r"\\d").')),

    ('Группы, именованные группы и флаги',
     '<h2>Группы захвата, именованные группы и флаги</h2>'
     '<p>Группы позволяют захватывать части совпадения. '
     'Именованные группы делают код более читаемым.</p>'
     + code('python',
            'import re\n\n'
            '# Группы захвата: ()\n'
            r"m = re.search(r'(\d{4})-(\d{2})-(\d{2})', '2024-01-15')" + '\n'
            'print(m.group(0))  # 2024-01-15 (всё совпадение)\n'
            'print(m.group(1))  # 2024 (первая группа)\n'
            'print(m.group(2))  # 01\n'
            'print(m.group(3))  # 15\n\n'
            '# Именованные группы: (?P<name>...)\n'
            r"pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'" + '\n'
            r"m = re.search(pattern, '2024-01-15')" + '\n'
            "print(m.group('year'))   # 2024\n"
            "print(m.group('month'))  # 01\n"
            "print(m.groupdict())  # {'year': '2024', 'month': '01', 'day': '15'}\n\n"
            '# findall с группами → список кортежей\n'
            r"dates = re.findall(r'(\d{4})-(\d{2})-(\d{2})', 'Встречи: 2024-01-15 и 2024-03-22')" + '\n'
            "print(dates)  # [('2024','01','15'), ('2024','03','22')]")
     + '<h3>Флаги</h3>'
     + table(['Флаг', 'Значение'],
             [['re.IGNORECASE (re.I)', 'Нечувствительность к регистру'],
              ['re.MULTILINE (re.M)', '^ и $ работают на каждой строке'],
              ['re.DOTALL (re.S)', '. совпадает с \\n тоже'],
              ['re.VERBOSE (re.X)', 'Пробелы и # в паттерне как комментарии']])
     + code('python',
            '# VERBOSE — для сложных паттернов\n'
            'email_pattern = re.compile(r"""\n'
            '    (?P<user>[\\w.+-]+)   # имя пользователя\n'
            '    @                     # разделитель\n'
            '    (?P<domain>[\\w-]+)   # домен\n'
            '    \\.                   # точка\n'
            '    (?P<tld>[\\w.]{2,6})  # зона (.com, .ru, .co.uk)\n'
            '""", re.VERBOSE)\n\n'
            'm = email_pattern.search("user.name@example.com")\n'
            "print(m.groupdict())  # {'user': 'user.name', 'domain': 'example', 'tld': 'com'}")
     + info('Компилируй паттерн через <code>re.compile()</code> если используешь его много раз — '
            'это ускоряет работу за счёт кэширования.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Тестирование
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('Тестирование', [

    ('unittest: структура тестов и assert-методы',
     '<h2>unittest: структура тестов и assert-методы</h2>'
     '<p><code>unittest</code> — встроенный фреймворк для тестирования. '
     'Он следует паттерну Arrange-Act-Assert (AAA).</p>'
     + diagram(620, 120,
               ARROW,
               svg_box(20, 40, 160, 40, '#dbeafe', '#3b82f6', 'Arrange\nПодготовить данные', 11),
               arr(180, 60, 240, 60),
               svg_box(240, 40, 140, 40, '#d1fae5', '#059669', 'Act\nВызвать функцию', 11),
               arr(380, 60, 440, 60),
               svg_box(440, 40, 160, 40, '#ede9fe', '#7c3aed', 'Assert\nПроверить результат', 11))
     + code('python',
            'import unittest\n\n'
            'def add(a, b): return a + b\n'
            'def divide(a, b):\n'
            '    if b == 0: raise ValueError("Делитель не может быть 0")\n'
            '    return a / b\n\n'
            'class TestMath(unittest.TestCase):\n\n'
            '    def test_add_positive(self):\n'
            '        # Arrange\n'
            '        a, b = 3, 5\n'
            '        # Act\n'
            '        result = add(a, b)\n'
            '        # Assert\n'
            '        self.assertEqual(result, 8)\n\n'
            '    def test_add_negative(self):\n'
            '        self.assertEqual(add(-1, -2), -3)\n\n'
            '    def test_divide_normal(self):\n'
            '        self.assertAlmostEqual(divide(1, 3), 0.333, places=3)\n\n'
            '    def test_divide_by_zero(self):\n'
            '        with self.assertRaises(ValueError) as ctx:\n'
            '            divide(10, 0)\n'
            '        self.assertIn("0", str(ctx.exception))\n\n'
            '    def test_types(self):\n'
            '        self.assertIsInstance(add(1, 2), int)\n'
            '        self.assertIsNone(None)\n'
            '        self.assertTrue(add(2, 3) > 4)\n\n'
            'if __name__ == "__main__":\n'
            '    unittest.main()')
     + '<h3>setUp и tearDown</h3>'
     + code('python',
            'class TestDatabase(unittest.TestCase):\n'
            '    def setUp(self):          # вызывается ПЕРЕД каждым тестом\n'
            '        self.db = {"users": []}\n\n'
            '    def tearDown(self):       # вызывается ПОСЛЕ каждого теста\n'
            '        self.db.clear()       # очищаем состояние\n\n'
            '    def test_add_user(self):\n'
            '        self.db["users"].append("Alice")\n'
            '        self.assertEqual(len(self.db["users"]), 1)')
     + tip('Запуск тестов из командной строки: <code>python -m unittest discover</code> — '
            'автоматически найдёт все файлы test_*.py.')),

    ('pytest и написание хороших тестов',
     '<h2>pytest: современный подход к тестированию</h2>'
     '<p>pytest проще unittest, поддерживает fixtures, параметризацию, '
     'и в реальных проектах используется чаще.</p>'
     + code('python',
            '# test_calculator.py\n'
            'import pytest\n\n'
            'def add(a, b): return a + b\n'
            'def divide(a, b):\n'
            '    if b == 0: raise ValueError("деление на 0")\n'
            '    return a / b\n\n'
            '# Простой тест — просто функция с assert\n'
            'def test_add():\n'
            '    assert add(2, 3) == 5\n'
            '    assert add(-1, 1) == 0\n\n'
            '# Параметризованный тест — запустится 4 раза\n'
            '@pytest.mark.parametrize("a,b,expected", [\n'
            '    (1, 2, 3),\n'
            '    (0, 0, 0),\n'
            '    (-1, 1, 0),\n'
            '    (100, -50, 50),\n'
            '])\n'
            'def test_add_parametrized(a, b, expected):\n'
            '    assert add(a, b) == expected\n\n'
            '# Тест исключения\n'
            'def test_divide_zero():\n'
            '    with pytest.raises(ValueError, match="деление на 0"):\n'
            '        divide(5, 0)\n\n'
            '# Fixture — переиспользуемые данные\n'
            '@pytest.fixture\n'
            'def sample_data():\n'
            '    return [1, 2, 3, 4, 5]\n\n'
            'def test_sum(sample_data):\n'
            '    assert sum(sample_data) == 15\n\n'
            '# Запуск: pytest test_calculator.py -v')
     + info('Установка pytest: <code>pip install pytest</code>. '
            'Для покрытия кода: <code>pip install pytest-cov</code> и '
            '<code>pytest --cov=.</code>')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: HTTP-запросы и REST API
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('HTTP-запросы и REST API', [

    ('HTTP-запросы с библиотекой requests',
     '<h2>HTTP-запросы с библиотекой requests</h2>'
     '<p><code>requests</code> — самая популярная Python-библиотека для HTTP. '
     'Понимание REST API необходимо для работы с любыми внешними сервисами.</p>'
     + diagram(640, 100,
               ARROW,
               svg_box(20, 30, 160, 40, '#dbeafe', '#3b82f6', 'Python\nrequests.get(url)', 11),
               arr(180, 50, 260, 50, '#64748b', 'HTTP GET'),
               svg_box(260, 30, 120, 40, '#d1fae5', '#059669', 'Сервер\nAPI endpoint', 11),
               arr(380, 50, 460, 50, '#64748b', 'JSON'),
               svg_box(460, 30, 160, 40, '#ede9fe', '#7c3aed', 'response.json()\nобработка', 11))
     + code('python',
            'import requests\n\n'
            '# GET-запрос: получить данные\n'
            'response = requests.get("https://jsonplaceholder.typicode.com/posts/1")\n'
            'print(response.status_code)  # 200\n'
            'print(response.headers["content-type"])\n'
            'data = response.json()\n'
            'print(data["title"])         # заголовок поста\n\n'
            '# POST-запрос: отправить данные\n'
            'new_post = {"title": "Мой пост", "body": "Текст", "userId": 1}\n'
            'r = requests.post(\n'
            '    "https://jsonplaceholder.typicode.com/posts",\n'
            '    json=new_post          # автоматически Content-Type: application/json\n'
            ')\n'
            'print(r.status_code)     # 201 Created\n'
            'print(r.json()["id"])    # 101 (новый id)\n\n'
            '# Параметры запроса (?key=value)\n'
            'r = requests.get(\n'
            '    "https://jsonplaceholder.typicode.com/posts",\n'
            '    params={"userId": 1, "_limit": 3}\n'
            ')\n'
            'posts = r.json()\n'
            'print(len(posts))  # 3')
     + '<h3>Обработка ошибок</h3>'
     + code('python',
            'import requests\n'
            'from requests.exceptions import ConnectionError, Timeout\n\n'
            'def safe_get(url, timeout=5):\n'
            '    try:\n'
            '        r = requests.get(url, timeout=timeout)\n'
            '        r.raise_for_status()  # исключение при 4xx/5xx\n'
            '        return r.json()\n'
            '    except Timeout:\n'
            '        print("Превышено время ожидания")\n'
            '    except ConnectionError:\n'
            '        print("Нет подключения к интернету")\n'
            '    except requests.HTTPError as e:\n'
            '        print(f"HTTP ошибка: {e.response.status_code}")\n'
            '    return None\n\n'
            'data = safe_get("https://api.github.com/users/python")\n'
            'if data:\n'
            '    print(data["public_repos"])')
     + tip('Заголовки авторизации: <code>headers={"Authorization": "Bearer TOKEN"}</code>. '
            'Никогда не хардкодь токены — используй переменные окружения.')),

    ('REST API: архитектура и CRUD операции',
     '<h2>REST API: архитектура и CRUD операции</h2>'
     '<p>REST — архитектурный стиль веб-сервисов. '
     'Понимание CRUD (Create-Read-Update-Delete) нужно для работы с любым API.</p>'
     + table(['HTTP-метод', 'CRUD', 'Пример URL', 'Что делает'],
             [['GET', 'Read', '/api/users/', 'Получить список'],
              ['GET', 'Read', '/api/users/5/', 'Получить запись с id=5'],
              ['POST', 'Create', '/api/users/', 'Создать новую запись'],
              ['PUT', 'Update', '/api/users/5/', 'Заменить запись полностью'],
              ['PATCH', 'Update', '/api/users/5/', 'Изменить часть полей'],
              ['DELETE', 'Delete', '/api/users/5/', 'Удалить запись']])
     + code('python',
            'import requests\n\n'
            'BASE = "https://jsonplaceholder.typicode.com"\n\n'
            '# CREATE — POST\n'
            'r = requests.post(f"{BASE}/todos", json={\n'
            '    "title": "Купить молоко", "completed": False, "userId": 1\n'
            '})\n'
            'todo = r.json()\n'
            'print(f"Создан: id={todo[\'id\']}")  # id=201\n\n'
            '# READ — GET\n'
            'r = requests.get(f"{BASE}/todos/1")\n'
            'print(r.json())  # {"id": 1, "title": "...", "completed": False}\n\n'
            '# UPDATE — PUT (полная замена)\n'
            'r = requests.put(f"{BASE}/todos/1", json={\n'
            '    "id": 1, "title": "Купить молоко", "completed": True, "userId": 1\n'
            '})\n'
            'print(r.json()["completed"])  # True\n\n'
            '# UPDATE — PATCH (частичное обновление)\n'
            'r = requests.patch(f"{BASE}/todos/1", json={"completed": True})\n\n'
            '# DELETE\n'
            'r = requests.delete(f"{BASE}/todos/1")\n'
            'print(r.status_code)  # 200')
     + info('Статусы HTTP: <b>200</b> OK, <b>201</b> Created, <b>400</b> Bad Request, '
            '<b>401</b> Unauthorized, <b>403</b> Forbidden, <b>404</b> Not Found, <b>500</b> Server Error.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: asyncio
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('asyncio', [

    ('Основы async/await и событийный цикл',
     '<h2>Основы async/await: как работает асинхронность</h2>'
     '<p>Асинхронность позволяет выполнять тысячи операций ввода-вывода "одновременно" '
     'без создания потоков. asyncio — встроенная библиотека для этого.</p>'
     + diagram(640, 180,
               ARROW,
               svg_box(20, 20, 140, 40, '#dbeafe', '#3b82f6', 'Синхронно:\nФ1 → Ф2 → Ф3', 11),
               svg_box(20, 80, 600, 40, '#f8fafc', '#94a3b8', '', 11),
               svg_box(20, 80, 160, 40, '#fef9c3', '#d97706', 'Ф1: запрос...', 11),
               svg_box(190, 80, 140, 40, '#d1fae5', '#059669', 'Ф2: запрос', 11),
               svg_box(340, 80, 140, 40, '#ede9fe', '#7c3aed', 'Ф3: запрос', 11),
               svg_box(20, 130, 140, 40, '#dbeafe', '#3b82f6', 'Асинхронно:\nВсе вместе!', 11))
     + code('python',
            'import asyncio\n\n'
            '# Обычная функция — блокирует\n'
            'def sync_sleep():\n'
            '    import time\n'
            '    time.sleep(1)   # блокирует всё\n\n'
            '# Корутина — не блокирует, передаёт управление\n'
            'async def fetch(url):\n'
            '    print(f"Начали: {url}")\n'
            '    await asyncio.sleep(1)  # симуляция сетевого запроса\n'
            '    print(f"Готово: {url}")\n'
            '    return f"Данные с {url}"\n\n'
            'async def main():\n'
            '    # Запускаем все запросы ОДНОВРЕМЕННО\n'
            '    results = await asyncio.gather(\n'
            '        fetch("site-A.ru"),\n'
            '        fetch("site-B.ru"),\n'
            '        fetch("site-C.ru"),\n'
            '    )\n'
            '    print(results)  # все три результата\n\n'
            '# Запуск (Python 3.11+: asyncio.run(main()))\n'
            'asyncio.run(main())\n'
            '# Всё заняло ~1 секунду, а не 3!')
     + warn('asyncio не ускоряет CPU-задачи (вычисления). '
            'Он ускоряет только I/O: сетевые запросы, чтение файлов, базы данных.')),

    ('asyncio на практике: aiohttp и задачи',
     '<h2>asyncio на практике: aiohttp и параллельные задачи</h2>'
     '<p>aiohttp — асинхронный HTTP-клиент. '
     'В связке с asyncio он позволяет делать сотни запросов за секунды.</p>'
     + code('python',
            '# pip install aiohttp\n'
            'import asyncio\n'
            'import aiohttp\n\n'
            'async def fetch_json(session, url):\n'
            '    """Получить JSON с URL."""\n'
            '    async with session.get(url) as response:\n'
            '        return await response.json()\n\n'
            'async def fetch_many(urls):\n'
            '    """Параллельно загрузить все URL."""\n'
            '    async with aiohttp.ClientSession() as session:\n'
            '        tasks = [fetch_json(session, url) for url in urls]\n'
            '        return await asyncio.gather(*tasks)\n\n'
            'urls = [\n'
            '    "https://jsonplaceholder.typicode.com/posts/1",\n'
            '    "https://jsonplaceholder.typicode.com/posts/2",\n'
            '    "https://jsonplaceholder.typicode.com/posts/3",\n'
            ']\n'
            'results = asyncio.run(fetch_many(urls))\n'
            'for r in results:\n'
            '    print(r["title"][:40])')
     + '<h3>Tasks — явное управление задачами</h3>'
     + code('python',
            'import asyncio\n\n'
            'async def worker(name, delay):\n'
            '    print(f"{name}: начал")\n'
            '    await asyncio.sleep(delay)\n'
            '    print(f"{name}: закончил через {delay}с")\n'
            '    return name\n\n'
            'async def main():\n'
            '    # Создаём задачи явно\n'
            '    t1 = asyncio.create_task(worker("A", 2))\n'
            '    t2 = asyncio.create_task(worker("B", 1))\n'
            '    t3 = asyncio.create_task(worker("C", 3))\n\n'
            '    # Ждём все три (порядок завершения: B, A, C)\n'
            '    results = await asyncio.gather(t1, t2, t3)\n'
            '    print(f"Все завершены: {results}")\n\n'
            'asyncio.run(main())')
     + tip('Если нужен asyncio в Django/Flask — используй <code>asyncio.run()</code> '
            'или фреймворки с нативной async-поддержкой (FastAPI, Django 4.x).')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: NumPy
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('NumPy', [

    ('NumPy: создание и операции с массивами',
     '<h2>NumPy: создание и операции с массивами</h2>'
     '<p>NumPy — основа научных вычислений в Python. '
     'Массивы NumPy работают в 10-100 раз быстрее обычных списков Python.</p>'
     + code('python',
            'import numpy as np\n\n'
            '# Создание массивов\n'
            'a = np.array([1, 2, 3, 4, 5])          # из списка\n'
            'b = np.zeros((3, 4))                    # нули 3×4\n'
            'c = np.ones((2, 3))                     # единицы\n'
            'd = np.arange(0, 10, 2)                 # [0, 2, 4, 6, 8]\n'
            'e = np.linspace(0, 1, 5)                # 5 точек от 0 до 1\n'
            'f = np.random.randint(0, 100, size=(3, 3))  # случайная матрица\n\n'
            '# Свойства массива\n'
            'print(a.shape)    # (5,)    — одномерный\n'
            'print(f.shape)    # (3, 3)  — двумерный\n'
            'print(f.dtype)    # int32 или int64\n'
            'print(f.ndim)     # 2 (количество измерений)\n\n'
            '# Арифметика (поэлементная)\n'
            'x = np.array([1, 2, 3])\n'
            'y = np.array([4, 5, 6])\n'
            'print(x + y)     # [5, 7, 9]\n'
            'print(x * y)     # [4, 10, 18]\n'
            'print(x ** 2)    # [1, 4, 9]\n'
            'print(np.sqrt(x))  # [1.0, 1.414, 1.732]')
     + '<h3>Индексация и срезы</h3>'
     + code('python',
            'import numpy as np\n'
            'm = np.array([[1, 2, 3],\n'
            '              [4, 5, 6],\n'
            '              [7, 8, 9]])\n\n'
            'print(m[1, 2])        # 6 — строка 1, столбец 2\n'
            'print(m[0, :])        # [1, 2, 3] — первая строка\n'
            'print(m[:, 1])        # [2, 5, 8] — второй столбец\n'
            'print(m[1:, 1:])      # [[5,6],[8,9]] — подматрица\n\n'
            '# Булева индексация\n'
            'a = np.array([10, -5, 3, -8, 7])\n'
            'print(a[a > 0])       # [10, 3, 7] — только положительные\n'
            'a[a < 0] = 0          # заменить отрицательные на 0\n'
            'print(a)              # [10, 0, 3, 0, 7]')
     + tip('Срезы NumPy НЕ копируют данные — они создают <em>представление</em> (view). '
            'Используй <code>arr.copy()</code> если нужна независимая копия.')),

    ('NumPy: матричные операции и статистика',
     '<h2>NumPy: матричные операции и статистика</h2>'
     '<p>NumPy предоставляет линейную алгебру, статистические функции '
     'и широковещательные операции (broadcasting).</p>'
     + code('python',
            'import numpy as np\n\n'
            '# Статистика\n'
            'data = np.array([85, 92, 78, 96, 88, 74, 95, 82])\n'
            'print(f"Среднее: {data.mean():.1f}")\n'
            'print(f"Медиана: {np.median(data):.1f}")\n'
            'print(f"Станд. откл.: {data.std():.2f}")\n'
            'print(f"Минимум: {data.min()}, Максимум: {data.max()}")\n'
            'print(f"25-й перцентиль: {np.percentile(data, 25)}")\n\n'
            '# Матричные операции\n'
            'A = np.array([[1, 2], [3, 4]])\n'
            'B = np.array([[5, 6], [7, 8]])\n\n'
            'print(A @ B)          # матричное произведение\n'
            '# [[19, 22], [43, 50]]\n\n'
            'print(A.T)            # транспонирование\n'
            '# [[1, 3], [2, 4]]\n\n'
            'print(np.linalg.det(A))    # определитель: -2.0\n'
            'print(np.linalg.inv(A))    # обратная матрица')
     + '<h3>Broadcasting — мощь NumPy</h3>'
     + code('python',
            'import numpy as np\n\n'
            '# Broadcasting: операции с разными формами\n'
            'matrix = np.array([[1, 2, 3],\n'
            '                   [4, 5, 6],\n'
            '                   [7, 8, 9]])\n\n'
            '# Прибавить 10 к каждому элементу (скаляр)\n'
            'print(matrix + 10)\n\n'
            '# Прибавить [10, 20, 30] к каждой СТРОКЕ\n'
            'row = np.array([10, 20, 30])\n'
            'print(matrix + row)\n'
            '# [[11, 22, 33], [14, 25, 36], [17, 28, 39]]\n\n'
            '# Нормализация данных (приведение к [0, 1])\n'
            'scores = np.array([50, 70, 85, 92, 100])\n'
            'normalized = (scores - scores.min()) / (scores.max() - scores.min())\n'
            'print(normalized.round(2))\n'
            '# [0.0, 0.4, 0.7, 0.84, 1.0]')
     + info('NumPy — основа Pandas, scikit-learn, TensorFlow. '
            'Освоив NumPy, ты готов к машинному обучению и анализу данных.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Pandas
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('Pandas', [

    ('Pandas: DataFrame, индексация и фильтрация',
     '<h2>Pandas: DataFrame — таблицы в Python</h2>'
     '<p>Pandas — главная библиотека для анализа данных. '
     'DataFrame — это таблица с именованными строками и столбцами.</p>'
     + code('python',
            'import pandas as pd\n\n'
            '# Создание DataFrame\n'
            'df = pd.DataFrame({\n'
            '    "имя": ["Алиса", "Боря", "Вася", "Галя", "Денис"],\n'
            '    "возраст": [20, 22, 19, 23, 21],\n'
            '    "оценка": [95, 78, 92, 88, 85],\n'
            '    "группа": ["A", "B", "A", "B", "A"]\n'
            '})\n\n'
            '# Базовая информация\n'
            'print(df.shape)         # (5, 4) — 5 строк, 4 столбца\n'
            'print(df.dtypes)        # типы данных по столбцам\n'
            'print(df.describe())    # статистика по числовым столбцам\n\n'
            '# Выборка данных\n'
            'print(df["оценка"])             # один столбец → Series\n'
            'print(df[["имя", "оценка"]])    # несколько столбцов → DataFrame\n'
            'print(df.iloc[0])               # первая строка (по позиции)\n'
            'print(df.loc[df["возраст"] > 20])  # строки где возраст > 20')
     + '<h3>Фильтрация и сортировка</h3>'
     + code('python',
            '# Фильтрация (булева индексация)\n'
            'group_a = df[df["группа"] == "A"]\n'
            'high_scores = df[df["оценка"] >= 90]\n'
            'young_A = df[(df["группа"] == "A") & (df["возраст"] < 22)]\n\n'
            '# Сортировка\n'
            'df_sorted = df.sort_values("оценка", ascending=False)\n'
            'print(df_sorted[["имя", "оценка"]].head(3))\n\n'
            '# Добавить столбец\n'
            'df["успевает"] = df["оценка"].apply(lambda x: "✓" if x >= 90 else "✗")\n\n'
            '# Группировка и агрегация\n'
            'grouped = df.groupby("группа")["оценка"].agg(["mean", "max", "count"])\n'
            'print(grouped)\n'
            '#          mean  max  count\n'
            '# группа\n'
            '# A        90.7   95      3\n'
            '# B        83.0   88      2')
     + tip('Метод <code>.copy()</code> создаёт независимую копию DataFrame. '
            'Без него изменения могут повлиять на исходные данные (SettingWithCopyWarning).')),

    ('Pandas: чтение данных, обработка пропусков и экспорт',
     '<h2>Pandas: чтение данных и практический анализ</h2>'
     '<p>Pandas умеет читать CSV, Excel, JSON, базы данных. '
     'Это делает его центром любого data-пайплайна.</p>'
     + code('python',
            'import pandas as pd\n'
            'import io\n\n'
            '# Чтение CSV\n'
            'csv_data = """name,age,score,city\n'
            'Alice,20,95,Москва\n'
            'Bob,22,78,\n'
            'Charlie,19,,Санкт-Петербург\n'
            'Diana,23,92,Москва\n'
            '"""\n'
            'df = pd.read_csv(io.StringIO(csv_data))\n\n'
            '# Работа с пропусками (NaN)\n'
            'print(df.isna().sum())          # количество NaN по столбцам\n'
            'print(df.isna().sum() / len(df))  # доля пропусков\n\n'
            '# Стратегии заполнения пропусков\n'
            'df["city"].fillna("Неизвестно", inplace=True)\n'
            'df["score"].fillna(df["score"].mean(), inplace=True)  # средним\n'
            'df.dropna(inplace=True)          # удалить строки с NaN\n\n'
            '# Экспорт\n'
            'df.to_csv("output.csv", index=False, encoding="utf-8")\n'
            '# df.to_excel("output.xlsx", index=False)\n'
            '# df.to_json("output.json", orient="records", force_ascii=False)')
     + '<h3>Сводная таблица (pivot table)</h3>'
     + code('python',
            'import pandas as pd\n\n'
            'sales = pd.DataFrame({\n'
            '    "товар": ["яблоки", "бананы", "яблоки", "бананы", "яблоки"],\n'
            '    "месяц": ["янв", "янв", "фев", "фев", "март"],\n'
            '    "продажи": [100, 150, 130, 120, 200]\n'
            '})\n\n'
            'pivot = pd.pivot_table(\n'
            '    sales,\n'
            '    values="продажи",\n'
            '    index="товар",\n'
            '    columns="месяц",\n'
            '    aggfunc="sum",\n'
            '    fill_value=0\n'
            ')\n'
            'print(pivot)\n'
            '# месяц    фев  янв  март\n'
            '# товар\n'
            '# бананы   120  150     0\n'
            '# яблоки   130  100   200')
     + info('Pandas + Matplotlib = полный цикл анализа данных. '
            'Для больших датасетов (>1 ГБ) смотри на Polars или Dask.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Логгирование
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('logging', [

    ('Логгирование в Python: правильный подход',
     '<h2>Логгирование в Python: правильный подход</h2>'
     '<p>Логи — глаза программиста в продакшне. '
     '<code>print()</code> для отладки, <code>logging</code> — для реальных программ.</p>'
     + table(['Уровень', 'Когда использовать', 'Пример'],
             [['DEBUG', 'Детали для разработки', 'Входные параметры функции'],
              ['INFO', 'Обычные события', 'Пользователь вошёл в систему'],
              ['WARNING', 'Неожиданное, но не ошибка', 'Файл не найден, используется дефолт'],
              ['ERROR', 'Серьёзная ошибка', 'Не удалось сохранить данные'],
              ['CRITICAL', 'Критическая ошибка', 'База данных недоступна']])
     + code('python',
            'import logging\n\n'
            '# Базовая настройка\n'
            'logging.basicConfig(\n'
            '    level=logging.DEBUG,\n'
            '    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",\n'
            '    datefmt="%Y-%m-%d %H:%M:%S"\n'
            ')\n\n'
            'logger = logging.getLogger(__name__)\n\n'
            'def process_order(order_id, amount):\n'
            '    logger.debug(f"Начало обработки заказа {order_id}")\n'
            '    if amount <= 0:\n'
            '        logger.error(f"Некорректная сумма: {amount}")\n'
            '        return False\n'
            '    logger.info(f"Заказ {order_id} на {amount}₽ обработан")\n'
            '    return True\n\n'
            'process_order("A001", 1500)\n'
            '# 2024-01-15 10:30:00 [DEBUG] __main__: Начало обработки заказа A001\n'
            '# 2024-01-15 10:30:00 [INFO]  __main__: Заказ A001 на 1500₽ обработан')
     + '<h3>Запись в файл + ротация логов</h3>'
     + code('python',
            'import logging\n'
            'from logging.handlers import RotatingFileHandler\n\n'
            'logger = logging.getLogger("myapp")\n'
            'logger.setLevel(logging.DEBUG)\n\n'
            '# Файловый обработчик с ротацией (max 5 МБ, хранить 3 файла)\n'
            'fh = RotatingFileHandler(\n'
            '    "app.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"\n'
            ')\n'
            'fh.setLevel(logging.INFO)\n\n'
            '# Консольный обработчик (только WARNING и выше)\n'
            'ch = logging.StreamHandler()\n'
            'ch.setLevel(logging.WARNING)\n\n'
            'fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")\n'
            'fh.setFormatter(fmt)\n'
            'ch.setFormatter(fmt)\n\n'
            'logger.addHandler(fh)\n'
            'logger.addHandler(ch)\n\n'
            'logger.info("Приложение запущено")  # только в файл\n'
            'logger.warning("Диск почти заполнен")  # в файл И в консоль')
     + tip('Используй <code>logger = logging.getLogger(__name__)</code> в каждом модуле — '
            'имя логгера автоматически показывает откуда пришло сообщение.')),

    ('Структурированное логгирование и контекст',
     '<h2>Структурированное логгирование</h2>'
     '<p>В современных приложениях логи пишут в JSON — '
     'это позволяет их парсить и искать в системах мониторинга (ELK, Grafana).</p>'
     + code('python',
            'import logging\n'
            'import json\n\n'
            'class JSONFormatter(logging.Formatter):\n'
            '    """Форматирует логи как JSON."""\n'
            '    def format(self, record):\n'
            '        log_obj = {\n'
            '            "timestamp": self.formatTime(record),\n'
            '            "level": record.levelname,\n'
            '            "logger": record.name,\n'
            '            "message": record.getMessage(),\n'
            '        }\n'
            '        # Дополнительные поля через extra=\n'
            '        if hasattr(record, "user_id"):\n'
            '            log_obj["user_id"] = record.user_id\n'
            '        if record.exc_info:\n'
            '            log_obj["exception"] = self.formatException(record.exc_info)\n'
            '        return json.dumps(log_obj, ensure_ascii=False)\n\n'
            'logger = logging.getLogger("api")\n'
            'handler = logging.StreamHandler()\n'
            'handler.setFormatter(JSONFormatter())\n'
            'logger.addHandler(handler)\n\n'
            '# Логирование с контекстом\n'
            'logger.info("Запрос получен", extra={"user_id": 42})\n'
            '# {"timestamp": "2024-01-15 10:30", "level": "INFO",\n'
            '#  "message": "Запрос получен", "user_id": 42}')
     + info('Популярная альтернатива: <code>structlog</code> — '
            'устанавливается через <code>pip install structlog</code> '
            'и даёт гибкое структурированное логирование "из коробки".')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Профилировка
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append((43, [  # Модуль order=43: Профилировка

    ('Измерение производительности: timeit и cProfile',
     '<h2>Измерение производительности Python-кода</h2>'
     '<p>Не оптимизируй "на глаз" — сначала измерь, потом ускоряй. '
     '<code>timeit</code> и <code>cProfile</code> — встроенные инструменты.</p>'
     + code('python',
            'import timeit\n\n'
            '# timeit — микробенчмарк (время одной операции)\n\n'
            '# Вариант 1: конкатенация через +\n'
            'time1 = timeit.timeit(\n'
            '    stmt="result = \\"\\".join([str(i) for i in range(1000)])",\n'
            '    number=10000\n'
            ')\n\n'
            '# Вариант 2: через join\n'
            'time2 = timeit.timeit(\n'
            '    stmt="result = \\"\\".join(str(i) for i in range(1000))",\n'
            '    number=10000\n'
            ')\n\n'
            'print(f"List comprehension: {time1:.3f} сек")\n'
            'print(f"Generator expr:     {time2:.3f} сек")\n\n'
            '# В командной строке:\n'
            '# python -m timeit -n 10000 \'",".join(str(i) for i in range(1000))\'\n\n'
            '# %timeit в Jupyter Notebook:\n'
            '# %timeit sum(range(1000))')
     + '<h3>cProfile — профилирование всей программы</h3>'
     + code('python',
            'import cProfile\n'
            'import pstats\n\n'
            'def slow_function():\n'
            '    total = 0\n'
            '    for i in range(100_000):\n'
            '        total += i ** 2\n'
            '    return total\n\n'
            'def main():\n'
            '    for _ in range(10):\n'
            '        slow_function()\n\n'
            '# Профилирование\n'
            'with cProfile.Profile() as pr:\n'
            '    main()\n\n'
            '# Вывод результатов\n'
            'stats = pstats.Stats(pr)\n'
            'stats.sort_stats("cumulative")  # по суммарному времени\n'
            'stats.print_stats(10)           # топ 10 функций\n\n'
            '# Или: python -m cProfile -s cumtime script.py')
     + tip('Правило оптимизации: 80% времени тратится в 20% кода. '
            'Найди это 20% через cProfile, и только потом оптимизируй.')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Сетевое программирование
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('Сетевое программирование', [

    ('Сокеты Python: клиент и сервер',
     '<h2>Сокеты Python: как работает сеть</h2>'
     '<p>Сокет — это "дверь" в сеть. Через неё программы общаются по TCP/UDP. '
     'Понимание сокетов объясняет, как работают HTTP, FTP, WebSocket.</p>'
     + diagram(620, 150,
               ARROW,
               svg_box(20, 50, 160, 50, '#dbeafe', '#3b82f6', 'Клиент\nsocket.connect()', 11),
               arr(180, 75, 250, 75, '#64748b', 'TCP SYN'),
               svg_box(260, 30, 140, 90, '#d1fae5', '#059669', 'Сервер\nsocket.bind()\n.listen()\n.accept()', 11),
               arr(260, 75, 180, 75, '#64748b', 'SYN-ACK'),
               svg_box(20, 115, 160, 25, '#fef9c3', '#d97706', 'send("данные")', 10),
               arr(180, 127, 250, 127, '#d97706', 'данные'))
     + code('python',
            '# === СЕРВЕР ===\n'
            'import socket, threading\n\n'
            'def handle_client(conn, addr):\n'
            '    print(f"Подключился: {addr}")\n'
            '    with conn:\n'
            '        while True:\n'
            '            data = conn.recv(1024)\n'
            '            if not data: break\n'
            '            msg = data.decode("utf-8")\n'
            '            print(f"От {addr}: {msg}")\n'
            '            conn.sendall(f"Эхо: {msg}".encode("utf-8"))\n\n'
            'server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n'
            'server.bind(("localhost", 9000))\n'
            'server.listen(5)\n'
            'print("Сервер слушает на :9000")\n'
            'while True:\n'
            '    conn, addr = server.accept()\n'
            '    threading.Thread(target=handle_client, args=(conn, addr)).start()')
     + code('python',
            '# === КЛИЕНТ ===\n'
            'import socket\n\n'
            'with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n'
            '    s.connect(("localhost", 9000))\n'
            '    s.sendall("Привет, сервер!".encode("utf-8"))\n'
            '    response = s.recv(1024)\n'
            '    print(f"Ответ: {response.decode()}")\n'
            '    # Эхо: Привет, сервер!')
     + warn('TCP-сервер выше однопоточный. В продакшне используй asyncio, '
            'ThreadPoolExecutor или готовые фреймворки (aiohttp, FastAPI).')),
]))


# ══════════════════════════════════════════════════════════════════════════════════
# Модуль: Криптография
# ══════════════════════════════════════════════════════════════════════════════════
LESSONS.append(('secrets', [  # Модуль: Криптография

    ('Хэширование и безопасные пароли в Python',
     '<h2>Хэширование и безопасные пароли в Python</h2>'
     '<p>Никогда не храни пароли в открытом виде. '
     'Используй bcrypt или hashlib с солью.</p>'
     + table(['Алгоритм', 'Тип', 'Применение'],
             [['MD5 / SHA-1', 'Контрольная сумма', 'Целостность файлов (НЕ для паролей!)'],
              ['SHA-256 / SHA-3', 'Крипто-хэш', 'HMAC, подписи, хранение данных'],
              ['bcrypt / argon2', 'Пароль-хэш', 'Пароли пользователей (медленный умышленно)'],
              ['secrets', 'CSPRNG', 'Токены, ссылки сброса пароля']])
     + code('python',
            'import hashlib, secrets, hmac\n\n'
            '# SHA-256 — контрольная сумма файла\n'
            'def file_hash(path):\n'
            '    h = hashlib.sha256()\n'
            '    with open(path, "rb") as f:\n'
            '        for chunk in iter(lambda: f.read(8192), b""):\n'
            '            h.update(chunk)\n'
            '    return h.hexdigest()\n\n'
            '# HMAC — аутентификация сообщений\n'
            'secret_key = b"my-secret-key"\n'
            'message = b"transfer: 1000 USD"\n'
            'mac = hmac.new(secret_key, message, hashlib.sha256).hexdigest()\n'
            'print(f"HMAC: {mac}")\n\n'
            '# Безопасный пароль с солью (hashlib)\n'
            'def hash_password(password: str) -> str:\n'
            '    salt = secrets.token_hex(32)  # 64-символьная соль\n'
            '    key = hashlib.pbkdf2_hmac("sha256",\n'
            '                              password.encode(),\n'
            '                              salt.encode(),\n'
            '                              iterations=600_000)\n'
            '    return f"{salt}:{key.hex()}"\n\n'
            'def verify_password(password: str, stored: str) -> bool:\n'
            '    salt, key_hex = stored.split(":")\n'
            '    new_key = hashlib.pbkdf2_hmac("sha256",\n'
            '                                  password.encode(),\n'
            '                                  salt.encode(),\n'
            '                                  iterations=600_000)\n'
            '    return hmac.compare_digest(new_key.hex(), key_hex)\n\n'
            'stored = hash_password("mysecretpassword")\n'
            'print(verify_password("mysecretpassword", stored))  # True\n'
            'print(verify_password("wrongpassword", stored))     # False')
     + warn('Для паролей в продакшне используй <b>bcrypt</b> (<code>pip install bcrypt</code>) '
            'или <b>argon2-cffi</b> — они специально медленные, чтобы замедлить брутфорс.')),
]))


# ════════════════════════════════════════════════════════════════════════════════
# Команда
# ════════════════════════════════════════════════════════════════════════════════

class Command(BaseCommand):
    help = 'Расширяет тонкие Python-модули — добавляет 2+ урока в каждый'

    def handle(self, *args, **options):
        try:
            subject = Subject.objects.get(slug='python')
        except Subject.DoesNotExist:
            self.stderr.write('Subject python не найден')
            return

        created_total = 0
        skipped_total = 0

        for keyword, lesson_list in LESSONS:
            # Ищем модуль: целое число → по order, строка → по icontains
            if isinstance(keyword, int):
                modules = TheoryModule.objects.filter(
                    subject=subject,
                    order=keyword
                )
            else:
                modules = TheoryModule.objects.filter(
                    subject=subject,
                    title__icontains=keyword
                ).order_by('order')

            if not modules.exists():
                self.stdout.write(self.style.WARNING(
                    f'  Модуль с "{keyword}" не найден — пропускаем'
                ))
                continue

            # Берём первый подходящий модуль
            module = modules.first()
            existing_titles = set(
                TheoryLesson.objects.filter(module=module)
                .values_list('title', flat=True)
            )
            existing_count = len(existing_titles)
            next_order = existing_count + 1

            for title, content in lesson_list:
                if title in existing_titles:
                    skipped_total += 1
                    continue
                TheoryLesson.objects.create(
                    module=module,
                    title=title,
                    content=content,
                    order=next_order,
                    estimated_minutes=10,
                )
                next_order += 1
                created_total += 1
                self.stdout.write(
                    f'  + [{module.order}] {title}'
                )

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово: создано {created_total} уроков, пропущено {skipped_total} (уже есть).'
        ))
