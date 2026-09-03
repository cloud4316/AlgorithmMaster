from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


def code_block(code):
    return (
        '<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;'
        'border-radius:8px;font-family:monospace;font-size:.9rem;'
        'overflow-x:auto;margin:1rem 0"><pre style="margin:0">'
        + code + '</pre></div>'
    )


def info_table(headers, rows):
    hdr = ''.join('<th>' + h + '</th>' for h in headers)
    body = ''
    for row in rows:
        body += '<tr>' + ''.join('<td>' + c + '</td>' for c in row) + '</tr>'
    return (
        '<table border="1" cellpadding="8" cellspacing="0" '
        'style="border-collapse:collapse;width:100%;margin:1rem 0">'
        '<tr style="background:#f1f5f9">' + hdr + '</tr>' + body + '</table>'
    )


LESSONS = {
    # ── M13: ООП ──────────────────────────────────────────────────
    13: [
        {
            'title': 'Магические методы: __str__, __repr__ и сравнение',
            'order': 2,
            'minutes': 12,
            'code': (
                'class Product:\n'
                '    def __init__(self, name, price):\n'
                '        self.name = name\n'
                '        self.price = price\n\n'
                '    def __str__(self):\n'
                '        return f"{self.name} ({self.price} руб.)"\n\n'
                '    def __repr__(self):\n'
                '        return f"Product({self.name!r}, {self.price!r})"\n\n'
                '    def __eq__(self, other):\n'
                '        return self.name == other.name and self.price == other.price\n\n'
                '    def __lt__(self, other):\n'
                '        return self.price < other.price\n\n'
                'p = Product("Молоко", 89)\n'
                'print(str(p))   # Молоко (89 руб.)\n'
                'print(repr(p))  # Product(\'Молоко\', 89)\n'
                'print(p == Product("Молоко", 89))  # True\n'
                'print(p < Product("Хлеб", 45))     # False'
            ),
            'content': (
                '<h2>Магические методы: __str__, __repr__ и сравнение</h2>'
                '<p>Магические (dunder) методы позволяют объектам вашего класса '
                'поддерживать стандартные операции Python: вывод, сравнение, '
                'арифметику и многое другое.</p>'
                '<h3>__str__ vs __repr__</h3>'
                + info_table(
                    ['Метод', 'Назначение', 'Когда вызывается'],
                    [
                        ['<code>__str__</code>',
                         'Читаемое представление для пользователя',
                         '<code>print(obj)</code>, <code>str(obj)</code>'],
                        ['<code>__repr__</code>',
                         'Однозначное представление для разработчика',
                         '<code>repr(obj)</code>, в REPL, при отладке'],
                    ]
                )
                + '<p>Если <code>__str__</code> не определён, Python использует '
                '<code>__repr__</code>. Поэтому <code>__repr__</code> нужно определять '
                'всегда.</p>'
                '<h3>Методы сравнения</h3>'
                + info_table(
                    ['Метод', 'Оператор', 'Пример'],
                    [
                        ['<code>__eq__</code>', '==', 'a == b'],
                        ['<code>__ne__</code>', '!=', 'a != b'],
                        ['<code>__lt__</code>', '&lt;', 'a &lt; b'],
                        ['<code>__le__</code>', '&lt;=', 'a &lt;= b'],
                        ['<code>__gt__</code>', '&gt;', 'a &gt; b'],
                        ['<code>__ge__</code>', '&gt;=', 'a &gt;= b'],
                    ]
                )
                + '<h3>Декоратор @total_ordering</h3>'
                '<p>Если определить <code>__eq__</code> и один из операторов '
                '(<code>__lt__</code>), остальные можно получить автоматически:</p>'
                + code_block(
                    'from functools import total_ordering\n\n'
                    '@total_ordering\n'
                    'class Student:\n'
                    '    def __init__(self, name, grade):\n'
                    '        self.name = name\n'
                    '        self.grade = grade\n\n'
                    '    def __eq__(self, other):\n'
                    '        return self.grade == other.grade\n\n'
                    '    def __lt__(self, other):\n'
                    '        return self.grade &lt; other.grade'
                )
                + '<h3>Советы</h3>'
                '<ul>'
                '<li>Всегда определяйте <code>__repr__</code> для отладки</li>'
                '<li><code>__str__</code> - для пользовательского вывода</li>'
                '<li>Используйте <code>@total_ordering</code> вместо 6 методов сравнения</li>'
                '<li>При определении <code>__eq__</code> также определите <code>__hash__</code></li>'
                '</ul>'
            ),
        },
        {
            'title': 'Методы класса и статические методы',
            'order': 3,
            'minutes': 10,
            'code': (
                'class Date:\n'
                '    def __init__(self, day, month, year):\n'
                '        self.day = day\n'
                '        self.month = month\n'
                '        self.year = year\n\n'
                '    def __str__(self):\n'
                '        return f"{self.day:02d}.{self.month:02d}.{self.year}"\n\n'
                '    @classmethod\n'
                '    def from_string(cls, s):\n'
                '        """Альтернативный конструктор из строки."""\n'
                '        day, month, year = map(int, s.split("."))\n'
                '        return cls(day, month, year)\n\n'
                '    @staticmethod\n'
                '    def is_leap(year):\n'
                '        """Проверка високосного года."""\n'
                '        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n\n'
                '# Обычный конструктор\n'
                'd1 = Date(15, 3, 2025)\n\n'
                '# Альтернативный конструктор (classmethod)\n'
                'd2 = Date.from_string("15.03.2025")\n\n'
                '# Статический метод (не нужен экземпляр)\n'
                'print(Date.is_leap(2024))  # True'
            ),
            'content': (
                '<h2>Методы класса и статические методы</h2>'
                '<p>Python предоставляет три типа методов в классе: обычные методы экземпляра, '
                'методы класса (<code>@classmethod</code>) и статические методы '
                '(<code>@staticmethod</code>).</p>'
                '<h3>Сравнение типов методов</h3>'
                + info_table(
                    ['Тип', 'Декоратор', 'Первый аргумент', 'Доступ'],
                    [
                        ['Метод экземпляра', 'нет', '<code>self</code>',
                         'К атрибутам экземпляра и класса'],
                        ['Метод класса', '<code>@classmethod</code>', '<code>cls</code>',
                         'Только к атрибутам класса'],
                        ['Статический метод', '<code>@staticmethod</code>', 'нет',
                         'Ни к чему (обычная функция)'],
                    ]
                )
                + '<h3>Когда использовать @classmethod</h3>'
                '<p>Главное применение - <strong>альтернативные конструкторы</strong>. '
                'Когда объект можно создать разными способами:</p>'
                + code_block(
                    'class Config:\n'
                    '    def __init__(self, data):\n'
                    '        self.data = data\n\n'
                    '    @classmethod\n'
                    '    def from_json(cls, path):\n'
                    '        import json\n'
                    '        with open(path) as f:\n'
                    '            return cls(json.load(f))\n\n'
                    '    @classmethod\n'
                    '    def from_env(cls):\n'
                    '        import os\n'
                    '        return cls(dict(os.environ))'
                )
                + '<h3>Когда использовать @staticmethod</h3>'
                '<p>Когда функция логически относится к классу, но не использует '
                'ни экземпляр, ни класс:</p>'
                + code_block(
                    'class MathHelper:\n'
                    '    @staticmethod\n'
                    '    def gcd(a, b):\n'
                    '        while b:\n'
                    '            a, b = b, a % b\n'
                    '        return a'
                )
                + '<h3>Советы</h3>'
                '<ul>'
                '<li>Если метод не использует <code>self</code> - рассмотрите '
                '<code>@staticmethod</code></li>'
                '<li><code>@classmethod</code> наследуется правильно: '
                '<code>cls</code> будет подклассом</li>'
                '<li>Не злоупотребляйте статическими методами - обычная функция '
                'на уровне модуля часто проще</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Композиция и агрегация объектов',
            'order': 4,
            'minutes': 12,
            'code': (
                'class Engine:\n'
                '    def __init__(self, horsepower):\n'
                '        self.horsepower = horsepower\n\n'
                '    def start(self):\n'
                '        return "Двигатель запущен"\n\n'
                'class Wheel:\n'
                '    def __init__(self, size):\n'
                '        self.size = size\n\n'
                'class Car:\n'
                '    """Композиция: Car ВЛАДЕЕТ Engine и Wheel."""\n'
                '    def __init__(self, brand, hp):\n'
                '        self.brand = brand\n'
                '        self.engine = Engine(hp)  # создаёт внутри\n'
                '        self.wheels = [Wheel(17) for _ in range(4)]\n\n'
                '    def start(self):\n'
                '        return f"{self.brand}: {self.engine.start()}"\n\n'
                'car = Car("Toyota", 150)\n'
                'print(car.start())  # Toyota: Двигатель запущен'
            ),
            'content': (
                '<h2>Композиция и агрегация объектов</h2>'
                '<p>Наследование отвечает на вопрос "является" (is-a), '
                'а композиция - "содержит" (has-a). Часто композиция '
                'предпочтительнее наследования.</p>'
                '<h3>Наследование vs Композиция</h3>'
                + info_table(
                    ['Подход', 'Связь', 'Пример', 'Гибкость'],
                    [
                        ['Наследование', 'is-a (является)',
                         'Собака <em>является</em> Животным', 'Жёсткая иерархия'],
                        ['Композиция', 'has-a (содержит)',
                         'Автомобиль <em>содержит</em> Двигатель', 'Гибкая, заменяемая'],
                        ['Агрегация', 'has-a (использует)',
                         'Группа <em>содержит</em> Студентов', 'Объекты живут независимо'],
                    ]
                )
                + '<h3>Композиция vs Агрегация</h3>'
                '<p><strong>Композиция</strong> - часть не существует без целого '
                '(двигатель создаётся внутри автомобиля).</p>'
                '<p><strong>Агрегация</strong> - часть может существовать самостоятельно '
                '(студент существует без группы).</p>'
                + code_block(
                    'class Student:\n'
                    '    def __init__(self, name):\n'
                    '        self.name = name\n\n'
                    'class Group:\n'
                    '    """Агрегация: студенты существуют сами по себе."""\n'
                    '    def __init__(self, name):\n'
                    '        self.name = name\n'
                    '        self.students = []\n\n'
                    '    def add(self, student):\n'
                    '        self.students.append(student)\n\n'
                    's = Student("Иванов")\n'
                    'g = Group("3РЭУ2")\n'
                    'g.add(s)  # студент передан, а не создан внутри'
                )
                + '<h3>Принцип "Предпочитайте композицию наследованию"</h3>'
                '<ul>'
                '<li>Наследование создаёт жёсткую связь между классами</li>'
                '<li>Композиция позволяет менять поведение на лету</li>'
                '<li>Используйте наследование для чёткой иерархии "является"</li>'
                '<li>Используйте композицию для сборки объектов из компонентов</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Практические паттерны ООП в Python',
            'order': 5,
            'minutes': 14,
            'code': (
                '# Паттерн Singleton\n'
                'class Database:\n'
                '    _instance = None\n\n'
                '    def __new__(cls):\n'
                '        if cls._instance is None:\n'
                '            cls._instance = super().__new__(cls)\n'
                '        return cls._instance\n\n'
                'db1 = Database()\n'
                'db2 = Database()\n'
                'print(db1 is db2)  # True\n\n'
                '# Паттерн Observer\n'
                'class EventSystem:\n'
                '    def __init__(self):\n'
                '        self._handlers = {}\n\n'
                '    def on(self, event, handler):\n'
                '        self._handlers.setdefault(event, []).append(handler)\n\n'
                '    def emit(self, event, *args):\n'
                '        for h in self._handlers.get(event, []):\n'
                '            h(*args)\n\n'
                'bus = EventSystem()\n'
                'bus.on("login", lambda user: print(f"Привет, {user}!"))\n'
                'bus.emit("login", "Анна")  # Привет, Анна!'
            ),
            'content': (
                '<h2>Практические паттерны ООП в Python</h2>'
                '<p>Паттерны проектирования - это проверенные решения '
                'типичных задач. Рассмотрим самые полезные в Python.</p>'
                '<h3>Основные паттерны</h3>'
                + info_table(
                    ['Паттерн', 'Задача', 'Пример'],
                    [
                        ['Singleton', 'Один экземпляр класса',
                         'Подключение к БД, конфигурация'],
                        ['Observer', 'Уведомление подписчиков',
                         'Системы событий, UI-обновления'],
                        ['Strategy', 'Сменное поведение',
                         'Алгоритмы сортировки, валидации'],
                        ['Factory', 'Создание объектов без указания класса',
                         'Парсеры файлов разных форматов'],
                    ]
                )
                + '<h3>Паттерн Strategy</h3>'
                + code_block(
                    'class Sorter:\n'
                    '    def __init__(self, strategy):\n'
                    '        self.strategy = strategy\n\n'
                    '    def sort(self, data):\n'
                    '        return self.strategy(data)\n\n'
                    '# Разные стратегии - обычные функции\n'
                    'def sort_asc(data): return sorted(data)\n'
                    'def sort_desc(data): return sorted(data, reverse=True)\n\n'
                    's = Sorter(sort_asc)\n'
                    'print(s.sort([3, 1, 2]))  # [1, 2, 3]\n'
                    's.strategy = sort_desc\n'
                    'print(s.sort([3, 1, 2]))  # [3, 2, 1]'
                )
                + '<h3>Паттерн Factory</h3>'
                + code_block(
                    'class FileParser:\n'
                    '    @staticmethod\n'
                    '    def create(filename):\n'
                    '        if filename.endswith(".json"):\n'
                    '            return JsonParser()\n'
                    '        elif filename.endswith(".csv"):\n'
                    '            return CsvParser()\n'
                    '        raise ValueError("Неизвестный формат")\n\n'
                    'parser = FileParser.create("data.json")'
                )
                + '<h3>Когда применять паттерны</h3>'
                '<ul>'
                '<li>Не используйте паттерны ради паттернов</li>'
                '<li>В Python многие паттерны упрощаются благодаря динамической типизации</li>'
                '<li>Функции первого класса заменяют Strategy и Command</li>'
                '<li>Декораторы и контекстные менеджеры решают многие задачи проще</li>'
                '</ul>'
            ),
        },
    ],

    # ── M14: Основы ООП ───────────────────────────────────────────
    14: [
        {
            'title': 'Множественное наследование и MRO',
            'order': 3,
            'minutes': 12,
            'code': (
                'class A:\n'
                '    def greet(self):\n'
                '        return "A"\n\n'
                'class B(A):\n'
                '    def greet(self):\n'
                '        return "B"\n\n'
                'class C(A):\n'
                '    def greet(self):\n'
                '        return "C"\n\n'
                'class D(B, C):\n'
                '    pass\n\n'
                'd = D()\n'
                'print(d.greet())  # B\n'
                'print(D.__mro__)\n'
                '# (<class D>, <class B>, <class C>, <class A>, <class object>)\n\n'
                '# super() следует MRO\n'
                'class B2(A):\n'
                '    def greet(self):\n'
                '        return "B2 -> " + super().greet()\n\n'
                'class C2(A):\n'
                '    def greet(self):\n'
                '        return "C2 -> " + super().greet()\n\n'
                'class D2(B2, C2):\n'
                '    def greet(self):\n'
                '        return "D2 -> " + super().greet()\n\n'
                'print(D2().greet())  # D2 -> B2 -> C2 -> A'
            ),
            'content': (
                '<h2>Множественное наследование и MRO</h2>'
                '<p>Python поддерживает множественное наследование: класс может '
                'наследовать от нескольких родителей. Порядок поиска методов '
                'определяется алгоритмом <strong>MRO</strong> (Method Resolution Order).</p>'
                '<h3>Алгоритм C3-линеаризации</h3>'
                '<p>Python использует алгоритм C3 для определения порядка поиска методов. '
                'Основные правила:</p>'
                '<ul>'
                '<li>Дочерний класс проверяется раньше родительского</li>'
                '<li>Порядок перечисления родителей сохраняется</li>'
                '<li>Если есть общий предок, он проверяется последним</li>'
                '</ul>'
                '<h3>Проблема ромбовидного наследования</h3>'
                + info_table(
                    ['Проблема', 'Без MRO', 'С MRO (Python)'],
                    [
                        ['Общий предок вызывается дважды',
                         'Да, в C++ без virtual',
                         'Нет, C3 гарантирует один вызов'],
                        ['Неоднозначность метода',
                         'Ошибка компиляции (некоторые языки)',
                         'Чёткий порядок по MRO'],
                    ]
                )
                + '<h3>Как super() работает с MRO</h3>'
                '<p><code>super()</code> вызывает не "родителя", а '
                '<strong>следующий класс в MRO</strong>. Это ключевой момент:</p>'
                + code_block(
                    '# Проверка MRO\n'
                    'print(D.__mro__)\n'
                    '# или\n'
                    'print(D.mro())\n'
                    '# Полезно при отладке'
                )
                + '<h3>Миксины</h3>'
                '<p>Миксины - классы, добавляющие функциональность без '
                'собственного состояния:</p>'
                + code_block(
                    'class LogMixin:\n'
                    '    def log(self, msg):\n'
                    '        print(f"[{self.__class__.__name__}] {msg}")\n\n'
                    'class SerializeMixin:\n'
                    '    def to_dict(self):\n'
                    '        return self.__dict__.copy()\n\n'
                    'class User(LogMixin, SerializeMixin):\n'
                    '    def __init__(self, name):\n'
                    '        self.name = name\n\n'
                    'u = User("Анна")\n'
                    'u.log("создан")       # [User] создан\n'
                    'print(u.to_dict())    # {\'name\': \'Анна\'}'
                )
                + '<h3>Рекомендации</h3>'
                '<ul>'
                '<li>Избегайте глубоких иерархий множественного наследования</li>'
                '<li>Используйте миксины для добавления поведения</li>'
                '<li>Всегда вызывайте <code>super()</code> в методах</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Абстрактные классы и интерфейсы',
            'order': 4,
            'minutes': 10,
            'code': (
                'from abc import ABC, abstractmethod\n\n'
                'class Shape(ABC):\n'
                '    @abstractmethod\n'
                '    def area(self):\n'
                '        """Вычислить площадь."""\n'
                '        pass\n\n'
                '    @abstractmethod\n'
                '    def perimeter(self):\n'
                '        """Вычислить периметр."""\n'
                '        pass\n\n'
                '    def describe(self):\n'
                '        return f"Площадь: {self.area():.2f}, периметр: {self.perimeter():.2f}"\n\n'
                'class Circle(Shape):\n'
                '    def __init__(self, radius):\n'
                '        self.radius = radius\n\n'
                '    def area(self):\n'
                '        from math import pi\n'
                '        return pi * self.radius ** 2\n\n'
                '    def perimeter(self):\n'
                '        from math import pi\n'
                '        return 2 * pi * self.radius\n\n'
                'c = Circle(5)\n'
                'print(c.describe())  # Площадь: 78.54, периметр: 31.42\n\n'
                '# Shape() вызовет TypeError - нельзя создать экземпляр'
            ),
            'content': (
                '<h2>Абстрактные классы и интерфейсы</h2>'
                '<p>Абстрактный класс - это класс, который нельзя создать напрямую. '
                'Он определяет интерфейс, который обязаны реализовать наследники.</p>'
                '<h3>Модуль abc</h3>'
                '<p>В Python абстрактные классы создаются с помощью модуля '
                '<code>abc</code> (Abstract Base Classes):</p>'
                + info_table(
                    ['Элемент', 'Назначение'],
                    [
                        ['<code>ABC</code>', 'Базовый класс для абстрактных классов'],
                        ['<code>@abstractmethod</code>',
                         'Метод, который обязаны реализовать наследники'],
                        ['<code>@abstractproperty</code>',
                         'Абстрактное свойство (устарело, используйте '
                         '<code>@property</code> + <code>@abstractmethod</code>)'],
                    ]
                )
                + '<h3>Правила абстрактных классов</h3>'
                '<ul>'
                '<li>Нельзя создать экземпляр абстрактного класса</li>'
                '<li>Наследник обязан реализовать все абстрактные методы</li>'
                '<li>Абстрактный класс может содержать обычные методы</li>'
                '<li>Абстрактный класс может наследовать от другого абстрактного</li>'
                '</ul>'
                '<h3>Протоколы (Python 3.8+)</h3>'
                '<p>Альтернатива ABC - структурная типизация через Protocol:</p>'
                + code_block(
                    'from typing import Protocol\n\n'
                    'class Drawable(Protocol):\n'
                    '    def draw(self) -> str: ...\n\n'
                    'class Circle:\n'
                    '    def draw(self) -> str:\n'
                    '        return "O"\n\n'
                    'def render(shape: Drawable):\n'
                    '    print(shape.draw())\n\n'
                    '# Circle не наследует Drawable,\n'
                    '# но подходит по структуре\n'
                    'render(Circle())  # O'
                )
                + '<h3>ABC vs Protocol</h3>'
                + info_table(
                    ['Подход', 'Тип типизации', 'Наследование'],
                    [
                        ['ABC', 'Номинальная (явная)', 'Требуется'],
                        ['Protocol', 'Структурная (утиная)', 'Не требуется'],
                    ]
                )
            ),
        },
        {
            'title': 'Инкапсуляция и свойства (property)',
            'order': 5,
            'minutes': 10,
            'code': (
                'class BankAccount:\n'
                '    def __init__(self, owner, balance=0):\n'
                '        self._owner = owner      # protected\n'
                '        self.__balance = balance  # private (name mangling)\n\n'
                '    @property\n'
                '    def balance(self):\n'
                '        """Геттер: чтение баланса."""\n'
                '        return self.__balance\n\n'
                '    @balance.setter\n'
                '    def balance(self, value):\n'
                '        """Сеттер: проверка перед записью."""\n'
                '        if value < 0:\n'
                '            raise ValueError("Баланс не может быть отрицательным")\n'
                '        self.__balance = value\n\n'
                '    @property\n'
                '    def owner(self):\n'
                '        return self._owner\n\n'
                'acc = BankAccount("Иванов", 1000)\n'
                'print(acc.balance)   # 1000 (используется геттер)\n'
                'acc.balance = 500    # OK (используется сеттер)\n'
                '# acc.balance = -100  # ValueError!'
            ),
            'content': (
                '<h2>Инкапсуляция и свойства (property)</h2>'
                '<p>Инкапсуляция - сокрытие внутреннего состояния объекта и '
                'предоставление контролируемого доступа через методы.</p>'
                '<h3>Уровни доступа в Python</h3>'
                + info_table(
                    ['Соглашение', 'Пример', 'Доступ'],
                    [
                        ['Публичный', '<code>self.name</code>',
                         'Свободный доступ'],
                        ['Защищённый', '<code>self._name</code>',
                         'Соглашение: не трогать извне'],
                        ['Приватный', '<code>self.__name</code>',
                         'Name mangling: <code>_Class__name</code>'],
                    ]
                )
                + '<p><strong>Важно:</strong> в Python нет настоящей приватности. '
                '<code>__name</code> превращается в <code>_ClassName__name</code>, '
                'и технически доступен. Это соглашение, а не запрет.</p>'
                '<h3>Декоратор @property</h3>'
                '<p><code>@property</code> позволяет обращаться к методу как к атрибуту, '
                'добавляя валидацию и вычисления:</p>'
                + code_block(
                    'class Temperature:\n'
                    '    def __init__(self, celsius):\n'
                    '        self._celsius = celsius\n\n'
                    '    @property\n'
                    '    def celsius(self):\n'
                    '        return self._celsius\n\n'
                    '    @celsius.setter\n'
                    '    def celsius(self, value):\n'
                    '        if value &lt; -273.15:\n'
                    '            raise ValueError("Ниже абсолютного нуля!")\n'
                    '        self._celsius = value\n\n'
                    '    @property\n'
                    '    def fahrenheit(self):\n'
                    '        return self._celsius * 9/5 + 32\n\n'
                    't = Temperature(100)\n'
                    'print(t.fahrenheit)  # 212.0\n'
                    't.celsius = 0\n'
                    'print(t.fahrenheit)  # 32.0'
                )
                + '<h3>Когда использовать property</h3>'
                '<ul>'
                '<li>Валидация при установке значения</li>'
                '<li>Вычисляемые атрибуты (fahrenheit из celsius)</li>'
                '<li>Ленивая инициализация (вычислить один раз при первом обращении)</li>'
                '<li>Логирование доступа к атрибутам</li>'
                '</ul>'
            ),
        },
    ],

    # ── M15: Генераторы и итераторы ────────────────────────────────
    15: [
        {
            'title': 'Конвейеры генераторов',
            'order': 3,
            'minutes': 12,
            'code': (
                '# Конвейер: чтение -> фильтрация -> обработка\n'
                'def read_lines(path):\n'
                '    with open(path) as f:\n'
                '        for line in f:\n'
                '            yield line.strip()\n\n'
                'def filter_nonempty(lines):\n'
                '    for line in lines:\n'
                '        if line:\n'
                '            yield line\n\n'
                'def to_upper(lines):\n'
                '    for line in lines:\n'
                '        yield line.upper()\n\n'
                '# Собираем конвейер\n'
                '# pipeline = to_upper(filter_nonempty(read_lines("data.txt")))\n'
                '# for line in pipeline:\n'
                '#     print(line)\n\n'
                '# Пример с числами\n'
                'def numbers():\n'
                '    for i in range(1, 101):\n'
                '        yield i\n\n'
                'def evens(nums):\n'
                '    for n in nums:\n'
                '        if n % 2 == 0:\n'
                '            yield n\n\n'
                'def squares(nums):\n'
                '    for n in nums:\n'
                '        yield n ** 2\n\n'
                'pipeline = squares(evens(numbers()))\n'
                'print(list(pipeline)[:5])  # [4, 16, 36, 64, 100]'
            ),
            'content': (
                '<h2>Конвейеры генераторов</h2>'
                '<p>Конвейер (pipeline) - это цепочка генераторов, где выход одного '
                'становится входом следующего. Данные обрабатываются по одному элементу, '
                'без загрузки всего набора в память.</p>'
                '<h3>Преимущества конвейеров</h3>'
                + info_table(
                    ['Подход', 'Память', 'Скорость старта'],
                    [
                        ['Списки: filter, map', 'O(n) на каждом шаге',
                         'Ждём полной обработки'],
                        ['Генераторы-конвейер', 'O(1)',
                         'Первый результат сразу'],
                    ]
                )
                + '<h3>Шаблон конвейера</h3>'
                + code_block(
                    'def source():\n'
                    '    """Генерирует данные."""\n'
                    '    yield from range(100)\n\n'
                    'def transform(data):\n'
                    '    """Преобразует каждый элемент."""\n'
                    '    for item in data:\n'
                    '        yield item * 2\n\n'
                    'def filter_step(data):\n'
                    '    """Фильтрует элементы."""\n'
                    '    for item in data:\n'
                    '        if item > 50:\n'
                    '            yield item\n\n'
                    '# Цепочка\n'
                    'result = filter_step(transform(source()))'
                )
                + '<h3>yield from для делегирования</h3>'
                '<p><code>yield from</code> передаёт генерацию другому итерируемому объекту:</p>'
                + code_block(
                    'def flatten(nested):\n'
                    '    for item in nested:\n'
                    '        if isinstance(item, list):\n'
                    '            yield from flatten(item)\n'
                    '        else:\n'
                    '            yield item\n\n'
                    'data = [1, [2, 3], [4, [5, 6]]]\n'
                    'print(list(flatten(data)))  # [1, 2, 3, 4, 5, 6]'
                )
                + '<h3>Практические применения</h3>'
                '<ul>'
                '<li>Обработка лог-файлов (миллионы строк)</li>'
                '<li>ETL-пайплайны (Extract-Transform-Load)</li>'
                '<li>Потоковая обработка данных</li>'
                '<li>Парсинг больших CSV/JSON файлов</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Модуль itertools: основные функции',
            'order': 4,
            'minutes': 12,
            'code': (
                'import itertools\n\n'
                '# count - бесконечный счётчик\n'
                'counter = itertools.count(start=1, step=2)\n'
                'print([next(counter) for _ in range(5)])  # [1, 3, 5, 7, 9]\n\n'
                '# chain - объединение итераторов\n'
                'a = [1, 2, 3]\n'
                'b = [4, 5, 6]\n'
                'print(list(itertools.chain(a, b)))  # [1, 2, 3, 4, 5, 6]\n\n'
                '# islice - срез итератора\n'
                'inf = itertools.count(0)\n'
                'print(list(itertools.islice(inf, 5)))  # [0, 1, 2, 3, 4]\n\n'
                '# groupby - группировка\n'
                'data = sorted(["apple", "avocado", "banana", "blueberry", "cherry"])\n'
                'for key, group in itertools.groupby(data, key=lambda x: x[0]):\n'
                '    print(key, list(group))\n'
                '# a [\'apple\', \'avocado\']\n'
                '# b [\'banana\', \'blueberry\']\n'
                '# c [\'cherry\']\n\n'
                '# product - декартово произведение\n'
                'colors = ["R", "G"]\n'
                'sizes = ["S", "L"]\n'
                'print(list(itertools.product(colors, sizes)))\n'
                '# [(\'R\', \'S\'), (\'R\', \'L\'), (\'G\', \'S\'), (\'G\', \'L\')]'
            ),
            'content': (
                '<h2>Модуль itertools: основные функции</h2>'
                '<p>Модуль <code>itertools</code> содержит эффективные '
                'итераторы для работы с данными. Все они ленивые - '
                'не создают промежуточных списков.</p>'
                '<h3>Бесконечные итераторы</h3>'
                + info_table(
                    ['Функция', 'Описание', 'Пример'],
                    [
                        ['<code>count(start, step)</code>', 'Счётчик',
                         '<code>count(10, 2) -&gt; 10, 12, 14...</code>'],
                        ['<code>cycle(iterable)</code>', 'Бесконечный цикл',
                         '<code>cycle("AB") -&gt; A, B, A, B...</code>'],
                        ['<code>repeat(x, n)</code>', 'Повторение',
                         '<code>repeat(7, 3) -&gt; 7, 7, 7</code>'],
                    ]
                )
                + '<h3>Комбинаторные итераторы</h3>'
                + info_table(
                    ['Функция', 'Описание', 'Кол-во'],
                    [
                        ['<code>product(A, B)</code>', 'Декартово произведение',
                         'len(A) * len(B)'],
                        ['<code>permutations(A, r)</code>', 'Перестановки',
                         'n! / (n-r)!'],
                        ['<code>combinations(A, r)</code>', 'Сочетания',
                         'C(n, r)'],
                    ]
                )
                + '<h3>Полезные функции</h3>'
                + code_block(
                    'from itertools import takewhile, dropwhile, accumulate\n\n'
                    '# takewhile - пока условие True\n'
                    'print(list(takewhile(lambda x: x &lt; 5, [1, 3, 5, 2])))\n'
                    '# [1, 3]\n\n'
                    '# dropwhile - пропустить пока True\n'
                    'print(list(dropwhile(lambda x: x &lt; 5, [1, 3, 5, 2])))\n'
                    '# [5, 2]\n\n'
                    '# accumulate - накопительная сумма\n'
                    'print(list(accumulate([1, 2, 3, 4])))\n'
                    '# [1, 3, 6, 10]'
                )
                + '<h3>Рецепты</h3>'
                '<ul>'
                '<li>Объединить списки: <code>chain(*lists)</code></li>'
                '<li>Взять первые N из бесконечного: <code>islice(gen, N)</code></li>'
                '<li>Все пары: <code>combinations(items, 2)</code></li>'
                '<li>Группировка: предварительно отсортируйте перед <code>groupby</code></li>'
                '</ul>'
            ),
        },
        {
            'title': 'Практические шаблоны генераторов',
            'order': 5,
            'minutes': 10,
            'code': (
                '# 1. Генератор с состоянием: скользящее среднее\n'
                'def moving_average(window):\n'
                '    values = []\n'
                '    total = 0\n'
                '    result = None\n'
                '    while True:\n'
                '        value = yield result\n'
                '        values.append(value)\n'
                '        total += value\n'
                '        if len(values) > window:\n'
                '            total -= values.pop(0)\n'
                '        result = total / len(values)\n\n'
                'avg = moving_average(3)\n'
                'next(avg)  # инициализация\n'
                'print(avg.send(10))  # 10.0\n'
                'print(avg.send(20))  # 15.0\n'
                'print(avg.send(30))  # 20.0\n'
                'print(avg.send(40))  # 30.0 (среднее 20, 30, 40)\n\n'
                '# 2. Генератор-контекст: таймер\n'
                'import time\n'
                'from contextlib import contextmanager\n\n'
                '@contextmanager\n'
                'def timer(label):\n'
                '    start = time.time()\n'
                '    yield\n'
                '    elapsed = time.time() - start\n'
                '    print(f"{label}: {elapsed:.3f} сек")\n\n'
                'with timer("Сортировка"):\n'
                '    sorted(range(100000, 0, -1))'
            ),
            'content': (
                '<h2>Практические шаблоны генераторов</h2>'
                '<p>Генераторы - не только ленивые списки. Они поддерживают '
                'двустороннюю передачу данных через <code>send()</code> и '
                'являются основой контекстных менеджеров.</p>'
                '<h3>send() - отправка данных в генератор</h3>'
                '<p>Метод <code>send()</code> позволяет передавать значения внутрь генератора:</p>'
                + code_block(
                    'def accumulator():\n'
                    '    total = 0\n'
                    '    while True:\n'
                    '        value = yield total\n'
                    '        total += value\n\n'
                    'acc = accumulator()\n'
                    'next(acc)        # инициализация, возвращает 0\n'
                    'acc.send(10)     # 10\n'
                    'acc.send(20)     # 30\n'
                    'acc.send(5)      # 35'
                )
                + '<h3>Контекстные менеджеры из генераторов</h3>'
                '<p><code>@contextmanager</code> превращает генератор с одним <code>yield</code> '
                'в контекстный менеджер:</p>'
                + info_table(
                    ['Часть', 'Когда выполняется'],
                    [
                        ['Код до yield', 'При входе в <code>with</code>'],
                        ['yield', 'Передаёт значение в <code>as</code>'],
                        ['Код после yield', 'При выходе из <code>with</code>'],
                    ]
                )
                + '<h3>Обработка ошибок в генераторах</h3>'
                + code_block(
                    'def safe_gen(iterable):\n'
                    '    for item in iterable:\n'
                    '        try:\n'
                    '            yield int(item)\n'
                    '        except (ValueError, TypeError):\n'
                    '            continue  # пропускаем ошибочные\n\n'
                    'data = ["1", "abc", "3", None, "5"]\n'
                    'print(list(safe_gen(data)))  # [1, 3, 5]'
                )
                + '<h3>Полезные шаблоны</h3>'
                '<ul>'
                '<li>Скользящее окно для потоковых данных</li>'
                '<li>Контекстные менеджеры для ресурсов</li>'
                '<li>Корутины для конечных автоматов</li>'
                '<li>Ленивое чтение больших файлов по частям</li>'
                '</ul>'
            ),
        },
    ],

    # ── M16: Декораторы ───────────────────────────────────────────
    16: [
        {
            'title': 'Практические декораторы: замер времени и кэширование',
            'order': 4,
            'minutes': 12,
            'code': (
                'import time\n'
                'from functools import wraps, lru_cache\n\n'
                '# Декоратор замера времени\n'
                'def timer(func):\n'
                '    @wraps(func)\n'
                '    def wrapper(*args, **kwargs):\n'
                '        start = time.perf_counter()\n'
                '        result = func(*args, **kwargs)\n'
                '        elapsed = time.perf_counter() - start\n'
                '        print(f"{func.__name__}: {elapsed:.4f} сек")\n'
                '        return result\n'
                '    return wrapper\n\n'
                '# Декоратор кэширования (простой)\n'
                'def cache(func):\n'
                '    memo = {}\n'
                '    @wraps(func)\n'
                '    def wrapper(*args):\n'
                '        if args not in memo:\n'
                '            memo[args] = func(*args)\n'
                '        return memo[args]\n'
                '    return wrapper\n\n'
                '@timer\n'
                '@cache\n'
                'def fibonacci(n):\n'
                '    if n < 2:\n'
                '        return n\n'
                '    return fibonacci(n - 1) + fibonacci(n - 2)\n\n'
                'print(fibonacci(30))  # 832040 (мгновенно благодаря кэшу)\n\n'
                '# Встроенный lru_cache\n'
                '@lru_cache(maxsize=128)\n'
                'def fib(n):\n'
                '    return n if n < 2 else fib(n-1) + fib(n-2)\n\n'
                'print(fib(100))  # 354224848179261915075'
            ),
            'content': (
                '<h2>Практические декораторы: замер времени и кэширование</h2>'
                '<p>Рассмотрим декораторы, которые пригодятся в реальных проектах.</p>'
                '<h3>Декоратор @timer</h3>'
                '<p>Измеряет время выполнения функции. Незаменим при профилировании:</p>'
                + code_block(
                    'import time\n'
                    'from functools import wraps\n\n'
                    'def timer(func):\n'
                    '    @wraps(func)\n'
                    '    def wrapper(*args, **kwargs):\n'
                    '        start = time.perf_counter()\n'
                    '        result = func(*args, **kwargs)\n'
                    '        elapsed = time.perf_counter() - start\n'
                    '        print(f"{func.__name__}: {elapsed:.4f} сек")\n'
                    '        return result\n'
                    '    return wrapper'
                )
                + '<h3>Кэширование</h3>'
                + info_table(
                    ['Способ', 'Описание', 'Ограничение'],
                    [
                        ['Свой декоратор', 'Словарь args -> результат',
                         'Нет вытеснения, утечка памяти'],
                        ['<code>@lru_cache</code>', 'Встроенный LRU-кэш',
                         'Только хешируемые аргументы'],
                        ['<code>@cache</code> (3.9+)', 'Безлимитный кэш',
                         'Может занять всю память'],
                    ]
                )
                + '<h3>Декоратор повторных попыток (retry)</h3>'
                + code_block(
                    'def retry(max_attempts=3, delay=1):\n'
                    '    def decorator(func):\n'
                    '        @wraps(func)\n'
                    '        def wrapper(*args, **kwargs):\n'
                    '            for attempt in range(1, max_attempts + 1):\n'
                    '                try:\n'
                    '                    return func(*args, **kwargs)\n'
                    '                except Exception as e:\n'
                    '                    if attempt == max_attempts:\n'
                    '                        raise\n'
                    '                    time.sleep(delay)\n'
                    '        return wrapper\n'
                    '    return decorator\n\n'
                    '@retry(max_attempts=3, delay=0.5)\n'
                    'def fetch_data(url):\n'
                    '    # может вызвать исключение\n'
                    '    pass'
                )
                + '<h3>Важно: @wraps</h3>'
                '<p>Всегда используйте <code>@wraps(func)</code> из '
                '<code>functools</code>, чтобы сохранить имя и документацию '
                'оригинальной функции.</p>'
            ),
        },
        {
            'title': 'Декораторы классов',
            'order': 5,
            'minutes': 10,
            'code': (
                'from dataclasses import dataclass, field\n\n'
                '# @dataclass - встроенный декоратор класса\n'
                '@dataclass\n'
                'class Point:\n'
                '    x: float\n'
                '    y: float\n\n'
                '    def distance(self, other):\n'
                '        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5\n\n'
                'p1 = Point(0, 0)\n'
                'p2 = Point(3, 4)\n'
                'print(p1)                # Point(x=0, y=4)\n'
                'print(p1 == Point(0, 0)) # True\n'
                'print(p1.distance(p2))   # 5.0\n\n'
                '# Свой декоратор класса\n'
                'def add_repr(cls):\n'
                '    """Добавляет __repr__ к любому классу."""\n'
                '    def __repr__(self):\n'
                '        attrs = ", ".join(\n'
                '            f"{k}={v!r}" for k, v in self.__dict__.items()\n'
                '        )\n'
                '        return f"{cls.__name__}({attrs})"\n'
                '    cls.__repr__ = __repr__\n'
                '    return cls\n\n'
                '@add_repr\n'
                'class Config:\n'
                '    def __init__(self, host, port):\n'
                '        self.host = host\n'
                '        self.port = port\n\n'
                'print(Config("localhost", 8080))\n'
                '# Config(host=\'localhost\', port=8080)'
            ),
            'content': (
                '<h2>Декораторы классов</h2>'
                '<p>Декораторы применяются не только к функциям, но и к классам. '
                'Декоратор класса принимает класс и возвращает модифицированный класс.</p>'
                '<h3>Встроенный @dataclass</h3>'
                '<p><code>@dataclass</code> автоматически генерирует '
                '<code>__init__</code>, <code>__repr__</code>, <code>__eq__</code> и другие методы:</p>'
                + info_table(
                    ['Параметр', 'По умолчанию', 'Описание'],
                    [
                        ['<code>frozen</code>', 'False',
                         'Неизменяемый класс (как tuple)'],
                        ['<code>order</code>', 'False',
                         'Добавить операторы сравнения'],
                        ['<code>slots</code>', 'False (3.10+)',
                         'Использовать __slots__ для экономии памяти'],
                    ]
                )
                + '<h3>Продвинутый dataclass</h3>'
                + code_block(
                    'from dataclasses import dataclass, field\n'
                    'from typing import List\n\n'
                    '@dataclass(frozen=True)\n'
                    'class Color:\n'
                    '    r: int\n'
                    '    g: int\n'
                    '    b: int\n\n'
                    '@dataclass\n'
                    'class Palette:\n'
                    '    name: str\n'
                    '    colors: List[Color] = field(default_factory=list)\n\n'
                    '    def add(self, color):\n'
                    '        self.colors.append(color)\n\n'
                    'p = Palette("Основные")\n'
                    'p.add(Color(255, 0, 0))\n'
                    'p.add(Color(0, 255, 0))'
                )
                + '<h3>Свои декораторы классов</h3>'
                '<p>Декоратор класса - функция, которая принимает класс, '
                'модифицирует его и возвращает:</p>'
                + code_block(
                    'def singleton(cls):\n'
                    '    instances = {}\n'
                    '    def get_instance(*args, **kwargs):\n'
                    '        if cls not in instances:\n'
                    '            instances[cls] = cls(*args, **kwargs)\n'
                    '        return instances[cls]\n'
                    '    return get_instance\n\n'
                    '@singleton\n'
                    'class Logger:\n'
                    '    def __init__(self):\n'
                    '        self.messages = []\n\n'
                    'log1 = Logger()\n'
                    'log2 = Logger()\n'
                    'print(log1 is log2)  # True'
                )
                + '<h3>Итоги</h3>'
                '<ul>'
                '<li><code>@dataclass</code> избавляет от рутинного кода</li>'
                '<li>Декораторы классов модифицируют или заменяют класс</li>'
                '<li><code>frozen=True</code> создаёт неизменяемые объекты</li>'
                '<li>Используйте <code>field(default_factory=list)</code> для '
                'изменяемых значений по умолчанию</li>'
                '</ul>'
            ),
        },
    ],

    # ── M17: Регулярные выражения ─────────────────────────────────
    17: [
        {
            'title': 'Практические задачи с регулярными выражениями',
            'order': 4,
            'minutes': 12,
            'code': (
                'import re\n\n'
                '# 1. Валидация email\n'
                'def is_valid_email(email):\n'
                '    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"\n'
                '    return bool(re.match(pattern, email))\n\n'
                'print(is_valid_email("user@example.com"))  # True\n'
                'print(is_valid_email("bad@.com"))           # False\n\n'
                '# 2. Извлечение данных из текста\n'
                'text = "Звоните: +7(495)123-45-67 или 8-800-555-35-35"\n'
                'phones = re.findall(r"[+\\d][\\d()-]{6,}\\d", text)\n'
                'print(phones)  # [\'+7(495)123-45-67\', \'8-800-555-35-35\']\n\n'
                '# 3. Замена с функцией\n'
                'def censor(text):\n'
                '    return re.sub(\n'
                '        r"\\b\\d{4}\\b",\n'
                '        lambda m: "****",\n'
                '        text\n'
                '    )\n\n'
                'print(censor("Пароль: 1234, код: 5678"))\n'
                '# Пароль: ****, код: ****\n\n'
                '# 4. Парсинг лога\n'
                'log = "2025-01-15 10:30:45 ERROR Database connection failed"\n'
                'match = re.match(\n'
                '    r"(\\d{4}-\\d{2}-\\d{2}) (\\d{2}:\\d{2}:\\d{2}) (\\w+) (.+)",\n'
                '    log\n'
                ')\n'
                'if match:\n'
                '    date, time_str, level, msg = match.groups()\n'
                '    print(f"{level}: {msg} ({date})")'
            ),
            'content': (
                '<h2>Практические задачи с регулярными выражениями</h2>'
                '<p>Регулярные выражения используются для валидации, '
                'извлечения и замены текста. Рассмотрим типичные задачи.</p>'
                '<h3>Валидация данных</h3>'
                + info_table(
                    ['Данные', 'Шаблон', 'Пример'],
                    [
                        ['Email', '<code>^[\\w.+-]+@[\\w-]+\\.[a-z]{2,}$</code>',
                         'user@mail.ru'],
                        ['Телефон РФ', '<code>^\\+?7\\d{10}$</code>',
                         '+79001234567'],
                        ['IP-адрес', '<code>^\\d{1,3}(\\.\\d{1,3}){3}$</code>',
                         '192.168.0.1'],
                        ['Дата', '<code>^\\d{2}\\.\\d{2}\\.\\d{4}$</code>',
                         '01.01.2025'],
                    ]
                )
                + '<h3>Именованные группы</h3>'
                '<p>Вместо номеров групп можно использовать имена:</p>'
                + code_block(
                    'import re\n\n'
                    'pattern = r"(?P&lt;year&gt;\\d{4})-(?P&lt;month&gt;\\d{2})-(?P&lt;day&gt;\\d{2})"\n'
                    'm = re.match(pattern, "2025-03-15")\n'
                    'print(m.group("year"))   # 2025\n'
                    'print(m.group("month"))  # 03\n'
                    'print(m.groupdict())     # {\'year\': \'2025\', ...}'
                )
                + '<h3>re.sub() с функцией</h3>'
                '<p>Второй аргумент <code>re.sub()</code> может быть функцией, '
                'получающей объект Match:</p>'
                + code_block(
                    'def multiply(match):\n'
                    '    num = int(match.group())\n'
                    '    return str(num * 2)\n\n'
                    'result = re.sub(r"\\d+", multiply, "яблок: 5, груш: 3")\n'
                    'print(result)  # яблок: 10, груш: 6'
                )
                + '<h3>Советы</h3>'
                '<ul>'
                '<li>Используйте <code>re.VERBOSE</code> для читаемых шаблонов</li>'
                '<li>Используйте сырые строки <code>r"..."</code></li>'
                '<li>Тестируйте на regex101.com</li>'
                '<li>Не валидируйте HTML регулярками</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Производительность и подводные камни regex',
            'order': 5,
            'minutes': 10,
            'code': (
                'import re\n'
                'import time\n\n'
                '# 1. Компиляция для повторного использования\n'
                'pattern = re.compile(r"\\b\\w+@\\w+\\.\\w+\\b")\n'
                'emails = pattern.findall("mail: a@b.com и c@d.ru")\n\n'
                '# 2. Катастрофический бэктрекинг\n'
                '# ПЛОХО: (a+)+ - экспоненциальное время\n'
                '# bad = re.compile(r"(a+)+")\n\n'
                '# 3. Жадные vs ленивые квантификаторы\n'
                'html = "<b>жирный</b> и <b>тоже</b>"\n'
                'print(re.findall(r"<b>.*</b>", html))\n'
                '# [\'<b>жирный</b> и <b>тоже</b>\']  -- жадный, захватил всё\n\n'
                'print(re.findall(r"<b>.*?</b>", html))\n'
                '# [\'<b>жирный</b>\', \'<b>тоже</b>\']  -- ленивый, минимум\n\n'
                '# 4. Атомарные группы (Python 3.11+)\n'
                '# (?>a+) - запрещает бэктрекинг\n\n'
                '# 5. Предпочитайте конкретные классы\n'
                '# Хорошо: [0-9]{3}\n'
                '# Плохо:  \\d{3} (может включать Unicode-цифры)\n\n'
                '# 6. Измерение скорости\n'
                'text = "a" * 1000 + "b"\n'
                'start = time.perf_counter()\n'
                're.search(r"a+b", text)\n'
                'print(f"Быстрый: {time.perf_counter() - start:.6f} сек")'
            ),
            'content': (
                '<h2>Производительность и подводные камни regex</h2>'
                '<p>Неправильно написанное регулярное выражение может работать '
                'экспоненциально долго. Разберём типичные ошибки.</p>'
                '<h3>Компиляция шаблонов</h3>'
                '<p>Если шаблон используется многократно, компилируйте его заранее:</p>'
                + code_block(
                    'import re\n\n'
                    '# Компиляция один раз\n'
                    'EMAIL_RE = re.compile(r"[\\w.+-]+@[\\w-]+\\.\\w+")\n\n'
                    '# Использование многократно\n'
                    'for line in open("data.txt"):\n'
                    '    matches = EMAIL_RE.findall(line)'
                )
                + '<h3>Жадные vs Ленивые квантификаторы</h3>'
                + info_table(
                    ['Квантификатор', 'Тип', 'Поведение'],
                    [
                        ['<code>*</code>, <code>+</code>', 'Жадный',
                         'Захватывает максимум'],
                        ['<code>*?</code>, <code>+?</code>', 'Ленивый',
                         'Захватывает минимум'],
                        ['<code>*+</code>, <code>++</code> (3.11+)', 'Притяжательный',
                         'Жадный без бэктрекинга'],
                    ]
                )
                + '<h3>Катастрофический бэктрекинг</h3>'
                '<p>Вложенные квантификаторы могут привести к экспоненциальному '
                'времени работы:</p>'
                + code_block(
                    '# ОПАСНО - экспоненциальное время!\n'
                    '# r"(a+)+" на строке "aaaaaaaaaaaaaab"\n'
                    '# r"(a|aa)+" на строке из a без b в конце\n\n'
                    '# БЕЗОПАСНО - переписать\n'
                    '# r"a+" вместо r"(a+)+"\n'
                    '# Или использовать атомарные группы (3.11+):\n'
                    '# r"(?>a+)"'
                )
                + '<h3>Альтернативы regex</h3>'
                + info_table(
                    ['Задача', 'regex', 'Альтернатива'],
                    [
                        ['Проверить начало', '<code>re.match(r"^http")</code>',
                         '<code>s.startswith("http")</code>'],
                        ['Найти подстроку', '<code>re.search(r"error")</code>',
                         '<code>"error" in s</code>'],
                        ['Разбить строку', '<code>re.split(r"[,;]")</code>',
                         '<code>s.split(",")</code> (для одного символа)'],
                    ]
                )
                + '<h3>Правила хорошего тона</h3>'
                '<ul>'
                '<li>Не используйте regex, если задачу решает строковый метод</li>'
                '<li>Компилируйте шаблоны для повторного использования</li>'
                '<li>Избегайте вложенных квантификаторов</li>'
                '<li>Тестируйте на граничных случаях и длинных строках</li>'
                '</ul>'
            ),
        },
    ],

    # ── M18: Алгоритмы поиска ─────────────────────────────────────
    18: [
        {
            'title': 'Вариации бинарного поиска',
            'order': 2,
            'minutes': 12,
            'code': (
                'from bisect import bisect_left, bisect_right\n\n'
                '# 1. Найти первое вхождение\n'
                'def first_occurrence(arr, target):\n'
                '    lo, hi = 0, len(arr) - 1\n'
                '    result = -1\n'
                '    while lo <= hi:\n'
                '        mid = (lo + hi) // 2\n'
                '        if arr[mid] == target:\n'
                '            result = mid\n'
                '            hi = mid - 1  # ищем левее\n'
                '        elif arr[mid] < target:\n'
                '            lo = mid + 1\n'
                '        else:\n'
                '            hi = mid - 1\n'
                '    return result\n\n'
                '# 2. Найти последнее вхождение\n'
                'def last_occurrence(arr, target):\n'
                '    lo, hi = 0, len(arr) - 1\n'
                '    result = -1\n'
                '    while lo <= hi:\n'
                '        mid = (lo + hi) // 2\n'
                '        if arr[mid] == target:\n'
                '            result = mid\n'
                '            lo = mid + 1  # ищем правее\n'
                '        elif arr[mid] < target:\n'
                '            lo = mid + 1\n'
                '        else:\n'
                '            hi = mid - 1\n'
                '    return result\n\n'
                'arr = [1, 2, 2, 2, 3, 4, 5]\n'
                'print(first_occurrence(arr, 2))  # 1\n'
                'print(last_occurrence(arr, 2))   # 3\n\n'
                '# 3. Модуль bisect\n'
                'print(bisect_left(arr, 2))   # 1 (первая позиция для 2)\n'
                'print(bisect_right(arr, 2))  # 4 (позиция после последней 2)'
            ),
            'content': (
                '<h2>Вариации бинарного поиска</h2>'
                '<p>Классический бинарный поиск ищет любое вхождение. '
                'На практике часто нужны его модификации.</p>'
                '<h3>Виды бинарного поиска</h3>'
                + info_table(
                    ['Задача', 'Модификация', 'Сложность'],
                    [
                        ['Первое вхождение', 'При совпадении ищем левее (hi = mid - 1)',
                         'O(log n)'],
                        ['Последнее вхождение', 'При совпадении ищем правее (lo = mid + 1)',
                         'O(log n)'],
                        ['Ближайший элемент', 'Сравниваем соседей после цикла',
                         'O(log n)'],
                        ['Нижняя граница', 'bisect_left - куда вставить слева',
                         'O(log n)'],
                    ]
                )
                + '<h3>Модуль bisect</h3>'
                '<p>Стандартный модуль <code>bisect</code> реализует бинарный поиск '
                'в отсортированных списках:</p>'
                + code_block(
                    'from bisect import bisect_left, insort\n\n'
                    '# Поиск позиции\n'
                    'arr = [10, 20, 30, 40, 50]\n'
                    'pos = bisect_left(arr, 25)\n'
                    'print(pos)  # 2 (вставка между 20 и 30)\n\n'
                    '# Вставка с сохранением порядка\n'
                    'insort(arr, 25)\n'
                    'print(arr)  # [10, 20, 25, 30, 40, 50]'
                )
                + '<h3>Поиск по ответу</h3>'
                '<p>Бинарный поиск применяется не только к массивам, '
                'но и к пространству ответов:</p>'
                + code_block(
                    '# Найти целый квадратный корень числа\n'
                    'def int_sqrt(n):\n'
                    '    lo, hi = 0, n\n'
                    '    while lo &lt;= hi:\n'
                    '        mid = (lo + hi) // 2\n'
                    '        if mid * mid &lt;= n:\n'
                    '            result = mid\n'
                    '            lo = mid + 1\n'
                    '        else:\n'
                    '            hi = mid - 1\n'
                    '    return result\n\n'
                    'print(int_sqrt(26))  # 5'
                )
                + '<h3>Типичные ошибки</h3>'
                '<ul>'
                '<li>Забыть, что массив должен быть отсортирован</li>'
                '<li>Бесконечный цикл из-за неправильного сдвига границ</li>'
                '<li>Переполнение: используйте <code>(lo + hi) // 2</code>, не <code>(lo + hi) / 2</code></li>'
                '</ul>'
            ),
        },
        {
            'title': 'Хеш-таблицы: словари и множества',
            'order': 3,
            'minutes': 12,
            'code': (
                '# 1. Словарь как хеш-таблица\n'
                'phone_book = {}\n'
                'phone_book["Иванов"] = "+7-900-111-22-33"\n'
                'phone_book["Петров"] = "+7-900-444-55-66"\n\n'
                '# Поиск за O(1)\n'
                'print("Иванов" in phone_book)  # True\n'
                'print(phone_book.get("Сидоров", "не найден"))  # не найден\n\n'
                '# 2. Подсчёт частот\n'
                'from collections import Counter\n'
                'text = "абракадабра"\n'
                'freq = Counter(text)\n'
                'print(freq.most_common(3))  # [(\'а\', 5), (\'б\', 2), (\'р\', 2)]\n\n'
                '# 3. Множество для быстрой проверки\n'
                'seen = set()\n'
                'data = [1, 2, 3, 2, 4, 1, 5]\n'
                'duplicates = []\n'
                'for x in data:\n'
                '    if x in seen:\n'
                '        duplicates.append(x)\n'
                '    seen.add(x)\n'
                'print(duplicates)  # [2, 1]\n\n'
                '# 4. Два числа с заданной суммой (Two Sum)\n'
                'def two_sum(nums, target):\n'
                '    seen = {}\n'
                '    for i, n in enumerate(nums):\n'
                '        complement = target - n\n'
                '        if complement in seen:\n'
                '            return [seen[complement], i]\n'
                '        seen[n] = i\n'
                '    return []\n\n'
                'print(two_sum([2, 7, 11, 15], 9))  # [0, 1]'
            ),
            'content': (
                '<h2>Хеш-таблицы: словари и множества</h2>'
                '<p>Хеш-таблица - структура данных, обеспечивающая поиск, '
                'вставку и удаление в среднем за O(1).</p>'
                '<h3>Сложность операций</h3>'
                + info_table(
                    ['Операция', 'Список', 'Словарь / Множество'],
                    [
                        ['Поиск', 'O(n)', 'O(1) в среднем'],
                        ['Вставка', 'O(1) в конец', 'O(1) в среднем'],
                        ['Удаление по значению', 'O(n)', 'O(1) в среднем'],
                        ['Проверка наличия', 'O(n)', 'O(1) в среднем'],
                    ]
                )
                + '<h3>Как работает хеширование</h3>'
                '<p>Python вычисляет <code>hash(key)</code>, получает индекс в '
                'массиве. При коллизии (два ключа дают один индекс) использует '
                'открытую адресацию.</p>'
                + code_block(
                    '# Хеширование\n'
                    'print(hash("hello"))      # число\n'
                    'print(hash(42))           # 42\n'
                    'print(hash((1, 2, 3)))    # число\n'
                    '# hash([1, 2, 3])  -- TypeError: unhashable'
                )
                + '<h3>Типичные задачи на хеш-таблицы</h3>'
                '<ul>'
                '<li>Подсчёт частот (<code>Counter</code>)</li>'
                '<li>Поиск дубликатов (<code>set</code>)</li>'
                '<li>Два числа с суммой (Two Sum)</li>'
                '<li>Группировка анаграмм</li>'
                '<li>Кэширование результатов</li>'
                '</ul>'
                '<h3>defaultdict и Counter</h3>'
                + code_block(
                    'from collections import defaultdict, Counter\n\n'
                    '# Группировка слов по первой букве\n'
                    'words = ["яблоко", "арбуз", "ананас", "банан", "апельсин"]\n'
                    'groups = defaultdict(list)\n'
                    'for w in words:\n'
                    '    groups[w[0]].append(w)\n\n'
                    'print(dict(groups))\n'
                    '# {\'я\': [\'яблоко\'], \'а\': [\'арбуз\', \'ананас\', \'апельсин\'], \'б\': [\'банан\']}'
                )
            ),
        },
        {
            'title': 'Поиск в отсортированных структурах',
            'order': 4,
            'minutes': 10,
            'code': (
                'from bisect import bisect_left, insort\n\n'
                '# 1. Поиск диапазона в отсортированном массиве\n'
                'def count_in_range(arr, lo, hi):\n'
                '    """Количество элементов в [lo, hi]."""\n'
                '    left = bisect_left(arr, lo)\n'
                '    right = bisect_left(arr, hi + 1)\n'
                '    return right - left\n\n'
                'data = [1, 3, 5, 7, 9, 11, 13, 15]\n'
                'print(count_in_range(data, 5, 11))  # 4 (5, 7, 9, 11)\n\n'
                '# 2. Merge двух отсортированных массивов\n'
                'def merge_sorted(a, b):\n'
                '    result = []\n'
                '    i = j = 0\n'
                '    while i < len(a) and j < len(b):\n'
                '        if a[i] <= b[j]:\n'
                '            result.append(a[i])\n'
                '            i += 1\n'
                '        else:\n'
                '            result.append(b[j])\n'
                '            j += 1\n'
                '    result.extend(a[i:])\n'
                '    result.extend(b[j:])\n'
                '    return result\n\n'
                'print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]\n\n'
                '# 3. K-й наименьший элемент двух отсортированных\n'
                'import heapq\n'
                'a = [1, 5, 9]\n'
                'b = [2, 3, 7]\n'
                'merged = heapq.merge(a, b)\n'
                'for _ in range(3):  # 3-й элемент\n'
                '    val = next(merged)\n'
                'print(val)  # 3'
            ),
            'content': (
                '<h2>Поиск в отсортированных структурах</h2>'
                '<p>Отсортированные данные открывают доступ к эффективным '
                'алгоритмам: бинарный поиск, слияние, поиск диапазонов.</p>'
                '<h3>Операции над отсортированными массивами</h3>'
                + info_table(
                    ['Операция', 'Неотсортированный', 'Отсортированный'],
                    [
                        ['Поиск элемента', 'O(n)', 'O(log n)'],
                        ['Поиск диапазона', 'O(n)', 'O(log n)'],
                        ['Слияние двух', 'O(n log n)', 'O(n)'],
                        ['Вставка с сохранением порядка', '-', 'O(n), но поиск O(log n)'],
                    ]
                )
                + '<h3>Алгоритм слияния (Merge)</h3>'
                '<p>Слияние двух отсортированных массивов - основа сортировки слиянием. '
                'Работает за O(n + m), где n и m - размеры массивов.</p>'
                + code_block(
                    'def merge(a, b):\n'
                    '    result, i, j = [], 0, 0\n'
                    '    while i &lt; len(a) and j &lt; len(b):\n'
                    '        if a[i] &lt;= b[j]:\n'
                    '            result.append(a[i]); i += 1\n'
                    '        else:\n'
                    '            result.append(b[j]); j += 1\n'
                    '    return result + a[i:] + b[j:]'
                )
                + '<h3>heapq.merge</h3>'
                '<p>Для слияния нескольких отсортированных последовательностей '
                'используйте <code>heapq.merge()</code> - это генератор, '
                'не загружающий всё в память:</p>'
                + code_block(
                    'import heapq\n\n'
                    'files = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]\n'
                    'for val in heapq.merge(*files):\n'
                    '    print(val, end=" ")  # 1 2 3 4 5 6 7 8 9'
                )
                + '<h3>Практические применения</h3>'
                '<ul>'
                '<li>Поиск пересечения отсортированных списков</li>'
                '<li>Слияние результатов из нескольких источников</li>'
                '<li>Эффективный поиск по диапазону дат</li>'
                '<li>Медиана потока данных (два heap-а)</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Интерполяционный поиск и сравнение алгоритмов',
            'order': 5,
            'minutes': 10,
            'code': (
                '# 1. Интерполяционный поиск\n'
                'def interpolation_search(arr, target):\n'
                '    lo, hi = 0, len(arr) - 1\n'
                '    while lo <= hi and arr[lo] <= target <= arr[hi]:\n'
                '        if lo == hi:\n'
                '            return lo if arr[lo] == target else -1\n'
                '        # Оценка позиции пропорционально значению\n'
                '        pos = lo + (target - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])\n'
                '        if arr[pos] == target:\n'
                '            return pos\n'
                '        elif arr[pos] < target:\n'
                '            lo = pos + 1\n'
                '        else:\n'
                '            hi = pos - 1\n'
                '    return -1\n\n'
                '# Равномерно распределённые данные\n'
                'data = list(range(0, 1000, 3))  # [0, 3, 6, ..., 999]\n'
                'print(interpolation_search(data, 333))  # 111\n\n'
                '# 2. Сравнение алгоритмов\n'
                'import time\n\n'
                'def benchmark(search_func, arr, target, runs=10000):\n'
                '    start = time.perf_counter()\n'
                '    for _ in range(runs):\n'
                '        search_func(arr, target)\n'
                '    return (time.perf_counter() - start) / runs\n\n'
                'def binary_search(arr, target):\n'
                '    lo, hi = 0, len(arr) - 1\n'
                '    while lo <= hi:\n'
                '        mid = (lo + hi) // 2\n'
                '        if arr[mid] == target: return mid\n'
                '        elif arr[mid] < target: lo = mid + 1\n'
                '        else: hi = mid - 1\n'
                '    return -1\n\n'
                'arr = list(range(10000))\n'
                'target = 7777\n'
                'print(f"Binary:        {benchmark(binary_search, arr, target):.8f} сек")\n'
                'print(f"Interpolation: {benchmark(interpolation_search, arr, target):.8f} сек")'
            ),
            'content': (
                '<h2>Интерполяционный поиск и сравнение алгоритмов</h2>'
                '<p>Интерполяционный поиск улучшает бинарный, если данные '
                'распределены равномерно. Вместо середины он оценивает '
                'позицию пропорционально значению.</p>'
                '<h3>Сравнение алгоритмов поиска</h3>'
                + info_table(
                    ['Алгоритм', 'Лучший', 'Средний', 'Худший', 'Требования'],
                    [
                        ['Линейный', 'O(1)', 'O(n)', 'O(n)', 'Нет'],
                        ['Бинарный', 'O(1)', 'O(log n)', 'O(log n)',
                         'Отсортированный'],
                        ['Интерполяционный', 'O(1)', 'O(log log n)', 'O(n)',
                         'Отсортированный + равномерный'],
                        ['Хеш-таблица', 'O(1)', 'O(1)', 'O(n)', 'Хеш-функция'],
                    ]
                )
                + '<h3>Когда что использовать</h3>'
                + info_table(
                    ['Ситуация', 'Лучший алгоритм'],
                    [
                        ['Неотсортированные данные', 'Линейный или хеш-таблица'],
                        ['Отсортированный массив', 'Бинарный поиск (bisect)'],
                        ['Равномерные числовые данные', 'Интерполяционный'],
                        ['Частые проверки наличия', 'Множество (set)'],
                        ['Ключ-значение', 'Словарь (dict)'],
                    ]
                )
                + '<h3>Формула интерполяции</h3>'
                '<p>Вместо <code>mid = (lo + hi) // 2</code> используется:</p>'
                + code_block(
                    'pos = lo + (target - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])'
                )
                + '<p>Это даёт O(log log n) для равномерных данных, но O(n) '
                'в худшем случае (сильно неравномерные данные).</p>'
                '<h3>Выводы</h3>'
                '<ul>'
                '<li>Для большинства задач достаточно <code>bisect</code></li>'
                '<li>Хеш-таблицы (dict/set) быстрее для проверки наличия</li>'
                '<li>Интерполяционный поиск - нишевый, для больших равномерных данных</li>'
                '<li>Всегда измеряйте производительность на реальных данных</li>'
                '</ul>'
            ),
        },
    ],

    # ── M19: Тестирование кода ────────────────────────────────────
    19: [
        {
            'title': 'Разработка через тестирование (TDD)',
            'order': 4,
            'minutes': 12,
            'code': (
                'import unittest\n\n'
                '# Шаг 1: Пишем тест ДО кода\n'
                'class TestStack(unittest.TestCase):\n'
                '    def test_push_and_pop(self):\n'
                '        s = Stack()\n'
                '        s.push(1)\n'
                '        s.push(2)\n'
                '        self.assertEqual(s.pop(), 2)\n'
                '        self.assertEqual(s.pop(), 1)\n\n'
                '    def test_empty_pop_raises(self):\n'
                '        s = Stack()\n'
                '        with self.assertRaises(IndexError):\n'
                '            s.pop()\n\n'
                '    def test_peek(self):\n'
                '        s = Stack()\n'
                '        s.push(42)\n'
                '        self.assertEqual(s.peek(), 42)\n'
                '        self.assertEqual(len(s), 1)  # peek не удаляет\n\n'
                '    def test_len(self):\n'
                '        s = Stack()\n'
                '        self.assertEqual(len(s), 0)\n'
                '        s.push(1)\n'
                '        self.assertEqual(len(s), 1)\n\n'
                '# Шаг 2: Пишем минимальный код\n'
                'class Stack:\n'
                '    def __init__(self):\n'
                '        self._items = []\n\n'
                '    def push(self, item):\n'
                '        self._items.append(item)\n\n'
                '    def pop(self):\n'
                '        if not self._items:\n'
                '            raise IndexError("pop from empty stack")\n'
                '        return self._items.pop()\n\n'
                '    def peek(self):\n'
                '        return self._items[-1]\n\n'
                '    def __len__(self):\n'
                '        return len(self._items)\n\n'
                '# Шаг 3: Рефакторинг (при необходимости)\n'
                '# if __name__ == "__main__":\n'
                '#     unittest.main()'
            ),
            'content': (
                '<h2>Разработка через тестирование (TDD)</h2>'
                '<p>TDD (Test-Driven Development) - методология, где тесты '
                'пишутся <strong>до</strong> кода. Цикл: Red - Green - Refactor.</p>'
                '<h3>Цикл TDD</h3>'
                + info_table(
                    ['Шаг', 'Действие', 'Результат'],
                    [
                        ['<span style="color:red">Red</span>',
                         'Написать падающий тест',
                         'Тест не проходит (код ещё не написан)'],
                        ['<span style="color:green">Green</span>',
                         'Написать минимальный код',
                         'Тест проходит'],
                        ['<span style="color:blue">Refactor</span>',
                         'Улучшить код',
                         'Тесты продолжают проходить'],
                    ]
                )
                + '<h3>Пример TDD: класс Stack</h3>'
                '<p>Сначала определяем поведение через тесты, потом реализуем:</p>'
                + code_block(
                    '# 1. Пишем тест (Red)\n'
                    'def test_push_and_pop(self):\n'
                    '    s = Stack()\n'
                    '    s.push(1)\n'
                    '    self.assertEqual(s.pop(), 1)\n\n'
                    '# 2. Минимальная реализация (Green)\n'
                    'class Stack:\n'
                    '    def __init__(self): self._items = []\n'
                    '    def push(self, x): self._items.append(x)\n'
                    '    def pop(self): return self._items.pop()\n\n'
                    '# 3. Добавляем тест на ошибку (Red)\n'
                    'def test_empty_pop(self):\n'
                    '    with self.assertRaises(IndexError):\n'
                    '        Stack().pop()\n\n'
                    '# 4. Дополняем реализацию (Green)\n'
                    'def pop(self):\n'
                    '    if not self._items:\n'
                    '        raise IndexError("empty")\n'
                    '    return self._items.pop()'
                )
                + '<h3>Преимущества TDD</h3>'
                '<ul>'
                '<li>Чёткое понимание требований до написания кода</li>'
                '<li>100% покрытие тестами по определению</li>'
                '<li>Уверенность при рефакторинге</li>'
                '<li>Документация через тесты</li>'
                '</ul>'
                '<h3>Когда TDD не подходит</h3>'
                '<ul>'
                '<li>Прототипирование и исследование</li>'
                '<li>UI-код, который часто меняется</li>'
                '<li>Интеграции с внешними сервисами (нужны моки)</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Мокирование: unittest.mock',
            'order': 5,
            'minutes': 12,
            'code': (
                'from unittest.mock import Mock, patch, MagicMock\n'
                'import unittest\n\n'
                '# Класс, который зависит от внешнего сервиса\n'
                'class WeatherService:\n'
                '    def get_temperature(self, city):\n'
                '        # В реальности - HTTP-запрос\n'
                '        raise NotImplementedError\n\n'
                'class WeatherApp:\n'
                '    def __init__(self, service):\n'
                '        self.service = service\n\n'
                '    def is_cold(self, city):\n'
                '        temp = self.service.get_temperature(city)\n'
                '        return temp < 0\n\n'
                '# Тестирование с Mock\n'
                'class TestWeatherApp(unittest.TestCase):\n'
                '    def test_is_cold_true(self):\n'
                '        mock_service = Mock()\n'
                '        mock_service.get_temperature.return_value = -5\n\n'
                '        app = WeatherApp(mock_service)\n'
                '        self.assertTrue(app.is_cold("Москва"))\n'
                '        mock_service.get_temperature.assert_called_once_with("Москва")\n\n'
                '    def test_is_cold_false(self):\n'
                '        mock_service = Mock()\n'
                '        mock_service.get_temperature.return_value = 25\n\n'
                '        app = WeatherApp(mock_service)\n'
                '        self.assertFalse(app.is_cold("Сочи"))\n\n'
                '    @patch("builtins.open", create=True)\n'
                '    def test_read_config(self, mock_open):\n'
                '        mock_open.return_value.__enter__ = Mock(return_value=Mock())\n'
                '        mock_open.return_value.__exit__ = Mock(return_value=False)\n'
                '        # Тестируем код, читающий файл'
            ),
            'content': (
                '<h2>Мокирование: unittest.mock</h2>'
                '<p>Мок (mock) - подставной объект, имитирующий поведение '
                'реальной зависимости. Позволяет тестировать код изолированно.</p>'
                '<h3>Когда нужны моки</h3>'
                + info_table(
                    ['Зависимость', 'Почему мокаем'],
                    [
                        ['HTTP-запросы', 'Медленно, нестабильно, стоит денег'],
                        ['База данных', 'Требует настройки, медленно'],
                        ['Файловая система', 'Побочные эффекты'],
                        ['Текущее время', 'Тесты должны быть детерминированы'],
                        ['Случайные числа', 'Нужна предсказуемость'],
                    ]
                )
                + '<h3>Mock, MagicMock, patch</h3>'
                + info_table(
                    ['Инструмент', 'Назначение'],
                    [
                        ['<code>Mock()</code>', 'Базовый мок-объект'],
                        ['<code>MagicMock()</code>',
                         'Mock + магические методы (__len__, __iter__)'],
                        ['<code>@patch</code>',
                         'Подменяет объект в указанном модуле'],
                        ['<code>patch.object</code>',
                         'Подменяет атрибут конкретного объекта'],
                    ]
                )
                + '<h3>Основные возможности Mock</h3>'
                + code_block(
                    'from unittest.mock import Mock\n\n'
                    'm = Mock()\n\n'
                    '# Задать возвращаемое значение\n'
                    'm.some_method.return_value = 42\n'
                    'print(m.some_method())  # 42\n\n'
                    '# Задать побочный эффект (исключение)\n'
                    'm.fail.side_effect = ValueError("ошибка")\n'
                    '# m.fail()  -> ValueError\n\n'
                    '# Проверить вызовы\n'
                    'm.some_method.assert_called_once()\n'
                    'm.some_method.assert_called_with()'
                )
                + '<h3>Декоратор @patch</h3>'
                + code_block(
                    'from unittest.mock import patch\n\n'
                    '# Подменяет time.time на время теста\n'
                    '@patch("time.time", return_value=1000.0)\n'
                    'def test_timestamp(mock_time):\n'
                    '    import time\n'
                    '    assert time.time() == 1000.0'
                )
                + '<h3>Правила мокирования</h3>'
                '<ul>'
                '<li>Мокайте то, что принадлежит вам, а не чужие библиотеки</li>'
                '<li>Предпочитайте внедрение зависимостей (DI) вместо patch</li>'
                '<li>Не мокайте слишком много - это признак плохой архитектуры</li>'
                '<li>Проверяйте вызовы: <code>assert_called_with</code></li>'
                '</ul>'
            ),
        },
    ],

    # ── M20: Алгоритмическое мышление ─────────────────────────────
    20: [
        {
            'title': 'Жадные алгоритмы',
            'order': 2,
            'minutes': 12,
            'code': (
                '# 1. Задача о сдаче монетами\n'
                'def min_coins(amount, coins):\n'
                '    """Жадный: берём наибольшую монету."""\n'
                '    coins_sorted = sorted(coins, reverse=True)\n'
                '    result = []\n'
                '    for coin in coins_sorted:\n'
                '        while amount >= coin:\n'
                '            result.append(coin)\n'
                '            amount -= coin\n'
                '    return result if amount == 0 else None\n\n'
                'print(min_coins(67, [1, 5, 10, 25]))  # [25, 25, 10, 5, 1, 1]\n\n'
                '# 2. Задача об интервалах (расписание)\n'
                'def max_meetings(meetings):\n'
                '    """Максимум непересекающихся встреч."""\n'
                '    # Сортируем по времени окончания\n'
                '    meetings.sort(key=lambda m: m[1])\n'
                '    result = [meetings[0]]\n'
                '    for start, end in meetings[1:]:\n'
                '        if start >= result[-1][1]:\n'
                '            result.append((start, end))\n'
                '    return result\n\n'
                'meetings = [(1, 3), (2, 5), (3, 6), (5, 7), (6, 8)]\n'
                'print(max_meetings(meetings))  # [(1, 3), (3, 6), (6, 8)]\n\n'
                '# 3. Задача о рюкзаке (дробный)\n'
                'def fractional_knapsack(capacity, items):\n'
                '    """items = [(weight, value), ...]"""\n'
                '    items.sort(key=lambda x: x[1]/x[0], reverse=True)\n'
                '    total = 0\n'
                '    for w, v in items:\n'
                '        if capacity >= w:\n'
                '            total += v\n'
                '            capacity -= w\n'
                '        else:\n'
                '            total += v * (capacity / w)\n'
                '            break\n'
                '    return total\n\n'
                'items = [(10, 60), (20, 100), (30, 120)]\n'
                'print(fractional_knapsack(50, items))  # 240.0'
            ),
            'content': (
                '<h2>Жадные алгоритмы</h2>'
                '<p>Жадный алгоритм на каждом шаге делает локально оптимальный выбор, '
                'надеясь получить глобально оптимальное решение.</p>'
                '<h3>Когда жадный подход работает</h3>'
                + info_table(
                    ['Задача', 'Жадный работает?', 'Почему'],
                    [
                        ['Сдача монетами (1, 5, 10, 25)', 'Да',
                         'Каждая монета кратна меньшей'],
                        ['Сдача монетами (1, 3, 4), сумма 6', 'Нет',
                         'Жадный: 4+1+1=3 монеты, оптимально: 3+3=2'],
                        ['Расписание (max встреч)', 'Да',
                         'Доказано математически'],
                        ['Дробный рюкзак', 'Да',
                         'Можно брать часть предмета'],
                        ['0/1 рюкзак', 'Нет',
                         'Нужна динамика'],
                    ]
                )
                + '<h3>Шаблон жадного алгоритма</h3>'
                + code_block(
                    'def greedy(items, capacity):\n'
                    '    # 1. Отсортировать по "жадному" критерию\n'
                    '    items.sort(key=greedy_criterion, reverse=True)\n'
                    '    result = []\n'
                    '    # 2. На каждом шаге - лучший доступный выбор\n'
                    '    for item in items:\n'
                    '        if can_take(item, capacity):\n'
                    '            result.append(item)\n'
                    '            update(capacity, item)\n'
                    '    return result'
                )
                + '<h3>Признаки жадной задачи</h3>'
                '<ul>'
                '<li>Оптимальная подструктура: оптимальное решение содержит '
                'оптимальные решения подзадач</li>'
                '<li>Свойство жадного выбора: локально оптимальный выбор ведёт '
                'к глобально оптимальному решению</li>'
                '<li>Если не уверены - проверьте контрпримером</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Разделяй и властвуй',
            'order': 3,
            'minutes': 12,
            'code': (
                '# 1. Сортировка слиянием\n'
                'def merge_sort(arr):\n'
                '    if len(arr) <= 1:\n'
                '        return arr\n'
                '    mid = len(arr) // 2\n'
                '    left = merge_sort(arr[:mid])\n'
                '    right = merge_sort(arr[mid:])\n'
                '    return merge(left, right)\n\n'
                'def merge(a, b):\n'
                '    result, i, j = [], 0, 0\n'
                '    while i < len(a) and j < len(b):\n'
                '        if a[i] <= b[j]:\n'
                '            result.append(a[i]); i += 1\n'
                '        else:\n'
                '            result.append(b[j]); j += 1\n'
                '    return result + a[i:] + b[j:]\n\n'
                'print(merge_sort([38, 27, 43, 3, 9, 82, 10]))\n'
                '# [3, 9, 10, 27, 38, 43, 82]\n\n'
                '# 2. Быстрое возведение в степень\n'
                'def power(base, exp):\n'
                '    if exp == 0:\n'
                '        return 1\n'
                '    if exp % 2 == 0:\n'
                '        half = power(base, exp // 2)\n'
                '        return half * half\n'
                '    return base * power(base, exp - 1)\n\n'
                'print(power(2, 10))  # 1024\n\n'
                '# 3. Количество инверсий\n'
                'def count_inversions(arr):\n'
                '    if len(arr) <= 1:\n'
                '        return arr, 0\n'
                '    mid = len(arr) // 2\n'
                '    left, left_inv = count_inversions(arr[:mid])\n'
                '    right, right_inv = count_inversions(arr[mid:])\n'
                '    merged, split_inv = merge_count(left, right)\n'
                '    return merged, left_inv + right_inv + split_inv\n\n'
                'def merge_count(a, b):\n'
                '    result, i, j, inv = [], 0, 0, 0\n'
                '    while i < len(a) and j < len(b):\n'
                '        if a[i] <= b[j]:\n'
                '            result.append(a[i]); i += 1\n'
                '        else:\n'
                '            result.append(b[j]); j += 1\n'
                '            inv += len(a) - i\n'
                '    return result + a[i:] + b[j:], inv\n\n'
                'print(count_inversions([5, 3, 1, 4, 2]))  # (..., 7)'
            ),
            'content': (
                '<h2>Разделяй и властвуй</h2>'
                '<p>Метод "разделяй и властвуй" (Divide and Conquer) решает задачу, '
                'разбивая её на подзадачи, решая каждую рекурсивно '
                'и объединяя результаты.</p>'
                '<h3>Три шага</h3>'
                + info_table(
                    ['Шаг', 'Действие', 'Пример (merge sort)'],
                    [
                        ['Divide (Разделяй)', 'Разбить на подзадачи',
                         'Массив пополам'],
                        ['Conquer (Властвуй)', 'Решить подзадачи рекурсивно',
                         'Отсортировать каждую половину'],
                        ['Combine (Объединяй)', 'Собрать результат',
                         'Слить два отсортированных'],
                    ]
                )
                + '<h3>Классические задачи</h3>'
                + info_table(
                    ['Задача', 'Divide', 'Combine', 'Сложность'],
                    [
                        ['Merge Sort', 'Пополам', 'Слияние', 'O(n log n)'],
                        ['Quick Sort', 'По pivot', 'Конкатенация', 'O(n log n) ср.'],
                        ['Бинарный поиск', 'Отбросить половину', '-', 'O(log n)'],
                        ['Возведение в степень', 'x^n = (x^(n/2))^2', 'Умножение', 'O(log n)'],
                    ]
                )
                + '<h3>Мастер-теорема</h3>'
                '<p>Для рекуррентности T(n) = a * T(n/b) + O(n^d):</p>'
                '<ul>'
                '<li>d &lt; log_b(a): T(n) = O(n^log_b(a))</li>'
                '<li>d = log_b(a): T(n) = O(n^d * log n)</li>'
                '<li>d &gt; log_b(a): T(n) = O(n^d)</li>'
                '</ul>'
                '<p>Merge Sort: a=2, b=2, d=1. log_2(2)=1=d, значит O(n log n).</p>'
            ),
        },
        {
            'title': 'Стратегии решения алгоритмических задач',
            'order': 4,
            'minutes': 12,
            'code': (
                '# 1. Метод двух указателей\n'
                'def is_palindrome(s):\n'
                '    s = s.lower()\n'
                '    left, right = 0, len(s) - 1\n'
                '    while left < right:\n'
                '        if s[left] != s[right]:\n'
                '            return False\n'
                '        left += 1\n'
                '        right -= 1\n'
                '    return True\n\n'
                'print(is_palindrome("шалаш"))  # True\n\n'
                '# 2. Скользящее окно\n'
                'def max_sum_subarray(arr, k):\n'
                '    """Максимальная сумма подмассива длины k."""\n'
                '    window = sum(arr[:k])\n'
                '    best = window\n'
                '    for i in range(k, len(arr)):\n'
                '        window += arr[i] - arr[i - k]\n'
                '        best = max(best, window)\n'
                '    return best\n\n'
                'print(max_sum_subarray([1, 4, 2, 10, 2, 3, 1, 0, 20], 3))  # 24\n\n'
                '# 3. Стек для скобок\n'
                'def is_balanced(s):\n'
                '    stack = []\n'
                '    pairs = {")": "(", "]": "[", "}": "{"}\n'
                '    for ch in s:\n'
                '        if ch in "([{":\n'
                '            stack.append(ch)\n'
                '        elif ch in ")]}":\n'
                '            if not stack or stack[-1] != pairs[ch]:\n'
                '                return False\n'
                '            stack.pop()\n'
                '    return len(stack) == 0\n\n'
                'print(is_balanced("({[]})"))  # True\n'
                'print(is_balanced("({[})"))   # False'
            ),
            'content': (
                '<h2>Стратегии решения алгоритмических задач</h2>'
                '<p>Знание типовых техник помогает распознавать задачи и '
                'быстро находить решение.</p>'
                '<h3>Основные техники</h3>'
                + info_table(
                    ['Техника', 'Когда использовать', 'Пример задачи'],
                    [
                        ['Два указателя', 'Отсортированный массив, строки',
                         'Палиндром, сумма пары'],
                        ['Скользящее окно', 'Подмассив/подстрока фиксированной длины',
                         'Максимальная сумма подмассива'],
                        ['Стек', 'Скобки, вложенность, история',
                         'Проверка скобок, обратная польская'],
                        ['Хеш-таблица', 'Быстрый поиск, подсчёт',
                         'Two Sum, анаграммы'],
                        ['BFS/DFS', 'Графы, деревья, лабиринты',
                         'Кратчайший путь, обход'],
                    ]
                )
                + '<h3>Метод двух указателей</h3>'
                '<p>Два указателя движутся навстречу или в одном направлении:</p>'
                + code_block(
                    '# Удалить дубликаты из отсортированного массива\n'
                    'def remove_duplicates(arr):\n'
                    '    if not arr:\n'
                    '        return []\n'
                    '    write = 0\n'
                    '    for read in range(1, len(arr)):\n'
                    '        if arr[read] != arr[write]:\n'
                    '            write += 1\n'
                    '            arr[write] = arr[read]\n'
                    '    return arr[:write + 1]\n\n'
                    'print(remove_duplicates([1, 1, 2, 3, 3, 4]))  # [1, 2, 3, 4]'
                )
                + '<h3>Как подступиться к задаче</h3>'
                '<ul>'
                '<li>Поймите задачу: перефразируйте своими словами</li>'
                '<li>Разберите примеры вручную</li>'
                '<li>Определите тип задачи (поиск, сортировка, граф...)</li>'
                '<li>Начните с грубой силы (brute force), потом оптимизируйте</li>'
                '<li>Проверьте граничные случаи: пустой ввод, один элемент, дубликаты</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Анализ сложности на практике',
            'order': 5,
            'minutes': 10,
            'code': (
                'import time\n\n'
                '# O(1) - константная\n'
                'def get_first(arr):\n'
                '    return arr[0] if arr else None\n\n'
                '# O(log n) - логарифмическая\n'
                'def binary_search(arr, target):\n'
                '    lo, hi = 0, len(arr) - 1\n'
                '    while lo <= hi:\n'
                '        mid = (lo + hi) // 2\n'
                '        if arr[mid] == target: return mid\n'
                '        elif arr[mid] < target: lo = mid + 1\n'
                '        else: hi = mid - 1\n'
                '    return -1\n\n'
                '# O(n) - линейная\n'
                'def find_max(arr):\n'
                '    mx = arr[0]\n'
                '    for x in arr:\n'
                '        if x > mx:\n'
                '            mx = x\n'
                '    return mx\n\n'
                '# O(n^2) - квадратичная\n'
                'def has_duplicate_naive(arr):\n'
                '    for i in range(len(arr)):\n'
                '        for j in range(i + 1, len(arr)):\n'
                '            if arr[i] == arr[j]:\n'
                '                return True\n'
                '    return False\n\n'
                '# Замер на разных размерах\n'
                'for n in [1000, 5000, 10000]:\n'
                '    arr = list(range(n))\n'
                '    start = time.perf_counter()\n'
                '    has_duplicate_naive(arr)\n'
                '    elapsed = time.perf_counter() - start\n'
                '    print(f"n={n:>5}: {elapsed:.4f} сек")\n'
                '# n= 1000: ~0.05 сек\n'
                '# n= 5000: ~1.2 сек   (x25 при x5 размера)\n'
                '# n=10000: ~4.8 сек   (квадратичный рост!)'
            ),
            'content': (
                '<h2>Анализ сложности на практике</h2>'
                '<p>Понимание сложности алгоритмов помогает писать '
                'эффективный код и предсказывать время работы.</p>'
                '<h3>Шпаргалка по сложностям</h3>'
                + info_table(
                    ['O(...)', 'Название', 'n=1000', 'Пример'],
                    [
                        ['O(1)', 'Константная', '1 оп.', 'Доступ по индексу'],
                        ['O(log n)', 'Логарифмическая', '~10 оп.',
                         'Бинарный поиск'],
                        ['O(n)', 'Линейная', '1000 оп.', 'Поиск максимума'],
                        ['O(n log n)', 'Линейно-логарифмическая', '~10 000 оп.',
                         'Сортировка'],
                        ['O(n^2)', 'Квадратичная', '1 000 000 оп.',
                         'Вложенные циклы'],
                        ['O(2^n)', 'Экспоненциальная', '~10^301 оп.',
                         'Все подмножества'],
                    ]
                )
                + '<h3>Как определить сложность</h3>'
                '<ul>'
                '<li>Один цикл по n элементам: O(n)</li>'
                '<li>Вложенный цикл: O(n^2)</li>'
                '<li>Деление пополам: O(log n)</li>'
                '<li>Рекурсия с двумя вызовами: O(2^n)</li>'
                '<li>Сортировка + один проход: O(n log n)</li>'
                '</ul>'
                '<h3>Пространственная сложность</h3>'
                '<p>Помимо времени, оцениваем используемую память:</p>'
                + code_block(
                    '# O(1) по памяти - модификация на месте\n'
                    'def reverse_in_place(arr):\n'
                    '    left, right = 0, len(arr) - 1\n'
                    '    while left &lt; right:\n'
                    '        arr[left], arr[right] = arr[right], arr[left]\n'
                    '        left += 1; right -= 1\n\n'
                    '# O(n) по памяти - новый массив\n'
                    'def reverse_copy(arr):\n'
                    '    return arr[::-1]'
                )
                + '<h3>Как оптимизировать</h3>'
                + info_table(
                    ['Было', 'Стало', 'Приём'],
                    [
                        ['O(n^2) поиск дубликатов', 'O(n)', 'Использовать set'],
                        ['O(n^2) сортировка', 'O(n log n)', 'sorted() / Timsort'],
                        ['O(2^n) Фибоначчи', 'O(n)', 'Мемоизация / DP'],
                        ['O(n) поиск', 'O(log n)', 'Отсортировать + bisect'],
                    ]
                )
                + '<h3>Практическое правило</h3>'
                '<p>Python выполняет ~10^7 простых операций в секунду. '
                'Для n=10^6 алгоритм O(n^2) будет работать ~1000 секунд. '
                'O(n log n) - около 20 секунд. O(n) - около 0.1 секунды.</p>'
            ),
        },
    ],
}


class Command(BaseCommand):
    help = 'Rasshiryaet moduli 13-20 OAIP do 5+ urokov'

    def handle(self, *args, **options):
        oaip = Subject.objects.get(title__contains='ОАИП')
        modules = {m.order: m for m in oaip.modules.order_by('order')}

        added = 0
        for m_order, lessons_data in sorted(LESSONS.items()):
            module = modules.get(m_order)
            if not module:
                self.stdout.write('[SKIP] Module %d not found' % m_order)
                continue

            existing = set(module.lessons.values_list('title', flat=True))

            for ld in lessons_data:
                if ld['title'] in existing:
                    self.stdout.write(
                        '[SKIP] M%d: %s (exists)' % (m_order, ld['title'][:40])
                    )
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
                    '[+] M%d L%d: %s' % (m_order, ld['order'], ld['title'][:45])
                ))

        self.stdout.write(self.style.SUCCESS(
            '\n[DONE] Added %d lessons' % added
        ))
