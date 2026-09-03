"""
seed_theory_advanced2 — Modules 41–50
Topics: web scraping, packaging, logging, profiling, network sockets,
databases (SQLAlchemy), pandas, NumPy, Jupyter/data tools, advanced OOP.
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
    cap = f'<p style="text-align:center;font-size:.85rem;color:#6b7280;margin-top:.4rem">{caption}</p>' if caption else ''
    return (f'<div style="overflow-x:auto;margin:1rem 0">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;display:block;margin:0 auto">'
            f'{inner}</svg>{cap}</div>')


MODULES = [
    # ─────────────────────────────────────────────────────────────────────────
    # Module 41 — Web scraping
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Web-скрейпинг: requests + BeautifulSoup',
        'description': 'Автоматизированный сбор данных с веб-страниц на Python.',
        'icon': 'fas fa-spider',
        'order': 41,
        'lessons': [
            {
                'title': 'HTTP-запросы с requests',
                'order': 1,
                'estimated_minutes': 60,
                'content': (
                    '<h2>Библиотека requests</h2>'
                    '<p><code>requests</code> — самая популярная библиотека Python для HTTP-запросов.</p>'
                    + table(
                        ['Метод', 'Назначение', 'Пример'],
                        [
                            ['requests.get(url)', 'Получить ресурс', 'r = requests.get("https://api.example.com/data")'],
                            ['requests.post(url, json=...)', 'Отправить данные', 'r = requests.post(url, json={"key":"val"})'],
                            ['requests.put(url, ...)', 'Обновить ресурс', 'requests.put(url, data=payload)'],
                            ['requests.delete(url)', 'Удалить ресурс', 'requests.delete(url)'],
                        ],
                        'Основные HTTP-методы'
                    )
                    + '<h3>Объект Response</h3>'
                    '<pre><code>import requests\n\nr = requests.get("https://httpbin.org/get")\nprint(r.status_code)    # 200\nprint(r.headers["Content-Type"])\nprint(r.json())          # dict если JSON\nprint(r.text[:100])      # строка\nprint(r.content[:50])    # bytes\n\n# Параметры запроса\nr = requests.get(\n    "https://httpbin.org/get",\n    params={"q": "python", "page": 1},\n    headers={"User-Agent": "MyBot/1.0"},\n    timeout=10\n)\n</code></pre>'
                    + tip('Всегда устанавливайте timeout чтобы запрос не завис навечно.')
                    + '<h3>Сессии — переиспользование соединения</h3>'
                    '<pre><code>with requests.Session() as s:\n    s.headers["Authorization"] = "Bearer TOKEN"\n    r1 = s.get("https://api.example.com/profile")\n    r2 = s.get("https://api.example.com/repos")\n</code></pre>'
                    + diagram(
                        '<rect x="10" y="50" width="120" height="40" rx="6" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>'
                        '<text x="70" y="74" text-anchor="middle" font-size="12" fill="#374151">Python script</text>'
                        '<path d="M130 70 L200 70" stroke="#7c3aed" stroke-width="2" marker-end="url(#arr)"/>'
                        '<rect x="200" y="50" width="100" height="40" rx="6" fill="#3b82f6" opacity=".15" stroke="#3b82f6"/>'
                        '<text x="250" y="69" text-anchor="middle" font-size="12" fill="#374151">HTTP GET</text>'
                        '<text x="250" y="83" text-anchor="middle" font-size="11" fill="#6b7280">status_code</text>'
                        '<path d="M300 70 L370 70" stroke="#3b82f6" stroke-width="2" marker-end="url(#arr2)"/>'
                        '<rect x="370" y="50" width="120" height="40" rx="6" fill="#10b981" opacity=".15" stroke="#10b981"/>'
                        '<text x="430" y="74" text-anchor="middle" font-size="12" fill="#374151">Web Server</text>'
                        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#7c3aed"/></marker>'
                        '<marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#3b82f6"/></marker></defs>',
                        caption='Цикл HTTP-запроса'
                    )
                ),
                'code_example': (
                    'import requests\n\n'
                    '# Получить курсы валют (публичный API)\n'
                    'url = "https://api.exchangerate-api.com/v4/latest/USD"\n'
                    'try:\n'
                    '    r = requests.get(url, timeout=5)\n'
                    '    if r.status_code == 200:\n'
                    '        data = r.json()\n'
                    '        print("Дата:", data["date"])\n'
                    '        for currency in ["EUR", "RUB", "CNY"]:\n'
                    '            print(f"1 USD = {data[\'rates\'].get(currency, \'N/A\')} {currency}")\n'
                    '    else:\n'
                    '        print(f"Ошибка: {r.status_code}")\n'
                    'except requests.Timeout:\n'
                    '    print("Запрос превысил время ожидания")\n'
                    'except requests.ConnectionError:\n'
                    '    print("Нет соединения с сервером")\n'
                ),
            },
            {
                'title': 'BeautifulSoup: парсинг HTML',
                'order': 2,
                'estimated_minutes': 75,
                'content': (
                    '<h2>BeautifulSoup 4</h2>'
                    '<p><strong>BeautifulSoup</strong> преобразует HTML/XML-строку в дерево объектов, '
                    'по которому можно искать элементы.</p>'
                    + table(
                        ['Метод', 'Что ищет', 'Пример'],
                        [
                            ['find(tag, attrs)', 'Первый подходящий тег', 'soup.find("h1")'],
                            ['find_all(tag)', 'Все подходящие теги', 'soup.find_all("a")'],
                            ['select(css)', 'CSS-селектор', 'soup.select(".price")'],
                            ['select_one(css)', 'Первый по CSS', 'soup.select_one("#title")'],
                            ['.text / .string', 'Текстовое содержимое', 'tag.text.strip()'],
                            ['.get(attr)', 'Значение атрибута', 'a.get("href")'],
                        ],
                        'Основные методы BeautifulSoup'
                    )
                    + '<h3>Пример: парсинг таблицы</h3>'
                    '<pre><code>import requests\nfrom bs4 import BeautifulSoup\n\nurl = "https://en.wikipedia.org/wiki/List_of_countries_by_population"\nr = requests.get(url, timeout=10)\nsoup = BeautifulSoup(r.text, "html.parser")\n\ntable = soup.find("table", class_="wikitable")\nrows = table.find_all("tr")[1:6]   # первые 5 строк\n\nfor row in rows:\n    cells = row.find_all(["td", "th"])\n    data = [c.text.strip() for c in cells]\n    print(data)\n</code></pre>'
                    + warn('Всегда проверяйте robots.txt сайта перед скрейпингом. Не перегружайте сервер запросами.')
                    + '<h3>CSS-селекторы — краткий справочник</h3>'
                    + table(
                        ['Селектор', 'Что выбирает'],
                        [
                            ['div.price', '&lt;div class="price"&gt;'],
                            ['#main-title', 'элемент с id="main-title"'],
                            ['table tr td:first-child', 'первая колонка каждой строки таблицы'],
                            ['a[href^="https"]', 'ссылки начинающиеся с https'],
                            ['ul > li', 'прямые дочерние li внутри ul'],
                        ],
                        'Полезные CSS-селекторы'
                    )
                ),
                'code_example': (
                    'import re\n'
                    'from html.parser import HTMLParser\n\n'
                    '# Простой парсер без внешних библиотек\n'
                    'class LinkParser(HTMLParser):\n'
                    '    def __init__(self):\n'
                    '        super().__init__()\n'
                    '        self.links = []\n'
                    '    def handle_starttag(self, tag, attrs):\n'
                    '        if tag == "a":\n'
                    '            for attr, val in attrs:\n'
                    '                if attr == "href" and val:\n'
                    '                    self.links.append(val)\n\n'
                    'html = """\n'
                    '<html><body>\n'
                    '  <a href="https://python.org">Python</a>\n'
                    '  <a href="/about">About</a>\n'
                    '  <a href="https://docs.python.org">Docs</a>\n'
                    '</body></html>\n'
                    '"""\n\n'
                    'parser = LinkParser()\n'
                    'parser.feed(html)\n'
                    'print("Все ссылки:", parser.links)\n'
                    'external = [l for l in parser.links if l.startswith("http")]\n'
                    'print("Внешние:", external)\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 42 — Logging
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Логирование: модуль logging',
        'description': 'Профессиональная диагностика приложений через стандартный модуль logging.',
        'icon': 'fas fa-clipboard-list',
        'order': 42,
        'lessons': [
            {
                'title': 'Уровни, форматы, обработчики',
                'order': 1,
                'estimated_minutes': 55,
                'content': (
                    '<h2>Зачем logging вместо print()?</h2>'
                    '<ul>'
                    '<li>Запись в файл без изменения кода</li>'
                    '<li>Уровни важности: DEBUG → INFO → WARNING → ERROR → CRITICAL</li>'
                    '<li>Временные метки и имя модуля автоматически</li>'
                    '<li>Отключить отладочные сообщения одной строкой</li>'
                    '</ul>'
                    + table(
                        ['Уровень', 'Числовой', 'Использование'],
                        [
                            ['DEBUG', '10', 'Подробная отладочная информация'],
                            ['INFO', '20', 'Подтверждение нормальной работы'],
                            ['WARNING', '30', 'Что-то неожиданное, но ещё работает'],
                            ['ERROR', '40', 'Серьёзная проблема, функция не выполнена'],
                            ['CRITICAL', '50', 'Критическая ошибка, приложение падает'],
                        ],
                        'Уровни логирования'
                    )
                    + '<h3>Базовая настройка</h3>'
                    '<pre><code>import logging\n\n# Простая настройка\nlogging.basicConfig(\n    level=logging.DEBUG,\n    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",\n    datefmt="%Y-%m-%d %H:%M:%S"\n)\n\nlogger = logging.getLogger(__name__)\n\nlogger.debug("Отладочная информация")\nlogger.info("Приложение запущено")\nlogger.warning("Диск почти заполнен: %d%%", 92)\nlogger.error("Файл не найден: %s", "config.json")\n</code></pre>'
                    + '<h3>Запись в файл + консоль</h3>'
                    '<pre><code>import logging\n\nlogger = logging.getLogger("myapp")\nlogger.setLevel(logging.DEBUG)\n\n# Обработчик файла\nfh = logging.FileHandler("app.log", encoding="utf-8")\nfh.setLevel(logging.DEBUG)\n\n# Обработчик консоли\nch = logging.StreamHandler()\nch.setLevel(logging.WARNING)    # в консоль только WARNING+\n\nfmt = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")\nfh.setFormatter(fmt)\nch.setFormatter(fmt)\n\nlogger.addHandler(fh)\nlogger.addHandler(ch)\n\nlogger.debug("В файл, не в консоль")\nlogger.warning("И в файл, и в консоль")\n</code></pre>'
                    + tip('Используйте именованные логгеры `logging.getLogger(__name__)` — это позволяет управлять логированием по модулям.')
                    + '<h3>Ротация логов</h3>'
                    '<pre><code>from logging.handlers import RotatingFileHandler\n\nhandler = RotatingFileHandler(\n    "app.log",\n    maxBytes=1_000_000,  # 1 МБ\n    backupCount=5        # хранить 5 архивов\n)\n</code></pre>'
                ),
                'code_example': (
                    'import logging\nimport sys\n\n'
                    '# Настройка логгера для модуля\n'
                    'def setup_logger(name, level=logging.DEBUG):\n'
                    '    logger = logging.getLogger(name)\n'
                    '    logger.setLevel(level)\n'
                    '    if not logger.handlers:\n'
                    '        handler = logging.StreamHandler(sys.stdout)\n'
                    '        handler.setFormatter(logging.Formatter(\n'
                    '            "%(asctime)s [%(levelname)s] %(message)s",\n'
                    '            datefmt="%H:%M:%S"\n'
                    '        ))\n'
                    '        logger.addHandler(handler)\n'
                    '    return logger\n\n'
                    'log = setup_logger("demo")\n\n'
                    'def divide(a, b):\n'
                    '    log.debug(f"divide({a}, {b}) вызвана")\n'
                    '    if b == 0:\n'
                    '        log.error("Деление на ноль!")\n'
                    '        return None\n'
                    '    result = a / b\n'
                    '    log.info(f"Результат: {result}")\n'
                    '    return result\n\n'
                    'print(divide(10, 2))\n'
                    'print(divide(5, 0))\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 43 — Profiling & optimization
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Профилирование и оптимизация кода',
        'description': 'Как измерять производительность Python-кода и устранять узкие места.',
        'icon': 'fas fa-tachometer-alt',
        'order': 43,
        'lessons': [
            {
                'title': 'timeit, cProfile, memory_profiler',
                'order': 1,
                'estimated_minutes': 60,
                'content': (
                    '<h2>Правило оптимизации</h2>'
                    '<blockquote style="border-left:4px solid #7c3aed;padding-left:1rem;font-style:italic">'
                    '"Premature optimization is the root of all evil" — Donald Knuth</blockquote>'
                    '<p>Сначала измерь, потом оптимизируй!</p>'
                    + table(
                        ['Инструмент', 'Применение', 'Точность'],
                        [
                            ['time.time()', 'Быстрая оценка', 'Низкая (зависит от ОС)'],
                            ['timeit.timeit()', 'Сравнение небольших фрагментов', 'Высокая (многократный запуск)'],
                            ['cProfile', 'Профиль всего приложения', 'Средняя (overhead на каждый вызов)'],
                            ['line_profiler', 'Профиль построчно', 'Высокая (требует установки)'],
                            ['memory_profiler', 'Потребление памяти', 'Высокая'],
                        ],
                        'Инструменты измерения производительности'
                    )
                    + '<h3>timeit — правильное измерение</h3>'
                    '<pre><code>import timeit\n\n# Вариант 1: функция timeit\nt = timeit.timeit(\n    "sum(range(1000))",\n    number=10000\n)\nprint(f"10000 вызовов: {t:.4f}с  =>  {t/10000*1e6:.2f} мкс/вызов")\n\n# Вариант 2: сравнение двух реализаций\nsetup = "data = list(range(1000))"\n\nt1 = timeit.timeit("sorted(data)", setup=setup, number=10000)\nt2 = timeit.timeit("data.sort()", setup=setup, number=10000)\nprint(f"sorted(): {t1:.4f}s   .sort(): {t2:.4f}s")\n</code></pre>'
                    + '<h3>cProfile — профиль функций</h3>'
                    '<pre><code>import cProfile\nimport pstats\n\ndef slow_function():\n    result = []\n    for i in range(10000):\n        result.append(i ** 2)\n    return sorted(result, reverse=True)\n\n# Профилирование\nwith cProfile.Profile() as pr:\n    slow_function()\n\nstats = pstats.Stats(pr).sort_stats("cumulative")\nstats.print_stats(10)  # топ-10 функций по времени\n</code></pre>'
                    + '<h3>Типичные оптимизации Python</h3>'
                    + table(
                        ['Медленно', 'Быстро', 'Причина'],
                        [
                            ['for i in range(len(lst)): lst[i]', 'for x in lst: x', 'Прямая итерация'],
                            ['"" + s1 + s2 + s3 (в цикле)', '"".join([s1,s2,s3])', 'join O(n), + O(n²)'],
                            ['x in list (поиск)', 'x in set', 'Хэш O(1) vs O(n)'],
                            ['[x for x in gen]', 'list(gen)', 'Нет разницы, но gen() экономит RAM'],
                            ['a, b = b, a + tmp', 'a, b = b, a+b', 'Swap через tuple'],
                        ],
                        'Типичные оптимизации Python'
                    )
                    + tip('Используйте `__slots__` в классах при создании миллионов объектов — экономит 40–50% памяти.')
                ),
                'code_example': (
                    'import timeit\n\n'
                    '# Сравниваем 4 способа конкатенации строк\n'
                    'N = 1000\n\n'
                    'def method1():\n'
                    '    result = ""\n'
                    '    for i in range(N):\n'
                    '        result += str(i)\n'
                    '    return result\n\n'
                    'def method2():\n'
                    '    return "".join(str(i) for i in range(N))\n\n'
                    'def method3():\n'
                    '    parts = []\n'
                    '    for i in range(N):\n'
                    '        parts.append(str(i))\n'
                    '    return "".join(parts)\n\n'
                    'def method4():\n'
                    '    return "".join(map(str, range(N)))\n\n'
                    'for name, fn in [("+=", method1), ("join gen", method2),\n'
                    '                  ("list+join", method3), ("map", method4)]:\n'
                    '    t = timeit.timeit(fn, number=1000)\n'
                    '    print(f"{name:12s}: {t*1000:.2f} мс")\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 44 — Network sockets
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Сетевое программирование: сокеты',
        'description': 'Создание клиент-серверных приложений с помощью модуля socket.',
        'icon': 'fas fa-network-wired',
        'order': 44,
        'lessons': [
            {
                'title': 'TCP/UDP сокеты, клиент-сервер',
                'order': 1,
                'estimated_minutes': 70,
                'content': (
                    '<h2>Модель клиент-сервер</h2>'
                    + diagram(
                        '<rect x="20" y="80" width="130" height="60" rx="8" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>'
                        '<text x="85" y="108" text-anchor="middle" font-size="13" font-weight="600" fill="#7c3aed">КЛИЕНТ</text>'
                        '<text x="85" y="125" text-anchor="middle" font-size="11" fill="#374151">connect()</text>'
                        '<path d="M155 100 L300 100" stroke="#7c3aed" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#a1)"/>'
                        '<text x="227" y="93" text-anchor="middle" font-size="11" fill="#7c3aed">send(data)</text>'
                        '<path d="M300 120 L155 120" stroke="#10b981" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#a2)"/>'
                        '<text x="227" y="138" text-anchor="middle" font-size="11" fill="#10b981">recv(data)</text>'
                        '<rect x="300" y="70" width="140" height="80" rx="8" fill="#10b981" opacity=".15" stroke="#10b981"/>'
                        '<text x="370" y="103" text-anchor="middle" font-size="13" font-weight="600" fill="#10b981">СЕРВЕР</text>'
                        '<text x="370" y="120" text-anchor="middle" font-size="11" fill="#374151">bind() → listen()</text>'
                        '<text x="370" y="136" text-anchor="middle" font-size="11" fill="#374151">accept() → recv()</text>'
                        '<defs><marker id="a1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#7c3aed"/></marker>'
                        '<marker id="a2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#10b981"/></marker></defs>',
                        caption='TCP клиент-сервер'
                    )
                    + table(
                        ['Тип', 'Протокол', 'Гарантия', 'Применение'],
                        [
                            ['SOCK_STREAM', 'TCP', 'Порядок + доставка', 'HTTP, FTP, SSH'],
                            ['SOCK_DGRAM', 'UDP', 'Нет гарантий', 'DNS, видеостриминг, игры'],
                        ],
                        'TCP vs UDP'
                    )
                    + '<h3>TCP-сервер (эхо)</h3>'
                    '<pre><code>import socket\nimport threading\n\ndef handle_client(conn, addr):\n    print(f"Подключился: {addr}")\n    with conn:\n        while True:\n            data = conn.recv(1024)\n            if not data: break\n            conn.sendall(b"Echo: " + data)\n    print(f"Отключился: {addr}")\n\nwith socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:\n    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n    srv.bind(("localhost", 9000))\n    srv.listen(5)\n    print("Сервер слушает :9000")\n    while True:\n        conn, addr = srv.accept()\n        t = threading.Thread(target=handle_client, args=(conn, addr))\n        t.daemon = True\n        t.start()\n</code></pre>'
                    + '<h3>TCP-клиент</h3>'
                    '<pre><code>import socket\n\nwith socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n    s.connect(("localhost", 9000))\n    s.sendall(b"Hello, Server!")\n    data = s.recv(1024)\n    print(f"Получено: {data.decode()}")\n</code></pre>'
                    + warn('Не забывайте закрывать сокеты! Используйте контекстный менеджер `with`.')
                ),
                'code_example': (
                    'import socket\n\n'
                    '# Простой HTTP GET через сокет\n'
                    'def http_get(host, path="/"):\n'
                    '    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n'
                    '        s.settimeout(5)\n'
                    '        s.connect((host, 80))\n'
                    '        request = (\n'
                    '            f"GET {path} HTTP/1.0\\r\\n"\n'
                    '            f"Host: {host}\\r\\n"\n'
                    '            "Connection: close\\r\\n"\n'
                    '            "\\r\\n"\n'
                    '        )\n'
                    '        s.sendall(request.encode())\n'
                    '        response = b""\n'
                    '        while True:\n'
                    '            chunk = s.recv(4096)\n'
                    '            if not chunk:\n'
                    '                break\n'
                    '            response += chunk\n'
                    '    return response.decode("utf-8", errors="replace")\n\n'
                    '# Показать заголовки ответа\n'
                    'resp = http_get("example.com", "/")\n'
                    'headers, _, body = resp.partition("\\r\\n\\r\\n")\n'
                    'print("=== ЗАГОЛОВКИ ===")\n'
                    'print(headers[:300])\n'
                    'print("\\n=== ТЕЛО (первые 200 символов) ===")\n'
                    'print(body[:200])\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 45 — Packaging & pip
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Пакетирование и публикация на PyPI',
        'description': 'Создание собственного pip-пакета и публикация на PyPI.',
        'icon': 'fas fa-box',
        'order': 45,
        'lessons': [
            {
                'title': 'pyproject.toml, setup.py, virtual environments',
                'order': 1,
                'estimated_minutes': 65,
                'content': (
                    '<h2>Структура Python-пакета</h2>'
                    '<pre><code>mypackage/\n├── src/\n│   └── mypackage/\n│       ├── __init__.py\n│       ├── core.py\n│       └── utils.py\n├── tests/\n│   └── test_core.py\n├── pyproject.toml\n├── README.md\n└── LICENSE\n</code></pre>'
                    + '<h3>pyproject.toml (современный стандарт)</h3>'
                    '<pre><code>[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"\n\n[project]\nname = "mypackage"\nversion = "0.1.0"\ndescription = "Мой первый пакет"\nreadme = "README.md"\nrequires-python = ">=3.10"\nlicense = {file = "LICENSE"}\n\ndependencies = [\n    "requests>=2.28",\n    "click>=8.0"\n]\n\n[project.scripts]\nmycli = "mypackage.cli:main"  # консольная команда\n</code></pre>'
                    + table(
                        ['Команда', 'Назначение'],
                        [
                            ['python -m venv .venv', 'Создать виртуальное окружение'],
                            ['.venv\\Scripts\\activate (Win)', 'Активировать venv'],
                            ['pip install -e .', 'Установить в режиме разработки (editable)'],
                            ['pip freeze > requirements.txt', 'Сохранить зависимости'],
                            ['pip install -r requirements.txt', 'Восстановить зависимости'],
                            ['python -m build', 'Собрать пакет (wheel + sdist)'],
                            ['twine upload dist/*', 'Опубликовать на PyPI'],
                        ],
                        'Основные команды'
                    )
                    + '<h3>__init__.py — публичный API пакета</h3>'
                    '<pre><code># mypackage/__init__.py\nfrom .core import Calculator\nfrom .utils import format_number\n\n__version__ = "0.1.0"\n__all__ = ["Calculator", "format_number"]\n</code></pre>'
                    + tip('Используйте `__all__` чтобы явно указать, что экспортирует ваш пакет.')
                    + '<h3>Виртуальные окружения</h3>'
                    + diagram(
                        '<rect x="10" y="20" width="580" height="220" rx="10" fill="#f3f4f6" stroke="#d1d5db"/>'
                        '<text x="295" y="50" text-anchor="middle" font-size="14" font-weight="600" fill="#374151">Система Python</text>'
                        '<rect x="30" y="65" width="160" height="80" rx="8" fill="#7c3aed" opacity=".15" stroke="#7c3aed"/>'
                        '<text x="110" y="100" text-anchor="middle" font-size="12" fill="#374151">.venv_project1</text>'
                        '<text x="110" y="118" text-anchor="middle" font-size="11" fill="#6b7280">django==4.2</text>'
                        '<text x="110" y="134" text-anchor="middle" font-size="11" fill="#6b7280">requests==2.28</text>'
                        '<rect x="220" y="65" width="160" height="80" rx="8" fill="#10b981" opacity=".15" stroke="#10b981"/>'
                        '<text x="300" y="100" text-anchor="middle" font-size="12" fill="#374151">.venv_project2</text>'
                        '<text x="300" y="118" text-anchor="middle" font-size="11" fill="#6b7280">fastapi==0.100</text>'
                        '<text x="300" y="134" text-anchor="middle" font-size="11" fill="#6b7280">sqlalchemy==2.0</text>'
                        '<rect x="410" y="65" width="160" height="80" rx="8" fill="#f59e0b" opacity=".15" stroke="#f59e0b"/>'
                        '<text x="490" y="100" text-anchor="middle" font-size="12" fill="#374151">.venv_project3</text>'
                        '<text x="490" y="118" text-anchor="middle" font-size="11" fill="#6b7280">flask==3.0</text>'
                        '<text x="490" y="134" text-anchor="middle" font-size="11" fill="#6b7280">numpy==1.26</text>'
                        '<text x="295" y="190" text-anchor="middle" font-size="12" fill="#6b7280">Каждое окружение изолировано — нет конфликтов версий</text>',
                        caption='Виртуальные окружения изолируют зависимости проектов'
                    )
                ),
                'code_example': (
                    '# Демонстрация __init__.py и структуры пакета\n\n'
                    '# Представим, что у нас есть пакет mathutils\n'
                    '# mathutils/__init__.py\n\n'
                    'class Calculator:\n'
                    '    """Простой калькулятор."""\n'
                    '    def __init__(self):\n'
                    '        self.history = []\n\n'
                    '    def calculate(self, a, op, b):\n'
                    '        ops = {"+": a+b, "-": a-b, "*": a*b, "/": a/b if b else None}\n'
                    '        result = ops.get(op)\n'
                    '        if result is not None:\n'
                    '            self.history.append(f"{a} {op} {b} = {result}")\n'
                    '        return result\n\n'
                    '    def show_history(self):\n'
                    '        for entry in self.history:\n'
                    '            print(entry)\n\n'
                    'def format_number(n, decimals=2):\n'
                    '    """Форматировать число с разделителем тысяч."""\n'
                    '    return f"{n:,.{decimals}f}"\n\n'
                    '# Использование\n'
                    'calc = Calculator()\n'
                    'print(calc.calculate(10, "+", 5))\n'
                    'print(calc.calculate(100, "/", 3))\n'
                    'calc.show_history()\n'
                    'print(format_number(1234567.89))\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 46 — NumPy basics
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'NumPy: массивы и математика',
        'description': 'Эффективные числовые вычисления с NumPy — основа data science.',
        'icon': 'fas fa-calculator',
        'order': 46,
        'lessons': [
            {
                'title': 'ndarray: создание, срезы, операции',
                'order': 1,
                'estimated_minutes': 70,
                'content': (
                    '<h2>Почему NumPy быстрее списков?</h2>'
                    '<p>NumPy хранит данные в непрерывном блоке памяти как C-массивы. '
                    'Операции выполняются на уровне C без интерпретации Python.</p>'
                    + table(
                        ['Операция', 'Python list', 'NumPy ndarray'],
                        [
                            ['Суммирование 10⁶ чисел', '~100 мс', '~2 мс (50x быстрее)'],
                            ['Хранение 10⁶ float', '~35 МБ', '~8 МБ'],
                            ['Умножение матриц', 'Ручные вложенные циклы', 'np.dot(A, B) — BLAS'],
                        ],
                        'Python list vs NumPy ndarray'
                    )
                    + '<h3>Создание массивов</h3>'
                    '<pre><code>import numpy as np\n\n# Из списка\na = np.array([1, 2, 3, 4, 5])\nb = np.array([[1, 2, 3], [4, 5, 6]])  # 2D\n\n# Специальные массивы\nnp.zeros((3, 4))        # нули 3x4\nnp.ones((2, 3))         # единицы\nnp.eye(4)               # единичная матрица\nnp.arange(0, 10, 0.5)   # как range(), но float\nnp.linspace(0, 1, 11)   # 11 равноотстоящих точек\nnp.random.rand(3, 3)    # случайные [0,1)\nnp.full((3, 3), 7)      # заполненный значением\n</code></pre>'
                    + '<h3>Атрибуты и срезы</h3>'
                    '<pre><code>a = np.array([[1,2,3],[4,5,6],[7,8,9]])\n\nprint(a.shape)   # (3, 3)\nprint(a.dtype)   # int64\nprint(a.ndim)    # 2\nprint(a.size)    # 9\n\n# Срезы\nprint(a[0, :])   # первая строка: [1 2 3]\nprint(a[:, 1])   # второй столбец: [2 5 8]\nprint(a[1:, 1:]) # подматрица: [[5,6],[8,9]]\nprint(a[a > 5])  # булева маска: [6 7 8 9]\n</code></pre>'
                    + '<h3>Векторизованные операции</h3>'
                    '<pre><code>x = np.array([1, 2, 3, 4, 5])\n\nprint(x * 2)        # [2 4 6 8 10]\nprint(x ** 2)       # [1 4 9 16 25]\nprint(np.sqrt(x))   # поэлементный sqrt\nprint(np.sum(x))    # 15\nprint(np.mean(x))   # 3.0\nprint(np.std(x))    # стандартное отклонение\n\n# Матричное умножение\nA = np.array([[1,2],[3,4]])\nB = np.array([[5,6],[7,8]])\nprint(A @ B)   # [[19,22],[43,50]]\n# или np.dot(A, B)\n</code></pre>'
                    + tip('`@` — оператор матричного умножения (Python 3.5+). Не путайте с `*` (поэлементное умножение).')
                ),
                'code_example': (
                    'import numpy as np\n\n'
                    '# Линейная регрессия методом наименьших квадратов\n'
                    '# y = a*x + b\n\n'
                    'x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)\n'
                    'y = 2.5 * x + 1.0 + np.random.normal(0, 0.5, len(x))  # зашумлённые данные\n\n'
                    '# Нормальное уравнение: [a, b] = (X^T X)^{-1} X^T y\n'
                    'X = np.column_stack([x, np.ones(len(x))])  # матрица признаков\n'
                    'coeffs, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)\n'
                    'a, b = coeffs\n'
                    'print(f"Найдено: y = {a:.3f}*x + {b:.3f}")\n'
                    'print(f"Ожидалось: y = 2.500*x + 1.000")\n\n'
                    '# Предсказание\n'
                    'x_new = np.array([11, 12, 15])\n'
                    'y_pred = a * x_new + b\n'
                    'print(f"Предсказание для x={x_new}: y={np.round(y_pred, 2)}")\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 47 — Pandas intro
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Pandas: анализ табличных данных',
        'description': 'DataFrame и Series для загрузки, очистки и агрегации данных.',
        'icon': 'fas fa-table',
        'order': 47,
        'lessons': [
            {
                'title': 'DataFrame, Series, группировка',
                'order': 1,
                'estimated_minutes': 80,
                'content': (
                    '<h2>Pandas — Excel для Python</h2>'
                    '<p>pandas предоставляет два основных типа данных:</p>'
                    '<ul>'
                    '<li><strong>Series</strong> — одномерный индексированный массив</li>'
                    '<li><strong>DataFrame</strong> — двумерная таблица (столбцы = Series)</li>'
                    '</ul>'
                    + '<h3>Создание DataFrame</h3>'
                    '<pre><code>import pandas as pd\nimport numpy as np\n\n# Из словаря\ndf = pd.DataFrame({\n    "name": ["Alice", "Bob", "Charlie", "Diana"],\n    "age":  [25, 30, 35, 28],\n    "score": [88.5, 92.0, 78.3, 95.1],\n    "passed": [True, True, True, True]\n})\n\n# Из CSV\ndf = pd.read_csv("data.csv", encoding="utf-8")\n\n# Из Excel\ndf = pd.read_excel("data.xlsx", sheet_name="Sheet1")\n</code></pre>'
                    + '<h3>Основные операции</h3>'
                    '<pre><code>print(df.head())       # первые 5 строк\nprint(df.info())       # типы, количество не-null\nprint(df.describe())   # статистика числовых столбцов\n\n# Выборка\nprint(df["name"])                    # столбец (Series)\nprint(df[["name", "score"]])         # несколько столбцов\nprint(df[df["age"] > 28])            # фильтрация\nprint(df.loc[0:2, "name":"score"])   # по меткам\nprint(df.iloc[0:2, 0:3])             # по позиции\n</code></pre>'
                    + '<h3>Группировка и агрегация</h3>'
                    '<pre><code># groupby — аналог SQL GROUP BY\ndf_scores = pd.DataFrame({\n    "student": ["Alice","Bob","Alice","Bob","Charlie"],\n    "subject": ["Math","Math","Python","Python","Math"],\n    "grade":   [90, 85, 95, 88, 72]\n})\n\n# Средний балл по студентам\nprint(df_scores.groupby("student")["grade"].mean())\n\n# Несколько агрегатов\nprint(df_scores.groupby("subject")["grade"].agg(["mean","min","max"]))\n\n# pivot_table — сводная таблица\npt = df_scores.pivot_table(\n    values="grade", index="student", columns="subject", fill_value=0\n)\nprint(pt)\n</code></pre>'
                    + '<h3>Очистка данных</h3>'
                    '<pre><code>df.dropna()              # удалить строки с NaN\ndf.fillna(0)             # заполнить NaN нулями\ndf.drop_duplicates()     # удалить дубликаты\ndf.rename(columns={"old":"new"})  # переименовать\ndf["age"] = df["age"].astype(int) # приведение типа\n\n# Применить функцию к столбцу\ndf["grade_letter"] = df["grade"].apply(\n    lambda g: "A" if g >= 90 else "B" if g >= 80 else "C"\n)\n</code></pre>'
                    + tip('`df.value_counts()` — быстрый способ посчитать уникальные значения в столбце.')
                ),
                'code_example': (
                    'import pandas as pd\n\n'
                    '# Анализ успеваемости студентов\n'
                    'data = {\n'
                    '    "student": ["Иванов", "Петров", "Сидорова", "Козлова", "Новиков",\n'
                    '                "Иванов", "Петров", "Сидорова", "Козлова", "Новиков"],\n'
                    '    "subject": ["Python", "Python", "Python", "Python", "Python",\n'
                    '                "Алгоритмы", "Алгоритмы", "Алгоритмы", "Алгоритмы", "Алгоритмы"],\n'
                    '    "grade":   [85, 92, 78, 95, 61, 88, 75, 82, 90, 55]\n'
                    '}\n\n'
                    'df = pd.DataFrame(data)\n\n'
                    '# 1. Средний балл по предметам\n'
                    'print("Средний балл по предметам:")\n'
                    'print(df.groupby("subject")["grade"].mean().round(1))\n\n'
                    '# 2. Рейтинг студентов (средний по всем предметам)\n'
                    'print("\\nРейтинг студентов:")\n'
                    'ranking = df.groupby("student")["grade"].mean().sort_values(ascending=False)\n'
                    'print(ranking.round(1))\n\n'
                    '# 3. Кто не сдал (< 70 баллов)\n'
                    'print("\\nНезачёты:")\n'
                    'print(df[df["grade"] < 70][["student", "subject", "grade"]])\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 48 — Databases with SQLAlchemy
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Базы данных: SQLAlchemy ORM',
        'description': 'ORM-подход к работе с реляционными базами данных в Python.',
        'icon': 'fas fa-database',
        'order': 48,
        'lessons': [
            {
                'title': 'Модели, сессии, CRUD',
                'order': 1,
                'estimated_minutes': 75,
                'content': (
                    '<h2>SQLAlchemy — два уровня</h2>'
                    + table(
                        ['Уровень', 'Что это', 'Когда использовать'],
                        [
                            ['Core', 'SQL Expression Language', 'Сложные запросы, производительность'],
                            ['ORM', 'Объектно-реляционное отображение', 'Обычные CRUD-приложения'],
                        ],
                        'Уровни SQLAlchemy'
                    )
                    + '<h3>Определение моделей (ORM)</h3>'
                    '<pre><code>from sqlalchemy import create_engine, String, Integer, ForeignKey, select\nfrom sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session\n\nclass Base(DeclarativeBase):\n    pass\n\nclass Student(Base):\n    __tablename__ = "students"\n\n    id:    Mapped[int]  = mapped_column(primary_key=True)\n    name:  Mapped[str]  = mapped_column(String(100))\n    group: Mapped[str]  = mapped_column(String(20))\n    scores: Mapped[list["Score"]] = relationship(back_populates="student")\n\n    def __repr__(self):\n        return f"Student({self.name!r}, {self.group!r})"\n\nclass Score(Base):\n    __tablename__ = "scores"\n\n    id:         Mapped[int] = mapped_column(primary_key=True)\n    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))\n    subject:    Mapped[str] = mapped_column(String(50))\n    value:      Mapped[int]\n    student:    Mapped["Student"] = relationship(back_populates="scores")\n</code></pre>'
                    + '<h3>CRUD операции</h3>'
                    '<pre><code># Создание таблиц\nengine = create_engine("sqlite:///school.db", echo=False)\nBase.metadata.create_all(engine)\n\nwith Session(engine) as session:\n    # CREATE\n    s1 = Student(name="Иванов Иван", group="ИТ-21")\n    session.add(s1)\n    session.commit()\n\n    # READ\n    stmt = select(Student).where(Student.group == "ИТ-21")\n    students = session.scalars(stmt).all()\n\n    # UPDATE\n    s1.group = "ИТ-22"\n    session.commit()\n\n    # DELETE\n    session.delete(s1)\n    session.commit()\n</code></pre>'
                    + '<h3>Запросы и агрегация</h3>'
                    '<pre><code>from sqlalchemy import func\n\nwith Session(engine) as session:\n    # Средний балл по группам\n    stmt = (\n        select(Student.group, func.avg(Score.value).label("avg_score"))\n        .join(Score)\n        .group_by(Student.group)\n        .order_by(func.avg(Score.value).desc())\n    )\n    results = session.execute(stmt).all()\n    for group, avg in results:\n        print(f"{group}: {avg:.1f}")\n</code></pre>'
                    + tip('SQLAlchemy 2.0 использует `select()` вместо `session.query()` — это новый рекомендуемый стиль.')
                ),
                'code_example': (
                    'from sqlalchemy import create_engine, String, Integer, select, func\n'
                    'from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session\n\n'
                    'class Base(DeclarativeBase):\n'
                    '    pass\n\n'
                    'class Product(Base):\n'
                    '    __tablename__ = "products"\n'
                    '    id:       Mapped[int] = mapped_column(primary_key=True)\n'
                    '    name:     Mapped[str] = mapped_column(String(100))\n'
                    '    category: Mapped[str] = mapped_column(String(50))\n'
                    '    price:    Mapped[float]\n'
                    '    stock:    Mapped[int] = mapped_column(default=0)\n\n'
                    'engine = create_engine("sqlite:///:memory:")\n'
                    'Base.metadata.create_all(engine)\n\n'
                    'products = [\n'
                    '    Product(name="Ноутбук", category="Электроника", price=75000, stock=5),\n'
                    '    Product(name="Мышь", category="Электроника", price=1500, stock=50),\n'
                    '    Product(name="Стол", category="Мебель", price=12000, stock=3),\n'
                    '    Product(name="Кресло", category="Мебель", price=8500, stock=7),\n'
                    '    Product(name="Телефон", category="Электроника", price=45000, stock=12),\n'
                    ']\n\n'
                    'with Session(engine) as s:\n'
                    '    s.add_all(products)\n'
                    '    s.commit()\n\n'
                    '    # Средняя цена по категориям\n'
                    '    stmt = select(Product.category, func.avg(Product.price).label("avg"))\\\n'
                    '           .group_by(Product.category)\n'
                    '    for cat, avg in s.execute(stmt):\n'
                    '        print(f"{cat}: {avg:,.0f} руб.")\n\n'
                    '    # Товары дороже 10000\n'
                    '    expensive = s.scalars(select(Product).where(Product.price > 10000)).all()\n'
                    '    print("\\nДорогие товары:", [p.name for p in expensive])\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 49 — Async programming
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Асинхронное программирование: asyncio',
        'description': 'Конкурентность без потоков — coroutines, event loop, aiohttp.',
        'icon': 'fas fa-bolt',
        'order': 49,
        'lessons': [
            {
                'title': 'async/await, Tasks, gather',
                'order': 1,
                'estimated_minutes': 75,
                'content': (
                    '<h2>Зачем asyncio?</h2>'
                    '<p>При I/O-операциях (сеть, файлы) CPU простаивает. '
                    'asyncio позволяет другим задачам работать в это время <strong>без потоков</strong>.</p>'
                    + diagram(
                        '<rect x="10" y="10" width="580" height="50" rx="6" fill="#f3f4f6" stroke="#d1d5db"/>'
                        '<text x="295" y="40" text-anchor="middle" font-size="13" font-weight="600" fill="#374151">Синхронно: задачи выполняются последовательно</text>'
                        '<rect x="10" y="80" width="120" height="30" rx="4" fill="#7c3aed" opacity=".7"/>'
                        '<text x="70" y="100" text-anchor="middle" font-size="11" fill="white">Task A (5s)</text>'
                        '<rect x="140" y="80" width="100" height="30" rx="4" fill="#3b82f6" opacity=".7"/>'
                        '<text x="190" y="100" text-anchor="middle" font-size="11" fill="white">Task B (3s)</text>'
                        '<rect x="250" y="80" width="80" height="30" rx="4" fill="#10b981" opacity=".7"/>'
                        '<text x="290" y="100" text-anchor="middle" font-size="11" fill="white">Task C (2s)</text>'
                        '<text x="350" y="100" font-size="11" fill="#6b7280">Итого: 10 секунд</text>'
                        '<rect x="10" y="140" width="580" height="50" rx="6" fill="#f0fdf4" stroke="#86efac"/>'
                        '<text x="295" y="170" text-anchor="middle" font-size="13" font-weight="600" fill="#374151">Асинхронно: задачи пересекаются</text>'
                        '<rect x="10" y="200" width="120" height="30" rx="4" fill="#7c3aed" opacity=".7"/>'
                        '<text x="70" y="220" text-anchor="middle" font-size="11" fill="white">Task A (5s)</text>'
                        '<rect x="10" y="200" width="100" height="30" rx="4" fill="#3b82f6" opacity=".3"/>'
                        '<rect x="10" y="200" width="80" height="30" rx="4" fill="#10b981" opacity=".3"/>'
                        '<text x="450" y="220" font-size="11" fill="#10b981" font-weight="600">Итого: 5 секунд</text>',
                        h=240,
                        caption='Асинхронность сокращает общее время ожидания'
                    )
                    + '<h3>Основные концепции</h3>'
                    '<pre><code>import asyncio\n\n# coroutine — функция с async def\nasync def greet(name: str, delay: float):\n    print(f"Привет, {name}!")\n    await asyncio.sleep(delay)   # уступить управление\n    print(f"Пока, {name}!")\n\n# Запуск одной корутины\nasyncio.run(greet("Alice", 1.0))\n</code></pre>'
                    + '<h3>asyncio.gather — параллельный запуск</h3>'
                    '<pre><code>import asyncio\nimport time\n\nasync def fetch(url: str, delay: float) -> str:\n    print(f"  -> {url}")\n    await asyncio.sleep(delay)   # имитация I/O\n    print(f"  <- {url} готово")\n    return f"data:{url}"\n\nasync def main():\n    start = time.perf_counter()\n    results = await asyncio.gather(\n        fetch("api.com/users", 1.5),\n        fetch("api.com/posts", 2.0),\n        fetch("api.com/tags",  0.5),\n    )\n    elapsed = time.perf_counter() - start\n    print(f"Всего: {elapsed:.2f}с (а не {1.5+2.0+0.5}с)")\n    print(results)\n\nasyncio.run(main())\n</code></pre>'
                    + '<h3>Task — запуск в фоне</h3>'
                    '<pre><code>async def main():\n    # create_task запускает корутину немедленно\n    task1 = asyncio.create_task(fetch("url1", 1.0))\n    task2 = asyncio.create_task(fetch("url2", 0.5))\n\n    result2 = await task2    # ждём task2\n    result1 = await task1    # ждём task1\n    return result1, result2\n</code></pre>'
                    + warn('`asyncio.sleep()` не блокирует. Блокирует `time.sleep()` — никогда не используйте его внутри async-кода.')
                    + table(
                        ['Синхронная библиотека', 'Async-альтернатива'],
                        [
                            ['requests', 'aiohttp / httpx[async]'],
                            ['sqlite3', 'aiosqlite'],
                            ['open() / file I/O', 'aiofiles'],
                            ['time.sleep()', 'asyncio.sleep()'],
                        ],
                        'Async-замены синхронных библиотек'
                    )
                ),
                'code_example': (
                    'import asyncio\n\n'
                    'async def process_item(item_id: int) -> dict:\n'
                    '    """Имитация асинхронной обработки (запрос к API/БД)."""\n'
                    '    import random\n'
                    '    delay = random.uniform(0.1, 0.5)\n'
                    '    await asyncio.sleep(delay)\n'
                    '    score = random.randint(50, 100)\n'
                    '    return {"id": item_id, "score": score, "time": f"{delay:.2f}s"}\n\n'
                    'async def main():\n'
                    '    import time\n'
                    '    items = list(range(1, 11))   # 10 элементов\n'
                    '    \n'
                    '    print("Запускаем 10 задач параллельно...")\n'
                    '    start = time.perf_counter()\n'
                    '    \n'
                    '    results = await asyncio.gather(\n'
                    '        *[process_item(i) for i in items]\n'
                    '    )\n'
                    '    \n'
                    '    elapsed = time.perf_counter() - start\n'
                    '    print(f"Завершено за {elapsed:.2f}с")\n'
                    '    \n'
                    '    for r in sorted(results, key=lambda x: x["score"], reverse=True):\n'
                    '        print(f"  item {r[\'id\']:2d}: score={r[\'score\']}  ({r[\'time\']})")\n\n'
                    'asyncio.run(main())\n'
                ),
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # Module 50 — Design patterns advanced
    # ─────────────────────────────────────────────────────────────────────────
    {
        'title': 'Паттерны проектирования: SOLID и DI',
        'description': 'Принципы SOLID, инверсия зависимостей и практические паттерны Python.',
        'icon': 'fas fa-drafting-compass',
        'order': 50,
        'lessons': [
            {
                'title': 'SOLID принципы на Python',
                'order': 1,
                'estimated_minutes': 70,
                'content': (
                    '<h2>SOLID — пять принципов ООП</h2>'
                    + table(
                        ['Буква', 'Принцип', 'Суть'],
                        [
                            ['S', 'Single Responsibility', 'Класс делает одно дело'],
                            ['O', 'Open/Closed', 'Открыт для расширения, закрыт для изменения'],
                            ['L', 'Liskov Substitution', 'Подкласс заменяет родительский везде'],
                            ['I', 'Interface Segregation', 'Много маленьких интерфейсов лучше одного большого'],
                            ['D', 'Dependency Inversion', 'Зависеть от абстракций, не от конкретных классов'],
                        ],
                        'SOLID'
                    )
                    + '<h3>S — Single Responsibility</h3>'
                    '<pre><code># ПЛОХО: класс делает и сохранение, и отчёты\nclass UserManager:\n    def save_user(self, user): ...\n    def send_email(self, user): ...\n    def generate_report(self): ...\n\n# ХОРОШО: разделить ответственности\nclass UserRepository:\n    def save(self, user): ...\n\nclass EmailService:\n    def send(self, user, message): ...\n\nclass ReportGenerator:\n    def generate(self): ...\n</code></pre>'
                    + '<h3>O — Open/Closed</h3>'
                    '<pre><code>from abc import ABC, abstractmethod\n\nclass Discount(ABC):\n    @abstractmethod\n    def apply(self, price: float) -> float: ...\n\nclass NoDiscount(Discount):\n    def apply(self, price): return price\n\nclass PercentDiscount(Discount):\n    def __init__(self, pct): self.pct = pct\n    def apply(self, price): return price * (1 - self.pct/100)\n\nclass BlackFridayDiscount(Discount):   # расширяем — не меняем\n    def apply(self, price): return price * 0.5\n\ndef checkout(price: float, discount: Discount) -> float:\n    return discount.apply(price)\n</code></pre>'
                    + '<h3>D — Dependency Inversion (DI)</h3>'
                    '<pre><code>from abc import ABC, abstractmethod\n\nclass NotificationSender(ABC):\n    @abstractmethod\n    def send(self, user: str, msg: str): ...\n\nclass EmailSender(NotificationSender):\n    def send(self, user, msg):\n        print(f"Email → {user}: {msg}")\n\nclass SMSSender(NotificationSender):\n    def send(self, user, msg):\n        print(f"SMS → {user}: {msg}")\n\nclass OrderService:\n    def __init__(self, sender: NotificationSender):\n        self.sender = sender    # инъекция зависимости\n\n    def place_order(self, user, item):\n        print(f"Заказ {item} создан")\n        self.sender.send(user, f"Ваш заказ {item!r} принят!")\n\n# Можно заменить EmailSender на SMSSender без изменения OrderService\nservice = OrderService(EmailSender())\nservice.place_order("ivan@example.com", "Ноутбук")\n</code></pre>'
                    + tip('Dependency Injection — не фреймворк, это паттерн. В Python его легко реализовать через конструктор.')
                    + '<h3>Паттерн Repository</h3>'
                    '<pre><code>from abc import ABC, abstractmethod\nfrom typing import List, Optional\n\nclass UserRepository(ABC):\n    @abstractmethod\n    def get(self, user_id: int) -> Optional[dict]: ...\n    @abstractmethod\n    def save(self, user: dict) -> None: ...\n    @abstractmethod\n    def all(self) -> List[dict]: ...\n\nclass InMemoryUserRepository(UserRepository):\n    def __init__(self): self._db = {}\n    def get(self, uid): return self._db.get(uid)\n    def save(self, u): self._db[u["id"]] = u\n    def all(self): return list(self._db.values())\n\nclass SqliteUserRepository(UserRepository):\n    # реализация для БД\n    def get(self, uid): ...\n    def save(self, u): ...\n    def all(self): ...\n</code></pre>'
                ),
                'code_example': (
                    'from abc import ABC, abstractmethod\nfrom typing import List\n\n'
                    '# Пример: система оплаты с DI\n\n'
                    'class PaymentGateway(ABC):\n'
                    '    @abstractmethod\n'
                    '    def charge(self, amount: float, card: str) -> bool: ...\n\n'
                    'class MockGateway(PaymentGateway):\n'
                    '    """Для тестирования."""\n'
                    '    def charge(self, amount, card):\n'
                    '        print(f"[MOCK] Списание {amount} с {card[-4:]}")\n'
                    '        return amount < 100000   # отклоняем слишком большие суммы\n\n'
                    'class StripeGateway(PaymentGateway):\n'
                    '    """Реальный платёжный шлюз."""\n'
                    '    def charge(self, amount, card):\n'
                    '        # здесь был бы вызов Stripe API\n'
                    '        print(f"[Stripe] Списание {amount}")\n'
                    '        return True\n\n'
                    'class OrderService:\n'
                    '    def __init__(self, gateway: PaymentGateway):\n'
                    '        self.gateway = gateway\n'
                    '        self.orders: List[dict] = []\n\n'
                    '    def checkout(self, item: str, price: float, card: str) -> bool:\n'
                    '        success = self.gateway.charge(price, card)\n'
                    '        if success:\n'
                    '            self.orders.append({"item": item, "price": price})\n'
                    '            print(f"Заказ {item!r} оплачен!")\n'
                    '        else:\n'
                    '            print(f"Оплата отклонена!")\n'
                    '        return success\n\n'
                    '# В тестах используем MockGateway\n'
                    'svc = OrderService(MockGateway())\n'
                    'svc.checkout("Ноутбук", 75000, "4111111111111234")\n'
                    'svc.checkout("Яхта", 99999999, "4111111111115678")\n'
                ),
            },
            {
                'title': 'Паттерны: Decorator, Proxy, Chain of Responsibility',
                'order': 2,
                'estimated_minutes': 60,
                'content': (
                    '<h2>Структурные и поведенческие паттерны</h2>'
                    + '<h3>Decorator (обёртка) — уже в Python!</h3>'
                    '<pre><code>import functools\nimport time\n\ndef retry(times=3, delay=0.5):\n    """Повторить вызов при исключении."""\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(1, times + 1):\n                try:\n                    return func(*args, **kwargs)\n                except Exception as e:\n                    if attempt == times: raise\n                    print(f"Попытка {attempt}/{times} неудачна: {e}")\n                    time.sleep(delay)\n        return wrapper\n    return decorator\n\n@retry(times=3, delay=0.1)\ndef unstable_api():\n    import random\n    if random.random() < 0.7:\n        raise ConnectionError("Временная ошибка")\n    return "OK"\n\nresult = unstable_api()\n</code></pre>'
                    + '<h3>Proxy — контроль доступа</h3>'
                    '<pre><code>class Database:\n    def query(self, sql: str) -> list:\n        print(f"SQL: {sql}")\n        return []  # реальный результат\n\nclass CachedDatabase:\n    """Proxy с кешированием."""\n    def __init__(self, db: Database):\n        self._db = db\n        self._cache = {}\n\n    def query(self, sql: str) -> list:\n        if sql not in self._cache:\n            self._cache[sql] = self._db.query(sql)\n        else:\n            print(f"Cache hit: {sql[:30]}")\n        return self._cache[sql]\n\ndb = CachedDatabase(Database())\ndb.query("SELECT * FROM users")\ndb.query("SELECT * FROM users")  # из кеша\n</code></pre>'
                    + '<h3>Chain of Responsibility</h3>'
                    '<pre><code>from abc import ABC, abstractmethod\nfrom typing import Optional\n\nclass Handler(ABC):\n    def __init__(self):\n        self._next: Optional["Handler"] = None\n\n    def set_next(self, handler: "Handler") -> "Handler":\n        self._next = handler\n        return handler\n\n    @abstractmethod\n    def handle(self, amount: int) -> str: ...\n\nclass SupportL1(Handler):\n    def handle(self, amount):\n        if amount <= 1000:\n            return f"L1 решил: {amount} руб."\n        return self._next.handle(amount) if self._next else "Не решено"\n\nclass SupportL2(Handler):\n    def handle(self, amount):\n        if amount <= 10000:\n            return f"L2 решил: {amount} руб."\n        return self._next.handle(amount) if self._next else "Не решено"\n\nclass SupportManager(Handler):\n    def handle(self, amount):\n        return f"Менеджер решил: {amount} руб."\n\n# Выстраиваем цепочку\nl1 = SupportL1()\nl1.set_next(SupportL2()).set_next(SupportManager())\n\nfor amt in [500, 5000, 50000]:\n    print(l1.handle(amt))\n</code></pre>'
                    + tip('Chain of Responsibility используется в Django middleware, logging handlers, Flask before_request.')
                ),
                'code_example': (
                    'import functools\nimport time\n\n'
                    '# Система декораторов для API-эндпоинтов\n\n'
                    'def log_call(func):\n'
                    '    @functools.wraps(func)\n'
                    '    def wrapper(*args, **kwargs):\n'
                    '        print(f"[LOG] Вызов {func.__name__}")\n'
                    '        result = func(*args, **kwargs)\n'
                    '        print(f"[LOG] {func.__name__} вернул {result!r}")\n'
                    '        return result\n'
                    '    return wrapper\n\n'
                    'def require_auth(func):\n'
                    '    @functools.wraps(func)\n'
                    '    def wrapper(*args, user=None, **kwargs):\n'
                    '        if not user:\n'
                    '            raise PermissionError("Требуется авторизация")\n'
                    '        return func(*args, user=user, **kwargs)\n'
                    '    return wrapper\n\n'
                    'def measure_time(func):\n'
                    '    @functools.wraps(func)\n'
                    '    def wrapper(*args, **kwargs):\n'
                    '        t0 = time.perf_counter()\n'
                    '        result = func(*args, **kwargs)\n'
                    '        print(f"[PERF] {func.__name__}: {(time.perf_counter()-t0)*1000:.2f}мс")\n'
                    '        return result\n'
                    '    return wrapper\n\n'
                    '@log_call\n'
                    '@require_auth\n'
                    '@measure_time\n'
                    'def get_profile(user_id: int, user=None) -> dict:\n'
                    '    time.sleep(0.01)  # имитация БД\n'
                    '    return {"id": user_id, "name": "Иван", "auth_user": user}\n\n'
                    'try:\n'
                    '    get_profile(42)             # без user → PermissionError\n'
                    'except PermissionError as e:\n'
                    '    print(f"Ошибка: {e}")\n\n'
                    'get_profile(42, user="admin")\n'
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed theory modules 41-50'

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
            f'seed_theory_advanced2: {total_modules} modules, {total_lessons} lessons'
        ))
