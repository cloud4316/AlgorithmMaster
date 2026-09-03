"""
seed_theory_advanced3 — Modules 51–60
Topics: matplotlib, string algorithms, caching, functional programming,
metaclasses, concurrent queues, security/hashing, clean architecture,
generators deep dive, final project guide.
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


def tip(text):
    return f'<div class="tip">&#128161; {text}</div>'


def warn(text):
    return f'<div class="warning">&#9888;&#65039; {text}</div>'


def table(headers, rows, caption=''):
    cap = f'<caption style="font-weight:600;margin-bottom:.5rem">{caption}</caption>' if caption else ''
    ths = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return (f'<div class="theory-table"><table>{cap}'
            f'<thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>')


def diagram(inner, w=600, h=260, caption=''):
    cap = (f'<p style="text-align:center;font-size:.85rem;color:#6b7280;margin-top:.4rem">{caption}</p>'
           if caption else '')
    return (f'<div style="overflow-x:auto;margin:1rem 0">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;display:block;margin:0 auto">'
            f'{inner}</svg>{cap}</div>')


MODULES = [
    # ─── 51: Matplotlib ──────────────────────────────────────────────────────
    {
        'title': 'Визуализация данных: Matplotlib',
        'description': 'Построение графиков и диаграмм для анализа данных.',
        'icon': 'fas fa-chart-line',
        'order': 51,
        'lessons': [
            {
                'title': 'Графики, гистограммы, scatter',
                'order': 1,
                'estimated_minutes': 65,
                'content': (
                    '<h2>Matplotlib — основы</h2>'
                    '<p>matplotlib — стандарт визуализации Python. Почти все data science библиотеки '
                    'строят свои графики поверх него.</p>'
                    + table(
                        ['Функция', 'Тип графика', 'Применение'],
                        [
                            ['plt.plot(x, y)', 'Линейный', 'Временные ряды, функции'],
                            ['plt.scatter(x, y)', 'Точечный', 'Корреляции, кластеры'],
                            ['plt.bar(x, height)', 'Столбчатый', 'Категориальные данные'],
                            ['plt.hist(data, bins)', 'Гистограмма', 'Распределение'],
                            ['plt.pie(sizes, labels)', 'Круговой', 'Доли целого'],
                            ['plt.boxplot(data)', 'Box plot', 'Квартили, выбросы'],
                            ['plt.imshow(matrix)', 'Тепловая карта', 'Матрицы, изображения'],
                        ],
                        'Типы графиков'
                    )
                    + '<h3>Базовый линейный график</h3>'
                    '<pre><code>import matplotlib.pyplot as plt\nimport numpy as np\n\n# Данные\nx = np.linspace(0, 2 * np.pi, 100)\ny1 = np.sin(x)\ny2 = np.cos(x)\n\n# Рисуем\nfig, ax = plt.subplots(figsize=(8, 4))\nax.plot(x, y1, label="sin(x)", color="blue", linewidth=2)\nax.plot(x, y2, label="cos(x)", color="red", linewidth=2, linestyle="--")\n\nax.set_title("Тригонометрические функции", fontsize=14)\nax.set_xlabel("x (радианы)")\nax.set_ylabel("y")\nax.legend()\nax.grid(True, alpha=0.3)\n\nplt.tight_layout()\nplt.savefig("trig.png", dpi=150)\nplt.show()\n</code></pre>'
                    + '<h3>Несколько графиков (subplots)</h3>'
                    '<pre><code>fig, axes = plt.subplots(1, 3, figsize=(12, 4))\n\n# График 1: линейный\naxes[0].plot([1,2,3,4,5], [1,4,9,16,25])\naxes[0].set_title("Квадраты")\n\n# График 2: гистограмма\ndata = np.random.randn(1000)\naxes[1].hist(data, bins=30, color="steelblue", edgecolor="white")\naxes[1].set_title("Нормальное распределение")\n\n# График 3: scatter\nx, y = np.random.rand(50), np.random.rand(50)\ncolors = np.random.rand(50)\naxes[2].scatter(x, y, c=colors, s=100, cmap="viridis")\naxes[2].set_title("Scatter plot")\n\nplt.tight_layout()\nplt.savefig("subplots.png")\n</code></pre>'
                    + tip('Используйте объектно-ориентированный API (`fig, ax = plt.subplots()`) вместо pyplot-функций — он предсказуемее при сложных графиках.')
                ),
                'code_example': (
                    'import math\n\n'
                    '# Визуализация без matplotlib — ASCII-график\n\n'
                    'def ascii_plot(func, x_min, x_max, width=60, height=15):\n'
                    '    """ASCII-график функции."""\n'
                    '    xs = [x_min + (x_max - x_min) * i / (width - 1) for i in range(width)]\n'
                    '    ys = [func(x) for x in xs]\n'
                    '    y_min, y_max = min(ys), max(ys)\n'
                    '    grid = [[" "] * width for _ in range(height)]\n'
                    '    for col, y in enumerate(ys):\n'
                    '        row = int((y_max - y) / (y_max - y_min) * (height - 1))\n'
                    '        row = max(0, min(height - 1, row))\n'
                    '        grid[row][col] = "*"\n'
                    '    print(f"y_max={y_max:.2f}")\n'
                    '    for row in grid:\n'
                    '        print("|" + "".join(row) + "|")\n'
                    '    print(f"y_min={y_min:.2f}")\n'
                    '    print(f" {x_min:.1f}" + " " * (width - 8) + f"{x_max:.1f}")\n\n'
                    '# sin(x)\n'
                    'print("--- sin(x) от 0 до 2pi ---")\n'
                    'ascii_plot(math.sin, 0, 2 * math.pi)\n\n'
                    '# x^2 - 4\n'
                    'print("\\n--- x^2 - 4 от -3 до 3 ---")\n'
                    'ascii_plot(lambda x: x**2 - 4, -3, 3)\n'
                ),
            },
            {
                'title': 'Seaborn и статистические визуализации',
                'order': 2,
                'estimated_minutes': 55,
                'content': (
                    '<h2>Seaborn — статистическая визуализация</h2>'
                    '<p>Seaborn строится поверх matplotlib и предоставляет высокоуровневые '
                    'функции для статистических графиков.</p>'
                    + table(
                        ['Функция', 'Тип', 'Применение'],
                        [
                            ['sns.histplot()', 'Гистограмма + KDE', 'Распределение'],
                            ['sns.boxplot()', 'Box plot', 'Сравнение групп'],
                            ['sns.violinplot()', 'Violin plot', 'Форма распределения'],
                            ['sns.heatmap()', 'Тепловая карта', 'Корреляционная матрица'],
                            ['sns.pairplot()', 'Матрица графиков', 'EDA (exploratory analysis)'],
                            ['sns.lineplot()', 'Линейный с CI', 'Временные ряды'],
                            ['sns.barplot()', 'Столбчатый с CI', 'Средние с доверит. интервалом'],
                        ],
                        'Seaborn функции'
                    )
                    + '<h3>Пример: анализ данных студентов</h3>'
                    '<pre><code>import seaborn as sns\nimport matplotlib.pyplot as plt\nimport pandas as pd\n\ndf = pd.DataFrame({\n    "group": ["А"]*10 + ["Б"]*10,\n    "score": [85,90,78,92,88,76,95,82,79,88,\n              72,68,80,75,90,65,78,83,71,77]\n})\n\nfig, axes = plt.subplots(1, 2, figsize=(10, 4))\n\n# Сравнение групп\nsns.boxplot(data=df, x="group", y="score", ax=axes[0])\naxes[0].set_title("Распределение баллов по группам")\n\n# Гистограмма\nsns.histplot(data=df, x="score", hue="group", bins=8, ax=axes[1])\naxes[1].set_title("Гистограмма баллов")\n\nplt.tight_layout()\nplt.show()\n</code></pre>'
                    + '<h3>Корреляционная матрица</h3>'
                    '<pre><code>corr = df_numeric.corr()      # pandas DataFrame\nsns.heatmap(\n    corr,\n    annot=True,    # числа в ячейках\n    fmt=".2f",\n    cmap="coolwarm",\n    center=0,\n    square=True\n)\nplt.title("Матрица корреляций")\n</code></pre>'
                    + tip('Начинайте EDA с `df.describe()`, `sns.pairplot(df)` и корреляционной матрицы — это даёт быстрое понимание данных.')
                ),
                'code_example': (
                    'import statistics\n\n'
                    '# Статистический анализ без библиотек\n\n'
                    'def describe(data: list) -> dict:\n'
                    '    """Аналог df.describe() для списка."""\n'
                    '    n = len(data)\n'
                    '    if n == 0:\n'
                    '        return {}\n'
                    '    sorted_data = sorted(data)\n'
                    '    mean = statistics.mean(data)\n'
                    '    return {\n'
                    '        "count": n,\n'
                    '        "mean":  round(mean, 2),\n'
                    '        "std":   round(statistics.stdev(data), 2),\n'
                    '        "min":   sorted_data[0],\n'
                    '        "25%":   sorted_data[n // 4],\n'
                    '        "50%":   statistics.median(data),\n'
                    '        "75%":   sorted_data[3 * n // 4],\n'
                    '        "max":   sorted_data[-1],\n'
                    '    }\n\n'
                    'scores = [85, 90, 78, 92, 88, 76, 95, 82, 79, 88, 72, 68, 80, 75, 90]\n\n'
                    'stats = describe(scores)\n'
                    'for key, val in stats.items():\n'
                    '    print(f"  {key:8s}: {val}")\n\n'
                    '# Гистограмма в ASCII\n'
                    'def ascii_hist(data, bins=5):\n'
                    '    lo, hi = min(data), max(data)\n'
                    '    step = (hi - lo) / bins\n'
                    '    for i in range(bins):\n'
                    '        low = lo + i * step\n'
                    '        high = lo + (i + 1) * step\n'
                    '        count = sum(1 for x in data if low <= x < high)\n'
                    '        bar = "#" * count\n'
                    '        print(f"  {low:5.1f}-{high:5.1f} | {bar} ({count})")\n\n'
                    'print("\\nГистограмма:")\n'
                    'ascii_hist(scores)\n'
                ),
            },
        ],
    },

    # ─── 52: String algorithms ────────────────────────────────────────────────
    {
        'title': 'Алгоритмы на строках',
        'description': 'KMP, Z-функция, хэширование строк, расстояние Левенштейна.',
        'icon': 'fas fa-font',
        'order': 52,
        'lessons': [
            {
                'title': 'KMP, Z-функция, rolling hash',
                'order': 1,
                'estimated_minutes': 75,
                'content': (
                    '<h2>Поиск подстроки: наивный vs умный</h2>'
                    + table(
                        ['Алгоритм', 'Сложность', 'Особенность'],
                        [
                            ['Наивный поиск', 'O(n·m)', 'Прост, медленно на длинных паттернах'],
                            ['KMP (Кнут-Моррис-Пратт)', 'O(n+m)', 'Использует prefix-функцию'],
                            ['Z-функция', 'O(n+m)', 'Аналог KMP, другой подход'],
                            ['Rabin-Karp (rolling hash)', 'O(n+m) avg', 'Поиск нескольких паттернов'],
                            ['Boyer-Moore', 'O(n/m) best', 'Быстрейший на практике для длинных'],
                        ],
                        'Алгоритмы поиска подстроки'
                    )
                    + '<h3>KMP — prefix-функция</h3>'
                    '<pre><code>def prefix_function(s: str) -> list:\n    """Длина наибольшего собственного суффикса = префиксу."""\n    n = len(s)\n    pi = [0] * n\n    k = 0\n    for i in range(1, n):\n        while k > 0 and s[i] != s[k]:\n            k = pi[k - 1]\n        if s[i] == s[k]:\n            k += 1\n        pi[i] = k\n    return pi\n\ndef kmp_search(text: str, pattern: str) -> list:\n    """Найти все вхождения pattern в text. O(n+m)."""\n    if not pattern: return []\n    combined = pattern + "#" + text\n    pi = prefix_function(combined)\n    m = len(pattern)\n    return [i - 2 * m for i in range(m + 1, len(combined)) if pi[i] == m]\n\n# Пример\npositions = kmp_search("abcabcabc", "abc")\nprint(positions)   # [0, 3, 6]\n</code></pre>'
                    + '<h3>Z-функция</h3>'
                    '<pre><code>def z_function(s: str) -> list:\n    """z[i] = длина наибольшего префикса s, совпадающего с s[i:]."""\n    n = len(s)\n    z = [0] * n\n    z[0] = n\n    l, r = 0, 0\n    for i in range(1, n):\n        if i < r:\n            z[i] = min(r - i, z[i - l])\n        while i + z[i] < n and s[z[i]] == s[i + z[i]]:\n            z[i] += 1\n        if i + z[i] > r:\n            l, r = i, i + z[i]\n    return z\n\ndef z_search(text: str, pattern: str) -> list:\n    combined = pattern + "$" + text\n    z = z_function(combined)\n    m = len(pattern)\n    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] >= m]\n</code></pre>'
                    + '<h3>Расстояние Левенштейна (редакционное)</h3>'
                    '<pre><code>def levenshtein(s1: str, s2: str) -> int:\n    """Минимальное число операций (вставка/удаление/замена) для s1 → s2."""\n    m, n = len(s1), len(s2)\n    dp = list(range(n + 1))\n    for i in range(1, m + 1):\n        prev = dp[:]\n        dp[0] = i\n        for j in range(1, n + 1):\n            if s1[i-1] == s2[j-1]:\n                dp[j] = prev[j-1]\n            else:\n                dp[j] = 1 + min(prev[j], dp[j-1], prev[j-1])\n    return dp[n]\n\nprint(levenshtein("kitten", "sitting"))  # 3\nprint(levenshtein("python", "python"))   # 0\n</code></pre>'
                    + tip('Расстояние Левенштейна используется в spell checkers, поиске дублей, биоинформатике (выравнивание ДНК).')
                ),
                'code_example': (
                    '# Реализация алгоритма KMP и поиска опечаток\n\n'
                    'def levenshtein(s1, s2):\n'
                    '    m, n = len(s1), len(s2)\n'
                    '    dp = list(range(n + 1))\n'
                    '    for i in range(1, m + 1):\n'
                    '        prev = dp[:]\n'
                    '        dp[0] = i\n'
                    '        for j in range(1, n + 1):\n'
                    '            if s1[i-1] == s2[j-1]:\n'
                    '                dp[j] = prev[j-1]\n'
                    '            else:\n'
                    '                dp[j] = 1 + min(prev[j], dp[j-1], prev[j-1])\n'
                    '    return dp[n]\n\n'
                    'def spell_check(word, dictionary, max_dist=2):\n'
                    '    """Найти ближайшие слова в словаре."""\n'
                    '    suggestions = []\n'
                    '    for w in dictionary:\n'
                    '        d = levenshtein(word.lower(), w.lower())\n'
                    '        if d <= max_dist:\n'
                    '            suggestions.append((w, d))\n'
                    '    return sorted(suggestions, key=lambda x: x[1])\n\n'
                    'words = ["python", "функция", "список", "словарь", "цикл",\n'
                    '         "класс", "модуль", "строка", "число", "переменная"]\n\n'
                    'typos = ["pytohn", "фунцкия", "спиоск", "клас"]\n'
                    'for typo in typos:\n'
                    '    sugg = spell_check(typo, words)\n'
                    '    print(f"  {typo!r} -> {sugg[:3]}")\n'
                ),
            },
        ],
    },

    # ─── 53: Caching ─────────────────────────────────────────────────────────
    {
        'title': 'Кэширование и мемоизация',
        'description': 'lru_cache, functools.cache, паттерн кэширования, TTL-кэш.',
        'icon': 'fas fa-memory',
        'order': 53,
        'lessons': [
            {
                'title': 'lru_cache, TTL-кэш, паттерны инвалидации',
                'order': 1,
                'estimated_minutes': 60,
                'content': (
                    '<h2>Зачем кэш?</h2>'
                    '<p>Кэш сохраняет результат дорогих вычислений, чтобы не повторять их при повторных вызовах.</p>'
                    + diagram(
                        '<rect x="10" y="40" width="120" height="50" rx="6" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>'
                        '<text x="70" y="68" text-anchor="middle" font-size="12" fill="#374151">Запрос</text>'
                        '<path d="M130 65 L200 65" stroke="#374151" stroke-width="1.5" marker-end="url(#ax)"/>'
                        '<rect x="200" y="40" width="100" height="50" rx="6" fill="#10b981" opacity=".15" stroke="#10b981"/>'
                        '<text x="250" y="62" text-anchor="middle" font-size="12" fill="#374151">Cache</text>'
                        '<text x="250" y="78" text-anchor="middle" font-size="11" fill="#6b7280">HIT → return</text>'
                        '<path d="M300 65 L370 65" stroke="#374151" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#ax2)"/>'
                        '<text x="335" y="58" text-anchor="middle" font-size="10" fill="#dc2626">MISS</text>'
                        '<rect x="370" y="40" width="110" height="50" rx="6" fill="#f59e0b" opacity=".15" stroke="#f59e0b"/>'
                        '<text x="425" y="62" text-anchor="middle" font-size="12" fill="#374151">Источник</text>'
                        '<text x="425" y="78" text-anchor="middle" font-size="11" fill="#6b7280">(БД/API)</text>'
                        '<path d="M425 90 L425 160 L250 160 L250 90" stroke="#10b981" stroke-width="1.5" fill="none" stroke-dasharray="4,3"/>'
                        '<text x="337" y="150" text-anchor="middle" font-size="10" fill="#10b981">сохранить в кэш</text>'
                        '<defs><marker id="ax" markerWidth="7" markerHeight="7" refX="5" refY="2.5" orient="auto"><path d="M0,0 L7,2.5 L0,5 Z" fill="#374151"/></marker>'
                        '<marker id="ax2" markerWidth="7" markerHeight="7" refX="5" refY="2.5" orient="auto"><path d="M0,0 L7,2.5 L0,5 Z" fill="#374151"/></marker></defs>',
                        caption='Cache-Aside паттерн'
                    )
                    + '<h3>functools.lru_cache</h3>'
                    '<pre><code>from functools import lru_cache, cache\nimport time\n\n@lru_cache(maxsize=128)   # до 128 кэшированных результатов\ndef expensive_fibonacci(n: int) -> int:\n    if n < 2: return n\n    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2)\n\n# Без кэша fib(40) ≈ 1 секунда, с кэшем — мгновенно\nt0 = time.perf_counter()\nprint(expensive_fibonacci(40))\nprint(f"Первый вызов: {(time.perf_counter()-t0)*1000:.1f}мс")\n\nt0 = time.perf_counter()\nprint(expensive_fibonacci(40))\nprint(f"Повторный вызов: {(time.perf_counter()-t0)*1000:.3f}мс")\n\n# Статистика кэша\nprint(expensive_fibonacci.cache_info())\n# CacheInfo(hits=1, misses=41, maxsize=128, currsize=41)\n</code></pre>'
                    + '<h3>TTL-кэш (с временем жизни)</h3>'
                    '<pre><code>import time\nfrom functools import wraps\n\ndef ttl_cache(ttl_seconds=60):\n    """Декоратор: кэш с временем жизни."""\n    cache = {}\n    def decorator(func):\n        @wraps(func)\n        def wrapper(*args):\n            key = args\n            now = time.time()\n            if key in cache:\n                result, ts = cache[key]\n                if now - ts < ttl_seconds:\n                    return result   # из кэша\n            result = func(*args)\n            cache[key] = (result, now)\n            return result\n        wrapper.cache_clear = lambda: cache.clear()\n        return wrapper\n    return decorator\n\n@ttl_cache(ttl_seconds=5)\ndef get_stock_price(symbol: str) -> float:\n    # имитация запроса к API\n    import random\n    return random.uniform(100, 200)\n\nprint(get_stock_price("AAPL"))  # запрос\nprint(get_stock_price("AAPL"))  # из кэша (те же 5 сек)\ntime.sleep(6)\nprint(get_stock_price("AAPL"))  # новый запрос (TTL истёк)\n</code></pre>'
                    + table(
                        ['Стратегия инвалидации', 'Когда чистить кэш'],
                        [
                            ['TTL (Time-To-Live)', 'Каждые N секунд автоматически'],
                            ['Write-through', 'При каждой записи в источник'],
                            ['Event-driven', 'При событии изменения данных'],
                            ['Capacity-based (LRU)', 'Выбросить наименее используемый при переполнении'],
                        ],
                        'Стратегии инвалидации кэша'
                    )
                ),
                'code_example': (
                    'from functools import lru_cache\nimport time\n\n'
                    '# Сравнение: рекурсия без кэша vs с кэшем\n\n'
                    'def fib_slow(n):\n'
                    '    if n < 2: return n\n'
                    '    return fib_slow(n-1) + fib_slow(n-2)\n\n'
                    '@lru_cache(maxsize=None)\n'
                    'def fib_fast(n):\n'
                    '    if n < 2: return n\n'
                    '    return fib_fast(n-1) + fib_fast(n-2)\n\n'
                    '# Замеры\n'
                    'for n in [10, 20, 30, 35]:\n'
                    '    t0 = time.perf_counter()\n'
                    '    r1 = fib_slow(n)\n'
                    '    slow_ms = (time.perf_counter() - t0) * 1000\n\n'
                    '    t0 = time.perf_counter()\n'
                    '    r2 = fib_fast(n)\n'
                    '    fast_ms = (time.perf_counter() - t0) * 1000\n\n'
                    '    speedup = slow_ms / fast_ms if fast_ms > 0 else float("inf")\n'
                    '    print(f"fib({n:2d})={r1:8d}  slow={slow_ms:8.2f}ms  fast={fast_ms:.4f}ms  "\n'
                    '          f"speedup={speedup:.0f}x")\n'
                ),
            },
        ],
    },

    # ─── 54: Functional programming ──────────────────────────────────────────
    {
        'title': 'Функциональное программирование',
        'description': 'Чистые функции, иммутабельность, монады, функции высшего порядка.',
        'icon': 'fas fa-infinity',
        'order': 54,
        'lessons': [
            {
                'title': 'Чистые функции, композиция, каррирование',
                'order': 1,
                'estimated_minutes': 70,
                'content': (
                    '<h2>Принципы функционального программирования</h2>'
                    + table(
                        ['Принцип', 'Суть', 'Python-инструмент'],
                        [
                            ['Чистые функции', 'Нет побочных эффектов, результат зависит только от аргументов', 'Обычные функции'],
                            ['Иммутабельность', 'Данные не изменяются после создания', 'tuple, frozenset, namedtuple'],
                            ['Функции высшего порядка', 'Функции принимают/возвращают функции', 'map, filter, sorted, functools'],
                            ['Композиция', 'f(g(x)) — комбинирование функций', 'functools.reduce, pipe-паттерн'],
                            ['Каррирование', 'f(a,b) → f(a)(b)', 'functools.partial'],
                            ['Ленивые вычисления', 'Вычислять только когда нужно', 'generator, itertools'],
                        ],
                        'Концепции ФП'
                    )
                    + '<h3>Чистые функции vs с побочными эффектами</h3>'
                    '<pre><code># НЕЧИСТАЯ: зависит от внешнего состояния\ntax_rate = 0.2\ndef calculate_price(base):         # зависит от глобальной переменной\n    return base * (1 + tax_rate)\n\n# ЧИСТАЯ: результат = f(аргументы) всегда\ndef calculate_price_pure(base: float, tax_rate: float) -> float:\n    return base * (1 + tax_rate)\n\n# НЕЧИСТАЯ: изменяет переданный список\ndef add_item_impure(lst, item):\n    lst.append(item)    # изменяет оригинал!\n\n# ЧИСТАЯ: возвращает новый объект\ndef add_item_pure(lst: tuple, item) -> tuple:\n    return lst + (item,)\n</code></pre>'
                    + '<h3>Каррирование через partial</h3>'
                    '<pre><code>from functools import partial\n\ndef power(base, exp):\n    return base ** exp\n\nsquare = partial(power, exp=2)\ncube   = partial(power, exp=3)\n\nprint(list(map(square, [1,2,3,4,5])))  # [1,4,9,16,25]\nprint(list(map(cube,   [1,2,3,4,5])))  # [1,8,27,64,125]\n\n# Каррирование URL-builder\nimport urllib.parse\nbuild_url = partial(urllib.parse.urljoin, "https://api.example.com")\nprint(build_url("/users"))     # https://api.example.com/users\nprint(build_url("/products"))  # https://api.example.com/products\n</code></pre>'
                    + '<h3>Функциональные трубопроводы (pipe)</h3>'
                    '<pre><code>from functools import reduce\n\ndef pipe(*funcs):\n    """Применить функции слева направо: pipe(f, g, h)(x) = h(g(f(x)))"""\n    return lambda x: reduce(lambda v, f: f(v), funcs, x)\n\n# Пример: обработка текста\nprocess = pipe(\n    str.strip,\n    str.lower,\n    lambda s: s.replace("-", " "),\n    str.split,\n    sorted,\n    lambda words: " ".join(words)\n)\n\nresult = process("  Python-Programming  ")\nprint(result)  # "programming python"\n</code></pre>'
                    + tip('ФП-стиль удобен для ETL-пайплайнов (Extract-Transform-Load), обработки данных и написания тестируемого кода.')
                ),
                'code_example': (
                    'from functools import reduce, partial\n\n'
                    '# Функциональный конвейер обработки данных\n\n'
                    'students = [\n'
                    '    {"name": "Иванов", "grade": 85, "group": "А"},\n'
                    '    {"name": "Петров", "grade": 92, "group": "Б"},\n'
                    '    {"name": "Сидоров", "grade": 67, "group": "А"},\n'
                    '    {"name": "Козлов", "grade": 78, "group": "Б"},\n'
                    '    {"name": "Новиков", "grade": 55, "group": "А"},\n'
                    '    {"name": "Соколов", "grade": 95, "group": "Б"},\n'
                    ']\n\n'
                    '# ФП-подход: цепочка трансформаций\n'
                    'def pipeline(data, *transforms):\n'
                    '    return reduce(lambda d, f: f(d), transforms, data)\n\n'
                    'by_group = partial(filter, lambda s: s["group"] == "А")\n'
                    'passing = partial(filter, lambda s: s["grade"] >= 70)\n'
                    'get_names = partial(map, lambda s: f"{s[\'name\']} ({s[\'grade\']})")\n\n'
                    'result = list(pipeline(\n'
                    '    students,\n'
                    '    list,\n'
                    '    by_group,\n'
                    '    passing,\n'
                    '    get_names,\n'
                    '))\n\n'
                    'print("Сдавшие из группы А:")\n'
                    'for r in result:\n'
                    '    print(f"  {r}")\n\n'
                    '# Статистика через functools\n'
                    'grades = [s["grade"] for s in students]\n'
                    'total = reduce(lambda a, b: a + b, grades)\n'
                    'print(f"\\nСредний балл: {total/len(grades):.1f}")\n'
                ),
            },
        ],
    },

    # ─── 55: Metaclasses ─────────────────────────────────────────────────────
    {
        'title': 'Метаклассы и дескрипторы',
        'description': 'Как Python создаёт классы: type, метаклассы, дескрипторы протокола.',
        'icon': 'fas fa-microscope',
        'order': 55,
        'lessons': [
            {
                'title': 'type(), метаклассы, __init_subclass__',
                'order': 1,
                'estimated_minutes': 75,
                'content': (
                    '<h2>Как Python создаёт классы</h2>'
                    '<p>В Python <strong>всё является объектом</strong>, включая классы. '
                    'Класс класса — это метакласс. По умолчанию — <code>type</code>.</p>'
                    '<pre><code>class MyClass:\n    x = 42\n\n# Эквивалентно:\nMyClass = type("MyClass", (), {"x": 42})\n\nprint(type(MyClass))   # <class \'type\'>\nprint(type(42))        # <class \'int\'>\nprint(type(type))      # <class \'type\'> — type — метакласс самого себя\n</code></pre>'
                    + '<h3>Динамическое создание классов</h3>'
                    '<pre><code># type(name, bases, dict)\nAnimal = type("Animal", (), {\n    "sound": "...",\n    "speak": lambda self: f"Я {self.__class__.__name__}, говорю: {self.sound}"\n})\n\nDog = type("Dog", (Animal,), {"sound": "Гав"})\nCat = type("Cat", (Animal,), {"sound": "Мяу"})\n\nprint(Dog().speak())   # Я Dog, говорю: Гав\n</code></pre>'
                    + '<h3>Метакласс: контроль создания классов</h3>'
                    '<pre><code>class SingletonMeta(type):\n    """Метакласс Singleton — только один экземпляр."""\n    _instances = {}\n\n    def __call__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__call__(*args, **kwargs)\n        return cls._instances[cls]\n\nclass Database(metaclass=SingletonMeta):\n    def __init__(self):\n        self.connection = "postgres://localhost/mydb"\n\ndb1 = Database()\ndb2 = Database()\nprint(db1 is db2)   # True — один объект!\n</code></pre>'
                    + '<h3>__init_subclass__ — более простая альтернатива</h3>'
                    '<pre><code>class PluginBase:\n    registry = {}\n\n    def __init_subclass__(cls, plugin_name=None, **kwargs):\n        super().__init_subclass__(**kwargs)\n        if plugin_name:\n            PluginBase.registry[plugin_name] = cls\n\nclass CSVPlugin(PluginBase, plugin_name="csv"):\n    def process(self, data): return data.split(",")\n\nclass JSONPlugin(PluginBase, plugin_name="json"):\n    def process(self, data):\n        import json; return json.loads(data)\n\nprint(PluginBase.registry)  # {"csv": CSVPlugin, "json": JSONPlugin}\n</code></pre>'
                    + '<h3>Дескрипторы — как работают @property</h3>'
                    '<pre><code>class Validated:\n    """Дескриптор: число в заданном диапазоне."""\n    def __init__(self, min_val, max_val):\n        self.min_val = min_val\n        self.max_val = max_val\n        self.name = None\n\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, objtype=None):\n        if obj is None: return self\n        return getattr(obj, f"_{self.name}", None)\n\n    def __set__(self, obj, value):\n        if not (self.min_val <= value <= self.max_val):\n            raise ValueError(f"{self.name} должен быть от {self.min_val} до {self.max_val}")\n        setattr(obj, f"_{self.name}", value)\n\nclass Student:\n    age   = Validated(0, 120)\n    grade = Validated(0, 100)\n\n    def __init__(self, name, age, grade):\n        self.name  = name\n        self.age   = age\n        self.grade = grade\n\ns = Student("Иван", 20, 85)\nprint(s.grade)     # 85\ns.grade = 105      # ValueError!\n</code></pre>'
                    + tip('Метаклассы — это мощный инструмент, но используйте `__init_subclass__` или декораторы классов — они проще и понятнее.')
                ),
                'code_example': (
                    '# Реестр стратегий через __init_subclass__\n\n'
                    'class Sorter:\n'
                    '    """Базовый класс алгоритмов сортировки."""\n'
                    '    registry = {}\n\n'
                    '    def __init_subclass__(cls, name=None, **kwargs):\n'
                    '        super().__init_subclass__(**kwargs)\n'
                    '        if name:\n'
                    '            Sorter.registry[name] = cls\n\n'
                    '    def sort(self, data: list) -> list:\n'
                    '        raise NotImplementedError\n\n'
                    'class BubbleSorter(Sorter, name="bubble"):\n'
                    '    def sort(self, data):\n'
                    '        data = data[:]\n'
                    '        n = len(data)\n'
                    '        for i in range(n):\n'
                    '            for j in range(n - i - 1):\n'
                    '                if data[j] > data[j+1]:\n'
                    '                    data[j], data[j+1] = data[j+1], data[j]\n'
                    '        return data\n\n'
                    'class QuickSorter(Sorter, name="quick"):\n'
                    '    def sort(self, data):\n'
                    '        if len(data) <= 1:\n'
                    '            return data\n'
                    '        pivot = data[len(data)//2]\n'
                    '        left  = [x for x in data if x < pivot]\n'
                    '        mid   = [x for x in data if x == pivot]\n'
                    '        right = [x for x in data if x > pivot]\n'
                    '        return self.sort(left) + mid + self.sort(right)\n\n'
                    'data = [64, 25, 12, 22, 11]\n'
                    'print("Доступные алгоритмы:", list(Sorter.registry.keys()))\n'
                    'for name, cls in Sorter.registry.items():\n'
                    '    print(f"  {name}: {cls().sort(data)}")\n'
                ),
            },
        ],
    },

    # ─── 56: Security & hashing ──────────────────────────────────────────────
    {
        'title': 'Безопасность: хэши, шифрование, secrets',
        'description': 'hashlib, hmac, secrets, bcrypt — безопасная работа с паролями и данными.',
        'icon': 'fas fa-shield-alt',
        'order': 56,
        'lessons': [
            {
                'title': 'hashlib, HMAC, bcrypt, secrets',
                'order': 1,
                'estimated_minutes': 65,
                'content': (
                    '<h2>Хэш-функции в Python</h2>'
                    + table(
                        ['Алгоритм', 'Длина хэша', 'Назначение'],
                        [
                            ['MD5', '128 бит / 32 hex', 'Проверка целостности файлов (НЕ для паролей!)'],
                            ['SHA-1', '160 бит / 40 hex', 'Устарел, небезопасен'],
                            ['SHA-256', '256 бит / 64 hex', 'Цифровые подписи, цепочки блоков'],
                            ['SHA-3', '256/512 бит', 'Современный стандарт NIST'],
                            ['bcrypt', 'фиксированный', 'Хэширование паролей (slow-hash)'],
                            ['PBKDF2', 'настраиваемый', 'Деривация ключей из паролей'],
                        ],
                        'Алгоритмы хэширования'
                    )
                    + '<h3>hashlib — базовые хэши</h3>'
                    '<pre><code>import hashlib\n\n# SHA-256 строки\ntext = "Привет, мир!"\nhash_hex = hashlib.sha256(text.encode("utf-8")).hexdigest()\nprint(f"SHA-256: {hash_hex}")\n\n# Хэш файла (поблочно, для больших файлов)\ndef file_hash(path: str, algo="sha256") -> str:\n    h = hashlib.new(algo)\n    with open(path, "rb") as f:\n        for chunk in iter(lambda: f.read(65536), b""):\n            h.update(chunk)\n    return h.hexdigest()\n</code></pre>'
                    + '<h3>HMAC — аутентификация сообщений</h3>'
                    '<pre><code>import hmac\nimport hashlib\n\ndef sign(message: bytes, secret: bytes) -> str:\n    return hmac.new(secret, message, hashlib.sha256).hexdigest()\n\ndef verify(message: bytes, signature: str, secret: bytes) -> bool:\n    expected = sign(message, secret)\n    return hmac.compare_digest(expected, signature)  # защита от timing attacks!\n\nsecret = b"super_secret_key"\nmsg = b"user_id=42&action=delete"\nsig = sign(msg, secret)\nprint("Верно:", verify(msg, sig, secret))          # True\nprint("Подделка:", verify(msg + b"!", sig, secret)) # False\n</code></pre>'
                    + '<h3>secrets — криптостойкие случайные данные</h3>'
                    '<pre><code>import secrets\nimport string\n\n# Безопасный токен (для сессий, API-ключей)\ntoken = secrets.token_hex(32)      # 64-символьная hex-строка\ntoken_url = secrets.token_urlsafe(16)  # base64url-безопасный\n\n# Безопасный пароль\nalphabet = string.ascii_letters + string.digits + "!@#$%"\npassword = "".join(secrets.choice(alphabet) for _ in range(16))\n\nprint(f"Token: {token}")\nprint(f"Password: {password}")\n</code></pre>'
                    + warn('Никогда не используйте `random` для паролей, токенов, ключей — он не криптостойкий. Используйте `secrets`.')
                    + '<h3>Хэширование паролей правильно</h3>'
                    '<pre><code>import hashlib, os\n\ndef hash_password(password: str) -> str:\n    """PBKDF2 с солью — правильный способ хранить пароли."""\n    salt = os.urandom(32)        # случайная соль\n    key = hashlib.pbkdf2_hmac(\n        "sha256",\n        password.encode("utf-8"),\n        salt,\n        iterations=600_000       # рекомендация NIST 2023\n    )\n    return salt.hex() + ":" + key.hex()\n\ndef verify_password(password: str, stored: str) -> bool:\n    salt_hex, key_hex = stored.split(":")\n    salt = bytes.fromhex(salt_hex)\n    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)\n    return hmac.compare_digest(key.hex(), key_hex)\n</code></pre>'
                ),
                'code_example': (
                    'import hashlib\nimport hmac\nimport secrets\n\n'
                    '# Система аутентификации на основе токенов\n\n'
                    'class TokenAuth:\n'
                    '    def __init__(self, secret_key: str):\n'
                    '        self.secret = secret_key.encode()\n'
                    '        self.tokens = {}  # token -> user_id\n\n'
                    '    def create_token(self, user_id: int) -> str:\n'
                    '        """Создать подписанный токен."""\n'
                    '        raw = secrets.token_hex(16)\n'
                    '        payload = f"{user_id}:{raw}"\n'
                    '        sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()\n'
                    '        token = f"{payload}:{sig}"\n'
                    '        self.tokens[token] = user_id\n'
                    '        return token\n\n'
                    '    def validate(self, token: str):\n'
                    '        """Вернуть user_id если токен валидный, иначе None."""\n'
                    '        try:\n'
                    '            parts = token.rsplit(":", 1)\n'
                    '            payload, sig = parts[0], parts[1]\n'
                    '            expected = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()\n'
                    '            if not hmac.compare_digest(expected, sig):\n'
                    '                return None\n'
                    '            return self.tokens.get(token)\n'
                    '        except Exception:\n'
                    '            return None\n\n'
                    'auth = TokenAuth("my_django_secret_key")\n'
                    'token = auth.create_token(42)\n'
                    'print(f"Токен: {token[:40]}...")\n'
                    'print(f"Валидный: {auth.validate(token)}")\n'
                    'print(f"Поддельный: {auth.validate(token + "x")}")\n'
                ),
            },
        ],
    },

    # ─── 57: Clean Architecture ──────────────────────────────────────────────
    {
        'title': 'Архитектура приложений: Clean Architecture',
        'description': 'Слоистая архитектура, Hexagonal Architecture, разделение бизнес-логики.',
        'icon': 'fas fa-layer-group',
        'order': 57,
        'lessons': [
            {
                'title': 'Слои, Use Cases, Repository паттерн',
                'order': 1,
                'estimated_minutes': 70,
                'content': (
                    '<h2>Проблема: всё в одном файле</h2>'
                    '<p>В маленьких проектах логика в views/controllers выглядит нормально. '
                    'При росте проекта это приводит к <strong>запутанному, нетестируемому коду</strong>.</p>'
                    + diagram(
                        '<circle cx="295" cy="130" r="110" fill="none" stroke="#e5e7eb" stroke-width="2"/>'
                        '<circle cx="295" cy="130" r="80" fill="none" stroke="#e5e7eb" stroke-width="2"/>'
                        '<circle cx="295" cy="130" r="50" fill="none" stroke="#e5e7eb" stroke-width="2"/>'
                        '<circle cx="295" cy="130" r="22" fill="#7c3aed" opacity=".3" stroke="#7c3aed"/>'
                        '<text x="295" y="134" text-anchor="middle" font-size="10" font-weight="600" fill="#7c3aed">Entities</text>'
                        '<text x="295" y="92" text-anchor="middle" font-size="11" fill="#3b82f6">Use Cases</text>'
                        '<text x="295" y="58" text-anchor="middle" font-size="11" fill="#10b981">Interface Adapters</text>'
                        '<text x="295" y="26" text-anchor="middle" font-size="11" fill="#6b7280">Frameworks &amp; Drivers</text>'
                        '<path d="M420 130 L500 130" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="3,3"/>'
                        '<text x="510" y="110" font-size="11" fill="#374151">DB, Web,</text>'
                        '<text x="510" y="124" font-size="11" fill="#374151">UI, API</text>'
                        '<text x="510" y="143" font-size="10" fill="#6b7280">зависят от →</text>'
                        '<text x="510" y="157" font-size="10" fill="#6b7280">бизнес-логики</text>',
                        caption='Чистая архитектура: зависимости направлены внутрь'
                    )
                    + '<h3>Слои Clean Architecture</h3>'
                    + table(
                        ['Слой', 'Что содержит', 'Зависит от'],
                        [
                            ['Entities', 'Бизнес-объекты, правила', 'Ничего'],
                            ['Use Cases', 'Бизнес-логика, операции', 'Только Entities'],
                            ['Interface Adapters', 'Контроллеры, Presenters, Gateways', 'Use Cases'],
                            ['Frameworks', 'Django, FastAPI, SQLAlchemy', 'Все слои'],
                        ],
                        'Слои и их зависимости'
                    )
                    + '<h3>Пример на Python</h3>'
                    '<pre><code>from dataclasses import dataclass\nfrom abc import ABC, abstractmethod\nfrom typing import Optional, List\n\n# --- ENTITIES ---\n@dataclass\nclass User:\n    id: int\n    email: str\n    name: str\n\n# --- INTERFACES (порты) ---\nclass UserRepository(ABC):\n    @abstractmethod\n    def find_by_email(self, email: str) -> Optional[User]: ...\n    @abstractmethod\n    def save(self, user: User) -> User: ...\n    @abstractmethod\n    def all(self) -> List[User]: ...\n\n# --- USE CASES ---\nclass RegisterUser:\n    def __init__(self, repo: UserRepository):\n        self.repo = repo\n\n    def execute(self, email: str, name: str) -> User:\n        if self.repo.find_by_email(email):\n            raise ValueError(f"Email {email!r} уже зарегистрирован")\n        user = User(id=0, email=email, name=name)\n        return self.repo.save(user)\n\n# --- ADAPTER (in-memory реализация) ---\nclass InMemoryUserRepo(UserRepository):\n    def __init__(self):\n        self._users: dict[str, User] = {}\n        self._counter = 0\n\n    def find_by_email(self, email):\n        return self._users.get(email)\n\n    def save(self, user):\n        self._counter += 1\n        user.id = self._counter\n        self._users[user.email] = user\n        return user\n\n    def all(self):\n        return list(self._users.values())\n\n# --- MAIN ---\nrepo = InMemoryUserRepo()\nuse_case = RegisterUser(repo)\nu = use_case.execute("ivan@example.com", "Иван")\nprint(u)   # User(id=1, email=\'ivan@example.com\', name=\'Иван\')\n</code></pre>'
                    + tip('Главная польза: бизнес-логика (Use Cases) тестируется без Django, без БД, без HTTP — только Python-объекты.')
                ),
                'code_example': (
                    'from dataclasses import dataclass, field\n'
                    'from abc import ABC, abstractmethod\n'
                    'from typing import Optional, List\n\n'
                    '# Чистая архитектура: система библиотеки\n\n'
                    '@dataclass\n'
                    'class Book:\n'
                    '    id: int\n'
                    '    title: str\n'
                    '    author: str\n'
                    '    available: bool = True\n\n'
                    'class BookRepository(ABC):\n'
                    '    @abstractmethod\n'
                    '    def find(self, book_id: int) -> Optional[Book]: ...\n'
                    '    @abstractmethod\n'
                    '    def save(self, book: Book) -> None: ...\n'
                    '    @abstractmethod\n'
                    '    def available_books(self) -> List[Book]: ...\n\n'
                    'class BorrowBook:\n'
                    '    """Use Case: взять книгу."""\n'
                    '    def __init__(self, repo: BookRepository):\n'
                    '        self.repo = repo\n\n'
                    '    def execute(self, book_id: int, user: str) -> str:\n'
                    '        book = self.repo.find(book_id)\n'
                    '        if not book:\n'
                    '            raise ValueError("Книга не найдена")\n'
                    '        if not book.available:\n'
                    '            raise ValueError(f"{book.title!r} уже взята")\n'
                    '        book.available = False\n'
                    '        self.repo.save(book)\n'
                    '        return f"{user} взял {book.title!r}"\n\n'
                    'class InMemoryBookRepo(BookRepository):\n'
                    '    def __init__(self, books):\n'
                    '        self._books = {b.id: b for b in books}\n'
                    '    def find(self, book_id): return self._books.get(book_id)\n'
                    '    def save(self, book): self._books[book.id] = book\n'
                    '    def available_books(self): return [b for b in self._books.values() if b.available]\n\n'
                    'repo = InMemoryBookRepo([\n'
                    '    Book(1, "Чистый код", "Мартин"),\n'
                    '    Book(2, "Паттерны", "Банда четырёх"),\n'
                    '])\n'
                    'uc = BorrowBook(repo)\n'
                    'print(uc.execute(1, "Иванов"))\n'
                    'print([b.title for b in repo.available_books()])\n'
                ),
            },
        ],
    },

    # ─── 58: Generators advanced ─────────────────────────────────────────────
    {
        'title': 'Генераторы и итераторы: продвинутый уровень',
        'description': 'send(), throw(), yield from, coroutine-пайплайны, бесконечные последовательности.',
        'icon': 'fas fa-stream',
        'order': 58,
        'lessons': [
            {
                'title': 'send(), yield from, генераторные пайплайны',
                'order': 1,
                'estimated_minutes': 70,
                'content': (
                    '<h2>Генераторы как двунаправленные каналы</h2>'
                    '<p>Генератор можно использовать не только для получения данных, '
                    'но и для <strong>отправки</strong> данных через <code>send()</code>.</p>'
                    '<pre><code>def accumulator():\n    """Накапливает суммы, отвечает текущим итогом."""\n    total = 0\n    while True:\n        value = yield total   # yield возвращает total, receive — value\n        if value is None: break\n        total += value\n\nacc = accumulator()\nnext(acc)               # запускаем генератор до первого yield\nprint(acc.send(10))     # 10\nprint(acc.send(20))     # 30\nprint(acc.send(5))      # 35\n</code></pre>'
                    + '<h3>yield from — делегирование</h3>'
                    '<pre><code>def inner_gen():\n    yield 1\n    yield 2\n    yield 3\n\ndef outer_gen():\n    yield 0\n    yield from inner_gen()   # делегируем в inner_gen\n    yield 4\n\nprint(list(outer_gen()))   # [0, 1, 2, 3, 4]\n\n# Практический пример: обход дерева\ndef traverse(node):\n    if node is None: return\n    yield node["value"]\n    yield from traverse(node.get("left"))\n    yield from traverse(node.get("right"))\n\ntree = {"value": 1,\n        "left": {"value": 2, "left": {"value": 4, "left": None, "right": None},\n                              "right": {"value": 5, "left": None, "right": None}},\n        "right": {"value": 3, "left": None, "right": None}}\n\nprint(list(traverse(tree)))   # [1, 2, 4, 5, 3] — preorder\n</code></pre>'
                    + '<h3>Генераторные пайплайны (ленивая обработка)</h3>'
                    '<pre><code>def read_lines(filename):\n    with open(filename, encoding="utf-8") as f:\n        yield from f\n\ndef parse_numbers(lines):\n    for line in lines:\n        line = line.strip()\n        if line and not line.startswith("#"):\n            try: yield int(line)\n            except ValueError: pass\n\ndef filter_large(numbers, threshold=100):\n    for n in numbers:\n        if n > threshold:\n            yield n\n\ndef square(numbers):\n    for n in numbers:\n        yield n ** 2\n\n# Конвейер — обрабатывает файл построчно без загрузки в память!\npipeline = square(filter_large(parse_numbers(read_lines("numbers.txt"))))\nresult = list(pipeline)\n</code></pre>'
                    + tip('Генераторные пайплайны работают с данными любого размера, используя O(1) памяти — только одна строка в памяти в любой момент.')
                    + '<h3>itertools для бесконечных генераторов</h3>'
                    '<pre><code>import itertools\n\n# Фибоначчи бесконечная последовательность\ndef fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\n# Первые 10 чётных чисел Фибоначчи > 100\nresult = list(itertools.islice(\n    filter(lambda x: x % 2 == 0,\n           filter(lambda x: x > 100, fibonacci())),\n    10\n))\nprint(result)\n</code></pre>'
                ),
                'code_example': (
                    '# Бесконечный генератор простых чисел + пайплайн\n\n'
                    'def primes():\n'
                    '    """Бесконечный генератор простых чисел (решето Эратосфена-стрим)."""\n'
                    '    yield 2\n'
                    '    found = [2]\n'
                    '    candidate = 3\n'
                    '    while True:\n'
                    '        if all(candidate % p != 0 for p in found if p * p <= candidate):\n'
                    '            found.append(candidate)\n'
                    '            yield candidate\n'
                    '        candidate += 2\n\n'
                    'def take(n, gen):\n'
                    '    """Взять первые n элементов генератора."""\n'
                    '    for _, val in zip(range(n), gen):\n'
                    '        yield val\n\n'
                    'def window(gen, size=2):\n'
                    '    """Скользящее окно по генератору."""\n'
                    '    from collections import deque\n'
                    '    buf = deque(maxlen=size)\n'
                    '    for val in gen:\n'
                    '        buf.append(val)\n'
                    '        if len(buf) == size:\n'
                    '            yield tuple(buf)\n\n'
                    '# Пример: найти первые 5 пар простых-близнецов (p, p+2)\n'
                    'twin_primes = (\n'
                    '    (a, b) for a, b in window(primes())\n'
                    '    if b - a == 2\n'
                    ')\n\n'
                    'print("Первые 8 простых-близнецов:")\n'
                    'for pair in take(8, twin_primes):\n'
                    '    print(f"  {pair}")\n'
                ),
            },
        ],
    },

    # ─── 59: concurrency queues ──────────────────────────────────────────────
    {
        'title': 'Очереди задач и параллелизм',
        'description': 'queue.Queue, multiprocessing.Pool, concurrent.futures, паттерн Producer-Consumer.',
        'icon': 'fas fa-tasks',
        'order': 59,
        'lessons': [
            {
                'title': 'Producer-Consumer, ThreadPool, ProcessPool',
                'order': 1,
                'estimated_minutes': 65,
                'content': (
                    '<h2>Паттерн Producer-Consumer</h2>'
                    + diagram(
                        '<rect x="10" y="80" width="120" height="50" rx="6" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>'
                        '<text x="70" y="108" text-anchor="middle" font-size="12" font-weight="600" fill="#7c3aed">Producer</text>'
                        '<path d="M130 105 L210 105" stroke="#7c3aed" stroke-width="2" marker-end="url(#ap)"/>'
                        '<rect x="210" y="70" width="120" height="70" rx="6" fill="#f59e0b" opacity=".15" stroke="#f59e0b"/>'
                        '<text x="270" y="100" text-anchor="middle" font-size="12" font-weight="600" fill="#b45309">Queue</text>'
                        '<text x="270" y="118" text-anchor="middle" font-size="11" fill="#6b7280">task task task</text>'
                        '<path d="M330 105 L410 90" stroke="#374151" stroke-width="1.5" marker-end="url(#ap2)"/>'
                        '<path d="M330 105 L410 115" stroke="#374151" stroke-width="1.5" marker-end="url(#ap2)"/>'
                        '<rect x="410" y="60" width="100" height="40" rx="6" fill="#10b981" opacity=".15" stroke="#10b981"/>'
                        '<text x="460" y="83" text-anchor="middle" font-size="11" fill="#374151">Worker-1</text>'
                        '<rect x="410" y="110" width="100" height="40" rx="6" fill="#10b981" opacity=".15" stroke="#10b981"/>'
                        '<text x="460" y="133" text-anchor="middle" font-size="11" fill="#374151">Worker-2</text>'
                        '<defs><marker id="ap" markerWidth="7" markerHeight="7" refX="5" refY="2.5" orient="auto"><path d="M0,0 L7,2.5 L0,5 Z" fill="#7c3aed"/></marker>'
                        '<marker id="ap2" markerWidth="7" markerHeight="7" refX="5" refY="2.5" orient="auto"><path d="M0,0 L7,2.5 L0,5 Z" fill="#374151"/></marker></defs>',
                        caption='Producer-Consumer с очередью задач'
                    )
                    + '<h3>queue.Queue — потокобезопасная очередь</h3>'
                    '<pre><code>import queue\nimport threading\nimport time\nimport random\n\ndef producer(q: queue.Queue, n: int):\n    for i in range(n):\n        task = {"id": i, "data": random.randint(1, 100)}\n        q.put(task)\n        print(f"Producer: задача {i}")\n        time.sleep(0.1)\n    q.put(None)  # сигнал завершения\n\ndef consumer(q: queue.Queue, name: str):\n    while True:\n        task = q.get(timeout=5)\n        if task is None:\n            q.put(None)  # передаём сигнал другим воркерам\n            break\n        result = task["data"] ** 2\n        print(f"{name}: обработал {task[\'id\']} → {result}")\n        q.task_done()\n        time.sleep(0.2)\n\ntask_queue = queue.Queue(maxsize=10)\nthreads = [\n    threading.Thread(target=producer, args=(task_queue, 5)),\n    threading.Thread(target=consumer, args=(task_queue, "Worker-1")),\n    threading.Thread(target=consumer, args=(task_queue, "Worker-2")),\n]\nfor t in threads: t.start()\nfor t in threads: t.join()\n</code></pre>'
                    + '<h3>concurrent.futures — высокоуровневый API</h3>'
                    '<pre><code>from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed\n\ndef cpu_task(n):\n    """CPU-интенсивная задача."""\n    return sum(i*i for i in range(n))\n\ndef io_task(url):\n    """I/O задача — запрос к API."""\n    import time; time.sleep(0.5)\n    return f"data:{url}"\n\n# ThreadPool для I/O задач\nwith ThreadPoolExecutor(max_workers=4) as pool:\n    futures = {pool.submit(io_task, f"url{i}"): i for i in range(8)}\n    for future in as_completed(futures):\n        print(f"Готово: {future.result()}")\n\n# ProcessPool для CPU задач (обходит GIL)\nwith ProcessPoolExecutor(max_workers=4) as pool:\n    results = list(pool.map(cpu_task, [10**6, 2*10**6, 3*10**6]))\n    print(results)\n</code></pre>'
                    + table(
                        ['Тип задачи', 'Рекомендация', 'Почему'],
                        [
                            ['I/O-bound (сеть, файлы)', 'ThreadPoolExecutor или asyncio', 'GIL освобождается при I/O'],
                            ['CPU-bound (вычисления)', 'ProcessPoolExecutor', 'Каждый процесс имеет свой GIL'],
                            ['Много лёгких задач', 'asyncio.gather()', 'Минимальный overhead'],
                        ],
                        'Когда что использовать'
                    )
                ),
                'code_example': (
                    'from concurrent.futures import ThreadPoolExecutor, as_completed\n'
                    'import time\nimport random\n\n'
                    '# Параллельная проверка "доступности серверов"\n\n'
                    'def check_server(host: str) -> dict:\n'
                    '    """Имитация пинга сервера."""\n'
                    '    delay = random.uniform(0.1, 1.0)\n'
                    '    time.sleep(delay)  # I/O операция\n'
                    '    is_up = random.random() > 0.2  # 80% серверов отвечают\n'
                    '    return {\n'
                    '        "host": host,\n'
                    '        "status": "UP" if is_up else "DOWN",\n'
                    '        "latency_ms": int(delay * 1000)\n'
                    '    }\n\n'
                    'servers = [\n'
                    '    "web-01.example.com",\n'
                    '    "web-02.example.com",\n'
                    '    "db-01.example.com",\n'
                    '    "cache-01.example.com",\n'
                    '    "api-01.example.com",\n'
                    ']\n\n'
                    'start = time.perf_counter()\n\n'
                    'with ThreadPoolExecutor(max_workers=5) as pool:\n'
                    '    futures = {pool.submit(check_server, s): s for s in servers}\n'
                    '    results = []\n'
                    '    for future in as_completed(futures):\n'
                    '        results.append(future.result())\n\n'
                    'elapsed = time.perf_counter() - start\n'
                    'results.sort(key=lambda x: x["latency_ms"])\n\n'
                    'print(f"Проверено {len(servers)} серверов за {elapsed:.2f}с:")\n'
                    'for r in results:\n'
                    '    icon = "OK" if r["status"] == "UP" else "!"\n'
                    '    print(f"  [{icon}] {r[\'host\']:30s} {r[\'status\']:5s} {r[\'latency_ms\']}мс")\n'
                ),
            },
        ],
    },

    # ─── 60: Final project guide ─────────────────────────────────────────────
    {
        'title': 'Финальный проект: от идеи до деплоя',
        'description': 'Структура учебного Python-проекта, чеклист разработчика, советы по код-ревью.',
        'icon': 'fas fa-rocket',
        'order': 60,
        'lessons': [
            {
                'title': 'Чеклист проекта: структура, тесты, документация',
                'order': 1,
                'estimated_minutes': 60,
                'content': (
                    '<h2>Жизненный цикл Python-проекта</h2>'
                    + diagram(
                        '<rect x="10" y="30" width="100" height="45" rx="6" fill="#7c3aed" opacity=".2" stroke="#7c3aed"/>'
                        '<text x="60" y="55" text-anchor="middle" font-size="11" font-weight="600" fill="#7c3aed">Идея</text>'
                        '<path d="M110 52 L150 52" stroke="#374151" stroke-width="1.5" marker-end="url(#fa)"/>'
                        '<rect x="150" y="30" width="100" height="45" rx="6" fill="#3b82f6" opacity=".2" stroke="#3b82f6"/>'
                        '<text x="200" y="55" text-anchor="middle" font-size="11" font-weight="600" fill="#3b82f6">Дизайн</text>'
                        '<path d="M250 52 L290 52" stroke="#374151" stroke-width="1.5" marker-end="url(#fa)"/>'
                        '<rect x="290" y="30" width="100" height="45" rx="6" fill="#10b981" opacity=".2" stroke="#10b981"/>'
                        '<text x="340" y="55" text-anchor="middle" font-size="11" font-weight="600" fill="#10b981">Разработка</text>'
                        '<path d="M390 52 L430 52" stroke="#374151" stroke-width="1.5" marker-end="url(#fa)"/>'
                        '<rect x="430" y="30" width="80" height="45" rx="6" fill="#f59e0b" opacity=".2" stroke="#f59e0b"/>'
                        '<text x="470" y="55" text-anchor="middle" font-size="11" font-weight="600" fill="#b45309">Тесты</text>'
                        '<path d="M510 52 L550 52" stroke="#374151" stroke-width="1.5" marker-end="url(#fa)"/>'
                        '<rect x="550" y="30" width="45" height="45" rx="6" fill="#ef4444" opacity=".2" stroke="#ef4444"/>'
                        '<text x="572" y="55" text-anchor="middle" font-size="11" font-weight="600" fill="#ef4444">Deploy</text>'
                        '<path d="M572 75 Q572 160 340 160 Q108 160 108 75" stroke="#6b7280" stroke-width="1" fill="none" stroke-dasharray="4,3" marker-end="url(#fa)"/>'
                        '<text x="340" y="185" text-anchor="middle" font-size="11" fill="#6b7280">итеративно</text>'
                        '<defs><marker id="fa" markerWidth="7" markerHeight="7" refX="5" refY="2.5" orient="auto"><path d="M0,0 L7,2.5 L0,5 Z" fill="#374151"/></marker></defs>',
                        caption='Жизненный цикл разработки'
                    )
                    + '<h3>Чеклист Python-проекта</h3>'
                    + table(
                        ['Категория', 'Пункт', 'Инструмент'],
                        [
                            ['Структура', 'src/ layout + __init__.py', 'hatchling / setuptools'],
                            ['Зависимости', 'pyproject.toml или requirements.txt', 'pip / poetry'],
                            ['Форматирование', 'Единый стиль кода', 'black, ruff'],
                            ['Линтинг', 'Нет синтаксических ошибок', 'ruff, flake8, pylint'],
                            ['Type hints', 'Аннотации типов', 'mypy, pyright'],
                            ['Тесты', 'Покрытие > 80%', 'pytest, coverage'],
                            ['Документация', 'Docstrings для публичного API', 'Sphinx, pdoc'],
                            ['Безопасность', 'Нет секретов в коде', '.env + python-dotenv'],
                            ['CI/CD', 'Автоматические проверки', 'GitHub Actions'],
                            ['README', 'Установка + примеры', 'Markdown'],
                        ],
                        'Чеклист Python-проекта'
                    )
                    + '<h3>Структура хорошего проекта</h3>'
                    '<pre><code>myproject/\n├── src/\n│   └── myproject/\n│       ├── __init__.py\n│       ├── models.py       # Entities\n│       ├── services.py     # Use Cases / Business Logic\n│       ├── repositories.py # Data Access\n│       └── api.py          # Controllers\n├── tests/\n│   ├── conftest.py         # Fixtures\n│   ├── test_models.py\n│   ├── test_services.py\n│   └── test_api.py\n├── docs/\n├── pyproject.toml\n├── .env.example\n├── .gitignore\n└── README.md\n</code></pre>'
                    + '<h3>Советы по код-ревью</h3>'
                    '<ul>'
                    '<li><strong>Имена переменных</strong> — понятные, без сокращений вроде <code>x, tmp, d</code></li>'
                    '<li><strong>Функции</strong> — делают одно дело, не длиннее 20–30 строк</li>'
                    '<li><strong>Комментарии</strong> — объясняют <em>почему</em>, а не <em>что</em></li>'
                    '<li><strong>Magic numbers</strong> — заменяй константами: <code>MAX_RETRY = 3</code></li>'
                    '<li><strong>Error handling</strong> — перехватывай конкретные исключения</li>'
                    '<li><strong>DRY</strong> — Don\'t Repeat Yourself, но не оверинжиниринг</li>'
                    '</ul>'
                    + tip('Начни с рабочего кода, потом рефакторинг. "Make it work, make it right, make it fast" — Kent Beck.')
                ),
                'code_example': (
                    '# Шаблон Python-проекта: конфигурация через .env\n\n'
                    'import os\nfrom dataclasses import dataclass\n\n'
                    '@dataclass\n'
                    'class Config:\n'
                    '    """Конфигурация приложения из переменных окружения."""\n'
                    '    debug: bool\n'
                    '    database_url: str\n'
                    '    secret_key: str\n'
                    '    max_workers: int\n'
                    '    log_level: str\n\n'
                    '    @classmethod\n'
                    '    def from_env(cls) -> "Config":\n'
                    '        """Загрузить конфиг из переменных окружения."""\n'
                    '        return cls(\n'
                    '            debug=os.getenv("DEBUG", "false").lower() == "true",\n'
                    '            database_url=os.getenv("DATABASE_URL", "sqlite:///app.db"),\n'
                    '            secret_key=os.getenv("SECRET_KEY", "dev-secret-change-me"),\n'
                    '            max_workers=int(os.getenv("MAX_WORKERS", "4")),\n'
                    '            log_level=os.getenv("LOG_LEVEL", "INFO"),\n'
                    '        )\n\n'
                    '    def validate(self) -> None:\n'
                    '        """Проверить обязательные поля."""\n'
                    '        if self.secret_key == "dev-secret-change-me" and not self.debug:\n'
                    '            raise ValueError("Установите SECRET_KEY перед запуском в production!")\n'
                    '        if self.max_workers < 1 or self.max_workers > 32:\n'
                    '            raise ValueError("MAX_WORKERS должен быть от 1 до 32")\n\n'
                    '# Демонстрация\n'
                    'cfg = Config.from_env()\n'
                    'print(f"Debug: {cfg.debug}")\n'
                    'print(f"DB: {cfg.database_url}")\n'
                    'print(f"Workers: {cfg.max_workers}")\n'
                    'print(f"Log level: {cfg.log_level}")\n\n'
                    'try:\n'
                    '    cfg.validate()\n'
                    '    print("Конфиг валиден")\n'
                    'except ValueError as e:\n'
                    '    print(f"Предупреждение: {e}")\n'
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed theory modules 51-60'

    def handle(self, *args, **options):
        try:
            subject = Subject.objects.get(slug='python')
        except Subject.DoesNotExist:
            self.stdout.write(self.style.ERROR('Subject python not found'))
            return

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
            total_modules += 1

            for lesson_data in mod_data['lessons']:
                TheoryLesson.objects.update_or_create(
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
            f'seed_theory_advanced3: {total_modules} modules, {total_lessons} lessons'
        ))
