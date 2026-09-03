# -*- coding: utf-8 -*-
"""
Добавляет SVG-диаграммы в базовые уроки Python без визуализации.
Запуск: python manage.py seed_diagrams_patch
"""
from django.core.management.base import BaseCommand
from works.models import TheoryLesson

ARROW = ('<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" '
         'orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker>'
         '<marker id="ah2" markerWidth="8" markerHeight="8" refX="6" refY="3" '
         'orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#059669"/></marker>'
         '<marker id="ahr" markerWidth="8" markerHeight="8" refX="6" refY="3" '
         'orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#dc2626"/></marker>'
         '</defs>')


def svg(w, h, *parts):
    inner = ''.join(parts)
    return (f'<div style="overflow-x:auto;margin:1.2rem 0">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto;font-family:sans-serif">'
            f'{ARROW}{inner}</svg></div>')


def rect(x, y, w, h, fill, stroke='none', rx=8, tc='#1e293b', label='', fs=13):
    lines = label.split('\n')
    lh = fs + 5
    y0 = y + h // 2 - (lh * (len(lines) - 1)) // 2
    tspans = ''.join(
        f'<tspan x="{x + w // 2}" dy="{0 if i == 0 else lh}">{l}</tspan>'
        for i, l in enumerate(lines)
    )
    r = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    t = (f'<text x="{x+w//2}" y="{y0}" text-anchor="middle" font-size="{fs}" '
         f'fill="{tc}" dominant-baseline="middle">{tspans}</text>')
    return r + t


def diamond(cx, cy, hw, hh, fill, stroke, label, fs=12):
    pts = f'{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}'
    t = f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="{fs}" fill="#1e293b" dominant-baseline="middle">{label}</text>'
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>{t}'


def line(x1, y1, x2, y2, color='#64748b', marker='url(#ah)', dashed=False):
    dash = 'stroke-dasharray="5,4"' if dashed else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="1.5" marker-end="{marker}" {dash}/>')


def txt(x, y, text, fs=11, color='#475569', anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{color}">{text}</text>'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Диаграммы
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def diag_if_elif_else():
    """Блок-схема if / elif / else"""
    return svg(560, 400,
        rect(200, 10, 160, 40, '#e0f2fe', '#0284c7', label='Начало', fs=13, tc='#0369a1'),
        line(280, 50, 280, 90),
        diamond(280, 120, 110, 35, '#fef9c3', '#ca8a04', 'условие 1?', fs=12),
        line(390, 120, 480, 120, '#059669', 'url(#ah2)'),
        txt(435, 115, 'True', 11, '#059669'),
        rect(480, 98, 65, 44, '#dcfce7', '#16a34a', label='блок\nif', fs=12, tc='#15803d'),
        line(280, 155, 280, 195),
        txt(285, 178, 'False', 11, '#dc2626', 'start'),
        diamond(280, 225, 110, 35, '#fef9c3', '#ca8a04', 'условие 2?', fs=12),
        line(390, 225, 480, 225, '#059669', 'url(#ah2)'),
        txt(435, 220, 'True', 11, '#059669'),
        rect(480, 203, 65, 44, '#dcfce7', '#16a34a', label='блок\nelif', fs=12, tc='#15803d'),
        line(280, 260, 280, 300),
        txt(285, 285, 'False', 11, '#dc2626', 'start'),
        rect(220, 300, 120, 44, '#fee2e2', '#dc2626', label='блок else', fs=12, tc='#991b1b'),
        # сводим ветки в конец
        f'<path d="M 545 120 L 545 370 L 280 370" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        f'<path d="M 545 225 L 545 370" stroke="#64748b" stroke-width="1.5" fill="none"/>',
        line(280, 344, 280, 360),
        rect(200, 360, 160, 36, '#f1f5f9', '#94a3b8', label='Конец / продолжение', fs=11, tc='#475569'),
    )


def diag_while():
    """Блок-схема цикла while"""
    return svg(480, 380,
        rect(170, 10, 140, 40, '#e0f2fe', '#0284c7', label='Начало', fs=13, tc='#0369a1'),
        line(240, 50, 240, 88),
        diamond(240, 120, 120, 36, '#fef9c3', '#ca8a04', 'условие\nTrue?', fs=12),
        line(360, 120, 420, 120, '#dc2626', 'url(#ahr)'),
        txt(388, 112, 'False', 11, '#dc2626'),
        rect(400, 98, 65, 44, '#fee2e2', '#dc2626', label='выход\nиз цикла', fs=11, tc='#991b1b'),
        line(240, 156, 240, 196),
        txt(245, 178, 'True', 11, '#059669', 'start'),
        rect(175, 196, 130, 44, '#dcfce7', '#16a34a', label='тело цикла', fs=13, tc='#15803d'),
        # стрелка назад (влево-вверх-вправо)
        f'<path d="M 175 218 L 80 218 L 80 120 L 120 120" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        txt(50, 175, 'повтор', 11, '#64748b'),
        line(432, 142, 432, 340),
        line(432, 340, 240, 340),
        rect(170, 340, 140, 36, '#f1f5f9', '#94a3b8', label='После цикла', fs=11, tc='#475569'),
    )


def diag_for():
    """Блок-схема цикла for + итератор"""
    return svg(560, 400,
        # верхний блок — итерируемый объект
        rect(190, 10, 180, 44, '#ede9fe', '#7c3aed', label='Итерируемый объект\n[0, 1, 2, 3, 4]', fs=12, tc='#4c1d95'),
        line(280, 54, 280, 92),
        rect(190, 92, 180, 40, '#e0f2fe', '#0284c7', label='Взять следующий элемент', fs=11, tc='#0369a1'),
        line(280, 132, 280, 168),
        diamond(280, 200, 115, 34, '#fef9c3', '#ca8a04', 'элементы\nесть?', fs=12),
        line(395, 200, 455, 200, '#dc2626', 'url(#ahr)'),
        txt(420, 193, 'Нет', 11, '#dc2626'),
        rect(435, 178, 110, 44, '#fee2e2', '#dc2626', label='Конец\nцикла for', fs=12, tc='#991b1b'),
        line(280, 234, 280, 272),
        txt(285, 256, 'Да', 11, '#059669', 'start'),
        rect(195, 272, 170, 44, '#dcfce7', '#16a34a', label='тело цикла\n(переменная = элемент)', fs=11, tc='#15803d'),
        # обратная стрелка
        f'<path d="M 195 294 L 90 294 L 90 112 L 190 112" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        txt(55, 205, 'следующий', 11, '#64748b'),
        # выход
        f'<path d="M 490 200 L 490 370 L 280 370" stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>',
        rect(195, 358, 170, 36, '#f1f5f9', '#94a3b8', label='После цикла for', fs=11, tc='#475569'),
    )


def diag_function():
    """Вызов функции: caller → frame → return"""
    return svg(580, 300,
        # caller
        rect(20, 110, 150, 80, '#e0f2fe', '#0284c7', label='Вызывающий\nкод\nresult = f(x)', fs=12, tc='#0369a1'),
        line(170, 150, 215, 150),
        txt(192, 143, 'вызов', 10, '#64748b'),
        # stack frame
        rect(215, 60, 170, 180, '#ede9fe', '#7c3aed', label='', fs=12),
        txt(300, 82, 'Stack Frame', 11, '#4c1d95', 'middle'),
        rect(225, 92, 150, 36, '#ddd6fe', '#7c3aed', label='параметры (x=...)', fs=11, tc='#4c1d95', rx=5),
        rect(225, 136, 150, 36, '#ddd6fe', '#7c3aed', label='локальные переменные', fs=11, tc='#4c1d95', rx=5),
        rect(225, 180, 150, 44, '#c4b5fd', '#6d28d9', label='return result', fs=12, tc='#3b0764', rx=5),
        # return arrow
        f'<path d="M 300 224 L 300 260 L 95 260 L 95 190" stroke="#059669" stroke-width="1.5" fill="none" marker-end="url(#ah2)"/>',
        txt(200, 274, 'возврат значения', 11, '#059669'),
        # result
        rect(20, 150, 70, 30, '#dcfce7', '#16a34a', label='result', fs=12, tc='#15803d', rx=5),
        # heap
        rect(410, 80, 145, 100, '#fff7ed', '#ea580c', label='Heap Memory\n(объекты)\n42, [1,2,3], "hi"', fs=11, tc='#9a3412'),
        f'<path d="M 375 130 L 410 130" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3" fill="none" marker-end="url(#ah)"/>',
        txt(392, 123, 'ссылки', 10, '#94a3b8'),
    )


def diag_list_index():
    """Список Python: индексы, срезы"""
    items = ['🍎', '🍌', '🍇', '🍓', '🥝']
    parts = []
    W = 540
    box_w = 70
    start_x = (W - len(items) * box_w) // 2
    y_box = 60
    # boxes
    for i, v in enumerate(items):
        x = start_x + i * box_w
        parts.append(rect(x, y_box, box_w - 4, 50, '#e0f2fe', '#0284c7', label=v, fs=20, tc='#1e293b'))
        parts.append(txt(x + (box_w - 4)//2, y_box + 66, str(i), 12, '#059669'))
        parts.append(txt(x + (box_w - 4)//2, y_box + 82, str(i - len(items)), 12, '#dc2626'))
    parts.append(txt(W//2, y_box + 98, 'положительные индексы: 0..4', 11, '#059669'))
    parts.append(txt(W//2, y_box + 114, 'отрицательные индексы: -5..-1', 11, '#dc2626'))
    # header
    parts.append(txt(W//2, 40, 'lst = ["🍎","🍌","🍇","🍓","🥝"]', 13, '#1e293b'))
    # срезы
    slice_y = 145
    parts.append(rect(start_x, slice_y, (box_w - 4)*2 + 4, 34, '#fef9c3', '#ca8a04', label='lst[0:2] → [🍎, 🍌]', fs=11, tc='#854d0e'))
    parts.append(rect(start_x + (box_w)*2, slice_y, (box_w-4)*3 + 8, 34, '#dcfce7', '#16a34a', label='lst[2:] → [🍇, 🍓, 🥝]', fs=11, tc='#15803d'))
    parts.append(txt(W//2, slice_y + 54, 'lst[-1] → 🥝   •   lst[::2] → [🍎, 🍇, 🥝]   •   lst[::-1] — реверс', 11, '#475569'))
    return svg(W, 210, *parts)


def diag_try_except():
    """Поток выполнения try / except / finally"""
    return svg(580, 360,
        rect(200, 10, 180, 40, '#e0f2fe', '#0284c7', label='Начало', fs=13, tc='#0369a1'),
        line(290, 50, 290, 88),
        rect(195, 88, 190, 50, '#ede9fe', '#7c3aed', label='try: блок кода\n(может упасть)', fs=12, tc='#4c1d95'),
        # два исхода
        f'<path d="M 290 138 L 290 180" stroke="#059669" stroke-width="1.5" marker-end="url(#ah2)"/>',
        txt(297, 162, 'нет ошибки', 10, '#059669', 'start'),
        f'<path d="M 385 113 L 490 113 L 490 200" stroke="#dc2626" stroke-width="1.5" marker-end="url(#ahr)"/>',
        txt(437, 106, 'Exception!', 11, '#dc2626'),
        rect(215, 180, 150, 44, '#dcfce7', '#16a34a', label='else:\n(если нет ошибки)', fs=11, tc='#15803d'),
        rect(430, 188, 120, 44, '#fee2e2', '#dc2626', label='except:\nобработка', fs=12, tc='#991b1b'),
        # finally
        line(290, 224, 290, 272),
        f'<path d="M 490 232 L 490 272 L 340 272" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        rect(195, 272, 150, 44, '#fff7ed', '#ea580c', label='finally:\nвсегда выполняется', fs=11, tc='#9a3412'),
        line(290, 316, 290, 345),
        rect(200, 345, 180, 36, '#f1f5f9', '#94a3b8', label='Продолжение программы', fs=11, tc='#475569'),
    )


def diag_recursion():
    """Рекурсия: дерево вызовов factorial(4)"""
    return svg(560, 310,
        txt(280, 22, 'factorial(4) — дерево вызовов', 14, '#1e293b'),
        # level 0
        rect(210, 36, 140, 38, '#ede9fe', '#7c3aed', label='factorial(4)', fs=13, tc='#4c1d95'),
        line(280, 74, 280, 106),
        # level 1
        rect(210, 106, 140, 38, '#ddd6fe', '#7c3aed', label='factorial(3)', fs=13, tc='#4c1d95'),
        line(280, 144, 280, 176),
        # level 2
        rect(210, 176, 140, 38, '#c4b5fd', '#6d28d9', label='factorial(2)', fs=13, tc='#3730a3'),
        line(280, 214, 280, 244),
        # level 3 (base case)
        rect(210, 244, 140, 38, '#a78bfa', '#6d28d9', label='factorial(1) = 1', fs=13, tc='#2e1065'),
        # return arrows (right side)
        f'<path d="M 350 263 L 430 263 L 430 124 L 350 124" stroke="#059669" stroke-width="1.5" fill="none" marker-end="url(#ah2)" stroke-dasharray="5,3"/>',
        txt(454, 193, 'return', 11, '#059669'),
        txt(454, 207, '1,2,6,24', 11, '#059669'),
        # labels
        txt(165, 55, '4 × f(3)', 11, '#64748b'),
        txt(165, 125, '3 × f(2)', 11, '#64748b'),
        txt(165, 195, '2 × f(1)', 11, '#64748b'),
        txt(165, 263, 'база', 11, '#059669'),
        # result
        rect(195, 290, 170, 14, '#dcfce7', 'none', label='', fs=1),
        txt(280, 302, 'Результат: 4×3×2×1 = 24', 12, '#15803d'),
    )


def diag_class_object():
    """Класс → экземпляр (OOP)"""
    return svg(580, 300,
        # class blueprint
        rect(20, 30, 210, 240, '#ede9fe', '#7c3aed', label='', rx=10),
        txt(125, 52, 'class Student:', 13, '#4c1d95', 'middle'),
        rect(30, 62, 190, 38, '#ddd6fe', '#7c3aed', label='__init__(self, name, grade)', fs=11, tc='#4c1d95', rx=5),
        rect(30, 108, 190, 30, '#ddd6fe', '#7c3aed', label='self.name = name', fs=11, tc='#4c1d95', rx=5),
        rect(30, 146, 190, 30, '#ddd6fe', '#7c3aed', label='self.grade = grade', fs=11, tc='#4c1d95', rx=5),
        rect(30, 190, 190, 30, '#c4b5fd', '#6d28d9', label='def greet(self): ...', fs=11, tc='#3730a3', rx=5),
        rect(30, 228, 190, 30, '#c4b5fd', '#6d28d9', label='def study(self): ...', fs=11, tc='#3730a3', rx=5),
        txt(125, 278, 'Шаблон (Blueprint)', 12, '#7c3aed', 'middle'),
        # arrow
        f'<path d="M 230 150 L 290 150" stroke="#64748b" stroke-width="2" marker-end="url(#ah)"/>',
        txt(260, 143, 'создаёт', 11, '#64748b'),
        # instance 1
        rect(295, 30, 130, 120, '#dcfce7', '#16a34a', label='', rx=8),
        txt(360, 50, 's1 (объект)', 12, '#15803d', 'middle'),
        rect(305, 60, 110, 26, '#bbf7d0', '#16a34a', label='name = "Аня"', fs=11, tc='#15803d', rx=4),
        rect(305, 92, 110, 26, '#bbf7d0', '#16a34a', label='grade = 5', fs=11, tc='#15803d', rx=4),
        rect(305, 124, 110, 20, '#86efac', '#15803d', label='greet(), study()', fs=10, tc='#14532d', rx=4),
        # instance 2
        rect(440, 30, 130, 120, '#fff7ed', '#ea580c', label='', rx=8),
        txt(505, 50, 's2 (объект)', 12, '#9a3412', 'middle'),
        rect(450, 60, 110, 26, '#fed7aa', '#ea580c', label='name = "Вася"', fs=11, tc='#9a3412', rx=4),
        rect(450, 92, 110, 26, '#fed7aa', '#ea580c', label='grade = 4', fs=11, tc='#9a3412', rx=4),
        rect(450, 124, 110, 20, '#fdba74', '#c2410c', label='greet(), study()', fs=10, tc='#7c2d12', rx=4),
        f'<path d="M 230 150 L 290 150" stroke="#64748b" stroke-width="2"/>',
        # code sample
        rect(295, 168, 275, 60, '#f8fafc', '#e2e8f0', label='s1 = Student("Аня", 5)\ns2 = Student("Вася", 4)\ns1.greet()', fs=11, tc='#334155', rx=6),
        txt(432, 246, 'Student() → вызывает __init__ → создаёт объект', 10, '#64748b', 'middle'),
    )


def diag_bubble_sort():
    """Пузырьковая сортировка — один проход"""
    parts = []
    arr0 = [5, 3, 8, 1, 9]
    W = 520
    bw = 54
    step_y = [20, 100, 180, 260]
    colors = ['#fee2e2', '#fef9c3', '#dcfce7', '#e0f2fe']
    borders = ['#dc2626', '#ca8a04', '#16a34a', '#0284c7']
    labels = ['Исходный', 'Шаг 1: сравним 5,3 → меняем', 'Шаг 2: сравним 5,8 → ок', 'Шаг 3: …итог прохода']
    arrs = [
        [5, 3, 8, 1, 9],
        [3, 5, 8, 1, 9],
        [3, 5, 8, 1, 9],
        [3, 5, 1, 8, 9],
    ]
    for si, (sy, arr, c, b, lbl) in enumerate(zip(step_y, arrs, colors, borders, labels)):
        parts.append(txt(W//2, sy + 14, lbl, 11, '#475569'))
        for i, v in enumerate(arr):
            x = (W - len(arr)*bw)//2 + i*bw
            fill = '#bbf7d0' if (si > 0 and i in (si-1, si)) else c
            parts.append(rect(x, sy + 22, bw-4, 46, fill, b, label=str(v), fs=18, tc='#1e293b'))
    return svg(W, 340, *parts)


def diag_merge_sort():
    """Сортировка слиянием — дерево разбиений"""
    return svg(560, 320,
        txt(280, 18, 'Сортировка слиянием: [5,3,8,1] → разбить и слить', 12, '#1e293b'),
        # level 0
        rect(190, 30, 180, 38, '#e0f2fe', '#0284c7', label='[5, 3, 8, 1]', fs=14, tc='#0369a1'),
        # split arrows
        f'<path d="M 250 68 L 140 108" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        f'<path d="M 330 68 L 420 108" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        # level 1
        rect(80, 108, 120, 38, '#ede9fe', '#7c3aed', label='[5, 3]', fs=14, tc='#4c1d95'),
        rect(360, 108, 120, 38, '#ede9fe', '#7c3aed', label='[8, 1]', fs=14, tc='#4c1d95'),
        # split arrows 2
        f'<path d="M 120 146 L 75 186" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        f'<path d="M 160 146 L 195 186" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        f'<path d="M 400 146 L 355 186" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        f'<path d="M 440 146 L 475 186" stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>',
        # level 2 (leaves)
        rect(45, 186, 60, 38, '#dcfce7', '#16a34a', label='[5]', fs=14, tc='#15803d'),
        rect(165, 186, 60, 38, '#dcfce7', '#16a34a', label='[3]', fs=14, tc='#15803d'),
        rect(325, 186, 60, 38, '#dcfce7', '#16a34a', label='[8]', fs=14, tc='#15803d'),
        rect(445, 186, 60, 38, '#dcfce7', '#16a34a', label='[1]', fs=14, tc='#15803d'),
        txt(280, 248, '▼  слияние (merge)  ▼', 12, '#ca8a04', 'middle'),
        # merge level
        rect(80, 264, 120, 38, '#fef9c3', '#ca8a04', label='[3, 5]', fs=14, tc='#854d0e'),
        rect(360, 264, 120, 38, '#fef9c3', '#ca8a04', label='[1, 8]', fs=14, tc='#854d0e'),
        f'<path d="M 140 264 L 230 312" stroke="#064e3b" stroke-width="1.5" marker-end="url(#ah2)"/>',
        f'<path d="M 420 264 L 330 312" stroke="#064e3b" stroke-width="1.5" marker-end="url(#ah2)"/>',
        rect(190, 300, 180, 14, '#dcfce7', '#059669', label='', rx=4),
        txt(280, 313, '[1, 3, 5, 8]  — готово!', 13, '#15803d', 'middle'),
    )


def diag_nested_if():
    """Вложенные условия — дерево ветвлений"""
    return svg(560, 320,
        txt(280, 18, 'Вложенные условия: дерево решений', 13, '#1e293b'),
        diamond(280, 60, 120, 36, '#fef9c3', '#ca8a04', 'age >= 18?', fs=13),
        # left branch (False)
        f'<path d="M 160 60 L 80 130" stroke="#dc2626" stroke-width="1.5" marker-end="url(#ahr)"/>',
        txt(105, 98, 'Нет', 11, '#dc2626'),
        rect(20, 130, 120, 40, '#fee2e2', '#dc2626', label='«Вам нет 18 лет»', fs=11, tc='#991b1b'),
        # right branch (True)
        f'<path d="M 400 60 L 480 130" stroke="#059669" stroke-width="1.5" marker-end="url(#ah2)"/>',
        txt(455, 98, 'Да', 11, '#059669'),
        diamond(480, 170, 75, 30, '#ddd6fe', '#7c3aed', 'студент?', fs=12),
        f'<path d="M 405 170 L 330 230" stroke="#dc2626" stroke-width="1.5" marker-end="url(#ahr)"/>',
        txt(352, 203, 'Нет', 11, '#dc2626'),
        f'<path d="M 555 170 L 520 230" stroke="#059669" stroke-width="1.5" marker-end="url(#ah2)"/>',
        txt(546, 203, 'Да', 11, '#059669'),
        rect(270, 230, 120, 40, '#fee2e2', '#dc2626', label='Полная цена', fs=12, tc='#991b1b'),
        rect(450, 230, 120, 40, '#dcfce7', '#16a34a', label='Скидка 50%', fs=12, tc='#15803d'),
        txt(280, 302, 'Каждый ромб — одно условие (if). Глубина = количество вложений.', 11, '#64748b'),
    )


def diag_nested_loops():
    """Вложенные циклы — таблица умножения"""
    parts = []
    parts.append(txt(250, 18, 'Вложенные циклы: for i in range(1,4): for j in range(1,4)', 11, '#475569'))
    n = 3
    cell_w, cell_h = 65, 42
    ox, oy = 45, 36
    header_color = '#e0f2fe'
    header_tc = '#0369a1'
    # column headers
    for j in range(n):
        parts.append(rect(ox + (j+1)*cell_w, oy, cell_w-3, cell_h-3, header_color, '#0284c7', label=f'j={j+1}', fs=13, tc=header_tc))
    # row headers + cells
    for i in range(n):
        parts.append(rect(ox, oy + (i+1)*cell_h, cell_w-3, cell_h-3, header_color, '#0284c7', label=f'i={i+1}', fs=13, tc=header_tc))
        for j in range(n):
            val = (i+1)*(j+1)
            clr = '#dcfce7' if val < 5 else ('#fef9c3' if val < 7 else '#ede9fe')
            brd = '#16a34a' if val < 5 else ('#ca8a04' if val < 7 else '#7c3aed')
            tc2 = '#15803d' if val < 5 else ('#854d0e' if val < 7 else '#4c1d95')
            parts.append(rect(ox + (j+1)*cell_w, oy + (i+1)*cell_h, cell_w-3, cell_h-3, clr, brd, label=str(val), fs=16, tc=tc2))
    # code snippet
    code_x, code_y = ox + (n+1)*cell_w + 20, oy
    parts.append(rect(code_x, code_y, 165, 130, '#f8fafc', '#e2e8f0', label='for i in range(1,4):\n  for j in range(1,4):\n    print(i*j)\n\n→ i×j для каждой\n   пары (i,j)', fs=11, tc='#334155', rx=6))
    return svg(500, 210, *parts)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Таблица: название урока → (заголовок блока, SVG-функция)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PATCHES = [
    # (fragment of lesson title, section header, diagram_func)
    ('if / elif / else',
     '<h3>Блок-схема: если / иначе если / иначе</h3>',
     diag_if_elif_else),
    ('Цикл while',
     '<h3>Блок-схема цикла while</h3>',
     diag_while),
    ('Цикл for: итерация',
     '<h3>Блок-схема цикла for</h3>',
     diag_for),
    ('Функции: определение',
     '<h3>Как работает вызов функции</h3>',
     diag_function),
    ('Списки: создание',
     '<h3>Индексы и срезы списка</h3>',
     diag_list_index),
    ('Исключения: try',
     '<h3>Поток выполнения try / except / finally</h3>',
     diag_try_except),
    ('Рекурсия: суть',
     '<h3>Дерево рекурсивных вызовов</h3>',
     diag_recursion),
    ('Классы и объекты в Python',
     '<h3>Класс — шаблон, объект — экземпляр</h3>',
     diag_class_object),
    ('Квадратичные алгоритмы сортировки',
     '<h3>Пузырьковая сортировка: шаги</h3>',
     diag_bubble_sort),
    ('Быстрая сортировка и сортировка слиянием',
     '<h3>Сортировка слиянием: дерево разбиений</h3>',
     diag_merge_sort),
    ('Вложенные условия и упрощение',
     '<h3>Вложенные условия: дерево решений</h3>',
     diag_nested_if),
    ('Вложенные циклы: паттерны',
     '<h3>Вложенные циклы: визуализация</h3>',
     diag_nested_loops),
]


class Command(BaseCommand):
    help = 'Добавляет SVG-диаграммы в базовые уроки Python'

    def handle(self, *args, **options):
        updated = 0
        skipped = 0

        for title_fragment, header, diag_fn in PATCHES:
            lessons = TheoryLesson.objects.filter(title__icontains=title_fragment)
            if not lessons.exists():
                self.stdout.write(f'[SKIP] не найдено: {title_fragment!r}')
                skipped += 1
                continue

            diagram_block = f'\n{header}\n{diag_fn()}\n'

            for lesson in lessons:
                # Не добавлять повторно
                marker = header.replace('<h3>', '').replace('</h3>', '').strip()
                if marker in lesson.content:
                    self.stdout.write(f'[SKIP] уже есть: {lesson.title!r}')
                    skipped += 1
                    continue

                lesson.content = diagram_block + lesson.content
                lesson.save()
                self.stdout.write(f'[OK]   {lesson.title!r}')
                updated += 1

        self.stdout.write(f'\nГотово: обновлено {updated}, пропущено {skipped}')
