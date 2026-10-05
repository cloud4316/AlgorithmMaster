"""
Seed: РВЭС — модули M5-M7
КТП: Инструментальные средства, ЕСПД, тестирование ПО
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


MODULES = [
    {
        'order': 5,
        'title': 'Инструментальные средства разработки ПО для встраиваемых систем',
        'icon': 'fas fa-tools',
        'description': 'IDE, компиляторы, отладчики, цепочка инструментов (toolchain) для МК',
        'lessons': [
            {
                'order': 1,
                'title': 'Цепочка инструментов (toolchain) для МК',
                'estimated_minutes': 25,
                'content': (
                    '<h2>Toolchain для разработки ПО встраиваемых систем</h2>'
                    '<p>Toolchain — набор программных инструментов для превращения исходного кода в прошивку МК.</p>'
                    '<h3>Составляющие toolchain</h3>'
                    '<table>'
                    '<tr><th>Инструмент</th><th>Назначение</th><th>Пример</th></tr>'
                    '<tr><td>Компилятор</td><td>Исходный код (.c) → объектный файл (.o)</td><td>arm-none-eabi-gcc, IAR EW</td></tr>'
                    '<tr><td>Ассемблер</td><td>Ассемблер (.s) → объектный файл (.o)</td><td>arm-none-eabi-as</td></tr>'
                    '<tr><td>Компоновщик (линкер)</td><td>Объектные файлы → ELF/HEX/BIN</td><td>arm-none-eabi-ld, LD script</td></tr>'
                    '<tr><td>Отладчик</td><td>Пошаговое выполнение, точки останова</td><td>arm-none-eabi-gdb, OpenOCD</td></tr>'
                    '<tr><td>Программатор</td><td>Загрузка прошивки в Flash МК</td><td>STM32CubeProgrammer, JTAG/SWD</td></tr>'
                    '<tr><td>Менеджер сборки</td><td>Автоматизация компиляции</td><td>Make, CMake, SCons</td></tr>'
                    '</table>'
                    '<h3>GNU ARM Embedded Toolchain (arm-none-eabi-gcc)</h3>'
                    '<p>Бесплатный, кросс-платформенный GCC для ARM Cortex-M/R. Стандарт для open-source разработки.</p>'
                    '<pre><code># Компиляция:\narm-none-eabi-gcc -mcpu=cortex-m3 -mthumb -O2 -c main.c -o main.o\n\n# Компоновка:\narm-none-eabi-gcc -T linker.ld -o firmware.elf main.o startup.o\n\n# Конвертация в HEX для прошивки:\narm-none-eabi-objcopy -O ihex firmware.elf firmware.hex\n\n# Размер прошивки:\narm-none-eabi-size firmware.elf</code></pre>'
                    '<h3>Важные флаги компилятора для МК</h3>'
                    '<table>'
                    '<tr><th>Флаг</th><th>Назначение</th></tr>'
                    '<tr><td>-mcpu=cortex-m3</td><td>Целевое ядро</td></tr>'
                    '<tr><td>-mthumb</td><td>Набор инструкций Thumb-2 (компактный)</td></tr>'
                    '<tr><td>-O2</td><td>Оптимизация скорости</td></tr>'
                    '<tr><td>-Os</td><td>Оптимизация размера кода</td></tr>'
                    '<tr><td>-g</td><td>Отладочная информация</td></tr>'
                    '<tr><td>-Wall -Wextra</td><td>Все предупреждения</td></tr>'
                    '<tr><td>-ffunction-sections -fdata-sections</td><td>Позволяет линкеру удалять неиспользуемый код</td></tr>'
                    '<tr><td>--specs=nano.specs</td><td>Облегчённая libc (экономия Flash)</td></tr>'
                    '</table>'
                    '<div class="tip">-Wl,--gc-sections совместно с -ffunction-sections убирает неиспользуемые функции из прошивки. '
                    'Типичная экономия: 5–30% Flash на проектах с большими библиотеками.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'IDE для разработки встраиваемых систем',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Среды разработки (IDE) для встраиваемых систем</h2>'
                    '<table>'
                    '<tr><th>IDE</th><th>Производитель</th><th>Лицензия</th><th>Особенности</th></tr>'
                    '<tr><td>STM32CubeIDE</td><td>STMicroelectronics</td><td>Бесплатная</td><td>На основе Eclipse, интегрирован STM32CubeMX, HAL, отладчик</td></tr>'
                    '<tr><td>Keil MDK-ARM</td><td>ARM/Keil</td><td>Платная (бесплатно до 32КБ)</td><td>IDE + RTX RTOS, Pack Manager, профилировщик</td></tr>'
                    '<tr><td>IAR Embedded Workbench</td><td>IAR Systems</td><td>Платная</td><td>Лучший оптимизатор кода, сертифицирован DO-178C/IEC 62304</td></tr>'
                    '<tr><td>VS Code + PlatformIO</td><td>Microsoft + Сообщество</td><td>Бесплатная</td><td>Гибкая, поддерживает сотни плат, Arduino/STM32/ESP32</td></tr>'
                    '<tr><td>Eclipse + GNU ARM</td><td>Eclipse Foundation</td><td>Бесплатная</td><td>Классика, настраиваемая, сложная в настройке</td></tr>'
                    '</table>'
                    '<h3>STM32CubeIDE — рабочий процесс</h3>'
                    '<ol>'
                    '<li>Создать проект: File → New STM32 Project → выбрать МК</li>'
                    '<li>STM32CubeMX: настроить периферию через GUI (тактирование, GPIO, UART и т.д.)</li>'
                    '<li>Генерация кода: нажать "Generate Code" → создаст HAL-инициализацию</li>'
                    '<li>Написать логику в <code>main.c</code> в секциях <code>/* USER CODE BEGIN */</code></li>'
                    '<li>Сборка: Build (Ctrl+B), загрузка: Run → Debug или Flash</li>'
                    '<li>Отладка: точки останова, пошаговое выполнение, просмотр регистров/памяти</li>'
                    '</ol>'
                    '<h3>PlatformIO (VS Code) — рабочий процесс</h3>'
                    '<pre><code># platformio.ini:\n[env:bluepill_f103c8]\nplatform = ststm32\nboard = bluepill_f103c8\nframework = arduino  ; или stm32cube\nbuild_flags = -DUSE_HAL_DRIVER -DSTM32F103xB\n\n# Сборка:\npio run\n# Загрузка:\npio run --target upload\n# Монитор порта:\npio device monitor --baud 115200</code></pre>'
                    '<div class="tip">STM32CubeIDE — лучший выбор для начала: официальная, бесплатная, с визуальным конфигуратором. '
                    'PlatformIO + VS Code — для опытных и CI/CD. Keil/IAR — для коммерческих проектов с сертификацией.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Интерфейсы отладки: JTAG и SWD',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Интерфейсы отладки: JTAG и SWD</h2>'
                    '<h3>JTAG (Joint Test Action Group, IEEE 1149.1)</h3>'
                    '<ul>'
                    '<li>Разработан в 1990 для тестирования плат</li>'
                    '<li>5 сигналов: TDI, TDO, TCK, TMS, TRST</li>'
                    '<li>Цепочка (scan chain): несколько устройств последовательно</li>'
                    '<li>Возможности: граничное сканирование, пошаговая отладка, программирование Flash</li>'
                    '</ul>'
                    '<h3>SWD (Serial Wire Debug) — ARM-специфичный</h3>'
                    '<ul>'
                    '<li>Только 2 сигнала: SWDIO (данные) + SWCLK (тактирование)</li>'
                    '<li>Меньше пинов = удобнее на компактных МК</li>'
                    '<li>Те же возможности: пошаговое выполнение, точки останова, просмотр памяти</li>'
                    '<li>Стандарт для всех STM32, nRF52, RP2040</li>'
                    '</ul>'
                    '<h3>Сравнение</h3>'
                    '<table>'
                    '<tr><th>Параметр</th><th>JTAG</th><th>SWD</th></tr>'
                    '<tr><td>Сигналы</td><td>4–5</td><td>2</td></tr>'
                    '<tr><td>Скорость</td><td>До 100 МГц</td><td>До 10 МГц</td></tr>'
                    '<tr><td>Цепочка</td><td>Да</td><td>Нет (один МК)</td></tr>'
                    '<tr><td>Поддержка ARM</td><td>Да</td><td>Да (Cortex-M)</td></tr>'
                    '<tr><td>Применение</td><td>Сложные платы, FPGA</td><td>МК STM32, nRF</td></tr>'
                    '</table>'
                    '<h3>Адаптеры</h3>'
                    '<table>'
                    '<tr><th>Адаптер</th><th>Интерфейс</th><th>Стоимость</th><th>Применение</th></tr>'
                    '<tr><td>ST-Link V2/V3</td><td>SWD/JTAG</td><td>$3–30</td><td>STM32 (встроен в Nucleo)</td></tr>'
                    '<tr><td>J-Link (Segger)</td><td>SWD/JTAG</td><td>$60–600</td><td>Профессиональный, любой ARM</td></tr>'
                    '<tr><td>CMSIS-DAP (DAPLink)</td><td>SWD/JTAG</td><td>$5–20</td><td>Открытый стандарт ARM</td></tr>'
                    '<tr><td>Black Magic Probe</td><td>SWD/JTAG</td><td>$40–60</td><td>GDB-сервер на борту</td></tr>'
                    '</table>'
                    '<div class="tip">На платах Nucleo ST-Link встроен. "Blue Pill" (STM32F103) требует внешний ST-Link V2 (~300 руб.). '
                    'Для работы в STM32CubeIDE достаточно ST-Link V2.</div>'
                ),
            },
            {
                'order': 4,
                'title': 'Сборочные системы: Make и CMake',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Автоматизация сборки: Make и CMake</h2>'
                    '<h3>Make и Makefile</h3>'
                    '<p>Make — классическая утилита сборки. Описывает зависимости и команды в <code>Makefile</code>.</p>'
                    '<pre><code># Makefile для STM32\nTARGET = firmware\nCPU    = -mcpu=cortex-m3 -mthumb\nOPT    = -O2\n\nSRCS = main.c system_stm32f1xx.c\nOBJS = $(SRCS:.c=.o)\n\n$(TARGET).elf: $(OBJS)\n\tarm-none-eabi-gcc $(CPU) -T linker.ld -o $@ $^\n\n%.o: %.c\n\tarm-none-eabi-gcc $(CPU) $(OPT) -c $< -o $@\n\nflash:\n\tst-flash write $(TARGET).bin 0x08000000\n\nclean:\n\trm -f $(OBJS) $(TARGET).elf</code></pre>'
                    '<h3>CMake</h3>'
                    '<p>CMake — современная кросс-платформенная система сборки. Генерирует Makefile, Ninja или проекты IDE.</p>'
                    '<pre><code># CMakeLists.txt\ncmake_minimum_required(VERSION 3.22)\nproject(my_stm32 C ASM)\n\nset(CMAKE_SYSTEM_NAME Generic)\nset(CMAKE_C_COMPILER arm-none-eabi-gcc)\n\nadd_executable(firmware main.c startup_stm32f103xb.s)\n\ntarget_compile_options(firmware PRIVATE\n    -mcpu=cortex-m3 -mthumb -O2 -Wall\n)\ntarget_link_options(firmware PRIVATE\n    -T${CMAKE_SOURCE_DIR}/linker.ld\n    -Wl,--gc-sections\n)\n\n# Генерация HEX\nadd_custom_command(TARGET firmware POST_BUILD\n    COMMAND arm-none-eabi-objcopy -O ihex firmware firmware.hex\n)</code></pre>'
                    '<h3>Ninja (ускоренная сборка)</h3>'
                    '<pre><code>cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..\nninja -j4  # 4 параллельных задания</code></pre>'
                    '<div class="tip">STM32CubeIDE и PlatformIO генерируют Makefile автоматически. '
                    'CMake становится стандартом для больших проектов: хорошо интегрируется с CLion, VS Code, CI/CD.</div>'
                ),
            },
        ],
    },
    {
        'order': 6,
        'title': 'ЕСПД и техническая документация ПО',
        'icon': 'fas fa-file-alt',
        'description': 'Стандарты ЕСПД, ГОСТ 19, структура программной документации',
        'lessons': [
            {
                'order': 1,
                'title': 'ЕСПД: стандарты и состав документации',
                'estimated_minutes': 20,
                'content': (
                    '<h2>ЕСПД — Единая система программной документации</h2>'
                    '<p>ЕСПД — комплекс государственных стандартов СССР/России (ГОСТ 19.xxx), '
                    'регламентирующих состав, разработку, оформление и обращение программной документации.</p>'
                    '<h3>Основные стандарты ЕСПД</h3>'
                    '<table>'
                    '<tr><th>ГОСТ</th><th>Название</th></tr>'
                    '<tr><td>ГОСТ 19.001-77</td><td>Общие положения</td></tr>'
                    '<tr><td>ГОСТ 19.101-77</td><td>Виды программ и программных документов</td></tr>'
                    '<tr><td>ГОСТ 19.102-77</td><td>Стадии разработки</td></tr>'
                    '<tr><td>ГОСТ 19.103-77</td><td>Обозначение программ и программных документов</td></tr>'
                    '<tr><td>ГОСТ 19.104-78</td><td>Основные надписи</td></tr>'
                    '<tr><td>ГОСТ 19.105-78</td><td>Общие требования к программным документам</td></tr>'
                    '<tr><td>ГОСТ 19.201-78</td><td>Техническое задание. Требования к содержанию и оформлению</td></tr>'
                    '<tr><td>ГОСТ 19.301-79</td><td>Программа и методика испытаний</td></tr>'
                    '<tr><td>ГОСТ 19.402-78</td><td>Описание программы</td></tr>'
                    '<tr><td>ГОСТ 19.501-78</td><td>Формуляр. Требования к содержанию и оформлению</td></tr>'
                    '<tr><td>ГОСТ 19.502-78</td><td>Описание применения</td></tr>'
                    '<tr><td>ГОСТ 19.601-78</td><td>Правила дублирования, учёта и хранения</td></tr>'
                    '</table>'
                    '<h3>Стадии разработки (ГОСТ 19.102-77)</h3>'
                    '<ol>'
                    '<li><strong>Техническое задание (ТЗ)</strong> — требования к ПО</li>'
                    '<li><strong>Эскизный проект</strong> — предварительное решение</li>'
                    '<li><strong>Технический проект</strong> — окончательные технические решения</li>'
                    '<li><strong>Рабочий проект</strong> — полная документация для изготовления</li>'
                    '<li><strong>Внедрение</strong> — сдача заказчику</li>'
                    '</ol>'
                    '<div class="tip">ЕСПД — советский стандарт 1977–1979 гг. В коммерческих проектах его заменяют '
                    'гибкие методологии (Agile, Scrum), но ЕСПД обязателен для государственных контрактов в России.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'Техническое задание на ПО (ГОСТ 19.201-78)',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Техническое задание на разработку ПО</h2>'
                    '<h3>Структура ТЗ по ГОСТ 19.201-78</h3>'
                    '<ol>'
                    '<li><strong>Введение</strong> — наименование программы, краткое описание назначения</li>'
                    '<li><strong>Основания для разработки</strong> — документ (договор, приказ), организация</li>'
                    '<li><strong>Назначение разработки</strong> — функциональное и эксплуатационное назначение</li>'
                    '<li><strong>Требования к программе</strong>:'
                    '<ul>'
                    '<li>Требования к функциональным характеристикам</li>'
                    '<li>Требования к надёжности</li>'
                    '<li>Условия эксплуатации</li>'
                    '<li>Требования к составу и параметрам технических средств</li>'
                    '<li>Требования к информационной и программной совместимости</li>'
                    '</ul></li>'
                    '<li><strong>Требования к программной документации</strong> — перечень документов</li>'
                    '<li><strong>Технико-экономические показатели</strong> — ориентировочная стоимость</li>'
                    '<li><strong>Стадии и этапы разработки</strong> — план с датами</li>'
                    '<li><strong>Порядок контроля и приёмки</strong> — критерии приёмки</li>'
                    '</ol>'
                    '<h3>Пример требований к ПО МК (фрагмент ТЗ)</h3>'
                    '<pre><code>3. Требования к программе\n\n'
                    '3.1 Требования к функциональным характеристикам:\n'
                    '    - Измерение температуры с точностью ±0,5°C в диапазоне -40..+125°C\n'
                    '    - Период измерения: 1 секунда\n'
                    '    - Передача данных по UART 115200 бод\n'
                    '    - Отображение на LCD 16x2\n\n'
                    '3.2 Требования к надёжности:\n'
                    '    - Watchdog-таймер с периодом 1 сек\n'
                    '    - Перезапуск при зависании не более 1 секунды\n'
                    '    - MTBF не менее 50 000 часов\n\n'
                    '3.3 Требования к аппаратным средствам:\n'
                    '    - МК STM32F103C8T6 или совместимый\n'
                    '    - Питание 3.3V ± 5%\n'
                    '    - Температурный диапазон: -20..+70°C</code></pre>'
                    '<div class="tip">В реальных проектах ТЗ — юридически значимый документ. '
                    'Требования должны быть однозначными, проверяемыми (можно написать тест) и достижимыми.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Описание программы и руководство пользователя',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Описание программы и руководство пользователя</h2>'
                    '<h3>Описание программы (ГОСТ 19.402-78)</h3>'
                    '<p>Документ содержит сведения о логической структуре и функционировании программы.</p>'
                    '<table>'
                    '<tr><th>Раздел</th><th>Содержание</th></tr>'
                    '<tr><td>Общие сведения</td><td>Обозначение, наименование, ЯП, ОС/платформа</td></tr>'
                    '<tr><td>Функциональное назначение</td><td>Что делает программа</td></tr>'
                    '<tr><td>Описание логической структуры</td><td>Алгоритм, блок-схема, структура данных</td></tr>'
                    '<tr><td>Используемые технические средства</td><td>Аппаратные требования</td></tr>'
                    '<tr><td>Вызов и загрузка</td><td>Способ запуска, параметры</td></tr>'
                    '<tr><td>Входные данные</td><td>Форматы, источники</td></tr>'
                    '<tr><td>Выходные данные</td><td>Форматы, получатели</td></tr>'
                    '</table>'
                    '<h3>Руководство программиста (для МК-ПО)</h3>'
                    '<ul>'
                    '<li>Требования к рабочей среде: IDE, компилятор, версии</li>'
                    '<li>Структура каталогов проекта</li>'
                    '<li>Порядок сборки и прошивки</li>'
                    '<li>Описание конфигурационных параметров (<code>#define</code> в config.h)</li>'
                    '<li>Описание HAL-функций и API модулей</li>'
                    '<li>Диаграмма конечного автомата основного цикла</li>'
                    '</ul>'
                    '<h3>Пример: структура config.h</h3>'
                    '<pre><code>/**\n * @file config.h\n * @brief Конфигурационные параметры прошивки\n *\n * Все параметры, требующие изменения при адаптации,\n * сосредоточены здесь. Не изменять другие файлы.\n */\n\n// Тактовая частота системы\n#define SYSCLK_HZ       72000000UL\n\n// UART для вывода логов\n#define LOG_UART        USART1\n#define LOG_BAUD        115200\n\n// Период измерения датчика (мс)\n#define SENSOR_PERIOD_MS  1000\n\n// Порог тревоги температуры\n#define TEMP_ALARM_C      80.0f</code></pre>'
                    '<div class="tip">Хорошая документация для МК — это прежде всего комментарии в заголовочных файлах '
                    'в формате Doxygen. Они одновременно служат справочником API и генерируют HTML-документацию командой <code>doxygen Doxyfile</code>.</div>'
                ),
            },
        ],
    },
    {
        'order': 7,
        'title': 'Тестирование программного обеспечения',
        'icon': 'fas fa-vial',
        'description': 'Виды тестирования, тест-кейсы, тестирование МК-ПО, CI',
        'lessons': [
            {
                'order': 1,
                'title': 'Виды тестирования ПО',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Виды тестирования программного обеспечения</h2>'
                    '<h3>По уровню тестирования</h3>'
                    '<table>'
                    '<tr><th>Уровень</th><th>Объект</th><th>Выполняет</th><th>Инструменты</th></tr>'
                    '<tr><td>Модульное (Unit)</td><td>Функция, модуль</td><td>Разработчик</td><td>Unity, CppUTest, pytest</td></tr>'
                    '<tr><td>Интеграционное</td><td>Взаимодействие модулей</td><td>Разработчик/QA</td><td>Тестовые стенды, моки</td></tr>'
                    '<tr><td>Системное</td><td>Вся система</td><td>QA</td><td>Автотесты + ручное</td></tr>'
                    '<tr><td>Приёмочное</td><td>Соответствие требованиям</td><td>Заказчик</td><td>ТЗ как чеклист</td></tr>'
                    '</table>'
                    '<h3>По доступу к коду</h3>'
                    '<table>'
                    '<tr><th>Вид</th><th>Доступ к коду</th><th>Что проверяет</th></tr>'
                    '<tr><td>Белый ящик (white-box)</td><td>Полный доступ</td><td>Покрытие ветвей, путей</td></tr>'
                    '<tr><td>Чёрный ящик (black-box)</td><td>Нет</td><td>Функциональность по ТЗ</td></tr>'
                    '<tr><td>Серый ящик (grey-box)</td><td>Частичный</td><td>Интерфейсы, протоколы</td></tr>'
                    '</table>'
                    '<h3>По цели</h3>'
                    '<ul>'
                    '<li><strong>Функциональное</strong> — программа делает то, что указано в ТЗ</li>'
                    '<li><strong>Нагрузочное (stress)</strong> — поведение при максимальной нагрузке</li>'
                    '<li><strong>Регрессионное</strong> — новые изменения не сломали старую функциональность</li>'
                    '<li><strong>Дымовое (smoke)</strong> — базовая работоспособность после сборки</li>'
                    '<li><strong>Безопасности</strong> — устойчивость к атакам и некорректным данным</li>'
                    '</ul>'
                    '<h3>Специфика тестирования МК-ПО</h3>'
                    '<ul>'
                    '<li><strong>Hardware-in-the-loop (HIL):</strong> реальное железо подключено к тестовой системе</li>'
                    '<li><strong>Software-in-the-loop (SIL):</strong> ПО запускается на ПК с симулятором периферии</li>'
                    '<li><strong>Processor-in-the-loop (PIL):</strong> ПО на реальном МК, входные данные с ПК</li>'
                    '</ul>'
                    '<div class="tip">Для безопасно-критичного ПО (ISO 26262, IEC 62304) требуется 100% покрытие ветвей (MC/DC). '
                    'Инструменты: Tessy, VectorCAST, Parasoft.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'Написание тест-кейсов и модульных тестов',
                'estimated_minutes': 25,
                'content': (
                    '<h2>Тест-кейсы и модульное тестирование</h2>'
                    '<h3>Структура тест-кейса</h3>'
                    '<table>'
                    '<tr><th>Поле</th><th>Описание</th><th>Пример</th></tr>'
                    '<tr><td>ID</td><td>Уникальный идентификатор</td><td>TC-UART-001</td></tr>'
                    '<tr><td>Название</td><td>Краткое описание</td><td>Передача строки 64 байта по UART</td></tr>'
                    '<tr><td>Предусловие</td><td>Состояние системы до теста</td><td>UART инициализирован 115200 бод</td></tr>'
                    '<tr><td>Входные данные</td><td>Что подаётся</td><td>Строка "Hello World!" (12 байт)</td></tr>'
                    '<tr><td>Шаги</td><td>Последовательность действий</td><td>1. Вызвать UART_send(buf, 12)</td></tr>'
                    '<tr><td>Ожидаемый результат</td><td>Что должно произойти</td><td>На RX-пине принято "Hello World!" за ≤1 мс</td></tr>'
                    '<tr><td>Статус</td><td>Pass/Fail</td><td>Pass</td></tr>'
                    '</table>'
                    '<h3>Модульные тесты с Unity (для МК)</h3>'
                    '<pre><code>#include "unity.h"\n#include "crc16.h"\n\nvoid setUp(void) {}\nvoid tearDown(void) {}\n\nvoid test_crc16_known_value(void) {\n    uint8_t data[] = {0x31, 0x32, 0x33};\n    uint16_t crc = crc16_calc(data, sizeof(data));\n    TEST_ASSERT_EQUAL_HEX16(0x6F91, crc);\n}\n\nvoid test_crc16_empty(void) {\n    uint16_t crc = crc16_calc(NULL, 0);\n    TEST_ASSERT_EQUAL_HEX16(0xFFFF, crc);\n}\n\nint main(void) {\n    UNITY_BEGIN();\n    RUN_TEST(test_crc16_known_value);\n    RUN_TEST(test_crc16_empty);\n    return UNITY_END();\n}</code></pre>'
                    '<h3>Техника граничных значений</h3>'
                    '<p>Тестировать не только типичные значения, но и граничные:</p>'
                    '<ul>'
                    '<li>Минимальное значение (0, NULL, пустой массив)</li>'
                    '<li>Максимальное значение (255 для uint8, 65535 для uint16)</li>'
                    '<li>Максимум - 1 и Максимум + 1</li>'
                    '<li>Некорректный ввод (отрицательное, переполнение)</li>'
                    '</ul>'
                    '<div class="tip">Запускайте Unity-тесты на ПК (native GCC), не на МК — быстрее и удобнее для CI. '
                    'Логику изолируйте от железа через HAL-абстракцию, тогда тесты не требуют реального МК.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Метрики качества и покрытие кода',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Метрики качества ПО и покрытие кода</h2>'
                    '<h3>Метрики тестирования</h3>'
                    '<table>'
                    '<tr><th>Метрика</th><th>Формула</th><th>Хороший порог</th></tr>'
                    '<tr><td>Покрытие строк (Line Coverage)</td><td>Исполненные строки / Все строки</td><td>> 80%</td></tr>'
                    '<tr><td>Покрытие ветвей (Branch Coverage)</td><td>Пройденные ветви / Все ветви</td><td>> 70%</td></tr>'
                    '<tr><td>MC/DC Coverage</td><td>Каждое условие влияет на результат</td><td>100% для DO-178B уровня A</td></tr>'
                    '<tr><td>Плотность дефектов</td><td>Дефектов / KLOC (тысяч строк)</td><td>< 1 дефекта/KLOC</td></tr>'
                    '</table>'
                    '<h3>Покрытие кода с gcov/lcov</h3>'
                    '<pre><code># Компиляция с флагами покрытия:\ngcc -fprofile-arcs -ftest-coverage -o test_crc test_crc.c crc16.c\n./test_crc\n\n# Генерация отчёта:\ngcov crc16.c\nlcov --capture --directory . --output-file coverage.info\ngenhtml coverage.info --output-directory coverage_report\n# Открыть coverage_report/index.html в браузере</code></pre>'
                    '<h3>Статический анализ кода</h3>'
                    '<table>'
                    '<tr><th>Инструмент</th><th>Что ищет</th><th>Лицензия</th></tr>'
                    '<tr><td>cppcheck</td><td>Разыменование NULL, выход за массив</td><td>Бесплатный</td></tr>'
                    '<tr><td>clang-tidy</td><td>Стиль, паттерны ошибок</td><td>Бесплатный</td></tr>'
                    '<tr><td>PC-lint (Gimpel)</td><td>MISRA C compliance</td><td>Коммерческий</td></tr>'
                    '<tr><td>Polyspace (MathWorks)</td><td>Формальная верификация</td><td>Коммерческий</td></tr>'
                    '</table>'
                    '<h3>MISRA C</h3>'
                    '<p>MISRA C — стандарт безопасного кодирования на Си для встраиваемых систем (automotive, medical). '
                    'Запрещает опасные конструкции: рекурсию, динамическое выделение памяти, goto, goto и т.д.</p>'
                    '<div class="tip">cppcheck + clang-tidy запускаются бесплатно в GitHub Actions/GitLab CI. '
                    'Настройте их как обязательный шаг pipeline — любой коммит с ошибкой анализа блокирует мерж.</div>'
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed РВЭС модули M5-M7: инструменты, ЕСПД, тестирование'

    def handle(self, *args, **options):
        subject = Subject.objects.filter(slug='rves').first()
        if not subject:
            self.stderr.write('Subject rves not found')
            return

        for mod_data in MODULES:
            lessons_data = mod_data.pop('lessons')
            module, created = TheoryModule.objects.update_or_create(
                subject=subject,
                order=mod_data['order'],
                defaults={**mod_data, 'subject': subject},
            )
            tag = 'created' if created else 'updated'
            self.stdout.write(f'  Module M{mod_data["order"]}: {mod_data["title"]} [{tag}]')

            for lesson in lessons_data:
                TheoryLesson.objects.update_or_create(
                    module=module,
                    order=lesson['order'],
                    defaults={**lesson, 'module': module},
                )
            self.stdout.write(f'    → {len(lessons_data)} lessons')
            mod_data['lessons'] = lessons_data

        self.stdout.write(self.style.SUCCESS('Done: РВЭС M5-M7 seeded'))
