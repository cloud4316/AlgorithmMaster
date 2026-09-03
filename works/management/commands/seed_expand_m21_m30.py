# -*- coding: utf-8 -*-
"""
Seed-команда: добавляет уроки в модули 21-30 (ОАИП Python),
чтобы в каждом было минимум 5 уроков.

Запуск:
    python manage.py seed_expand_m21_m30
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


# ---------------------------------------------------------------------------
# Хелперы для генерации HTML
# ---------------------------------------------------------------------------

def code_block(code, lang="python"):
    """Оборачивает код в <pre><code>."""
    return (
        '<pre><code class="language-' + lang + '">'
        + code
        + "</code></pre>"
    )


def info_table(headers, rows):
    """Генерирует HTML-таблицу."""
    html = '<table class="table table-bordered table-striped">'
    html += "<thead><tr>"
    for h in headers:
        html += "<th>" + h + "</th>"
    html += "</tr></thead><tbody>"
    for row in rows:
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html


# ---------------------------------------------------------------------------
# Данные уроков: ключ -- order модуля, значение -- список словарей
# ---------------------------------------------------------------------------

LESSONS = {
    # ==== M21: Comprehensions и lambda ====
    21: [
        {
            "title": "Вложенные comprehensions",
            "order": 4,
            "minutes": 12,
            "code": (
                "# Транспонирование матрицы через вложенный list comprehension\n"
                "matrix = [\n"
                "    [1, 2, 3],\n"
                "    [4, 5, 6],\n"
                "    [7, 8, 9],\n"
                "]\n\n"
                "transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]\n"
                "print(transposed)  # [[1, 4, 7], [2, 5, 8], [3, 6, 9]]\n\n"
                "# Flat-список из вложенного\n"
                "flat = [x for row in matrix for x in row]\n"
                "print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]\n\n"
                "# Фильтрация внутри вложенного comprehension\n"
                "even_pairs = [\n"
                "    (i, j)\n"
                "    for i in range(5)\n"
                "    for j in range(5)\n"
                "    if (i + j) % 2 == 0\n"
                "]\n"
                "print(even_pairs[:6])  # [(0, 0), (0, 2), (0, 4), (1, 1), (1, 3), (2, 0)]"
            ),
            "content": (
                "<h2>Вложенные list comprehensions</h2>"
                "<p>Вложенные генераторы списков позволяют обрабатывать "
                "многомерные структуры данных в одну строку. Порядок циклов "
                "повторяет порядок обычных вложенных <code>for</code>.</p>"

                "<h3>Синтаксис</h3>"
                + code_block(
                    "[выражение for внешний in коллекция1 for внутренний in коллекция2]"
                )
                + "<p>Первый <code>for</code> -- внешний цикл, второй -- внутренний.</p>"

                "<h3>Типичные задачи</h3>"
                + info_table(
                    ["Задача", "Comprehension"],
                    [
                        ["Flat-список", "[x for row in matrix for x in row]"],
                        ["Транспонирование", "[[row[i] for row in m] for i in range(cols)]"],
                        ["Декартово произведение", "[(a, b) for a in A for b in B]"],
                        ["Фильтрация пар", "[(i,j) for i in R for j in R if cond]"],
                    ],
                )
                + "<h3>Когда НЕ использовать</h3>"
                "<p>Если вложенность больше двух уровней, читаемость резко падает. "
                "В таких случаях лучше написать обычные циклы или вынести "
                "логику в отдельную функцию.</p>"

                "<h3>Производительность</h3>"
                "<p>Вложенные comprehensions работают быстрее эквивалентных "
                "вложенных циклов с <code>append()</code>, поскольку Python "
                "оптимизирует генераторы списков на уровне байт-кода.</p>"
            ),
        },
        {
            "title": "Практические паттерны comprehensions",
            "order": 5,
            "minutes": 10,
            "code": (
                "# Словарь частот символов\n"
                "text = 'hello world'\n"
                "freq = {ch: text.count(ch) for ch in set(text) if ch != ' '}\n"
                "print(freq)  # {'h': 1, 'e': 1, 'l': 3, 'o': 2, ...}\n\n"
                "# Инвертирование словаря\n"
                "original = {'a': 1, 'b': 2, 'c': 3}\n"
                "inverted = {v: k for k, v in original.items()}\n"
                "print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}\n\n"
                "# Группировка по длине слова\n"
                "words = ['cat', 'dog', 'elephant', 'ant', 'bear']\n"
                "from itertools import groupby\n"
                "groups = {k: list(g) for k, g in groupby(sorted(words, key=len), key=len)}\n"
                "print(groups)  # {3: ['ant', 'cat', 'dog'], 4: ['bear'], 8: ['elephant']}\n\n"
                "# Walrus-оператор в comprehension (Python 3.8+)\n"
                "import math\n"
                "results = [y for x in range(20) if (y := math.sqrt(x)) == int(y)]\n"
                "print(results)  # [0.0, 1.0, 2.0, 3.0, 4.0]"
            ),
            "content": (
                "<h2>Практические паттерны comprehensions</h2>"
                "<p>Рассмотрим реальные задачи, где comprehensions заменяют "
                "многострочный код одной выразительной конструкцией.</p>"

                "<h3>Словарь частот</h3>"
                "<p>Подсчёт частоты элементов -- одна из самых распространённых задач. "
                "Dict comprehension делает это лаконично:</p>"
                + code_block(
                    "freq = {ch: text.count(ch) for ch in set(text) if ch.isalpha()}"
                )

                + "<h3>Инвертирование словаря</h3>"
                "<p>Меняем местами ключи и значения. Работает, если значения уникальны:</p>"
                + code_block("inverted = {v: k for k, v in d.items()}")

                + "<h3>Walrus-оператор (:=)</h3>"
                "<p>С Python 3.8 можно сохранять промежуточный результат "
                "прямо внутри comprehension через <code>:=</code>. "
                "Это избавляет от повторных вычислений:</p>"
                + code_block(
                    "# Без walrus: вычисление дважды\n"
                    "[f(x) for x in data if f(x) > 0]\n\n"
                    "# С walrus: вычисление один раз\n"
                    "[y for x in data if (y := f(x)) > 0]"
                )

                + "<h3>Set comprehension для дедупликации</h3>"
                + code_block(
                    "emails = ['a@b.com', 'A@B.COM', 'c@d.com', 'a@b.com']\n"
                    "unique = {e.lower() for e in emails}\n"
                    "print(unique)  # {'a@b.com', 'c@d.com'}"
                )

                + "<h3>Когда использовать какой тип</h3>"
                + info_table(
                    ["Тип", "Когда применять"],
                    [
                        ["list comprehension", "Нужен упорядоченный результат"],
                        ["dict comprehension", "Маппинг ключ-значение"],
                        ["set comprehension", "Уникальные элементы"],
                        ["generator expression", "Ленивая обработка, экономия памяти"],
                    ],
                )
            ),
        },
    ],

    # ==== M22: Сложность алгоритмов Big O ====
    22: [
        {
            "title": "Амортизированный анализ",
            "order": 4,
            "minutes": 12,
            "code": (
                "# Демонстрация амортизированной сложности list.append()\n"
                "import sys\n\n"
                "lst = []\n"
                "prev_size = 0\n"
                "for i in range(20):\n"
                "    lst.append(i)\n"
                "    curr_size = sys.getsizeof(lst)\n"
                "    if curr_size != prev_size:\n"
                "        print('i={0:2d}  len={1:2d}  bytes={2}  (расширение)'.format(\n"
                "            i, len(lst), curr_size))\n"
                "        prev_size = curr_size\n\n"
                "# Вывод показывает, что расширение происходит не каждый раз,\n"
                "# а через увеличивающиеся интервалы:\n"
                "# i= 0  len= 1  bytes=88   (расширение)\n"
                "# i= 4  len= 5  bytes=120  (расширение)\n"
                "# i= 8  len= 9  bytes=184  (расширение)\n"
                "# i=16  len=17  bytes=256  (расширение)\n"
                "# Амортизированная сложность append: O(1)"
            ),
            "content": (
                "<h2>Амортизированный анализ сложности</h2>"
                "<p>Амортизированный анализ оценивает <strong>среднюю</strong> "
                "стоимость операции в серии из <em>n</em> операций, даже если "
                "отдельная операция может быть дорогой.</p>"

                "<h3>Зачем нужен</h3>"
                "<p>Обычный worst-case анализ иногда слишком пессимистичен. "
                "Например, <code>list.append()</code> в Python иногда вызывает "
                "расширение массива за O(n), но в среднем работает за O(1).</p>"

                "<h3>Метод банковского счёта</h3>"
                "<p>Идея: каждая дешёвая операция 'откладывает' дополнительную работу "
                "на будущую дорогую операцию.</p>"
                + info_table(
                    ["Операция", "Реальная стоимость", "Амортизированная"],
                    [
                        ["append (без расширения)", "O(1)", "O(1)"],
                        ["append (с расширением)", "O(n)", "O(1)"],
                        ["Удаление из начала deque", "O(1)", "O(1)"],
                        ["Удаление из начала list", "O(n)", "O(n)"],
                    ],
                )

                + "<h3>Примеры в Python</h3>"
                + info_table(
                    ["Структура", "Операция", "Worst-case", "Амортизированная"],
                    [
                        ["list", "append", "O(n)", "O(1)"],
                        ["dict", "вставка", "O(n)", "O(1)"],
                        ["set", "add", "O(n)", "O(1)"],
                        ["deque", "append/appendleft", "O(1)", "O(1)"],
                    ],
                )

                + "<h3>Практическое значение</h3>"
                "<p>При выборе структуры данных важно учитывать именно "
                "амортизированную сложность: именно она определяет реальное "
                "время работы программы при большом количестве операций.</p>"
            ),
        },
        {
            "title": "Пространственная сложность",
            "order": 5,
            "minutes": 10,
            "code": (
                "import sys\n\n"
                "# Сравнение памяти: список vs генератор\n"
                "lst = [i * i for i in range(1000000)]\n"
                "gen = (i * i for i in range(1000000))\n\n"
                "print('Список:', sys.getsizeof(lst), 'байт')   # ~8 МБ\n"
                "print('Генератор:', sys.getsizeof(gen), 'байт') # ~200 байт\n\n"
                "# O(1) по памяти: суммирование через генератор\n"
                "total = sum(i * i for i in range(1000000))\n\n"
                "# O(n) по памяти: рекурсия без оптимизации\n"
                "def factorial_recursive(n):\n"
                "    if n <= 1:\n"
                "        return 1\n"
                "    return n * factorial_recursive(n - 1)\n\n"
                "# O(1) по памяти: итеративный вариант\n"
                "def factorial_iterative(n):\n"
                "    result = 1\n"
                "    for i in range(2, n + 1):\n"
                "        result *= i\n"
                "    return result"
            ),
            "content": (
                "<h2>Пространственная сложность (Space Complexity)</h2>"
                "<p>Пространственная сложность показывает, сколько "
                "<strong>дополнительной памяти</strong> потребляет алгоритм "
                "в зависимости от размера входных данных.</p>"

                "<h3>Виды памяти</h3>"
                + info_table(
                    ["Вид", "Описание"],
                    [
                        ["Входные данные", "Память под сами данные (не считается)"],
                        ["Вспомогательная", "Доп. структуры, созданные алгоритмом"],
                        ["Стек вызовов", "Память рекурсивных вызовов"],
                    ],
                )

                + "<h3>Типичные примеры</h3>"
                + info_table(
                    ["Сложность", "Пример"],
                    [
                        ["O(1)", "Поиск максимума в массиве (одна переменная)"],
                        ["O(log n)", "Рекурсивный бинарный поиск (глубина стека)"],
                        ["O(n)", "Копия массива, merge sort (вспомогательный массив)"],
                        ["O(n^2)", "Матрица смежности графа n вершин"],
                    ],
                )

                + "<h3>Генераторы и ленивые вычисления</h3>"
                "<p>В Python генераторы (<code>yield</code>, generator expressions) "
                "позволяют обрабатывать данные по одному элементу, используя "
                "O(1) дополнительной памяти вместо O(n).</p>"

                "<h3>Компромисс время-память</h3>"
                "<p>Часто можно ускорить алгоритм, используя больше памяти "
                "(мемоизация, хеш-таблицы), или сэкономить память за счёт "
                "повторных вычислений. Этот компромисс (time-space tradeoff) -- "
                "фундаментальная идея в computer science.</p>"
                + code_block(
                    "# Time-space tradeoff: два подхода к поиску дубликатов\n\n"
                    "# O(n) время, O(n) память -- через set\n"
                    "def has_dup_set(arr):\n"
                    "    seen = set()\n"
                    "    for x in arr:\n"
                    "        if x in seen:\n"
                    "            return True\n"
                    "        seen.add(x)\n"
                    "    return False\n\n"
                    "# O(n log n) время, O(1) память -- через сортировку\n"
                    "def has_dup_sort(arr):\n"
                    "    arr.sort()\n"
                    "    for i in range(1, len(arr)):\n"
                    "        if arr[i] == arr[i-1]:\n"
                    "            return True\n"
                    "    return False"
                )
            ),
        },
    ],

    # ==== M23: Стек, очередь, дек ====
    23: [
        {
            "title": "Проверка сбалансированности скобок (стек)",
            "order": 4,
            "minutes": 10,
            "code": (
                "def is_balanced(expression):\n"
                "    \"\"\"Проверяет сбалансированность скобок ()[]{}.\"\"\"\n"
                "    stack = []\n"
                "    pairs = {')': '(', ']': '[', '}': '{'}\n\n"
                "    for ch in expression:\n"
                "        if ch in '([{':\n"
                "            stack.append(ch)\n"
                "        elif ch in ')]}':\n"
                "            if not stack or stack[-1] != pairs[ch]:\n"
                "                return False\n"
                "            stack.pop()\n\n"
                "    return len(stack) == 0\n\n"
                "# Тесты\n"
                "print(is_balanced('({[]})'))    # True\n"
                "print(is_balanced('([)]'))      # False\n"
                "print(is_balanced('((()))'))    # True\n"
                "print(is_balanced('}{'))        # False\n\n"
                "# Применение: проверка HTML-тегов\n"
                "import re\n\n"
                "def check_html_tags(html):\n"
                "    tags = re.findall(r'<(/?)([a-z]+)[^>]*>', html)\n"
                "    stack = []\n"
                "    for is_closing, name in tags:\n"
                "        if not is_closing:\n"
                "            stack.append(name)\n"
                "        elif stack and stack[-1] == name:\n"
                "            stack.pop()\n"
                "        else:\n"
                "            return False\n"
                "    return len(stack) == 0"
            ),
            "content": (
                "<h2>Практика стека: проверка скобок</h2>"
                "<p>Проверка сбалансированности скобок -- классическая задача, "
                "идеально решаемая с помощью стека.</p>"

                "<h3>Алгоритм</h3>"
                "<ol>"
                "<li>Идём по строке слева направо</li>"
                "<li>Открывающую скобку кладём в стек</li>"
                "<li>Закрывающая: проверяем, что вершина стека -- парная открывающая</li>"
                "<li>В конце стек должен быть пуст</li>"
                "</ol>"

                "<h3>Сложность</h3>"
                + info_table(
                    ["Метрика", "Значение"],
                    [
                        ["Время", "O(n), один проход по строке"],
                        ["Память", "O(n) в худшем случае (все открывающие)"],
                    ],
                )

                + "<h3>Другие применения стека</h3>"
                + info_table(
                    ["Задача", "Как используется стек"],
                    [
                        ["Обратная польская нотация", "Операнды в стек, оператор снимает два"],
                        ["Undo/Redo в редакторе", "Стек действий и стек отменённых"],
                        ["Обход дерева (DFS)", "Стек хранит путь от корня"],
                        ["Вычисление выражений", "Два стека: операнды и операторы"],
                        ["Проверка HTML-тегов", "Открывающие теги в стек"],
                    ],
                )

                + "<h3>Обратная польская нотация (RPN)</h3>"
                "<p>Выражение <code>3 4 + 2 *</code> означает <code>(3 + 4) * 2 = 14</code>. "
                "Алгоритм вычисления RPN использует стек: числа кладутся в стек, "
                "оператор снимает два верхних и кладёт результат обратно.</p>"
            ),
        },
        {
            "title": "Очередь в задачах: BFS и очередь задач",
            "order": 5,
            "minutes": 12,
            "code": (
                "from collections import deque\n\n"
                "# BFS -- обход графа в ширину через очередь\n"
                "def bfs(graph, start):\n"
                "    visited = set()\n"
                "    queue = deque([start])\n"
                "    visited.add(start)\n"
                "    order = []\n\n"
                "    while queue:\n"
                "        node = queue.popleft()   # O(1) -- именно поэтому deque\n"
                "        order.append(node)\n"
                "        for neighbor in graph[node]:\n"
                "            if neighbor not in visited:\n"
                "                visited.add(neighbor)\n"
                "                queue.append(neighbor)\n\n"
                "    return order\n\n"
                "graph = {\n"
                "    'A': ['B', 'C'],\n"
                "    'B': ['A', 'D', 'E'],\n"
                "    'C': ['A', 'F'],\n"
                "    'D': ['B'],\n"
                "    'E': ['B', 'F'],\n"
                "    'F': ['C', 'E'],\n"
                "}\n"
                "print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E', 'F']\n\n"
                "# Очередь задач (простой пример)\n"
                "class TaskQueue:\n"
                "    def __init__(self):\n"
                "        self.queue = deque()\n\n"
                "    def add_task(self, task):\n"
                "        self.queue.append(task)\n\n"
                "    def process_next(self):\n"
                "        if self.queue:\n"
                "            task = self.queue.popleft()\n"
                "            print('Выполняю:', task)\n"
                "            return task\n"
                "        print('Очередь пуста')\n"
                "        return None"
            ),
            "content": (
                "<h2>Очередь в практических задачах</h2>"
                "<p>Очередь (FIFO) -- ключевая структура для алгоритма BFS "
                "и систем обработки задач.</p>"

                "<h3>BFS через очередь</h3>"
                "<p>Обход в ширину (Breadth-First Search) использует очередь "
                "для послойного обхода графа. Каждый уровень обрабатывается "
                "полностью, прежде чем перейти к следующему.</p>"
                + info_table(
                    ["Шаг", "Действие"],
                    [
                        ["1", "Поместить стартовую вершину в очередь"],
                        ["2", "Извлечь вершину из начала очереди"],
                        ["3", "Добавить непосещённых соседей в конец"],
                        ["4", "Повторять, пока очередь не пуста"],
                    ],
                )

                + "<h3>Почему deque, а не list</h3>"
                + info_table(
                    ["Операция", "list", "deque"],
                    [
                        ["append (конец)", "O(1)*", "O(1)"],
                        ["pop(0) / popleft()", "O(n)", "O(1)"],
                        ["Доступ по индексу", "O(1)", "O(n)"],
                    ],
                )
                + "<p>* -- амортизированная сложность</p>"
                "<p>Для очереди критична операция извлечения из начала. "
                "<code>deque.popleft()</code> работает за O(1), тогда как "
                "<code>list.pop(0)</code> за O(n), поскольку сдвигает все элементы.</p>"

                "<h3>Практические применения очереди</h3>"
                + info_table(
                    ["Область", "Пример"],
                    [
                        ["Алгоритмы", "BFS, поиск кратчайшего пути"],
                        ["Веб-серверы", "Очередь запросов"],
                        ["Принтеры", "Очередь печати"],
                        ["Планировщик ОС", "Планирование процессов (Round Robin)"],
                    ],
                )
            ),
        },
    ],

    # ==== M24: Связный список ====
    24: [
        {
            "title": "Кольцевой связный список",
            "order": 4,
            "minutes": 12,
            "code": (
                "class Node:\n"
                "    def __init__(self, data):\n"
                "        self.data = data\n"
                "        self.next = None\n\n"
                "class CircularLinkedList:\n"
                "    def __init__(self):\n"
                "        self.head = None\n\n"
                "    def append(self, data):\n"
                "        new_node = Node(data)\n"
                "        if not self.head:\n"
                "            self.head = new_node\n"
                "            new_node.next = self.head\n"
                "            return\n"
                "        current = self.head\n"
                "        while current.next != self.head:\n"
                "            current = current.next\n"
                "        current.next = new_node\n"
                "        new_node.next = self.head\n\n"
                "    def display(self):\n"
                "        if not self.head:\n"
                "            print('Список пуст')\n"
                "            return\n"
                "        elements = []\n"
                "        current = self.head\n"
                "        while True:\n"
                "            elements.append(str(current.data))\n"
                "            current = current.next\n"
                "            if current == self.head:\n"
                "                break\n"
                "        print(' -> '.join(elements) + ' -> (head)')\n\n"
                "    def length(self):\n"
                "        if not self.head:\n"
                "            return 0\n"
                "        count = 1\n"
                "        current = self.head.next\n"
                "        while current != self.head:\n"
                "            count += 1\n"
                "            current = current.next\n"
                "        return count\n\n"
                "cll = CircularLinkedList()\n"
                "for x in [10, 20, 30, 40]:\n"
                "    cll.append(x)\n"
                "cll.display()  # 10 -> 20 -> 30 -> 40 -> (head)"
            ),
            "content": (
                "<h2>Кольцевой (циклический) связный список</h2>"
                "<p>В кольцевом связном списке последний элемент указывает "
                "на первый, образуя замкнутый цикл. Это позволяет бесконечно "
                "обходить элементы.</p>"

                "<h3>Отличия от обычного списка</h3>"
                + info_table(
                    ["Свойство", "Обычный", "Кольцевой"],
                    [
                        ["Последний узел", "next = None", "next = head"],
                        ["Конец обхода", "current is None", "current == head"],
                        ["Круговой обход", "Невозможен", "Бесконечный цикл"],
                    ],
                )

                + "<h3>Применения</h3>"
                "<ul>"
                "<li><strong>Round Robin</strong> -- планирование задач ОС: "
                "каждый процесс получает квант времени по кругу</li>"
                "<li><strong>Кольцевой буфер</strong> -- аудио/видео потоки, "
                "буферизация ввода</li>"
                "<li><strong>Карусель</strong> -- циклический слайдер на веб-странице</li>"
                "<li><strong>Игры</strong> -- ходы игроков по кругу</li>"
                "</ul>"

                "<h3>Задача Иосифа Флавия</h3>"
                "<p>Классическая задача: <em>n</em> человек стоят в круге, "
                "каждый <em>k</em>-й выбывает. Кто останется последним? "
                "Решается через кольцевой список за O(n*k).</p>"
            ),
        },
        {
            "title": "Сравнение связного списка с массивом",
            "order": 5,
            "minutes": 10,
            "code": (
                "import time\n\n"
                "# Вставка в начало: list vs связный список\n"
                "n = 50000\n\n"
                "# list -- вставка в начало O(n)\n"
                "arr = []\n"
                "t0 = time.perf_counter()\n"
                "for i in range(n):\n"
                "    arr.insert(0, i)\n"
                "t1 = time.perf_counter()\n"
                "print('list.insert(0): {:.3f} сек'.format(t1 - t0))\n\n"
                "# collections.deque -- вставка в начало O(1)\n"
                "from collections import deque\n"
                "d = deque()\n"
                "t0 = time.perf_counter()\n"
                "for i in range(n):\n"
                "    d.appendleft(i)\n"
                "t1 = time.perf_counter()\n"
                "print('deque.appendleft: {:.3f} сек'.format(t1 - t0))\n\n"
                "# Вывод: для частых вставок в начало deque (двусвязный список)\n"
                "# значительно быстрее, чем list (массив)."
            ),
            "content": (
                "<h2>Связный список vs массив (list в Python)</h2>"
                "<p>Понимание различий помогает выбрать правильную структуру "
                "данных для конкретной задачи.</p>"

                "<h3>Сравнение операций</h3>"
                + info_table(
                    ["Операция", "Массив (list)", "Связный список"],
                    [
                        ["Доступ по индексу", "O(1)", "O(n)"],
                        ["Поиск элемента", "O(n)", "O(n)"],
                        ["Вставка в начало", "O(n)", "O(1)"],
                        ["Вставка в конец", "O(1)*", "O(1) при хранении tail"],
                        ["Вставка в середину", "O(n)", "O(1) если есть указатель"],
                        ["Удаление из начала", "O(n)", "O(1)"],
                        ["Удаление из конца", "O(1)", "O(n) для односвязного"],
                        ["Использование памяти", "Компактно", "Больше (указатели)"],
                    ],
                )
                + "<p>* -- амортизированная сложность</p>"

                "<h3>Когда выбирать связный список</h3>"
                "<ul>"
                "<li>Частые вставки/удаления в начале или середине</li>"
                "<li>Размер данных непредсказуем и меняется часто</li>"
                "<li>Не нужен доступ по индексу</li>"
                "</ul>"

                "<h3>Когда выбирать массив</h3>"
                "<ul>"
                "<li>Нужен быстрый доступ по индексу</li>"
                "<li>Данные в основном читаются, а не модифицируются</li>"
                "<li>Важна локальность данных в памяти (кэш CPU)</li>"
                "</ul>"

                "<h3>Python и связные списки</h3>"
                "<p>В стандартной библиотеке Python нет явного связного списка. "
                "<code>collections.deque</code> внутри реализован как двусвязный "
                "список блоков и подходит, когда нужны быстрые вставки/удаления "
                "с обоих концов.</p>"
            ),
        },
    ],

    # ==== M25: Бинарное дерево поиска BST (нужен 1 урок) ====
    25: [
        {
            "title": "Основы AVL-дерева (самобалансирующееся BST)",
            "order": 5,
            "minutes": 15,
            "code": (
                "class AVLNode:\n"
                "    def __init__(self, key):\n"
                "        self.key = key\n"
                "        self.left = None\n"
                "        self.right = None\n"
                "        self.height = 1\n\n"
                "def get_height(node):\n"
                "    return node.height if node else 0\n\n"
                "def get_balance(node):\n"
                "    if not node:\n"
                "        return 0\n"
                "    return get_height(node.left) - get_height(node.right)\n\n"
                "def rotate_right(y):\n"
                "    x = y.left\n"
                "    t2 = x.right\n"
                "    x.right = y\n"
                "    y.left = t2\n"
                "    y.height = 1 + max(get_height(y.left), get_height(y.right))\n"
                "    x.height = 1 + max(get_height(x.left), get_height(x.right))\n"
                "    return x\n\n"
                "def rotate_left(x):\n"
                "    y = x.right\n"
                "    t2 = y.left\n"
                "    y.left = x\n"
                "    x.right = t2\n"
                "    x.height = 1 + max(get_height(x.left), get_height(x.right))\n"
                "    y.height = 1 + max(get_height(y.left), get_height(y.right))\n"
                "    return y\n\n"
                "def insert(node, key):\n"
                "    if not node:\n"
                "        return AVLNode(key)\n"
                "    if key < node.key:\n"
                "        node.left = insert(node.left, key)\n"
                "    elif key > node.key:\n"
                "        node.right = insert(node.right, key)\n"
                "    else:\n"
                "        return node  # дубликаты не вставляем\n\n"
                "    node.height = 1 + max(get_height(node.left), get_height(node.right))\n"
                "    balance = get_balance(node)\n\n"
                "    # Left-Left\n"
                "    if balance > 1 and key < node.left.key:\n"
                "        return rotate_right(node)\n"
                "    # Right-Right\n"
                "    if balance < -1 and key > node.right.key:\n"
                "        return rotate_left(node)\n"
                "    # Left-Right\n"
                "    if balance > 1 and key > node.left.key:\n"
                "        node.left = rotate_left(node.left)\n"
                "        return rotate_right(node)\n"
                "    # Right-Left\n"
                "    if balance < -1 and key < node.right.key:\n"
                "        node.right = rotate_right(node.right)\n"
                "        return rotate_left(node)\n\n"
                "    return node\n\n"
                "# Использование\n"
                "root = None\n"
                "for val in [10, 20, 30, 40, 50, 25]:\n"
                "    root = insert(root, val)\n"
                "print('Корень:', root.key)           # 30\n"
                "print('Высота:', get_height(root))   # 3"
            ),
            "content": (
                "<h2>AVL-дерево: самобалансирующееся BST</h2>"
                "<p>AVL-дерево -- вариант BST, в котором для каждого узла "
                "разница высот левого и правого поддеревьев не превышает 1. "
                "Это гарантирует O(log n) для всех операций.</p>"

                "<h3>Проблема обычного BST</h3>"
                "<p>При вставке отсортированных данных BST вырождается в "
                "линейный список, и операции становятся O(n).</p>"

                "<h3>Баланс-фактор</h3>"
                + code_block("balance(node) = height(left) - height(right)")
                + "<p>Допустимые значения: -1, 0, +1. Если баланс выходит за "
                "эти пределы, нужна ротация.</p>"

                "<h3>Четыре типа ротаций</h3>"
                + info_table(
                    ["Случай", "Баланс", "Ротация"],
                    [
                        ["Left-Left", "+2, левый +1", "Правая"],
                        ["Right-Right", "-2, правый -1", "Левая"],
                        ["Left-Right", "+2, левый -1", "Левая + Правая"],
                        ["Right-Left", "-2, правый +1", "Правая + Левая"],
                    ],
                )

                + "<h3>Сравнение BST и AVL</h3>"
                + info_table(
                    ["Метрика", "BST (worst)", "AVL"],
                    [
                        ["Поиск", "O(n)", "O(log n)"],
                        ["Вставка", "O(n)", "O(log n)"],
                        ["Удаление", "O(n)", "O(log n)"],
                        ["Память (доп.)", "-", "+1 int на узел (height)"],
                    ],
                )

                + "<h3>Применение</h3>"
                "<p>AVL-деревья используются в базах данных и файловых системах, "
                "где важна гарантированная скорость поиска. В Python для "
                "аналогичных задач часто используют модуль <code>bisect</code> "
                "или сторонние библиотеки вроде <code>sortedcontainers</code>.</p>"
            ),
        },
    ],

    # ==== M26: Графы BFS и DFS ====
    26: [
        {
            "title": "Алгоритм Дейкстры (кратчайший путь)",
            "order": 4,
            "minutes": 15,
            "code": (
                "import heapq\n\n"
                "def dijkstra(graph, start):\n"
                "    \"\"\"Возвращает словарь кратчайших расстояний от start.\"\"\"\n"
                "    dist = {node: float('inf') for node in graph}\n"
                "    dist[start] = 0\n"
                "    pq = [(0, start)]  # (расстояние, вершина)\n\n"
                "    while pq:\n"
                "        d, u = heapq.heappop(pq)\n"
                "        if d > dist[u]:\n"
                "            continue  # устаревшая запись\n"
                "        for v, weight in graph[u]:\n"
                "            new_dist = dist[u] + weight\n"
                "            if new_dist < dist[v]:\n"
                "                dist[v] = new_dist\n"
                "                heapq.heappush(pq, (new_dist, v))\n\n"
                "    return dist\n\n"
                "# Граф: смежность с весами\n"
                "graph = {\n"
                "    'A': [('B', 4), ('C', 1)],\n"
                "    'B': [('A', 4), ('D', 1)],\n"
                "    'C': [('A', 1), ('B', 2), ('D', 5)],\n"
                "    'D': [('B', 1), ('C', 5)],\n"
                "}\n\n"
                "distances = dijkstra(graph, 'A')\n"
                "for node, d in sorted(distances.items()):\n"
                "    print('{0}: {1}'.format(node, d))\n"
                "# A: 0, B: 3, C: 1, D: 4"
            ),
            "content": (
                "<h2>Алгоритм Дейкстры</h2>"
                "<p>Алгоритм Дейкстры находит кратчайшие пути от одной "
                "вершины до всех остальных во взвешенном графе с "
                "<strong>неотрицательными</strong> весами рёбер.</p>"

                "<h3>Идея алгоритма</h3>"
                "<ol>"
                "<li>Устанавливаем расстояние до старта = 0, до всех остальных = бесконечность</li>"
                "<li>Выбираем непосещённую вершину с минимальным расстоянием</li>"
                "<li>Обновляем расстояния до её соседей (релаксация)</li>"
                "<li>Повторяем, пока все вершины не посещены</li>"
                "</ol>"

                "<h3>Реализация с heapq</h3>"
                "<p>Приоритетная очередь (<code>heapq</code>) позволяет "
                "эффективно извлекать вершину с минимальным расстоянием.</p>"

                "<h3>Сложность</h3>"
                + info_table(
                    ["Реализация", "Время"],
                    [
                        ["Наивная (массив)", "O(V^2)"],
                        ["С heapq", "O((V + E) log V)"],
                        ["С Fibonacci heap", "O(V log V + E)"],
                    ],
                )

                + "<h3>Ограничения</h3>"
                "<p>Дейкстра <strong>не работает</strong> с отрицательными весами. "
                "Для графов с отрицательными рёбрами используйте алгоритм "
                "Беллмана-Форда.</p>"

                "<h3>Восстановление пути</h3>"
                "<p>Чтобы восстановить сам путь, а не только расстояние, "
                "нужно хранить словарь предшественников: при каждой релаксации "
                "запоминаем, из какой вершины пришли.</p>"
            ),
        },
        {
            "title": "Топологическая сортировка",
            "order": 5,
            "minutes": 12,
            "code": (
                "from collections import deque\n\n"
                "def topological_sort_kahn(graph):\n"
                "    \"\"\"Алгоритм Кана: BFS-подход к топологической сортировке.\"\"\"\n"
                "    # Подсчёт входящих рёбер\n"
                "    in_degree = {node: 0 for node in graph}\n"
                "    for node in graph:\n"
                "        for neighbor in graph[node]:\n"
                "            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1\n\n"
                "    # Начинаем с вершин без входящих рёбер\n"
                "    queue = deque([n for n in in_degree if in_degree[n] == 0])\n"
                "    result = []\n\n"
                "    while queue:\n"
                "        node = queue.popleft()\n"
                "        result.append(node)\n"
                "        for neighbor in graph[node]:\n"
                "            in_degree[neighbor] -= 1\n"
                "            if in_degree[neighbor] == 0:\n"
                "                queue.append(neighbor)\n\n"
                "    if len(result) != len(graph):\n"
                "        raise ValueError('Граф содержит цикл!')\n"
                "    return result\n\n"
                "# DAG: зависимости предметов\n"
                "subjects = {\n"
                "    'Математика': [],\n"
                "    'Программирование': ['Математика'],\n"
                "    'Алгоритмы': ['Программирование', 'Математика'],\n"
                "    'Базы данных': ['Программирование'],\n"
                "    'Веб-разработка': ['Базы данных', 'Алгоритмы'],\n"
                "}\n\n"
                "order = topological_sort_kahn(subjects)\n"
                "print('Порядок изучения:', order)\n"
                "# Математика -> Программирование -> Алгоритмы -> Базы данных -> Веб-разработка"
            ),
            "content": (
                "<h2>Топологическая сортировка</h2>"
                "<p>Топологическая сортировка упорядочивает вершины "
                "ориентированного ациклического графа (DAG) так, что для "
                "каждого ребра (u, v) вершина u идёт перед v.</p>"

                "<h3>Применения</h3>"
                + info_table(
                    ["Область", "Пример"],
                    [
                        ["Сборка проекта", "Порядок компиляции файлов (Make, Gradle)"],
                        ["Учебный план", "Порядок изучения предметов"],
                        ["Менеджер пакетов", "pip, npm: установка зависимостей"],
                        ["Электронные таблицы", "Порядок пересчёта формул"],
                    ],
                )

                + "<h3>Алгоритм Кана (BFS)</h3>"
                "<ol>"
                "<li>Подсчитать входные степени (in-degree) всех вершин</li>"
                "<li>Добавить в очередь все вершины с in-degree = 0</li>"
                "<li>Извлечь вершину, уменьшить in-degree её соседей</li>"
                "<li>Если in-degree соседа стал 0, добавить в очередь</li>"
                "<li>Если обработали не все вершины -- есть цикл</li>"
                "</ol>"

                "<h3>DFS-подход</h3>"
                "<p>Альтернативный подход: запускаем DFS, записываем вершину "
                "в результат после обработки всех её потомков (post-order). "
                "Результат нужно перевернуть.</p>"

                "<h3>Сложность</h3>"
                + info_table(
                    ["Метрика", "Значение"],
                    [
                        ["Время", "O(V + E)"],
                        ["Память", "O(V)"],
                    ],
                )
            ),
        },
    ],

    # ==== M27: Динамическое программирование ====
    27: [
        {
            "title": "Задача о размене монет (Coin Change)",
            "order": 4,
            "minutes": 12,
            "code": (
                "def coin_change(coins, amount):\n"
                "    \"\"\"\n"
                "    Минимальное количество монет для набора суммы amount.\n"
                "    Возвращает -1, если невозможно.\n"
                "    \"\"\"\n"
                "    dp = [float('inf')] * (amount + 1)\n"
                "    dp[0] = 0  # для суммы 0 нужно 0 монет\n\n"
                "    for i in range(1, amount + 1):\n"
                "        for coin in coins:\n"
                "            if coin <= i and dp[i - coin] + 1 < dp[i]:\n"
                "                dp[i] = dp[i - coin] + 1\n\n"
                "    return dp[amount] if dp[amount] != float('inf') else -1\n\n"
                "# Пример: монеты 1, 3, 4 -- набрать 6\n"
                "print(coin_change([1, 3, 4], 6))   # 2 (3+3)\n"
                "print(coin_change([1, 5, 10], 27)) # 5 (10+10+5+1+1)\n"
                "print(coin_change([2], 3))          # -1 (невозможно)\n\n"
                "# Вариант: количество способов набрать сумму\n"
                "def coin_ways(coins, amount):\n"
                "    dp = [0] * (amount + 1)\n"
                "    dp[0] = 1\n"
                "    for coin in coins:\n"
                "        for i in range(coin, amount + 1):\n"
                "            dp[i] += dp[i - coin]\n"
                "    return dp[amount]\n\n"
                "print(coin_ways([1, 2, 5], 5))  # 4 способа"
            ),
            "content": (
                "<h2>Задача о размене монет (Coin Change)</h2>"
                "<p>Классическая задача ДП: дан набор номиналов монет и "
                "целевая сумма. Найти минимальное число монет для набора суммы "
                "(или количество способов).</p>"

                "<h3>Постановка</h3>"
                "<p>Дано: монеты номиналов <code>c1, c2, ..., ck</code> "
                "(неограниченное количество каждой). Найти минимальное "
                "количество монет, дающих сумму <code>S</code>.</p>"

                "<h3>Рекуррентное соотношение</h3>"
                + code_block(
                    "dp[0] = 0\n"
                    "dp[i] = min(dp[i - coin] + 1) для каждого coin <= i"
                )

                + "<h3>Пошаговый пример</h3>"
                "<p>Монеты [1, 3, 4], сумма 6:</p>"
                + info_table(
                    ["i", "dp[i]", "Выбранная монета"],
                    [
                        ["0", "0", "-"],
                        ["1", "1", "1"],
                        ["2", "2", "1"],
                        ["3", "1", "3"],
                        ["4", "1", "4"],
                        ["5", "2", "1+4"],
                        ["6", "2", "3+3"],
                    ],
                )

                + "<h3>Два варианта задачи</h3>"
                + info_table(
                    ["Вариант", "Что ищем", "Инициализация"],
                    [
                        ["Минимум монет", "min количество", "dp = [inf], dp[0]=0"],
                        ["Число способов", "Кол-во комбинаций", "dp = [0], dp[0]=1"],
                    ],
                )

                + "<h3>Сложность</h3>"
                "<p>Время: O(amount * len(coins)), память: O(amount).</p>"

                "<h3>Жадный алгоритм НЕ всегда работает</h3>"
                "<p>Жадный подход (всегда брать наибольшую монету) даёт "
                "неоптимальный ответ для некоторых наборов монет. "
                "Пример: монеты [1, 3, 4], сумма 6. Жадный: 4+1+1=3 монеты. "
                "ДП: 3+3=2 монеты.</p>"
            ),
        },
        {
            "title": "Редакционное расстояние (Edit Distance)",
            "order": 5,
            "minutes": 14,
            "code": (
                "def edit_distance(s1, s2):\n"
                "    \"\"\"\n"
                "    Минимальное число операций (вставка, удаление, замена)\n"
                "    для превращения s1 в s2.\n"
                "    \"\"\"\n"
                "    m, n = len(s1), len(s2)\n"
                "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n\n"
                "    # Базовые случаи\n"
                "    for i in range(m + 1):\n"
                "        dp[i][0] = i\n"
                "    for j in range(n + 1):\n"
                "        dp[0][j] = j\n\n"
                "    for i in range(1, m + 1):\n"
                "        for j in range(1, n + 1):\n"
                "            if s1[i - 1] == s2[j - 1]:\n"
                "                dp[i][j] = dp[i - 1][j - 1]\n"
                "            else:\n"
                "                dp[i][j] = 1 + min(\n"
                "                    dp[i - 1][j],      # удаление\n"
                "                    dp[i][j - 1],      # вставка\n"
                "                    dp[i - 1][j - 1],  # замена\n"
                "                )\n\n"
                "    return dp[m][n]\n\n"
                "print(edit_distance('kitten', 'sitting'))   # 3\n"
                "print(edit_distance('sunday', 'saturday'))  # 3\n"
                "print(edit_distance('', 'abc'))              # 3\n"
                "print(edit_distance('abc', 'abc'))            # 0"
            ),
            "content": (
                "<h2>Редакционное расстояние (расстояние Левенштейна)</h2>"
                "<p>Редакционное расстояние -- минимальное число операций "
                "(вставка, удаление, замена символа) для превращения одной "
                "строки в другую.</p>"

                "<h3>Применения</h3>"
                "<ul>"
                "<li>Проверка орфографии (автокоррекция)</li>"
                "<li>Сравнение ДНК-последовательностей</li>"
                "<li>Система автозаполнения (подсказки)</li>"
                "<li>Утилита <code>diff</code> для сравнения файлов</li>"
                "</ul>"

                "<h3>Рекуррентное соотношение</h3>"
                + code_block(
                    "Если s1[i] == s2[j]:\n"
                    "    dp[i][j] = dp[i-1][j-1]        # символы совпали\n"
                    "Иначе:\n"
                    "    dp[i][j] = 1 + min(\n"
                    "        dp[i-1][j],     # удаление из s1\n"
                    "        dp[i][j-1],     # вставка в s1\n"
                    "        dp[i-1][j-1],   # замена в s1\n"
                    "    )"
                )

                + "<h3>Пример: kitten -> sitting</h3>"
                + info_table(
                    ["Шаг", "Операция", "Результат"],
                    [
                        ["1", "k -> s (замена)", "sitten"],
                        ["2", "e -> i (замена)", "sittin"],
                        ["3", "вставить g", "sitting"],
                    ],
                )

                + "<h3>Сложность</h3>"
                + info_table(
                    ["Метрика", "Значение"],
                    [
                        ["Время", "O(m * n)"],
                        ["Память (полная таблица)", "O(m * n)"],
                        ["Память (оптимизация)", "O(min(m, n)) -- две строки"],
                    ],
                )

                + "<h3>Оптимизация памяти</h3>"
                "<p>Так как каждая строка таблицы зависит только от предыдущей, "
                "можно хранить лишь две строки вместо полной матрицы. "
                "Это снижает память с O(m*n) до O(min(m, n)).</p>"
            ),
        },
    ],

    # ==== M28: JSON CSV datetime ====
    28: [
        {
            "title": "Модуль os: работа с файлами и директориями",
            "order": 4,
            "minutes": 10,
            "code": (
                "import os\n\n"
                "# Текущая директория\n"
                "print(os.getcwd())\n\n"
                "# Список файлов и папок\n"
                "for entry in os.listdir('.'):\n"
                "    entry_type = 'DIR' if os.path.isdir(entry) else 'FILE'\n"
                "    print('{0:5s} {1}'.format(entry_type, entry))\n\n"
                "# Создание директории (с вложенными)\n"
                "os.makedirs('data/reports/2024', exist_ok=True)\n\n"
                "# Переименование файла\n"
                "# os.rename('old_name.txt', 'new_name.txt')\n\n"
                "# Размер файла\n"
                "size = os.path.getsize('example.txt')\n"
                "print('Размер: {0} байт'.format(size))\n\n"
                "# Рекурсивный обход дерева каталогов\n"
                "for root, dirs, files in os.walk('.'):\n"
                "    level = root.replace('.', '').count(os.sep)\n"
                "    indent = '  ' * level\n"
                "    print('{0}{1}/'.format(indent, os.path.basename(root)))\n"
                "    for f in files:\n"
                "        print('{0}  {1}'.format(indent, f))\n\n"
                "# Проверка существования\n"
                "print(os.path.exists('data'))     # True\n"
                "print(os.path.isfile('data'))     # False\n"
                "print(os.path.isdir('data'))      # True\n\n"
                "# Переменные окружения\n"
                "home = os.environ.get('HOME', os.environ.get('USERPROFILE', ''))\n"
                "print('Home:', home)"
            ),
            "content": (
                "<h2>Модуль os: работа с файловой системой</h2>"
                "<p>Модуль <code>os</code> предоставляет кроссплатформенный "
                "интерфейс для работы с операционной системой: файлами, "
                "директориями, переменными окружения.</p>"

                "<h3>Основные функции</h3>"
                + info_table(
                    ["Функция", "Описание"],
                    [
                        ["os.getcwd()", "Текущая рабочая директория"],
                        ["os.listdir(path)", "Список содержимого директории"],
                        ["os.makedirs(path, exist_ok=True)", "Создать вложенные папки"],
                        ["os.remove(path)", "Удалить файл"],
                        ["os.rmdir(path)", "Удалить пустую папку"],
                        ["os.rename(old, new)", "Переименовать файл/папку"],
                        ["os.walk(path)", "Рекурсивный обход дерева"],
                    ],
                )

                + "<h3>os.path -- работа с путями</h3>"
                + info_table(
                    ["Функция", "Описание", "Пример"],
                    [
                        ["os.path.join()", "Соединить части пути", "os.path.join('data', 'file.txt')"],
                        ["os.path.exists()", "Существует ли путь", "True / False"],
                        ["os.path.isfile()", "Это файл?", "True / False"],
                        ["os.path.isdir()", "Это директория?", "True / False"],
                        ["os.path.getsize()", "Размер в байтах", "1024"],
                        ["os.path.splitext()", "Разделить имя и расширение", "('file', '.txt')"],
                        ["os.path.basename()", "Имя файла из пути", "'file.txt'"],
                        ["os.path.dirname()", "Директория из пути", "'/home/user'"],
                    ],
                )

                + "<h3>os.walk() -- рекурсивный обход</h3>"
                "<p><code>os.walk()</code> возвращает генератор троек "
                "<code>(root, dirs, files)</code> для каждой директории в дереве. "
                "Это удобный способ найти все файлы определённого типа.</p>"

                "<h3>Кроссплатформенность</h3>"
                "<p>Используйте <code>os.path.join()</code> вместо конкатенации "
                "строк с <code>/</code> или <code>\\</code>, чтобы код "
                "работал на Windows, Linux и macOS.</p>"
            ),
        },
        {
            "title": "Модуль pathlib: современная работа с путями",
            "order": 5,
            "minutes": 10,
            "code": (
                "from pathlib import Path\n\n"
                "# Текущая директория\n"
                "cwd = Path.cwd()\n"
                "print('CWD:', cwd)\n\n"
                "# Домашняя директория\n"
                "home = Path.home()\n"
                "print('Home:', home)\n\n"
                "# Создание пути (оператор /)\n"
                "data_dir = Path('data') / 'reports' / '2024'\n"
                "data_dir.mkdir(parents=True, exist_ok=True)\n\n"
                "# Чтение и запись файлов\n"
                "file_path = data_dir / 'notes.txt'\n"
                "file_path.write_text('Hello, pathlib!', encoding='utf-8')\n"
                "content = file_path.read_text(encoding='utf-8')\n"
                "print(content)\n\n"
                "# Свойства пути\n"
                "p = Path('/home/user/documents/report.pdf')\n"
                "print('name:', p.name)         # report.pdf\n"
                "print('stem:', p.stem)         # report\n"
                "print('suffix:', p.suffix)     # .pdf\n"
                "print('parent:', p.parent)     # /home/user/documents\n"
                "print('parts:', p.parts)       # ('/', 'home', 'user', ...)\n\n"
                "# Поиск файлов по шаблону\n"
                "py_files = list(Path('.').glob('**/*.py'))\n"
                "print('Python-файлы:', len(py_files))\n\n"
                "# Итерация по директории\n"
                "for item in Path('.').iterdir():\n"
                "    marker = '[D]' if item.is_dir() else '[F]'\n"
                "    print('{0} {1}'.format(marker, item.name))"
            ),
            "content": (
                "<h2>Модуль pathlib: объектно-ориентированные пути</h2>"
                "<p><code>pathlib</code> (Python 3.4+) -- современная замена "
                "<code>os.path</code>. Пути представлены как объекты с "
                "удобными методами и свойствами.</p>"

                "<h3>Преимущества перед os.path</h3>"
                + info_table(
                    ["os.path", "pathlib", "Что делает"],
                    [
                        ["os.path.join('a', 'b')", "Path('a') / 'b'", "Объединение путей"],
                        ["os.path.exists(p)", "p.exists()", "Проверка существования"],
                        ["os.path.isfile(p)", "p.is_file()", "Это файл?"],
                        ["open(p).read()", "p.read_text()", "Чтение текста"],
                        ["os.listdir(p)", "p.iterdir()", "Содержимое папки"],
                        ["glob.glob('*.py')", "p.glob('*.py')", "Поиск по шаблону"],
                    ],
                )

                + "<h3>Полезные свойства Path</h3>"
                + info_table(
                    ["Свойство", "Пример для '/data/report.csv'"],
                    [
                        [".name", "report.csv"],
                        [".stem", "report"],
                        [".suffix", ".csv"],
                        [".parent", "/data"],
                        [".parts", "('/', 'data', 'report.csv')"],
                    ],
                )

                + "<h3>Оператор /</h3>"
                "<p>Главная особенность pathlib -- оператор <code>/</code> "
                "для построения путей. Это читабельнее и безопаснее, чем "
                "конкатенация строк:</p>"
                + code_block(
                    "# Вместо\n"
                    "os.path.join(base, 'subdir', 'file.txt')\n\n"
                    "# Пишем\n"
                    "Path(base) / 'subdir' / 'file.txt'"
                )

                + "<h3>glob и rglob</h3>"
                "<p><code>path.glob('*.txt')</code> ищет в текущей директории, "
                "<code>path.rglob('*.txt')</code> -- рекурсивно во всех "
                "поддиректориях (аналог <code>**/*.txt</code>).</p>"

                "<h3>Рекомендации</h3>"
                "<p>Для нового кода всегда используйте <code>pathlib</code> "
                "вместо <code>os.path</code>. Большинство функций стандартной "
                "библиотеки принимают объекты <code>Path</code> напрямую.</p>"
            ),
        },
    ],

    # ==== M29: ООП наследование и полиморфизм (нужен 1 урок) ====
    29: [
        {
            "title": "Композиция vs наследование",
            "order": 5,
            "minutes": 12,
            "code": (
                "# Наследование: \"является\" (is-a)\n"
                "class Animal:\n"
                "    def __init__(self, name):\n"
                "        self.name = name\n"
                "    def speak(self):\n"
                "        raise NotImplementedError\n\n"
                "class Dog(Animal):  # Собака ЯВЛЯЕТСЯ животным\n"
                "    def speak(self):\n"
                "        return 'Гав!'\n\n"
                "# Композиция: \"имеет\" (has-a)\n"
                "class Engine:\n"
                "    def __init__(self, horsepower):\n"
                "        self.horsepower = horsepower\n"
                "    def start(self):\n"
                "        return 'Двигатель {0} л.с. запущен'.format(self.horsepower)\n\n"
                "class GPS:\n"
                "    def navigate(self, destination):\n"
                "        return 'Маршрут до: {0}'.format(destination)\n\n"
                "class Car:  # Машина ИМЕЕТ двигатель и GPS\n"
                "    def __init__(self, model, hp):\n"
                "        self.model = model\n"
                "        self.engine = Engine(hp)       # композиция\n"
                "        self.gps = GPS()               # композиция\n\n"
                "    def drive(self, destination):\n"
                "        return '{0}: {1}. {2}'.format(\n"
                "            self.model,\n"
                "            self.engine.start(),\n"
                "            self.gps.navigate(destination)\n"
                "        )\n\n"
                "car = Car('Toyota', 150)\n"
                "print(car.drive('Москва'))\n"
                "# Toyota: Двигатель 150 л.с. запущен. Маршрут до: Москва\n\n"
                "# Гибкость композиции: легко заменить компонент\n"
                "class ElectricEngine:\n"
                "    def __init__(self, kw):\n"
                "        self.kw = kw\n"
                "    def start(self):\n"
                "        return 'Электродвигатель {0} кВт запущен'.format(self.kw)\n\n"
                "car.engine = ElectricEngine(200)  # замена без изменения Car\n"
                "print(car.drive('Питер'))"
            ),
            "content": (
                "<h2>Композиция vs наследование</h2>"
                "<p>Два основных способа построения отношений между классами. "
                "Понимание разницы -- ключ к хорошей архитектуре.</p>"

                "<h3>Наследование (is-a)</h3>"
                "<p>Класс-потомок <strong>является</strong> разновидностью "
                "родителя. Используйте, когда объект действительно является "
                "специализацией базового типа.</p>"
                + code_block(
                    "class Shape:       # Фигура\n"
                    "    ...\n"
                    "class Circle(Shape):  # Круг ЯВЛЯЕТСЯ фигурой\n"
                    "    ..."
                )

                + "<h3>Композиция (has-a)</h3>"
                "<p>Класс <strong>содержит</strong> экземпляры других классов "
                "как свои атрибуты. Используйте, когда объект состоит из "
                "компонентов.</p>"
                + code_block(
                    "class Car:         # Машина\n"
                    "    def __init__(self):\n"
                    "        self.engine = Engine()  # ИМЕЕТ двигатель\n"
                    "        self.gps = GPS()        # ИМЕЕТ GPS"
                )

                + "<h3>Сравнение</h3>"
                + info_table(
                    ["Критерий", "Наследование", "Композиция"],
                    [
                        ["Связь", "is-a (является)", "has-a (имеет)"],
                        ["Связанность", "Сильная", "Слабая"],
                        ["Гибкость", "Менее гибко", "Легко менять компоненты"],
                        ["Повторное использование", "Через иерархию", "Через компоненты"],
                        ["Тестируемость", "Сложнее мокать", "Легко подменять части"],
                    ],
                )

                + "<h3>Принцип: предпочитайте композицию</h3>"
                "<p>Знаменитое правило из книги GoF (Gang of Four): "
                "\"Предпочитайте композицию наследованию\" (Favor composition "
                "over inheritance). Наследование оправдано, когда:</p>"
                "<ul>"
                "<li>Объект действительно является подтипом (LSP)</li>"
                "<li>Нужен полиморфизм через общий интерфейс</li>"
                "<li>Иерархия неглубокая (1-2 уровня)</li>"
                "</ul>"
                "<p>Во всех остальных случаях композиция даёт более "
                "гибкий и сопровождаемый код.</p>"

                "<h3>Антипаттерн: глубокое наследование</h3>"
                "<p>Цепочки наследования глубже 2-3 уровней трудно понимать, "
                "отлаживать и модифицировать. Если вы ловите себя на создании "
                "длинной иерархии -- стоит переключиться на композицию.</p>"
            ),
        },
    ],

    # ==== M30: Числовые алгоритмы ====
    30: [
        {
            "title": "Модулярная арифметика",
            "order": 4,
            "minutes": 12,
            "code": (
                "# Основные свойства модулярной арифметики\n"
                "a, b, m = 17, 23, 7\n\n"
                "# (a + b) % m == ((a % m) + (b % m)) % m\n"
                "print((a + b) % m)                      # 5\n"
                "print(((a % m) + (b % m)) % m)          # 5\n\n"
                "# (a * b) % m == ((a % m) * (b % m)) % m\n"
                "print((a * b) % m)                      # 6\n"
                "print(((a % m) * (b % m)) % m)          # 6\n\n"
                "# Быстрое возведение в степень по модулю\n"
                "# встроенная функция pow(base, exp, mod)\n"
                "print(pow(2, 100, 1000000007))  # 976371285\n\n"
                "# Реализация вручную: бинарное возведение в степень\n"
                "def power_mod(base, exp, mod):\n"
                "    result = 1\n"
                "    base = base % mod\n"
                "    while exp > 0:\n"
                "        if exp % 2 == 1:      # нечётная степень\n"
                "            result = (result * base) % mod\n"
                "        exp = exp >> 1         # делим на 2\n"
                "        base = (base * base) % mod\n"
                "    return result\n\n"
                "print(power_mod(2, 100, 1000000007))  # 976371285\n\n"
                "# Применение: проверка больших чисел\n"
                "# Последние 3 цифры числа 7^256\n"
                "print(pow(7, 256, 1000))  # 801"
            ),
            "content": (
                "<h2>Модулярная арифметика</h2>"
                "<p>Модулярная (модульная) арифметика -- арифметика остатков "
                "от деления. Широко используется в криптографии, "
                "хешировании и олимпиадном программировании.</p>"

                "<h3>Основные свойства</h3>"
                + info_table(
                    ["Свойство", "Формула"],
                    [
                        ["Сложение", "(a + b) % m = ((a%m) + (b%m)) % m"],
                        ["Вычитание", "(a - b) % m = ((a%m) - (b%m) + m) % m"],
                        ["Умножение", "(a * b) % m = ((a%m) * (b%m)) % m"],
                        ["Степень", "a^n % m = pow(a, n, m)"],
                    ],
                )

                + "<h3>Бинарное возведение в степень</h3>"
                "<p>Вычисление <code>a^n mod m</code> за O(log n) "
                "вместо O(n). Идея: разбиваем степень на степени двойки.</p>"
                + code_block(
                    "# a^13 = a^8 * a^4 * a^1  (13 = 1101 в двоичной)\n"
                    "# Вместо 13 умножений -- всего 4 (возведение в квадрат + *)"
                )

                + "<h3>Встроенный pow()</h3>"
                "<p>В Python <code>pow(base, exp, mod)</code> -- встроенная "
                "функция, реализующая бинарное возведение в степень. "
                "Работает с произвольно большими числами.</p>"

                "<h3>Применения</h3>"
                + info_table(
                    ["Область", "Как используется"],
                    [
                        ["Криптография (RSA)", "Шифрование: c = m^e mod n"],
                        ["Хеш-функции", "hash = (a*x + b) mod p"],
                        ["Олимпиады", "Ответ по модулю 10^9+7"],
                        ["Контрольные суммы", "CRC, ISBN, ИНН"],
                    ],
                )

                + "<h3>Число 10^9 + 7</h3>"
                "<p>Это простое число, часто используемое в олимпиадных "
                "задачах как модуль. Оно достаточно велико, чтобы ответ был "
                "информативен, и помещается в 32-битное целое.</p>"
            ),
        },
        {
            "title": "Матричные операции",
            "order": 5,
            "minutes": 14,
            "code": (
                "# Матрица как список списков\n"
                "A = [\n"
                "    [1, 2, 3],\n"
                "    [4, 5, 6],\n"
                "]\n"
                "B = [\n"
                "    [7, 8],\n"
                "    [9, 10],\n"
                "    [11, 12],\n"
                "]\n\n"
                "def matrix_multiply(A, B):\n"
                "    \"\"\"Умножение матриц A (m x n) и B (n x p) -> (m x p).\"\"\"\n"
                "    m = len(A)\n"
                "    n = len(B)\n"
                "    p = len(B[0])\n"
                "    result = [[0] * p for _ in range(m)]\n"
                "    for i in range(m):\n"
                "        for j in range(p):\n"
                "            s = 0\n"
                "            for k in range(n):\n"
                "                s += A[i][k] * B[k][j]\n"
                "            result[i][j] = s\n"
                "    return result\n\n"
                "C = matrix_multiply(A, B)\n"
                "for row in C:\n"
                "    print(row)\n"
                "# [58, 64]\n"
                "# [139, 154]\n\n"
                "def transpose(M):\n"
                "    \"\"\"Транспонирование матрицы.\"\"\"\n"
                "    rows = len(M)\n"
                "    cols = len(M[0])\n"
                "    return [[M[i][j] for i in range(rows)] for j in range(cols)]\n\n"
                "print(transpose(A))\n"
                "# [[1, 4], [2, 5], [3, 6]]\n\n"
                "def determinant_2x2(M):\n"
                "    return M[0][0] * M[1][1] - M[0][1] * M[1][0]\n\n"
                "M2 = [[3, 8], [4, 6]]\n"
                "print('det:', determinant_2x2(M2))  # -14"
            ),
            "content": (
                "<h2>Матричные операции в Python</h2>"
                "<p>Матрица -- двумерная таблица чисел. Матричные операции "
                "лежат в основе компьютерной графики, машинного обучения "
                "и научных вычислений.</p>"

                "<h3>Представление матрицы</h3>"
                "<p>В Python матрицу удобно хранить как список списков:</p>"
                + code_block(
                    "matrix = [\n"
                    "    [1, 2, 3],   # строка 0\n"
                    "    [4, 5, 6],   # строка 1\n"
                    "]"
                )

                + "<h3>Основные операции</h3>"
                + info_table(
                    ["Операция", "Сложность", "Описание"],
                    [
                        ["Сложение", "O(m*n)", "Поэлементное сложение"],
                        ["Умножение на скаляр", "O(m*n)", "Каждый элемент * число"],
                        ["Умножение матриц", "O(m*n*p)", "A(m x n) * B(n x p)"],
                        ["Транспонирование", "O(m*n)", "Строки становятся столбцами"],
                        ["Определитель (2x2)", "O(1)", "ad - bc"],
                    ],
                )

                + "<h3>Умножение матриц</h3>"
                "<p>Элемент C[i][j] = сумма A[i][k] * B[k][j] для всех k. "
                "Количество столбцов A должно равняться количеству строк B.</p>"

                "<h3>Единичная матрица</h3>"
                + code_block(
                    "def identity(n):\n"
                    "    return [[1 if i == j else 0 for j in range(n)]\n"
                    "            for i in range(n)]"
                )

                + "<h3>Матричное быстрое возведение в степень</h3>"
                "<p>Матрицу можно возводить в степень по аналогии с числами: "
                "бинарное возведение в степень через повторное возведение в "
                "квадрат. Это позволяет вычислить n-е число Фибоначчи за "
                "O(log n) через матрицу 2x2.</p>"

                "<h3>Библиотека NumPy</h3>"
                "<p>Для реальных вычислений с матрицами используют NumPy, "
                "который работает в сотни раз быстрее благодаря оптимизированным "
                "C-расширениям:</p>"
                + code_block(
                    "import numpy as np\n"
                    "A = np.array([[1, 2], [3, 4]])\n"
                    "B = np.array([[5, 6], [7, 8]])\n"
                    "print(A @ B)        # матричное умножение\n"
                    "print(A.T)          # транспонирование\n"
                    "print(np.linalg.det(A))  # определитель"
                )
            ),
        },
    ],
}


class Command(BaseCommand):
    help = 'Добавляет уроки в модули 21-30 ОАИП (по 2 на модуль, до 5 уроков)'

    def handle(self, *args, **options):
        try:
            oaip = Subject.objects.get(title__contains='ОАИП')
        except Subject.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                '[ERROR] Subject with title containing "ОАИП" not found'
            ))
            return
        except Subject.MultipleObjectsReturned:
            oaip = Subject.objects.filter(title__contains='ОАИП').first()

        modules = {m.order: m for m in oaip.modules.order_by('order')}
        added = 0
        skipped = 0

        for m_order, lessons_data in sorted(LESSONS.items()):
            module = modules.get(m_order)
            if not module:
                self.stdout.write('[SKIP] Module {0} not found'.format(m_order))
                continue

            existing = set(module.lessons.values_list('title', flat=True))

            for ld in lessons_data:
                if ld['title'] in existing:
                    skipped += 1
                    self.stdout.write(
                        '[SKIP] M{0} L{1}: "{2}" already exists'.format(
                            m_order, ld['order'], ld['title'][:45]
                        )
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
                    '[+] M{0} L{1}: {2}'.format(
                        m_order, ld['order'], ld['title'][:45]
                    )
                ))

        self.stdout.write(self.style.SUCCESS(
            '[DONE] Added {0} lessons, skipped {1} duplicates'.format(
                added, skipped
            )
        ))
