from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson

M5_LESSONS = [
    {
        'order': 1,
        'title': 'Инструментальные средства разработки ПО МК: обзор',
        'content': '''<h2>Инструментальные средства разработки ПО МК: обзор</h2>
<p>Разработка программного обеспечения для встраиваемых систем требует специализированного инструментария. В отличие от прикладного программирования, разработчик МК работает с кросс-компиляцией, аппаратными отладчиками и специфическими IDE.</p>

<h3>Цепочка инструментов (Toolchain)</h3>
<p>Стандартная цепочка разработки ПО для МК:</p>
<ol>
  <li><strong>Редактор кода / IDE</strong> — написание исходного кода.</li>
  <li><strong>Кросс-компилятор</strong> — компиляция для целевой архитектуры (ARM, AVR, RISC-V).</li>
  <li><strong>Компоновщик (Linker)</strong> — сборка объектных файлов в исполняемый образ.</li>
  <li><strong>Загрузчик (Flash programmer)</strong> — прошивка МК.</li>
  <li><strong>Отладчик</strong> — пошаговое выполнение, точки останова.</li>
</ol>

<h3>Кросс-компиляция</h3>
<p>Host-система (x86 PC) компилирует код для Target-системы (ARM Cortex-M). Компилятор <strong>arm-none-eabi-gcc</strong> — стандарт для ARM МК без ОС:</p>
<pre><code># Компиляция
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 \
    -mfloat-abi=hard -O2 -Wall -c main.c -o main.o

# Компоновка
arm-none-eabi-gcc -T STM32F411CEUx_FLASH.ld -o firmware.elf main.o

# Создать бинарный образ
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin

# Размер секций
arm-none-eabi-size firmware.elf
</code></pre>

<h3>Основные IDE для STM32</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>IDE</th><th>Производитель</th><th>Особенности</th></tr>
  <tr><td>STM32CubeIDE</td><td>ST Microelectronics</td><td>Официальная, встроена CubeMX, Eclipse, GDB</td></tr>
  <tr><td>Keil MDK (µVision)</td><td>Arm/Keil</td><td>Проф. уровень, RTE, дорогая лицензия</td></tr>
  <tr><td>IAR EWARM</td><td>IAR Systems</td><td>Лучший компилятор для ARM, коммерческая</td></tr>
  <tr><td>PlatformIO + VS Code</td><td>Open Source</td><td>Бесплатная, множество платформ, удобна</td></tr>
  <tr><td>CLion + CMake</td><td>JetBrains</td><td>Современный UX, платная, удобна для опытных</td></tr>
</table>

<h3>STM32CubeMX — генератор кода инициализации</h3>
<p>Graphical Tool от ST. Настраивает периферию через GUI, генерирует код инициализации на C:</p>
<ul>
  <li>Выбор МК и конфигурация пинов.</li>
  <li>Настройка тактирования (Clock Configuration).</li>
  <li>Включение периферии (UART, SPI, I2C, TIM, ADC).</li>
  <li>Генерация проекта для STM32CubeIDE / Keil / IAR / Makefile.</li>
</ul>

<div class="tip">STM32CubeIDE включает CubeMX. Разработчик настраивает периферию в GUI, затем пишет логику в специально отмеченных секциях кода. При регенерации пользовательский код не затирается.</div>''',
    },
    {
        'order': 2,
        'title': 'Компилятор GCC: флаги, оптимизации, сборка',
        'content': '''<h2>Компилятор GCC: флаги, оптимизации, сборка</h2>
<p>GNU GCC (arm-none-eabi-gcc) — основной компилятор для ARM МК в свободном доступе. Понимание флагов компилятора критично для правильной и эффективной сборки.</p>

<h3>Ключевые флаги для ARM Cortex-M</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Флаг</th><th>Описание</th></tr>
  <tr><td><code>-mcpu=cortex-m4</code></td><td>Целевой процессор</td></tr>
  <tr><td><code>-mthumb</code></td><td>Набор команд Thumb-2</td></tr>
  <tr><td><code>-mfpu=fpv4-sp-d16</code></td><td>FPU (32-bit float)</td></tr>
  <tr><td><code>-mfloat-abi=hard</code></td><td>Аргументы float через FPU-регистры</td></tr>
  <tr><td><code>-mfloat-abi=soft</code></td><td>Программная эмуляция FPU</td></tr>
  <tr><td><code>-O0</code></td><td>Без оптимизации (отладка)</td></tr>
  <tr><td><code>-O2</code></td><td>Оптимизация скорости (продакшн)</td></tr>
  <tr><td><code>-Os</code></td><td>Оптимизация размера кода</td></tr>
  <tr><td><code>-g</code></td><td>Отладочная информация в ELF</td></tr>
  <tr><td><code>-Wall -Wextra</code></td><td>Максимум предупреждений</td></tr>
  <tr><td><code>-ffunction-sections</code></td><td>Каждая функция в отдельной секции</td></tr>
  <tr><td><code>-fdata-sections</code></td><td>Каждая переменная в отдельной секции</td></tr>
  <tr><td><code>--specs=nano.specs</code></td><td>Компактная libc (newlib-nano)</td></tr>
</table>

<h3>Флаги компоновщика</h3>
<pre><code>LDFLAGS = -T STM32F411CEUx_FLASH.ld         \
          -Wl,--gc-sections                  \  # удалить неиспользуемые секции
          -Wl,-Map=firmware.map              \  # карта памяти
          --specs=nano.specs                 \
          --specs=nosys.specs                   # без syscalls (bare metal)
</code></pre>

<h3>Оптимизации и отладка</h3>
<pre><code># Проблема: -O2 оптимизирует volatile-подобные конструкции
# Например, пустой цикл задержки исчезает:
for (int i = 0; i &lt; 1000; i++);  // удаляется при -O2

# Решение: use __attribute__((optimize("O0"))) для функции
__attribute__((optimize("O0")))
void delay_soft(uint32_t n) {
    while (n--);
}
</code></pre>

<h3>Анализ размера кода</h3>
<pre><code>arm-none-eabi-size firmware.elf
   text    data     bss     dec     hex filename
  28064     324    2048   30436    76E4 firmware.elf
# text = Flash, data = Flash+RAM, bss = RAM (нули)

arm-none-eabi-nm --size-sort firmware.elf | tail -20
# Самые большие символы (функции, переменные)

arm-none-eabi-objdump -D firmware.elf | grep "&lt;main&gt;:" -A 50
# Дизассемблер: что реально сгенерировал компилятор
</code></pre>

<h3>Makefile для STM32</h3>
<pre><code>CC = arm-none-eabi-gcc
CFLAGS = -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -O2 -g

all: firmware.bin

firmware.elf: main.o startup.o
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

firmware.bin: firmware.elf
	arm-none-eabi-objcopy -O binary $< $@

clean:
	rm -f *.o *.elf *.bin
</code></pre>''',
    },
    {
        'order': 3,
        'title': 'Отладчики: JTAG, SWD, OpenOCD, GDB',
        'content': '''<h2>Отладчики: JTAG, SWD, OpenOCD, GDB</h2>
<p>Отладчик — незаменимый инструмент при разработке встраиваемых систем. В отличие от ПК, нет printf в консоль, нет исключений с трассировкой стека — только аппаратный отладчик.</p>

<h3>Интерфейсы отладки</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Интерфейс</th><th>Сигналы</th><th>Особенности</th></tr>
  <tr><td>JTAG</td><td>TDI, TDO, TCK, TMS, TRST</td><td>5 пинов, IEEE 1149.1, цепочка устройств</td></tr>
  <tr><td>SWD</td><td>SWDIO, SWDCLK, SWO</td><td>2+1 пина, ARM-специфичный, заменяет JTAG</td></tr>
  <tr><td>cJTAG (JTAG-DP)</td><td>2 пина</td><td>Компактный JTAG, редко</td></tr>
</table>

<h3>Программаторы/отладчики</h3>
<ul>
  <li><strong>ST-Link V2/V3</strong> — встроен в Nucleo/Discovery, дешёвые внешние клоны.</li>
  <li><strong>J-Link (Segger)</strong> — профессиональный, быстрый, поддерживает все ARM. Edu версия бесплатна для учёбы.</li>
  <li><strong>CMSIS-DAP / DAPLink</strong> — открытый стандарт, много реализаций.</li>
  <li><strong>OpenOCD</strong> — открытое ПО, посредник между GDB и аппаратным отладчиком.</li>
</ul>

<h3>OpenOCD — запуск сессии</h3>
<pre><code># Запуск OpenOCD для STM32F4 через ST-Link
openocd -f interface/stlink.cfg \
        -f target/stm32f4x.cfg

# В другом терминале — GDB
arm-none-eabi-gdb firmware.elf
(gdb) target remote localhost:3333
(gdb) monitor reset halt
(gdb) load                        # прошить
(gdb) break main
(gdb) continue
</code></pre>

<h3>GDB — основные команды</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Команда</th><th>Описание</th></tr>
  <tr><td><code>b main</code></td><td>Точка останова на функции</td></tr>
  <tr><td><code>b file.c:42</code></td><td>Точка останова на строке</td></tr>
  <tr><td><code>c</code></td><td>Продолжить выполнение</td></tr>
  <tr><td><code>s</code></td><td>Шаг с заходом в функцию</td></tr>
  <tr><td><code>n</code></td><td>Шаг без захода</td></tr>
  <tr><td><code>p var</code></td><td>Напечатать значение переменной</td></tr>
  <tr><td><code>x/8xw 0x20000000</code></td><td>Дамп памяти: 8 слов hex</td></tr>
  <tr><td><code>info registers</code></td><td>Все регистры CPU</td></tr>
  <tr><td><code>bt</code></td><td>Трассировка стека</td></tr>
  <tr><td><code>watch var</code></td><td>Точка останова при изменении переменной</td></tr>
</table>

<h3>STM32CubeIDE отладка</h3>
<p>GUI поверх GDB + OpenOCD. Возможности:</p>
<ul>
  <li>Просмотр и изменение регистров периферии (SFR view).</li>
  <tr>Live Watch — обновление переменных без остановки.</tr>
  <li>SWV (Serial Wire Viewer) — трассировка через SWO.</li>
  <li>Fault Analyzer — расшифровка HardFault, MemManage Fault.</li>
</ul>''',
    },
    {
        'order': 4,
        'title': 'Системы сборки: Make, CMake, SCons',
        'content': '''<h2>Системы сборки: Make, CMake, SCons</h2>
<p>По мере роста проекта управление компиляцией через команды вручную становится невозможным. Системы сборки автоматизируют зависимости, пересборку изменённых файлов и управление конфигурациями.</p>

<h3>GNU Make</h3>
<p>Классика встраиваемой разработки. Makefile описывает цели, зависимости и команды.</p>
<pre><code># Переменные
CC      = arm-none-eabi-gcc
SRCS    = Src/main.c Src/stm32f4xx_it.c
OBJS    = $(SRCS:.c=.o)
TARGET  = firmware

# Главная цель
$(TARGET).elf: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

# Правило компиляции .c → .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Автоматические зависимости (пересборка при изменении .h)
-include $(OBJS:.o=.d)
%.d: %.c
	$(CC) -MM $(CFLAGS) $< > $@

.PHONY: clean flash
clean:
	rm -f $(OBJS) $(TARGET).elf $(TARGET).bin

flash: $(TARGET).bin
	st-flash write $< 0x08000000
</code></pre>

<h3>CMake</h3>
<p>Современный стандарт. Генерирует Makefile, Ninja или проект IDE. Обязателен для сложных проектов.</p>
<pre><code>cmake_minimum_required(VERSION 3.20)
project(firmware C ASM)

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_C_COMPILER arm-none-eabi-gcc)

set(MCU_FLAGS "-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard")
set(CMAKE_C_FLAGS "${MCU_FLAGS} -O2 -Wall")

add_executable(firmware
    Src/main.c
    Src/stm32f4xx_it.c
    startup_stm32f411xe.s
)

target_include_directories(firmware PRIVATE Inc Drivers/CMSIS/Include)

set_target_properties(firmware PROPERTIES
    LINK_FLAGS "-T ${CMAKE_SOURCE_DIR}/STM32F411CEUx_FLASH.ld -Wl,--gc-sections"
)

# Post-build: создать .bin и показать размер
add_custom_command(TARGET firmware POST_BUILD
    COMMAND arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
    COMMAND arm-none-eabi-size firmware.elf
)
</code></pre>

<h3>PlatformIO — упрощённая альтернатива</h3>
<p>Менеджер пакетов + система сборки + IDE (VS Code extension). Скрывает сложность CMake/Make.</p>
<pre><code># platformio.ini
[env:nucleo_f411re]
platform = ststm32
board = nucleo_f411re
framework = stm32cube
build_flags = -DUSE_HAL_DRIVER -DSTM32F411xE -O2
lib_deps =
    stm32duino/STM32duino FreeRTOS@^10.3.1
</code></pre>
<pre><code>pio run            # сборка
pio run -t upload  # прошивка
pio device monitor # мониторинг UART
pio debug          # отладка через GDB
</code></pre>

<h3>Ninja — быстрая замена Make</h3>
<p>CMake может генерировать Ninja-файлы. Ninja быстрее Make за счёт параллельной сборки и минимального анализа:</p>
<pre><code>cmake -G Ninja ..
ninja          # параллельная сборка
ninja -j4      # 4 параллельных задания
</code></pre>''',
    },
    {
        'order': 5,
        'title': 'Система контроля версий Git в разработке ПО МК',
        'content': '''<h2>Система контроля версий Git в разработке ПО МК</h2>
<p>Git — стандарт управления исходным кодом. Для встраиваемых проектов важно правильно настроить .gitignore и структуру репозитория.</p>

<h3>Типичная структура проекта STM32CubeIDE</h3>
<pre><code>project/
├── Core/
│   ├── Inc/        # заголовочные файлы
│   └── Src/        # исходный код (main.c, stm32f4xx_it.c)
├── Drivers/
│   ├── CMSIS/      # стандарт ARM (НЕ менять)
│   └── STM32F4xx_HAL_Driver/  # HAL ST
├── Middlewares/    # FreeRTOS, USB, FatFS
├── .ioc            # файл конфигурации CubeMX
├── Makefile / CMakeLists.txt
└── README.md
</code></pre>

<h3>.gitignore для STM32CubeIDE</h3>
<pre><code># Объектные файлы и артефакты сборки
*.o
*.d
*.elf
*.bin
*.hex
*.map
*.lst
build/
Debug/
Release/

# IDE-специфичные файлы
.cproject
.project
.settings/
*.launch

# Временные файлы редактора
*.swp
*~
.DS_Store
</code></pre>

<h3>Основные команды Git</h3>
<pre><code># Инициализация и первый коммит
git init
git add Core/ Drivers/ .ioc Makefile
git commit -m "Initial commit: STM32F4 project skeleton"

# Ветвление для новой функции
git checkout -b feature/uart-logging
# ... разработка ...
git add Core/Src/uart.c Core/Inc/uart.h
git commit -m "feat: add UART logging with ring buffer"
git checkout main
git merge feature/uart-logging

# Просмотр истории
git log --oneline --graph
git diff HEAD~1 Core/Src/main.c

# Теги для релизов прошивки
git tag -a v1.2.0 -m "Release 1.2.0: added FreeRTOS"
git push origin v1.2.0
</code></pre>

<h3>Соглашения по коммитам (Conventional Commits)</h3>
<pre><code>feat: добавить поддержку I2C датчика температуры
fix: устранить переполнение буфера в UART ISR
refactor: вынести инициализацию GPIO в отдельный модуль
docs: обновить README с описанием пинаута
test: добавить тест для CRC16
chore: обновить Drivers до HAL 1.28.0
</code></pre>

<h3>Управление зависимостями</h3>
<p>Библиотеки (HAL, FreeRTOS, Segger RTT) рекомендуется включать как git submodule:</p>
<pre><code>git submodule add https://github.com/STMicroelectronics/STM32CubeF4.git Drivers/STM32CubeF4
git submodule update --init --recursive

# При клонировании проекта
git clone --recurse-submodules https://github.com/user/project.git
</code></pre>''',
    },
    {
        'order': 6,
        'title': 'Статический анализ, форматирование кода и CI/CD для МК',
        'content': '''<h2>Статический анализ, форматирование кода и CI/CD для МК</h2>
<p>Качество кода для встраиваемых систем критично — баги в прошивке медицинского прибора или промышленного контроллера стоят дорого. Автоматические инструменты находят ошибки до запуска на железе.</p>

<h3>Статический анализ кода</h3>
<ul>
  <li><strong>Cppcheck</strong> — бесплатный, ищет неопределённое поведение, утечки памяти, неинициализированные переменные.</li>
  <li><strong>PC-lint / Gimpel Lint</strong> — коммерческий, MISRA C compliance.</li>
  <li><strong>Clang-Tidy</strong> — встроен в CLion, VS Code, проверяет стиль и безопасность.</li>
  <li><strong>SonarQube</strong> — корпоративный сервер анализа кода.</li>
</ul>

<h3>Cppcheck — использование</h3>
<pre><code># Проверить весь проект
cppcheck --enable=all --inconclusive \
         --suppress=missingIncludeSystem \
         -I Core/Inc -I Drivers/CMSIS/Include \
         Core/Src/ 2>&1 | tee cppcheck_report.txt

# Пример вывода:
# Core/Src/main.c:42:5: warning: Memory leak: buf [memleak]
# Core/Src/uart.c:18:1: error: Array index out of bounds [arrayIndexOutOfBounds]
</code></pre>

<h3>MISRA C — стандарт безопасного кода</h3>
<p>MISRA C 2012 — набор из 143 правил для безопасного программирования на Си в критических системах. Примеры правил:</p>
<ul>
  <li>Запрет dynamic memory allocation (malloc) — правило 21.3.</li>
  <li>Все switch-case должны иметь default — правило 16.4.</li>
  <li>Запрет рекурсии — правило 17.2.</li>
  <li>Все переменные инициализируются перед использованием — правило 9.1.</li>
</ul>

<h3>Clang-Format — форматирование кода</h3>
<pre><code># .clang-format — настройки стиля
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: None
SortIncludes: false
</code></pre>
<pre><code># Форматировать все .c и .h файлы
find Core/ -name "*.c" -o -name "*.h" | xargs clang-format -i
</code></pre>

<h3>CI/CD для встраиваемых проектов (GitHub Actions)</h3>
<pre><code># .github/workflows/build.yml
name: Build Firmware

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Install ARM toolchain
        run: |
          sudo apt-get install -y gcc-arm-none-eabi

      - name: Build
        run: make -j4

      - name: Static analysis
        run: cppcheck --error-exitcode=1 Core/Src/

      - name: Upload firmware artifact
        uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: build/firmware.bin
</code></pre>

<div class="tip">CI/CD для МК не прошивает железо автоматически (для этого нужен физический стенд с программатором), но проверяет компилируемость и статический анализ при каждом push — это уже ловит большинство ошибок.</div>''',
    },
]

M6_LESSONS = [
    {
        'order': 1,
        'title': 'ЕСПД: структура стандартов и виды документов',
        'content': '''<h2>ЕСПД: структура стандартов и виды документов</h2>
<p>ЕСПД (Единая система программной документации) — комплекс государственных стандартов СССР/России, регламентирующих разработку, оформление и сопровождение программного обеспечения. Основа — ГОСТ 19.xxx.</p>

<h3>История и актуальность</h3>
<p>ЕСПД разработана в 1977–1980 годах, актуализирована в 1990-х. Остаётся обязательной для государственных заказов, оборонных программ и регулируемых отраслей (медицина, транспорт, промышленность). В коммерческой разработке применяется реже, но знание стандартов обязательно для технических специалистов.</p>

<h3>Структура ГОСТ 19</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Группа</th><th>ГОСТ</th><th>Описание</th></tr>
  <tr><td>19.0xx</td><td>ГОСТ 19.001, 19.002, 19.004</td><td>Общие положения, термины</td></tr>
  <tr><td>19.1xx</td><td>ГОСТ 19.101, 19.102, 19.103</td><td>Виды документов, стадии разработки</td></tr>
  <tr><td>19.2xx</td><td>ГОСТ 19.201, 19.202</td><td>Техническое задание, эскизный проект</td></tr>
  <tr><td>19.3xx</td><td>ГОСТ 19.301, 19.302</td><td>Программа и методика испытаний</td></tr>
  <tr><td>19.4xx</td><td>ГОСТ 19.401, 19.402, 19.404</td><td>Текст программы, описание программы</td></tr>
  <tr><td>19.5xx</td><td>ГОСТ 19.501, 19.502, 19.503, 19.504, 19.505, 19.506</td><td>Эксплуатационные документы</td></tr>
  <tr><td>19.6xx</td><td>ГОСТ 19.601, 19.602, 19.603, 19.604</td><td>Сопровождение ПО</td></tr>
</table>

<h3>Основные виды программных документов (ГОСТ 19.101)</h3>
<ul>
  <li><strong>ТЗ — Техническое задание</strong> — требования к программе.</li>
  <li><strong>ЭП — Эскизный проект</strong> — предварительные решения.</li>
  <li><strong>ТП — Технический проект</strong> — детальные проектные решения.</li>
  <li><strong>РП — Рабочий проект</strong> — готовый к внедрению комплект.</li>
  <li><strong>Текст программы</strong> — исходный код с комментариями.</li>
  <li><strong>Описание программы</strong> — структура, данные, алгоритмы.</li>
  <li><strong>Руководство пользователя</strong> — инструкция по эксплуатации.</li>
  <li><strong>Программа и методика испытаний</strong> — как тестировать.</li>
  <li><strong>Ведомость держателей подлинников</strong> — реестр документов.</li>
</ul>

<h3>Стадии разработки (ГОСТ 19.102)</h3>
<ol>
  <li>Техническое задание</li>
  <li>Эскизный проект</li>
  <li>Технический проект</li>
  <li>Рабочий проект (кодирование + тестирование)</li>
  <li>Внедрение</li>
  <li>Сопровождение</li>
</ol>

<div class="tip">Для учебных проектов обычно требуют: ТЗ + Описание программы + Руководство пользователя + Программа и методика испытаний. Полный комплект РП — для дипломных работ и реальных проектов.</div>''',
    },
    {
        'order': 2,
        'title': 'Техническое задание по ГОСТ 19.201-78',
        'content': '''<h2>Техническое задание по ГОСТ 19.201-78</h2>
        <p>Техническое задание (ТЗ) — первичный документ, определяющий требования к разрабатываемому ПО. Оформляется по ГОСТ 19.201-78.</p>

<h3>Структура ТЗ (обязательные разделы)</h3>
<ol>
  <li>Введение (наименование, краткая характеристика)</li>
  <li>Основания для разработки (документ-основание, наименование организации-заказчика)</li>
  <li>Назначение разработки</li>
  <li>Требования к программе или программному изделию:
    <ul>
      <li>Требования к функциональным характеристикам</li>
      <li>Требования к надёжности</li>
      <li>Условия эксплуатации</li>
      <li>Требования к составу и параметрам технических средств</li>
      <li>Требования к информационной и программной совместимости</li>
    </ul>
  </li>
  <li>Требования к программной документации</li>
  <li>Технико-экономические показатели</li>
  <li>Стадии и этапы разработки</li>
  <li>Порядок контроля и приёмки</li>
</ol>

<h3>Пример раздела "Назначение разработки"</h3>
<pre><code>2. Назначение разработки

2.1 Функциональное назначение
Программа предназначена для управления установкой измерения
температуры на базе МК STM32F411 с датчиком DS18B20.

2.2 Эксплуатационное назначение
Программа эксплуатируется оператором установки для:
- непрерывного мониторинга температуры (диапазон -55...+125 °C);
- сигнализации при выходе за уставки (порог настраивается);
- передачи данных по UART (9600 Бод, 8N1) на ПК-терминал;
- хранения архива за последние 24 часа во Flash МК.
</code></pre>

<h3>Пример раздела "Требования к функциональным характеристикам"</h3>
<pre><code>4.1 Требования к функциональным характеристикам

4.1.1 Программа должна обеспечивать:
а) опрос датчика DS18B20 с периодом не более 1 с;
б) разрешение измерения — 0,0625 °C (12-разрядный режим DS18B20);
в) отображение текущей температуры на ЖКИ 16×2 (I2C интерфейс);
г) передачу данных по UART в формате JSON:
   {"t": 23.56, "ts": 1720000000}
д) запись в Flash при отклонении > 0,5 °C от предыдущего значения;
е) воспроизведение звукового сигнала (PWM) при T > Tmax или T < Tmin.

4.1.2 Уставки Tmax и Tmin должны сохраняться при выключении питания
(EEPROM-эмуляция во Flash).
</code></pre>

<h3>Оформление по ГОСТ 19.104</h3>
<ul>
  <li>Шрифт: Times New Roman, 14 пт (или эквивалент).</li>
  <li>Поля: левое 30 мм, правое 15 мм, верхнее и нижнее 20 мм.</li>
  <li>Нумерация: сквозная, арабскими цифрами.</li>
  <li>Титульный лист по ГОСТ 19.104-78: наименование организации, документа, обозначение, год.</li>
  <li>Лист утверждения при сдаче заказчику.</li>
</ul>''',
    },
    {
        'order': 3,
        'title': 'Описание программы по ГОСТ 19.402-78',
        'content': '''<h2>Описание программы по ГОСТ 19.402-78</h2>
<p>Описание программы — технический документ, раскрывающий логику программы, структуру данных и алгоритмы. Оформляется по ГОСТ 19.402-78.</p>

<h3>Структура документа</h3>
<ol>
  <li>Общие сведения (обозначение, наименование, язык программирования, ОС)</li>
  <li>Функциональное назначение (что делает программа)</li>
  <li>Описание логической структуры (алгоритм, методы решения задачи)</li>
  <li>Используемые технические средства (конфигурация, периферия)</li>
  <li>Вызов и загрузка (как запустить, загрузчик)</li>
  <li>Входные данные (форматы, диапазоны)</li>
  <li>Выходные данные (форматы, протоколы)</li>
</ol>

<h3>Пример раздела "Описание логической структуры"</h3>
<pre><code>3. Описание логической структуры

3.1 Структура модулей
Программа состоит из следующих модулей:
- main.c       — главная функция, инициализация, диспетчер задач;
- ds18b20.c    — драйвер датчика температуры (1-Wire протокол);
- lcd_i2c.c    — драйвер ЖКИ по шине I2C (PCF8574 + HD44780);
- uart_log.c   — модуль передачи данных по UART в формате JSON;
- flash_store.c — модуль EEPROM-эмуляции (хранение уставок и архива);
- alarms.c     — модуль звуковой и светодиодной сигнализации.

3.2 Алгоритм работы главного цикла
  ┌─── Инициализация: тактирование, GPIO, I2C, UART, TIM, Flash ───┐
  │                                                                   │
  └→ Цикл (1 с):                                                     │
       1. Запрос температуры DS18B20 (OneWire: Reset → ROM → Convert)│
       2. Ожидание преобразования 750 мс                             │
       3. Чтение результата (OneWire: Reset → ROM → Read Scratchpad) │
       4. Обновление ЖКИ                                             │
       5. Проверка уставок → аларм                                   │
       6. Отправка JSON по UART                                       │
       7. Запись в Flash (если Δ > 0,5 °C)                           │
       8. HAL_Delay до следующего цикла                              ─┘
</code></pre>

<h3>Пример раздела "Входные данные"</h3>
<pre><code>6. Входные данные

6.1 Настройки уставок
Устанавливаются через UART-команды в формате:
  SET Tmax=&lt;value&gt;\r\n  — установить верхний порог
  SET Tmin=&lt;value&gt;\r\n  — установить нижний порог
где value — число в диапазоне от -55 до 125 (тип float, точность 0,1).

6.2 Данные датчика DS18B20
9-байтный Scratchpad, регистры Temperature MSB/LSB.
Формула: T = (int16_t)(MSB&lt;&lt;8 | LSB) / 16.0f
</code></pre>

<h3>Схема алгоритма (ГОСТ 19.701)</h3>
<p>К описанию программы прилагается схема алгоритма по ГОСТ 19.701-90 (блок-схема). Элементы:</p>
<ul>
  <li>Прямоугольник — обработка (вычисление).</li>
  <li>Ромб — ветвление (условие).</li>
  <li>Параллелограмм — ввод/вывод.</li>
  <li>Скруглённый прямоугольник — начало/конец.</li>
  <li>Шестиугольник — подготовка (инициализация цикла).</li>
</ul>''',
    },
    {
        'order': 4,
        'title': 'Программа и методика испытаний по ГОСТ 19.301-79',
        'content': '''<h2>Программа и методика испытаний по ГОСТ 19.301-79</h2>
<p>Программа и методика испытаний (ПМИ) — документ, описывающий порядок и критерии проверки ПО. Оформляется по ГОСТ 19.301-79.</p>

<h3>Структура ПМИ</h3>
<ol>
  <li>Объект испытаний (наименование, обозначение)</li>
  <li>Цель испытаний</li>
  <li>Требования к программе (со ссылками на ТЗ)</li>
  <li>Требования к программной документации</li>
  <li>Средства и порядок испытаний (оборудование, инструменты)</li>
  <li>Методы испытаний (тест-кейсы)</li>
</ol>

<h3>Пример тест-кейсов для МК-программы</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>№</th><th>Название теста</th><th>Входные данные</th><th>Ожидаемый результат</th><th>Метод проверки</th></tr>
  <tr><td>1</td><td>Корректность измерения в норме</td><td>Эталонный датчик 25,0 °C</td><td>Показание 24,9–25,1 °C</td><td>Визуально по ЖКИ + UART</td></tr>
  <tr><td>2</td><td>Аларм по верхней уставке</td><td>T=50°C, Tmax=40°C</td><td>Зуммер активен, LED красный</td><td>Осциллограф на PWM пин</td></tr>
  <tr><td>3</td><td>Отсутствие аларма в норме</td><td>T=25°C, Tmax=40°C, Tmin=10°C</td><td>Зуммер выключен</td><td>Измерение напряжения на пине</td></tr>
  <tr><td>4</td><td>Сохранение уставок</td><td>SET Tmax=60\r\n, выключение/включение</td><td>Tmax=60 после перезапуска</td><td>UART, чтение Flash дампа</td></tr>
  <tr><td>5</td><td>Формат UART</td><td>— (штатный режим)</td><td>JSON с полями t и ts</td><td>Парсинг в Python-скрипте</td></tr>
  <tr><td>6</td><td>Обрыв датчика</td><td>Отключить DS18B20</td><td>Сообщение "Err" на ЖКИ, аларм</td><td>Визуально + UART</td></tr>
</table>

<h3>Виды тестирования</h3>
<ul>
  <li><strong>Модульное тестирование</strong> — проверка отдельных функций/модулей (например, функции CRC16).</li>
  <li><strong>Интеграционное тестирование</strong> — взаимодействие модулей (драйвер датчика + основной цикл).</li>
  <li><strong>Системное тестирование</strong> — полный прогон на реальном железе.</li>
  <li><strong>Нагрузочное тестирование</strong> — длительная работа (72 ч) без сбоев.</li>
  <li><strong>Испытание в граничных условиях</strong> — питание на границе допуска, температурные крайности.</li>
</ul>

<h3>Оформление результатов испытаний</h3>
<pre><code>Протокол испытаний № 1

Дата: 15.06.2025
Исполнитель: Иванов И.И.

Тест № 1: Корректность измерения
  Установлена температура эталона: 25,0 °C
  Показание программы: 25,06 °C
  Допустимое отклонение: ±0,1 °C
  Результат: ПРОЙДЕН ✓

Тест № 6: Обрыв датчика
  Датчик отключён в момент t=5 с
  Реакция программы: через 1 с появилось "Sensor Error"
  Результат: ПРОЙДЕН ✓

Итог: все 6 тестов пройдены.
</code></pre>''',
    },
    {
        'order': 5,
        'title': 'Руководство пользователя и руководство оператора',
        'content': '''<h2>Руководство пользователя и руководство оператора</h2>
<p>Руководство пользователя — ключевой эксплуатационный документ. Для встраиваемых систем часто создаётся и руководство оператора (для обслуживающего персонала).</p>

<h3>Руководство пользователя (ГОСТ 19.505-79)</h3>
<p>Структура:</p>
<ol>
  <li>Назначение программы</li>
  <li>Условия выполнения программы (требования к оборудованию)</li>
  <li>Выполнение программы (порядок запуска, управление)</li>
  <li>Сообщения оператору (описание всех сообщений программы)</li>
</ol>

<h3>Пример раздела "Выполнение программы"</h3>
<pre><code>3. Выполнение программы

3.1 Запуск
После подачи питания (5 В ±5%) на плату контроллера:
1. На ЖКИ в течение 2 с отображается:
   "Thermometer v1.2"
   "Initializing..."
2. Устройство переходит в режим измерения.
3. На ЖКИ отображается текущая температура:
   "T = +23.56 C"
   "Tmax=40 Tmin=10"

3.2 Настройка уставок
Подключите ПК через USB-UART (CH340 или аналог).
Откройте терминал: 9600 Бод, 8N1, нет контроля потока.
Введите команду:
   SET Tmax=50&lt;Enter&gt;
Ответ устройства:
   OK: Tmax set to 50.0 C
</code></pre>

<h3>Пример раздела "Сообщения оператору"</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Сообщение</th><th>Причина</th><th>Действие</th></tr>
  <tr><td>"Sensor Error"</td><td>Нет связи с DS18B20</td><td>Проверить подключение, 4.7 кОм подтяжку</td></tr>
  <tr><td>"ALARM HIGH"</td><td>T > Tmax</td><td>Устранить перегрев объекта</td></tr>
  <tr><td>"ALARM LOW"</td><td>T < Tmin</td><td>Проверить систему обогрева</td></tr>
  <tr><td>"Flash Full"</td><td>Архив заполнен (24 ч)</td><td>Выгрузить архив по UART командой DUMP</td></tr>
  <tr><td>"ERR: Cmd"</td><td>Неверная команда</td><td>Проверить синтаксис команды</td></tr>
</table>

<h3>Руководство по программированию (ГОСТ 19.504-79)</h3>
<p>Для разработчиков, которые будут модифицировать ПО:</p>
<ul>
  <li>Среда разработки: STM32CubeIDE 1.15, arm-none-eabi-gcc 12.3.</li>
  <li>Зависимости: STM32 HAL F4 v1.28.0, FreeRTOS v10.5.1.</li>
  <li>Конфигурация проекта: открыть thermometer.ioc в CubeMX.</li>
  <li>Точки расширения: добавление новых UART-команд в модуле uart_log.c, функция parseCommand().</li>
  <li>Прошивка: st-flash write firmware.bin 0x08000000 или через STM32CubeProgrammer.</li>
</ul>''',
    },
    {
        'order': 6,
        'title': 'Обозначение документов и ГОСТ 19.103: практика оформления',
        'content': '''<h2>Обозначение документов и ГОСТ 19.103: практика оформления</h2>
<p>Система обозначений программных документов формализована в ГОСТ 19.103-77. Правильное обозначение обязательно для документов, подлежащих регистрации и хранению.</p>

<h3>Структура обозначения</h3>
<pre><code>XXXXX.YYYYYY.ZZZ ДД

XXXXX   — код организации-разработчика (5 знаков)
YYYYYY  — регистрационный номер (6 знаков, присваивается)
ZZZ     — номер издания / версии (3 знака)
ДД      — код вида документа
</code></pre>

<h3>Коды видов документов</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Код</th><th>Документ</th><th>ГОСТ</th></tr>
  <tr><td>ТЗ</td><td>Техническое задание</td><td>19.201</td></tr>
  <tr><td>ПД</td><td>Пояснительная записка</td><td>19.404</td></tr>
  <tr><td>ТП</td><td>Текст программы</td><td>19.401</td></tr>
  <tr><td>ПС</td><td>Описание программы</td><td>19.402</td></tr>
  <tr><td>ПМ</td><td>Программа и методика испытаний</td><td>19.301</td></tr>
  <tr><td>ИЭ</td><td>Руководство пользователя</td><td>19.505</td></tr>
  <tr><td>ФО</td><td>Формуляр</td><td>19.501</td></tr>
</table>

<h3>Пример обозначений для учебного проекта</h3>
<pre><code>ГБПОУ.000001.001 ТЗ — Техническое задание
ГБПОУ.000001.001 ПС — Описание программы
ГБПОУ.000001.001 ПМ — Программа и методика испытаний
ГБПОУ.000001.001 ИЭ — Руководство пользователя
</code></pre>

<h3>Оформление титульного листа (ГОСТ 19.104-78)</h3>
<pre><code>Министерство образования и науки Российской Федерации
[Полное наименование организации]

                                    УТВЕРЖДАЮ
                                    Директор ___________
                                    «___» ________ 20__ г.

[НАИМЕНОВАНИЕ ПРОГРАММЫ]
[Наименование документа]
[Обозначение документа]

Листов __

20__ г.
</code></pre>

<h3>Практические советы по оформлению</h3>
<ul>
  <li>Используй Microsoft Word или LibreOffice Writer со стилями заголовков — упрощает автосодержание.</li>
  <li>Нумеруй все разделы арабскими цифрами (1.1, 1.1.1).</li>
  <li>Таблицы нумеруй (Таблица 1 — Перечень команд).</li>
  <li>Рисунки нумеруй (Рисунок 1 — Схема алгоритма).</li>
  <li>Перечни — с дефисом или арабской цифрой со скобкой.</li>
  <li>Ссылки на пункты ТЗ в ПМИ: «в соответствии с п. 4.1.1 ТЗ».</li>
</ul>

<div class="tip">Минимальный комплект для учебной сдачи: ТЗ + Описание программы + ПМИ + Руководство пользователя. Для дипломной работы — добавляется пояснительная записка и схема алгоритма по ГОСТ 19.701.</div>''',
    },
]

M7_LESSONS = [
    {
        'order': 1,
        'title': 'Тестирование ПО МК: виды, стратегии, специфика',
        'content': '''<h2>Тестирование ПО МК: виды, стратегии, специфика</h2>
<p>Тестирование встраиваемого ПО сложнее тестирования прикладных программ: нет удобного вывода, реальное железо дорого и ограничено, часть ошибок проявляется только при специфических условиях (температура, питание, помехи).</p>

<h3>Классификация тестирования</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Уровень</th><th>Объект</th><th>Инструменты</th></tr>
  <tr><td>Модульное (Unit)</td><td>Отдельная функция/модуль</td><td>Unity, CppUTest, CMocka</td></tr>
  <tr><td>Интеграционное</td><td>Взаимодействие модулей</td><td>Реальный МК + логический анализатор</td></tr>
  <tr><td>Системное</td><td>Полная система</td><td>Стенд, эталонные приборы</td></tr>
  <tr><td>Регрессионное</td><td>Проверка после изменений</td><td>Автоматизированный тест-стенд</td></tr>
  <tr><td>Нагрузочное / Stress</td><td>Поведение на пределе</td><td>Долгий прогон, внешние воздействия</td></tr>
</table>

<h3>Специфика тестирования МК</h3>
<ul>
  <li><strong>Hardware-in-the-Loop (HIL)</strong> — МК управляет реальной нагрузкой, результат сравнивается с эталоном.</li>
  <li><strong>Software-in-the-Loop (SIL)</strong> — алгоритм запускается на ПК (эмуляция), без реального железа.</li>
  <li><strong>Тестирование на ПК</strong> — модульные тесты для аппаратно-независимых функций (CRC, протоколы, алгоритмы).</li>
  <li><strong>Симуляторы</strong> — QEMU (ARM), Proteus (полная схема), Renode (целые системы).</li>
</ul>

<h3>Стратегия "Test Early"</h3>
<p>Для надёжного ПО МК рекомендуется:</p>
<ol>
  <li>Писать функции с отделением логики от аппаратуры (Layered Architecture).</li>
  <li>Тестировать логику на ПК (Unity framework) — быстро и без железа.</li>
  <li>Тестировать драйверы на реальном МК с осциллографом.</li>
  <li>Проводить системные тесты на тестовом стенде.</li>
</ol>

<h3>Наиболее частые ошибки в ПО МК</h3>
<ul>
  <li>Переполнение стека (stack overflow).</li>
  <li>Гонки данных между ISR и основным кодом (race condition).</li>
  <li>Зависание при ожидании периферии без таймаута.</li>
  <li>Неверное тактирование (забыли включить RCC).</li>
  <li>Проблемы с volatile (компилятор оптимизирует обращения к регистрам).</li>
  <li>Выход за границы массива (buffer overflow).</li>
  <li>Integer overflow при расчётах с uint8_t/uint16_t.</li>
</ul>

<div class="tip">Правило для надёжного кода МК: каждая функция, взаимодействующая с аппаратурой, должна возвращать код ошибки или иметь явный таймаут. Бесконечное ожидание — источник зависаний.</div>''',
    },
    {
        'order': 2,
        'title': 'Модульное тестирование на ПК: Unity framework',
        'content': '''<h2>Модульное тестирование на ПК: Unity framework</h2>
        <p>Unity — минималистичный фреймворк для юнит-тестирования на Си. Работает на ПК и на МК. Идеален для тестирования бизнес-логики и протоколов без реального железа.</p>

<h3>Архитектура "Testable Embedded Code"</h3>
<p>Разделяй аппаратно-зависимый и независимый код:</p>
<pre><code>// BAD: смешано всё в одном
void updateDisplay(void) {
    float t = readDS18B20();   // аппаратура
    char buf[16];
    sprintf(buf, "T=%.1f", t); // логика
    LCD_Print(buf);             // аппаратура
}

// GOOD: разделено
float DS18B20_Read(void);          // реализация — аппаратура
char* formatTemperature(float t);  // реализация — чистая логика → тестируется на ПК
void LCD_Print(const char *s);     // реализация — аппаратура
</code></pre>

<h3>Установка и структура проекта Unity</h3>
<pre><code>project/
├── src/
│   ├── temperature.c   # логика
│   └── temperature.h
├── test/
│   ├── unity/          # Unity framework (unity.c, unity.h)
│   ├── test_main.c     # точка входа тестов
│   └── test_temperature.c
└── Makefile
</code></pre>

<h3>Пример тестов (Unity)</h3>
<pre><code>#include "unity.h"
#include "temperature.h"

void setUp(void) {}     // перед каждым тестом
void tearDown(void) {}  // после каждого теста

void test_formatTemperature_positive(void) {
    char *result = formatTemperature(23.5f);
    TEST_ASSERT_EQUAL_STRING("T=+23.5 C", result);
}

void test_formatTemperature_negative(void) {
    char *result = formatTemperature(-5.25f);
    TEST_ASSERT_EQUAL_STRING("T=-5.3 C", result);
}

void test_tempInRange_normal(void) {
    TEST_ASSERT_TRUE(isTempInRange(25.0f, 10.0f, 40.0f));
}

void test_tempInRange_above(void) {
    TEST_ASSERT_FALSE(isTempInRange(50.0f, 10.0f, 40.0f));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_formatTemperature_positive);
    RUN_TEST(test_formatTemperature_negative);
    RUN_TEST(test_tempInRange_normal);
    RUN_TEST(test_tempInRange_above);
    return UNITY_END();
}
</code></pre>

<h3>Вывод Unity</h3>
<pre><code>test/test_temperature.c:12:test_formatTemperature_positive:PASS
test/test_temperature.c:17:test_formatTemperature_negative:PASS
test/test_temperature.c:22:test_tempInRange_normal:PASS
test/test_temperature.c:26:test_tempInRange_above:PASS

-----------------------
4 Tests 0 Failures 0 Ignored
OK
</code></pre>

<h3>Мокирование аппаратуры (CMock)</h3>
<pre><code>// CMock генерирует моки для HAL-функций
// mock_stm32f4xx_hal_uart.h — автогенерация

void test_sendData_callsUART(void) {
    // Ожидаем вызов HAL_UART_Transmit с нужными аргументами
    HAL_UART_Transmit_ExpectAndReturn(
        &huart1, (uint8_t*)"{\"t\":25.0}", 10, 100, HAL_OK
    );
    sendTemperatureUART(25.0f);
    // CMock автоматически проверит вызов
}
</code></pre>''',
    },
    {
        'order': 3,
        'title': 'Тестирование на реальном МК: инструменты и методы',
        'content': '''<h2>Тестирование на реальном МК: инструменты и методы</h2>
<p>Некоторые ошибки проявляются только на реальном железе: таймингбаги, проблемы с прерываниями, EMC. Тестирование на МК требует специальных инструментов.</p>

<h3>Инструменты для тестирования на МК</h3>
<ul>
  <li><strong>Осциллограф</strong> — измерение формы сигнала, таймингов, дребезга.</li>
  <li><strong>Логический анализатор</strong> — декодирование протоколов (SPI, I2C, UART, CAN). Saleae Logic, DSLOGIC, PulseView.</li>
  <li><strong>Мультиметр</strong> — потребление тока, уровни напряжения.</li>
  <li><strong>JTAG/SWD отладчик</strong> — точки останова, просмотр памяти в реальном времени.</li>
  <li><strong>Анализатор протоколов</strong> — CAN, RS-485, Modbus.</li>
</ul>

<h3>Метод "GPIO Signaling" для измерения времени</h3>
<pre><code>// Вместо таймеров — переключение GPIO и осциллограф
void criticalSection(void) {
    GPIOB->BSRR = GPIO_PIN_0;    // HIGH: начало измерения

    // ... код, время которого измеряем ...

    GPIOB->BSRR = GPIO_PIN_0 << 16; // LOW: конец измерения
}
// Осциллограф покажет ширину импульса = время выполнения
</code></pre>

<h3>Тестирование прерываний</h3>
<pre><code>// Счётчик вызовов ISR для верификации
volatile uint32_t isrCount = 0;

void TIM2_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim2);
    isrCount++;
}

// В main через 10 секунд:
// isrCount должен быть ≈ 10000 (если частота 1 кГц)
HAL_Delay(10000);
uint32_t expected = 10000;
uint32_t error = abs((int)isrCount - expected);
// error > 10 → проблема с тактированием
</code></pre>

<h3>Тестирование UART</h3>
<pre><code># Python-скрипт для автоматизированного тестирования UART
import serial, json, time

ser = serial.Serial('COM3', 9600, timeout=2)

# Тест 1: Формат JSON
line = ser.readline().decode().strip()
data = json.loads(line)
assert 't' in data, "Поле 't' отсутствует"
assert 'ts' in data, "Поле 'ts' отсутствует"
assert -55 &lt;= data['t'] &lt;= 125, "Температура вне диапазона"
print("Тест 1 PASS")

# Тест 2: Команда SET
ser.write(b"SET Tmax=50\r\n")
resp = ser.readline().decode()
assert "OK" in resp, f"Неверный ответ: {resp}"
print("Тест 2 PASS")
</code></pre>

<h3>Тестирование потребления тока</h3>
<p>Для IoT-устройств критично измерить потребление в каждом режиме:</p>
<ul>
  <li>Nordic PPK2 (Power Profiler Kit) — прецизионное измерение тока с временным разрешением.</li>
  <li>Keysight N6705C — лабораторный источник питания со встроенным анализатором мощности.</li>
  <li>Самодельно: шунт 1 Ом + осциллограф — грубо, но достаточно для сравнения режимов.</li>
</ul>

<div class="tip">Золотое правило тестирования МК: протоколируй все тесты. Дата, версия прошивки, оборудование стенда, результаты — в файл или журнал. При возврате дефекта будет понятно, что и когда проверялось.</div>''',
    },
    {
        'order': 4,
        'title': 'Покрытие кода, граничные значения и негативные тесты',
        'content': '''<h2>Покрытие кода, граничные значения и негативные тесты</h2>
<p>Качество тестирования определяется не количеством тестов, а покрытием критических путей выполнения и граничных случаев.</p>

<h3>Виды покрытия кода</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Покрытие</th><th>Что проверяет</th><th>Сложность</th></tr>
  <tr><td>Statement (строки)</td><td>Каждая строка выполнена хотя бы раз</td><td>Простое</td></tr>
  <tr><td>Branch (ветви)</td><td>Каждая ветвь if/else пройдена</td><td>Среднее</td></tr>
  <tr><td>Condition</td><td>Каждое условие принимало T и F</td><td>Сложное</td></tr>
  <tr><td>MC/DC</td><td>Каждое условие независимо влияет на результат</td><td>Для критических систем</td></tr>
  <tr><td>Path</td><td>Все пути через функцию</td><td>Экспоненциальный рост</td></tr>
</table>
<p>DO-178C (авиационные системы) требует 100% MC/DC для уровня A. ГОСТ Р МЭК 61508 (промышленная безопасность) — MC/DC для SIL 3/4.</p>

<h3>Измерение покрытия (gcov/lcov)</h3>
<pre><code># Компиляция с инструментацией
gcc -fprofile-arcs -ftest-coverage -o test test_main.c temperature.c unity/unity.c

# Запуск тестов
./test

# Генерация отчёта
gcov temperature.c
# Выводит: температуру.c: 87.50% of 16 lines executed

# HTML-отчёт (lcov)
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html
</code></pre>

<h3>Техника граничных значений</h3>
<pre><code>// Функция проверки диапазона температуры
bool isTempInRange(float t, float tmin, float tmax) {
    return t >= tmin && t <= tmax;
}

// Граничные тесты:
// t = tmin        → true  (на нижней границе)
// t = tmin - 0.1  → false (чуть ниже)
// t = tmax        → true  (на верхней границе)
// t = tmax + 0.1  → false (чуть выше)
// t = (tmin+tmax)/2 → true (середина диапазона)

TEST_ASSERT_TRUE(isTempInRange(10.0f, 10.0f, 40.0f));   // граница
TEST_ASSERT_FALSE(isTempInRange(9.9f, 10.0f, 40.0f));   // чуть ниже
TEST_ASSERT_TRUE(isTempInRange(40.0f, 10.0f, 40.0f));   // граница
TEST_ASSERT_FALSE(isTempInRange(40.1f, 10.0f, 40.0f));  // чуть выше
</code></pre>

<h3>Негативные тесты</h3>
<pre><code>// Тест: NULL-указатель
void test_parse_nullInput(void) {
    ParseResult r = parseCommand(NULL);
    TEST_ASSERT_EQUAL(PARSE_ERROR_NULL, r.error);
}

// Тест: пустая строка
void test_parse_emptyString(void) {
    ParseResult r = parseCommand("");
    TEST_ASSERT_EQUAL(PARSE_ERROR_EMPTY, r.error);
}

// Тест: слишком длинная команда (буфер overflow защита)
void test_parse_oversizedInput(void) {
    char longCmd[200];
    memset(longCmd, 'A', 199);
    longCmd[199] = '\0';
    ParseResult r = parseCommand(longCmd);
    TEST_ASSERT_EQUAL(PARSE_ERROR_TOO_LONG, r.error);
}
</code></pre>

<h3>Тестирование в граничных физических условиях</h3>
<ul>
  <li>Питание на нижней границе допуска (3,0 В вместо 3,3 В).</li>
  <li>Питание на верхней границе (3,6 В).</li>
  <li>Температура эксплуатации: -20°C (холодный пуск), +70°C (нагрев в корпусе).</li>
  <li>Длительная работа: 72–168 ч непрерывно.</li>
  <li>Входные данные на границах диапазона датчика.</li>
</ul>''',
    },
    {
        'order': 5,
        'title': 'Автоматизированное тестирование и CI для МК',
        'content': '''<h2>Автоматизированное тестирование и CI для МК</h2>
<p>Автоматизация тестирования сокращает время проверки и исключает человеческий фактор. Для МК возможны два уровня: тесты на ПК и тесты на реальном железе.</p>

<h3>Тесты на ПК в CI (GitHub Actions)</h3>
<pre><code># .github/workflows/test.yml
name: Unit Tests

on: [push, pull_request]

jobs:
  unit_test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: sudo apt-get install -y gcc gcov lcov

      - name: Build and run tests
        run: |
          gcc -fprofile-arcs -ftest-coverage \
              -o test_runner \
              test/test_temperature.c \
              src/temperature.c \
              test/unity/unity.c
          ./test_runner

      - name: Generate coverage report
        run: |
          gcov src/temperature.c
          lcov --capture --directory . -o coverage.info
          genhtml coverage.info -o coverage_html

      - name: Check coverage threshold
        run: |
          coverage=$(lcov --summary coverage.info 2>&1 | grep lines | grep -o "[0-9.]*%" | head -1)
          echo "Coverage: $coverage"
          # Fail if below 80%
          python3 -c "v=float('$coverage'[:-1]); exit(0 if v>=80 else 1)"

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage_html/
</code></pre>

<h3>Тест-стенд с реальным МК</h3>
<p>Для автоматизации тестов на железе нужен управляемый стенд:</p>
<pre><code>┌────────────────────────────────────────────────────────────┐
│  CI Server (Raspberry Pi / ПК)                            │
│    - Python pytest                                         │
│    - st-flash (прошивка МК)                               │
│    - pyserial (чтение UART результатов)                   │
└──────────────────────┬─────────────────────────────────────┘
                       │ USB (ST-Link + UART)
                  ┌────▼────┐
                  │  STM32  │── GPIO ──► Тестируемая схема
                  └─────────┘
</code></pre>

<h3>Python pytest для тестирования через UART</h3>
<pre><code># tests/test_firmware.py
import pytest, serial, time

@pytest.fixture
def device():
    ser = serial.Serial('COM3', 9600, timeout=3)
    time.sleep(0.5)  # МК перезагружается при открытии порта
    yield ser
    ser.close()

def test_temperature_json_format(device):
    device.flushInput()
    line = device.readline().decode().strip()
    import json
    data = json.loads(line)
    assert 't' in data
    assert isinstance(data['t'], float)
    assert -55 <= data['t'] <= 125

def test_set_tmax_command(device):
    device.write(b"SET Tmax=55\r\n")
    resp = device.readline().decode()
    assert "OK" in resp
    assert "55" in resp

def test_invalid_command(device):
    device.write(b"INVALID_CMD\r\n")
    resp = device.readline().decode()
    assert "ERR" in resp
</code></pre>
<pre><code># Запуск
pytest tests/ -v --tb=short
</code></pre>

<div class="tip">Инвестируй в тест-стенд с самого начала проекта. Прошивка МК + прогон тестов = 2 минуты автоматически. Ручная проверка того же набора = 30+ минут. При 10 итерациях в день — экономия 4+ часов ежедневно.</div>''',
    },
    {
        'order': 6,
        'title': 'Дефекты, трекинг и верификация исправлений',
        'content': '''<h2>Дефекты, трекинг и исправления в разработке ПО МК</h2>
<p>Управление дефектами — обязательная часть разработки промышленного ПО. Без трекинга дефекты теряются, исправления не проверяются, и устройства уходят к заказчику с известными ошибками.</p>

<h3>Жизненный цикл дефекта</h3>
<ol>
  <li><strong>Обнаружение</strong> — тестировщик или пользователь воспроизводит ошибку.</li>
  <li><strong>Регистрация</strong> — создание задачи в трекере (GitHub Issues, Jira, YouTrack).</li>
  <li><strong>Классификация</strong> — серьёзность (severity), приоритет (priority).</li>
  <li><strong>Анализ</strong> — разработчик определяет корневую причину (root cause).</li>
  <li><strong>Исправление</strong> — fix в коде с коммитом (ссылка на номер дефекта).</li>
  <li><strong>Верификация</strong> — тестировщик проверяет исправление по тест-кейсу дефекта.</li>
  <li><strong>Закрытие</strong> — дефект закрывается, регрессионный тест добавляется в набор.</li>
</ol>

<h3>Классификация серьёзности дефектов</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Уровень</th><th>Описание</th><th>Пример в МК ПО</th></tr>
  <tr><td>Critical</td><td>Система не работает, данные теряются</td><td>HardFault при нормальной работе</td></tr>
  <tr><td>High</td><td>Основная функция нарушена</td><td>Аларм не срабатывает при T>Tmax</td></tr>
  <tr><td>Medium</td><td>Частичная потеря функциональности</td><td>Неверный формат JSON раз в 100 циклов</td></tr>
  <tr><td>Low</td><td>Косметика, неудобство</td><td>Лишний пробел в сообщении на ЖКИ</td></tr>
</table>

<h3>Шаблон описания дефекта</h3>
<pre><code>Title: Аларм не срабатывает при T > Tmax в режиме Deep Sleep

Severity: High
Priority: P1

Steps to reproduce:
1. Установить Tmax = 30°C
2. Включить режим Deep Sleep командой SLEEP
3. Нагреть датчик до 35°C
4. Наблюдать светодиод аларма

Expected: LED RED включается в течение 2 с после выхода из Sleep
Actual:   LED остаётся выключенным; аларм не срабатывает

Environment:
  Firmware: v1.3.2 (commit abc1234)
  Board: Nucleo-F411RE
  DS18B20 s/n: 28FF4A22..

Root cause analysis:
  В функции wakeFromSleep() не вызывается checkAlarms().
  После выхода из Sleep проверка уставок происходит только
  через 1 цикл (1 с), но в данном сценарии цикл не завершён.

Fix: в wakeFromSleep() добавить вызов checkAlarms() перед возвратом.
</code></pre>

<h3>Регрессионное тестирование</h3>
<pre><code># При закрытии дефекта — добавить тест в regression suite
def test_alarm_after_sleep_wakeup(device):
    """Регрессия: BUG-047 — аларм должен сработать после Sleep"""
    device.write(b"SET Tmax=30\r\n")
    device.write(b"SLEEP\r\n")
    time.sleep(2)
    # Имитация нагрева (на тест-стенде: включить нагреватель)
    resp = device.readline().decode()
    assert "ALARM HIGH" in resp, "BUG-047 регрессия: аларм не сработал"
</code></pre>

<div class="tip">Каждый закрытый дефект должен оставлять след: регрессионный тест + ссылка в коммите (git commit -m "fix: alarm after sleep wakeup — closes #47"). Это гарантирует, что ошибка не вернётся незамеченной.</div>''',
    },
]


class Command(BaseCommand):
    help = 'Expand RVES modules M5, M6, M7 to 6 detailed lessons each'

    def handle(self, *args, **options):
        subject = Subject.objects.get(slug='rves')

        for mod_order, mod_title, lessons in [
            (5, 'Инструментальные средства разработки ПО МК', M5_LESSONS),
            (6, 'ЕСПД и документация', M6_LESSONS),
            (7, 'Тестирование ПО', M7_LESSONS),
        ]:
            module = TheoryModule.objects.filter(subject=subject, order=mod_order).first()
            if not module:
                self.stderr.write(f'Module M{mod_order} not found')
                continue
            for lesson in lessons:
                obj, created = TheoryLesson.objects.update_or_create(
                    module=module,
                    order=lesson['order'],
                    defaults={**lesson, 'module': module},
                )
                status = 'created' if created else 'updated'
                self.stdout.write(f'  M{mod_order} урок {lesson["order"]}: {lesson["title"][:50]} [{status}]')
            self.stdout.write(f'Module M{mod_order}: 6 lessons done')

        self.stdout.write('Done: RVES M5-M7 expanded')
