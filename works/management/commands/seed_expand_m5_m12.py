from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


def code_block(code):
    return (
        '<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;'
        'border-radius:8px;font-family:monospace;font-size:.9rem;'
        'overflow-x:auto;margin:1rem 0"><pre style="margin:0">'
        f'{code}</pre></div>'
    )


def info_table(headers, rows):
    hdr = ''.join(f'<th>{h}</th>' for h in headers)
    body = ''
    for row in rows:
        body += '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
    return (
        '<table border="1" cellpadding="8" cellspacing="0" '
        'style="border-collapse:collapse;width:100%;margin:1rem 0">'
        f'<tr style="background:#f1f5f9">{hdr}</tr>{body}</table>'
    )


LESSONS = {
    # ── M5: Цикл for и range() ────────────────────────────────
    5: [
        {
            'title': 'Функция range(): параметры и применение',
            'order': 4,
            'minutes': 10,
            'code': (
                '# range(stop)\n'
                'for i in range(5):\n'
                '    print(i)  # 0 1 2 3 4\n\n'
                '# range(start, stop)\n'
                'for i in range(2, 7):\n'
                '    print(i)  # 2 3 4 5 6\n\n'
                '# range(start, stop, step)\n'
                'for i in range(0, 20, 3):\n'
                '    print(i)  # 0 3 6 9 12 15 18\n\n'
                '# Обратный отсчёт\n'
                'for i in range(10, 0, -1):\n'
                '    print(i)  # 10 9 8 ... 1\n\n'
                '# range — не список, а генератор\n'
                'r = range(1000000)  # не занимает память\n'
                'print(500000 in r)  # True — проверка за O(1)\n'
                'print(len(r))       # 1000000\n'
                'print(r[999])       # 999 — поддерживает индексацию'
            ),
            'content': '''<h2>Функция range(): параметры и применение</h2>
<p><code>range()</code> — одна из самых используемых функций в Python. Она генерирует последовательность целых чисел без хранения их всех в памяти.</p>

<h3>Три формы вызова</h3>
''' + info_table(
    ['Форма', 'Пример', 'Результат'],
    [
        ['<code>range(stop)</code>', '<code>range(5)</code>', '0, 1, 2, 3, 4'],
        ['<code>range(start, stop)</code>', '<code>range(2, 7)</code>', '2, 3, 4, 5, 6'],
        ['<code>range(start, stop, step)</code>', '<code>range(0, 10, 2)</code>', '0, 2, 4, 6, 8'],
    ]
) + '''
<p><strong>Важно:</strong> конечное значение <code>stop</code> <em>не включается</em> в последовательность!</p>

<h3>Отрицательный шаг — обратный отсчёт</h3>
''' + code_block(
    'for i in range(10, 0, -1):\n'
    '    print(i, end=" ")  # 10 9 8 7 6 5 4 3 2 1\n\n'
    'for i in range(100, -1, -10):\n'
    '    print(i, end=" ")  # 100 90 80 ... 10 0'
) + '''
<h3>range — ленивый объект</h3>
<p><code>range()</code> не создаёт список в памяти. Это объект-генератор, который вычисляет числа по запросу:</p>
''' + code_block(
    'import sys\n'
    'lst = list(range(1000000))  # ~8 МБ памяти\n'
    'r = range(1000000)          # ~48 байт!\n'
    'print(sys.getsizeof(lst))   # 8448728\n'
    'print(sys.getsizeof(r))     # 48'
) + '''
<h3>Полезные приёмы</h3>
''' + info_table(
    ['Задача', 'Код'],
    [
        ['Чётные числа до 20', '<code>range(0, 21, 2)</code>'],
        ['Нечётные числа', '<code>range(1, 20, 2)</code>'],
        ['Обратный порядок', '<code>range(n-1, -1, -1)</code>'],
        ['Индексы списка', '<code>range(len(lst))</code>'],
        ['Список из range', '<code>list(range(5))</code>'],
    ]
) + '''
<h3>Запомните</h3>
<ul>
<li><code>range(stop)</code> — от 0 до stop-1</li>
<li><code>range(start, stop, step)</code> — полная форма</li>
<li>stop никогда не включается в результат</li>
<li>range — ленивый, экономит память</li>
<li>Поддерживает <code>in</code>, <code>len()</code>, индексацию</li>
</ul>'''
        },
        {
            'title': 'Строковые методы и итерация по строкам',
            'order': 5,
            'minutes': 12,
            'code': (
                '# Перебор символов строки\n'
                'for ch in "Python":\n'
                '    print(ch, end="-")  # P-y-t-h-o-n-\n\n'
                '# Подсчёт символов\n'
                'text = "Hello, World!"\n'
                'vowels = 0\n'
                'for ch in text.lower():\n'
                '    if ch in "aeiou":\n'
                '        vowels += 1\n'
                'print(f"Гласных: {vowels}")  # 3\n\n'
                '# Перебор слов\n'
                'sentence = "Python - отличный язык"\n'
                'for word in sentence.split():\n'
                '    print(f"{word}: {len(word)} букв")\n\n'
                '# Перебор строк файла\n'
                'text = "Строка 1\\nСтрока 2\\nСтрока 3"\n'
                'for line in text.splitlines():\n'
                '    print(line.strip())\n\n'
                '# Форматирование: f-строки\n'
                'name = "Мир"\n'
                'age = 2024\n'
                'print(f"Привет, {name}! Год: {age}")\n'
                'print(f"Число: {3.14159:.2f}")  # 3.14\n'
                "print(f\"{'Python':>10}\")  # выравнивание вправо"
            ),
            'content': '''<h2>Строковые методы и итерация по строкам</h2>
<p>Строки в Python — итерируемые объекты. Это значит, что <code>for</code> может
перебирать их посимвольно. Комбинируя циклы со строковыми методами, можно
решать множество задач обработки текста.</p>

<h3>Перебор символов</h3>
''' + code_block(
    'word = "Python"\n'
    'for i, ch in enumerate(word):\n'
    '    print(f"Символ {i}: {ch}")\n'
    '# Символ 0: P\n'
    '# Символ 1: y\n'
    '# ...'
) + '''
<h3>Основные строковые методы</h3>
''' + info_table(
    ['Метод', 'Описание', 'Пример'],
    [
        ['<code>.upper()</code>', 'В верхний регистр', '<code>"abc".upper() → "ABC"</code>'],
        ['<code>.lower()</code>', 'В нижний регистр', '<code>"ABC".lower() → "abc"</code>'],
        ['<code>.strip()</code>', 'Убрать пробелы по краям', '<code>" hi ".strip() → "hi"</code>'],
        ['<code>.split()</code>', 'Разбить на список слов', '<code>"a b c".split() → ["a","b","c"]</code>'],
        ['<code>.join(lst)</code>', 'Склеить список', '<code>"-".join(["a","b"]) → "a-b"</code>'],
        ['<code>.replace(a,b)</code>', 'Замена подстроки', '<code>"abc".replace("b","X") → "aXc"</code>'],
        ['<code>.find(s)</code>', 'Поиск подстроки', '<code>"hello".find("ll") → 2</code>'],
        ['<code>.count(s)</code>', 'Подсчёт вхождений', '<code>"abba".count("b") → 2</code>'],
        ['<code>.startswith(s)</code>', 'Начинается ли с s', '<code>"Python".startswith("Py") → True</code>'],
        ['<code>.isdigit()</code>', 'Только цифры?', '<code>"123".isdigit() → True</code>'],
    ]
) + '''
<h3>Разбиение и объединение</h3>
''' + code_block(
    '# split — разбить строку\n'
    'csv_line = "Анна,20,Москва"\n'
    'parts = csv_line.split(",")\n'
    'print(parts)  # ["Анна", "20", "Москва"]\n\n'
    '# join — собрать обратно\n'
    'result = " | ".join(parts)\n'
    'print(result)  # "Анна | 20 | Москва"\n\n'
    '# splitlines — разбить по строкам\n'
    'text = "Строка 1\\nСтрока 2\\nСтрока 3"\n'
    'lines = text.splitlines()\n'
    'for line in lines:\n'
    '    print(line)'
) + '''
<h3>f-строки — форматирование</h3>
''' + code_block(
    'name = "Python"\n'
    'version = 3.12\n'
    'print(f"{name} v{version}")  # Python v3.12\n\n'
    '# Форматирование чисел\n'
    'pi = 3.14159\n'
    'print(f"{pi:.2f}")    # 3.14 — 2 знака после точки\n'
    'print(f"{1000000:,}") # 1,000,000 — разделитель тысяч\n'
    'print(f"{42:05d}")    # 00042 — дополнение нулями\n\n'
    '# Выравнивание\n'
    'print(f"{name:<10}|")  # Python    | (влево)\n'
    'print(f"{name:>10}|")  #     Python| (вправо)\n'
    'print(f"{name:^10}|")  #   Python  | (по центру)'
) + '''
<h3>Запомните</h3>
<ul>
<li>Строки — итерируемые: <code>for ch in "text"</code></li>
<li><code>split()</code> и <code>join()</code> — пара для разбора и сборки</li>
<li>f-строки (<code>f"..."</code>) — лучший способ форматирования</li>
<li>Строки неизменяемы: методы возвращают <strong>новую</strong> строку</li>
</ul>'''
        },
    ],

    # ── M6: Функции ───────────────────────────────────────────
    6: [
        {
            'title': 'Аргументы функций: *args и **kwargs',
            'order': 3,
            'minutes': 12,
            'code': (
                '# Позиционные и именованные аргументы\n'
                'def greet(name, greeting="Привет"):\n'
                '    print(f"{greeting}, {name}!")\n\n'
                'greet("Анна")                  # Привет, Анна!\n'
                'greet("Борис", "Здравствуй")   # Здравствуй, Борис!\n'
                'greet(greeting="Салют", name="Вера")  # именованные\n\n'
                '# *args — произвольное число позиционных\n'
                'def total(*args):\n'
                '    print(f"Аргументы: {args}")\n'
                '    return sum(args)\n\n'
                'print(total(1, 2, 3))    # 6\n'
                'print(total(10, 20))     # 30\n\n'
                '# **kwargs — произвольное число именованных\n'
                'def show_info(**kwargs):\n'
                '    for key, value in kwargs.items():\n'
                '        print(f"{key}: {value}")\n\n'
                'show_info(name="Анна", age=20, city="Москва")\n\n'
                '# Комбинация всех видов\n'
                'def func(a, b, *args, key="default", **kwargs):\n'
                '    print(a, b, args, key, kwargs)'
            ),
            'content': '''<h2>Аргументы функций: *args и **kwargs</h2>
<p>Python предлагает гибкую систему аргументов функций — от простых позиционных
до переменного числа через <code>*args</code> и <code>**kwargs</code>.</p>

<h3>Виды аргументов</h3>
''' + info_table(
    ['Вид', 'Синтаксис', 'Пример'],
    [
        ['Позиционный', '<code>def f(a, b)</code>', '<code>f(1, 2)</code>'],
        ['С умолчанием', '<code>def f(a, b=10)</code>', '<code>f(1)</code> или <code>f(1, 20)</code>'],
        ['Именованный', '<code>def f(*, key)</code>', '<code>f(key="value")</code>'],
        ['*args', '<code>def f(*args)</code>', '<code>f(1, 2, 3)</code> — кортеж'],
        ['**kwargs', '<code>def f(**kw)</code>', '<code>f(a=1, b=2)</code> — словарь'],
    ]
) + '''
<h3>*args — переменное число аргументов</h3>
<p><code>*args</code> собирает все дополнительные позиционные аргументы в <strong>кортеж</strong>:</p>
''' + code_block(
    'def average(*numbers):\n'
    '    if not numbers:\n'
    '        return 0\n'
    '    return sum(numbers) / len(numbers)\n\n'
    'print(average(4, 5, 6))      # 5.0\n'
    'print(average(10, 20))       # 15.0\n'
    'print(average(100))          # 100.0'
) + '''
<h3>**kwargs — именованные аргументы</h3>
<p><code>**kwargs</code> собирает именованные аргументы в <strong>словарь</strong>:</p>
''' + code_block(
    'def create_user(**kwargs):\n'
    '    for field, value in kwargs.items():\n'
    '        print(f"  {field} = {value}")\n\n'
    'create_user(name="Анна", age=20, role="admin")\n'
    '# name = Анна\n'
    '# age = 20\n'
    '# role = admin'
) + '''
<h3>Распаковка при вызове</h3>
''' + code_block(
    'def point(x, y, z):\n'
    '    print(f"({x}, {y}, {z})")\n\n'
    'coords = [1, 2, 3]\n'
    'point(*coords)        # распаковка списка\n\n'
    'params = {"x": 10, "y": 20, "z": 30}\n'
    'point(**params)        # распаковка словаря'
) + '''
<h3>Порядок параметров</h3>
<p>Правильный порядок: <code>def f(pos, default=val, *args, keyword, **kwargs)</code></p>
<h3>Запомните</h3>
<ul>
<li><code>*args</code> — кортеж позиционных, <code>**kwargs</code> — словарь именованных</li>
<li><code>*</code> при вызове распаковывает список, <code>**</code> — словарь</li>
<li>Аргументы со значением по умолчанию идут <strong>после</strong> обязательных</li>
</ul>'''
        },
        {
            'title': 'Лямбда-функции и функции высшего порядка',
            'order': 4,
            'minutes': 10,
            'code': (
                '# lambda — анонимная функция в одну строку\n'
                'square = lambda x: x ** 2\n'
                'print(square(5))  # 25\n\n'
                'add = lambda a, b: a + b\n'
                'print(add(3, 7))  # 10\n\n'
                '# sorted с key\n'
                'students = [("Анна", 4.5), ("Борис", 3.8), ("Вера", 4.9)]\n'
                'by_grade = sorted(students, key=lambda s: s[1], reverse=True)\n'
                'print(by_grade)  # Вера, Анна, Борис\n\n'
                '# map — применить функцию к каждому элементу\n'
                'nums = [1, 2, 3, 4, 5]\n'
                'squares = list(map(lambda x: x**2, nums))\n'
                'print(squares)  # [1, 4, 9, 16, 25]\n\n'
                '# filter — отобрать элементы\n'
                'evens = list(filter(lambda x: x % 2 == 0, nums))\n'
                'print(evens)  # [2, 4]\n\n'
                '# Функция как аргумент\n'
                'def apply_twice(func, value):\n'
                '    return func(func(value))\n\n'
                'print(apply_twice(lambda x: x + 3, 10))  # 16\n'
                'print(apply_twice(lambda x: x * 2, 5))   # 20'
            ),
            'content': '''<h2>Лямбда-функции и функции высшего порядка</h2>
<p>В Python функции — объекты первого класса: их можно передавать как аргументы,
возвращать из других функций и сохранять в переменные.</p>

<h3>lambda — анонимная функция</h3>
<p>Синтаксис: <code>lambda параметры: выражение</code></p>
''' + code_block(
    '# Обычная функция:\n'
    'def double(x):\n'
    '    return x * 2\n\n'
    '# Эквивалент через lambda:\n'
    'double = lambda x: x * 2\n\n'
    'print(double(5))  # 10'
) + '''
<p><strong>Когда использовать lambda:</strong> короткие одноразовые функции, обычно как аргумент для <code>sorted</code>, <code>map</code>, <code>filter</code>.</p>

<h3>sorted с key</h3>
''' + code_block(
    'words = ["banana", "apple", "cherry", "date"]\n\n'
    '# Сортировка по длине\n'
    'print(sorted(words, key=lambda w: len(w)))\n'
    '# ["date", "apple", "banana", "cherry"]\n\n'
    '# Сортировка словаря по значению\n'
    'scores = {"Анна": 95, "Борис": 82, "Вера": 91}\n'
    'top = sorted(scores.items(), key=lambda x: x[1], reverse=True)\n'
    'print(top)  # [("Анна", 95), ("Вера", 91), ("Борис", 82)]'
) + '''
<h3>map и filter</h3>
''' + info_table(
    ['Функция', 'Действие', 'Пример'],
    [
        ['<code>map(f, seq)</code>', 'Применить f к каждому', '<code>map(str, [1,2,3]) → ["1","2","3"]</code>'],
        ['<code>filter(f, seq)</code>', 'Оставить где f=True', '<code>filter(bool, [0,1,"",2]) → [1,2]</code>'],
    ]
) + '''
<p><strong>Альтернатива:</strong> list comprehension часто читабельнее:</p>
''' + code_block(
    '# map + lambda\n'
    'squares = list(map(lambda x: x**2, nums))\n\n'
    '# comprehension (предпочтительно)\n'
    'squares = [x**2 for x in nums]'
) + '''
<h3>Функция как аргумент</h3>
''' + code_block(
    'def apply(func, data):\n'
    '    return [func(x) for x in data]\n\n'
    'print(apply(abs, [-1, 2, -3]))     # [1, 2, 3]\n'
    'print(apply(str.upper, ["hi"]))    # ["HI"]'
) + '''
<h3>Запомните</h3>
<ul>
<li><code>lambda</code> — короткая анонимная функция для одного выражения</li>
<li><code>sorted(key=...)</code> — самое частое место для lambda</li>
<li><code>map/filter</code> работают, но comprehension обычно читабельнее</li>
<li>Функции можно передавать и возвращать как обычные объекты</li>
</ul>'''
        },
        {
            'title': 'Замыкания и вложенные функции',
            'order': 5,
            'minutes': 10,
            'code': (
                '# Вложенная функция\n'
                'def outer():\n'
                '    message = "Привет"\n'
                '    def inner():\n'
                '        print(message)  # доступ к переменной outer\n'
                '    inner()\n\n'
                'outer()  # Привет\n\n'
                '# Замыкание — inner "запоминает" переменные outer\n'
                'def make_multiplier(n):\n'
                '    def multiplier(x):\n'
                '        return x * n\n'
                '    return multiplier\n\n'
                'double = make_multiplier(2)\n'
                'triple = make_multiplier(3)\n'
                'print(double(5))   # 10\n'
                'print(triple(5))   # 15\n\n'
                '# Фабрика функций\n'
                'def make_greeting(template):\n'
                '    def greet(name):\n'
                '        return template.format(name=name)\n'
                '    return greet\n\n'
                'ru = make_greeting("Привет, {name}!")\n'
                'en = make_greeting("Hello, {name}!")\n'
                'print(ru("Анна"))   # Привет, Анна!\n'
                'print(en("Anna"))   # Hello, Anna!\n\n'
                '# nonlocal — изменение переменной замыкания\n'
                'def counter():\n'
                '    count = 0\n'
                '    def increment():\n'
                '        nonlocal count\n'
                '        count += 1\n'
                '        return count\n'
                '    return increment\n\n'
                'c = counter()\n'
                'print(c())  # 1\n'
                'print(c())  # 2\n'
                'print(c())  # 3'
            ),
            'content': '''<h2>Замыкания и вложенные функции</h2>
<p>Замыкание (closure) — это функция, которая запоминает переменные из
окружающей области видимости, даже после завершения внешней функции.</p>

<h3>Вложенные функции</h3>
''' + code_block(
    'def outer():\n'
    '    x = 10\n'
    '    def inner():\n'
    '        print(x)  # inner видит x из outer\n'
    '    inner()\n\n'
    'outer()  # 10'
) + '''
<h3>Замыкание — функция-фабрика</h3>
<p>Когда внешняя функция возвращает внутреннюю, внутренняя <strong>запоминает</strong>
все переменные из внешней:</p>
''' + code_block(
    'def power_factory(exp):\n'
    '    def power(base):\n'
    '        return base ** exp  # exp "захвачен"\n'
    '    return power\n\n'
    'square = power_factory(2)\n'
    'cube = power_factory(3)\n'
    'print(square(5))  # 25\n'
    'print(cube(5))    # 125'
) + '''
<h3>Ключевое слово nonlocal</h3>
<p>Чтобы <strong>изменить</strong> (а не только прочитать) переменную замыкания,
используйте <code>nonlocal</code>:</p>
''' + code_block(
    'def make_counter(start=0):\n'
    '    count = start\n'
    '    def increment():\n'
    '        nonlocal count\n'
    '        count += 1\n'
    '        return count\n'
    '    return increment\n\n'
    'c = make_counter()\n'
    'print(c(), c(), c())  # 1 2 3'
) + '''
<h3>Практическое применение</h3>
<ul>
<li><strong>Фабрика функций</strong> — создание настроенных функций</li>
<li><strong>Кэширование</strong> — запоминание результатов</li>
<li><strong>Декораторы</strong> — обёртки над функциями (следующий модуль)</li>
<li><strong>Callback-функции</strong> — обработчики событий</li>
</ul>
<h3>Запомните</h3>
<ul>
<li>Замыкание = внутренняя функция + захваченные переменные</li>
<li><code>nonlocal</code> — для изменения переменных замыкания</li>
<li>Каждый вызов фабрики создаёт новое независимое замыкание</li>
</ul>'''
        },
    ],

    # ── M7: Списки и массивы ──────────────────────────────────
    7: [
        {
            'title': 'Срезы списков (slicing)',
            'order': 3,
            'minutes': 10,
            'code': (
                'lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\n\n'
                '# Базовые срезы\n'
                'print(lst[2:5])    # [2, 3, 4]\n'
                'print(lst[:3])     # [0, 1, 2]\n'
                'print(lst[7:])     # [7, 8, 9]\n'
                'print(lst[-3:])    # [7, 8, 9]\n\n'
                '# С шагом\n'
                'print(lst[::2])    # [0, 2, 4, 6, 8]\n'
                'print(lst[1::2])   # [1, 3, 5, 7, 9]\n'
                'print(lst[::-1])   # [9, 8, ..., 0] — реверс!\n\n'
                '# Изменение через срез\n'
                'lst[1:4] = [10, 20, 30]\n'
                'print(lst)  # [0, 10, 20, 30, 4, 5, 6, 7, 8, 9]\n\n'
                '# Удаление через срез\n'
                'del lst[1:4]\n'
                'print(lst)  # [0, 4, 5, 6, 7, 8, 9]\n\n'
                '# Копирование списка\n'
                'copy = lst[:]  # поверхностная копия'
            ),
            'content': '''<h2>Срезы списков (slicing)</h2>
<p>Срезы — мощный механизм Python для извлечения частей последовательностей.</p>
<h3>Синтаксис: <code>lst[start:stop:step]</code></h3>
''' + info_table(
    ['Срез', 'Результат', 'Описание'],
    [
        ['<code>lst[2:5]</code>', 'Элементы 2, 3, 4', 'От start до stop-1'],
        ['<code>lst[:3]</code>', 'Первые 3', 'От начала'],
        ['<code>lst[3:]</code>', 'С 3-го до конца', 'До конца'],
        ['<code>lst[-2:]</code>', 'Последние 2', 'Отрицательный индекс'],
        ['<code>lst[::2]</code>', 'Чётные позиции', 'С шагом 2'],
        ['<code>lst[::-1]</code>', 'Реверс', 'Обратный порядок'],
    ]
) + '''
<h3>Изменение через срезы</h3>
''' + code_block(
    'lst = [1, 2, 3, 4, 5]\n'
    'lst[1:3] = [20, 30]     # замена: [1, 20, 30, 4, 5]\n'
    'lst[1:1] = [10, 15]     # вставка: [1, 10, 15, 20, 30, 4, 5]\n'
    'del lst[2:4]            # удаление: [1, 10, 4, 5]'
) + '''
<h3>Копирование списков</h3>
''' + code_block(
    'original = [1, [2, 3], 4]\n\n'
    '# Поверхностная копия (3 способа)\n'
    'copy1 = original[:]\n'
    'copy2 = list(original)\n'
    'copy3 = original.copy()\n\n'
    '# Глубокая копия (для вложенных)\n'
    'import copy\n'
    'deep = copy.deepcopy(original)'
) + '''
<h3>Запомните</h3>
<ul>
<li><code>lst[start:stop]</code> — stop не включается</li>
<li><code>lst[::-1]</code> — самый быстрый реверс</li>
<li><code>lst[:]</code> — поверхностная копия</li>
<li>Срезы создают <strong>новый</strong> список, не меняют оригинал</li>
</ul>'''
        },
        {
            'title': 'Методы списков: append, insert, pop, sort',
            'order': 4,
            'minutes': 10,
            'code': (
                'lst = [3, 1, 4, 1, 5]\n\n'
                '# Добавление\n'
                'lst.append(9)       # в конец: [3, 1, 4, 1, 5, 9]\n'
                'lst.insert(0, 0)    # по индексу: [0, 3, 1, 4, 1, 5, 9]\n'
                'lst.extend([2, 6])  # несколько: [0, 3, 1, 4, 1, 5, 9, 2, 6]\n\n'
                '# Удаление\n'
                'lst.pop()           # последний → 6\n'
                'lst.pop(0)          # по индексу → 0\n'
                'lst.remove(1)       # первое вхождение 1\n\n'
                '# Поиск\n'
                'print(lst.index(4))  # индекс первого 4\n'
                'print(lst.count(1))  # сколько раз 1\n'
                'print(4 in lst)      # True\n\n'
                '# Сортировка\n'
                'lst.sort()           # на месте, по возрастанию\n'
                'lst.sort(reverse=True)  # по убыванию\n'
                'lst.reverse()        # перевернуть\n\n'
                '# sorted() — новый список\n'
                'nums = [3, 1, 2]\n'
                'new = sorted(nums)   # nums не меняется\n'
                'print(nums, new)     # [3, 1, 2] [1, 2, 3]'
            ),
            'content': '''<h2>Методы списков</h2>
<p>Списки — самая используемая структура данных в Python. Знание методов
списков необходимо для решения большинства задач.</p>

<h3>Методы изменения списка</h3>
''' + info_table(
    ['Метод', 'Действие', 'Возвращает'],
    [
        ['<code>.append(x)</code>', 'Добавить x в конец', 'None'],
        ['<code>.insert(i, x)</code>', 'Вставить x на позицию i', 'None'],
        ['<code>.extend(lst)</code>', 'Добавить все элементы lst', 'None'],
        ['<code>.pop(i)</code>', 'Удалить и вернуть элемент i', 'Элемент'],
        ['<code>.remove(x)</code>', 'Удалить первое вхождение x', 'None'],
        ['<code>.clear()</code>', 'Очистить список', 'None'],
        ['<code>.sort()</code>', 'Сортировать на месте', 'None'],
        ['<code>.reverse()</code>', 'Перевернуть на месте', 'None'],
    ]
) + '''
<h3>Методы поиска</h3>
''' + info_table(
    ['Метод', 'Описание', 'Пример'],
    [
        ['<code>.index(x)</code>', 'Индекс первого x', '<code>[1,2,3].index(2) → 1</code>'],
        ['<code>.count(x)</code>', 'Количество x', '<code>[1,1,2].count(1) → 2</code>'],
        ['<code>x in lst</code>', 'Есть ли x?', '<code>3 in [1,2,3] → True</code>'],
    ]
) + '''
<h3>sort() vs sorted()</h3>
''' + info_table(
    ['', '<code>lst.sort()</code>', '<code>sorted(lst)</code>'],
    [
        ['Изменяет оригинал?', 'Да', 'Нет (новый список)'],
        ['Возвращает', 'None', 'Новый список'],
        ['Работает с', 'Только списками', 'Любым iterable'],
    ]
) + '''
<h3>Запомните</h3>
<ul>
<li><code>append</code> — добавить один элемент, <code>extend</code> — добавить несколько</li>
<li><code>sort()</code> меняет список, <code>sorted()</code> — нет</li>
<li><code>pop()</code> возвращает удалённый элемент, <code>remove()</code> — нет</li>
<li>Все методы изменения возвращают <code>None</code> (кроме <code>pop</code>)</li>
</ul>'''
        },
        {
            'title': 'Кортежи (tuple) и отличия от списков',
            'order': 5,
            'minutes': 10,
            'code': (
                '# Создание кортежа\n'
                't = (1, 2, 3)\n'
                'single = (42,)   # запятая обязательна для одного элемента!\n'
                'empty = ()\n'
                'packed = 1, 2, 3  # без скобок тоже кортеж\n\n'
                '# Индексация и срезы\n'
                'print(t[0])     # 1\n'
                'print(t[-1])    # 3\n'
                'print(t[1:])    # (2, 3)\n\n'
                '# Кортеж НЕЛЬЗЯ изменить\n'
                '# t[0] = 99  # TypeError!\n\n'
                '# Распаковка\n'
                'a, b, c = t\n'
                'print(a, b, c)  # 1 2 3\n\n'
                '# Обмен значений\n'
                'x, y = 10, 20\n'
                'x, y = y, x\n'
                'print(x, y)  # 20 10\n\n'
                '# Возврат нескольких значений\n'
                'def min_max(lst):\n'
                '    return min(lst), max(lst)\n\n'
                'lo, hi = min_max([3, 1, 4, 1, 5])\n'
                'print(f"Мин: {lo}, Макс: {hi}")\n\n'
                '# Кортеж как ключ словаря\n'
                'grid = {(0, 0): "start", (1, 2): "end"}\n'
                'print(grid[(0, 0)])  # start'
            ),
            'content': '''<h2>Кортежи (tuple) и отличия от списков</h2>
<p>Кортеж — неизменяемый аналог списка. Его нельзя модифицировать после создания.</p>

<h3>Создание кортежей</h3>
''' + code_block(
    't1 = (1, 2, 3)       # обычный\n'
    't2 = 1, 2, 3         # без скобок (packing)\n'
    't3 = (42,)           # один элемент — запятая обязательна!\n'
    't4 = tuple([1,2,3])  # из списка\n'
    't5 = ()              # пустой'
) + '''
<h3>Список vs Кортеж</h3>
''' + info_table(
    ['Свойство', 'list', 'tuple'],
    [
        ['Синтаксис', '<code>[1, 2, 3]</code>', '<code>(1, 2, 3)</code>'],
        ['Изменяемый?', 'Да', 'Нет'],
        ['Методы изменения', 'append, pop, sort...', 'Нет'],
        ['Ключ словаря?', 'Нет', 'Да'],
        ['Скорость', 'Чуть медленнее', 'Чуть быстрее'],
        ['Когда использовать', 'Коллекция может меняться', 'Фиксированный набор'],
    ]
) + '''
<h3>Распаковка (unpacking)</h3>
''' + code_block(
    '# Базовая распаковка\n'
    'point = (3, 7)\n'
    'x, y = point\n\n'
    '# Звёздочка — захват остатка\n'
    'first, *rest = [1, 2, 3, 4, 5]\n'
    'print(first)  # 1\n'
    'print(rest)   # [2, 3, 4, 5]\n\n'
    'head, *middle, tail = [1, 2, 3, 4, 5]\n'
    'print(head, middle, tail)  # 1 [2, 3, 4] 5'
) + '''
<h3>Когда использовать кортеж</h3>
<ul>
<li><strong>Координаты:</strong> <code>(x, y)</code>, <code>(lat, lon)</code></li>
<li><strong>Возврат нескольких значений:</strong> <code>return min_val, max_val</code></li>
<li><strong>Ключ словаря:</strong> <code>cache[(x, y)] = result</code></li>
<li><strong>Защита от изменений:</strong> данные, которые не должны меняться</li>
</ul>
<h3>Запомните</h3>
<ul>
<li>Кортеж = неизменяемый список</li>
<li><code>(42,)</code> — кортеж из одного элемента (запятая!)</li>
<li>Распаковка: <code>a, b = (1, 2)</code></li>
<li><code>*rest</code> — захват остатка при распаковке</li>
</ul>'''
        },
    ],

    # ── M8: Словари и множества ───────────────────────────────
    8: [
        {
            'title': 'Практика: подсчёт, группировка, инвертирование',
            'order': 5,
            'minutes': 12,
            'code': (
                '# Подсчёт элементов вручную\n'
                'text = "абракадабра"\n'
                'freq = {}\n'
                'for ch in text:\n'
                '    freq[ch] = freq.get(ch, 0) + 1\n'
                'print(freq)  # {"а": 5, "б": 2, "р": 2, "к": 1, "д": 1}\n\n'
                '# Counter — встроенный подсчёт\n'
                'from collections import Counter\n'
                'freq = Counter(text)\n'
                'print(freq.most_common(3))  # [("а", 5), ("б", 2), ("р", 2)]\n\n'
                '# Группировка\n'
                'students = [\n'
                '    {"name": "Анна", "group": "А"},\n'
                '    {"name": "Борис", "group": "Б"},\n'
                '    {"name": "Вера", "group": "А"},\n'
                ']\n'
                'by_group = {}\n'
                'for s in students:\n'
                '    by_group.setdefault(s["group"], []).append(s["name"])\n'
                'print(by_group)  # {"А": ["Анна", "Вера"], "Б": ["Борис"]}\n\n'
                '# Инвертирование словаря\n'
                'eng_ru = {"cat": "кот", "dog": "пёс"}\n'
                'ru_eng = {v: k for k, v in eng_ru.items()}\n'
                'print(ru_eng)  # {"кот": "cat", "пёс": "dog"}'
            ),
            'content': '''<h2>Практика: подсчёт, группировка, инвертирование</h2>
<p>Словари — мощный инструмент для обработки данных. Рассмотрим три самых
распространённых паттерна.</p>

<h3>Паттерн 1: Подсчёт элементов</h3>
''' + code_block(
    '# Подсчёт через .get()\n'
    'words = "the cat sat on the mat the cat".split()\n'
    'count = {}\n'
    'for w in words:\n'
    '    count[w] = count.get(w, 0) + 1\n'
    'print(count)  # {"the": 3, "cat": 2, "sat": 1, ...}\n\n'
    '# Или через Counter\n'
    'from collections import Counter\n'
    'count = Counter(words)\n'
    'print(count.most_common(2))  # [("the", 3), ("cat", 2)]'
) + '''
<h3>Паттерн 2: Группировка</h3>
''' + code_block(
    'from collections import defaultdict\n\n'
    'scores = [("Анна", 5), ("Борис", 4), ("Анна", 4), ("Борис", 5)]\n'
    'grouped = defaultdict(list)\n'
    'for name, score in scores:\n'
    '    grouped[name].append(score)\n\n'
    'for name, grades in grouped.items():\n'
    '    avg = sum(grades) / len(grades)\n'
    '    print(f"{name}: средний балл {avg:.1f}")\n'
    '# Анна: 4.5, Борис: 4.5'
) + '''
<h3>Паттерн 3: Инвертирование</h3>
''' + code_block(
    'original = {"a": 1, "b": 2, "c": 3}\n'
    'inverted = {v: k for k, v in original.items()}\n'
    'print(inverted)  # {1: "a", 2: "b", 3: "c"}'
) + '''
<h3>defaultdict и setdefault</h3>
''' + info_table(
    ['Способ', 'Код', 'Когда использовать'],
    [
        ['<code>.get(k, default)</code>', '<code>d.get("x", 0)</code>', 'Чтение с умолчанием'],
        ['<code>.setdefault(k, v)</code>', '<code>d.setdefault("x", [])</code>', 'Создать если нет'],
        ['<code>defaultdict</code>', '<code>defaultdict(list)</code>', 'Много группировок'],
        ['<code>Counter</code>', '<code>Counter(seq)</code>', 'Подсчёт частот'],
    ]
) + '''
<h3>Запомните</h3>
<ul>
<li><code>Counter</code> — лучший способ подсчёта частот</li>
<li><code>defaultdict(list)</code> — автоматическая группировка</li>
<li>Dict comprehension <code>{v:k for k,v in d.items()}</code> — инвертирование</li>
</ul>'''
        },
    ],

    # ── M9: Обработка исключений ──────────────────────────────
    9: [
        {
            'title': 'Типичные ошибки Python и как их исправлять',
            'order': 4,
            'minutes': 12,
            'code': (
                '# 1. NameError — переменная не определена\n'
                '# print(x)  # NameError: name "x" is not defined\n'
                'x = 10\n'
                'print(x)  # OK\n\n'
                '# 2. TypeError — неправильный тип\n'
                '# "5" + 3  # TypeError: can only concatenate str to str\n'
                'print(int("5") + 3)  # 8\n\n'
                '# 3. IndexError — индекс за пределами\n'
                'lst = [1, 2, 3]\n'
                '# lst[5]  # IndexError\n'
                'if len(lst) > 5:\n'
                '    print(lst[5])\n\n'
                '# 4. KeyError — ключ не найден\n'
                'd = {"a": 1}\n'
                '# d["b"]  # KeyError\n'
                'print(d.get("b", "не найден"))\n\n'
                '# 5. ValueError — неправильное значение\n'
                '# int("abc")  # ValueError\n'
                'try:\n'
                '    num = int(input("Число: "))\n'
                'except ValueError:\n'
                '    print("Это не число!")\n\n'
                '# 6. ZeroDivisionError\n'
                'def safe_div(a, b):\n'
                '    if b == 0:\n'
                '        return None\n'
                '    return a / b'
            ),
            'content': '''<h2>Типичные ошибки Python и как их исправлять</h2>
<p>Знание частых ошибок и способов их предотвращения — ключевой навык программиста.</p>

<h3>Самые частые ошибки</h3>
''' + info_table(
    ['Ошибка', 'Причина', 'Как исправить'],
    [
        ['<code>NameError</code>', 'Переменная не определена', 'Проверьте имя, опечатки'],
        ['<code>TypeError</code>', 'Неправильный тип данных', 'Преобразуйте тип: int(), str()'],
        ['<code>IndexError</code>', 'Индекс за пределами', 'Проверьте len() или используйте try'],
        ['<code>KeyError</code>', 'Ключ не найден в словаре', 'Используйте .get() или in'],
        ['<code>ValueError</code>', 'Некорректное значение', 'Валидация входных данных'],
        ['<code>ZeroDivisionError</code>', 'Деление на ноль', 'Проверьте делитель'],
        ['<code>AttributeError</code>', 'У объекта нет атрибута', 'Проверьте тип и метод'],
        ['<code>IndentationError</code>', 'Неправильные отступы', '4 пробела, без табов'],
        ['<code>SyntaxError</code>', 'Ошибка синтаксиса', 'Скобки, двоеточия, кавычки'],
        ['<code>FileNotFoundError</code>', 'Файл не найден', 'Проверьте путь к файлу'],
    ]
) + '''
<h3>Безопасный ввод пользователя</h3>
''' + code_block(
    'def get_int(prompt):\n'
    '    while True:\n'
    '        try:\n'
    '            return int(input(prompt))\n'
    '        except ValueError:\n'
    '            print("Ошибка! Введите целое число.")\n\n'
    'age = get_int("Возраст: ")\n'
    'print(f"Вам {age} лет")'
) + '''
<h3>Защитное программирование</h3>
''' + code_block(
    '# Безопасный доступ к словарю\n'
    'config = {"host": "localhost"}\n'
    'port = config.get("port", 8080)  # 8080 если нет ключа\n\n'
    '# Безопасный доступ к списку\n'
    'items = [10, 20]\n'
    'val = items[2] if len(items) > 2 else None\n\n'
    '# Безопасное деление\n'
    'result = a / b if b != 0 else 0'
) + '''
<h3>Когда использовать try/except</h3>
<ul>
<li><strong>Ввод пользователя</strong> — всегда может быть неправильным</li>
<li><strong>Файлы</strong> — могут не существовать</li>
<li><strong>Сеть</strong> — соединение может оборваться</li>
<li><strong>Парсинг данных</strong> — формат может быть нарушен</li>
</ul>
<h3>Запомните</h3>
<ul>
<li>Ловите <strong>конкретные</strong> исключения, а не <code>except Exception</code></li>
<li><code>.get()</code> для словарей, <code>if len() > i</code> для списков</li>
<li>Пользовательский ввод <strong>всегда</strong> оборачивайте в try/except</li>
</ul>'''
        },
        {
            'title': 'Отладка: print, assert, logging',
            'order': 5,
            'minutes': 10,
            'code': (
                '# 1. Отладка через print\n'
                'def binary_search(arr, target):\n'
                '    lo, hi = 0, len(arr) - 1\n'
                '    while lo <= hi:\n'
                '        mid = (lo + hi) // 2\n'
                '        print(f"DEBUG: lo={lo}, hi={hi}, mid={mid}, arr[mid]={arr[mid]}")\n'
                '        if arr[mid] == target:\n'
                '            return mid\n'
                '        elif arr[mid] < target:\n'
                '            lo = mid + 1\n'
                '        else:\n'
                '            hi = mid - 1\n'
                '    return -1\n\n'
                '# 2. assert — проверка предусловий\n'
                'def divide(a, b):\n'
                '    assert b != 0, "Делитель не может быть нулём"\n'
                '    return a / b\n\n'
                'assert isinstance(42, int)   # OK\n'
                '# assert 1 == 2, "Не равны"  # AssertionError!\n\n'
                '# 3. breakpoint() — встроенный отладчик\n'
                'def process(data):\n'
                '    result = []\n'
                '    for item in data:\n'
                '        # breakpoint()  # остановка для отладки\n'
                '        result.append(item * 2)\n'
                '    return result'
            ),
            'content': '''<h2>Отладка: print, assert, logging</h2>
<p>Умение находить и исправлять ошибки (debugging) — один из важнейших
навыков программиста.</p>

<h3>Метод 1: print-отладка</h3>
<p>Самый простой способ — вставить <code>print()</code> для проверки значений:</p>
''' + code_block(
    'def factorial(n):\n'
    '    result = 1\n'
    '    for i in range(1, n + 1):\n'
    '        result *= i\n'
    '        print(f"  i={i}, result={result}")  # отладка\n'
    '    return result\n\n'
    'factorial(5)\n'
    '#  i=1, result=1\n'
    '#  i=2, result=2\n'
    '#  i=3, result=6\n'
    '#  i=4, result=24\n'
    '#  i=5, result=120'
) + '''
<h3>Метод 2: assert — утверждения</h3>
<p><code>assert условие, сообщение</code> — проверяет условие; если ложно — поднимает ошибку:</p>
''' + code_block(
    'def set_age(age):\n'
    '    assert 0 < age < 150, f"Некорректный возраст: {age}"\n'
    '    return age\n\n'
    'set_age(25)   # OK\n'
    'set_age(-5)   # AssertionError: Некорректный возраст: -5'
) + '''
<h3>Метод 3: breakpoint()</h3>
<p>Python 3.7+ имеет встроенный отладчик. Вставьте <code>breakpoint()</code>
в код и запустите — программа остановится на этой строке, и вы сможете
интерактивно проверять переменные.</p>

<h3>Стратегия отладки</h3>
<ol>
<li><strong>Воспроизведите ошибку</strong> — найдите минимальный пример</li>
<li><strong>Прочитайте traceback</strong> — снизу вверх, последняя строка = ошибка</li>
<li><strong>Проверьте предположения</strong> — print или assert</li>
<li><strong>Разделяй и властвуй</strong> — комментируйте половину кода</li>
<li><strong>Резиновая утка</strong> — объясните проблему вслух</li>
</ol>
<h3>Запомните</h3>
<ul>
<li><code>print()</code> — быстро, но не забудьте удалить после</li>
<li><code>assert</code> — документирует предусловия, отключается в продакшене</li>
<li><code>breakpoint()</code> — полноценный интерактивный отладчик</li>
<li>Читайте traceback <strong>снизу вверх</strong></li>
</ul>'''
        },
    ],

    # ── M10: Алгоритмы сортировки ─────────────────────────────
    10: [
        {
            'title': 'Быстрая сортировка (QuickSort)',
            'order': 3,
            'minutes': 15,
            'code': (
                'def quicksort(arr):\n'
                '    if len(arr) <= 1:\n'
                '        return arr\n'
                '    pivot = arr[len(arr) // 2]\n'
                '    left = [x for x in arr if x < pivot]\n'
                '    middle = [x for x in arr if x == pivot]\n'
                '    right = [x for x in arr if x > pivot]\n'
                '    return quicksort(left) + middle + quicksort(right)\n\n'
                'print(quicksort([3, 6, 8, 10, 1, 2, 1]))\n'
                '# [1, 1, 2, 3, 6, 8, 10]\n\n'
                '# Сравнение алгоритмов по времени\n'
                'import time\n'
                'import random\n\n'
                'data = [random.randint(0, 10000) for _ in range(10000)]\n\n'
                't0 = time.time()\n'
                'sorted_data = quicksort(data)\n'
                't1 = time.time()\n'
                'print(f"QuickSort: {t1-t0:.4f} сек")\n\n'
                't0 = time.time()\n'
                'sorted_builtin = sorted(data)\n'
                't1 = time.time()\n'
                'print(f"Built-in: {t1-t0:.4f} сек")'
            ),
            'content': '''<h2>Быстрая сортировка (QuickSort)</h2>
<p>QuickSort — один из самых популярных алгоритмов сортировки. Средняя сложность O(n log n),
что значительно быстрее пузырьковой O(n^2).</p>

<h3>Принцип "Разделяй и властвуй"</h3>
<ol>
<li><strong>Выбрать опорный элемент</strong> (pivot)</li>
<li><strong>Разделить</strong> массив: меньше pivot | равные | больше pivot</li>
<li><strong>Рекурсивно</strong> отсортировать левую и правую части</li>
<li><strong>Соединить</strong> результаты</li>
</ol>

''' + code_block(
    'def quicksort(arr):\n'
    '    if len(arr) <= 1:\n'
    '        return arr\n\n'
    '    pivot = arr[len(arr) // 2]  # средний элемент\n'
    '    left = [x for x in arr if x < pivot]\n'
    '    middle = [x for x in arr if x == pivot]\n'
    '    right = [x for x in arr if x > pivot]\n\n'
    '    return quicksort(left) + middle + quicksort(right)'
) + '''
<h3>Сравнение сортировок</h3>
''' + info_table(
    ['Алгоритм', 'Лучший', 'Средний', 'Худший', 'Память'],
    [
        ['Пузырьковая', 'O(n)', 'O(n^2)', 'O(n^2)', 'O(1)'],
        ['Вставками', 'O(n)', 'O(n^2)', 'O(n^2)', 'O(1)'],
        ['Слиянием', 'O(n log n)', 'O(n log n)', 'O(n log n)', 'O(n)'],
        ['<strong>QuickSort</strong>', 'O(n log n)', 'O(n log n)', 'O(n^2)', 'O(log n)'],
        ['Python sorted()', 'O(n)', 'O(n log n)', 'O(n log n)', 'O(n)'],
    ]
) + '''
<h3>Выбор опорного элемента</h3>
<ul>
<li><strong>Первый/последний</strong> — плохо для отсортированных данных (O(n^2))</li>
<li><strong>Средний</strong> — хороший компромисс</li>
<li><strong>Случайный</strong> — лучшая защита от худшего случая</li>
<li><strong>Медиана из трёх</strong> — оптимальный выбор</li>
</ul>
<h3>Запомните</h3>
<ul>
<li>QuickSort: средняя сложность O(n log n), на практике самый быстрый</li>
<li>Встроенный <code>sorted()</code> использует Timsort — ещё лучше</li>
<li>Всегда предпочитайте <code>sorted()</code>/<code>.sort()</code> своей реализации</li>
</ul>'''
        },
        {
            'title': 'Стабильность, ключи сортировки, кастомные компараторы',
            'order': 4,
            'minutes': 10,
            'code': (
                '# Сортировка с key\n'
                'words = ["banana", "apple", "cherry", "date"]\n'
                'print(sorted(words, key=len))  # по длине\n\n'
                '# Сортировка объектов\n'
                'students = [\n'
                '    {"name": "Анна", "grade": 4.5},\n'
                '    {"name": "Борис", "grade": 3.8},\n'
                '    {"name": "Вера", "grade": 4.9},\n'
                ']\n'
                'by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)\n'
                'for s in by_grade:\n'
                '    print(f\'{s["name"]}: {s["grade"]}\')\n\n'
                '# Множественная сортировка\n'
                'data = [(1, "b"), (2, "a"), (1, "a"), (2, "b")]\n'
                'print(sorted(data))  # (1,"a"), (1,"b"), (2,"a"), (2,"b")\n\n'
                '# Сортировка по нескольким полям\n'
                'from operator import itemgetter\n'
                'records = [\n'
                '    ("Анна", "Б", 4),\n'
                '    ("Борис", "А", 5),\n'
                '    ("Вера", "Б", 5),\n'
                ']\n'
                '# Сначала по группе, потом по оценке (убывание)\n'
                'result = sorted(records, key=lambda r: (r[1], -r[2]))\n'
                'print(result)'
            ),
            'content': '''<h2>Стабильность, ключи, кастомные компараторы</h2>
<p>Python предлагает мощные возможности для настройки сортировки.</p>

<h3>Стабильная сортировка</h3>
<p>Python sort() и sorted() — <strong>стабильные</strong>: элементы с одинаковым
ключом сохраняют исходный порядок. Это позволяет сортировать в несколько проходов.</p>

<h3>Параметр key</h3>
''' + info_table(
    ['Задача', 'key'],
    [
        ['По длине строки', '<code>key=len</code>'],
        ['Без учёта регистра', '<code>key=str.lower</code>'],
        ['По последнему символу', '<code>key=lambda s: s[-1]</code>'],
        ['По абсолютному значению', '<code>key=abs</code>'],
        ['По полю словаря', '<code>key=lambda d: d["age"]</code>'],
        ['По нескольким полям', '<code>key=lambda x: (x[0], -x[1])</code>'],
    ]
) + '''
<h3>Множественная сортировка</h3>
''' + code_block(
    '# Сортировка по фамилии, затем по имени\n'
    'people = [("Иванов", "Борис"), ("Иванов", "Анна"), ("Петров", "Вера")]\n'
    'result = sorted(people)  # кортежи сравниваются поэлементно\n'
    '# [("Иванов", "Анна"), ("Иванов", "Борис"), ("Петров", "Вера")]\n\n'
    '# Сортировка по возрасту (убывание), затем по имени\n'
    'students = [("Анна", 20), ("Борис", 22), ("Вера", 20)]\n'
    'result = sorted(students, key=lambda s: (-s[1], s[0]))\n'
    '# [("Борис", 22), ("Анна", 20), ("Вера", 20)]'
) + '''
<h3>operator.itemgetter и attrgetter</h3>
''' + code_block(
    'from operator import itemgetter, attrgetter\n\n'
    '# itemgetter — для кортежей/списков/словарей\n'
    'data = [("b", 2), ("a", 3), ("c", 1)]\n'
    'sorted(data, key=itemgetter(1))  # по второму элементу\n\n'
    '# attrgetter — для объектов с атрибутами\n'
    'class Student:\n'
    '    def __init__(self, name, grade):\n'
    '        self.name = name\n'
    '        self.grade = grade\n\n'
    'students = [Student("Анна", 4.5), Student("Борис", 3.8)]\n'
    'sorted(students, key=attrgetter("grade"))'
) + '''
<h3>Запомните</h3>
<ul>
<li>Python sort — <strong>стабильный</strong> (Timsort)</li>
<li><code>key=</code> принимает функцию, применяемую к каждому элементу</li>
<li>Кортежи для множественной сортировки: <code>key=lambda x: (x[0], -x[1])</code></li>
<li><code>reverse=True</code> для сортировки по убыванию</li>
</ul>'''
        },
    ],

    # ── M11: Рекурсия ─────────────────────────────────────────
    11: [
        {
            'title': 'Рекурсивные структуры данных: деревья и вложенные списки',
            'order': 2,
            'minutes': 12,
            'code': (
                '# Обход вложенного списка\n'
                'def flatten(lst):\n'
                '    result = []\n'
                '    for item in lst:\n'
                '        if isinstance(item, list):\n'
                '            result.extend(flatten(item))\n'
                '        else:\n'
                '            result.append(item)\n'
                '    return result\n\n'
                'nested = [1, [2, [3, 4], 5], [6, 7]]\n'
                'print(flatten(nested))  # [1, 2, 3, 4, 5, 6, 7]\n\n'
                '# Файловая система — рекурсивная структура\n'
                'fs = {\n'
                '    "type": "dir", "name": "root",\n'
                '    "children": [\n'
                '        {"type": "file", "name": "readme.txt", "size": 100},\n'
                '        {"type": "dir", "name": "src", "children": [\n'
                '            {"type": "file", "name": "main.py", "size": 500},\n'
                '            {"type": "file", "name": "utils.py", "size": 300},\n'
                '        ]},\n'
                '    ]\n'
                '}\n\n'
                'def total_size(node):\n'
                '    if node["type"] == "file":\n'
                '        return node["size"]\n'
                '    return sum(total_size(ch) for ch in node["children"])\n\n'
                'print(f"Размер: {total_size(fs)} байт")  # 900'
            ),
            'content': '''<h2>Рекурсивные структуры данных</h2>
<p>Рекурсия идеально подходит для обработки данных, которые сами по себе
имеют рекурсивную природу: деревья, вложенные списки, файловые системы.</p>

<h3>Вложенные списки</h3>
''' + code_block(
    'def flatten(lst):\n'
    '    """Превращает вложенный список в плоский."""\n'
    '    result = []\n'
    '    for item in lst:\n'
    '        if isinstance(item, list):\n'
    '            result.extend(flatten(item))  # рекурсия\n'
    '        else:\n'
    '            result.append(item)\n'
    '    return result\n\n'
    'print(flatten([1, [2, [3]], [[4, 5]]]))  # [1, 2, 3, 4, 5]'
) + '''
<h3>Обход дерева</h3>
''' + code_block(
    'tree = {\n'
    '    "value": 1,\n'
    '    "left": {\n'
    '        "value": 2,\n'
    '        "left": {"value": 4, "left": None, "right": None},\n'
    '        "right": {"value": 5, "left": None, "right": None}\n'
    '    },\n'
    '    "right": {"value": 3, "left": None, "right": None}\n'
    '}\n\n'
    'def tree_sum(node):\n'
    '    if node is None:\n'
    '        return 0\n'
    '    return node["value"] + tree_sum(node["left"]) + tree_sum(node["right"])\n\n'
    'print(tree_sum(tree))  # 15'
) + '''
<h3>Рекурсивный обход файловой системы</h3>
''' + code_block(
    'import os\n\n'
    'def list_files(path, indent=0):\n'
    '    prefix = "  " * indent\n'
    '    print(f"{prefix}{os.path.basename(path)}/")\n'
    '    for item in sorted(os.listdir(path)):\n'
    '        full = os.path.join(path, item)\n'
    '        if os.path.isdir(full):\n'
    '            list_files(full, indent + 1)\n'
    '        else:\n'
    '            print(f"{prefix}  {item}")'
) + '''
<h3>Запомните</h3>
<ul>
<li>Рекурсивные данные → рекурсивные функции</li>
<li>Всегда проверяйте базовый случай: <code>None</code>, пустой список</li>
<li>Деревья, графы, JSON — типичные рекурсивные структуры</li>
</ul>'''
        },
        {
            'title': 'Классические рекурсивные задачи',
            'order': 3,
            'minutes': 12,
            'code': (
                '# 1. Факториал\n'
                'def factorial(n):\n'
                '    if n <= 1:\n'
                '        return 1\n'
                '    return n * factorial(n - 1)\n\n'
                '# 2. Фибоначчи (наивный — медленный!)\n'
                'def fib(n):\n'
                '    if n <= 1:\n'
                '        return n\n'
                '    return fib(n-1) + fib(n-2)\n\n'
                '# 3. Фибоначчи с мемоизацией\n'
                'from functools import lru_cache\n\n'
                '@lru_cache(maxsize=None)\n'
                'def fib_fast(n):\n'
                '    if n <= 1:\n'
                '        return n\n'
                '    return fib_fast(n-1) + fib_fast(n-2)\n\n'
                'print(fib_fast(100))  # мгновенно!\n\n'
                '# 4. Степень числа\n'
                'def power(base, exp):\n'
                '    if exp == 0:\n'
                '        return 1\n'
                '    return base * power(base, exp - 1)\n\n'
                '# 5. Сумма цифр числа\n'
                'def digit_sum(n):\n'
                '    if n < 10:\n'
                '        return n\n'
                '    return n % 10 + digit_sum(n // 10)\n\n'
                'print(digit_sum(12345))  # 15\n\n'
                '# 6. Палиндром\n'
                'def is_palindrome(s):\n'
                '    if len(s) <= 1:\n'
                '        return True\n'
                '    return s[0] == s[-1] and is_palindrome(s[1:-1])\n\n'
                'print(is_palindrome("racecar"))  # True'
            ),
            'content': '''<h2>Классические рекурсивные задачи</h2>
<p>Эти задачи помогают понять принцип рекурсии и часто встречаются на собеседованиях.</p>

<h3>Шаблон рекурсивной функции</h3>
''' + code_block(
    'def recursive_func(data):\n'
    '    # 1. Базовый случай (выход из рекурсии)\n'
    '    if простейший_случай:\n'
    '        return результат\n'
    '    \n'
    '    # 2. Рекурсивный случай (уменьшаем задачу)\n'
    '    return recursive_func(уменьшенные_данные)'
) + '''
<h3>Классические задачи</h3>
''' + info_table(
    ['Задача', 'Базовый случай', 'Рекурсивный случай'],
    [
        ['Факториал n!', 'n <= 1: return 1', 'n * f(n-1)'],
        ['Фибоначчи', 'n <= 1: return n', 'f(n-1) + f(n-2)'],
        ['Степень x^n', 'n == 0: return 1', 'x * power(x, n-1)'],
        ['Сумма цифр', 'n < 10: return n', 'n%10 + f(n//10)'],
        ['Палиндром', 'len <= 1: True', 's[0]==s[-1] and f(s[1:-1])'],
        ['Бинарный поиск', 'lo > hi: return -1', 'сравнить mid, сузить'],
    ]
) + '''
<h3>Мемоизация — ускорение рекурсии</h3>
<p>Наивный Фибоначчи имеет экспоненциальную сложность O(2^n).
С мемоизацией — O(n):</p>
''' + code_block(
    'from functools import lru_cache\n\n'
    '@lru_cache(maxsize=None)\n'
    'def fib(n):\n'
    '    if n <= 1:\n'
    '        return n\n'
    '    return fib(n-1) + fib(n-2)\n\n'
    'print(fib(100))  # 354224848179261915075 — мгновенно!'
) + '''
<h3>Рекурсия vs итерация</h3>
''' + info_table(
    ['', 'Рекурсия', 'Итерация'],
    [
        ['Читабельность', 'Элегантнее для деревьев/разбиений', 'Проще для линейных задач'],
        ['Производительность', 'Медленнее (вызовы функций)', 'Быстрее'],
        ['Память', 'Стек вызовов (ограничен)', 'Постоянная'],
        ['Лимит', 'Python: ~1000 вызовов', 'Без ограничений'],
    ]
) + '''
<h3>Запомните</h3>
<ul>
<li>Каждая рекурсия = базовый случай + рекурсивный шаг</li>
<li>Задача должна <strong>уменьшаться</strong> на каждом шаге</li>
<li><code>@lru_cache</code> ускоряет рекурсию с повторными вызовами</li>
<li>Предел стека Python: ~1000 (можно увеличить через <code>sys.setrecursionlimit</code>)</li>
</ul>'''
        },
        {
            'title': 'Ханойские башни и генерация комбинаций',
            'order': 4,
            'minutes': 12,
            'code': (
                '# Ханойские башни\n'
                'def hanoi(n, src="A", dst="C", tmp="B"):\n'
                '    if n == 1:\n'
                '        print(f"  {src} -> {dst}")\n'
                '        return\n'
                '    hanoi(n-1, src, tmp, dst)\n'
                '    print(f"  {src} -> {dst}")\n'
                '    hanoi(n-1, tmp, dst, src)\n\n'
                'print("Ханойские башни (3 диска):")\n'
                'hanoi(3)\n\n'
                '# Генерация всех перестановок\n'
                'def permutations(lst):\n'
                '    if len(lst) <= 1:\n'
                '        return [lst]\n'
                '    result = []\n'
                '    for i, elem in enumerate(lst):\n'
                '        rest = lst[:i] + lst[i+1:]\n'
                '        for perm in permutations(rest):\n'
                '            result.append([elem] + perm)\n'
                '    return result\n\n'
                'print(permutations([1, 2, 3]))\n\n'
                '# Генерация подмножеств\n'
                'def subsets(lst):\n'
                '    if not lst:\n'
                '        return [[]]\n'
                '    first = lst[0]\n'
                '    rest_subs = subsets(lst[1:])\n'
                '    with_first = [[first] + s for s in rest_subs]\n'
                '    return rest_subs + with_first\n\n'
                'print(subsets([1, 2, 3]))\n'
                '# [[], [3], [2], [2,3], [1], [1,3], [1,2], [1,2,3]]'
            ),
            'content': '''<h2>Ханойские башни и генерация комбинаций</h2>
<p>Классические задачи, которые элегантно решаются рекурсией.</p>

<h3>Ханойские башни</h3>
<p>Нужно переместить n дисков с колышка A на C, используя B.
Правило: нельзя класть больший диск на меньший.</p>
''' + code_block(
    'def hanoi(n, src="A", dst="C", tmp="B"):\n'
    '    if n == 1:\n'
    '        print(f"{src} -> {dst}")\n'
    '        return\n'
    '    hanoi(n-1, src, tmp, dst)  # n-1 дисков на tmp\n'
    '    print(f"{src} -> {dst}")    # большой диск на dst\n'
    '    hanoi(n-1, tmp, dst, src)  # n-1 дисков на dst'
) + '''
<p>Для n дисков нужно <strong>2^n - 1</strong> ходов (3 диска = 7 ходов).</p>

<h3>Генерация перестановок</h3>
''' + code_block(
    'def permutations(lst):\n'
    '    if len(lst) <= 1:\n'
    '        return [lst[:]]\n'
    '    result = []\n'
    '    for i in range(len(lst)):\n'
    '        rest = lst[:i] + lst[i+1:]\n'
    '        for p in permutations(rest):\n'
    '            result.append([lst[i]] + p)\n'
    '    return result\n\n'
    '# [1,2,3] -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]'
) + '''
<h3>Генерация подмножеств</h3>
''' + code_block(
    'def subsets(lst):\n'
    '    if not lst:\n'
    '        return [[]]\n'
    '    rest = subsets(lst[1:])\n'
    '    return rest + [[lst[0]] + s for s in rest]\n\n'
    '# [1,2] -> [[], [2], [1], [1,2]]'
) + '''
<h3>Встроенная библиотека itertools</h3>
''' + code_block(
    'from itertools import permutations, combinations\n\n'
    'list(permutations([1,2,3]))       # 6 перестановок\n'
    'list(combinations([1,2,3,4], 2))  # 6 комбинаций по 2'
) + '''
<h3>Запомните</h3>
<ul>
<li>Ханойские башни: 2^n - 1 ходов</li>
<li>Перестановок n элементов: n! штук</li>
<li>Подмножеств: 2^n штук</li>
<li>В реальном коде используйте <code>itertools</code></li>
</ul>'''
        },
        {
            'title': 'Рекурсия vs итерация: когда что использовать',
            'order': 5,
            'minutes': 10,
            'code': (
                '# Пример: факториал обоими способами\n\n'
                '# Рекурсивно\n'
                'def fact_rec(n):\n'
                '    if n <= 1:\n'
                '        return 1\n'
                '    return n * fact_rec(n - 1)\n\n'
                '# Итеративно\n'
                'def fact_iter(n):\n'
                '    result = 1\n'
                '    for i in range(2, n + 1):\n'
                '        result *= i\n'
                '    return result\n\n'
                '# Пример: обход дерева итеративно (через стек)\n'
                'def tree_sum_iter(root):\n'
                '    if root is None:\n'
                '        return 0\n'
                '    stack = [root]\n'
                '    total = 0\n'
                '    while stack:\n'
                '        node = stack.pop()\n'
                '        total += node["value"]\n'
                '        if node["left"]:\n'
                '            stack.append(node["left"])\n'
                '        if node["right"]:\n'
                '            stack.append(node["right"])\n'
                '    return total\n\n'
                '# Хвостовая рекурсия (Python не оптимизирует!)\n'
                'def fact_tail(n, acc=1):\n'
                '    if n <= 1:\n'
                '        return acc\n'
                '    return fact_tail(n - 1, acc * n)  # хвостовой вызов'
            ),
            'content': '''<h2>Рекурсия vs итерация</h2>
<p>Любую рекурсию можно переписать итеративно (и наоборот).
Выбор зависит от задачи.</p>

<h3>Когда использовать рекурсию</h3>
<ul>
<li>Обход деревьев и графов</li>
<li>Задачи "разделяй и властвуй" (QuickSort, MergeSort)</li>
<li>Генерация комбинаций, перестановок</li>
<li>Обработка вложенных структур (JSON, XML)</li>
</ul>

<h3>Когда использовать итерацию</h3>
<ul>
<li>Линейные вычисления (сумма, произведение)</li>
<li>Обход массивов и списков</li>
<li>Когда важна производительность</li>
<li>Когда глубина может превысить 1000</li>
</ul>

<h3>Конвертация рекурсии в итерацию</h3>
<p>Рекурсию можно заменить циклом + стек:</p>
''' + code_block(
    '# Рекурсивный обход дерева\n'
    'def traverse_rec(node):\n'
    '    if node is None: return\n'
    '    print(node.value)\n'
    '    traverse_rec(node.left)\n'
    '    traverse_rec(node.right)\n\n'
    '# Итеративный обход (через стек)\n'
    'def traverse_iter(root):\n'
    '    stack = [root]\n'
    '    while stack:\n'
    '        node = stack.pop()\n'
    '        if node is None: continue\n'
    '        print(node.value)\n'
    '        stack.append(node.right)\n'
    '        stack.append(node.left)'
) + '''
<h3>Сравнение</h3>
''' + info_table(
    ['Критерий', 'Рекурсия', 'Итерация'],
    [
        ['Читабельность', 'Лучше для деревьев', 'Лучше для линейных задач'],
        ['Память', 'O(глубина) — стек вызовов', 'O(1) или O(n) — явный стек'],
        ['Скорость', 'Медленнее (overhead вызовов)', 'Быстрее'],
        ['Лимит Python', '~1000 вызовов', 'Нет ограничений'],
        ['Отладка', 'Труднее', 'Проще'],
    ]
) + '''
<h3>Запомните</h3>
<ul>
<li>Рекурсия — для рекурсивных структур (деревья, графы)</li>
<li>Итерация — для линейных задач и производительности</li>
<li>Любую рекурсию можно заменить циклом + стек</li>
<li>Python не оптимизирует хвостовую рекурсию</li>
</ul>'''
        },
    ],

    # ── M12: Работа с файлами ─────────────────────────────────
    12: [
        {
            'title': 'Режимы открытия и кодировки',
            'order': 2,
            'minutes': 10,
            'code': (
                '# Режимы открытия файла\n'
                '# "r"  — чтение (по умолчанию)\n'
                '# "w"  — запись (перезапись!)\n'
                '# "a"  — дополнение (в конец)\n'
                '# "x"  — создание (ошибка если существует)\n'
                '# "rb" — чтение бинарного\n'
                '# "r+" — чтение + запись\n\n'
                '# Чтение с кодировкой\n'
                'with open("data.txt", "r", encoding="utf-8") as f:\n'
                '    text = f.read()\n\n'
                '# Запись с кодировкой\n'
                'with open("output.txt", "w", encoding="utf-8") as f:\n'
                '    f.write("Привет, мир!\\n")\n\n'
                '# Дополнение (append)\n'
                'with open("log.txt", "a", encoding="utf-8") as f:\n'
                '    f.write("Новая запись\\n")\n\n'
                '# Бинарный режим\n'
                'with open("image.png", "rb") as f:\n'
                '    header = f.read(8)  # первые 8 байт\n'
                '    print(header)  # b"\\x89PNG\\r\\n\\x1a\\n"'
            ),
            'content': '''<h2>Режимы открытия и кодировки</h2>
<p>Правильный выбор режима открытия и кодировки файла — ключ к надёжной работе с файлами.</p>

<h3>Режимы открытия</h3>
''' + info_table(
    ['Режим', 'Описание', 'Файл должен существовать?'],
    [
        ['<code>"r"</code>', 'Чтение (по умолчанию)', 'Да'],
        ['<code>"w"</code>', 'Запись (перезапись!)', 'Нет (создаст)'],
        ['<code>"a"</code>', 'Дополнение в конец', 'Нет (создаст)'],
        ['<code>"x"</code>', 'Создание (ошибка если есть)', 'Нет'],
        ['<code>"r+"</code>', 'Чтение + запись', 'Да'],
        ['<code>"rb"</code>', 'Бинарное чтение', 'Да'],
        ['<code>"wb"</code>', 'Бинарная запись', 'Нет'],
    ]
) + '''
<h3>Кодировки</h3>
<p><strong>Всегда указывайте <code>encoding="utf-8"</code></strong>. Без этого Python
на Windows использует cp1251, что может вызвать ошибки.</p>
''' + code_block(
    '# Правильно\n'
    'with open("file.txt", "r", encoding="utf-8") as f:\n'
    '    data = f.read()\n\n'
    '# Обработка ошибок кодировки\n'
    'with open("file.txt", "r", encoding="utf-8", errors="replace") as f:\n'
    '    data = f.read()  # некорректные символы заменятся на ?'
) + '''
<h3>Конструкция with</h3>
<p><code>with</code> гарантирует закрытие файла даже при ошибке:</p>
''' + code_block(
    '# Правильно (with закроет автоматически)\n'
    'with open("data.txt") as f:\n'
    '    content = f.read()\n\n'
    '# Плохо (файл может не закрыться при ошибке)\n'
    'f = open("data.txt")\n'
    'content = f.read()\n'
    'f.close()  # может не выполниться!'
) + '''
<h3>Запомните</h3>
<ul>
<li><code>"w"</code> перезаписывает файл полностью — будьте осторожны!</li>
<li>Всегда используйте <code>with open(...)</code></li>
<li>Всегда указывайте <code>encoding="utf-8"</code></li>
<li>Для изображений/бинарных данных: <code>"rb"</code>/<code>"wb"</code></li>
</ul>'''
        },
        {
            'title': 'Построчное чтение и обработка данных',
            'order': 3,
            'minutes': 10,
            'code': (
                '# Чтение всех строк\n'
                'with open("data.txt", encoding="utf-8") as f:\n'
                '    lines = f.readlines()  # список строк\n\n'
                '# Построчное чтение (экономно по памяти)\n'
                'with open("data.txt", encoding="utf-8") as f:\n'
                '    for line in f:\n'
                '        line = line.strip()  # убрать \\n\n'
                '        if line:  # пропустить пустые\n'
                '            print(line)\n\n'
                '# Подсчёт слов в файле\n'
                'word_count = 0\n'
                'with open("text.txt", encoding="utf-8") as f:\n'
                '    for line in f:\n'
                '        word_count += len(line.split())\n'
                'print(f"Слов: {word_count}")\n\n'
                '# Чтение CSV вручную\n'
                'with open("students.csv", encoding="utf-8") as f:\n'
                '    header = f.readline().strip().split(",")\n'
                '    for line in f:\n'
                '        values = line.strip().split(",")\n'
                '        student = dict(zip(header, values))\n'
                '        print(student)\n\n'
                '# Запись результатов\n'
                'results = [("Анна", 95), ("Борис", 82)]\n'
                'with open("results.txt", "w", encoding="utf-8") as f:\n'
                '    for name, score in results:\n'
                '        f.write(f"{name}: {score}\\n")'
            ),
            'content': '''<h2>Построчное чтение и обработка данных</h2>
<p>Для больших файлов читать всё содержимое сразу — плохая идея.
Построчное чтение экономит память.</p>

<h3>Три способа чтения</h3>
''' + info_table(
    ['Метод', 'Возвращает', 'Память'],
    [
        ['<code>f.read()</code>', 'Весь файл как строку', 'Весь файл в RAM'],
        ['<code>f.readlines()</code>', 'Список строк', 'Весь файл в RAM'],
        ['<code>for line in f:</code>', 'Строки по одной', 'Одна строка в RAM'],
    ]
) + '''
<h3>Построчная обработка</h3>
''' + code_block(
    'with open("data.txt", encoding="utf-8") as f:\n'
    '    for line_num, line in enumerate(f, 1):\n'
    '        line = line.strip()  # убрать \\n и пробелы\n'
    '        if not line:\n'
    '            continue  # пропустить пустые\n'
    '        print(f"{line_num}: {line}")'
) + '''
<h3>Фильтрация и преобразование</h3>
''' + code_block(
    '# Прочитать числа из файла и найти максимум\n'
    'with open("numbers.txt", encoding="utf-8") as f:\n'
    '    numbers = [int(line.strip()) for line in f if line.strip()]\n\n'
    'print(f"Max: {max(numbers)}")\n'
    'print(f"Avg: {sum(numbers) / len(numbers):.1f}")'
) + '''
<h3>Запись в файл</h3>
''' + code_block(
    '# write — записывает строку\n'
    'with open("out.txt", "w", encoding="utf-8") as f:\n'
    '    f.write("Строка 1\\n")\n'
    '    f.write("Строка 2\\n")\n\n'
    '# writelines — записывает список строк\n'
    'lines = ["Первая\\n", "Вторая\\n", "Третья\\n"]\n'
    'with open("out.txt", "w", encoding="utf-8") as f:\n'
    '    f.writelines(lines)\n\n'
    '# print в файл\n'
    'with open("out.txt", "w", encoding="utf-8") as f:\n'
    '    print("Удобная запись", file=f)'
) + '''
<h3>Запомните</h3>
<ul>
<li><code>for line in f:</code> — лучший способ для больших файлов</li>
<li><code>.strip()</code> — убирает <code>\\n</code> в конце строк</li>
<li><code>f.write()</code> не добавляет <code>\\n</code> автоматически</li>
<li><code>print(..., file=f)</code> — удобная альтернатива write</li>
</ul>'''
        },
        {
            'title': 'Модуль pathlib: современная работа с путями',
            'order': 4,
            'minutes': 10,
            'code': (
                'from pathlib import Path\n\n'
                '# Создание пути\n'
                'p = Path("data") / "reports" / "2024"\n'
                'print(p)  # data/reports/2024\n\n'
                '# Информация о пути\n'
                'f = Path("script.py")\n'
                'print(f.name)      # script.py\n'
                'print(f.stem)      # script\n'
                'print(f.suffix)    # .py\n'
                'print(f.parent)    # .\n'
                'print(f.exists())  # True/False\n\n'
                '# Поиск файлов\n'
                'for py_file in Path(".").glob("*.py"):\n'
                '    print(py_file)\n\n'
                '# Рекурсивный поиск\n'
                'for txt in Path(".").rglob("*.txt"):\n'
                '    print(txt)\n\n'
                '# Чтение/запись\n'
                'p = Path("hello.txt")\n'
                'p.write_text("Привет!", encoding="utf-8")\n'
                'content = p.read_text(encoding="utf-8")\n\n'
                '# Создание директорий\n'
                'Path("output/reports").mkdir(parents=True, exist_ok=True)'
            ),
            'content': '''<h2>Модуль pathlib: современная работа с путями</h2>
<p><code>pathlib</code> — современный способ работы с файловой системой в Python 3.
Он удобнее и безопаснее, чем <code>os.path</code>.</p>

<h3>Создание путей</h3>
''' + code_block(
    'from pathlib import Path\n\n'
    '# Оператор / для объединения путей\n'
    'data_dir = Path("project") / "data" / "raw"\n'
    'print(data_dir)  # project/data/raw\n\n'
    '# Текущая директория\n'
    'cwd = Path.cwd()\n'
    '# Домашняя директория\n'
    'home = Path.home()'
) + '''
<h3>Свойства пути</h3>
''' + info_table(
    ['Свойство', 'Пример для Path("data/report.csv")', 'Результат'],
    [
        ['<code>.name</code>', 'Имя файла', 'report.csv'],
        ['<code>.stem</code>', 'Имя без расширения', 'report'],
        ['<code>.suffix</code>', 'Расширение', '.csv'],
        ['<code>.parent</code>', 'Родительская папка', 'data'],
        ['<code>.exists()</code>', 'Существует?', 'True/False'],
        ['<code>.is_file()</code>', 'Это файл?', 'True/False'],
        ['<code>.is_dir()</code>', 'Это папка?', 'True/False'],
    ]
) + '''
<h3>Поиск файлов</h3>
''' + code_block(
    '# Все .py файлы в текущей папке\n'
    'for f in Path(".").glob("*.py"):\n'
    '    print(f.name)\n\n'
    '# Рекурсивный поиск (все подпапки)\n'
    'for f in Path(".").rglob("*.txt"):\n'
    '    print(f)\n\n'
    '# Все файлы определённого размера\n'
    'large = [f for f in Path(".").rglob("*") if f.is_file() and f.stat().st_size > 1_000_000]'
) + '''
<h3>Быстрое чтение/запись</h3>
''' + code_block(
    'p = Path("notes.txt")\n\n'
    '# Запись\n'
    'p.write_text("Содержимое файла", encoding="utf-8")\n\n'
    '# Чтение\n'
    'text = p.read_text(encoding="utf-8")\n\n'
    '# Бинарные данные\n'
    'data = Path("image.png").read_bytes()'
) + '''
<h3>Запомните</h3>
<ul>
<li><code>Path("a") / "b"</code> — кроссплатформенное объединение путей</li>
<li><code>.glob("*.py")</code> — поиск по шаблону</li>
<li><code>.rglob("*")</code> — рекурсивный поиск</li>
<li><code>read_text()</code>/<code>write_text()</code> — быстрое чтение/запись</li>
<li>pathlib лучше os.path — используйте его в новом коде</li>
</ul>'''
        },
        {
            'title': 'Работа с CSV и JSON файлами',
            'order': 5,
            'minutes': 12,
            'code': (
                'import csv\n'
                'import json\n\n'
                '# === CSV ===\n'
                '# Запись CSV\n'
                'with open("students.csv", "w", newline="", encoding="utf-8") as f:\n'
                '    writer = csv.writer(f)\n'
                '    writer.writerow(["Имя", "Оценка", "Группа"])\n'
                '    writer.writerow(["Анна", 5, "А"])\n'
                '    writer.writerow(["Борис", 4, "Б"])\n\n'
                '# Чтение CSV\n'
                'with open("students.csv", encoding="utf-8") as f:\n'
                '    reader = csv.DictReader(f)\n'
                '    for row in reader:\n'
                '        print(f\'{row["Имя"]}: {row["Оценка"]}\')\n\n'
                '# === JSON ===\n'
                '# Запись JSON\n'
                'data = {"students": [{"name": "Анна", "grade": 5}]}\n'
                'with open("data.json", "w", encoding="utf-8") as f:\n'
                '    json.dump(data, f, ensure_ascii=False, indent=2)\n\n'
                '# Чтение JSON\n'
                'with open("data.json", encoding="utf-8") as f:\n'
                '    loaded = json.load(f)\n'
                '    print(loaded["students"][0]["name"])'
            ),
            'content': '''<h2>Работа с CSV и JSON файлами</h2>
<p>CSV и JSON — два самых распространённых формата данных.</p>

<h3>CSV — табличные данные</h3>
''' + code_block(
    'import csv\n\n'
    '# Чтение CSV\n'
    'with open("data.csv", encoding="utf-8") as f:\n'
    '    reader = csv.DictReader(f)  # строки как словари\n'
    '    for row in reader:\n'
    '        print(row["name"], row["age"])\n\n'
    '# Запись CSV\n'
    'with open("out.csv", "w", newline="", encoding="utf-8") as f:\n'
    '    writer = csv.DictWriter(f, fieldnames=["name", "age"])\n'
    '    writer.writeheader()\n'
    '    writer.writerow({"name": "Анна", "age": 20})'
) + '''
<h3>JSON — структурированные данные</h3>
''' + code_block(
    'import json\n\n'
    '# Чтение JSON\n'
    'with open("config.json", encoding="utf-8") as f:\n'
    '    config = json.load(f)\n\n'
    '# Запись JSON\n'
    'with open("out.json", "w", encoding="utf-8") as f:\n'
    '    json.dump(data, f, ensure_ascii=False, indent=2)\n\n'
    '# Строка <-> JSON\n'
    'json_str = json.dumps({"key": "value"})\n'
    'obj = json.loads(json_str)'
) + '''
<h3>Сравнение форматов</h3>
''' + info_table(
    ['', 'CSV', 'JSON'],
    [
        ['Структура', 'Таблица (строки и столбцы)', 'Дерево (вложенные объекты)'],
        ['Типы данных', 'Только строки', 'str, int, float, bool, null, list, dict'],
        ['Для чего', 'Excel, базы данных', 'API, конфигурации'],
        ['Модуль', '<code>csv</code>', '<code>json</code>'],
    ]
) + '''
<h3>Запомните</h3>
<ul>
<li>CSV: <code>csv.DictReader</code> — удобнее обычного reader</li>
<li>JSON: <code>ensure_ascii=False</code> для кириллицы</li>
<li>JSON: <code>indent=2</code> для красивого вывода</li>
<li>Всегда указывайте <code>encoding="utf-8"</code></li>
</ul>'''
        },
    ],
}


class Command(BaseCommand):
    help = 'Расширяет модули 5-12 ОАИП до 5+ уроков'

    def handle(self, *args, **options):
        oaip = Subject.objects.get(title__contains='ОАИП')
        modules = {m.order: m for m in oaip.modules.order_by('order')}

        added = 0
        for m_order, lessons_data in sorted(LESSONS.items()):
            module = modules.get(m_order)
            if not module:
                self.stdout.write(f'[SKIP] Module {m_order} not found')
                continue

            existing = set(module.lessons.values_list('title', flat=True))

            for ld in lessons_data:
                if ld['title'] in existing:
                    self.stdout.write(f'[SKIP] M{m_order}: {ld["title"][:40]} (exists)')
                    continue

                TheoryLesson.objects.create(
                    module=module,
                    title=ld['title'],
                    content=ld['content'],
                    code_example=ld.get('code', ''),
                    order=ld['order'],
                    estimated_minutes=ld.get('minutes', 10),
                )
                added += 1
                self.stdout.write(self.style.SUCCESS(
                    f'[+] M{m_order} L{ld["order"]}: {ld["title"][:45]}'
                ))

        self.stdout.write(self.style.SUCCESS(f'\n[DONE] Added {added} lessons'))
