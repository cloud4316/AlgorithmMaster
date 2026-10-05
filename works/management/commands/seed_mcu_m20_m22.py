"""
Seed: МПС — новые модули M20-M22
КТП: Организация памяти МПС, структура МК, язык Си для МК
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


MODULES = [
    {
        'order': 20,
        'title': 'Организация памяти МПС',
        'icon': 'fas fa-memory',
        'description': 'ОЗУ, ПЗУ, кэш-память, адресация, стек, карта памяти МК',
        'lessons': [
            {
                'order': 1,
                'title': 'Типы памяти: ОЗУ, ПЗУ, Flash',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Типы памяти в МПС</h2>'
                    '<h3>ОЗУ — оперативное запоминающее устройство (RAM)</h3>'
                    '<table>'
                    '<tr><th>Тип</th><th>Полное название</th><th>Особенности</th><th>Применение</th></tr>'
                    '<tr><td>SRAM</td><td>Static RAM</td><td>6 транзисторов на ячейку, быстрое, энергозависимое</td><td>Внутренняя RAM МК, кэш L1/L2</td></tr>'
                    '<tr><td>DRAM</td><td>Dynamic RAM</td><td>1 транзистор + конденсатор, требует регенерации</td><td>ОЗУ ПК (DDR4/DDR5)</td></tr>'
                    '<tr><td>PSRAM</td><td>Pseudo-SRAM</td><td>Интерфейс SRAM, внутренняя регенерация</td><td>Внешняя RAM для МК</td></tr>'
                    '</table>'
                    '<h3>ПЗУ — постоянное запоминающее устройство (ROM/Flash)</h3>'
                    '<table>'
                    '<tr><th>Тип</th><th>Программирование</th><th>Стирание</th><th>Применение</th></tr>'
                    '<tr><td>ROM</td><td>При изготовлении</td><td>Невозможно</td><td>Маски серийных МС</td></tr>'
                    '<tr><td>PROM</td><td>Одноразовое</td><td>Невозможно</td><td>Устаревшие OTP МК</td></tr>'
                    '<tr><td>EPROM</td><td>Электрически</td><td>УФ-излучение</td><td>Устарело</td></tr>'
                    '<tr><td>EEPROM</td><td>Побайтово</td><td>Побайтово</td><td>Настройки, калибровки (1–128 КБ)</td></tr>'
                    '<tr><td>Flash</td><td>Электрически</td><td>Страницами/секторами</td><td>Программа МК, SSD, USB</td></tr>'
                    '</table>'
                    '<h3>Характеристики Flash (важно для МК)</h3>'
                    '<ul>'
                    '<li><strong>Ресурс стирания:</strong> 10 000 — 100 000 циклов (ячейка EEPROM)</li>'
                    '<li><strong>Страница/сектор:</strong> минимальная единица стирания (512 Б — 128 КБ)</li>'
                    '<li><strong>Время записи страницы:</strong> 1–50 мс (нельзя прерывать)</li>'
                    '<li><strong>Latency чтения:</strong> 1–5 тактов (нужны wait states при высокой частоте)</li>'
                    '</ul>'
                    '<div class="tip">STM32 Flash: при 72 МГц нужен 2 wait state. Забыть установить — '
                    'программа работает неправильно: МП читает мусор. Настраивается в FLASH_ACR.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'Кэш-память и адресация',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Кэш-память и организация адресного пространства</h2>'
                    '<h3>Кэш-память</h3>'
                    '<p>Кэш — быстрая SRAM-буферная память между МП и медленной основной памятью.</p>'
                    '<table>'
                    '<tr><th>Уровень</th><th>Размер</th><th>Время доступа</th><th>Расположение</th></tr>'
                    '<tr><td>L1</td><td>8–64 КБ (I$ + D$)</td><td>1–4 такта</td><td>Внутри ядра</td></tr>'
                    '<tr><td>L2</td><td>128 КБ — 4 МБ</td><td>5–15 тактов</td><td>Внутри кристалла</td></tr>'
                    '<tr><td>L3</td><td>4–64 МБ</td><td>30–60 тактов</td><td>Разделяется ядрами</td></tr>'
                    '<tr><td>RAM</td><td>ГБ</td><td>100–300 тактов</td><td>Отдельный кристалл</td></tr>'
                    '</table>'
                    '<p>Cortex-M0/M3 — без кэша. Cortex-M7 — 4–64 КБ I$ и D$ (опционально).</p>'
                    '<h3>Способы адресации памяти</h3>'
                    '<table>'
                    '<tr><th>Метод</th><th>Описание</th><th>Объём адресного пространства</th></tr>'
                    '<tr><td>Линейная</td><td>Каждая ячейка имеет уникальный адрес 0…N</td><td>2<sup>разрядность адресной шины</sup></td></tr>'
                    '<tr><td>Банковая</td><td>Переключение банков памяти</td><td>Банков × размер банка</td></tr>'
                    '<tr><td>Страничная (MMU)</td><td>Виртуальный адрес → физический (таблицы страниц)</td><td>4 ГБ (32 бит) / 256 ТБ (64 бит)</td></tr>'
                    '</table>'
                    '<h3>Карта памяти ARM Cortex-M (32 бит = 4 ГБ)</h3>'
                    '<table>'
                    '<tr><th>Адрес</th><th>Регион</th><th>Содержимое</th></tr>'
                    '<tr><td>0x00000000</td><td>Code</td><td>Flash, ROM (512 МБ)</td></tr>'
                    '<tr><td>0x20000000</td><td>SRAM</td><td>Внутренняя SRAM (512 МБ)</td></tr>'
                    '<tr><td>0x40000000</td><td>Peripheral</td><td>Регистры периферии APB/AHB (512 МБ)</td></tr>'
                    '<tr><td>0x60000000</td><td>External RAM</td><td>FSMC/FMC внешняя память (1 ГБ)</td></tr>'
                    '<tr><td>0xA0000000</td><td>External Device</td><td>Внешняя периферия (1 ГБ)</td></tr>'
                    '<tr><td>0xE0000000</td><td>System</td><td>NVIC, SysTick, Debug (512 МБ)</td></tr>'
                    '</table>'
                    '<div class="tip">Зная карту памяти, понятно почему GPIOA_BASE = 0x40010800 — это область периферии. '
                    'Разыменование нулевого указателя вызывает HardFault, т.к. регион 0x00000000 — Flash (не SRAM).</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Стек, куча и сегментация программы',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Стек, куча и размещение программы в памяти МК</h2>'
                    '<h3>Сегменты программы</h3>'
                    '<table>'
                    '<tr><th>Сегмент</th><th>Расположение</th><th>Содержимое</th><th>Изменяемость</th></tr>'
                    '<tr><td>.text</td><td>Flash</td><td>Машинный код программы</td><td>Только чтение</td></tr>'
                    '<tr><td>.rodata</td><td>Flash</td><td>Константы, строки (const)</td><td>Только чтение</td></tr>'
                    '<tr><td>.data</td><td>Flash → SRAM</td><td>Инициализированные глобальные переменные</td><td>Копируется в SRAM при старте</td></tr>'
                    '<tr><td>.bss</td><td>SRAM</td><td>Нулевые глобальные переменные</td><td>Обнуляется при старте</td></tr>'
                    '<tr><td>Stack</td><td>SRAM (вверх)</td><td>Локальные переменные, адреса возврата</td><td>Растёт вниз</td></tr>'
                    '<tr><td>Heap</td><td>SRAM (вниз)</td><td>Динамическая память (malloc)</td><td>Растёт вверх</td></tr>'
                    '</table>'
                    '<h3>Стек (Stack)</h3>'
                    '<ul>'
                    '<li>LIFO — Last In First Out</li>'
                    '<li>SP (Stack Pointer) — регистр, указывающий на вершину стека</li>'
                    '<li>При вызове функции: PUSH параметров, адрес возврата → SP -= размер</li>'
                    '<li>При возврате: POP → SP += размер</li>'
                    '<li><strong>Stack overflow:</strong> SP уходит в область .bss/.data — данные портятся → сброс/HardFault</li>'
                    '</ul>'
                    '<h3>Куча (Heap)</h3>'
                    '<ul>'
                    '<li>Используется <code>malloc()</code>, <code>free()</code>, new/delete</li>'
                    '<li>Во встраиваемых системах динамическую память следует избегать: фрагментация, непредсказуемое время</li>'
                    '<li>Для МК предпочтительны статические/стековые выделения</li>'
                    '</ul>'
                    '<h3>Пример размещения для STM32F103 (20 КБ SRAM)</h3>'
                    '<pre><code>SRAM: 0x20000000 — 0x20004FFF (20480 байт)\n'
                    '  .data: 0x20000000 — +256 байт\n'
                    '  .bss:  +256 — +512 байт\n'
                    '  Heap:  +512 — +1024 байт (если нужна)\n'
                    '  Stack: 0x20004FFF — вниз (типично 1–4 КБ)</code></pre>'
                    '<div class="tip">Stack overflow на МК без MMU приводит к тихой порче данных. '
                    'Защита: FreeRTOS StackOverflowHook, или заполнить стек паттерном 0xDEADBEEF при старте и проверять в цикле.</div>'
                ),
            },
            {
                'order': 4,
                'title': 'Организация памяти МК STM32 на практике',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Практическая организация памяти STM32</h2>'
                    '<h3>Startup-код и карта памяти (.ld линкер-скрипт)</h3>'
                    '<p>Линкер-скрипт (<code>STM32F103C8Tx_FLASH.ld</code>) определяет расположение секций:</p>'
                    '<pre><code>MEMORY {\n'
                    '  RAM   (xrw) : ORIGIN = 0x20000000, LENGTH = 20K\n'
                    '  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 64K\n'
                    '}\n\n'
                    'SECTIONS {\n'
                    '  .text   : { *(.text*) } > FLASH\n'
                    '  .rodata : { *(.rodata*) } > FLASH\n'
                    '  .data   : { *(.data*) } > RAM AT> FLASH  /* LMA в Flash, VMA в RAM */\n'
                    '  .bss    : { *(.bss*) } > RAM\n'
                    '  ._user_heap_stack : { . = ALIGN(4); . += 0x400; } > RAM\n'
                    '}</code></pre>'
                    '<h3>Startup-последовательность</h3>'
                    '<ol>'
                    '<li>МК стартует с адреса из вектора сброса</li>'
                    '<li>Startup.s копирует .data из Flash в SRAM</li>'
                    '<li>Обнуляет .bss</li>'
                    '<li>Инициализирует системный таймер (SystemInit)</li>'
                    '<li>Вызывает main()</li>'
                    '</ol>'
                    '<h3>Работа с постоянной памятью (EEPROM-эмуляция)</h3>'
                    '<p>STM32 не имеет выделенного EEPROM. Для хранения настроек:</p>'
                    '<ul>'
                    '<li>Последняя страница Flash как эмулированный EEPROM</li>'
                    '<li>HAL: <code>HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, addr, data)</code></li>'
                    '<li>Стирание страницы: <code>HAL_FLASHEx_Erase(&erase_config, &err)</code></li>'
                    '<li>Ресурс: 10 000 циклов стирания. Алгоритм wear leveling продлевает до 100 000+</li>'
                    '</ul>'
                    '<div class="tip">Для частой записи (каждые секунды) — внешний EEPROM AT24Cxx по I2C (1 000 000 циклов).'
                    ' Flash подходит для редко меняемых настроек (конфигурация устройства).</div>'
                ),
            },
        ],
    },
    {
        'order': 21,
        'title': 'Микроконтроллеры STM32: структура и периферия',
        'icon': 'fas fa-microchip',
        'description': 'Структура STM32, GPIO, тактирование, регистры периферии',
        'lessons': [
            {
                'order': 1,
                'title': 'Архитектура STM32: ядро и периферия',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Архитектура STM32</h2>'
                    '<p>STM32 — семейство 32-битных МК Texas Instruments на ядре ARM Cortex-M производства STMicroelectronics.</p>'
                    '<h3>Семейства STM32</h3>'
                    '<table>'
                    '<tr><th>Серия</th><th>Ядро</th><th>Частота</th><th>Позиционирование</th></tr>'
                    '<tr><td>STM32F0</td><td>Cortex-M0</td><td>48 МГц</td><td>Бюджетные, замена 8-бит МК</td></tr>'
                    '<tr><td>STM32F1</td><td>Cortex-M3</td><td>72 МГц</td><td>Основная рабочая лошадка</td></tr>'
                    '<tr><td>STM32F4</td><td>Cortex-M4F</td><td>168–180 МГц</td><td>DSP, FPU, USB OTG</td></tr>'
                    '<tr><td>STM32F7</td><td>Cortex-M7</td><td>216 МГц</td><td>Высокая производительность, кэш</td></tr>'
                    '<tr><td>STM32H7</td><td>Cortex-M7</td><td>480 МГц</td><td>Топовая производительность</td></tr>'
                    '<tr><td>STM32L0/L4</td><td>Cortex-M0+/M4</td><td>32–80 МГц</td><td>Ультра-низкое потребление</td></tr>'
                    '<tr><td>STM32G0/G4</td><td>Cortex-M0+/M4</td><td>64–170 МГц</td><td>Универсальные новые серии</td></tr>'
                    '</table>'
                    '<h3>Структура STM32F103 (Cortex-M3)</h3>'
                    '<ul>'
                    '<li><strong>Ядро:</strong> ARM Cortex-M3, 72 МГц, 32-бит RISC</li>'
                    '<li><strong>Flash:</strong> 64–128 КБ (программа)</li>'
                    '<li><strong>SRAM:</strong> 20 КБ</li>'
                    '<li><strong>GPIO:</strong> до 80 линий, порты A–E</li>'
                    '<li><strong>Таймеры:</strong> TIM1 (advanced), TIM2–TIM4 (general purpose)</li>'
                    '<li><strong>Коммуникация:</strong> 3×USART, 2×SPI, 2×I2C, CAN, USB FS</li>'
                    '<li><strong>АЦП:</strong> 2×ADC, 12-бит, 1 МГц</li>'
                    '<li><strong>Питание:</strong> 2.0–3.6 В</li>'
                    '</ul>'
                    '<h3>Шинная матрица STM32</h3>'
                    '<ul>'
                    '<li><strong>AHB (Advanced High-performance Bus):</strong> ядро, Flash, SRAM, DMA — высокоскоростная</li>'
                    '<li><strong>APB1 (36 МГц):</strong> медленная периферия: USART2-3, SPI2, I2C, таймеры 2-4</li>'
                    '<li><strong>APB2 (72 МГц):</strong> быстрая периферия: GPIO, ADC, SPI1, USART1, TIM1</li>'
                    '</ul>'
                    '<div class="tip">GPIO на APB2 (72 МГц) — порт может переключаться до 50 МГц. '
                    'I2C на APB1 (36 МГц) — максимум 400 кГц Fast Mode. Учитывать при настройке предделителей.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'GPIO и управление тактированием',
                'estimated_minutes': 20,
                'content': (
                    '<h2>GPIO и система тактирования STM32</h2>'
                    '<h3>GPIO (General Purpose Input/Output)</h3>'
                    '<p>Каждый порт GPIO (A–E) имеет 16 линий. Конфигурируется через регистры:</p>'
                    '<table>'
                    '<tr><th>Регистр</th><th>Назначение</th></tr>'
                    '<tr><td>GPIOx_CRL</td><td>Конфигурация линий 0–7 (2+2 бита на линию)</td></tr>'
                    '<tr><td>GPIOx_CRH</td><td>Конфигурация линий 8–15</td></tr>'
                    '<tr><td>GPIOx_IDR</td><td>Регистр входных данных (чтение)</td></tr>'
                    '<tr><td>GPIOx_ODR</td><td>Регистр выходных данных (запись)</td></tr>'
                    '<tr><td>GPIOx_BSRR</td><td>Атомарная установка/сброс битов (без операций чтение-модификация-запись)</td></tr>'
                    '</table>'
                    '<h3>Режимы GPIO</h3>'
                    '<table>'
                    '<tr><th>Режим</th><th>CNF[1:0]+MODE[1:0]</th><th>Применение</th></tr>'
                    '<tr><td>Входной с подтяжкой</td><td>CNF=10, MODE=00</td><td>Кнопка, датчик (pull-up/down)</td></tr>'
                    '<tr><td>Входной аналоговый</td><td>CNF=00, MODE=00</td><td>АЦП вход</td></tr>'
                    '<tr><td>Входной плавающий</td><td>CNF=01, MODE=00</td><td>Высокоимпедансный вход</td></tr>'
                    '<tr><td>Выход 2 МГц</td><td>CNF=00, MODE=10</td><td>Медленная цифровая логика</td></tr>'
                    '<tr><td>Выход 50 МГц</td><td>CNF=00, MODE=11</td><td>Быстрая логика, SPI CLK</td></tr>'
                    '<tr><td>Альтернативная функция (AF)</td><td>CNF=10, MODE=11</td><td>USART, SPI, I2C, TIM_CH</td></tr>'
                    '</table>'
                    '<h3>Тактирование — система RCC</h3>'
                    '<p>Прежде чем работать с периферией, нужно включить её тактирование через RCC (Reset and Clock Control).</p>'
                    '<pre><code>// Включить тактирование порта C и APB2\n'
                    'RCC->APB2ENR |= RCC_APB2ENR_IOPCEN;\n'
                    '// Включить тактирование TIM2 через APB1\n'
                    'RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;\n'
                    '// Настроить PC13 как выход 2 МГц push-pull\n'
                    'GPIOC->CRH &= ~(GPIO_CRH_CNF13 | GPIO_CRH_MODE13);\n'
                    'GPIOC->CRH |= GPIO_CRH_MODE13_1; // 2 МГц output\n'
                    '// Включить LED (PC13 на Blue Pill — инверсная логика)\n'
                    'GPIOC->BSRR = GPIO_BSRR_BR13; // сброс = лог. 0 = LED ON</code></pre>'
                    '<div class="tip">Самая частая ошибка: периферия не работает → проверьте RCC. '
                    'Если не включить тактирование через APB1ENR/APB2ENR — регистры периферии недоступны, '
                    'записанное значение не сохраняется.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Прерывания NVIC и EXTI',
                'estimated_minutes': 20,
                'content': (
                    '<h2>NVIC и внешние прерывания EXTI в STM32</h2>'
                    '<h3>NVIC — Nested Vectored Interrupt Controller</h3>'
                    '<p>NVIC — контроллер прерываний ARM Cortex-M. Особенности:</p>'
                    '<ul>'
                    '<li>До 240 внешних прерываний (STM32F1 — 68)</li>'
                    '<li>16 уровней приоритетов (4-битное поле)</li>'
                    '<li>Вложенность: ISR с высоким приоритетом прерывает ISR с низким</li>'
                    '<li>Автосохранение контекста аппаратно (R0-R3, R12, LR, PC, xPSR)</li>'
                    '<li>Низкая задержка: 12 тактов до входа в ISR</li>'
                    '</ul>'
                    '<h3>Конфигурация прерывания от кнопки (EXTI)</h3>'
                    '<pre><code>// 1. Включить тактирование GPIOA и AFIO\n'
                    'RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_AFIOEN;\n\n'
                    '// 2. PA0 как вход с подтяжкой вверх\n'
                    'GPIOA->CRL &= ~(GPIO_CRL_CNF0 | GPIO_CRL_MODE0);\n'
                    'GPIOA->CRL |= GPIO_CRL_CNF0_1; // Вход с подтяжкой\n'
                    'GPIOA->ODR |= GPIO_ODR_ODR0;   // Подтяжка вверх\n\n'
                    '// 3. Маппинг PA0 на EXTI0\n'
                    'AFIO->EXTICR[0] &= ~AFIO_EXTICR1_EXTI0;\n\n'
                    '// 4. Настройка EXTI: триггер по спаду\n'
                    'EXTI->FTSR |= EXTI_FTSR_TR0;\n'
                    'EXTI->IMR  |= EXTI_IMR_MR0;  // Разрешить прерывание\n\n'
                    '// 5. Включить в NVIC с приоритетом 1\n'
                    'NVIC_SetPriority(EXTI0_IRQn, 1);\n'
                    'NVIC_EnableIRQ(EXTI0_IRQn);\n\n'
                    '// ISR\n'
                    'void EXTI0_IRQHandler(void) {\n'
                    '    if (EXTI->PR & EXTI_PR_PR0) {\n'
                    '        EXTI->PR = EXTI_PR_PR0; // Сбросить флаг (записью 1)\n'
                    '        GPIOC->ODR ^= GPIO_ODR_ODR13; // Переключить LED\n'
                    '    }\n'
                    '}</code></pre>'
                    '<div class="tip">EXTI->PR сбрасывается записью <strong>единицы</strong> в бит (не нуля!). '
                    'Если не сбросить — ISR будет вызываться бесконечно.</div>'
                ),
            },
        ],
    },
    {
        'order': 22,
        'title': 'Язык Си для МК: основы и управляющие конструкции',
        'icon': 'fas fa-code',
        'description': 'Типы данных, операторы, указатели, управление памятью в Си для МК',
        'lessons': [
            {
                'order': 1,
                'title': 'Типы данных и переменные в Си для МК',
                'estimated_minutes': 25,
                'content': (
                    '<h2>Типы данных Си для встраиваемых систем</h2>'
                    '<p>В отличие от ПК, на МК размер <code>int</code> может быть 16 или 32 бита. '
                    'Используйте фиксированные типы из <code>&lt;stdint.h&gt;</code>:</p>'
                    '<table>'
                    '<tr><th>Тип (stdint.h)</th><th>Размер</th><th>Диапазон</th><th>Применение</th></tr>'
                    '<tr><td>uint8_t</td><td>1 байт</td><td>0 … 255</td><td>Байт данных, регистр</td></tr>'
                    '<tr><td>int8_t</td><td>1 байт</td><td>-128 … 127</td><td>Знаковый байт</td></tr>'
                    '<tr><td>uint16_t</td><td>2 байта</td><td>0 … 65535</td><td>АЦП результат (12 бит)</td></tr>'
                    '<tr><td>int16_t</td><td>2 байта</td><td>-32768 … 32767</td><td>Угол (градусы × 100)</td></tr>'
                    '<tr><td>uint32_t</td><td>4 байта</td><td>0 … 4 294 967 295</td><td>Регистры периферии, мс от старта</td></tr>'
                    '<tr><td>int32_t</td><td>4 байта</td><td>±2 млрд</td><td>Счётчики с переполнением</td></tr>'
                    '<tr><td>bool (stdbool.h)</td><td>1 байт</td><td>false/true</td><td>Флаги состояния</td></tr>'
                    '</table>'
                    '<h3>Квалификаторы для МК</h3>'
                    '<table>'
                    '<tr><th>Квалификатор</th><th>Значение</th><th>Применение</th></tr>'
                    '<tr><td>volatile</td><td>Запрет оптимизации чтения/записи</td><td>Регистры периферии, переменные ISR</td></tr>'
                    '<tr><td>const</td><td>Константа, размещается в Flash</td><td>Таблицы, строки, конфигурация</td></tr>'
                    '<tr><td>static</td><td>Постоянное место в RAM (не стек)</td><td>Локальные переменные с сохранением значения</td></tr>'
                    '<tr><td>register</td><td>Подсказка компилятору хранить в регистре</td><td>Устарело, компилятор сам оптимизирует</td></tr>'
                    '</table>'
                    '<h3>Пример: volatile обязателен для регистров</h3>'
                    '<pre><code>// НЕПРАВИЛЬНО — компилятор уберёт "лишние" чтения:\nuint32_t val = GPIOA->IDR;\nwhile (val == 0) val = GPIOA->IDR; // может стать while(true)\n\n// ПРАВИЛЬНО:\nvolatile uint32_t *idr = &GPIOA->IDR;\nwhile (*idr == 0); // каждое чтение = реальное обращение к регистру</code></pre>'
                    '<p>В HAL все регистры уже объявлены через <code>__IO</code> (= volatile), поэтому <code>GPIOA->IDR</code> безопасен.</p>'
                    '<div class="tip">Забыть volatile на переменную флага из ISR — классическая ошибка МК-программирования. '
                    'Компилятор кэширует значение в регистре процессора и не видит изменений из прерывания.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'Управляющие конструкции и функции',
                'estimated_minutes': 25,
                'content': (
                    '<h2>Управляющие конструкции Си</h2>'
                    '<h3>Условные операторы</h3>'
                    '<pre><code>// if-else\nif (button_pressed) {\n    LED_ON();\n} else {\n    LED_OFF();\n}\n\n// switch — эффективен для состояний (конечный автомат)\nswitch (state) {\n    case STATE_IDLE:\n        handle_idle();\n        break;\n    case STATE_RUN:\n        handle_run();\n        break;\n    default:\n        error_handler();\n}</code></pre>'
                    '<h3>Циклы</h3>'
                    '<pre><code>// for — счётный цикл\nfor (uint8_t i = 0; i < 8; i++) {\n    send_bit(data >> i & 1);\n}\n\n// while — с условием\nwhile (!USART_ready()) {\n    __NOP(); // не пустой цикл — NOP явно\n}\n\n// do-while — хоть раз выполнить\ndo {\n    status = ADC_read();\n} while (status == ADC_BUSY);</code></pre>'
                    '<h3>Функции</h3>'
                    '<pre><code>// Объявление и определение\nvoid delay_ms(uint32_t ms);\n\nvoid delay_ms(uint32_t ms) {\n    uint32_t start = HAL_GetTick();\n    while ((HAL_GetTick() - start) < ms);\n}\n\n// Inline для коротких критичных функций\nstatic inline void LED_toggle(void) {\n    GPIOC->ODR ^= GPIO_ODR_ODR13;\n}</code></pre>'
                    '<h3>Полезные паттерны для МК</h3>'
                    '<table>'
                    '<tr><th>Паттерн</th><th>Код</th><th>Назначение</th></tr>'
                    '<tr><td>Установить бит</td><td><code>reg |= (1 &lt;&lt; n)</code></td><td>Включить функцию</td></tr>'
                    '<tr><td>Сбросить бит</td><td><code>reg &amp;= ~(1 &lt;&lt; n)</code></td><td>Выключить функцию</td></tr>'
                    '<tr><td>Переключить бит</td><td><code>reg ^= (1 &lt;&lt; n)</code></td><td>Мигание LED</td></tr>'
                    '<tr><td>Проверить бит</td><td><code>if (reg &amp; (1 &lt;&lt; n))</code></td><td>Проверить флаг</td></tr>'
                    '</table>'
                    '<div class="tip">На МК без кэша каждое условие, цикл и вызов функции — реальные такты. '
                    'Конечный автомат (switch по состоянию) эффективнее глубокой вложенности if-else.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Указатели и работа с памятью',
                'estimated_minutes': 25,
                'content': (
                    '<h2>Указатели в Си для МК</h2>'
                    '<h3>Зачем указатели на МК</h3>'
                    '<ul>'
                    '<li>Прямой доступ к регистрам периферии по физическому адресу</li>'
                    '<li>Передача больших структур в функции без копирования</li>'
                    '<li>Обработчики прерываний, таблицы функций, callback-и</li>'
                    '<li>Работа с кольцевыми буферами (DMA, UART)</li>'
                    '</ul>'
                    '<h3>Указатели на регистры периферии</h3>'
                    '<pre><code>// STM32 GPIOC_ODR по физическому адресу:\n'
                    '#define GPIOC_ODR (*(volatile uint32_t*)0x4001100C)\n'
                    'GPIOC_ODR |= (1 << 13); // Установить PC13\n\n'
                    '// Тоже самое через CMSIS-структуры (удобнее):\n'
                    'GPIOC->ODR |= GPIO_ODR_ODR13;</code></pre>'
                    '<h3>Указатели на функции (callback)</h3>'
                    '<pre><code>typedef void (*callback_t)(void);\n\nvoid timer_set_callback(callback_t cb);\n\nvoid my_handler(void) {\n    LED_toggle();\n}\n\n// Регистрация:\ntimer_set_callback(my_handler);\n\n// Вызов из ISR таймера:\nif (callback) callback();</code></pre>'
                    '<h3>Указатели и массивы</h3>'
                    '<pre><code>uint8_t buf[64];\nuint8_t *p = buf; // p указывает на buf[0]\n\n// Итерация через указатель (быстрее на МК без кэша):\nfor (uint8_t *end = buf + 64; p < end; p++) {\n    *p = 0;\n}\n\n// Передача буфера в функцию:\nvoid UART_send(const uint8_t *data, uint16_t len) {\n    for (uint16_t i = 0; i < len; i++) {\n        while (!(USART1->SR & USART_SR_TXE));\n        USART1->DR = data[i];\n    }\n}</code></pre>'
                    '<h3>Квалификатор const с указателями</h3>'
                    '<table>'
                    '<tr><th>Объявление</th><th>Что константно</th></tr>'
                    '<tr><td><code>const uint8_t *p</code></td><td>Данные нельзя менять, адрес можно</td></tr>'
                    '<tr><td><code>uint8_t * const p</code></td><td>Адрес нельзя менять, данные можно</td></tr>'
                    '<tr><td><code>const uint8_t * const p</code></td><td>Ни адрес, ни данные нельзя менять</td></tr>'
                    '</table>'
                    '<div class="tip">Используй <code>const uint8_t *</code> для входных буферов функций — компилятор запретит случайную запись и сможет разместить данные в Flash (экономия ценной RAM).</div>'
                ),
            },
            {
                'order': 4,
                'title': 'Структуры, битовые поля и перечисления',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Структуры, битовые поля и перечисления в Си для МК</h2>'
                    '<h3>Структуры</h3>'
                    '<pre><code>typedef struct {\n'
                    '    float temperature;   // 4 байта\n'
                    '    float humidity;      // 4 байта\n'
                    '    uint32_t timestamp;  // 4 байта\n'
                    '    uint8_t  sensor_id;  // 1 байт (+ 3 выравнивания)\n'
                    '} SensorData_t;           // Итого: 16 байт\n\n'
                    'SensorData_t data;\n'
                    'data.temperature = 23.5f;\n\n'
                    '// Передача по ссылке (без копирования 16 байт):\n'
                    'void log_data(const SensorData_t *d) {\n'
                    '    printf("T=%.1f H=%.1f\\n", d->temperature, d->humidity);\n'
                    '}</code></pre>'
                    '<h3>Битовые поля</h3>'
                    '<pre><code>// Отображение регистра управления\ntypedef struct {\n'
                    '    uint8_t enable    : 1; // бит 0\n'
                    '    uint8_t direction : 1; // бит 1\n'
                    '    uint8_t speed     : 2; // биты 2-3\n'
                    '    uint8_t reserved  : 4; // биты 4-7\n'
                    '} MotorCtrl_t;\n\n'
                    'MotorCtrl_t ctrl = {0};\n'
                    'ctrl.enable = 1;\n'
                    'ctrl.speed  = 3; // максимальная скорость</code></pre>'
                    '<h3>Перечисления (enum)</h3>'
                    '<pre><code>typedef enum {\n'
                    '    STATE_IDLE = 0,\n'
                    '    STATE_INIT,\n'
                    '    STATE_MEASURE,\n'
                    '    STATE_SEND,\n'
                    '    STATE_ERROR,\n'
                    '} AppState_t;\n\n'
                    'AppState_t state = STATE_IDLE;\n\n'
                    'switch (state) {\n'
                    '    case STATE_IDLE:    /* ... */ break;\n'
                    '    case STATE_MEASURE: /* ... */ break;\n'
                    '    default: error();\n'
                    '}</code></pre>'
                    '<div class="tip">Конечный автомат на enum + switch — стандартный паттерн встраиваемых систем. '
                    'Читаем, эффективен (switch компилируется в jump table), легко расширяем.</div>'
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed МПС модули M20-M22: память МПС, структура STM32, Си для МК'

    def handle(self, *args, **options):
        subject = Subject.objects.filter(slug='mcu').first()
        if not subject:
            self.stderr.write('Subject mcu not found')
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

        self.stdout.write(self.style.SUCCESS('Done: M20-M22 seeded'))
