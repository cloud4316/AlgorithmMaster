# -*- coding: utf-8 -*-
"""
Вторая волна SVG-диаграмм для базовых Python-уроков.
Запуск: python manage.py seed_diagrams_patch2
"""
from django.core.management.base import BaseCommand
from works.models import TheoryLesson

ARROW = ('<defs>'
         '<marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
         '<path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker>'
         '<marker id="ag" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
         '<path d="M0,0 L0,6 L8,3 z" fill="#059669"/></marker>'
         '<marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
         '<path d="M0,0 L0,6 L8,3 z" fill="#dc2626"/></marker>'
         '</defs>')


def svg(w, h, *parts):
    inner = ''.join(str(p) for p in parts)
    return (f'<div style="overflow-x:auto;margin:1.2rem 0">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto;font-family:sans-serif">'
            f'{ARROW}{inner}</svg></div>')


def rect(x, y, w, h, fill, stroke='none', rx=8, tc='#1e293b', label='', fs=13):
    lines = label.split('\n')
    lh = fs + 5
    y0 = y + h // 2 - (lh * (len(lines) - 1)) // 2
    tspans = ''.join(
        f'<tspan x="{x+w//2}" dy="{0 if i==0 else lh}">{l}</tspan>'
        for i, l in enumerate(lines))
    r = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    t = (f'<text x="{x+w//2}" y="{y0}" text-anchor="middle" font-size="{fs}" '
         f'fill="{tc}" dominant-baseline="middle">{tspans}</text>')
    return r + t


def line(x1, y1, x2, y2, c='#64748b', m='url(#ah)', dashed=False):
    d = 'stroke-dasharray="5,4"' if dashed else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.5" marker-end="{m}" {d}/>'


def txt(x, y, text, fs=11, color='#475569', anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{color}">{text}</text>'


def circle(cx, cy, r, fill, stroke, label='', fs=12, tc='#1e293b'):
    c = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    t = f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" font-size="{fs}" fill="{tc}">{label}</text>'
    return c + t


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def diag_numbers():
    """Числовая иерархия Python + примеры"""
    return svg(560, 260,
        txt(280, 18, 'Числовые типы Python', 14, '#1e293b'),
        # int
        rect(20, 36, 155, 200, '#e0f2fe', '#0284c7', rx=10),
        txt(97, 56, 'int', 15, '#0369a1', 'middle'),
        rect(30, 68, 135, 30, '#bfdbfe', '#3b82f6', label='42   -7   0   999', fs=12, tc='#1e3a5f', rx=5),
        rect(30, 104, 135, 30, '#bfdbfe', '#3b82f6', label='0xFF  0b1010  0o17', fs=11, tc='#1e3a5f', rx=5),
        rect(30, 140, 135, 30, '#bfdbfe', '#3b82f6', label='10**18  (без предела!)', fs=11, tc='#1e3a5f', rx=5),
        rect(30, 176, 135, 50, '#93c5fd', '#2563eb', label='int(3.9) → 3\nint("42") → 42', fs=11, tc='#1e3a5f', rx=5),
        # float
        rect(195, 36, 155, 200, '#dcfce7', '#16a34a', rx=10),
        txt(272, 56, 'float', 15, '#15803d', 'middle'),
        rect(205, 68, 135, 30, '#bbf7d0', '#22c55e', label='3.14   -0.5   1e10', fs=12, tc='#14532d', rx=5),
        rect(205, 104, 135, 30, '#bbf7d0', '#22c55e', label='float("inf")  float("nan")', fs=11, tc='#14532d', rx=5),
        rect(205, 140, 135, 30, '#bbf7d0', '#22c55e', label='round(3.14159, 2) → 3.14', fs=11, tc='#14532d', rx=5),
        rect(205, 176, 135, 50, '#86efac', '#15803d', label='float(5) → 5.0\nfloat("3.14") → 3.14', fs=11, tc='#14532d', rx=5),
        # complex
        rect(370, 36, 170, 200, '#fef9c3', '#ca8a04', rx=10),
        txt(455, 56, 'complex', 15, '#854d0e', 'middle'),
        rect(380, 68, 150, 30, '#fef08a', '#eab308', label='2+3j   -1j   0+0j', fs=12, tc='#713f12', rx=5),
        rect(380, 104, 150, 30, '#fef08a', '#eab308', label='z.real → 2.0', fs=11, tc='#713f12', rx=5),
        rect(380, 140, 150, 30, '#fef08a', '#eab308', label='z.imag → 3.0', fs=11, tc='#713f12', rx=5),
        rect(380, 176, 150, 50, '#fde68a', '#d97706', label='abs(3+4j) → 5.0\ncomplex(2,3) → (2+3j)', fs=11, tc='#713f12', rx=5),
    )


def diag_string_ops():
    """Строка Python: индексация, методы"""
    s = list('Python')
    W = 540
    bw = 60
    ox = (W - len(s) * bw) // 2
    parts = [txt(W//2, 18, 's = "Python"', 14, '#1e293b')]
    for i, ch in enumerate(s):
        x = ox + i * bw
        parts.append(rect(x, 28, bw-4, 48, '#ede9fe', '#7c3aed', label=ch, fs=20, tc='#1e293b'))
        parts.append(txt(x+(bw-4)//2, 86, str(i), 12, '#059669'))
        parts.append(txt(x+(bw-4)//2, 100, str(i-len(s)), 12, '#dc2626'))
    parts.append(txt(W//2, 116, 'зелёные — положительные [0..5],  красные — отрицательные [-6..-1]', 11, '#475569'))
    # методы
    methods = [
        ('#e0f2fe','#0284c7','#0369a1', 's.upper() → "PYTHON"'),
        ('#dcfce7','#16a34a','#15803d', 's.lower() → "python"'),
        ('#fef9c3','#ca8a04','#854d0e', 's[0:3] → "Pyt"'),
        ('#fee2e2','#dc2626','#991b1b', 's[::-1] → "nohtyP"'),
        ('#ede9fe','#7c3aed','#4c1d95', 's.replace("P","J") → "Jython"'),
        ('#fff7ed','#ea580c','#9a3412', '"hello world".split() → ["hello","world"]'),
    ]
    cols = 3
    mw, mh = 240, 34
    mx0 = (W - cols * (mw + 8)) // 2
    for idx, (f, s2, tc, lbl) in enumerate(methods):
        row, col = divmod(idx, cols)
        parts.append(rect(mx0 + col*(mw+8), 130 + row*(mh+6), mw, mh, f, s2, label=lbl, fs=11, tc=tc, rx=5))
    return svg(W, 210, *parts)


def diag_range():
    """range() — три формы"""
    return svg(540, 250,
        txt(270, 18, 'Три формы range()', 14, '#1e293b'),
        # form 1
        rect(20, 34, 155, 56, '#e0f2fe', '#0284c7', label='range(5)', fs=14, tc='#0369a1'),
        txt(97, 98, 'stop=5, start=0, step=1', 10, '#475569'),
        # cells
        *[rect(20+i*31, 108, 28, 32, '#bfdbfe', '#3b82f6', label=str(i), fs=13, tc='#1e3a5f') for i in range(5)],
        txt(97, 150, '[0, 1, 2, 3, 4]', 12, '#0369a1'),
        # form 2
        rect(195, 34, 155, 56, '#dcfce7', '#16a34a', label='range(2, 8)', fs=14, tc='#15803d'),
        txt(272, 98, 'start=2, stop=8, step=1', 10, '#475569'),
        *[rect(195+i*31, 108, 28, 32, '#bbf7d0', '#22c55e', label=str(i+2), fs=13, tc='#14532d') for i in range(6)],
        txt(272, 150, '[2, 3, 4, 5, 6, 7]', 12, '#15803d'),
        # form 3
        rect(370, 34, 155, 56, '#fef9c3', '#ca8a04', label='range(0, 10, 2)', fs=13, tc='#854d0e'),
        txt(447, 98, 'start=0, stop=10, step=2', 10, '#475569'),
        *[rect(370+i*31, 108, 28, 32, '#fef08a', '#eab308', label=str(i*2), fs=13, tc='#713f12') for i in range(5)],
        txt(447, 150, '[0, 2, 4, 6, 8]', 12, '#854d0e'),
        # memory note
        rect(20, 168, 500, 68, '#f8fafc', '#e2e8f0', label='range НЕ хранит список в памяти — он генерирует числа по требованию.\nrange(1_000_000) занимает столько же памяти, что и range(5).\nДля получения списка: list(range(5)) → [0, 1, 2, 3, 4]', fs=12, tc='#334155', rx=8),
    )


def diag_matrix():
    """Двумерный массив — сетка"""
    rows, cols = 3, 4
    data = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    cw, ch = 64, 44
    ox, oy = 30, 50
    parts = [txt(280, 18, 'Двумерный массив (матрица) 3×4', 14, '#1e293b')]
    # column headers
    for j in range(cols):
        parts.append(txt(ox + j*cw + cw//2, oy - 12, f'[{j}]', 11, '#0369a1'))
    for i in range(rows):
        # row header
        parts.append(txt(ox - 18, oy + i*ch + ch//2, f'[{i}]', 11, '#dc2626'))
        for j in range(cols):
            val = data[i][j]
            clr = '#e0f2fe' if (i+j)%2==0 else '#ede9fe'
            brd = '#0284c7' if (i+j)%2==0 else '#7c3aed'
            parts.append(rect(ox+j*cw, oy+i*ch, cw-3, ch-3, clr, brd, label=f'mat[{i}][{j}]\n= {val}', fs=11, tc='#1e293b', rx=4))
    # index note
    parts.append(txt(30, oy+rows*ch+20, f'mat[строка][столбец]  →  mat[1][2] = {data[1][2]}', 12, '#475569', 'start'))
    # code
    code_x = ox + cols*cw + 20
    parts.append(rect(code_x, oy, 175, 120, '#f8fafc', '#e2e8f0',
        label='mat = [\n  [1,2,3,4],\n  [5,6,7,8],\n  [9,10,11,12]\n]\n\nfor row in mat:\n  for v in row:\n    print(v)', fs=11, tc='#334155', rx=6))
    return svg(560, 230, *parts)


def diag_dict():
    """Словарь Python: ключ → значение (хеш-таблица)"""
    pairs = [('name', '"Алиса"', '#e0f2fe', '#0284c7', '#0369a1'),
             ('age',  '20',      '#dcfce7', '#16a34a', '#15803d'),
             ('city', '"Москва"','#fef9c3', '#ca8a04', '#854d0e'),
             ('gpa',  '4.8',     '#ede9fe', '#7c3aed', '#4c1d95')]
    parts = [txt(260, 18, 'Словарь (dict): ключ → хеш → значение', 13, '#1e293b')]
    # key column header
    parts.append(txt(100, 40, 'Ключ', 12, '#475569'))
    parts.append(txt(260, 40, 'hash(ключ)', 12, '#475569'))
    parts.append(txt(400, 40, 'Значение', 12, '#475569'))
    for i, (k, v, f, s, tc) in enumerate(pairs):
        y = 52 + i * 48
        parts.append(rect(30, y, 140, 38, f, s, label=f'"{k}"', fs=13, tc=tc, rx=5))
        parts.append(line(170, y+19, 210, y+19))
        parts.append(rect(210, y, 100, 38, '#f1f5f9', '#cbd5e1', label=f'hash(…)', fs=11, tc='#64748b', rx=4))
        parts.append(line(310, y+19, 350, y+19))
        parts.append(rect(350, y, 150, 38, f, s, label=v, fs=13, tc=tc, rx=5))
    parts.append(txt(30, 52+len(pairs)*48+16, 'Поиск по ключу O(1) — хеш сразу указывает на ячейку', 11, '#475569', 'start'))
    return svg(520, 52+len(pairs)*48+36, *parts)


def diag_set():
    """Операции над множествами"""
    def ellipse(cx, cy, rx, ry, fill, stroke, opacity=0.55):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" fill-opacity="{opacity}"/>'

    W, H = 560, 260
    parts = [txt(W//2, 18, 'Операции над множествами', 14, '#1e293b')]

    # A∪B
    parts.append(txt(80, 40, 'A | B  (объединение)', 11, '#0369a1'))
    parts.append(ellipse(60, 80, 38, 28, '#3b82f6', '#0284c7'))
    parts.append(ellipse(90, 80, 38, 28, '#3b82f6', '#0284c7'))
    parts.append(txt(60, 80, 'A', 11, '#fff', 'middle'))
    parts.append(txt(90, 80, 'B', 11, '#fff', 'middle'))
    parts.append(txt(75, 118, '{1,2,3,4,5}', 10, '#475569'))

    # A∩B
    parts.append(txt(220, 40, 'A & B  (пересечение)', 11, '#15803d'))
    parts.append(ellipse(200, 80, 38, 28, '#e2e8f0', '#94a3b8', 0.9))
    parts.append(ellipse(240, 80, 38, 28, '#e2e8f0', '#94a3b8', 0.9))
    parts.append(ellipse(220, 80, 20, 28, '#22c55e', '#16a34a', 0.8))
    parts.append(txt(200, 80, 'A', 11, '#334155', 'middle'))
    parts.append(txt(240, 80, 'B', 11, '#334155', 'middle'))
    parts.append(txt(220, 118, '{3}', 10, '#475569'))

    # A-B
    parts.append(txt(370, 40, 'A - B  (разность)', 11, '#991b1b'))
    parts.append(ellipse(355, 80, 38, 28, '#fca5a5', '#dc2626', 0.8))
    parts.append(ellipse(395, 80, 38, 28, '#e2e8f0', '#94a3b8', 0.8))
    parts.append(txt(348, 80, 'A', 11, '#991b1b', 'middle'))
    parts.append(txt(395, 80, 'B', 11, '#334155', 'middle'))
    parts.append(txt(365, 118, '{1,2}', 10, '#475569'))

    # A^B (symmetric)
    parts.append(txt(475, 40, 'A ^ B  (симм. разность)', 11, '#854d0e'))
    parts.append(ellipse(462, 80, 38, 28, '#fde68a', '#d97706', 0.8))
    parts.append(ellipse(502, 80, 38, 28, '#fde68a', '#d97706', 0.8))
    parts.append(ellipse(482, 80, 20, 28, '#e2e8f0', '#94a3b8', 0.9))
    parts.append(txt(458, 80, 'A', 11, '#92400e', 'middle'))
    parts.append(txt(502, 80, 'B', 11, '#92400e', 'middle'))
    parts.append(txt(482, 118, '{1,2,4,5}', 10, '#475569'))

    # A={1,2,3}  B={3,4,5}
    parts.append(txt(W//2, 142, 'Пример: A = {1, 2, 3},  B = {3, 4, 5}', 12, '#334155'))

    # свойства
    props = [('Нет дубликатов', '#e0f2fe','#0284c7','#0369a1'),
             ('Нет порядка', '#fef9c3','#ca8a04','#854d0e'),
             ('O(1) проверка "in"', '#dcfce7','#16a34a','#15803d'),
             ('Только хешируемые', '#ede9fe','#7c3aed','#4c1d95')]
    pw = 118
    px0 = (W - len(props)*(pw+6))//2
    for idx, (lbl, f, s, tc) in enumerate(props):
        parts.append(rect(px0+idx*(pw+6), 156, pw, 34, f, s, label=lbl, fs=11, tc=tc, rx=5))

    parts.append(txt(W//2, 204, 'frozenset — неизменяемое множество, можно использовать как ключ словаря', 11, '#64748b'))
    return svg(W, 215, *parts)


def diag_inheritance():
    """Наследование: иерархия классов"""
    return svg(560, 300,
        txt(280, 18, 'Наследование: иерархия классов', 14, '#1e293b'),
        # base
        rect(195, 34, 170, 60, '#e0f2fe', '#0284c7', label='Animal (базовый)\n+ name, sound\n+ speak()', fs=12, tc='#0369a1', rx=8),
        # arrows down
        f'<path d="M 255 94 L 140 138" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        f'<path d="M 280 94 L 280 138" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        f'<path d="M 325 94 L 420 138" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        txt(175, 120, 'наследует', 10, '#94a3b8'),
        # children
        rect(60, 138, 140, 70, '#dcfce7', '#16a34a', label='Dog\n+ breed\n+ speak() → "Гав!"', fs=11, tc='#15803d', rx=7),
        rect(210, 138, 140, 70, '#fef9c3', '#ca8a04', label='Cat\n+ indoor\n+ speak() → "Мяу!"', fs=11, tc='#854d0e', rx=7),
        rect(360, 138, 140, 70, '#ede9fe', '#7c3aed', label='Bird\n+ can_fly\n+ speak() → "Чирик!"', fs=11, tc='#4c1d95', rx=7),
        # grandchild
        f'<path d="M 130 208 L 130 252" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        rect(60, 252, 140, 44, '#bbf7d0', '#059669', label='GuideDog(Dog)\n+ owner', fs=11, tc='#064e3b', rx=7),
        # polymorphism note
        rect(220, 252, 290, 44, '#fff7ed', '#ea580c', label='Полиморфизм: for a in [Dog(),Cat(),Bird()]:\n    a.speak()  → разный вывод!', fs=11, tc='#9a3412', rx=7),
    )


def diag_comprehension():
    """List comprehension vs обычный цикл"""
    return svg(540, 230,
        txt(270, 18, 'Генератор списка vs обычный цикл', 14, '#1e293b'),
        # loop version
        rect(20, 36, 230, 110, '#fee2e2', '#dc2626', label='', rx=8),
        txt(135, 56, 'Обычный цикл (3 строки)', 12, '#991b1b', 'middle'),
        rect(30, 66, 210, 70, '#fecaca', '#ef4444', label='result = []\nfor x in range(10):\n    if x % 2 == 0:\n        result.append(x**2)', fs=11, tc='#7f1d1d', rx=5),
        # arrow
        f'<path d="M 250 91 L 290 91" stroke="#64748b" stroke-width="2" marker-end="url(#ah)"/>',
        txt(270, 84, 'то же', 10, '#475569'),
        # comprehension
        rect(290, 36, 230, 110, '#dcfce7', '#16a34a', label='', rx=8),
        txt(405, 56, 'List comprehension (1 строка)', 12, '#15803d', 'middle'),
        rect(300, 66, 210, 70, '#bbf7d0', '#22c55e', label='result = [\n  x**2\n  for x in range(10)\n  if x % 2 == 0\n]', fs=11, tc='#14532d', rx=5),
        # result
        rect(140, 158, 260, 36, '#f0fdf4', '#15803d', label='Результат: [0, 4, 16, 36, 64]', fs=13, tc='#15803d', rx=6),
        # anatomy
        rect(20, 200, 500, 24, '#f8fafc', '#e2e8f0', label='[выражение  for переменная in итерируемое  if условие]', fs=11, tc='#334155', rx=4),
    )


def diag_decorator():
    """Декоратор: обёртка над функцией"""
    return svg(560, 300,
        txt(280, 18, 'Декоратор: @wraps оборачивает функцию', 14, '#1e293b'),
        # original function
        rect(30, 36, 155, 60, '#e0f2fe', '#0284c7', label='def greet(name):\n    return f"Привет, {name}"', fs=11, tc='#0369a1', rx=7),
        txt(107, 104, 'оригинальная функция', 10, '#64748b'),
        line(107, 96, 107, 128, '#64748b', 'none'),
        # decorator
        f'<path d="M 185 66 L 250 66" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        txt(217, 58, '@log_call', 11, '#7c3aed'),
        rect(250, 36, 275, 195, '#ede9fe', '#7c3aed', label='', rx=10),
        txt(387, 56, 'Декоратор log_call', 13, '#4c1d95', 'middle'),
        rect(260, 66, 255, 40, '#ddd6fe', '#7c3aed', label='def wrapper(*args, **kwargs):', fs=11, tc='#4c1d95', rx=5),
        rect(260, 114, 255, 34, '#c4b5fd', '#6d28d9', label='print("Вызов до...")', fs=11, tc='#3730a3', rx=5),
        rect(260, 154, 255, 34, '#a78bfa', '#6d28d9', label='result = func(*args, **kwargs)', fs=11, tc='#3730a3', rx=5),
        rect(260, 194, 255, 34, '#c4b5fd', '#6d28d9', label='print("После")', fs=11, tc='#3730a3', rx=5),
        # result arrow
        f'<path d="M 387 231 L 387 262" stroke="#059669" stroke-width="1.5" marker-end="url(#ag)"/>',
        # call
        rect(250, 262, 275, 30, '#dcfce7', '#16a34a', label='greet("Аня")  →  обёрнутый вызов', fs=11, tc='#15803d', rx=5),
        # usage
        txt(107, 155, '@log_call', 12, '#7c3aed', 'middle'),
        txt(107, 170, 'def greet(name):', 11, '#0369a1', 'middle'),
        txt(107, 185, '   ...', 11, '#475569', 'middle'),
        txt(107, 208, '≡ greet = log_call(greet)', 10, '#94a3b8', 'middle'),
    )


def diag_iterator():
    """Протокол итератора __iter__ / __next__"""
    return svg(540, 270,
        txt(270, 18, 'Протокол итератора в Python', 14, '#1e293b'),
        # iterable
        rect(20, 36, 150, 56, '#e0f2fe', '#0284c7', label='Iterable\n(list, range, str…)', fs=12, tc='#0369a1', rx=7),
        txt(95, 100, '__iter__()', 11, '#0284c7'),
        f'<path d="M 170 64 L 220 64" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        txt(195, 56, 'iter()', 10, '#475569'),
        # iterator
        rect(220, 36, 150, 56, '#dcfce7', '#16a34a', label='Iterator\n(хранит позицию)', fs=12, tc='#15803d', rx=7),
        txt(295, 100, '__next__()', 11, '#16a34a'),
        f'<path d="M 370 64 L 420 64" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        txt(395, 56, 'next()', 10, '#475569'),
        # values
        rect(420, 36, 100, 56, '#fef9c3', '#ca8a04', label='Значения\nпо одному', fs=12, tc='#854d0e', rx=7),
        # stopiteration
        f'<path d="M 470 92 L 470 132" stroke="#dc2626" stroke-width="1.5" marker-end="url(#ar)"/>',
        rect(390, 132, 130, 36, '#fee2e2', '#dc2626', label='StopIteration\n(конец)', fs=11, tc='#991b1b', rx=5),
        # for loop = auto iterator
        rect(20, 120, 340, 56, '#fff7ed', '#ea580c', label='for x in iterable:\n    # Python сам вызывает iter() и next()\n    # StopIteration → выход', fs=11, tc='#9a3412', rx=8),
        # custom iterator
        rect(20, 192, 500, 64, '#f8fafc', '#e2e8f0',
             label='class Counter:\n    def __iter__(self): self.n=0; return self\n    def __next__(self):\n        if self.n>=5: raise StopIteration\n        self.n+=1; return self.n', fs=11, tc='#334155', rx=7),
    )


def diag_asyncio():
    """asyncio: event loop, корутины, задачи"""
    return svg(560, 280,
        txt(280, 18, 'asyncio: Event Loop и корутины', 14, '#1e293b'),
        # event loop
        rect(185, 34, 190, 46, '#1e293b', '#0f172a', label='Event Loop', fs=14, tc='#e2e8f0', rx=10),
        # tasks
        rect(20, 110, 140, 50, '#ede9fe', '#7c3aed', label='Task 1\nasync def fetch(url)', fs=11, tc='#4c1d95', rx=7),
        rect(200, 110, 140, 50, '#dcfce7', '#16a34a', label='Task 2\nasync def save(data)', fs=11, tc='#15803d', rx=7),
        rect(380, 110, 140, 50, '#fef9c3', '#ca8a04', label='Task 3\nasync def process()', fs=11, tc='#854d0e', rx=7),
        # arrows loop → tasks
        f'<path d="M 220 80 L 90 110" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        f'<path d="M 280 80 L 270 110" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        f'<path d="M 340 80 L 450 110" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        # await IO
        rect(90, 180, 100, 36, '#fee2e2', '#dc2626', label='await IO\n(ждёт ответа)', fs=10, tc='#991b1b', rx=5),
        f'<path d="M 90 160 L 90 180" stroke="#dc2626" stroke-width="1.5" fill="none" marker-end="url(#ar)" stroke-dasharray="4,3"/>',
        txt(90, 224, 'loop берёт другую\nзадачу', 10, '#64748b', 'middle'),
        # resume
        f'<path d="M 140 198 L 200 198 L 200 160" stroke="#059669" stroke-width="1.5" fill="none" marker-end="url(#ag)" stroke-dasharray="4,3"/>',
        txt(172, 192, 'resume', 10, '#059669'),
        # code
        rect(245, 175, 290, 80, '#f8fafc', '#e2e8f0',
             label='async def main():\n    r = await asyncio.gather(\n        fetch(url1), fetch(url2)\n    )  # параллельно!\nasyncio.run(main())', fs=11, tc='#334155', rx=7),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PATCHES = [
    ('Числовые типы: int, float',   '<h3>Три числовых типа Python</h3>',           diag_numbers),
    ('Числа: int, float',            '<h3>Три числовых типа Python</h3>',           diag_numbers),
    ('Строки: создание',             '<h3>Индексы и методы строки</h3>',            diag_string_ops),
    ('Строки и функция',             '<h3>Индексы и методы строки</h3>',            diag_string_ops),
    ('Цикл for и функция range',     '<h3>Как работает range()</h3>',              diag_range),
    ('Двумерные массивы',            '<h3>Двумерный массив: индексы</h3>',          diag_matrix),
    ('Словари: хранение данных',     '<h3>Словарь: ключ → хеш → значение</h3>',   diag_dict),
    ('Словари (dict)',               '<h3>Словарь: ключ → хеш → значение</h3>',   diag_dict),
    ('Кортежи, множества',           '<h3>Операции над множествами</h3>',           diag_set),
    ('Наследование и полиморфизм',   '<h3>Иерархия классов и полиморфизм</h3>',    diag_inheritance),
    ('Генераторы списков',           '<h3>List comprehension vs цикл</h3>',         diag_comprehension),
    ('Декораторы: обёртки',          '<h3>Как работает декоратор</h3>',             diag_decorator),
    ('Итераторы: протокол',          '<h3>Протокол итератора</h3>',                 diag_iterator),
    ('asyncio на практике',          '<h3>Event Loop и корутины</h3>',              diag_asyncio),
]


class Command(BaseCommand):
    help = 'Вторая волна SVG-диаграмм для Python-уроков'

    def handle(self, *args, **options):
        updated = skipped = 0
        for title_fragment, header, diag_fn in PATCHES:
            lessons = TheoryLesson.objects.filter(title__icontains=title_fragment)
            if not lessons.exists():
                self.stdout.write(f'[SKIP] не найдено: {title_fragment!r}')
                skipped += 1
                continue
            marker = header.replace('<h3>', '').replace('</h3>', '').strip()
            for lesson in lessons:
                if marker in lesson.content:
                    self.stdout.write(f'[SKIP] уже есть: {lesson.title!r}')
                    skipped += 1
                    continue
                lesson.content = f'\n{header}\n{diag_fn()}\n' + lesson.content
                lesson.save()
                self.stdout.write(f'[OK]   {lesson.title!r}')
                updated += 1
        self.stdout.write(f'\nГотово: обновлено {updated}, пропущено {skipped}')
