from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


def svg_wrap(title, svg_body):
    return (
        '<div style="overflow:auto;margin:1.5rem 0;text-align:center">'
        '<svg viewBox="0 0 620 320" style="max-width:100%;height:auto;'
        'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">'
        f'{svg_body}</svg>'
        f'<p style="color:#64748b;font-size:13px;margin-top:8px">{title}</p>'
        '</div>'
    )


# ── М1 новые уроки ──────────────────────────────────────────────────────────

M1_NEW = [
    {
        'title': 'Как мыслит компьютер: память, процессор, инструкции',
        'order': 5,
        'minutes': 15,
        'code': '''# Пример: компьютер выполняет инструкции последовательно
# Каждая строка — одна инструкция процессору

a = 10          # записать 10 в ячейку памяти "a"
b = 20          # записать 20 в ячейку памяти "b"
c = a + b       # прочитать a и b, сложить, записать результат в "c"
print(c)        # вывести значение "c" на экран
# Результат: 30

# Оперативная память — как таблица с ячейками
# Каждая переменная занимает свою ячейку
x = 5
print(id(x))    # адрес объекта в памяти (число вроде 140234567890)

# Размер объектов в байтах
import sys
print(sys.getsizeof(42))       # ~28 байт (int)
print(sys.getsizeof("hello"))  # ~54 байт (str)
print(sys.getsizeof([1,2,3]))  # ~88 байт (list)''',
        'content': '''
<h2>Как мыслит компьютер</h2>
<p>Чтобы писать программы, важно понимать, как компьютер выполняет ваш код.
Компьютер — это не волшебный ящик, а набор простых компонентов, каждый из
которых выполняет свою задачу.</p>

''' + svg_wrap('Архитектура компьютера: CPU, RAM, диск', '''
<rect width="620" height="320" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
<rect x="40" y="30" width="160" height="100" rx="10" fill="#667eea" stroke="#4c51bf" stroke-width="2"/>
<text x="120" y="70" text-anchor="middle" font-size="15" fill="white" font-weight="bold">CPU</text>
<text x="120" y="90" text-anchor="middle" font-size="11" fill="#e0e7ff">Процессор</text>
<text x="120" y="108" text-anchor="middle" font-size="10" fill="#c7d2fe">Выполняет команды</text>

<rect x="240" y="30" width="160" height="100" rx="10" fill="#16a34a" stroke="#15803d" stroke-width="2"/>
<text x="320" y="70" text-anchor="middle" font-size="15" fill="white" font-weight="bold">RAM</text>
<text x="320" y="90" text-anchor="middle" font-size="11" fill="#dcfce7">Оперативная память</text>
<text x="320" y="108" text-anchor="middle" font-size="10" fill="#bbf7d0">Хранит данные</text>

<rect x="440" y="30" width="140" height="100" rx="10" fill="#ea580c" stroke="#c2410c" stroke-width="2"/>
<text x="510" y="70" text-anchor="middle" font-size="15" fill="white" font-weight="bold">SSD/HDD</text>
<text x="510" y="90" text-anchor="middle" font-size="11" fill="#fed7aa">Постоянная память</text>
<text x="510" y="108" text-anchor="middle" font-size="10" fill="#fdba74">Файлы, программы</text>

<line x1="200" y1="80" x2="240" y2="80" stroke="#334155" stroke-width="2" marker-end="url(#arr)"/>
<line x1="400" y1="80" x2="440" y2="80" stroke="#334155" stroke-width="2" marker-end="url(#arr)"/>

<rect x="40" y="160" width="540" height="140" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
<text x="310" y="185" text-anchor="middle" font-size="13" fill="#334155" font-weight="bold">Как выполняется программа</text>
<text x="60" y="210" font-size="12" fill="#475569">1. Файл .py загружается с диска в RAM</text>
<text x="60" y="232" font-size="12" fill="#475569">2. CPU читает инструкции одну за другой</text>
<text x="60" y="254" font-size="12" fill="#475569">3. Результат вычислений сохраняется в RAM</text>
<text x="60" y="276" font-size="12" fill="#475569">4. print() отправляет данные на экран (вывод)</text>
''') + '''

<h3>Процессор (CPU) — мозг компьютера</h3>
<p>Процессор выполняет команды вашей программы <strong>последовательно</strong> — одну за другой.
Каждая строка кода Python превращается в набор машинных инструкций.</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Компонент</th><th>Аналогия</th><th>Роль</th><th>Скорость</th></tr>
<tr><td><strong>CPU</strong></td><td>Повар на кухне</td><td>Выполняет вычисления</td><td>Миллиарды операций/сек</td></tr>
<tr><td><strong>RAM</strong></td><td>Рабочий стол повара</td><td>Хранит текущие данные</td><td>Наносекунды</td></tr>
<tr><td><strong>SSD/HDD</strong></td><td>Холодильник/кладовка</td><td>Постоянное хранение</td><td>Миллисекунды</td></tr>
<tr><td><strong>Монитор</strong></td><td>Окно выдачи</td><td>Показывает результат</td><td>—</td></tr>
</table>

<h3>Оперативная память (RAM)</h3>
<p>Когда вы пишете <code>x = 42</code>, Python создает объект <code>42</code> в оперативной
памяти и связывает с ним имя <code>x</code>. RAM — это быстрая, но <strong>временная</strong>
память: при выключении компьютера все данные из RAM теряются.</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#8be9fd">x</span> = <span style="color:#bd93f9">42</span><br>
<span style="color:#6272a4"># В памяти: создан объект int(42) по адресу 0x7f...</span><br>
<span style="color:#6272a4"># Имя "x" указывает на этот адрес</span><br><br>
<span style="color:#8be9fd">y</span> = <span style="color:#8be9fd">x</span><br>
<span style="color:#6272a4"># y указывает на тот же объект 42 (не копия!)</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#50fa7b">id</span>(<span style="color:#8be9fd">x</span>) == <span style="color:#50fa7b">id</span>(<span style="color:#8be9fd">y</span>))  <span style="color:#6272a4"># True — один и тот же объект</span>
</div>

<h3>Двоичная система</h3>
<p>Компьютер понимает только два состояния: <strong>0</strong> (нет тока) и <strong>1</strong>
(есть ток). Один бит — это одна единица информации (0 или 1). Восемь бит = один байт.</p>

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Десятичное</th><th>Двоичное</th><th>Байт</th></tr>
<tr><td>0</td><td>0</td><td>00000000</td></tr>
<tr><td>1</td><td>1</td><td>00000001</td></tr>
<tr><td>5</td><td>101</td><td>00000101</td></tr>
<tr><td>42</td><td>101010</td><td>00101010</td></tr>
<tr><td>255</td><td>11111111</td><td>11111111</td></tr>
</table>

<p>Python позволяет работать с двоичными числами:</p>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#50fa7b">print</span>(<span style="color:#50fa7b">bin</span>(<span style="color:#bd93f9">42</span>))    <span style="color:#6272a4"># 0b101010</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#bd93f9">0b101010</span>)  <span style="color:#6272a4"># 42</span>
</div>

<h3>Что происходит при запуске программы</h3>
<ol>
<li><strong>Вы нажимаете Run</strong> — файл .py отправляется интерпретатору Python</li>
<li><strong>Компиляция в байт-код</strong> — Python переводит ваш код в промежуточные инструкции (.pyc)</li>
<li><strong>Виртуальная машина PVM</strong> выполняет байт-код строка за строкой</li>
<li><strong>Результат</strong> появляется в терминале или сохраняется в файл</li>
</ol>

<h3>Запомните</h3>
<ul>
<li>Компьютер выполняет инструкции <strong>последовательно</strong> (сверху вниз)</li>
<li>Все данные программы живут в <strong>оперативной памяти</strong></li>
<li>Переменная — это <strong>имя</strong>, указывающее на объект в памяти</li>
<li>Python — <strong>интерпретируемый</strong> язык: код выполняется построчно</li>
</ul>
'''
    },
    {
        'title': 'Комментарии, стиль кода и PEP 8',
        'order': 6,
        'minutes': 12,
        'code': '''# Однострочный комментарий — начинается с #

# Плохой стиль:
x=2+3 *4
X = "hello"
def MyFunc(A,B):return A+B

# Хороший стиль (PEP 8):
result = 2 + 3 * 4           # пробелы вокруг операторов
name = "hello"                # snake_case для переменных
def my_func(a, b):            # snake_case для функций
    return a + b

# Длинные строки: максимум 79 символов
long_text = (
    "Это очень длинная строка, "
    "которую мы разбиваем на части"
)

# Пустые строки отделяют логические блоки
age = 18

if age >= 18:
    print("Совершеннолетний")

# Документирующая строка (docstring)
def calculate_area(width, height):
    """Вычисляет площадь прямоугольника."""
    return width * height''',
        'content': '''
<h2>Комментарии, стиль кода и PEP 8</h2>
<p>Код пишется один раз, а читается многократно — и вами, и другими. Чистый, понятный
код экономит часы при отладке и поддержке.</p>

<h3>Комментарии</h3>
<p>Комментарий — это текст, который Python <strong>полностью игнорирует</strong>. Он нужен
людям, чтобы пояснить сложные места.</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Однострочный комментарий</span><br>
<span style="color:#8be9fd">price</span> = <span style="color:#bd93f9">100</span>  <span style="color:#6272a4"># комментарий в конце строки</span><br><br>
<span style="color:#6272a4"># Многострочный комментарий:</span><br>
<span style="color:#6272a4"># просто несколько строк подряд</span><br>
<span style="color:#6272a4"># каждая начинается с #</span>
</div>

<p><strong>Когда писать комментарии:</strong></p>
<ul>
<li>Объяснить <em>почему</em> сделано именно так (а не что делает код)</li>
<li>Пояснить неочевидную логику или формулу</li>
<li>TODO-метки для будущих доработок</li>
</ul>

<p><strong>Когда НЕ надо:</strong></p>
<ul>
<li><code># увеличиваем x на 1</code> перед <code>x += 1</code> — и так понятно</li>
<li>Комментарии, которые повторяют код — лишний шум</li>
</ul>

<h3>PEP 8 — стандарт стиля Python</h3>
<p>PEP 8 (Python Enhancement Proposal #8) — это официальное руководство по стилю кода Python.
Его создал сам Гвидо ван Россум. Следование PEP 8 делает код единообразным и понятным.</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#fee2e2"><th>Плохо</th><th style="background:#dcfce7">Хорошо</th><th>Правило</th></tr>
<tr><td><code>x=2+3</code></td><td><code>x = 2 + 3</code></td><td>Пробелы вокруг операторов</td></tr>
<tr><td><code>myVariable</code></td><td><code>my_variable</code></td><td>snake_case для переменных</td></tr>
<tr><td><code>def CalcArea():</code></td><td><code>def calc_area():</code></td><td>snake_case для функций</td></tr>
<tr><td><code>class my_class:</code></td><td><code>class MyClass:</code></td><td>CamelCase для классов</td></tr>
<tr><td><code>MAX_SIZE=100</code></td><td><code>MAX_SIZE = 100</code></td><td>UPPER_SNAKE для констант</td></tr>
<tr><td><code>import os,sys</code></td><td><code>import os<br>import sys</code></td><td>Каждый import на отдельной строке</td></tr>
</table>

<h3>Отступы — 4 пробела</h3>
<p>В Python отступы — это <strong>часть синтаксиса</strong>, а не украшение. Неправильный отступ
вызовет ошибку <code>IndentationError</code>.</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Правильно: 4 пробела</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">age</span> >= <span style="color:#bd93f9">18</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"OK"</span>)<br><br>
<span style="color:#6272a4"># Ошибка: смешаны табы и пробелы</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">age</span> >= <span style="color:#bd93f9">18</span>:<br>
<span style="color:#ff5555">&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"OK"</span>)  # IndentationError!</span>
</div>

<h3>Именование переменных</h3>
<p>Хорошее имя переменной — это мини-документация:</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Плохо</th><th>Хорошо</th><th>Почему</th></tr>
<tr><td><code>x</code></td><td><code>age</code></td><td>Понятно, что хранится</td></tr>
<tr><td><code>lst</code></td><td><code>students</code></td><td>Описывает содержание</td></tr>
<tr><td><code>f</code></td><td><code>is_valid</code></td><td>Булевы: is_, has_, can_</td></tr>
<tr><td><code>data2</code></td><td><code>filtered_data</code></td><td>Числа в именах — плохо</td></tr>
</table>

<h3>Длина строки</h3>
<p>PEP 8 рекомендует не более <strong>79 символов</strong> в строке. Длинные строки
разбивайте:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Способ 1: скобки</span><br>
<span style="color:#8be9fd">total</span> = (<span style="color:#8be9fd">price</span> * <span style="color:#8be9fd">quantity</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ <span style="color:#8be9fd">tax</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <span style="color:#8be9fd">discount</span>)<br><br>
<span style="color:#6272a4"># Способ 2: обратный слеш (менее предпочтителен)</span><br>
<span style="color:#8be9fd">total</span> = <span style="color:#8be9fd">price</span> * <span style="color:#8be9fd">quantity</span> \<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ <span style="color:#8be9fd">tax</span>
</div>

<h3>Запомните</h3>
<ul>
<li><strong>Комментарии</strong> объясняют <em>почему</em>, а не <em>что</em></li>
<li><strong>PEP 8</strong> — официальный стиль Python: 4 пробела, snake_case, 79 символов</li>
<li><strong>Имена переменных</strong> должны говорить сами за себя</li>
<li>Код читается <strong>в 10 раз чаще</strong>, чем пишется — пишите для читателя</li>
</ul>
'''
    },
    {
        'title': 'Арифметические операции и выражения',
        'order': 7,
        'minutes': 12,
        'code': '''# Основные арифметические операции
a, b = 17, 5

print(a + b)    # 22  — сложение
print(a - b)    # 12  — вычитание
print(a * b)    # 85  — умножение
print(a / b)    # 3.4 — деление (всегда float!)
print(a // b)   # 3   — целочисленное деление
print(a % b)    # 2   — остаток от деления
print(a ** b)   # 1419857 — возведение в степень

# Приоритет операций (как в математике)
result = 2 + 3 * 4      # 14, не 20!
result = (2 + 3) * 4    # 20 — скобки меняют порядок

# Комбинированное присваивание
x = 10
x += 5   # x = x + 5  → 15
x -= 3   # x = x - 3  → 12
x *= 2   # x = x * 2  → 24
x //= 5  # x = x // 5 → 4
x **= 3  # x = x ** 3 → 64

# Полезные встроенные функции
print(abs(-7))       # 7 — модуль
print(round(3.7))    # 4 — округление
print(round(3.14159, 2))  # 3.14
print(max(1, 5, 3))  # 5
print(min(1, 5, 3))  # 1

# Модуль math
import math
print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.14159...
print(math.ceil(3.2))  # 4 (вверх)
print(math.floor(3.8)) # 3 (вниз)''',
        'content': '''
<h2>Арифметические операции и выражения</h2>
<p>Python — мощный калькулятор. Он поддерживает все стандартные математические операции
и множество дополнительных возможностей.</p>

<h3>Основные операции</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Оператор</th><th>Название</th><th>Пример</th><th>Результат</th></tr>
<tr><td><code>+</code></td><td>Сложение</td><td><code>7 + 3</code></td><td>10</td></tr>
<tr><td><code>-</code></td><td>Вычитание</td><td><code>7 - 3</code></td><td>4</td></tr>
<tr><td><code>*</code></td><td>Умножение</td><td><code>7 * 3</code></td><td>21</td></tr>
<tr><td><code>/</code></td><td>Деление</td><td><code>7 / 3</code></td><td>2.333...</td></tr>
<tr><td><code>//</code></td><td>Целочисленное деление</td><td><code>7 // 3</code></td><td>2</td></tr>
<tr><td><code>%</code></td><td>Остаток от деления</td><td><code>7 % 3</code></td><td>1</td></tr>
<tr><td><code>**</code></td><td>Возведение в степень</td><td><code>2 ** 10</code></td><td>1024</td></tr>
</table>

<h3>Важные нюансы деления</h3>
<p>В Python 3 обычное деление <code>/</code> <strong>всегда</strong> возвращает <code>float</code>,
даже если делится нацело:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#50fa7b">print</span>(<span style="color:#bd93f9">10</span> / <span style="color:#bd93f9">2</span>)   <span style="color:#6272a4"># 5.0 (float, не int!)</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#bd93f9">10</span> // <span style="color:#bd93f9">2</span>)  <span style="color:#6272a4"># 5   (int)</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#bd93f9">10</span> // <span style="color:#bd93f9">3</span>)  <span style="color:#6272a4"># 3   (округление вниз)</span><br>
<span style="color:#50fa7b">print</span>(-<span style="color:#bd93f9">7</span> // <span style="color:#bd93f9">2</span>)  <span style="color:#6272a4"># -4  (не -3! округление к минус бесконечности)</span>
</div>

<h3>Остаток от деления (%)</h3>
<p>Оператор <code>%</code> очень полезен в программировании:</p>
<ul>
<li><strong>Проверка четности:</strong> <code>n % 2 == 0</code> — число четное</li>
<li><strong>Последняя цифра:</strong> <code>n % 10</code> — последняя цифра числа</li>
<li><strong>Циклические значения:</strong> <code>hour % 24</code> — часы (0-23)</li>
</ul>

<h3>Приоритет операций</h3>
<p>Python следует стандартным математическим правилам:</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Приоритет</th><th>Оператор</th><th>Пример</th></tr>
<tr><td>1 (высший)</td><td><code>()</code> скобки</td><td><code>(2 + 3) * 4 = 20</code></td></tr>
<tr><td>2</td><td><code>**</code> степень</td><td><code>2 ** 3 ** 2 = 512</code></td></tr>
<tr><td>3</td><td><code>+x, -x</code> унарные</td><td><code>-5 + 3 = -2</code></td></tr>
<tr><td>4</td><td><code>*, /, //, %</code></td><td><code>2 + 3 * 4 = 14</code></td></tr>
<tr><td>5 (низший)</td><td><code>+, -</code></td><td><code>10 - 3 + 2 = 9</code></td></tr>
</table>

<p><strong>Совет:</strong> если сомневаетесь в порядке — ставьте скобки. Они улучшают читаемость.</p>

<h3>Комбинированное присваивание</h3>
<p>Вместо <code>x = x + 5</code> можно писать короче:</p>

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Сокращение</th><th>Эквивалент</th></tr>
<tr><td><code>x += 5</code></td><td><code>x = x + 5</code></td></tr>
<tr><td><code>x -= 3</code></td><td><code>x = x - 3</code></td></tr>
<tr><td><code>x *= 2</code></td><td><code>x = x * 2</code></td></tr>
<tr><td><code>x /= 4</code></td><td><code>x = x / 4</code></td></tr>
<tr><td><code>x //= 3</code></td><td><code>x = x // 3</code></td></tr>
<tr><td><code>x %= 7</code></td><td><code>x = x % 7</code></td></tr>
<tr><td><code>x **= 2</code></td><td><code>x = x ** 2</code></td></tr>
</table>

<h3>Встроенные математические функции</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Функция</th><th>Описание</th><th>Пример</th></tr>
<tr><td><code>abs(x)</code></td><td>Модуль числа</td><td><code>abs(-7) = 7</code></td></tr>
<tr><td><code>round(x, n)</code></td><td>Округление до n знаков</td><td><code>round(3.14159, 2) = 3.14</code></td></tr>
<tr><td><code>max(a, b, ...)</code></td><td>Максимум</td><td><code>max(1, 5, 3) = 5</code></td></tr>
<tr><td><code>min(a, b, ...)</code></td><td>Минимум</td><td><code>min(1, 5, 3) = 1</code></td></tr>
<tr><td><code>pow(x, y)</code></td><td>Степень (аналог **)</td><td><code>pow(2, 10) = 1024</code></td></tr>
<tr><td><code>divmod(a, b)</code></td><td>Частное и остаток</td><td><code>divmod(17, 5) = (3, 2)</code></td></tr>
</table>

<h3>Модуль math</h3>
<p>Для продвинутых вычислений подключите модуль <code>math</code>:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#ff79c6">import</span> <span style="color:#8be9fd">math</span><br><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">math</span>.<span style="color:#50fa7b">sqrt</span>(<span style="color:#bd93f9">16</span>))     <span style="color:#6272a4"># 4.0 — квадратный корень</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">math</span>.<span style="color:#8be9fd">pi</span>)           <span style="color:#6272a4"># 3.141592653589793</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">math</span>.<span style="color:#50fa7b">ceil</span>(<span style="color:#bd93f9">3.2</span>))   <span style="color:#6272a4"># 4 — округление вверх</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">math</span>.<span style="color:#50fa7b">floor</span>(<span style="color:#bd93f9">3.8</span>))  <span style="color:#6272a4"># 3 — округление вниз</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">math</span>.<span style="color:#50fa7b">factorial</span>(<span style="color:#bd93f9">5</span>)) <span style="color:#6272a4"># 120 — факториал (5!)</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">math</span>.<span style="color:#50fa7b">log2</span>(<span style="color:#bd93f9">1024</span>))  <span style="color:#6272a4"># 10.0 — логарифм по основанию 2</span>
</div>

<h3>Запомните</h3>
<ul>
<li><code>/</code> всегда возвращает float, <code>//</code> — целое</li>
<li><code>%</code> даёт остаток: незаменим для проверки делимости</li>
<li><code>**</code> — степень, а не побитовое XOR (как в C)</li>
<li>Приоритет: скобки > степень > умножение/деление > сложение/вычитание</li>
</ul>
'''
    },
]

# ── М3 новые уроки ──────────────────────────────────────────────────────────

M3_NEW = [
    {
        'title': 'Тернарный оператор и match-case',
        'order': 4,
        'minutes': 12,
        'code': '''# Тернарный (условный) оператор — одна строка вместо 4
age = 20

# Обычный if-else:
if age >= 18:
    status = "взрослый"
else:
    status = "ребёнок"

# Тернарный оператор:
status = "взрослый" if age >= 18 else "ребёнок"
print(status)  # взрослый

# Можно использовать в print, f-строках, списках
print("чётное" if 10 % 2 == 0 else "нечётное")

# Вложенный тернарный (не злоупотребляйте!)
score = 85
grade = "отлично" if score >= 90 else "хорошо" if score >= 70 else "удовл."

# match-case (Python 3.10+) — аналог switch
command = "start"

match command:
    case "start":
        print("Запуск программы")
    case "stop":
        print("Остановка")
    case "pause":
        print("Пауза")
    case _:
        print("Неизвестная команда")

# match с числами
http_code = 404

match http_code:
    case 200:
        print("OK")
    case 404:
        print("Не найдено")
    case 500:
        print("Ошибка сервера")
    case _:
        print(f"Код: {http_code}")''',
        'content': '''
<h2>Тернарный оператор и match-case</h2>
<p>Python предлагает короткие формы записи условий для простых случаев.</p>

<h3>Тернарный (условный) оператор</h3>
<p>Когда нужно присвоить одно из двух значений по условию, можно записать в одну строку:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Синтаксис:</span><br>
<span style="color:#8be9fd">значение_если_True</span> <span style="color:#ff79c6">if</span> <span style="color:#8be9fd">условие</span> <span style="color:#ff79c6">else</span> <span style="color:#8be9fd">значение_если_False</span><br><br>
<span style="color:#6272a4"># Примеры:</span><br>
<span style="color:#8be9fd">status</span> = <span style="color:#f1fa8c">"четное"</span> <span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> % <span style="color:#bd93f9">2</span> == <span style="color:#bd93f9">0</span> <span style="color:#ff79c6">else</span> <span style="color:#f1fa8c">"нечетное"</span><br>
<span style="color:#8be9fd">sign</span> = <span style="color:#f1fa8c">"+"</span> <span style="color:#ff79c6">if</span> <span style="color:#8be9fd">x</span> > <span style="color:#bd93f9">0</span> <span style="color:#ff79c6">else</span> <span style="color:#f1fa8c">"-"</span> <span style="color:#ff79c6">if</span> <span style="color:#8be9fd">x</span> &lt; <span style="color:#bd93f9">0</span> <span style="color:#ff79c6">else</span> <span style="color:#f1fa8c">"0"</span>
</div>

''' + svg_wrap('Тернарный оператор: одна строка вместо блока if-else', '''
<rect width="620" height="320" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
<text x="310" y="35" text-anchor="middle" font-size="14" fill="#334155" font-weight="bold">result = A if condition else B</text>
<circle cx="310" cy="110" r="45" fill="#ea580c"/>
<text x="310" y="115" text-anchor="middle" font-size="13" fill="white" font-weight="bold">condition</text>
<line x1="265" y1="110" x2="120" y2="210" stroke="#16a34a" stroke-width="2"/>
<text x="170" y="165" font-size="13" fill="#16a34a" font-weight="bold">True</text>
<line x1="355" y1="110" x2="500" y2="210" stroke="#dc2626" stroke-width="2"/>
<text x="450" y="165" font-size="13" fill="#dc2626" font-weight="bold">False</text>
<rect x="40" y="210" width="160" height="60" rx="8" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
<text x="120" y="245" text-anchor="middle" font-size="14" fill="#15803d" font-weight="bold">A</text>
<rect x="420" y="210" width="160" height="60" rx="8" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
<text x="500" y="245" text-anchor="middle" font-size="14" fill="#991b1b" font-weight="bold">B</text>
<text x="310" y="300" text-anchor="middle" font-size="12" fill="#64748b">result = A или B</text>
''') + '''

<p><strong>Когда использовать тернарный оператор:</strong></p>
<ul>
<li>Простое присваивание по условию</li>
<li>Короткие выражения без побочных эффектов</li>
<li>Внутри f-строк: <code>f"Результат: {'да' if ok else 'нет'}"</code></li>
</ul>
<p><strong>Когда НЕ использовать:</strong></p>
<ul>
<li>Сложные условия с несколькими действиями</li>
<li>Вложенные тернарные операторы (трудно читать)</li>
</ul>

<h3>match-case (Python 3.10+)</h3>
<p>Конструкция <code>match-case</code> — структурное сопоставление с образцом.
Это мощная альтернатива цепочкам <code>if-elif</code>:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#ff79c6">match</span> <span style="color:#8be9fd">command</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> <span style="color:#f1fa8c">"start"</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Запуск"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> <span style="color:#f1fa8c">"stop"</span> | <span style="color:#f1fa8c">"exit"</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Выход"</span>)  <span style="color:#6272a4"># | = ИЛИ</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> <span style="color:#8be9fd">_</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Неизвестно"</span>)  <span style="color:#6272a4"># _ = все остальное</span>
</div>

<h3>match с кортежами и условиями</h3>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#8be9fd">point</span> = (<span style="color:#bd93f9">0</span>, <span style="color:#bd93f9">5</span>)<br><br>
<span style="color:#ff79c6">match</span> <span style="color:#8be9fd">point</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> (<span style="color:#bd93f9">0</span>, <span style="color:#bd93f9">0</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Начало координат"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> (<span style="color:#bd93f9">0</span>, <span style="color:#8be9fd">y</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"На оси Y: y={y}"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> (<span style="color:#8be9fd">x</span>, <span style="color:#bd93f9">0</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"На оси X: x={x}"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> (<span style="color:#8be9fd">x</span>, <span style="color:#8be9fd">y</span>) <span style="color:#ff79c6">if</span> <span style="color:#8be9fd">x</span> == <span style="color:#8be9fd">y</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"На диагонали: {x}"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">case</span> (<span style="color:#8be9fd">x</span>, <span style="color:#8be9fd">y</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"Точка ({x}, {y})"</span>)
</div>

<h3>Сравнение if-elif и match-case</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>if-elif</th><th>match-case</th></tr>
<tr><td>Работает в любой версии Python</td><td>Python 3.10+</td></tr>
<tr><td>Проверяет произвольные условия</td><td>Сопоставляет с образцом</td></tr>
<tr><td>Может быть громоздким</td><td>Элегантно для множества вариантов</td></tr>
<tr><td>Стандартный выбор</td><td>Идеален для разбора команд, форматов</td></tr>
</table>

<h3>Запомните</h3>
<ul>
<li>Тернарный: <code>A if condition else B</code> — для простых случаев</li>
<li><code>match-case</code> — мощная замена switch/case из других языков</li>
<li><code>case _:</code> — ветка "по умолчанию" (аналог else)</li>
<li><code>|</code> в case — объединение нескольких значений</li>
</ul>
'''
    },
    {
        'title': 'Логические выражения: истина, ложь, приоритеты',
        'order': 5,
        'minutes': 12,
        'code': '''# Значения True и False
print(type(True))   # <class 'bool'>
print(type(False))  # <class 'bool'>

# Операторы сравнения
print(5 > 3)    # True
print(5 < 3)    # False
print(5 >= 5)   # True
print(5 == 5)   # True  (== сравнение, = присваивание!)
print(5 != 3)   # True

# Логические операторы
print(True and False)  # False
print(True or False)   # True
print(not True)        # False

# Цепочки сравнений (уникальная фишка Python!)
x = 5
print(1 < x < 10)      # True  (в других языках так нельзя)
print(0 <= x <= 100)    # True

# Truthiness — что считается "ложным"
# False: 0, 0.0, "", [], {}, (), None, False
# True: все остальное

print(bool(0))       # False
print(bool(""))      # False
print(bool([]))      # False
print(bool(None))    # False
print(bool(42))      # True
print(bool("hello")) # True
print(bool([1, 2]))  # True

# Короткое замыкание (short-circuit evaluation)
# and: если первое False — второе не проверяется
# or:  если первое True — второе не проверяется
name = ""
greeting = name or "Аноним"  # "Аноним" (потому что "" — False)
print(greeting)

# Приоритет: not > and > or
print(True or False and False)   # True  (and раньше or)
print((True or False) and False) # False (скобки меняют порядок)''',
        'content': '''
<h2>Логические выражения</h2>
<p>Логические выражения — основа любых условий и циклов. Каждое логическое
выражение вычисляется в <code>True</code> или <code>False</code>.</p>

<h3>Операторы сравнения</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Оператор</th><th>Значение</th><th>Пример</th><th>Результат</th></tr>
<tr><td><code>==</code></td><td>Равно</td><td><code>5 == 5</code></td><td>True</td></tr>
<tr><td><code>!=</code></td><td>Не равно</td><td><code>5 != 3</code></td><td>True</td></tr>
<tr><td><code>&gt;</code></td><td>Больше</td><td><code>5 &gt; 3</code></td><td>True</td></tr>
<tr><td><code>&lt;</code></td><td>Меньше</td><td><code>3 &lt; 5</code></td><td>True</td></tr>
<tr><td><code>&gt;=</code></td><td>Больше или равно</td><td><code>5 &gt;= 5</code></td><td>True</td></tr>
<tr><td><code>&lt;=</code></td><td>Меньше или равно</td><td><code>3 &lt;= 5</code></td><td>True</td></tr>
</table>

<p><strong>Частая ошибка:</strong> путать <code>=</code> (присваивание) и <code>==</code> (сравнение)!</p>

<h3>Логические операторы: and, or, not</h3>

''' + svg_wrap('Таблица истинности: and, or, not', '''
<rect width="620" height="320" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
<text x="130" y="30" text-anchor="middle" font-size="14" fill="#334155" font-weight="bold">AND</text>
<text x="310" y="30" text-anchor="middle" font-size="14" fill="#334155" font-weight="bold">OR</text>
<text x="510" y="30" text-anchor="middle" font-size="14" fill="#334155" font-weight="bold">NOT</text>

<rect x="30" y="40" width="200" height="30" rx="4" fill="#e2e8f0"/>
<text x="60" y="60" font-size="11" fill="#334155" font-weight="bold">A</text>
<text x="100" y="60" font-size="11" fill="#334155" font-weight="bold">B</text>
<text x="160" y="60" font-size="11" fill="#334155" font-weight="bold">A and B</text>

<text x="60" y="90" font-size="11" fill="#334155">T</text><text x="100" y="90" font-size="11" fill="#334155">T</text><text x="160" y="90" font-size="11" fill="#16a34a" font-weight="bold">True</text>
<text x="60" y="115" font-size="11" fill="#334155">T</text><text x="100" y="115" font-size="11" fill="#334155">F</text><text x="160" y="115" font-size="11" fill="#dc2626" font-weight="bold">False</text>
<text x="60" y="140" font-size="11" fill="#334155">F</text><text x="100" y="140" font-size="11" fill="#334155">T</text><text x="160" y="140" font-size="11" fill="#dc2626" font-weight="bold">False</text>
<text x="60" y="165" font-size="11" fill="#334155">F</text><text x="100" y="165" font-size="11" fill="#334155">F</text><text x="160" y="165" font-size="11" fill="#dc2626" font-weight="bold">False</text>

<rect x="210" y="40" width="200" height="30" rx="4" fill="#e2e8f0"/>
<text x="240" y="60" font-size="11" fill="#334155" font-weight="bold">A</text>
<text x="280" y="60" font-size="11" fill="#334155" font-weight="bold">B</text>
<text x="340" y="60" font-size="11" fill="#334155" font-weight="bold">A or B</text>

<text x="240" y="90" font-size="11" fill="#334155">T</text><text x="280" y="90" font-size="11" fill="#334155">T</text><text x="340" y="90" font-size="11" fill="#16a34a" font-weight="bold">True</text>
<text x="240" y="115" font-size="11" fill="#334155">T</text><text x="280" y="115" font-size="11" fill="#334155">F</text><text x="340" y="115" font-size="11" fill="#16a34a" font-weight="bold">True</text>
<text x="240" y="140" font-size="11" fill="#334155">F</text><text x="280" y="140" font-size="11" fill="#334155">T</text><text x="340" y="140" font-size="11" fill="#16a34a" font-weight="bold">True</text>
<text x="240" y="165" font-size="11" fill="#334155">F</text><text x="280" y="165" font-size="11" fill="#334155">F</text><text x="340" y="165" font-size="11" fill="#dc2626" font-weight="bold">False</text>

<rect x="420" y="40" width="170" height="30" rx="4" fill="#e2e8f0"/>
<text x="460" y="60" font-size="11" fill="#334155" font-weight="bold">A</text>
<text x="540" y="60" font-size="11" fill="#334155" font-weight="bold">not A</text>
<text x="460" y="90" font-size="11" fill="#334155">True</text><text x="540" y="90" font-size="11" fill="#dc2626" font-weight="bold">False</text>
<text x="460" y="115" font-size="11" fill="#334155">False</text><text x="540" y="115" font-size="11" fill="#16a34a" font-weight="bold">True</text>

<text x="310" y="210" text-anchor="middle" font-size="13" fill="#334155" font-weight="bold">Приоритет: not > and > or</text>
<text x="310" y="240" text-anchor="middle" font-size="12" fill="#64748b">not True or False and True</text>
<text x="310" y="260" text-anchor="middle" font-size="12" fill="#64748b">= (False) or (False and True)</text>
<text x="310" y="280" text-anchor="middle" font-size="12" fill="#64748b">= False or False = False</text>
''') + '''

<h3>Truthiness: что считается истиной и ложью</h3>
<p>В Python любой объект можно использовать как логическое значение.
Python считает <strong>"пустое" = ложь, "непустое" = истина</strong>:</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#fee2e2"><th>Ложные (Falsy)</th><th style="background:#dcfce7">Истинные (Truthy)</th></tr>
<tr><td><code>False</code></td><td><code>True</code></td></tr>
<tr><td><code>0</code>, <code>0.0</code></td><td>Любое ненулевое число</td></tr>
<tr><td><code>""</code> (пустая строка)</td><td>Непустая строка</td></tr>
<tr><td><code>[]</code>, <code>()</code>, <code>{}</code></td><td>Непустые коллекции</td></tr>
<tr><td><code>None</code></td><td>Все остальные объекты</td></tr>
</table>

<p>Это позволяет писать элегантный код:</p>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Вместо: if len(items) > 0:</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">items</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Список не пуст"</span>)<br><br>
<span style="color:#6272a4"># Вместо: if name != "":</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">name</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"Привет, {name}"</span>)
</div>

<h3>Короткое замыкание</h3>
<p>Python вычисляет логические выражения <strong>лениво</strong>:</p>
<ul>
<li><code>and</code>: если первое значение ложно — второе не проверяется</li>
<li><code>or</code>: если первое значение истинно — второе не проверяется</li>
</ul>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Значение по умолчанию</span><br>
<span style="color:#8be9fd">username</span> = <span style="color:#8be9fd">input_name</span> <span style="color:#ff79c6">or</span> <span style="color:#f1fa8c">"Гость"</span><br><br>
<span style="color:#6272a4"># Безопасный доступ</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">data</span> <span style="color:#ff79c6">and</span> <span style="color:#8be9fd">data</span>[<span style="color:#bd93f9">0</span>] > <span style="color:#bd93f9">0</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Первый элемент положительный"</span>)
</div>

<h3>Цепочки сравнений</h3>
<p>Уникальная фишка Python — можно писать цепочки:</p>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Вместо: if x > 0 and x < 100:</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#bd93f9">0</span> &lt; <span style="color:#8be9fd">x</span> &lt; <span style="color:#bd93f9">100</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"x в диапазоне (0, 100)"</span>)<br><br>
<span style="color:#6272a4"># Можно с разными операторами:</span><br>
<span style="color:#ff79c6">if</span> <span style="color:#bd93f9">1</span> &lt;= <span style="color:#8be9fd">grade</span> &lt;= <span style="color:#bd93f9">5</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">"Оценка корректна"</span>)
</div>

<h3>Запомните</h3>
<ul>
<li><code>==</code> сравнивает, <code>=</code> присваивает — не путайте!</li>
<li>Приоритет: <code>not</code> > <code>and</code> > <code>or</code></li>
<li>Пустое = ложь, непустое = истина (truthiness)</li>
<li>Python поддерживает цепочки: <code>0 &lt; x &lt; 100</code></li>
<li>Короткое замыкание: <code>name or "default"</code></li>
</ul>
'''
    },
]

# ── М4 новые уроки ──────────────────────────────────────────────────────────

M4_NEW = [
    {
        'title': 'break, continue и else в циклах',
        'order': 4,
        'minutes': 12,
        'code': '''# break — досрочный выход из цикла
for i in range(100):
    if i == 5:
        break
    print(i, end=" ")
# Вывод: 0 1 2 3 4

# continue — пропустить текущую итерацию
for i in range(10):
    if i % 2 == 0:
        continue  # пропустить четные
    print(i, end=" ")
# Вывод: 1 3 5 7 9

# Поиск элемента с break
numbers = [4, 7, 2, 9, 1, 8]
target = 9

for num in numbers:
    if num == target:
        print(f"Найдено: {target}")
        break
else:
    # else выполняется если цикл завершился
    # БЕЗ break (т.е. элемент не найден)
    print(f"{target} не найден")

# Пример: проверка простого числа
n = 17
for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
        print(f"{n} составное, делитель: {i}")
        break
else:
    print(f"{n} — простое число")

# while + break: ввод с проверкой
while True:
    s = input("Введите число (или 'q' для выхода): ")
    if s == 'q':
        break
    print(f"Вы ввели: {s}")''',
        'content': '''
<h2>break, continue и else в циклах</h2>
<p>Python предоставляет три инструмента для управления выполнением цикла:
<code>break</code>, <code>continue</code> и уникальный <code>else</code>-блок.</p>

''' + svg_wrap('break и continue: управление потоком цикла', '''
<rect width="620" height="320" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
<text x="155" y="30" text-anchor="middle" font-size="14" fill="#334155" font-weight="bold">break</text>
<text x="465" y="30" text-anchor="middle" font-size="14" fill="#334155" font-weight="bold">continue</text>

<rect x="30" y="45" width="250" height="250" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1"/>
<rect x="55" y="60" width="200" height="35" rx="6" fill="#16a34a" stroke="#15803d" stroke-width="1"/>
<text x="155" y="82" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Итерация 1</text>
<rect x="55" y="105" width="200" height="35" rx="6" fill="#16a34a" stroke="#15803d" stroke-width="1"/>
<text x="155" y="127" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Итерация 2</text>
<rect x="55" y="150" width="200" height="35" rx="6" fill="#dc2626" stroke="#991b1b" stroke-width="1"/>
<text x="155" y="172" text-anchor="middle" font-size="12" fill="white" font-weight="bold">break!</text>
<rect x="55" y="195" width="200" height="35" rx="6" fill="#e5e7eb" stroke="#9ca3af" stroke-width="1" stroke-dasharray="4"/>
<text x="155" y="217" text-anchor="middle" font-size="11" fill="#9ca3af">Пропущено</text>
<text x="155" y="270" text-anchor="middle" font-size="11" fill="#64748b">Цикл завершен досрочно</text>

<rect x="340" y="45" width="250" height="250" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1"/>
<rect x="365" y="60" width="200" height="35" rx="6" fill="#16a34a" stroke="#15803d" stroke-width="1"/>
<text x="465" y="82" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Итерация 1</text>
<rect x="365" y="105" width="200" height="35" rx="6" fill="#f59e0b" stroke="#d97706" stroke-width="1"/>
<text x="465" y="127" text-anchor="middle" font-size="12" fill="white" font-weight="bold">continue</text>
<rect x="365" y="150" width="200" height="35" rx="6" fill="#16a34a" stroke="#15803d" stroke-width="1"/>
<text x="465" y="172" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Итерация 3</text>
<rect x="365" y="195" width="200" height="35" rx="6" fill="#16a34a" stroke="#15803d" stroke-width="1"/>
<text x="465" y="217" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Итерация 4</text>
<text x="465" y="270" text-anchor="middle" font-size="11" fill="#64748b">Пропущена только 2-я итерация</text>
''') + '''

<h3>break — выход из цикла</h3>
<p><code>break</code> немедленно прерывает цикл. Код после цикла продолжает выполняться.</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Поиск первого отрицательного числа</span><br>
<span style="color:#8be9fd">numbers</span> = [<span style="color:#bd93f9">3</span>, <span style="color:#bd93f9">7</span>, <span style="color:#bd93f9">-2</span>, <span style="color:#bd93f9">5</span>, <span style="color:#bd93f9">-8</span>]<br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> <span style="color:#8be9fd">numbers</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> &lt; <span style="color:#bd93f9">0</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"Первое отрицательное: {n}"</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">break</span><br>
<span style="color:#6272a4"># Вывод: Первое отрицательное: -2</span>
</div>

<h3>continue — пропуск итерации</h3>
<p><code>continue</code> пропускает оставшийся код текущей итерации и переходит к следующей:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Вывести только положительные</span><br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> [<span style="color:#bd93f9">3</span>, <span style="color:#bd93f9">-1</span>, <span style="color:#bd93f9">7</span>, <span style="color:#bd93f9">-4</span>, <span style="color:#bd93f9">5</span>]:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> &lt; <span style="color:#bd93f9">0</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">continue</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">n</span>, end=<span style="color:#f1fa8c">" "</span>)<br>
<span style="color:#6272a4"># Вывод: 3 7 5</span>
</div>

<h3>else в циклах — уникальная фишка Python</h3>
<p>Блок <code>else</code> после цикла выполняется, <strong>только если цикл
завершился нормально</strong> (без <code>break</code>):</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Ситуация</th><th>else выполнится?</th></tr>
<tr><td>Цикл завершился нормально (все итерации)</td><td style="color:#16a34a;font-weight:bold">Да</td></tr>
<tr><td>Цикл прерван через <code>break</code></td><td style="color:#dc2626;font-weight:bold">Нет</td></tr>
<tr><td>Цикл не выполнялся ни разу (пустой range)</td><td style="color:#16a34a;font-weight:bold">Да</td></tr>
</table>

<h3>Практический пример: проверка простого числа</h3>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#ff79c6">def</span> <span style="color:#50fa7b">is_prime</span>(<span style="color:#8be9fd">n</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> &lt; <span style="color:#bd93f9">2</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">return</span> <span style="color:#bd93f9">False</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">i</span> <span style="color:#ff79c6">in</span> <span style="color:#50fa7b">range</span>(<span style="color:#bd93f9">2</span>, <span style="color:#50fa7b">int</span>(<span style="color:#8be9fd">n</span>**<span style="color:#bd93f9">0.5</span>) + <span style="color:#bd93f9">1</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> % <span style="color:#8be9fd">i</span> == <span style="color:#bd93f9">0</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">return</span> <span style="color:#bd93f9">False</span>  <span style="color:#6272a4"># нашли делитель</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">return</span> <span style="color:#bd93f9">True</span>  <span style="color:#6272a4"># делителей не нашлось</span>
</div>

<h3>Паттерн: бесконечный цикл с break</h3>
<p>Распространённый паттерн — <code>while True</code> с выходом через <code>break</code>:</p>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#ff79c6">while</span> <span style="color:#bd93f9">True</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">cmd</span> = <span style="color:#50fa7b">input</span>(<span style="color:#f1fa8c">">>> "</span>)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">cmd</span> == <span style="color:#f1fa8c">"exit"</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">break</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"Команда: {cmd}"</span>)
</div>

<h3>Запомните</h3>
<ul>
<li><code>break</code> — полный выход из цикла</li>
<li><code>continue</code> — пропуск текущей итерации</li>
<li><code>else</code> после цикла — выполняется, если не было <code>break</code></li>
<li><code>while True: ... break</code> — стандартный паттерн для ввода</li>
<li>В многоуровневых циклах <code>break</code> выходит только из ближайшего</li>
</ul>
'''
    },
    {
        'title': 'Практические алгоритмы: накопление, подсчет, поиск',
        'order': 5,
        'minutes': 15,
        'code': '''# 1. Накопление суммы
numbers = [10, 20, 30, 40, 50]
total = 0
for n in numbers:
    total += n
print(f"Сумма: {total}")  # 150

# 2. Подсчет элементов
grades = [5, 4, 3, 5, 4, 5, 2, 4, 5]
count_5 = 0
for g in grades:
    if g == 5:
        count_5 += 1
print(f"Пятерок: {count_5}")  # 4

# 3. Поиск максимума
values = [3, 7, 1, 9, 4, 6]
max_val = values[0]  # начинаем с первого элемента
for v in values[1:]:
    if v > max_val:
        max_val = v
print(f"Максимум: {max_val}")  # 9

# 4. Фильтрация
numbers = [1, -3, 5, -7, 9, -2, 4]
positive = []
for n in numbers:
    if n > 0:
        positive.append(n)
print(f"Положительные: {positive}")  # [1, 5, 9, 4]

# 5. Среднее арифметическое
data = [85, 92, 78, 95, 88]
avg = sum(data) / len(data)
print(f"Среднее: {avg:.1f}")  # 87.6

# 6. Факториал
n = 5
factorial = 1
for i in range(1, n + 1):
    factorial *= i
print(f"{n}! = {factorial}")  # 120

# 7. Числа Фибоначчи
a, b = 0, 1
fib = []
for _ in range(10):
    fib.append(a)
    a, b = b, a + b
print(f"Фибоначчи: {fib}")
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# 8. Обращение строки
text = "Python"
reversed_text = ""
for ch in text:
    reversed_text = ch + reversed_text
print(reversed_text)  # nohtyP''',
        'content': '''
<h2>Практические алгоритмы: накопление, подсчет, поиск</h2>
<p>Большинство задач с циклами сводятся к нескольким базовым паттернам.
Освоив их, вы сможете решить 90% типовых задач.</p>

<h3>Паттерн 1: Накопление (аккумулятор)</h3>
<p>Идея: создаём переменную-аккумулятор и прибавляем к ней на каждой итерации.</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Сумма чисел от 1 до N</span><br>
<span style="color:#8be9fd">n</span> = <span style="color:#bd93f9">100</span><br>
<span style="color:#8be9fd">total</span> = <span style="color:#bd93f9">0</span>  <span style="color:#6272a4"># аккумулятор</span><br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">i</span> <span style="color:#ff79c6">in</span> <span style="color:#50fa7b">range</span>(<span style="color:#bd93f9">1</span>, <span style="color:#8be9fd">n</span> + <span style="color:#bd93f9">1</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">total</span> += <span style="color:#8be9fd">i</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#8be9fd">total</span>)  <span style="color:#6272a4"># 5050</span>
</div>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Задача</th><th>Начальное значение</th><th>Операция</th></tr>
<tr><td>Сумма</td><td><code>total = 0</code></td><td><code>total += x</code></td></tr>
<tr><td>Произведение</td><td><code>product = 1</code></td><td><code>product *= x</code></td></tr>
<tr><td>Конкатенация</td><td><code>result = ""</code></td><td><code>result += s</code></td></tr>
<tr><td>Сбор в список</td><td><code>items = []</code></td><td><code>items.append(x)</code></td></tr>
</table>

<h3>Паттерн 2: Подсчёт</h3>
<p>Считаем, сколько элементов удовлетворяют условию:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#8be9fd">count</span> = <span style="color:#bd93f9">0</span><br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">char</span> <span style="color:#ff79c6">in</span> <span style="color:#f1fa8c">"Hello, World!"</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">char</span>.<span style="color:#50fa7b">isupper</span>():<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">count</span> += <span style="color:#bd93f9">1</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"Заглавных букв: {count}"</span>)  <span style="color:#6272a4"># 2</span>
</div>

<h3>Паттерн 3: Поиск минимума/максимума</h3>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#8be9fd">temps</span> = [<span style="color:#bd93f9">-5</span>, <span style="color:#bd93f9">3</span>, <span style="color:#bd93f9">-12</span>, <span style="color:#bd93f9">7</span>, <span style="color:#bd93f9">0</span>, <span style="color:#bd93f9">-3</span>]<br>
<span style="color:#8be9fd">min_t</span> = <span style="color:#8be9fd">temps</span>[<span style="color:#bd93f9">0</span>]<br>
<span style="color:#8be9fd">min_idx</span> = <span style="color:#bd93f9">0</span><br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">i</span>, <span style="color:#8be9fd">t</span> <span style="color:#ff79c6">in</span> <span style="color:#50fa7b">enumerate</span>(<span style="color:#8be9fd">temps</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">t</span> &lt; <span style="color:#8be9fd">min_t</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">min_t</span> = <span style="color:#8be9fd">t</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">min_idx</span> = <span style="color:#8be9fd">i</span><br>
<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"Мин: {min_t} (день {min_idx + 1})"</span>)
</div>

<h3>Паттерн 4: Фильтрация</h3>
<p>Отбираем только нужные элементы:</p>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Через цикл</span><br>
<span style="color:#8be9fd">evens</span> = []<br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> <span style="color:#50fa7b">range</span>(<span style="color:#bd93f9">20</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> % <span style="color:#bd93f9">2</span> == <span style="color:#bd93f9">0</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">evens</span>.<span style="color:#50fa7b">append</span>(<span style="color:#8be9fd">n</span>)<br><br>
<span style="color:#6272a4"># Через list comprehension (изучим позже)</span><br>
<span style="color:#8be9fd">evens</span> = [<span style="color:#8be9fd">n</span> <span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> <span style="color:#50fa7b">range</span>(<span style="color:#bd93f9">20</span>) <span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> % <span style="color:#bd93f9">2</span> == <span style="color:#bd93f9">0</span>]
</div>

<h3>Паттерн 5: Флаг</h3>
<p>Проверяем, выполняется ли условие хотя бы для одного элемента:</p>
<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#8be9fd">has_negative</span> = <span style="color:#bd93f9">False</span><br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> <span style="color:#8be9fd">numbers</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">if</span> <span style="color:#8be9fd">n</span> &lt; <span style="color:#bd93f9">0</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#8be9fd">has_negative</span> = <span style="color:#bd93f9">True</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#ff79c6">break</span><br><br>
<span style="color:#6272a4"># Встроенные аналоги:</span><br>
<span style="color:#50fa7b">any</span>(<span style="color:#8be9fd">n</span> &lt; <span style="color:#bd93f9">0</span> <span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> <span style="color:#8be9fd">numbers</span>)  <span style="color:#6272a4"># True если хоть один</span><br>
<span style="color:#50fa7b">all</span>(<span style="color:#8be9fd">n</span> > <span style="color:#bd93f9">0</span> <span style="color:#ff79c6">for</span> <span style="color:#8be9fd">n</span> <span style="color:#ff79c6">in</span> <span style="color:#8be9fd">numbers</span>)  <span style="color:#6272a4"># True если все</span>
</div>

<h3>Шпаргалка по паттернам</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Паттерн</th><th>Начало</th><th>Тело цикла</th><th>Встроенный аналог</th></tr>
<tr><td>Сумма</td><td><code>s = 0</code></td><td><code>s += x</code></td><td><code>sum(lst)</code></td></tr>
<tr><td>Подсчет</td><td><code>c = 0</code></td><td><code>if cond: c += 1</code></td><td><code>sum(1 for x in ...)</code></td></tr>
<tr><td>Максимум</td><td><code>m = lst[0]</code></td><td><code>if x > m: m = x</code></td><td><code>max(lst)</code></td></tr>
<tr><td>Фильтр</td><td><code>res = []</code></td><td><code>if cond: res.append(x)</code></td><td><code>[x for x if cond]</code></td></tr>
<tr><td>Флаг</td><td><code>f = False</code></td><td><code>if cond: f = True</code></td><td><code>any(...)</code></td></tr>
</table>

<h3>Запомните</h3>
<ul>
<li>Каждый паттерн начинается с <strong>инициализации</strong> переменной перед циклом</li>
<li>Используйте встроенные функции (<code>sum</code>, <code>max</code>, <code>min</code>, <code>any</code>, <code>all</code>) когда возможно</li>
<li>Комбинируйте паттерны: поиск максимума + его индекса через <code>enumerate</code></li>
<li>Числа Фибоначчи и факториал — классические задачи на накопление</li>
</ul>
'''
    },
]

# ── М5 новые уроки ──────────────────────────────────────────────────────────

M5_NEW = [
    {
        'title': 'enumerate, zip и распаковка в циклах',
        'order': 3,
        'minutes': 12,
        'code': '''# enumerate — индекс + элемент
fruits = ["яблоко", "банан", "вишня"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: яблоко
# 1: банан
# 2: вишня

# enumerate с начальным индексом
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip — параллельный обход
names = ["Анна", "Борис", "Вера"]
ages = [20, 22, 19]
for name, age in zip(names, ages):
    print(f"{name}: {age} лет")

# zip с тремя списками
cities = ["Москва", "Питер", "Казань"]
for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age}, {city}")

# Распаковка кортежей
points = [(1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"({x}, {y})")

# Создание словаря из zip
keys = ["name", "age", "city"]
values = ["Алиса", 25, "Москва"]
person = dict(zip(keys, values))
print(person)  # {'name': 'Алиса', 'age': 25, 'city': 'Москва'}

# reversed и sorted в циклах
for n in reversed(range(5)):
    print(n, end=" ")  # 4 3 2 1 0

for ch in sorted("python"):
    print(ch, end="")  # hnopty''',
        'content': '''
<h2>enumerate, zip и распаковка в циклах</h2>
<p>Python предоставляет мощные инструменты для элегантной итерации. Вместо
работы с индексами вручную используйте <code>enumerate</code> и <code>zip</code>.</p>

<h3>enumerate — нумерация элементов</h3>
<p>Когда нужен и индекс, и значение, не пишите <code>for i in range(len(lst))</code>.
Используйте <code>enumerate</code>:</p>

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr><th style="background:#fee2e2">Плохо</th><th style="background:#dcfce7">Хорошо</th></tr>
<tr><td><code>for i in range(len(items)):<br>&nbsp;&nbsp;print(i, items[i])</code></td>
    <td><code>for i, item in enumerate(items):<br>&nbsp;&nbsp;print(i, item)</code></td></tr>
</table>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#8be9fd">students</span> = [<span style="color:#f1fa8c">"Анна"</span>, <span style="color:#f1fa8c">"Борис"</span>, <span style="color:#f1fa8c">"Вера"</span>]<br><br>
<span style="color:#6272a4"># Нумерация с 1</span><br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">num</span>, <span style="color:#8be9fd">name</span> <span style="color:#ff79c6">in</span> <span style="color:#50fa7b">enumerate</span>(<span style="color:#8be9fd">students</span>, <span style="color:#8be9fd">start</span>=<span style="color:#bd93f9">1</span>):<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"{num}. {name}"</span>)<br>
<span style="color:#6272a4"># 1. Анна</span><br>
<span style="color:#6272a4"># 2. Борис</span><br>
<span style="color:#6272a4"># 3. Вера</span>
</div>

<h3>zip — параллельный обход нескольких списков</h3>
<p><code>zip</code> объединяет элементы нескольких коллекций в кортежи:</p>

''' + svg_wrap('zip: параллельное объединение списков', '''
<rect width="620" height="320" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
<text x="100" y="35" text-anchor="middle" font-size="13" fill="#334155" font-weight="bold">names</text>
<text x="310" y="35" text-anchor="middle" font-size="13" fill="#334155" font-weight="bold">ages</text>
<text x="520" y="35" text-anchor="middle" font-size="13" fill="#334155" font-weight="bold">zip(names, ages)</text>

<rect x="30" y="50" width="140" height="35" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>
<text x="100" y="72" text-anchor="middle" font-size="12" fill="#1e40af">"Анна"</text>
<rect x="30" y="95" width="140" height="35" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>
<text x="100" y="117" text-anchor="middle" font-size="12" fill="#1e40af">"Борис"</text>
<rect x="30" y="140" width="140" height="35" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>
<text x="100" y="162" text-anchor="middle" font-size="12" fill="#1e40af">"Вера"</text>

<rect x="240" y="50" width="140" height="35" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>
<text x="310" y="72" text-anchor="middle" font-size="12" fill="#15803d">20</text>
<rect x="240" y="95" width="140" height="35" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>
<text x="310" y="117" text-anchor="middle" font-size="12" fill="#15803d">22</text>
<rect x="240" y="140" width="140" height="35" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>
<text x="310" y="162" text-anchor="middle" font-size="12" fill="#15803d">19</text>

<line x1="180" y1="67" x2="430" y2="67" stroke="#64748b" stroke-width="1" stroke-dasharray="4"/>
<line x1="180" y1="112" x2="430" y2="112" stroke="#64748b" stroke-width="1" stroke-dasharray="4"/>
<line x1="180" y1="157" x2="430" y2="157" stroke="#64748b" stroke-width="1" stroke-dasharray="4"/>

<rect x="430" y="50" width="170" height="35" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
<text x="515" y="72" text-anchor="middle" font-size="11" fill="#92400e">("Анна", 20)</text>
<rect x="430" y="95" width="170" height="35" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
<text x="515" y="117" text-anchor="middle" font-size="11" fill="#92400e">("Борис", 22)</text>
<rect x="430" y="140" width="170" height="35" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
<text x="515" y="162" text-anchor="middle" font-size="11" fill="#92400e">("Вера", 19)</text>

<rect x="30" y="200" width="560" height="100" rx="8" fill="#1e1e2e"/>
<text x="50" y="225" font-size="12" fill="#ff79c6" font-family="monospace">for</text>
<text x="80" y="225" font-size="12" fill="#8be9fd" font-family="monospace">name, age</text>
<text x="180" y="225" font-size="12" fill="#ff79c6" font-family="monospace">in</text>
<text x="200" y="225" font-size="12" fill="#50fa7b" font-family="monospace">zip(names, ages):</text>
<text x="70" y="255" font-size="12" fill="#50fa7b" font-family="monospace">print(f"{name}: {age}")</text>
<text x="50" y="285" font-size="11" fill="#6272a4" font-family="monospace"># Анна: 20 / Борис: 22 / Вера: 19</text>
''') + '''

<h3>Распаковка (unpacking) в циклах</h3>
<p>Если элементы коллекции — кортежи или списки, их можно распаковать прямо в цикле:</p>

<div style="background:#1e1e2e;color:#f8f8f2;padding:1rem;border-radius:8px;font-family:monospace;margin:1rem 0">
<span style="color:#6272a4"># Список точек (x, y)</span><br>
<span style="color:#8be9fd">points</span> = [(<span style="color:#bd93f9">0</span>, <span style="color:#bd93f9">0</span>), (<span style="color:#bd93f9">1</span>, <span style="color:#bd93f9">3</span>), (<span style="color:#bd93f9">2</span>, <span style="color:#bd93f9">7</span>)]<br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">x</span>, <span style="color:#8be9fd">y</span> <span style="color:#ff79c6">in</span> <span style="color:#8be9fd">points</span>:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"({x}, {y})"</span>)<br><br>
<span style="color:#6272a4"># Обход словаря (ключ + значение)</span><br>
<span style="color:#8be9fd">scores</span> = {<span style="color:#f1fa8c">"Анна"</span>: <span style="color:#bd93f9">95</span>, <span style="color:#f1fa8c">"Борис"</span>: <span style="color:#bd93f9">82</span>}<br>
<span style="color:#ff79c6">for</span> <span style="color:#8be9fd">name</span>, <span style="color:#8be9fd">score</span> <span style="color:#ff79c6">in</span> <span style="color:#8be9fd">scores</span>.<span style="color:#50fa7b">items</span>():<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#50fa7b">print</span>(<span style="color:#f1fa8c">f"{name}: {score}"</span>)
</div>

<h3>Полезные функции для циклов</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;margin:1rem 0">
<tr style="background:#f1f5f9"><th>Функция</th><th>Описание</th><th>Пример</th></tr>
<tr><td><code>enumerate(seq)</code></td><td>Индекс + элемент</td><td><code>for i, x in enumerate(lst)</code></td></tr>
<tr><td><code>zip(a, b)</code></td><td>Параллельный обход</td><td><code>for x, y in zip(a, b)</code></td></tr>
<tr><td><code>reversed(seq)</code></td><td>Обратный порядок</td><td><code>for x in reversed(lst)</code></td></tr>
<tr><td><code>sorted(seq)</code></td><td>Отсортированный</td><td><code>for x in sorted(lst)</code></td></tr>
<tr><td><code>dict.items()</code></td><td>Пары ключ-значение</td><td><code>for k, v in d.items()</code></td></tr>
</table>

<h3>Запомните</h3>
<ul>
<li><code>enumerate</code> — вместо <code>range(len(...))</code></li>
<li><code>zip</code> — для параллельного обхода нескольких списков</li>
<li><code>zip</code> останавливается по самому <strong>короткому</strong> списку</li>
<li>Распаковка кортежей делает циклы чистыми и понятными</li>
<li><code>dict(zip(keys, values))</code> — быстрое создание словаря</li>
</ul>
'''
    },
]


class Command(BaseCommand):
    help = 'Расширяет модули 1-5 ОАИП новыми уроками'

    def handle(self, *args, **options):
        oaip = Subject.objects.get(title__contains='ОАИП')

        modules = {m.order: m for m in oaip.modules.order_by('order')}

        plan = [
            (1, M1_NEW),
            (3, M3_NEW),
            (4, M4_NEW),
            (5, M5_NEW),
        ]

        added = 0
        for m_order, lessons_data in plan:
            module = modules.get(m_order)
            if not module:
                self.stdout.write(f'[SKIP] Module {m_order} not found')
                continue

            existing_titles = set(
                module.lessons.values_list('title', flat=True)
            )

            for ld in lessons_data:
                if ld['title'] in existing_titles:
                    self.stdout.write(
                        f'[SKIP] M{m_order} L{ld["order"]}: {ld["title"][:40]} (exists)'
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
                    f'[+] M{m_order} L{ld["order"]}: {ld["title"][:45]}'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'\n[DONE] Added {added} new lessons'
        ))
