from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, PracticalWork, Quiz, Question, AnswerChoice

PRACTICAL_WORKS = [
    {'order': 1, 'title': 'ПР1: Управление GPIO и светодиод',
     'theory_module_order': 1,
     'difficulty': 'easy', 'max_score': 10, 'language': 'c',
     'description': '''Написать программу управления светодиодом на STM32 (HAL).

Задание:
1. Инициализировать PA5 (LED2 на Nucleo-F411RE) как выход Push-Pull.
2. Реализовать мигание 2 Гц (250 мс ON / 250 мс OFF) через HAL_Delay.
3. Подключить кнопку PC13 как вход с подтяжкой PULLUP.
4. При нажатии кнопки — изменять частоту мигания на 1 Гц (500/500 мс).
5. Вывести в UART (115200 8N1) строку "Button pressed!" при каждом нажатии.

Требования к коду:
- Использовать только HAL (не напрямую регистры).
- Кнопку читать через HAL_GPIO_ReadPin.
- Для UART: HAL_UART_Transmit или printf с retarget.
- Код должен компилироваться без предупреждений (-Wall).

Оформление: загрузить main.c (или архив проекта .zip).''',
     'input_example': 'Состояние кнопки (нажата/не нажата)',
     'output_example': 'LED мигает 2 Гц; при нажатии — 1 Гц; UART: "Button pressed!"'},

    {'order': 2, 'title': 'ПР2: Таймер и прерывания (TIM + EXTI)',
     'theory_module_order': 2,
     'difficulty': 'medium', 'max_score': 15, 'language': 'c',
     'description': '''Реализовать управление LED через аппаратный таймер и внешнее прерывание.

Задание:
1. Настроить TIM2 на переполнение 2 Гц (без HAL_Delay). Мигать LED в ISR.
2. Настроить EXTI на PC13 (кнопка, спадающий фронт).
3. В обработчике EXTI: переключать период между 250 мс и 1000 мс.
4. Счётчик нажатий вывести через UART каждые 5 нажатий.
5. Реализовать программный антидребезг: игнорировать повторные нажатия в течение 50 мс.

Вычисление параметров TIM2:
- TIM2_CLK = 84 МГц (APB1 x2 на STM32F411).
- PSC и ARR рассчитать для нужной частоты.
- Формула: f = TIM_CLK / ((PSC+1) * (ARR+1)).

Дополнительно (+2 балла): добавить PWM на PA6 (TIM3 CH1) — яркость LED пропорционально счётчику нажатий.

Оформление: загрузить main.c и файл с расчётами PSC/ARR.''',
     'input_example': 'Нажатия кнопки PC13',
     'output_example': 'LED мигает через таймер; UART показывает счётчик нажатий'},

    {'order': 3, 'title': 'ПР3: UART и SPI — работа с периферией',
     'theory_module_order': 3,
     'difficulty': 'medium', 'max_score': 15, 'language': 'c',
     'description': '''Реализовать обмен данными по UART и SPI.

Задание часть A — UART (10 баллов):
1. Настроить USART1 на 115200 8N1 (PA9=TX, PA10=RX).
2. Реализовать приём команд через прерывание (HAL_UART_Receive_IT).
3. Поддержать команды:
   - "LED ON\\r\\n" — включить PA5
   - "LED OFF\\r\\n" — выключить PA5
   - "STATUS\\r\\n" — ответить JSON: {"led":1,"btn":0}
4. На неизвестную команду: "ERR: unknown\\r\\n".

Задание часть B — SPI Loopback (+5 баллов):
1. Настроить SPI1 Master (PA5=SCK, PA6=MISO, PA7=MOSI, PA4=NSS_soft).
2. Соединить MOSI и MISO перемычкой (loopback).
3. Передать массив {0x01, 0x02, 0x03, 0xAA, 0xFF}.
4. Принять обратно и вывести через UART в формате HEX.
5. Сравнить TX и RX: вывести "PASS" или "FAIL".

Оформление: загрузить main.c и скриншот терминала (PuTTY/Tera Term).''',
     'input_example': 'Команды через UART: "LED ON", "STATUS"',
     'output_example': '{"led":1,"btn":0}, PASS (SPI loopback)'},

    {'order': 4, 'title': 'ПР4: FreeRTOS — две задачи и очередь',
     'theory_module_order': 4,
     'difficulty': 'hard', 'max_score': 20, 'language': 'c',
     'description': '''Реализовать многозадачное приложение на FreeRTOS (STM32CubeIDE + CMSIS-RTOS v2).

Задание:
1. Создать задачу vLedTask (приоритет 1, стек 128 слов):
   - Мигать PA5 каждые 500 мс через osDelay.

2. Создать задачу vSensorTask (приоритет 2, стек 256 слов):
   - Каждые 1000 мс читать ADC1 Channel0 (PA0).
   - Преобразовать в напряжение: V = ADC * 3.3 / 4096.
   - Положить SensorData_t {voltage, tick} в очередь.

3. Создать задачу vUartTask (приоритет 1, стек 256 слов):
   - Читать из очереди (osMessageQueueGet, таймаут 2000 мс).
   - Вывести через UART: "V=2.31 T=1234\\r\\n".

4. Обработка ошибок:
   - При таймауте очереди — вывести "TIMEOUT\\r\\n".
   - Проверить HWM всех задач при старте и вывести через UART.

Структура данных:
typedef struct { float voltage; uint32_t tick; } SensorData_t;

Дополнительно (+3 балла): добавить мьютекс для UART (защита от race condition).

Оформление: main.c, FreeRTOSConfig.h (если изменён), скриншот UART-вывода.''',
     'input_example': 'Напряжение на PA0 (потенциометр)',
     'output_example': 'UART: "V=1.65 T=1000", "V=1.70 T=2000" каждую секунду'},

    {'order': 5, 'title': 'ПР5: Toolchain — сборка проекта через Makefile',
     'theory_module_order': 5,
     'difficulty': 'medium', 'max_score': 15, 'language': 'c',
     'description': '''Настроить сборку STM32-проекта через Makefile (без IDE).

Задание:
1. Взять минимальный проект мигания LED (main.c + startup.s + linker.ld).
2. Написать Makefile с целями:
   - all — сборка firmware.elf, firmware.bin
   - flash — прошивка через st-flash
   - clean — удалить артефакты
   - size — вывести arm-none-eabi-size
3. Параметры сборки:
   - CC = arm-none-eabi-gcc
   - CFLAGS = -mcpu=cortex-m4 -mthumb -O2 -Wall -Wextra
   - Флаги для HAL: -DSTM32F411xE -DUSE_HAL_DRIVER
4. Добавить правило .c → .o с выводом зависимостей (-MMD).
5. Подключить 2–3 файла HAL (stm32f4xx_hal.c, stm32f4xx_hal_gpio.c, stm32f4xx_hal_uart.c).

Проверка:
- make all должен пройти без ошибок.
- make size — вывести размеры секций text/data/bss.
- Скриншот вывода make.

Оформление: загрузить Makefile и скриншот make all.''',
     'input_example': 'Исходный код main.c и HAL',
     'output_example': 'firmware.elf, вывод arm-none-eabi-size'},

    {'order': 6, 'title': 'ПР6: Техническая документация — ТЗ по ГОСТ 19.201',
     'theory_module_order': 6,
     'difficulty': 'easy', 'max_score': 10, 'language': 'c',
     'description': '''Разработать техническое задание на программу по ГОСТ 19.201-78.

Тема программы (выбрать одну):
A. Система мониторинга температуры на STM32 + UART.
B. Контроллер управления сервоприводом по UART-командам.
C. Регистратор данных (datalogger) на STM32 + SPI Flash W25Q.

Структура ТЗ (обязательные разделы по ГОСТ 19.201):
1. Введение — наименование программы, краткая характеристика.
2. Основания для разработки — документ, организация.
3. Назначение разработки — функциональное и эксплуатационное.
4. Требования к программе:
   а) требования к функциональным характеристикам (что делает);
   б) требования к надёжности;
   в) условия эксплуатации;
   г) требования к составу и параметрам технических средств (МК, частота, ОЗУ);
   д) требования к программной документации.
5. Технико-экономические показатели.
6. Стадии и этапы разработки.
7. Порядок контроля и приёмки.

Требования к оформлению:
- Шрифт Times New Roman 12–14 пт, интервал 1.5.
- Нумерация ГОСТ 19.103-77 (обозначение: ХХ.ХХХ.ХХХ ТЗ).
- Объём: 3–5 страниц.

Оформление: загрузить .docx или .pdf.''',
     'input_example': 'Выбранная тема проекта',
     'output_example': 'ТЗ по ГОСТ 19.201 в формате .docx/.pdf'},

    {'order': 7, 'title': 'ПР7: Тестирование с Unity Framework',
     'theory_module_order': 7,
     'difficulty': 'medium', 'max_score': 15, 'language': 'c',
     'description': '''Написать модульные тесты для функций обработки данных датчика с помощью Unity.

Тестируемые функции (реализовать самостоятельно):
1. float ntc_to_celsius(uint16_t adc, float r_ref, float b_coef) — перевод показаний NTC-термистора в °C (формула Стейнхарта-Харта или B-параметрическая).
2. uint16_t crc16_modbus(uint8_t *buf, uint16_t len) — расчёт CRC16 для Modbus.
3. int parse_cmd(char *input, char *cmd, int *value) — парсинг команды "LED 1" → cmd="LED", value=1, returns 0 или -1 при ошибке.

Требования к тестам (Unity):
- Минимум 5 тестов для каждой функции (итого ≥ 15 тестов).
- Тесты должны проверять: нормальные значения, граничные значения, ошибочный ввод.
- Использовать: TEST_ASSERT_EQUAL_FLOAT, TEST_ASSERT_EQUAL_UINT16, TEST_ASSERT_EQUAL_INT.
- Запускать на ПК (gcc, не МК): Makefile с target test.
- Вывод: "X Tests, 0 Failures, 0 Ignored".

Структура проекта:
src/ntc.c, src/crc16.c, src/cmd_parser.c
tests/test_ntc.c, tests/test_crc16.c, tests/test_cmd.c
Makefile (target test: gcc + unity.c + test files)

Оформление: архив .zip проекта + скриншот вывода тестов.''',
     'input_example': 'Тестовые данные: ADC=2048, buf[]={0x01,0x03,0x00,0x00,0x00,0x02}',
     'output_example': '15 Tests, 0 Failures, 0 Ignored'},

    {'order': 8, 'title': 'ПР8: Git-workflow и код-ревью',
     'theory_module_order': 8,
     'difficulty': 'easy', 'max_score': 10, 'language': 'c',
     'description': '''Отработать командный Git-процесс и провести рефакторинг кода.

Задание часть A — Git workflow (5 баллов):
1. Инициализировать репозиторий: git init + первый commit с "Initial: empty project".
2. Создать ветку feature/led-blink от main.
3. Написать код мигания LED (main.c).
4. Сделать commit по conventional commits: "feat: add LED blink 2 Hz".
5. Создать ветку feature/uart от main.
6. Написать UART init (uart.c, uart.h).
7. Commit: "feat: add UART 115200 init".
8. Сделать merge feature/led-blink в main (fast-forward).
9. Сделать merge feature/uart в main (merge commit — будет конфликт если есть).
10. Вывести: git log --oneline --graph --all.

Задание часть B — Рефакторинг (5 баллов):
Дан исходный код (скачать ниже — bad_code.c). Провести рефакторинг:
1. Выделить Magic Numbers в именованные константы (#define или const).
2. Разбить функцию длиннее 40 строк на функции.
3. Убрать глобальные переменные там, где можно передать параметром.
4. Добавить enum для состояний конечного автомата (если есть).

Оформление: архив .zip (репозиторий) + вывод git log --graph + файл до/после рефакторинга.''',
     'input_example': 'Исходный код bad_code.c',
     'output_example': 'git log --graph + рефакторированный код'},

    {'order': 9, 'title': 'ПР9: Подключение датчиков — I2C и 1-Wire',
     'theory_module_order': 9,
     'difficulty': 'hard', 'max_score': 20, 'language': 'c',
     'description': '''Подключить и опросить два датчика: BME280 (I2C) и DS18B20 (1-Wire).

Задание часть A — BME280 по I2C (12 баллов):
Датчик атмосферного давления, влажности и температуры.
1. Подключить: SDA=PB7, SCL=PB6, VCC=3.3V, GND. Адрес 0x76 или 0x77 (зависит от SDO).
2. Реализовать I2C_ReadReg() и I2C_WriteReg() через HAL_I2C_Mem_Read/Write.
3. Инициализировать BME280: режим Normal, oversampling x4 (temp/pres/hum).
4. Прочитать и применить калибровочные коэффициенты (из datasheet BME280).
5. Каждые 2 секунды вывести через UART:
   T=23.45C H=55.2% P=1013.5hPa

Задание часть B — DS18B20 по 1-Wire (+8 баллов):
1. Подключить: DQ=PA1, подтяжка 4.7 кОм к 3.3В.
2. Реализовать 1-Wire протокол (Reset+Presence, Write Byte, Read Byte).
3. Команды: SKIP ROM (0xCC), CONVERT T (0x44), READ SCRATCHPAD (0xBE).
4. Прочитать температуру, перевести из формата 12-bit в float (шаг 0.0625°C).
5. Вывести: "DS18B20: 23.125C".
6. Сравнить с BME280 температурой — вывести разницу.

Оформление: main.c (или архив), скриншот UART-вывода.''',
     'input_example': 'Датчики BME280 и DS18B20 подключены к STM32',
     'output_example': 'UART: T=23.45C H=55.2% P=1013.5hPa | DS18B20: 23.125C'},

    {'order': 10, 'title': 'ПР10: Финальный проект — FreeRTOS мониторинг',
     'theory_module_order': 10,
     'difficulty': 'hard', 'max_score': 25, 'language': 'c',
     'description': '''Разработать систему мониторинга параметров среды на FreeRTOS.

Состав системы:
- МК: STM32F411RE (Nucleo-F411RE)
- Датчик: BME280 (I2C) или DHT22 (1-Wire-like)
- Дисплей: OLED SSD1306 128x64 (I2C)
- Интерфейс: UART 115200

Задание:
1. Задача vSensorTask (приоритет 3, каждые 2 с):
   - Читать BME280/DHT22: температуру, влажность.
   - Класть SensorReading_t в очередь xSensorQueue (глубина 5).

2. Задача vDisplayTask (приоритет 2, каждые 500 мс):
   - Читать из очереди (неблокирующий вызов).
   - Показывать на OLED: строка 1 "T: 23.4 C", строка 2 "H: 55%".
   - Использовать мьютекс для шины I2C (разделяется с vSensorTask).

3. Задача vUartTask (приоритет 1, каждые 5 с):
   - Вывести в UART JSON: {"t":23.4,"h":55,"uptime":12345}
   - Принимать команды "RESET" (перезапуск), "STATUS" (ответить немедленно).

4. Сторожевой таймер IWDG (4 с):
   - Сбрасывать только если все 3 задачи "живы" (маска активности).

5. Мониторинг ресурсов (при старте):
   - Вывести HWM стека каждой задачи.
   - Вывести свободную кучу FreeRTOS.

Минимальные баллы за каждую часть:
- Задачи без очереди: 10 б
- Очередь + мьютекс: +5 б
- OLED + UART JSON: +5 б
- IWDG + мониторинг: +5 б

Оформление: архив проекта + видео/скриншот работающей системы.''',
     'input_example': 'Данные BME280/DHT22, UART-команды',
     'output_example': 'OLED показывает T/H; UART JSON каждые 5 с; IWDG не срабатывает'},
]

# Quizzes for M5–M10
QUIZZES = {
    5: {
        'title': 'Тест: Инструментальные средства разработки',
        'description': 'Компилятор, отладчик, системы сборки для встраиваемых систем',
        'pass_score': 70,
        'questions': [
            {'text': 'Какая команда arm-none-eabi-gcc преобразует .elf в бинарный файл для прошивки?',
             'q_type': 'single', 'order': 1,
             'explanation': 'objcopy -O binary конвертирует ELF в плоский бинарный файл.',
             'choices': [
                 ('arm-none-eabi-objcopy -O binary firmware.elf firmware.bin', True),
                 ('arm-none-eabi-strip firmware.elf', False),
                 ('arm-none-eabi-ld -o firmware.bin firmware.elf', False),
                 ('arm-none-eabi-size firmware.elf', False),
             ]},
            {'text': 'Что означает секция .bss в ELF-файле встраиваемой программы?',
             'q_type': 'single', 'order': 2,
             'explanation': '.bss содержит глобальные/статические переменные, инициализированные нулём. В Flash не хранятся, только размер.',
             'choices': [
                 ('Глобальные переменные, инициализированные нулём (в RAM, не в Flash)', True),
                 ('Инициализированные глобальные переменные (в Flash и RAM)', False),
                 ('Константы в Flash-памяти', False),
                 ('Код программы (исполняемые инструкции)', False),
             ]},
            {'text': 'Какой флаг GCC показывает размер секций text/data/bss?',
             'q_type': 'single', 'order': 3,
             'explanation': 'arm-none-eabi-size выводит размеры секций ELF-файла.',
             'choices': [
                 ('arm-none-eabi-size firmware.elf', True),
                 ('arm-none-eabi-gcc -v firmware.elf', False),
                 ('arm-none-eabi-nm -s firmware.elf', False),
                 ('arm-none-eabi-readelf -S firmware.elf', False),
             ]},
            {'text': 'SWD отладка использует два сигнала. Какие?',
             'q_type': 'single', 'order': 4,
             'explanation': 'SWD (Serial Wire Debug) = SWDIO (данные) + SWDCLK (такт). JTAG требует 4 сигнала.',
             'choices': [
                 ('SWDIO и SWDCLK', True),
                 ('TDI и TDO', False),
                 ('MOSI и MISO', False),
                 ('TX и RX', False),
             ]},
            {'text': 'Что делает флаг компилятора -Os?',
             'q_type': 'single', 'order': 5,
             'explanation': '-Os оптимизирует размер кода (как -O2 но отключает расширяющие код оптимизации). Полезно при ограниченной Flash.',
             'choices': [
                 ('Оптимизировать размер кода (code size)', True),
                 ('Оптимизировать скорость (как -O3)', False),
                 ('Отключить все оптимизации', False),
                 ('Включить отладочные символы', False),
             ]},
            {'text': 'OpenOCD используется для:',
             'q_type': 'single', 'order': 6,
             'explanation': 'OpenOCD — Open On-Chip Debugger: прошивка и отладка МК через SWD/JTAG-адаптеры.',
             'choices': [
                 ('Прошивки и GDB-отладки МК через SWD/JTAG', True),
                 ('Статического анализа кода на C', False),
                 ('Компиляции под ARM без установки GCC', False),
                 ('Генерации документации из комментариев', False),
             ]},
            {'text': 'В CMake для кросс-компиляции под ARM нужно указать:',
             'q_type': 'single', 'order': 7,
             'explanation': 'CMAKE_TOOLCHAIN_FILE задаёт toolchain для кросс-компиляции (компилятор, флаги, sysroot).',
             'choices': [
                 ('CMAKE_TOOLCHAIN_FILE с путём к arm-none-eabi toolchain', True),
                 ('set(CMAKE_CXX_COMPILER arm-none-eabi-g++) без toolchain-файла', False),
                 ('Только TARGET_ARCH=ARM в командной строке', False),
                 ('Установить переменную PATH перед вызовом cmake', False),
             ]},
        ]
    },
    6: {
        'title': 'Тест: ЕСПД и техническая документация',
        'description': 'ГОСТ 19.xxx — правила оформления программной документации',
        'pass_score': 70,
        'questions': [
            {'text': 'Какой ГОСТ регламентирует содержание Технического задания на программу?',
             'q_type': 'single', 'order': 1,
             'explanation': 'ГОСТ 19.201-78 "ЕСПД. Техническое задание. Требования к содержанию и оформлению".',
             'choices': [
                 ('ГОСТ 19.201-78', True),
                 ('ГОСТ 19.101-77', False),
                 ('ГОСТ 19.402-78', False),
                 ('ГОСТ 34.602-89', False),
             ]},
            {'text': 'Какой документ ЕСПД описывает логическую структуру программы?',
             'q_type': 'single', 'order': 2,
             'explanation': 'ГОСТ 19.402-78 "Описание программы" — назначение, структура, составные части, входные/выходные данные.',
             'choices': [
                 ('Описание программы (ГОСТ 19.402-78)', True),
                 ('Техническое задание (ГОСТ 19.201-78)', False),
                 ('Программа и методика испытаний (ГОСТ 19.301-79)', False),
                 ('Руководство пользователя (ГОСТ 19.505-79)', False),
             ]},
            {'text': 'Обозначение программного документа по ГОСТ 19.103-77 имеет вид:',
             'q_type': 'single', 'order': 3,
             'explanation': 'Формат: ХХ.ХХХ.ХХХ ДД — цифры идентифицируют организацию, разработку, версию. ДД — код документа.',
             'choices': [
                 ('ХХ.ХХХ.ХХХ ДД', True),
                 ('ГОСТ-19-XXXX', False),
                 ('v1.0-ДДММГГ', False),
                 ('ПО-ХХХ/ДД', False),
             ]},
            {'text': 'Программа и методика испытаний (ГОСТ 19.301-79) должна содержать:',
             'q_type': 'single', 'order': 4,
             'explanation': 'ПМИ описывает объект испытаний, цель, методы, условия, порядок, критерии прохождения.',
             'choices': [
                 ('Объект испытаний, методы, условия, критерии прохождения', True),
                 ('Только перечень тест-кейсов без критериев', False),
                 ('Исходный код тестов', False),
                 ('Руководство по установке ПО', False),
             ]},
            {'text': 'Какой раздел ТЗ по ГОСТ 19.201-78 описывает аппаратную платформу?',
             'q_type': 'single', 'order': 5,
             'explanation': 'Раздел "Требования к составу и параметрам технических средств" описывает МК, частоту, ОЗУ, Flash.',
             'choices': [
                 ('Требования к составу и параметрам технических средств', True),
                 ('Назначение разработки', False),
                 ('Стадии и этапы разработки', False),
                 ('Порядок контроля и приёмки', False),
             ]},
            {'text': 'Руководство пользователя по ГОСТ 19.505-79 НЕ должно содержать:',
             'q_type': 'single', 'order': 6,
             'explanation': 'Исходный код — не часть руководства пользователя. РП описывает установку, запуск, использование, ошибки.',
             'choices': [
                 ('Исходный код программы', True),
                 ('Порядок установки и запуска', False),
                 ('Описание функций и режимов работы', False),
                 ('Перечень возможных ошибок и способы их устранения', False),
             ]},
        ]
    },
    7: {
        'title': 'Тест: Тестирование программного обеспечения',
        'description': 'Виды тестирования, Unity, покрытие, CI/CD',
        'pass_score': 70,
        'questions': [
            {'text': 'Что проверяет модульное (unit) тестирование?',
             'q_type': 'single', 'order': 1,
             'explanation': 'Unit-тест проверяет одну функцию/модуль в изоляции от остальных.',
             'choices': [
                 ('Отдельные функции или модули в изоляции', True),
                 ('Взаимодействие нескольких модулей', False),
                 ('Производительность системы под нагрузкой', False),
                 ('Поведение системы на реальном железе', False),
             ]},
            {'text': 'В фреймворке Unity правильный макрос для сравнения float:',
             'q_type': 'single', 'order': 2,
             'explanation': 'TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual) используется для сравнения float с допуском.',
             'choices': [
                 ('TEST_ASSERT_FLOAT_WITHIN(0.01f, expected, actual)', True),
                 ('TEST_ASSERT_EQUAL_FLOAT(expected, actual)', False),
                 ('ASSERT_EQ(expected, actual)', False),
                 ('TEST_EQUAL_DOUBLE(expected, actual, 0.01)', False),
             ]},
            {'text': 'HIL (Hardware-in-the-Loop) тестирование означает:',
             'q_type': 'single', 'order': 3,
             'explanation': 'HIL: реальный МК + симулированная внешняя среда (датчики, нагрузки эмулируются стендом).',
             'choices': [
                 ('Тестирование с реальным МК и симулированной средой', True),
                 ('Тестирование только на ПК без реального железа', False),
                 ('Тестирование с реальным МК и реальными датчиками', False),
                 ('Автоматизированное тестирование пользовательского интерфейса', False),
             ]},
            {'text': 'Code coverage 80% означает:',
             'q_type': 'single', 'order': 4,
             'explanation': '80% coverage — 80% строк/ветвей кода выполнено хотя бы в одном тесте.',
             'choices': [
                 ('80% строк кода выполнено тестами', True),
                 ('80% тестов прошли успешно', False),
                 ('Найдено 80% всех ошибок', False),
                 ('Протестировано 80% функций вручную', False),
             ]},
            {'text': 'Для чего в Unity используют mock-функции?',
             'q_type': 'single', 'order': 5,
             'explanation': 'Mock заменяет реальный HAL/аппаратуру заглушкой, позволяя тестировать логику без железа.',
             'choices': [
                 ('Заменить реальный HAL/аппаратуру заглушкой для тестирования логики', True),
                 ('Ускорить выполнение тестов', False),
                 ('Генерировать тестовые данные случайно', False),
                 ('Измерять время выполнения функций', False),
             ]},
            {'text': 'Тест для функции uint16_t crc16(uint8_t *buf, uint16_t len). Граничный случай — это:',
             'q_type': 'single', 'order': 6,
             'explanation': 'Граничный случай: пустой буфер (len=0), один байт (len=1), максимальная длина.',
             'choices': [
                 ('len=0 (пустой буфер) и len=1 (один байт)', True),
                 ('buf=NULL без проверки длины', False),
                 ('Только "типичные" значения из документации', False),
                 ('Тест с len=1000 (производительность)', False),
             ]},
            {'text': 'CI/CD в контексте МК-разработки чаще всего запускает:',
             'q_type': 'single', 'order': 7,
             'explanation': 'CI для МК: компиляция (кросс-компилятор) + unit-тесты на ПК (без железа).',
             'choices': [
                 ('Кросс-компиляцию и unit-тесты на ПК', True),
                 ('Прошивку всех МК в лаборатории', False),
                 ('Только статический анализ кода', False),
                 ('Запуск только на реальном железе через HIL', False),
             ]},
        ]
    },
    8: {
        'title': 'Тест: Отладка, рефакторинг и контроль версий',
        'description': 'Git, Code Smells, профилирование, архитектура МК-ПО',
        'pass_score': 70,
        'questions': [
            {'text': 'Команда git для создания ветки и переключения на неё:',
             'q_type': 'single', 'order': 1,
             'explanation': 'git checkout -b или git switch -c создают ветку и переключаются на неё.',
             'choices': [
                 ('git checkout -b feature/new', True),
                 ('git branch feature/new && git switch', False),
                 ('git create branch feature/new', False),
                 ('git new branch feature/new', False),
             ]},
            {'text': 'Code Smell "Magic Number" — это:',
             'q_type': 'single', 'order': 2,
             'explanation': 'Magic Number — числовая константа в коде без объяснения. Решение: именованная константа или #define.',
             'choices': [
                 ('Числовая константа без имени прямо в коде (например, HAL_Delay(500))', True),
                 ('Переполнение числового типа данных', False),
                 ('Ошибка в арифметических вычислениях', False),
                 ('Использование float вместо double', False),
             ]},
            {'text': 'DWT->CYCCNT в STM32 используется для:',
             'q_type': 'single', 'order': 3,
             'explanation': 'DWT CYCCNT — счётчик тактов CPU. Используется для профилирования и точных задержек в мкс.',
             'choices': [
                 ('Точного измерения времени в тактах CPU (профилирование)', True),
                 ('Чтения состояния прерываний', False),
                 ('Управления тактированием AHB шины', False),
                 ('Записи в регистры MPU', False),
             ]},
            {'text': 'Conventional Commits — формат сообщения коммита "feat: add UART init" означает:',
             'q_type': 'single', 'order': 4,
             'explanation': 'feat: — новая функциональность. fix: — исправление. chore: — технические изменения. docs: — документация.',
             'choices': [
                 ('Добавлена новая функциональность (UART инициализация)', True),
                 ('Исправлена ошибка в UART', False),
                 ('Изменена конфигурация сборки', False),
                 ('Добавлена документация к UART', False),
             ]},
            {'text': 'Безопасный рефакторинг функции в реальном времени МК-кода — главное требование:',
             'q_type': 'single', 'order': 5,
             'explanation': 'При рефакторинге RT-кода: поведение должно быть идентично. Тесты + измерение времени до/после.',
             'choices': [
                 ('Сохранить идентичное поведение; измерить время выполнения до и после', True),
                 ('Уменьшить количество строк кода любой ценой', False),
                 ('Заменить все int на float для точности', False),
                 ('Добавить больше комментариев к каждой строке', False),
             ]},
            {'text': 'Паттерн "конечный автомат" (FSM) в МК-программировании используется для:',
             'q_type': 'single', 'order': 6,
             'explanation': 'FSM управляет поведением системы с несколькими состояниями и переходами между ними (протоколы, UI, моторы).',
             'choices': [
                 ('Управления системой с несколькими состояниями и переходами', True),
                 ('Оптимизации скорости математических вычислений', False),
                 ('Замены RTOS в однозадачных программах', False),
                 ('Хранения данных во Flash-памяти', False),
             ]},
        ]
    },
    9: {
        'title': 'Тест: Практикум — компоненты и протоколы',
        'description': 'BME280, DS18B20, DHT22, OLED, SPI Flash, отладка датчиков',
        'pass_score': 70,
        'questions': [
            {'text': 'Адрес BME280 на I2C шине при SDO=GND:',
             'q_type': 'single', 'order': 1,
             'explanation': 'BME280: при SDO=GND адрес 0x76, при SDO=VCC — 0x77.',
             'choices': [
                 ('0x76', True),
                 ('0x77', False),
                 ('0x68', False),
                 ('0x48', False),
             ]},
            {'text': 'DS18B20 возвращает температуру в формате 16-bit. При 12-bit разрешении шаг:',
             'q_type': 'single', 'order': 2,
             'explanation': 'DS18B20 при 12-bit разрешении: шаг 0.0625°C (1/16 °C). Raw value 0x00D0 = 13°C.',
             'choices': [
                 ('0.0625°C (1/16 °C)', True),
                 ('0.5°C', False),
                 ('0.1°C', False),
                 ('1°C', False),
             ]},
            {'text': 'Для DHT22 требуется задержка перед чтением данных после команды START. Какая?',
             'q_type': 'single', 'order': 3,
             'explanation': 'DHT22: хост удерживает LOW минимум 1 мс (обычно 18 мс для совместимости с DHT11).',
             'choices': [
                 ('Минимум 1 мс (хост удерживает LOW)', True),
                 ('10 мкс (как у 1-Wire)', False),
                 ('500 нс', False),
                 ('100 мс (ждать окончания измерения)', False),
             ]},
            {'text': 'MPU6050 выдаёт данные акселерометра в raw-формате. При диапазоне ±2g масштаб:',
             'q_type': 'single', 'order': 4,
             'explanation': 'MPU6050 при ±2g: 16384 LSB/g. Для перевода в g: raw / 16384.0.',
             'choices': [
                 ('16384 LSB/g (делить raw на 16384 для получения g)', True),
                 ('32768 LSB/g', False),
                 ('1000 LSB/g', False),
                 ('256 LSB/g', False),
             ]},
            {'text': 'SSD1306 OLED (128x64) подключён по I2C. Команда для очистки дисплея:',
             'q_type': 'single', 'order': 5,
             'explanation': 'SSD1306 не имеет аппаратной команды очистки. Нужно записать 0x00 в весь GDDRAM (8 страниц × 128 байт).',
             'choices': [
                 ('Записать 0x00 во весь GDDRAM (8 страниц × 128 байт)', True),
                 ('Послать команду 0xAE (Display OFF)', False),
                 ('Послать команду 0xFF', False),
                 ('Перезапустить I2C шину', False),
             ]},
            {'text': 'W25Q SPI Flash команда чтения JEDEC ID (0x9F) возвращает:',
             'q_type': 'single', 'order': 6,
             'explanation': 'JEDEC ID: Manufacturer ID (0xEF для Winbond) + Memory Type + Capacity. Используется для идентификации чипа.',
             'choices': [
                 ('Manufacturer ID, Memory Type, Capacity (3 байта)', True),
                 ('Только Manufacturer ID (1 байт)', False),
                 ('Объём Flash в байтах (4 байта)', False),
                 ('Случайные данные — ID не поддерживается', False),
             ]},
        ]
    },
    10: {
        'title': 'Тест: Системы реального времени и финальный проект',
        'description': 'Modbus RTU, FreeRTOS мониторинг, финальный проект',
        'pass_score': 70,
        'questions': [
            {'text': 'Modbus RTU кадр содержит: [Addr][FC][Data...][CRC]. CRC вычисляется от:',
             'q_type': 'single', 'order': 1,
             'explanation': 'CRC16 Modbus считается от Addr+FC+Data (всё кроме самого CRC). Полином 0xA001 (обратный).',
             'choices': [
                 ('Addr + FC + Data (всё до CRC)', True),
                 ('Только Data', False),
                 ('FC + Data', False),
                 ('Всего кадра включая CRC', False),
             ]},
            {'text': 'Function Code 0x03 в Modbus означает:',
             'q_type': 'single', 'order': 2,
             'explanation': 'FC=0x03 Read Holding Registers — чтение регистров хранения (16-бит слова).',
             'choices': [
                 ('Read Holding Registers', True),
                 ('Write Single Register', False),
                 ('Read Coils', False),
                 ('Write Multiple Registers', False),
             ]},
            {'text': 'uxTaskGetStackHighWaterMark() возвращает:',
             'q_type': 'single', 'order': 3,
             'explanation': 'HWM = минимальный свободный остаток стека за всё время. Если HWM=0 — стек переполнился.',
             'choices': [
                 ('Минимальный свободный остаток стека в словах (наихудший случай)', True),
                 ('Текущий свободный остаток стека', False),
                 ('Максимальное использование стека', False),
                 ('Общий размер стека задачи', False),
             ]},
            {'text': 'xQueueSendFromISR() отличается от xQueueSend() тем, что:',
             'q_type': 'single', 'order': 4,
             'explanation': 'FromISR не может блокироваться, принимает &pxHigherPriorityTaskWoken для yield-сигнала планировщику.',
             'choices': [
                 ('Не блокируется и принимает параметр pxHigherPriorityTaskWoken', True),
                 ('Работает быстрее за счёт отключения прерываний', False),
                 ('Может передавать данные только размером 1 байт', False),
                 ('Автоматически вызывает portYIELD после отправки', False),
             ]},
            {'text': 'IWDG (Independent Watchdog) на STM32 отличается от WWDG тем, что:',
             'q_type': 'single', 'order': 5,
             'explanation': 'IWDG работает от независимого LSI-генератора, не останавливается при остановке CPU. WWDG — от PCLK, с окном.',
             'choices': [
                 ('Работает от независимого LSI генератора, не останавливается при остановке CPU', True),
                 ('Имеет программируемое временное окно для сброса', False),
                 ('Более точный благодаря HSE кварцу', False),
                 ('Может быть отключён программно', False),
             ]},
            {'text': 'При Priority Inversion в FreeRTOS: высокоприоритетная задача ждёт мьютекс, удерживаемый низкоприоритетной. Решение FreeRTOS:',
             'q_type': 'single', 'order': 6,
             'explanation': 'Priority Inheritance: временно повышает приоритет держателя мьютекса до уровня ожидающей задачи.',
             'choices': [
                 ('Priority Inheritance — временно повысить приоритет низкоприоритетной задачи', True),
                 ('Перезапустить все задачи с одинаковым приоритетом', False),
                 ('Автоматически освободить мьютекс через таймаут', False),
                 ('Использовать семафор вместо мьютекса', False),
             ]},
            {'text': 'Для многозадачного мониторинга (N задач) лучший паттерн передачи данных:',
             'q_type': 'single', 'order': 7,
             'explanation': 'Queue: задача-производитель кладёт данные, задача-потребитель читает. Безопасно, без общей памяти.',
             'choices': [
                 ('Queue: производитель → queue → потребитель', True),
                 ('Глобальная переменная с volatile', False),
                 ('Прямая запись через указатель в стек другой задачи', False),
                 ('Event Group для каждого значения', False),
             ]},
        ]
    }
}


class Command(BaseCommand):
    help = 'Seed RVES: practical works (all modules) + quizzes M5-M10'

    def handle(self, *args, **options):
        subject = Subject.objects.get(slug='rves')
        modules = {m.order: m for m in TheoryModule.objects.filter(subject=subject)}

        # ── Practical works ──────────────────────────────────────────────
        self.stdout.write('=== Practical Works ===')
        for pw_data in PRACTICAL_WORKS:
            tm_order = pw_data.pop('theory_module_order')
            module = modules.get(tm_order)
            obj, created = PracticalWork.objects.update_or_create(
                subject=subject, order=pw_data['order'],
                defaults={**pw_data, 'subject': subject,
                          'theory_module': module, 'is_active': True},
            )
            status = 'created' if created else 'updated'
            self.stdout.write(f'  [{pw_data["order"]}] {obj.title[:50]} [{status}]')
            # restore for next iterations
            pw_data['theory_module_order'] = tm_order

        # ── Quizzes M5–M10 ───────────────────────────────────────────────
        self.stdout.write('=== Quizzes M5-M10 ===')
        for mod_order, qdata in QUIZZES.items():
            module = modules.get(mod_order)
            if not module:
                self.stderr.write(f'Module M{mod_order} not found')
                continue

            quiz, created = Quiz.objects.update_or_create(
                module=module,
                defaults={
                    'title': qdata['title'],
                    'description': qdata['description'],
                    'pass_score': qdata['pass_score'],
                    'is_active': True,
                }
            )
            status = 'created' if created else 'updated'
            self.stdout.write(f'  M{mod_order} Quiz: {quiz.title[:50]} [{status}]')

            for q_info in qdata['questions']:
                choices = q_info.pop('choices')
                question, _ = Question.objects.update_or_create(
                    quiz=quiz, order=q_info['order'],
                    defaults={**q_info, 'quiz': quiz},
                )
                AnswerChoice.objects.filter(question=question).delete()
                for idx, (text, is_correct) in enumerate(choices, start=1):
                    AnswerChoice.objects.create(
                        question=question, text=text,
                        is_correct=is_correct, order=idx,
                    )
                q_info['choices'] = choices  # restore
                self.stdout.write(
                    f'    Q{q_info["order"]}: {q_info["text"][:55]} ({len(choices)} choices)')

        self.stdout.write('Done.')
