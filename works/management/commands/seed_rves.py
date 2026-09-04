"""
Seed: Разработка ПО для встраиваемых систем (МДК.04.02)
Специальность: Разработка электронных устройств и систем
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson, Quiz, Question, AnswerChoice

SUBJECT = {
    'slug': 'rves',
    'title': 'Разработка ПО для встраиваемых систем',
    'icon': 'fas fa-microchip',
    'color': '#e8562a',
    'description': 'МДК.04.02. Специальность: Разработка электронных устройств и систем. '
                   'Программирование встраиваемых систем: C для МК, RTOS, периферия, оптимизация.',
    'order': 3,
}

MODULES = [
    {
        'title': 'Введение в встраиваемые системы',
        'icon': 'fas fa-microchip',
        'order': 1,
        'description': 'Архитектура МК, инструменты разработки, первый проект',
        'lessons': [
            {
                'title': 'Что такое встраиваемая система',
                'order': 1,
                'estimated_minutes': 15,
                'content': (
                    '<h3>Встраиваемые системы</h3>'
                    '<p>Встраиваемая (embedded) система — компьютер, встроенный в другое устройство '
                    'для выполнения специализированной функции. Примеры: стиральная машина, '
                    'автомобильный ЭБУ, медицинский кардиомонитор, промышленный ПЛК.</p>'
                    '<h3>Отличия от ПК</h3>'
                    '<table><tr><th>Параметр</th><th>ПК</th><th>Встраиваемая система</th></tr>'
                    '<tr><td>Назначение</td><td>Общего назначения</td><td>Специализированная задача</td></tr>'
                    '<tr><td>Ресурсы</td><td>ГБ RAM, ГГц CPU</td><td>КБ RAM, МГц CPU</td></tr>'
                    '<tr><td>ОС</td><td>Windows/Linux</td><td>RTOS или bare-metal</td></tr>'
                    '<tr><td>Питание</td><td>100+ Вт</td><td>мкВт — Вт</td></tr>'
                    '<tr><td>Реальное время</td><td>Не гарантировано</td><td>Детерминированное</td></tr></table>'
                    '<h3>Классификация по мощности</h3>'
                    '<ul>'
                    '<li><strong>Микроконтроллеры (MCU)</strong>: AVR, STM32, PIC — КБ RAM, простые задачи</li>'
                    '<li><strong>Микропроцессоры (MPU)</strong>: Raspberry Pi CM, i.MX — МБ RAM, Linux</li>'
                    '<li><strong>DSP</strong>: TMS320 — обработка сигналов, аудио, радар</li>'
                    '<li><strong>FPGA</strong>: Xilinx, Intel Altera — параллельная логика</li>'
                    '</ul>'
                    '<h3>Требования к встраиваемому ПО</h3>'
                    '<ul>'
                    '<li><strong>Реальное время</strong> — реакция за гарантированное время</li>'
                    '<li><strong>Надёжность</strong> — работа без сбоев месяцы и годы</li>'
                    '<li><strong>Минимум ресурсов</strong> — вписаться в КБ flash и RAM</li>'
                    '<li><strong>Детерминизм</strong> — одинаковое поведение при одинаковых условиях</li>'
                    '</ul>'
                ),
                'code_example': '',
            },
            {
                'title': 'Инструменты разработки: компилятор и IDE',
                'order': 2,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Цепочка инструментов (toolchain)</h3>'
                    '<p>Разработка встраиваемого ПО требует специального набора инструментов, '
                    'отличного от десктопной разработки.</p>'
                    '<h3>Компилятор GCC для ARM/AVR</h3>'
                    '<ul>'
                    '<li><strong>arm-none-eabi-gcc</strong> — для ARM Cortex-M (STM32, NXP)</li>'
                    '<li><strong>avr-gcc</strong> — для Atmel AVR (Arduino, ATmega)</li>'
                    '<li><strong>riscv32-unknown-elf-gcc</strong> — для RISC-V МК</li>'
                    '</ul>'
                    '<h3>Процесс сборки</h3>'
                    '<pre>Исходник (.c) → Препроцессор → Компилятор → Ассемблер (.o) → Линковщик → .elf → .hex/.bin</pre>'
                    '<h3>Ключевые опции компилятора</h3>'
                    '<table><tr><th>Флаг</th><th>Смысл</th></tr>'
                    '<tr><td>-Os</td><td>Оптимизация по размеру кода</td></tr>'
                    '<tr><td>-O2</td><td>Оптимизация по скорости</td></tr>'
                    '<tr><td>-g</td><td>Отладочная информация</td></tr>'
                    '<tr><td>-Wall -Wextra</td><td>Все предупреждения</td></tr>'
                    '<tr><td>-mcpu=cortex-m4</td><td>Целевой процессор</td></tr>'
                    '<tr><td>-mthumb</td><td>Режим Thumb (компактный код)</td></tr></table>'
                    '<h3>IDE и среды</h3>'
                    '<ul>'
                    '<li><strong>STM32CubeIDE</strong> — Eclipse-based, для STM32, бесплатно</li>'
                    '<li><strong>Keil MDK</strong> — промышленный стандарт ARM, платный</li>'
                    '<li><strong>IAR EWARM</strong> — лучшая оптимизация, платный</li>'
                    '<li><strong>VS Code + PlatformIO</strong> — современный, бесплатный, все платформы</li>'
                    '<li><strong>Arduino IDE</strong> — простой вход, ограниченный контроль</li>'
                    '</ul>'
                ),
                'code_example': (
                    '# Makefile для bare-metal STM32\n'
                    'CC = arm-none-eabi-gcc\n'
                    'CFLAGS = -mcpu=cortex-m4 -mthumb -Os -Wall -Wextra\n'
                    'LDFLAGS = -T linker.ld -nostartfiles\n\n'
                    'TARGET = firmware\n'
                    'SRCS = main.c startup.c\n'
                    'OBJS = $(SRCS:.c=.o)\n\n'
                    'all: $(TARGET).hex\n\n'
                    '$(TARGET).elf: $(OBJS)\n'
                    '\t$(CC) $(LDFLAGS) -o $@ $^\n\n'
                    '$(TARGET).hex: $(TARGET).elf\n'
                    '\tarm-none-eabi-objcopy -O ihex $< $@\n\n'
                    'flash: $(TARGET).hex\n'
                    '\tst-flash write $(TARGET).bin 0x08000000\n\n'
                    'clean:\n'
                    '\trm -f *.o *.elf *.hex *.bin'
                ),
            },
            {
                'title': 'Структура программы для МК',
                'order': 3,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Startup-код и карта памяти</h3>'
                    '<p>Программа для МК начинается не с main(), а с вектора сброса (Reset_Handler). '
                    'Startup-файл инициализирует стек, копирует данные из Flash в RAM, очищает BSS, '
                    'вызывает конструкторы C++ и передаёт управление main().</p>'
                    '<h3>Карта памяти STM32F4</h3>'
                    '<table><tr><th>Адрес</th><th>Область</th><th>Размер</th></tr>'
                    '<tr><td>0x08000000</td><td>Flash (код)</td><td>1 МБ</td></tr>'
                    '<tr><td>0x20000000</td><td>SRAM (данные)</td><td>128 КБ</td></tr>'
                    '<tr><td>0x40000000</td><td>Периферия (APB1)</td><td>—</td></tr>'
                    '<tr><td>0x40020000</td><td>Периферия (AHB1)</td><td>—</td></tr>'
                    '<tr><td>0xE000E000</td><td>NVIC, SysTick</td><td>—</td></tr></table>'
                    '<h3>Секции программы</h3>'
                    '<ul>'
                    '<li><strong>.text</strong> — код и константы, хранится в Flash</li>'
                    '<li><strong>.data</strong> — инициализированные глобальные переменные, '
                    'хранятся в Flash, копируются в RAM при старте</li>'
                    '<li><strong>.bss</strong> — неинициализированные глобальные (обнуляются при старте)</li>'
                    '<li><strong>.stack</strong> — стек (уменьшается от верхнего адреса RAM)</li>'
                    '<li><strong>.heap</strong> — динамическая память (malloc)</li>'
                    '</ul>'
                    '<h3>Таблица векторов прерываний</h3>'
                    '<p>Первые 4 байта — начальное значение SP. Затем адреса обработчиков: Reset, NMI, '
                    'HardFault, ... и периферийные прерывания. Хранится в начале Flash.</p>'
                ),
                'code_example': (
                    '// Минимальный startup для Cortex-M\n'
                    '#include <stdint.h>\n\n'
                    'extern uint32_t _stack_top;  // из linker script\n'
                    'extern uint32_t _data_start, _data_end, _data_load;\n'
                    'extern uint32_t _bss_start, _bss_end;\n\n'
                    'void Reset_Handler(void);\n'
                    'void Default_Handler(void) { while(1); }\n\n'
                    'int main(void);\n\n'
                    '// Таблица векторов прерываний\n'
                    '__attribute__((section(".vectors")))\n'
                    'const void* vectors[] = {\n'
                    '    &_stack_top,       // Начальный SP\n'
                    '    Reset_Handler,     // Reset\n'
                    '    Default_Handler,   // NMI\n'
                    '    Default_Handler,   // HardFault\n'
                    '    // ...\n'
                    '};\n\n'
                    'void Reset_Handler(void) {\n'
                    '    // Копировать .data из Flash в RAM\n'
                    '    uint32_t *src = &_data_load;\n'
                    '    for (uint32_t *dst = &_data_start; dst < &_data_end;)\n'
                    '        *dst++ = *src++;\n'
                    '    // Обнулить .bss\n'
                    '    for (uint32_t *p = &_bss_start; p < &_bss_end;)\n'
                    '        *p++ = 0;\n'
                    '    main();\n'
                    '    while(1);\n'
                    '}'
                ),
            },
            {
                'title': 'Регистры периферии и битовые операции',
                'order': 4,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Доступ к регистрам периферии</h3>'
                    '<p>Периферия МК управляется через регистры, отображённые в адресное пространство '
                    '(Memory-Mapped I/O). Читаем/пишем как обычную память, но по фиксированным адресам.</p>'
                    '<h3>volatile — ключевое слово</h3>'
                    '<p>Все указатели на регистры периферии должны быть <code>volatile</code>. '
                    'Это запрещает компилятору кэшировать значение регистра в переменной — '
                    'регистр может измениться аппаратно в любой момент.</p>'
                    '<h3>Битовые операции</h3>'
                    '<table><tr><th>Операция</th><th>Код</th><th>Смысл</th></tr>'
                    '<tr><td>Установить бит N</td><td>reg |= (1 &lt;&lt; N)</td><td>OR с маской</td></tr>'
                    '<tr><td>Сбросить бит N</td><td>reg &= ~(1 &lt;&lt; N)</td><td>AND с инверсией</td></tr>'
                    '<tr><td>Переключить бит N</td><td>reg ^= (1 &lt;&lt; N)</td><td>XOR с маской</td></tr>'
                    '<tr><td>Проверить бит N</td><td>if (reg &amp; (1 &lt;&lt; N))</td><td>AND с маской</td></tr>'
                    '<tr><td>Записать поле</td><td>reg = (reg &amp; ~MASK) | (val &lt;&lt; POS)</td><td>Read-Modify-Write</td></tr></table>'
                    '<h3>Структуры для группировки регистров (CMSIS)</h3>'
                    '<p>CMSIS определяет typedef-структуры для каждого периферийного блока, '
                    'что позволяет писать <code>GPIOA->ODR |= GPIO_PIN_5</code> '
                    'вместо <code>*(volatile uint32_t*)0x40020014 |= (1&lt;&lt;5)</code>.</p>'
                ),
                'code_example': (
                    '// Прямая работа с регистрами STM32\n'
                    '#include <stdint.h>\n\n'
                    '// Базовые адреса\n'
                    '#define RCC_BASE   0x40023800\n'
                    '#define GPIOA_BASE 0x40020000\n\n'
                    '// Структуры регистров\n'
                    'typedef struct {\n'
                    '    volatile uint32_t MODER;   // Mode register\n'
                    '    volatile uint32_t OTYPER;  // Output type\n'
                    '    volatile uint32_t OSPEEDR; // Speed\n'
                    '    volatile uint32_t PUPDR;   // Pull-up/down\n'
                    '    volatile uint32_t IDR;     // Input data\n'
                    '    volatile uint32_t ODR;     // Output data\n'
                    '    volatile uint32_t BSRR;    // Bit set/reset\n'
                    '    volatile uint32_t LCKR;\n'
                    '    volatile uint32_t AFR[2];\n'
                    '} GPIO_t;\n\n'
                    'typedef struct {\n'
                    '    volatile uint32_t CR;       // Control\n'
                    '    volatile uint32_t PLLCFGR;\n'
                    '    volatile uint32_t CFGR;\n'
                    '    volatile uint32_t CIR;\n'
                    '    volatile uint32_t AHB1ENR;  // AHB1 clocks\n'
                    '    // ...\n'
                    '} RCC_t;\n\n'
                    '#define GPIOA ((GPIO_t*)GPIOA_BASE)\n'
                    '#define RCC   ((RCC_t*)RCC_BASE)\n\n'
                    'int main(void) {\n'
                    '    // Включить тактирование GPIOA\n'
                    '    RCC->AHB1ENR |= (1 << 0);\n'
                    '    // PA5 = выход (MODER[11:10] = 01)\n'
                    '    GPIOA->MODER &= ~(3 << 10);\n'
                    '    GPIOA->MODER |=  (1 << 10);\n'
                    '    // Мигать PA5\n'
                    '    while (1) {\n'
                    '        GPIOA->ODR ^= (1 << 5);\n'
                    '        for (volatile int i = 0; i < 100000; i++);\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'Отладка встраиваемого ПО',
                'order': 5,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Методы отладки</h3>'
                    '<h3>1. JTAG/SWD отладчик</h3>'
                    '<p>Золотой стандарт. Позволяет: остановить CPU, читать/писать память и регистры, '
                    'ставить точки останова, трассировку инструкций.</p>'
                    '<ul>'
                    '<li><strong>ST-Link</strong> — встроен в отладочные платы STM32 Nucleo/Discovery</li>'
                    '<li><strong>J-Link</strong> — лучший коммерческий отладчик, быстрый Flash</li>'
                    '<li><strong>CMSIS-DAP / DAPLink</strong> — открытый стандарт</li>'
                    '</ul>'
                    '<h3>2. Printf через UART</h3>'
                    '<p>Простейший способ: перенаправить stdout на UART, читать в терминале. '
                    'Минус: изменяет тайминги, может скрыть ошибки реального времени.</p>'
                    '<h3>3. Semihosting</h3>'
                    '<p>printf() через отладчик без UART. Медленно, только с подключённым отладчиком.</p>'
                    '<h3>4. RTT (Real-Time Transfer)</h3>'
                    '<p>Segger RTT — буфер в RAM, данные читает отладчик не останавливая CPU. '
                    'Быстро, не влияет на тайминги.</p>'
                    '<h3>5. LED-индикация</h3>'
                    '<p>Мигание светодиодами — самый древний метод. Работает когда нет ничего другого.</p>'
                    '<h3>HardFault анализ</h3>'
                    '<p>При HardFault — посмотреть стек: PC (адрес упавшей инструкции), LR (откуда вызов), '
                    'CFSR/HFSR регистры причины. arm-none-eabi-addr2line по адресу даст строку кода.</p>'
                ),
                'code_example': (
                    '// Printf через UART (retarget)\n'
                    '#include <stdio.h>\n'
                    '#include "usart.h"\n\n'
                    '// Перехватить _write для printf\n'
                    'int _write(int fd, char *ptr, int len) {\n'
                    '    (void)fd;\n'
                    '    HAL_UART_Transmit(&huart2, (uint8_t*)ptr, len, 100);\n'
                    '    return len;\n'
                    '}\n\n'
                    '// HardFault handler с дампом регистров\n'
                    'void HardFault_Handler(void) __attribute__((naked));\n'
                    'void HardFault_Handler(void) {\n'
                    '    __asm volatile (\n'
                    '        "tst lr, #4 \\n"\n'
                    '        "ite eq \\n"\n'
                    '        "mrseq r0, msp \\n"\n'
                    '        "mrsne r0, psp \\n"\n'
                    '        "ldr r1, =hard_fault_handler_c \\n"\n'
                    '        "bx r1 \\n"\n'
                    '    );\n'
                    '}\n\n'
                    'void hard_fault_handler_c(uint32_t *sp) {\n'
                    '    printf("HardFault! PC=0x%08lX LR=0x%08lX\\n",\n'
                    '           sp[6], sp[5]);\n'
                    '    while(1);\n'
                    '}'
                ),
            },
            {
                'title': 'Язык C для встраиваемых систем',
                'order': 6,
                'estimated_minutes': 25,
                'content': (
                    '<h3>Особенности C во встраиваемых системах</h3>'
                    '<p>Стандарт C11/C99 используется для встраиваемых систем. '
                    'Но не всё из "обычного" C применимо.</p>'
                    '<h3>Типы с фиксированным размером (stdint.h)</h3>'
                    '<p>ВСЕГДА используйте uint8_t, int16_t и т.д. вместо int, char — '
                    'размер обычных типов зависит от архитектуры!</p>'
                    '<table><tr><th>Тип</th><th>Размер</th><th>Диапазон</th></tr>'
                    '<tr><td>uint8_t</td><td>8 бит</td><td>0..255</td></tr>'
                    '<tr><td>int8_t</td><td>8 бит</td><td>-128..127</td></tr>'
                    '<tr><td>uint16_t</td><td>16 бит</td><td>0..65535</td></tr>'
                    '<tr><td>int32_t</td><td>32 бит</td><td>±2 млрд</td></tr></table>'
                    '<h3>Что избегать во встраиваемом C</h3>'
                    '<ul>'
                    '<li><strong>malloc/free</strong> — фрагментация кучи, недетерминизм. Используй статические буферы.</li>'
                    '<li><strong>Рекурсия</strong> — непредсказуемый расход стека. Заменяй итерацией.</li>'
                    '<li><strong>Форматированный printf в ISR</strong> — долго, недопустимо в обработчике прерывания.</li>'
                    '<li><strong>Плавающая точка без FPU</strong> — программная эмуляция медленна. Используй fixed-point.</li>'
                    '</ul>'
                    '<h3>Ключевые квалификаторы</h3>'
                    '<ul>'
                    '<li><code>volatile</code> — запрет оптимизации, для регистров и ISR-переменных</li>'
                    '<li><code>const</code> — данные в Flash (экономия RAM)</li>'
                    '<li><code>static</code> в функции — переменная сохраняется между вызовами</li>'
                    '<li><code>__attribute__((section(".ccmram")))</code> — разместить в быстрой CCM RAM</li>'
                    '</ul>'
                ),
                'code_example': (
                    '#include <stdint.h>\n'
                    '#include <stdbool.h>\n\n'
                    '// Константа в Flash (не занимает RAM)\n'
                    'const uint8_t sine_table[256] = {\n'
                    '    128, 131, 134, /* ... */ 128\n'
                    '};\n\n'
                    '// Fixed-point: Q8.8 (8 целых, 8 дробных бит)\n'
                    'typedef int16_t q8_8_t;\n'
                    '#define FLOAT_TO_Q88(x) ((q8_8_t)((x) * 256.0f))\n'
                    '#define Q88_TO_FLOAT(x) ((float)(x) / 256.0f)\n\n'
                    'q8_8_t q88_mul(q8_8_t a, q8_8_t b) {\n'
                    '    return (q8_8_t)(((int32_t)a * b) >> 8);\n'
                    '}\n\n'
                    '// Кольцевой буфер без malloc\n'
                    '#define UART_BUF_SIZE 64\n'
                    'typedef struct {\n'
                    '    uint8_t  buf[UART_BUF_SIZE];\n'
                    '    uint8_t  head, tail;\n'
                    '    uint8_t  count;\n'
                    '} ring_buf_t;\n\n'
                    'bool ring_push(ring_buf_t *rb, uint8_t data) {\n'
                    '    if (rb->count >= UART_BUF_SIZE) return false;\n'
                    '    rb->buf[rb->head] = data;\n'
                    '    rb->head = (rb->head + 1) % UART_BUF_SIZE;\n'
                    '    rb->count++;\n'
                    '    return true;\n'
                    '}'
                ),
            },
        ],
        'quiz': {
            'title': 'Тест: Введение в встраиваемые системы',
            'pass_score': 70,
            'questions': [
                {
                    'text': 'Что означает ключевое слово volatile при работе с регистрами периферии МК?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'volatile запрещает компилятору кэшировать значение переменной — '
                                   'при каждом обращении происходит реальное чтение/запись памяти.',
                    'choices': [
                        ('Переменная не может быть изменена программой', False),
                        ('Компилятор не будет кэшировать значение и всегда обращается к памяти', True),
                        ('Переменная хранится в быстрой SRAM', False),
                        ('Переменная не инициализируется при старте', False),
                    ],
                },
                {
                    'text': 'Какой тип следует использовать для 8-битной беззнаковой переменной во встраиваемом C?',
                    'q_type': 'single',
                    'difficulty': 1,
                    'explanation': 'uint8_t из stdint.h гарантирует точно 8 бит на любой архитектуре. '
                                   'unsigned char тоже обычно 8 бит, но это не гарантировано стандартом.',
                    'choices': [
                        ('unsigned char', False),
                        ('uint8_t', True),
                        ('short', False),
                        ('byte', False),
                    ],
                },
                {
                    'text': 'Какие операции НЕ рекомендуется использовать в прерываниях (ISR)?',
                    'q_type': 'multiple',
                    'difficulty': 2,
                    'explanation': 'В ISR нельзя вызывать долгие операции: printf (медленно), '
                                   'malloc (не реентерабелен), HAL_Delay (использует SysTick).',
                    'choices': [
                        ('printf("debug")', True),
                        ('Установить флаг volatile-переменной', False),
                        ('malloc()', True),
                        ('Инкрементировать счётчик', False),
                    ],
                },
                {
                    'text': 'Что происходит с секцией .data при старте программы на МК?',
                    'q_type': 'single',
                    'difficulty': 3,
                    'explanation': '.data содержит инициализированные глобальные переменные. '
                                   'Их начальные значения хранятся во Flash, а startup-код копирует их в RAM.',
                    'choices': [
                        ('Автоматически обнуляется', False),
                        ('Остаётся во Flash и не трогается', False),
                        ('Копируется из Flash в RAM startup-кодом', True),
                        ('Выделяется динамически', False),
                    ],
                },
                {
                    'text': 'Какой интерфейс отладки не останавливает выполнение CPU при выводе данных?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'Segger RTT (Real-Time Transfer) использует буфер в RAM, '
                                   'отладчик читает его в фоне, не прерывая выполнение программы.',
                    'choices': [
                        ('UART printf', False),
                        ('Semihosting', False),
                        ('Segger RTT', True),
                        ('LED мигание', False),
                    ],
                },
            ],
        },
    },
    {
        'title': 'Прерывания и таймеры',
        'icon': 'fas fa-bolt',
        'order': 2,
        'description': 'NVIC, обработчики прерываний, таймеры, ШИМ, SysTick',
        'lessons': [
            {
                'title': 'NVIC и приоритеты прерываний',
                'order': 1,
                'estimated_minutes': 20,
                'content': (
                    '<h3>NVIC — Nested Vectored Interrupt Controller</h3>'
                    '<p>Контроллер прерываний ARM Cortex-M. Поддерживает до 240 внешних прерываний, '
                    'вложенные прерывания, аппаратное сохранение/восстановление контекста.</p>'
                    '<h3>Приоритеты</h3>'
                    '<p>Меньшее число = более высокий приоритет. На STM32F4: 4 бита приоритета (0-15). '
                    'Делятся на группы и подгруппы (PRIGROUP в SCB->AIRCR).</p>'
                    '<table><tr><th>Прерывание</th><th>Приоритет</th><th>Назначение</th></tr>'
                    '<tr><td>SysTick</td><td>0 (высший)</td><td>Системный тик HAL</td></tr>'
                    '<tr><td>UART RX</td><td>5</td><td>Приём данных</td></tr>'
                    '<tr><td>TIM3</td><td>10</td><td>ШИМ обновление</td></tr></table>'
                    '<h3>Аппаратное сохранение контекста</h3>'
                    '<p>При входе в ISR Cortex-M автоматически сохраняет на стек: R0-R3, R12, LR, PC, xPSR. '
                    'Это занимает 8 тактов. Восстанавливает при выходе. R4-R11 — ответственность ISR.</p>'
                    '<h3>Важные правила ISR</h3>'
                    '<ul>'
                    '<li>ISR должен выполняться быстро — не задерживать систему</li>'
                    '<li>Данные в ISR → main через volatile-переменные или очереди</li>'
                    '<li>Нельзя блокировать (HAL_Delay, ожидание флага)</li>'
                    '<li>FreeRTOS API: только функции с суффиксом FromISR</li>'
                    '</ul>'
                ),
                'code_example': (
                    '// Настройка UART RX прерывания (HAL)\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'UART_HandleTypeDef huart2;\n'
                    'volatile uint8_t rx_byte;\n'
                    'volatile bool data_ready = false;\n\n'
                    'void uart_init(void) {\n'
                    '    huart2.Instance = USART2;\n'
                    '    huart2.Init.BaudRate = 115200;\n'
                    '    huart2.Init.WordLength = UART_WORDLENGTH_8B;\n'
                    '    huart2.Init.StopBits = UART_STOPBITS_1;\n'
                    '    huart2.Init.Parity = UART_PARITY_NONE;\n'
                    '    HAL_UART_Init(&huart2);\n\n'
                    '    // Установить приоритет и включить\n'
                    '    HAL_NVIC_SetPriority(USART2_IRQn, 5, 0);\n'
                    '    HAL_NVIC_EnableIRQ(USART2_IRQn);\n\n'
                    '    // Запустить приём первого байта\n'
                    '    HAL_UART_Receive_IT(&huart2, (uint8_t*)&rx_byte, 1);\n'
                    '}\n\n'
                    '// Колбэк вызывается HAL после получения байта\n'
                    'void HAL_UART_RxCpltCallback(UART_HandleTypeDef *h) {\n'
                    '    if (h->Instance == USART2) {\n'
                    '        data_ready = true;\n'
                    '        // Запустить следующий приём\n'
                    '        HAL_UART_Receive_IT(&huart2,\n'
                    '                            (uint8_t*)&rx_byte, 1);\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'Таймеры: базовые режимы',
                'order': 2,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Таймеры STM32</h3>'
                    '<p>STM32F4 имеет 14 таймеров разных типов:</p>'
                    '<ul>'
                    '<li><strong>TIM1, TIM8</strong> — продвинутые (Advanced), ШИМ с мёртвым временем</li>'
                    '<li><strong>TIM2-TIM5</strong> — общего назначения, 32-бит</li>'
                    '<li><strong>TIM9-TIM14</strong> — простые, 16-бит</li>'
                    '<li><strong>TIM6, TIM7</strong> — базовые (только счёт)</li>'
                    '</ul>'
                    '<h3>Формула частоты</h3>'
                    '<p><code>f_timer = f_APB / ((PSC + 1) * (ARR + 1))</code></p>'
                    '<p>PSC = предделитель, ARR = период (Auto-Reload Register)</p>'
                    '<h3>Пример расчёта</h3>'
                    '<p>Нужен таймер 1 кГц при APB1 = 84 МГц:<br>'
                    'PSC = 8400 - 1 = 8399, ARR = 10 - 1 = 9<br>'
                    'f = 84 000 000 / (8400 * 10) = 1000 Гц ✓</p>'
                    '<h3>Режимы работы</h3>'
                    '<table><tr><th>Режим</th><th>Применение</th></tr>'
                    '<tr><td>Upcounting</td><td>Периодические прерывания</td></tr>'
                    '<tr><td>PWM Mode 1/2</td><td>Управление яркостью, моторами</td></tr>'
                    '<tr><td>Input Capture</td><td>Измерение частоты/периода</td></tr>'
                    '<tr><td>Output Compare</td><td>Генерация точных задержек</td></tr>'
                    '<tr><td>Encoder</td><td>Квадратурный энкодер</td></tr></table>'
                ),
                'code_example': (
                    '// TIM3 - периодическое прерывание 1 кГц\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'TIM_HandleTypeDef htim3;\n'
                    'volatile uint32_t ms_tick = 0;\n\n'
                    'void TIM3_init(void) {\n'
                    '    __HAL_RCC_TIM3_CLK_ENABLE();\n\n'
                    '    htim3.Instance = TIM3;\n'
                    '    htim3.Init.Prescaler = 8400 - 1;   // 84MHz/8400 = 10kHz\n'
                    '    htim3.Init.Period = 10 - 1;         // 10kHz/10 = 1kHz\n'
                    '    htim3.Init.ClockDivision = 0;\n'
                    '    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;\n'
                    '    HAL_TIM_Base_Init(&htim3);\n\n'
                    '    HAL_NVIC_SetPriority(TIM3_IRQn, 8, 0);\n'
                    '    HAL_NVIC_EnableIRQ(TIM3_IRQn);\n'
                    '    HAL_TIM_Base_Start_IT(&htim3);\n'
                    '}\n\n'
                    'void TIM3_IRQHandler(void) {\n'
                    '    HAL_TIM_IRQHandler(&htim3);\n'
                    '}\n\n'
                    'void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *h) {\n'
                    '    if (h->Instance == TIM3)\n'
                    '        ms_tick++;\n'
                    '}'
                ),
            },
            {
                'title': 'ШИМ (PWM) на таймерах',
                'order': 3,
                'estimated_minutes': 20,
                'content': (
                    '<h3>ШИМ — Широтно-Импульсная Модуляция</h3>'
                    '<p>PWM — сигнал с постоянной частотой и переменным скважностью (duty cycle). '
                    'Скважность 0..100% задаёт среднее напряжение: 50% duty при 3.3 В = 1.65 В среднее.</p>'
                    '<h3>Режим PWM Mode 1</h3>'
                    '<p>Таймер считает от 0 до ARR. Пока счётчик &lt; CCR — вывод HIGH. '
                    'Пока счётчик &gt;= CCR — LOW. CCR/ARR = duty cycle.</p>'
                    '<h3>Применение ШИМ</h3>'
                    '<ul>'
                    '<li>Управление яркостью светодиодов (LED dimmer)</li>'
                    '<li>Управление скоростью мотора постоянного тока</li>'
                    '<li>Серводвигатели (20 мс период, 1-2 мс импульс)</li>'
                    '<li>Цифро-аналоговое преобразование (ШИМ + RC-фильтр)</li>'
                    '<li>Аудио (1-битный ЦАП)</li>'
                    '</ul>'
                    '<h3>Сервопривод</h3>'
                    '<p>Стандартный серво: период 20 мс (50 Гц).<br>'
                    '1 мс = -90°, 1.5 мс = 0°, 2 мс = +90°.<br>'
                    'При ARR=19999 (20 мс): CCR от 1000 до 2000.</p>'
                ),
                'code_example': (
                    '// ШИМ на TIM2 CH1 (PA0) - управление яркостью LED\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'TIM_HandleTypeDef htim2;\n'
                    'TIM_OC_InitTypeDef sConfig;\n\n'
                    'void PWM_init(void) {\n'
                    '    __HAL_RCC_TIM2_CLK_ENABLE();\n'
                    '    // PA0 -> AF1 (TIM2_CH1)\n'
                    '    GPIO_InitTypeDef gpio = {0};\n'
                    '    __HAL_RCC_GPIOA_CLK_ENABLE();\n'
                    '    gpio.Pin = GPIO_PIN_0;\n'
                    '    gpio.Mode = GPIO_MODE_AF_PP;\n'
                    '    gpio.Alternate = GPIO_AF1_TIM2;\n'
                    '    HAL_GPIO_Init(GPIOA, &gpio);\n\n'
                    '    htim2.Instance = TIM2;\n'
                    '    htim2.Init.Prescaler = 84 - 1;   // 84MHz/84 = 1MHz\n'
                    '    htim2.Init.Period = 1000 - 1;     // 1MHz/1000 = 1kHz PWM\n'
                    '    HAL_TIM_PWM_Init(&htim2);\n\n'
                    '    sConfig.OCMode = TIM_OCMODE_PWM1;\n'
                    '    sConfig.Pulse = 500;  // 50% duty\n'
                    '    HAL_TIM_PWM_ConfigChannel(&htim2, &sConfig, TIM_CHANNEL_1);\n'
                    '    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);\n'
                    '}\n\n'
                    'void set_brightness(uint8_t percent) {\n'
                    '    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1,\n'
                    '                          (uint32_t)percent * 10);\n'
                    '}'
                ),
            },
            {
                'title': 'SysTick и системное время',
                'order': 4,
                'estimated_minutes': 15,
                'content': (
                    '<h3>SysTick</h3>'
                    '<p>SysTick — системный таймер Cortex-M. Автоматически настраивается HAL '
                    'для генерации прерывания каждую миллисекунду. Основа HAL_Delay() и HAL_GetTick().</p>'
                    '<h3>HAL_GetTick() vs TIM</h3>'
                    '<p>HAL_GetTick() возвращает миллисекунды с момента старта. '
                    'Достаточно для большинства задержек. Для микросекундной точности — отдельный таймер.</p>'
                    '<h3>Неблокирующие задержки</h3>'
                    '<p>HAL_Delay() блокирует CPU и прерывания с меньшим приоритетом. '
                    'Правильный подход — запомнить время начала и проверять elapsed time.</p>'
                    '<h3>Переполнение счётчика</h3>'
                    '<p>HAL_GetTick() переполняется через 49.7 дней (uint32_t, мс). '
                    'Для вычисления прошедшего времени используй: '
                    '<code>elapsed = now - start</code> (работает корректно при переполнении '
                    'благодаря беззнаковой арифметике).</p>'
                ),
                'code_example': (
                    '// Неблокирующие задержки\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'typedef struct {\n'
                    '    uint32_t start;\n'
                    '    uint32_t period_ms;\n'
                    '} timer_t;\n\n'
                    'void timer_start(timer_t *t, uint32_t period_ms) {\n'
                    '    t->start = HAL_GetTick();\n'
                    '    t->period_ms = period_ms;\n'
                    '}\n\n'
                    'bool timer_expired(timer_t *t) {\n'
                    '    return (HAL_GetTick() - t->start) >= t->period_ms;\n'
                    '}\n\n'
                    '// Пример: мигать LED без блокировки\n'
                    'int main(void) {\n'
                    '    HAL_Init();\n'
                    '    // ... инициализация ...\n\n'
                    '    timer_t led_timer, uart_timer;\n'
                    '    timer_start(&led_timer, 500);\n'
                    '    timer_start(&uart_timer, 1000);\n\n'
                    '    while (1) {\n'
                    '        if (timer_expired(&led_timer)) {\n'
                    '            timer_start(&led_timer, 500);\n'
                    '            HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);\n'
                    '        }\n'
                    '        if (timer_expired(&uart_timer)) {\n'
                    '            timer_start(&uart_timer, 1000);\n'
                    '            printf("Tick %lu\\n", HAL_GetTick());\n'
                    '        }\n'
                    '        // Другие задачи...\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'DMA: передача данных без CPU',
                'order': 5,
                'estimated_minutes': 20,
                'content': (
                    '<h3>DMA — Direct Memory Access</h3>'
                    '<p>DMA-контроллер передаёт данные между памятью и периферией '
                    'без участия CPU. CPU свободен для других задач.</p>'
                    '<h3>Режимы DMA</h3>'
                    '<ul>'
                    '<li><strong>Периферия → Память</strong>: UART RX, ADC, SPI RX</li>'
                    '<li><strong>Память → Периферия</strong>: UART TX, SPI TX, DAC</li>'
                    '<li><strong>Память → Память</strong>: memcpy через DMA</li>'
                    '</ul>'
                    '<h3>Режимы передачи</h3>'
                    '<table><tr><th>Режим</th><th>Описание</th></tr>'
                    '<tr><td>Normal</td><td>Передача одного блока, затем остановка</td></tr>'
                    '<tr><td>Circular</td><td>Автоматический перезапуск (кольцевой буфер)</td></tr>'
                    '<tr><td>Double Buffer</td><td>Два буфера поочерёдно (ping-pong)</td></tr></table>'
                    '<h3>Когда использовать DMA</h3>'
                    '<ul>'
                    '<li>Передача больших блоков данных (SPI дисплей, SD-карта)</li>'
                    '<li>Непрерывный АЦП (аудио, осциллограф)</li>'
                    '<li>UART: приём потока данных без потерь</li>'
                    '</ul>'
                    '<p>Без DMA при 1 Мбит/с UART и 168 МГц CPU тратится ~168 тактов на байт = 16% загрузки CPU.</p>'
                ),
                'code_example': (
                    '// UART TX через DMA\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'UART_HandleTypeDef huart2;\n'
                    'DMA_HandleTypeDef hdma_usart2_tx;\n\n'
                    'void DMA_UART_init(void) {\n'
                    '    __HAL_RCC_DMA1_CLK_ENABLE();\n\n'
                    '    // DMA1 Stream6 Channel4 = USART2 TX\n'
                    '    hdma_usart2_tx.Instance = DMA1_Stream6;\n'
                    '    hdma_usart2_tx.Init.Channel = DMA_CHANNEL_4;\n'
                    '    hdma_usart2_tx.Init.Direction = DMA_MEMORY_TO_PERIPH;\n'
                    '    hdma_usart2_tx.Init.PeriphInc = DMA_PINC_DISABLE;\n'
                    '    hdma_usart2_tx.Init.MemInc = DMA_MINC_ENABLE;\n'
                    '    hdma_usart2_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;\n'
                    '    hdma_usart2_tx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;\n'
                    '    hdma_usart2_tx.Init.Mode = DMA_NORMAL;\n'
                    '    hdma_usart2_tx.Init.Priority = DMA_PRIORITY_LOW;\n'
                    '    HAL_DMA_Init(&hdma_usart2_tx);\n\n'
                    '    __HAL_LINKDMA(&huart2, hdmatx, hdma_usart2_tx);\n'
                    '}\n\n'
                    'const char msg[] = "Hello via DMA!\\r\\n";\n\n'
                    'void send_dma(void) {\n'
                    '    // Неблокирующая отправка\n'
                    '    HAL_UART_Transmit_DMA(&huart2, (uint8_t*)msg, sizeof(msg)-1);\n'
                    '    // CPU сразу свободен\n'
                    '}'
                ),
            },
        ],
        'quiz': {
            'title': 'Тест: Прерывания и таймеры',
            'pass_score': 70,
            'questions': [
                {
                    'text': 'В ARM Cortex-M: чем меньше число приоритета прерывания, тем...',
                    'q_type': 'single',
                    'difficulty': 1,
                    'explanation': 'В NVIC Cortex-M приоритет 0 — высший (наиболее срочный). '
                                   'Прерывание с меньшим числом приоритета прервёт прерывание с большим числом.',
                    'choices': [
                        ('Ниже его приоритет', False),
                        ('Выше его приоритет', True),
                        ('Приоритет не изменяется', False),
                        ('Прерывание отключается', False),
                    ],
                },
                {
                    'text': 'Для управления серводвигателем используется ШИМ с периодом 20 мс. Какой duty cycle соответствует нейтральному положению (0°)?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'Стандартный сервопривод: 1 мс = -90°, 1.5 мс = 0° (нейтраль), 2 мс = +90°. '
                                   'При периоде 20 мс: 1.5 мс / 20 мс = 7.5%.',
                    'choices': [
                        ('5% (1 мс из 20 мс)', False),
                        ('7.5% (1.5 мс из 20 мс)', True),
                        ('10% (2 мс из 20 мс)', False),
                        ('50% (10 мс из 20 мс)', False),
                    ],
                },
                {
                    'text': 'Какие данные ARM Cortex-M автоматически сохраняет на стек при входе в ISR?',
                    'q_type': 'single',
                    'difficulty': 3,
                    'explanation': 'Cortex-M автоматически stash: R0-R3, R12, LR (R14), PC (R15), xPSR. '
                                   'Регистры R4-R11 программист сохраняет сам при необходимости.',
                    'choices': [
                        ('Все регистры R0-R15', False),
                        ('R0-R3, R12, LR, PC, xPSR', True),
                        ('Только PC и SP', False),
                        ('R4-R11 (callee-saved)', False),
                    ],
                },
                {
                    'text': 'DMA в режиме Circular используется для...',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'Circular DMA автоматически перезапускает передачу по достижении конца буфера, '
                                   'возвращаясь в начало. Идеально для непрерывных потоков: АЦП, аудио.',
                    'choices': [
                        ('Однократной передачи блока данных', False),
                        ('Непрерывного потока данных с автоматическим перезапуском', True),
                        ('Передачи данных между двумя МК', False),
                        ('Шифрования данных при передаче', False),
                    ],
                },
                {
                    'text': 'Формула частоты таймера: f = f_APB / ((PSC+1) * (ARR+1)). При f_APB=84 МГц, PSC=83, ARR=999, чему равна f?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'f = 84000000 / (84 * 1000) = 1000 Гц = 1 кГц.',
                    'choices': [
                        ('100 Гц', False),
                        ('1 кГц', True),
                        ('10 кГц', False),
                        ('84 кГц', False),
                    ],
                },
            ],
        },
    },
    {
        'title': 'Интерфейсы и протоколы связи',
        'icon': 'fas fa-exchange-alt',
        'order': 3,
        'description': 'UART, SPI, I2C, USB — настройка и использование в HAL',
        'lessons': [
            {
                'title': 'UART: настройка и работа через HAL',
                'order': 1,
                'estimated_minutes': 20,
                'content': (
                    '<h3>UART в STM32 HAL</h3>'
                    '<p>USART/UART — универсальный асинхронный приёмопередатчик. '
                    'Наиболее простой протокол для отладки и связи с ПК/модулями.</p>'
                    '<h3>Параметры инициализации</h3>'
                    '<table><tr><th>Параметр</th><th>Типичные значения</th></tr>'
                    '<tr><td>BaudRate</td><td>9600, 115200, 921600</td></tr>'
                    '<tr><td>WordLength</td><td>8 бит</td></tr>'
                    '<tr><td>StopBits</td><td>1</td></tr>'
                    '<tr><td>Parity</td><td>None</td></tr>'
                    '<tr><td>HwFlowCtl</td><td>None (без аппаратного управления потоком)</td></tr></table>'
                    '<h3>Режимы работы HAL</h3>'
                    '<ul>'
                    '<li><strong>Polling</strong>: HAL_UART_Transmit() — блокирует до завершения</li>'
                    '<li><strong>Interrupt</strong>: HAL_UART_Transmit_IT() — неблокирующий, колбэк</li>'
                    '<li><strong>DMA</strong>: HAL_UART_Transmit_DMA() — максимальная эффективность</li>'
                    '</ul>'
                    '<h3>Приём строки неизвестной длины</h3>'
                    '<p>Проблема: HAL_UART_Receive_IT() ждёт фиксированное число байт. '
                    'Решения: UART Idle Line Detection (прерывание по паузе), '
                    'или DMA Circular с анализом изменений буфера.</p>'
                ),
                'code_example': (
                    '// UART с приёмом по прерыванию + кольцевой буфер\n'
                    '#include "stm32f4xx_hal.h"\n'
                    '#include <string.h>\n'
                    '#include <stdio.h>\n\n'
                    '#define RX_BUF_SIZE 256\n'
                    'uint8_t rx_buf[RX_BUF_SIZE];\n'
                    'uint8_t rx_head = 0, rx_tail = 0;\n\n'
                    '// Вызывается HAL при получении каждого байта\n'
                    'void HAL_UART_RxCpltCallback(UART_HandleTypeDef *h) {\n'
                    '    if (h->Instance == USART2) {\n'
                    '        rx_head = (rx_head + 1) % RX_BUF_SIZE;\n'
                    '        // Перезапустить приём следующего байта\n'
                    '        HAL_UART_Receive_IT(&huart2,\n'
                    '            &rx_buf[rx_head], 1);\n'
                    '    }\n'
                    '}\n\n'
                    'uint8_t uart_read_byte(void) {\n'
                    '    while (rx_tail == rx_head);  // Ждать байт\n'
                    '    rx_tail = (rx_tail + 1) % RX_BUF_SIZE;\n'
                    '    return rx_buf[rx_tail];\n'
                    '}\n\n'
                    'void uart_send_str(const char *s) {\n'
                    '    HAL_UART_Transmit(&huart2,\n'
                    '        (uint8_t*)s, strlen(s), 100);\n'
                    '}'
                ),
            },
            {
                'title': 'SPI: быстрая синхронная передача',
                'order': 2,
                'estimated_minutes': 20,
                'content': (
                    '<h3>SPI — Serial Peripheral Interface</h3>'
                    '<p>Синхронный полнодуплексный протокол. 4 провода: SCK, MOSI, MISO, CS(NSS). '
                    'Скорость: до нескольких десятков МГц.</p>'
                    '<h3>4 режима SPI (CPOL/CPHA)</h3>'
                    '<table><tr><th>Режим</th><th>CPOL</th><th>CPHA</th><th>Применение</th></tr>'
                    '<tr><td>0</td><td>0</td><td>0</td><td>SD-карта, большинство датчиков</td></tr>'
                    '<tr><td>1</td><td>0</td><td>1</td><td>Редко</td></tr>'
                    '<tr><td>2</td><td>1</td><td>0</td><td>Редко</td></tr>'
                    '<tr><td>3</td><td>1</td><td>1</td><td>MAX31855, некоторые АЦП</td></tr></table>'
                    '<ul>'
                    '<li><strong>CPOL</strong> — полярность тактового сигнала в покое</li>'
                    '<li><strong>CPHA</strong> — фаза захвата данных (0 = по первому фронту)</li>'
                    '</ul>'
                    '<h3>Несколько устройств</h3>'
                    '<p>Общие линии SCK, MOSI, MISO. Каждое устройство — свой CS. '
                    'Перед транзакцией опустить CS выбранного устройства, после — поднять.</p>'
                ),
                'code_example': (
                    '// SPI чтение MAX31855 (термопара, режим 0)\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'SPI_HandleTypeDef hspi1;\n\n'
                    '#define CS_LOW()  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_6, GPIO_PIN_RESET)\n'
                    '#define CS_HIGH() HAL_GPIO_WritePin(GPIOB, GPIO_PIN_6, GPIO_PIN_SET)\n\n'
                    'float read_thermocouple(void) {\n'
                    '    uint8_t data[4];\n'
                    '    CS_LOW();\n'
                    '    HAL_SPI_Receive(&hspi1, data, 4, 10);\n'
                    '    CS_HIGH();\n\n'
                    '    // Биты 31:18 — температура термопары, Q11.2\n'
                    '    uint32_t raw = (data[0] << 24) | (data[1] << 16)\n'
                    '                | (data[2] << 8)  |  data[3];\n\n'
                    '    if (raw & (1 << 16)) {  // fault bit\n'
                    '        return -999.0f;\n'
                    '    }\n\n'
                    '    int16_t temp_raw = (raw >> 18) & 0x3FFF;\n'
                    '    if (temp_raw & 0x2000)  // знаковое расширение 14-бит\n'
                    '        temp_raw |= 0xC000;\n\n'
                    '    return temp_raw * 0.25f;\n'
                    '}'
                ),
            },
            {
                'title': 'I2C: адресная шина датчиков',
                'order': 3,
                'estimated_minutes': 20,
                'content': (
                    '<h3>I2C в встраиваемых системах</h3>'
                    '<p>I2C — 2-проводной протокол (SDA + SCL). До 127 устройств на одной шине. '
                    'Скорости: Standard 100 кГц, Fast 400 кГц, Fast-Plus 1 МГц.</p>'
                    '<h3>Транзакция I2C</h3>'
                    '<ol>'
                    '<li>START условие (SDA LOW при SCL HIGH)</li>'
                    '<li>Адрес устройства (7 бит) + бит R/W</li>'
                    '<li>ACK от устройства</li>'
                    '<li>Данные (каждый байт + ACK)</li>'
                    '<li>STOP условие</li>'
                    '</ol>'
                    '<h3>HAL I2C функции</h3>'
                    '<table><tr><th>Функция</th><th>Назначение</th></tr>'
                    '<tr><td>HAL_I2C_Master_Transmit</td><td>Отправить блок данных ведомому</td></tr>'
                    '<tr><td>HAL_I2C_Master_Receive</td><td>Принять блок данных от ведомого</td></tr>'
                    '<tr><td>HAL_I2C_Mem_Write</td><td>Записать регистр (адрес + данные)</td></tr>'
                    '<tr><td>HAL_I2C_Mem_Read</td><td>Прочитать регистр</td></tr></table>'
                    '<h3>Типичные проблемы</h3>'
                    '<ul>'
                    '<li>Неправильный адрес (7-бит vs 8-бит со сдвигом)</li>'
                    '<li>Забыли подтяжку (4.7 кОм на SDA и SCL к VCC)</li>'
                    '<li>Слишком длинная шина или высокая ёмкость кабеля</li>'
                    '<li>Устройство не ответило: шина зависла — нужен reset I2C</li>'
                    '</ul>'
                ),
                'code_example': (
                    '// Работа с BME280 по I2C через HAL\n'
                    '#include "stm32f4xx_hal.h"\n\n'
                    'I2C_HandleTypeDef hi2c1;\n\n'
                    '// BME280 адрес: 0x76 (SDO=GND) или 0x77 (SDO=VCC)\n'
                    '// HAL требует адрес сдвинутый влево на 1 бит!\n'
                    '#define BME280_ADDR (0x76 << 1)\n\n'
                    '// Регистры BME280\n'
                    '#define REG_CHIP_ID   0xD0\n'
                    '#define REG_CTRL_MEAS 0xF4\n'
                    '#define REG_TEMP_MSB  0xFA\n\n'
                    'uint8_t bme280_read_reg(uint8_t reg) {\n'
                    '    uint8_t val;\n'
                    '    HAL_I2C_Mem_Read(&hi2c1, BME280_ADDR,\n'
                    '                     reg, 1, &val, 1, 10);\n'
                    '    return val;\n'
                    '}\n\n'
                    'void bme280_write_reg(uint8_t reg, uint8_t val) {\n'
                    '    HAL_I2C_Mem_Write(&hi2c1, BME280_ADDR,\n'
                    '                      reg, 1, &val, 1, 10);\n'
                    '}\n\n'
                    'void bme280_init(void) {\n'
                    '    uint8_t id = bme280_read_reg(REG_CHIP_ID);\n'
                    '    if (id != 0x60) { /* Ошибка! */ return; }\n'
                    '    // Forced mode, oversample x1\n'
                    '    bme280_write_reg(REG_CTRL_MEAS, 0x25);\n'
                    '}'
                ),
            },
            {
                'title': 'USB и виртуальный COM-порт',
                'order': 4,
                'estimated_minutes': 20,
                'content': (
                    '<h3>USB CDC — виртуальный COM-порт</h3>'
                    '<p>USB CDC (Communication Device Class) позволяет МК выглядеть как COM-порт для ПК. '
                    'Не нужен конвертер USB-UART. STM32 с USB FS поддерживает это из коробки.</p>'
                    '<h3>STM32 USB стек (STM32CubeIDE)</h3>'
                    '<p>Генерируется STM32CubeMX. Файлы: usbd_cdc_if.c — пользовательский интерфейс. '
                    'Функции: CDC_Transmit_FS() для отправки, CDC_Receive_FS callback для приёма.</p>'
                    '<h3>Особенности USB CDC</h3>'
                    '<ul>'
                    '<li>Скорость до 12 Мбит/с (USB FS) — намного быстрее UART</li>'
                    '<li>Буферизация: данные отправляются пакетами до 64 байт</li>'
                    '<li>Нет гарантии доставки без подтверждения от хоста</li>'
                    '<li>CDC_Transmit_FS() возвращает USBD_BUSY если предыдущий пакет не отправлен</li>'
                    '</ul>'
                    '<h3>Альтернативы</h3>'
                    '<ul>'
                    '<li><strong>HID</strong> — клавиатура, мышь, геймпад</li>'
                    '<li><strong>MSC</strong> — флеш-накопитель (USB Mass Storage)</li>'
                    '<li><strong>Bulk</strong> — произвольный протокол (нужен драйвер на ПК)</li>'
                    '</ul>'
                ),
                'code_example': (
                    '// USB CDC отправка и приём (STM32CubeIDE)\n'
                    '#include "usbd_cdc_if.h"\n'
                    '#include <stdio.h>\n'
                    '#include <string.h>\n\n'
                    '// Глобальный флаг получения данных\n'
                    'volatile uint8_t usb_rx_buf[64];\n'
                    'volatile uint16_t usb_rx_len = 0;\n'
                    'volatile bool usb_data_ready = false;\n\n'
                    '// Переопределить в usbd_cdc_if.c:\n'
                    'static int8_t CDC_Receive_FS(uint8_t *buf, uint32_t *len) {\n'
                    '    if (*len < sizeof(usb_rx_buf)) {\n'
                    '        memcpy((void*)usb_rx_buf, buf, *len);\n'
                    '        usb_rx_len = *len;\n'
                    '        usb_data_ready = true;\n'
                    '    }\n'
                    '    USBD_CDC_SetRxBuffer(&hUsbDeviceFS, buf);\n'
                    '    USBD_CDC_ReceivePacket(&hUsbDeviceFS);\n'
                    '    return USBD_OK;\n'
                    '}\n\n'
                    'void usb_printf(const char *fmt, ...) {\n'
                    '    char buf[128];\n'
                    '    va_list args;\n'
                    '    va_start(args, fmt);\n'
                    '    int len = vsnprintf(buf, sizeof(buf), fmt, args);\n'
                    '    va_end(args);\n'
                    '    // Ждать, пока предыдущий пакет отправлен\n'
                    '    uint32_t t = HAL_GetTick();\n'
                    '    while (CDC_Transmit_FS((uint8_t*)buf, len) == USBD_BUSY) {\n'
                    '        if (HAL_GetTick() - t > 10) break;\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'Протоколы прикладного уровня',
                'order': 5,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Прикладные протоколы для МК</h3>'
                    '<p>Поверх физических протоколов (UART, SPI, I2C) строят прикладные протоколы '
                    'для структурированной передачи команд и данных.</p>'
                    '<h3>Простой бинарный протокол</h3>'
                    '<p>Структура пакета: [STX][LEN][CMD][DATA...][CRC][ETX]<br>'
                    'STX/ETX — маркеры начала/конца, LEN — длина данных, CRC — контрольная сумма.</p>'
                    '<h3>Modbus RTU</h3>'
                    '<p>Промышленный стандарт поверх RS-485/UART. Ведущий-ведомый. '
                    'Команды: чтение/запись регистров. Широко применяется в ПЛК и датчиках.</p>'
                    '<h3>Контрольные суммы</h3>'
                    '<table><tr><th>Алгоритм</th><th>Размер</th><th>Применение</th></tr>'
                    '<tr><td>Сумма байт</td><td>8/16 бит</td><td>Простые протоколы</td></tr>'
                    '<tr><td>CRC-8</td><td>8 бит</td><td>1-Wire, SMBus</td></tr>'
                    '<tr><td>CRC-16</td><td>16 бит</td><td>Modbus, UART</td></tr>'
                    '<tr><td>CRC-32</td><td>32 бита</td><td>Ethernet, ZIP, Flash</td></tr></table>'
                ),
                'code_example': (
                    '// Простой command-response протокол по UART\n'
                    '#include <stdint.h>\n'
                    '#include <stdbool.h>\n\n'
                    '#define CMD_GET_TEMP   0x01\n'
                    '#define CMD_SET_PWM    0x02\n'
                    '#define CMD_GET_STATUS 0x03\n\n'
                    'typedef struct __attribute__((packed)) {\n'
                    '    uint8_t stx;      // 0xAA\n'
                    '    uint8_t cmd;\n'
                    '    uint8_t len;\n'
                    '    uint8_t data[8];\n'
                    '    uint8_t crc;\n'
                    '} packet_t;\n\n'
                    'uint8_t calc_crc(uint8_t *data, uint8_t len) {\n'
                    '    uint8_t crc = 0;\n'
                    '    for (uint8_t i = 0; i < len; i++)\n'
                    '        crc ^= data[i];\n'
                    '    return crc;\n'
                    '}\n\n'
                    'void process_packet(packet_t *p) {\n'
                    '    if (p->stx != 0xAA) return;\n'
                    '    uint8_t crc = calc_crc(&p->cmd, p->len + 2);\n'
                    '    if (crc != p->crc) return;  // Bad CRC\n\n'
                    '    switch (p->cmd) {\n'
                    '        case CMD_GET_TEMP: {\n'
                    '            float t = read_temperature();\n'
                    '            send_response(CMD_GET_TEMP,\n'
                    '                          (uint8_t*)&t, 4);\n'
                    '            break;\n'
                    '        }\n'
                    '        case CMD_SET_PWM:\n'
                    '            set_pwm_duty(p->data[0]);\n'
                    '            break;\n'
                    '    }\n'
                    '}'
                ),
            },
        ],
        'quiz': {
            'title': 'Тест: Интерфейсы связи',
            'pass_score': 70,
            'questions': [
                {
                    'text': 'Какой физический уровень использует I2C?',
                    'q_type': 'single',
                    'difficulty': 1,
                    'explanation': 'I2C использует 2 провода: SDA (данные) и SCL (тактирование). '
                                   'Оба провода с подтяжкой к питанию через резисторы.',
                    'choices': [
                        ('4 провода: SCK, MOSI, MISO, CS', False),
                        ('2 провода: SDA, SCL', True),
                        ('1 провод + земля', False),
                        ('2 дифференциальные пары', False),
                    ],
                },
                {
                    'text': 'HAL_I2C_Mem_Read принимает адрес устройства. Как передать адрес 0x76?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'HAL использует 8-битный формат адреса (7-битный адрес + бит R/W). '
                                   'Нужно сдвинуть адрес влево: 0x76 << 1 = 0xEC.',
                    'choices': [
                        ('0x76', False),
                        ('0x76 << 1 (= 0xEC)', True),
                        ('0x76 | 1', False),
                        ('0x76 >> 1', False),
                    ],
                },
                {
                    'text': 'Что такое CPOL и CPHA в SPI?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'CPOL (Clock Polarity) — уровень тактового сигнала в покое (0=LOW, 1=HIGH). '
                                   'CPHA (Clock Phase) — по какому фронту захватываются данные.',
                    'choices': [
                        ('Скорость и количество стоп-бит', False),
                        ('Полярность тактового сигнала и фаза захвата данных', True),
                        ('Число бит данных и чётность', False),
                        ('Направление передачи и тип CS', False),
                    ],
                },
                {
                    'text': 'USB CDC (виртуальный COM-порт) на STM32 работает со скоростью до:',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'USB Full Speed (FS) — стандарт для большинства STM32 — обеспечивает до 12 Мбит/с. '
                                   'USB High Speed (HS) — 480 Мбит/с, требует внешний PHY.',
                    'choices': [
                        ('115200 бит/с (как UART)', False),
                        ('1 Мбит/с', False),
                        ('12 Мбит/с (USB FS)', True),
                        ('480 Мбит/с (USB HS)', False),
                    ],
                },
            ],
        },
    },
    {
        'title': 'RTOS: FreeRTOS',
        'icon': 'fas fa-tasks',
        'order': 4,
        'description': 'Задачи, очереди, семафоры, мьютексы в FreeRTOS',
        'lessons': [
            {
                'title': 'Введение в FreeRTOS',
                'order': 1,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Зачем RTOS?</h3>'
                    '<p>Суперцикл ломается когда задачи мешают друг другу по времени. '
                    'RTOS (Real-Time Operating System) решает это вытесняющей многозадачностью.</p>'
                    '<h3>FreeRTOS — стандарт для embedded</h3>'
                    '<p>Открытый RTOS, поддерживает ARM Cortex-M, AVR, RISC-V и десятки других архитектур. '
                    'Минимальный размер: ~5 КБ Flash, ~1 КБ RAM + стеки задач.</p>'
                    '<h3>Ключевые концепции</h3>'
                    '<ul>'
                    '<li><strong>Задача (Task)</strong> — поток выполнения со своим стеком</li>'
                    '<li><strong>Планировщик</strong> — переключает задачи по приоритету и кванту времени</li>'
                    '<li><strong>Тик</strong> — период планировщика (обычно 1 мс)</li>'
                    '<li><strong>Семафор</strong> — синхронизация, сигналы между задачами</li>'
                    '<li><strong>Очередь</strong> — обмен данными между задачами</li>'
                    '<li><strong>Мьютекс</strong> — взаимное исключение для разделяемых ресурсов</li>'
                    '</ul>'
                    '<h3>Состояния задачи</h3>'
                    '<p>Running → Blocked (ждёт семафор/очередь/время) → Ready → Running. '
                    'Suspended — принудительно остановлена. Deleted — уничтожена.</p>'
                ),
                'code_example': (
                    '#include "FreeRTOS.h"\n'
                    '#include "task.h"\n'
                    '#include "queue.h"\n\n'
                    '// Задача мигания LED\n'
                    'void vLedTask(void *params) {\n'
                    '    (void)params;\n'
                    '    while (1) {\n'
                    '        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);\n'
                    '        vTaskDelay(pdMS_TO_TICKS(500));\n'
                    '    }\n'
                    '}\n\n'
                    '// Задача вывода данных\n'
                    'void vPrintTask(void *params) {\n'
                    '    uint32_t count = 0;\n'
                    '    while (1) {\n'
                    '        printf("Tick: %lu\\n", count++);\n'
                    '        vTaskDelay(pdMS_TO_TICKS(1000));\n'
                    '    }\n'
                    '}\n\n'
                    'int main(void) {\n'
                    '    HAL_Init();\n'
                    '    // ... инициализация ...\n\n'
                    '    xTaskCreate(\n'
                    '        vLedTask,    // Функция задачи\n'
                    '        "LED",       // Имя (для отладки)\n'
                    '        128,         // Стек (слова = байты/4)\n'
                    '        NULL,        // Параметр\n'
                    '        1,           // Приоритет\n'
                    '        NULL         // Хэндл (не нужен)\n'
                    '    );\n\n'
                    '    xTaskCreate(vPrintTask, "Print", 256, NULL, 2, NULL);\n\n'
                    '    vTaskStartScheduler();  // Запустить планировщик\n'
                    '    while(1);  // Сюда не доходим\n'
                    '}'
                ),
            },
            {
                'title': 'Очереди и семафоры',
                'order': 2,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Очереди (Queue)</h3>'
                    '<p>FIFO-буфер для передачи данных между задачами. Потокобезопасен. '
                    'Задача блокируется если очередь пуста (чтение) или полна (запись).</p>'
                    '<h3>API очереди</h3>'
                    '<ul>'
                    '<li><code>xQueueCreate(len, item_size)</code> — создать очередь</li>'
                    '<li><code>xQueueSend(q, &item, ticks)</code> — отправить (ждать ticks если полна)</li>'
                    '<li><code>xQueueReceive(q, &item, ticks)</code> — получить (ждать ticks если пуста)</li>'
                    '<li><code>xQueueSendFromISR(q, &item, &woken)</code> — из ISR</li>'
                    '</ul>'
                    '<h3>Семафоры</h3>'
                    '<ul>'
                    '<li><strong>Binary semaphore</strong> — флаг 0/1. ISR сигналит, задача ждёт.</li>'
                    '<li><strong>Counting semaphore</strong> — счётчик. Несколько ресурсов.</li>'
                    '<li><strong>Mutex</strong> — для защиты разделяемых ресурсов. Владелец = та задача, что взяла.</li>'
                    '</ul>'
                    '<h3>Правило ISR</h3>'
                    '<p>Из ISR можно вызывать только функции с суффиксом <code>FromISR</code>. '
                    'После отдать управление планировщику если <code>pxHigherPriorityTaskWoken == pdTRUE</code>: '
                    '<code>portYIELD_FROM_ISR(woken)</code>.</p>'
                ),
                'code_example': (
                    '#include "FreeRTOS.h"\n'
                    '#include "task.h"\n'
                    '#include "queue.h"\n'
                    '#include "semphr.h"\n\n'
                    'typedef struct {\n'
                    '    float    temperature;\n'
                    '    float    humidity;\n'
                    '    uint32_t timestamp;\n'
                    '} sensor_data_t;\n\n'
                    'QueueHandle_t xSensorQueue;\n'
                    'SemaphoreHandle_t xUartMutex;\n\n'
                    '// Задача: читать датчик\n'
                    'void vSensorTask(void *p) {\n'
                    '    sensor_data_t data;\n'
                    '    while (1) {\n'
                    '        data.temperature = bme280_get_temp();\n'
                    '        data.humidity = bme280_get_hum();\n'
                    '        data.timestamp = HAL_GetTick();\n'
                    '        xQueueSend(xSensorQueue, &data, 0);\n'
                    '        vTaskDelay(pdMS_TO_TICKS(1000));\n'
                    '    }\n'
                    '}\n\n'
                    '// Задача: выводить данные\n'
                    'void vDisplayTask(void *p) {\n'
                    '    sensor_data_t data;\n'
                    '    while (1) {\n'
                    '        // Ждать данные бесконечно\n'
                    '        if (xQueueReceive(xSensorQueue, &data,\n'
                    '                          portMAX_DELAY) == pdTRUE) {\n'
                    '            xSemaphoreTake(xUartMutex, portMAX_DELAY);\n'
                    '            printf("T=%.1f H=%.1f\\n",\n'
                    '                   data.temperature, data.humidity);\n'
                    '            xSemaphoreGive(xUartMutex);\n'
                    '        }\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'Управление памятью в FreeRTOS',
                'order': 3,
                'estimated_minutes': 15,
                'content': (
                    '<h3>Схемы выделения памяти</h3>'
                    '<p>FreeRTOS предлагает 5 схем управления кучей (heap_1.c ... heap_5.c):</p>'
                    '<table><tr><th>Схема</th><th>Особенность</th><th>Когда использовать</th></tr>'
                    '<tr><td>heap_1</td><td>Только выделение (нет освобождения)</td><td>Статические задачи</td></tr>'
                    '<tr><td>heap_2</td><td>Освобождение без объединения</td><td>Фиксированные размеры</td></tr>'
                    '<tr><td>heap_4</td><td>Освобождение с объединением</td><td>Общий случай ✓</td></tr>'
                    '<tr><td>heap_5</td><td>Несколько регионов памяти</td><td>Фрагментированная RAM</td></tr></table>'
                    '<h3>Практические советы</h3>'
                    '<ul>'
                    '<li>Создавать все задачи/очереди до vTaskStartScheduler() → использовать heap_1</li>'
                    '<li>Для динамических задач — heap_4</li>'
                    '<li>configMINIMAL_STACK_SIZE — минимальный стек задачи idle</li>'
                    '<li>Задача стека недостаточно: симптомы — HardFault, случайный крэш</li>'
                    '<li>uxTaskGetStackHighWaterMark() — проверить свободный стек</li>'
                    '</ul>'
                    '<h3>configTOTAL_HEAP_SIZE</h3>'
                    '<p>Общий размер кучи FreeRTOS в байтах. Каждая задача берёт из неё стек. '
                    'При нехватке xTaskCreate возвращает NULL.</p>'
                ),
                'code_example': (
                    '// FreeRTOSConfig.h — ключевые настройки\n'
                    '#define configUSE_PREEMPTION         1\n'
                    '#define configUSE_IDLE_HOOK          0\n'
                    '#define configUSE_TICK_HOOK          0\n'
                    '#define configCPU_CLOCK_HZ           168000000\n'
                    '#define configTICK_RATE_HZ           1000  // 1 мс тик\n'
                    '#define configMAX_PRIORITIES         5\n'
                    '#define configMINIMAL_STACK_SIZE     128\n'
                    '#define configTOTAL_HEAP_SIZE        16384 // 16 КБ\n'
                    '#define configMAX_TASK_NAME_LEN      16\n'
                    '#define configUSE_MUTEXES            1\n'
                    '#define configUSE_COUNTING_SEMAPHORES 1\n'
                    '#define configUSE_QUEUE_SETS         0\n'
                    '#define INCLUDE_vTaskDelay           1\n'
                    '#define INCLUDE_vTaskDelete          1\n\n'
                    '// Проверка свободного стека задачи\n'
                    'void check_stacks(void) {\n'
                    '    TaskHandle_t tasks[] = {\n'
                    '        hSensorTask, hDisplayTask\n'
                    '    };\n'
                    '    for (int i = 0; i < 2; i++) {\n'
                    '        UBaseType_t free = uxTaskGetStackHighWaterMark(\n'
                    '                               tasks[i]);\n'
                    '        printf("Task %d free stack: %u words\\n",\n'
                    '               i, (unsigned)free);\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'Паттерны FreeRTOS',
                'order': 4,
                'estimated_minutes': 20,
                'content': (
                    '<h3>Типовые паттерны проектирования с FreeRTOS</h3>'
                    '<h3>1. ISR → Task через семафор</h3>'
                    '<p>ISR получает данные (быстро), даёт семафор. '
                    'Задача ждёт семафор, обрабатывает (медленно). '
                    'Это освобождает ISR от долгой обработки.</p>'
                    '<h3>2. Producer-Consumer через очередь</h3>'
                    '<p>Задача-датчик публикует данные в очередь. '
                    'Задача-дисплей читает из очереди. Независимы по скорости.</p>'
                    '<h3>3. Event Groups</h3>'
                    '<p>xEventGroupSetBits() — установить флаги событий. '
                    'xEventGroupWaitBits() — ждать комбинацию флагов. '
                    'Одно событие может разбудить несколько задач.</p>'
                    '<h3>4. Task Notification</h3>'
                    '<p>Прямая нотификация задачи (без семафора). '
                    'Быстрее семафора, только один отправитель → один получатель. '
                    'xTaskNotify() / ulTaskNotifyTake().</p>'
                    '<h3>Приоритеты и инверсия приоритетов</h3>'
                    '<p>Проблема: задача с низким приоритетом держит мьютекс, '
                    'нужный задаче с высоким. Решение: Priority Inheritance — '
                    'мьютекс FreeRTOS автоматически поднимает приоритет держателя.</p>'
                ),
                'code_example': (
                    '// Паттерн ISR -> Task через семафор\n'
                    '#include "FreeRTOS.h"\n'
                    '#include "semphr.h"\n\n'
                    'SemaphoreHandle_t xAdcSemaphore;\n'
                    'volatile uint16_t adc_value;\n\n'
                    '// ISR АЦП: быстро сохранить результат и дать семафор\n'
                    'void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *h) {\n'
                    '    BaseType_t woken = pdFALSE;\n'
                    '    adc_value = HAL_ADC_GetValue(h);\n'
                    '    xSemaphoreGiveFromISR(xAdcSemaphore, &woken);\n'
                    '    portYIELD_FROM_ISR(woken);\n'
                    '}\n\n'
                    '// Задача: ждать семафор, обработать данные\n'
                    'void vAdcTask(void *p) {\n'
                    '    xAdcSemaphore = xSemaphoreCreateBinary();\n'
                    '    // Запустить первое преобразование\n'
                    '    HAL_ADC_Start_IT(&hadc1);\n\n'
                    '    while (1) {\n'
                    '        // Блокируемся до готовности АЦП\n'
                    '        if (xSemaphoreTake(xAdcSemaphore,\n'
                    '                           pdMS_TO_TICKS(100))) {\n'
                    '            float voltage = adc_value * 3.3f / 4096.0f;\n'
                    '            // ... обработка ...\n'
                    '            HAL_ADC_Start_IT(&hadc1);\n'
                    '        }\n'
                    '    }\n'
                    '}'
                ),
            },
            {
                'title': 'Отладка и профилирование FreeRTOS',
                'order': 5,
                'estimated_minutes': 15,
                'content': (
                    '<h3>Инструменты отладки FreeRTOS</h3>'
                    '<h3>vTaskList()</h3>'
                    '<p>Выводит таблицу задач: имя, состояние, приоритет, свободный стек, номер. '
                    'Требует configUSE_TRACE_FACILITY=1 и configUSE_STATS_FORMATTING_FUNCTIONS=1.</p>'
                    '<h3>vTaskGetRunTimeStats()</h3>'
                    '<p>Показывает время CPU на каждую задачу (в тиках или мкс). '
                    'Требует настройки таймера для высокочастотного счёта.</p>'
                    '<h3>configASSERT</h3>'
                    '<p>Определить как макрос с breakpoint или printf+while(1). '
                    'FreeRTOS вставляет assert во все критические места.</p>'
                    '<h3>Segger SystemView</h3>'
                    '<p>Профессиональный инструмент трассировки через RTT. '
                    'Показывает переключения задач на временной шкале, ISR, блокировки. '
                    'Бесплатен для FreeRTOS.</p>'
                    '<h3>Типичные проблемы</h3>'
                    '<ul>'
                    '<li><strong>Stack overflow</strong> — configCHECK_FOR_STACK_OVERFLOW=2</li>'
                    '<li><strong>Deadlock</strong> — две задачи ждут мьютексы друг друга</li>'
                    '<li><strong>Priority inversion</strong> — использовать мьютекс, не бинарный семафор</li>'
                    '<li><strong>ISR вызывает не-FromISR API</strong> — HardFault</li>'
                    '</ul>'
                ),
                'code_example': (
                    '// Вывод статистики задач\n'
                    '#include "FreeRTOS.h"\n'
                    '#include "task.h"\n\n'
                    '// В FreeRTOSConfig.h:\n'
                    '// #define configUSE_TRACE_FACILITY 1\n'
                    '// #define configUSE_STATS_FORMATTING_FUNCTIONS 1\n\n'
                    'void print_task_stats(void) {\n'
                    '    static char buf[512];\n\n'
                    '    printf("\\n=== Task List ===\\n");\n'
                    '    vTaskList(buf);\n'
                    '    printf("%s", buf);\n\n'
                    '    printf("\\n=== CPU Usage ===\\n");\n'
                    '    vTaskGetRunTimeStats(buf);\n'
                    '    printf("%s", buf);\n'
                    '}\n\n'
                    '// Stack overflow hook\n'
                    '// configCHECK_FOR_STACK_OVERFLOW = 2\n'
                    'void vApplicationStackOverflowHook(\n'
                    '        TaskHandle_t xTask, char *pcTaskName) {\n'
                    '    printf("STACK OVERFLOW: %s\\n", pcTaskName);\n'
                    '    while(1);  // Или reset\n'
                    '}'
                ),
            },
        ],
        'quiz': {
            'title': 'Тест: FreeRTOS',
            'pass_score': 70,
            'questions': [
                {
                    'text': 'Что делает vTaskDelay(pdMS_TO_TICKS(100))?',
                    'q_type': 'single',
                    'difficulty': 1,
                    'explanation': 'vTaskDelay переводит текущую задачу в состояние Blocked на указанное '
                                   'число тиков. pdMS_TO_TICKS конвертирует миллисекунды в тики планировщика.',
                    'choices': [
                        ('Останавливает всю систему на 100 мс', False),
                        ('Задача уходит в сон на 100 мс, CPU переходит к другим задачам', True),
                        ('Задача переходит в состояние Suspended', False),
                        ('Устанавливает тик планировщика равным 100 мс', False),
                    ],
                },
                {
                    'text': 'Какую функцию нужно использовать для отправки в очередь из ISR?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'Из ISR можно вызывать только функции с суффиксом FromISR. '
                                   'xQueueSend() нельзя вызывать из ISR — это может привести к HardFault.',
                    'choices': [
                        ('xQueueSend()', False),
                        ('xQueueSendFromISR()', True),
                        ('xQueueSendIT()', False),
                        ('xQueuePost()', False),
                    ],
                },
                {
                    'text': 'Что такое Priority Inheritance в контексте мьютексов FreeRTOS?',
                    'q_type': 'single',
                    'difficulty': 3,
                    'explanation': 'Priority Inheritance решает проблему инверсии приоритетов: '
                                   'когда низкоприоритетная задача держит мьютекс, нужный высокоприоритетной, '
                                   'её приоритет временно повышается до уровня ожидающей задачи.',
                    'choices': [
                        ('Задача наследует приоритет своего создателя', False),
                        ('Держатель мьютекса получает приоритет ожидающей задачи', True),
                        ('Задача с более высоким приоритетом ждёт завершения более низкой', False),
                        ('Приоритеты распределяются автоматически планировщиком', False),
                    ],
                },
                {
                    'text': 'Какая схема памяти FreeRTOS рекомендуется для большинства проектов?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'heap_4 поддерживает как выделение, так и освобождение памяти с '
                                   'объединением смежных свободных блоков (слияние), что минимизирует фрагментацию.',
                    'choices': [
                        ('heap_1 (только выделение)', False),
                        ('heap_2 (без слияния блоков)', False),
                        ('heap_4 (выделение + освобождение + слияние)', True),
                        ('malloc/free стандартной библиотеки', False),
                    ],
                },
                {
                    'text': 'Как правильно проверить, достаточно ли стека выделено задаче?',
                    'q_type': 'single',
                    'difficulty': 2,
                    'explanation': 'uxTaskGetStackHighWaterMark() возвращает минимальный свободный '
                                   'остаток стека за всё время жизни задачи (в словах). '
                                   'Если результат близок к 0 — стек слишком мал.',
                    'choices': [
                        ('Посмотреть значение SP в отладчике', False),
                        ('uxTaskGetStackHighWaterMark() — свободный стек в словах', True),
                        ('xTaskGetStackSize() — размер стека', False),
                        ('Запустить программу и ждать HardFault', False),
                    ],
                },
            ],
        },
    },
]


class Command(BaseCommand):
    help = 'Seed subject: Razrabotka PO dlya vstraivaemykh sistem (MDK.04.02)'

    def handle(self, *args, **options):
        subj, _ = Subject.objects.get_or_create(
            slug=SUBJECT['slug'],
            defaults={k: v for k, v in SUBJECT.items() if k != 'slug'}
        )
        self.stdout.write(f'Subject: {subj.title}')

        total_lessons = 0
        total_questions = 0

        for mod_data in MODULES:
            module, _ = TheoryModule.objects.get_or_create(
                subject=subj,
                title=mod_data['title'],
                defaults={
                    'icon': mod_data['icon'],
                    'order': mod_data['order'],
                    'description': mod_data['description'],
                }
            )
            self.stdout.write(f'  Module: {mod_data["title"]}')

            for lesson_data in mod_data['lessons']:
                lesson, is_new = TheoryLesson.objects.get_or_create(
                    module=module,
                    title=lesson_data['title'],
                    defaults={
                        'content': lesson_data['content'],
                        'code_example': lesson_data.get('code_example', ''),
                        'order': lesson_data['order'],
                        'estimated_minutes': lesson_data.get('estimated_minutes', 20),
                    }
                )
                if is_new:
                    total_lessons += 1
                    self.stdout.write(f'    [+] {lesson_data["title"]}')

            # Quiz
            qdata = mod_data.get('quiz')
            if qdata:
                quiz, _ = Quiz.objects.get_or_create(
                    module=module,
                    title=qdata['title'],
                    defaults={
                        'pass_score': qdata.get('pass_score', 70),
                        'is_active': True,
                        'order': mod_data['order'],
                    }
                )
                for i, q in enumerate(qdata['questions']):
                    question, is_new = Question.objects.get_or_create(
                        quiz=quiz,
                        text=q['text'],
                        defaults={
                            'q_type': q['q_type'],
                            'order': i + 1,
                            'difficulty': q.get('difficulty', 2),
                            'explanation': q.get('explanation', ''),
                            'code_snippet': q.get('code_snippet', ''),
                        }
                    )
                    if is_new:
                        total_questions += 1
                        for j, (text, correct) in enumerate(q['choices']):
                            AnswerChoice.objects.get_or_create(
                                question=question,
                                text=text,
                                defaults={'is_correct': correct, 'order': j + 1}
                            )

        self.stdout.write(f'\nDone. Lessons: {total_lessons}, Questions: {total_questions}')
