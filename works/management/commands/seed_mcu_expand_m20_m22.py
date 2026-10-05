from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson

M20_LESSONS = [
    {
        'order': 1,
        'title': 'Организация памяти МПС: типы и иерархия',
        'content': '''<h2>Организация памяти МПС: типы и иерархия</h2>
<p>Память микропроцессорной системы — многоуровневая иерархия хранилищ, различающихся по скорости, объёму и стоимости. Чем ближе память к процессору, тем она быстрее и меньше по объёму.</p>

<h3>Иерархия памяти</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Уровень</th><th>Тип</th><th>Время доступа</th><th>Типичный объём</th></tr>
  <tr><td>L0</td><td>Регистры ЦП</td><td>1 такт</td><td>16–32 × 32/64 бит</td></tr>
  <tr><td>L1</td><td>Кэш L1</td><td>2–4 такта</td><td>16–64 КБ</td></tr>
  <tr><td>L2</td><td>Кэш L2</td><td>10–20 тактов</td><td>256 КБ – 4 МБ</td></tr>
  <tr><td>L3</td><td>Кэш L3</td><td>30–50 тактов</td><td>8–64 МБ</td></tr>
  <tr><td>—</td><td>ОЗУ (DRAM)</td><td>50–200 нс</td><td>ГБ</td></tr>
  <tr><td>—</td><td>Flash / SSD</td><td>100 мкс – мс</td><td>ГБ–ТБ</td></tr>
</table>

<h3>Виды ОЗУ</h3>
<ul>
  <li><strong>SRAM (Static RAM)</strong> — триггерная ячейка, 6 транзисторов. Быстрая, дорогая. Используется для кэшей и встроенной ОЗУ МК.</li>
  <li><strong>DRAM (Dynamic RAM)</strong> — конденсатор + транзистор. Требует регенерации каждые ~64 мс. Дешёвая, плотная. Основная системная память ПК.</li>
  <li><strong>SDRAM / DDR5</strong> — синхронная DRAM, передача по обоим фронтам, пакетная передача. DDR5: до 8400 МТ/с.</li>
</ul>

<h3>Виды ПЗУ</h3>
<ul>
  <li><strong>Mask ROM</strong> — прошивается на заводе. Производство дорого, изменение невозможно.</li>
  <li><strong>OTP (One-Time Programmable)</strong> — программируется один раз пользователем.</li>
  <li><strong>Flash</strong> — электрически стираемая, секторная запись. Стандарт для МК (STM32, AVR).</li>
  <li><strong>EEPROM</strong> — побайтовое стирание, ресурс ~100 000 циклов. Хранение настроек.</li>
</ul>

<h3>Карта памяти МПС</h3>
<p>Микроконтроллер STM32F103 имеет единое 32-битное адресное пространство 4 ГБ:</p>
<pre><code>0x0800 0000 – 0x0801 FFFF  Flash (128 КБ)
0x2000 0000 – 0x2000 4FFF  SRAM  (20 КБ)
0x4000 0000 – 0x4FFF FFFF  Периферия APB1/APB2
0xE000 0000 – 0xE00F FFFF  System (NVIC, SysTick, ITM)
</code></pre>

<div class="tip">Принцип: регистры периферии отображаются в адресное пространство (Memory-Mapped I/O). Доступ через обычные инструкции LDR/STR.</div>''',
    },
    {
        'order': 2,
        'title': 'Кэш-память: принципы, ассоциативность и политики',
        'content': '''<h2>Кэш-память: принципы, ассоциативность и политики</h2>
<p>Кэш — быстрая буферная память между процессором и медленной основной памятью. Работает на принципах <em>пространственной</em> и <em>временной локальности</em>.</p>

<h3>Локальность</h3>
<ul>
  <li><strong>Временная</strong> — если ячейка использована, она скоро понадобится снова (циклы, переменные).</li>
  <li><strong>Пространственная</strong> — если ячейка использована, соседние тоже понадобятся (массивы, инструкции).</li>
</ul>

<h3>Структура кэша</h3>
<p>Кэш делится на <strong>строки (cache lines)</strong>, типично 64 байта. Адрес разбивается:</p>
<pre><code>[Tag | Index | Offset]
 Tag    — идентифицирует блок в памяти
 Index  — номер набора (set) в кэше
 Offset — байт внутри строки
</code></pre>

<h3>Ассоциативность</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Тип</th><th>Описание</th><th>Плюс</th><th>Минус</th></tr>
  <tr><td>Прямое отображение</td><td>1 место для строки</td><td>Простота</td><td>Конфликты</td></tr>
  <tr><td>N-way set-associative</td><td>N мест на набор</td><td>Баланс</td><td>Сложнее</td></tr>
  <tr><td>Полностью ассоциативный</td><td>Любое место</td><td>Нет конфликтов</td><td>Дорог</td></tr>
</table>
<p>ARM Cortex-M7 L1 data cache — 4-way set-associative, 32 байта/строка.</p>

<h3>Политики замещения</h3>
<ul>
  <li><strong>LRU (Least Recently Used)</strong> — вытесняется самая давно использованная строка.</li>
  <li><strong>FIFO</strong> — вытесняется самая старая загруженная строка.</li>
  <li><strong>Random</strong> — случайный выбор. Прост в реализации.</li>
</ul>

<h3>Политики записи</h3>
<ul>
  <li><strong>Write-through</strong> — запись одновременно в кэш и в RAM. Просто, медленнее.</li>
  <li><strong>Write-back</strong> — запись только в кэш, в RAM при вытеснении строки. Быстрее, сложнее когерентность.</li>
</ul>

<h3>Кэш в STM32 (Cortex-M7)</h3>
<pre><code>// Включить I-cache и D-cache
SCB_EnableICache();
SCB_EnableDCache();

// Очистить D-cache перед DMA-передачей
SCB_CleanDCache_by_Addr((uint32_t*)buffer, sizeof(buffer));
// Инвалидировать после DMA-приёма
SCB_InvalidateDCache_by_Addr((uint32_t*)buffer, sizeof(buffer));
</code></pre>
<div class="tip">Не включив кэш-операции при DMA, получишь данные из кэша (старые), а не из памяти.</div>''',
    },
    {
        'order': 3,
        'title': 'Flash-память МК: организация, запись, защита',
        'content': '''<h2>Flash-память МК: организация, запись, защита</h2>
<p>Flash во встраиваемых системах — основное хранилище программ и констант. STM32 хранит скетч и конфиг прямо во Flash. EEPROM-эмуляция — стандартная техника для хранения настроек.</p>

<h3>Структура Flash STM32F4</h3>
<pre><code>Сектор 0:  0x0800 0000,  16 КБ
Сектор 1:  0x0800 4000,  16 КБ
Сектор 2:  0x0800 8000,  16 КБ
Сектор 3:  0x0800 C000,  16 КБ
Сектор 4:  0x0801 0000,  64 КБ
Сектор 5:  0x0802 0000, 128 КБ
...
Сектор 11: 0x080E 0000, 128 КБ  (итого 1 МБ)
</code></pre>

<h3>Алгоритм записи во Flash (STM32 HAL)</h3>
<pre><code>HAL_FLASH_Unlock();

// Стереть сектор
FLASH_EraseInitTypeDef er = {
    .TypeErase   = FLASH_TYPEERASE_SECTORS,
    .Sector      = FLASH_SECTOR_5,
    .NbSectors   = 1,
    .VoltageRange= FLASH_VOLTAGE_RANGE_3
};
uint32_t err;
HAL_FLASHEx_Erase(&er, &err);

// Записать данные (32-разрядными словами)
uint32_t addr = 0x08020000;
uint32_t data[] = {0xDEADBEEF, 0x12345678};
for (int i = 0; i < 2; i++) {
    HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD,
                      addr + i*4, data[i]);
}

HAL_FLASH_Lock();
</code></pre>

<h3>Важные ограничения</h3>
<ul>
  <li>Нельзя стереть байт — только целый сектор.</li>
  <li>Запись только в стёртые ячейки (0xFF → любое).</li>
  <li>Ресурс: 10 000 – 100 000 циклов стирания.</li>
  <li>Во время стирания/записи процессор не может читать Flash (если нет wait-buffer). Критический код копируют в RAM (атрибут <code>__attribute__((section(".RamFunc")))</code>).</li>
</ul>

<h3>EEPROM-эмуляция</h3>
<p>STM32 не имеет аппаратного EEPROM. Стандартный метод: два Flash-сектора, данные пишутся постранично, при заполнении — перенос на второй сектор.</p>
<pre><code>#include "eeprom.h"   // ST Application Note AN2594

EE_Init();
EE_WriteVariable(VirtAddr, Data);
EE_ReadVariable(VirtAddr, &Data);
</code></pre>

<h3>Защита Flash</h3>
<ul>
  <li><strong>Read protection (RDP)</strong> — уровни 0/1/2. Level 1: JTAG-дамп запрещён. Level 2: необратимо.</li>
  <li><strong>Write protection</strong> — защита секторов от записи через OB (Option Bytes).</li>
</ul>''',
    },
    {
        'order': 4,
        'title': 'ОЗУ во встраиваемых системах: стек, куча, секции',
        'content': '''<h2>ОЗУ во встраиваемых системах: стек, куча, секции</h2>
<p>В МК ОЗУ ограничен — типично 20–512 КБ. Программист обязан понимать раскладку памяти.</p>

<h3>Секции ELF / ld-скрипта</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Секция</th><th>Содержимое</th><th>Где</th></tr>
  <tr><td>.text</td><td>Машинный код</td><td>Flash</td></tr>
  <tr><td>.rodata</td><td>Константы (const)</td><td>Flash</td></tr>
  <tr><td>.data</td><td>Инициализированные глобальные переменные</td><td>Flash (init) → RAM (runtime)</td></tr>
  <tr><td>.bss</td><td>Нулевые глобальные переменные</td><td>RAM (заполняется 0 при старте)</td></tr>
  <tr><td>Heap</td><td>Динамическая память (malloc)</td><td>RAM ↑</td></tr>
  <tr><td>Stack</td><td>Локальные переменные, возврат функций</td><td>RAM ↓ (растёт вниз)</td></tr>
</table>

<h3>Карта RAM (пример STM32F103, 20 КБ)</h3>
<pre><code>0x2000 0000  _sdata  ← .data (инициализированные)
             _edata
             _sbss   ← .bss  (нулевые)
             _ebss
             heap_start
               ...   (malloc)
             heap_end
               ...   (пусто)
0x2000 5000  _estack ← верхушка стека (MSP = 0x20004FFF)
</code></pre>

<h3>Переполнение стека</h3>
<p>Stack overflow во встраиваемых — частая причина зависаний. Защиты:</p>
<ul>
  <li><strong>MPU Stack Guard</strong> — регион с запретом записи у дна стека. Fault при выходе.</li>
  <li><strong>Watermark</strong> — заполнить стек паттерном 0xDEADDEAD при старте, проверить остаток.</li>
  <li>FreeRTOS: <code>uxTaskGetStackHighWaterMark()</code>.</li>
</ul>

<h3>Динамическая память (куча)</h3>
<p>На МК <code>malloc</code> нежелателен из-за фрагментации и непредсказуемого времени. Альтернативы:</p>
<ul>
  <li>Статическое выделение массивов нужного размера.</li>
  <li>Пул фиксированных блоков (memory pool).</li>
  <li>FreeRTOS heap_4 / heap_5 с детерминированным поведением.</li>
</ul>

<h3>Pragma и атрибуты размещения</h3>
<pre><code>// Разместить массив в CCM RAM (Core-Coupled Memory, 0 wait states)
uint8_t fastBuf[1024] __attribute__((section(".ccmram")));

// Разместить функцию в RAM (работает при программировании Flash)
void __attribute__((section(".RamFunc"))) FlashErase(void) { ... }
</code></pre>''',
    },
    {
        'order': 5,
        'title': 'Внешняя память: SDRAM, SPI Flash, NAND',
        'content': '''<h2>Внешняя память: SDRAM, SPI Flash, NAND</h2>
<p>Когда встроенной памяти МК недостаточно, подключают внешние микросхемы. STM32F4/F7/H7 имеют контроллер FMC/FSMC для прямого подключения SDRAM и NOR Flash.</p>

<h3>SDRAM через FMC (STM32H7)</h3>
<pre><code>// Инициализация FMC SDRAM Bank 1
FMC_SDRAM_InitTypeDef sdram = {
  .SDBank            = FMC_SDRAM_BANK1,
  .ColumnBitsNumber  = FMC_SDRAM_COLUMN_BITS_NUM_8,
  .RowBitsNumber     = FMC_SDRAM_ROW_BITS_NUM_12,
  .MemoryDataWidth   = FMC_SDRAM_MEM_BUS_WIDTH_16,
  .InternalBankNumber= FMC_SDRAM_INTERN_BANKS_NUM_4,
  .CASLatency        = FMC_SDRAM_CAS_LATENCY_3,
  .SDClockPeriod     = FMC_SDRAM_CLOCK_PERIOD_2,
  .ReadBurst         = FMC_SDRAM_RBURST_ENABLE,
};
HAL_SDRAM_Init(&hsdram1, &sdram_timing);
</code></pre>
<p>После инициализации SDRAM отображается в адресное пространство (0xC000 0000). Компилятор видит её как обычный RAM.</p>

<h3>SPI Flash (W25Q, IS25)</h3>
<p>Подключается по SPI, используется для хранения файловой системы (FAT, LittleFS) и OTA-обновлений.</p>
<pre><code>// Чтение из W25Q64 (8 МБ)
void W25Q_Read(uint32_t addr, uint8_t *buf, uint32_t len) {
    CS_LOW();
    SPI_Transfer(0x03);          // Read command
    SPI_Transfer(addr >> 16);
    SPI_Transfer(addr >> 8);
    SPI_Transfer(addr);
    for (uint32_t i = 0; i < len; i++)
        buf[i] = SPI_Transfer(0xFF);
    CS_HIGH();
}
</code></pre>

<h3>NAND Flash и файловые системы</h3>
<ul>
  <li>NAND дешевле, плотнее NOR, но нет прямого исполнения кода (XIP).</li>
  <li>Требует контроллера ECC и управления wear-leveling.</li>
  <li><strong>LittleFS</strong> — отказоустойчивая файловая система для Flash, встроена в Mbed/ESP-IDF.</li>
  <li><strong>FatFS</strong> — FAT12/16/32, порт для МК (Elm Chan), без wear-leveling.</li>
</ul>

<h3>Сравнение интерфейсов внешней памяти</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Интерфейс</th><th>Скорость</th><th>Применение</th></tr>
  <tr><td>SPI</td><td>до 133 МГц (QSPI)</td><td>Flash, EEPROM, дисплеи</td></tr>
  <tr><td>SDIO / SDMMC</td><td>до 208 МГц</td><td>SD-карты</td></tr>
  <tr><td>FMC (параллельный)</td><td>до 100 МГц × 16/32 бит</td><td>SDRAM, SRAM, NOR Flash</td></tr>
  <tr><td>HyperBus</td><td>до 800 МБ/с</td><td>HyperRAM, HyperFlash</td></tr>
</table>''',
    },
    {
        'order': 6,
        'title': 'Защита памяти: MPU и безопасность МПС',
        'content': '''<h2>Защита памяти: MPU и безопасность МПС</h2>
<p>Memory Protection Unit (MPU) — аппаратный модуль ARM Cortex-M3/M4/M7/M33. Разделяет адресное пространство на регионы с разными правами доступа.</p>

<h3>Зачем нужен MPU</h3>
<ul>
  <li>Изолирует задачи RTOS: одна задача не перезапишет стек другой.</li>
  <li>Защищает системный стек от переполнения (Stack Guard Region).</li>
  <li>Запрещает выполнение кода из RAM (XN — eXecute Never).</li>
  <li>Разграничивает привилегированный и непривилегированный режимы.</li>
</ul>

<h3>Настройка MPU (HAL)</h3>
<pre><code>MPU_Region_InitTypeDef reg = {0};

HAL_MPU_Disable();

// Регион 0: Flash — только чтение и выполнение
reg.Enable           = MPU_REGION_ENABLE;
reg.Number           = MPU_REGION_NUMBER0;
reg.BaseAddress      = 0x08000000;
reg.Size             = MPU_REGION_SIZE_256KB;
reg.AccessPermission = MPU_REGION_PRIV_RO_URO;
reg.IsBufferable     = MPU_ACCESS_NOT_BUFFERABLE;
reg.IsCacheable      = MPU_ACCESS_CACHEABLE;
reg.IsShareable      = MPU_ACCESS_NOT_SHAREABLE;
reg.DisableExec      = MPU_INSTRUCTION_ACCESS_ENABLE;
HAL_MPU_ConfigRegion(&reg);

// Регион 1: Stack Guard — запрет записи у дна стека
reg.Number           = MPU_REGION_NUMBER1;
reg.BaseAddress      = 0x20000000;  // дно стека
reg.Size             = MPU_REGION_SIZE_32B;
reg.AccessPermission = MPU_REGION_NO_ACCESS;
reg.DisableExec      = MPU_INSTRUCTION_ACCESS_DISABLE;
HAL_MPU_ConfigRegion(&reg);

HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);
</code></pre>

<h3>Ограничения MPU Cortex-M</h3>
<ul>
  <li>8 регионов (Cortex-M3/M4), 16 регионов (M7/M33).</li>
  <li>Размер региона — степень двойки, минимум 32 байта.</li>
  <li>Адрес начала — кратен размеру.</li>
  <li>Нет виртуальной памяти — только физическая защита.</li>
</ul>

<h3>TrustZone (ARMv8-M, Cortex-M33)</h3>
<p>Расширение безопасности: два мира — Secure и Non-Secure. Безопасный мир хранит ключи, крипто-операции и критический код. Несекурный мир — пользовательское приложение. Переход через специальные инструкции SG (Secure Gateway).</p>

<pre><code>// Вызов функции из безопасного мира
// Определена в Secure-partition как NSC (Non-Secure Callable)
extern int32_t Secure_AES_Encrypt(uint8_t *in, uint8_t *out, uint32_t len);

// Вызывается из Non-Secure кода как обычная функция
int result = Secure_AES_Encrypt(plaintext, ciphertext, 16);
</code></pre>

<div class="tip">STM32L5 и STM32U5 — первые серийные МК ST с TrustZone. Идеальны для IoT-устройств с требованиями PSA Certified.</div>''',
    },
]

M21_LESSONS = [
    {
        'order': 1,
        'title': 'STM32: архитектура, шины и тактирование',
        'content': '''<h2>STM32: архитектура, шины и тактирование</h2>
<p>STM32 — семейство 32-битных МК компании ST Microelectronics на ядре ARM Cortex-M. Наиболее распространены серии F1/F4/F7/G0/L4/H7.</p>

<h3>Внутренняя шинная архитектура</h3>
<p>Cortex-M4 (STM32F4) использует многоуровневую матрицу шин:</p>
<pre><code>AHB Matrix (Advanced High-performance Bus)
  ├─ ICode Bus  — чтение инструкций из Flash
  ├─ DCode Bus  — чтение данных из Flash
  ├─ System Bus — ОЗУ, периферия AHB
  │     ├─ AHB1: GPIO, DMA, USB_OTG, Ethernet
  │     ├─ AHB2: USB_FS, DCMI, RNG, AES
  │     └─ AHB3: FMC (внешняя память)
  └─ APB bridges
        ├─ APB1 (до 42 МГц): UART2-5, SPI2-3, I2C, TIM2-14, CAN
        └─ APB2 (до 84 МГц): USART1/6, SPI1, TIM1/8, ADC, SDIO
</code></pre>

<h3>Тактирование (Clock Tree)</h3>
<p>Источники тактовой частоты:</p>
<ul>
  <li><strong>HSI</strong> — внутренний RC 8/16 МГц, ±1%, запускается при включении.</li>
  <li><strong>HSE</strong> — внешний кварц 4–26 МГц, точнее HSI.</li>
  <li><strong>PLL</strong> — умножитель частоты от HSI/HSE. STM32F4: до 168 МГц SYSCLK.</li>
  <li><strong>LSI</strong> — низкочастотный 32 кГц (IWDG, RTC).</li>
  <li><strong>LSE</strong> — кварц 32768 Гц (RTC).</li>
</ul>

<h3>Настройка PLL (STM32F4, 168 МГц)</h3>
<pre><code>// В CubeMX генерируется SystemClock_Config():
RCC_OscInitTypeDef osc = {0};
osc.OscillatorType = RCC_OSCILLATORTYPE_HSE;
osc.HSEState       = RCC_HSE_ON;
osc.PLL.PLLState   = RCC_PLL_ON;
osc.PLL.PLLSource  = RCC_PLLSOURCE_HSE;
osc.PLL.PLLM       = 8;    // HSE 8 МГц / 8 = 1 МГц VCO input
osc.PLL.PLLN       = 336;  // × 336 = 336 МГц VCO output
osc.PLL.PLLP       = RCC_PLLP_DIV2; // / 2 = 168 МГц SYSCLK
osc.PLL.PLLQ       = 7;    // 48 МГц USB
HAL_RCC_OscConfig(&osc);

RCC_ClkInitTypeDef clk = {0};
clk.ClockType      = RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_HCLK |
                     RCC_CLOCKTYPE_PCLK1  | RCC_CLOCKTYPE_PCLK2;
clk.SYSCLKSource   = RCC_SYSCLKSOURCE_PLLCLK;
clk.AHBCLKDivider  = RCC_SYSCLK_DIV1;   // AHB  = 168 МГц
clk.APB1CLKDivider = RCC_HCLK_DIV4;     // APB1 =  42 МГц
clk.APB2CLKDivider = RCC_HCLK_DIV2;     // APB2 =  84 МГц
HAL_RCC_ClockConfig(&clk, FLASH_LATENCY_5);
</code></pre>

<h3>RCC и включение периферии</h3>
<pre><code>// Обязательно включить тактирование перед обращением к периферии
__HAL_RCC_GPIOA_CLK_ENABLE();
__HAL_RCC_USART1_CLK_ENABLE();
__HAL_RCC_DMA2_CLK_ENABLE();
</code></pre>
<div class="tip">Если периферия не тактируется — чтение её регистров даёт 0 или HardFault. Первое что проверять при отладке.</div>''',
    },
    {
        'order': 2,
        'title': 'GPIO: режимы, прерывания EXTI, настройка',
        'content': '''<h2>GPIO: режимы, прерывания EXTI, настройка</h2>
<p>GPIO (General Purpose Input/Output) — универсальные порты ввода-вывода. Каждый вывод МК может работать в нескольких режимах.</p>

<h3>Режимы GPIO STM32</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Режим</th><th>Описание</th><th>Применение</th></tr>
  <tr><td>Input Floating</td><td>Вход без подтяжки</td><td>Когда нагрузка задаёт уровень</td></tr>
  <tr><td>Input Pull-Up/Down</td><td>Вход с программной подтяжкой</td><td>Кнопки, I²C SCL/SDA</td></tr>
  <tr><td>Output Push-Pull</td><td>Активный 0/1</td><td>LED, сигналы управления</td></tr>
  <tr><td>Output Open-Drain</td><td>Активный только 0, 1 — через внешний резистор</td><td>I²C, шины с несколькими ведущими</td></tr>
  <tr><td>Alternate Function</td><td>Управление периферией (UART, SPI, TIM)</td><td>Любая периферия</td></tr>
  <tr><td>Analog</td><td>Аналоговый вход/выход</td><td>ADC, DAC</td></tr>
</table>

<h3>Настройка GPIO (HAL)</h3>
<pre><code>GPIO_InitTypeDef gpio = {0};

// LED на PA5 (Output Push-Pull)
__HAL_RCC_GPIOA_CLK_ENABLE();
gpio.Pin   = GPIO_PIN_5;
gpio.Mode  = GPIO_MODE_OUTPUT_PP;
gpio.Speed = GPIO_SPEED_FREQ_LOW;
HAL_GPIO_Init(GPIOA, &gpio);

// Кнопка PC13 с подтяжкой и прерыванием по фронту
__HAL_RCC_GPIOC_CLK_ENABLE();
gpio.Pin  = GPIO_PIN_13;
gpio.Mode = GPIO_MODE_IT_FALLING;   // прерывание по спаду
gpio.Pull = GPIO_PULLUP;
HAL_GPIO_Init(GPIOC, &gpio);

// Включить прерывание EXTI15_10 (PC13 → EXTI13)
HAL_NVIC_SetPriority(EXTI15_10_IRQn, 0, 0);
HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
</code></pre>

<h3>Обработчик EXTI</h3>
<pre><code>void EXTI15_10_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);
}

// Callback вызывается из HAL_GPIO_EXTI_IRQHandler
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_13) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}
</code></pre>

<h3>Прямое управление регистрами (без HAL)</h3>
<pre><code>// Быстрее HAL, используется в критических участках
GPIOA->BSRR = GPIO_PIN_5;          // Установить PA5
GPIOA->BSRR = GPIO_PIN_5 << 16;   // Сбросить PA5

uint8_t state = (GPIOC->IDR & GPIO_PIN_13) ? 1 : 0;
</code></pre>

<h3>Скорость GPIO и EMC</h3>
<p>Высокая скорость переключения (Very High Speed) даёт крутые фронты → паразитные выбросы. Для неответственных сигналов выбирают Low или Medium speed. Для SPI/USB — High или Very High.</p>''',
    },
    {
        'order': 3,
        'title': 'Таймеры STM32: базовые, общего назначения, PWM',
        'content': '''<h2>Таймеры STM32: базовые, общего назначения, PWM</h2>
<p>STM32 имеет до 17 таймеров. Категории: базовые (TIM6/7), общего назначения (TIM2–5, TIM9–14), расширенные (TIM1/8).</p>

<h3>Классификация таймеров</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Тип</th><th>Таймеры</th><th>Каналов</th><th>Особенности</th></tr>
  <tr><td>Базовые</td><td>TIM6, TIM7</td><td>0</td><td>Только счётчик + прерывание + DMA</td></tr>
  <tr><td>Общего назначения</td><td>TIM2–5</td><td>4</td><td>Capture/Compare, PWM, Encoder</td></tr>
  <tr><td>Расширенные</td><td>TIM1, TIM8</td><td>4+1</td><td>Дополнительно: Dead-Time, Break, 3-phase PWM</td></tr>
  <tr><td>Мало каналов</td><td>TIM9–14</td><td>1–2</td><td>Упрощённые, потребление меньше</td></tr>
</table>

<h3>Счётчик и делители частоты</h3>
<pre><code>// TIM2, APB1 = 42 МГц, при AHB/APB1=4 → TIM clock = 84 МГц
// PSC=8399, ARR=9999 → 84 МГц / (8400 × 10000) = 1 Гц
TIM_HandleTypeDef htim2;
htim2.Instance           = TIM2;
htim2.Init.Prescaler     = 8399;
htim2.Init.CounterMode   = TIM_COUNTERMODE_UP;
htim2.Init.Period        = 9999;
htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
HAL_TIM_Base_Init(&htim2);
HAL_TIM_Base_Start_IT(&htim2);   // запуск с прерыванием
</code></pre>

<h3>PWM — широтно-импульсная модуляция</h3>
<pre><code>// TIM3 CH1 (PA6) PWM, 1 кГц, 50% duty
TIM_OC_InitTypeDef oc = {0};
oc.OCMode       = TIM_OCMODE_PWM1;
oc.Pulse        = 4999;   // CCR = ARR/2 → 50%
oc.OCPolarity   = TIM_OCPOLARITY_HIGH;
HAL_TIM_PWM_ConfigChannel(&htim3, &oc, TIM_CHANNEL_1);
HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);

// Плавное изменение яркости LED
for (uint32_t i = 0; i <= 9999; i++) {
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, i);
    HAL_Delay(1);
}
</code></pre>

<h3>Input Capture — измерение частоты / ширины импульса</h3>
<pre><code>// TIM4 CH1 (PB6) — измерить период входного сигнала
TIM_IC_InitTypeDef ic = {0};
ic.ICPolarity  = TIM_ICPOLARITY_RISING;
ic.ICSelection = TIM_ICSELECTION_DIRECTTI;
ic.ICPrescaler = TIM_ICPSC_DIV1;
HAL_TIM_IC_ConfigChannel(&htim4, &ic, TIM_CHANNEL_1);
HAL_TIM_IC_Start_IT(&htim4, TIM_CHANNEL_1);

// В callback:
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
    static uint32_t prev = 0;
    uint32_t curr = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
    uint32_t period = curr - prev;   // в тактах таймера
    prev = curr;
    freq_hz = HAL_RCC_GetPCLK1Freq() * 2 / period;
}
</code></pre>

<div class="tip">TIM2 и TIM5 на STM32F4 — 32-битные. TIM3/4 — 16-битные. Учитывай при измерении длинных периодов.</div>''',
    },
    {
        'order': 4,
        'title': 'ADC и DAC в STM32: режимы, DMA, калибровка',
        'content': '''<h2>ADC и DAC в STM32: режимы, DMA, калибровка</h2>
<p>ADC (Analog-to-Digital Converter) преобразует аналоговый сигнал в цифровой код. STM32F4 имеет до трёх 12-битных АЦП с частотой до 2,4 МГц каждый.</p>

<h3>Параметры ADC STM32F4</h3>
<ul>
  <li>Разрядность: 6, 8, 10 или 12 бит (выбирается программно).</li>
  <li>Опорное напряжение: VREF+ (обычно 3,3 В).</li>
  <li>Время преобразования = время выборки + 12 тактов ADC (12-bit).</li>
  <li>Максимальная частота ADC: 36 МГц (F4).</li>
  <li>До 19 каналов (16 внешних + VBAT, VREFINT, температурный датчик).</li>
</ul>

<h3>Одиночное преобразование (опрос)</h3>
<pre><code>ADC_HandleTypeDef hadc1;
hadc1.Instance                   = ADC1;
hadc1.Init.Resolution            = ADC_RESOLUTION_12B;
hadc1.Init.ScanConvMode          = DISABLE;
hadc1.Init.ContinuousConvMode    = DISABLE;
hadc1.Init.EOCSelection          = ADC_EOC_SINGLE_CONV;
HAL_ADC_Init(&hadc1);

ADC_ChannelConfTypeDef ch = {0};
ch.Channel      = ADC_CHANNEL_1;  // PA1
ch.Rank         = 1;
ch.SamplingTime = ADC_SAMPLETIME_84CYCLES;
HAL_ADC_ConfigChannel(&hadc1, &ch);

HAL_ADC_Start(&hadc1);
HAL_ADC_PollForConversion(&hadc1, 10);
uint32_t raw = HAL_ADC_GetValue(&hadc1);
float voltage = raw * 3.3f / 4095.0f;
</code></pre>

<h3>ADC + DMA (непрерывный режим)</h3>
<pre><code>uint16_t adcBuf[256];  // буфер DMA

// Настройка: ContinuousConvMode = ENABLE, DMA = ENABLE
HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adcBuf, 256);

// Callback при заполнении половины/всего буфера
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *hadc) {
    // обработать adcBuf[128..255]
}
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef *hadc) {
    // обработать adcBuf[0..127]
}
</code></pre>

<h3>DAC STM32</h3>
<pre><code>// 12-bit DAC, канал 1 (PA4)
DAC_HandleTypeDef hdac;
HAL_DAC_Init(&hdac);
DAC_ChannelConfTypeDef dch = {.DAC_Trigger = DAC_TRIGGER_NONE,
                               .DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE};
HAL_DAC_ConfigChannel(&hdac, &dch, DAC_CHANNEL_1);
HAL_DAC_Start(&hdac, DAC_CHANNEL_1);

// Синусоида из таблицы 256 отсчётов
HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, sineTable[i]);
</code></pre>

<h3>Калибровка ADC и смещение нуля</h3>
<p>STM32 ADC имеет внутренний отсчёт VREFINT (1,21 В типично). Используй его для компенсации нестабильности питания:</p>
<pre><code>uint32_t vrefint = readChannel(ADC_CHANNEL_VREFINT);
float vdda = 3.3f * (*VREFINT_CAL_ADDR) / vrefint;
// Теперь vdda точнее, чем предположение 3,3 В
float voltage = raw * vdda / 4095.0f;
</code></pre>''',
    },
    {
        'order': 5,
        'title': 'DMA: принципы, режимы, связь с периферией',
        'content': '''<h2>DMA: принципы, режимы, связь с периферией</h2>
<p>DMA (Direct Memory Access) — аппаратный модуль для передачи данных между памятью и периферией без участия ЦП. Критически важен для высокоскоростных интерфейсов.</p>

<h3>Зачем DMA</h3>
<ul>
  <li>Без DMA: CPU читает байт из UART → пишет в RAM → ждёт следующий байт. CPU занят.</li>
  <li>С DMA: CPU запускает передачу, DMA делает всё сам → CPU свободен для вычислений.</li>
  <li>Пропускная способность DMA ≈ пропускная способность шины (не зависит от частоты CPU).</li>
</ul>

<h3>Потоки DMA STM32F4</h3>
<p>DMA1/DMA2 имеют по 8 потоков (stream), каждый — до 8 каналов запроса. Таблица назначений в Reference Manual, раздел DMA.</p>
<pre><code>// Пример: USART1_RX → DMA2, Stream 2, Channel 4
DMA_HandleTypeDef hdma_usart1_rx;
hdma_usart1_rx.Instance                 = DMA2_Stream2;
hdma_usart1_rx.Init.Channel             = DMA_CHANNEL_4;
hdma_usart1_rx.Init.Direction           = DMA_PERIPH_TO_MEMORY;
hdma_usart1_rx.Init.PeriphInc           = DMA_PINC_DISABLE;
hdma_usart1_rx.Init.MemInc              = DMA_MINC_ENABLE;
hdma_usart1_rx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
hdma_usart1_rx.Init.MemDataAlignment    = DMA_MDATAALIGN_BYTE;
hdma_usart1_rx.Init.Mode                = DMA_CIRCULAR;
hdma_usart1_rx.Init.Priority            = DMA_PRIORITY_HIGH;
hdma_usart1_rx.Init.FIFOMode            = DMA_FIFOMODE_DISABLE;
HAL_DMA_Init(&hdma_usart1_rx);
__HAL_LINKDMA(&huart1, hdmarx, hdma_usart1_rx);
</code></pre>

<h3>Режимы DMA</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Режим</th><th>Описание</th></tr>
  <tr><td>Normal</td><td>Одна передача, затем стоп. Перезапуск вручную.</td></tr>
  <tr><td>Circular</td><td>Непрерывная циклическая передача (поток АЦП, аудио).</td></tr>
  <tr><td>Double Buffer</td><td>Два буфера, переключение автоматически. Нет пропуска данных.</td></tr>
</table>

<h3>IDLE-прерывание UART + DMA</h3>
<p>Стандартный паттерн приёма пакетов переменной длины:</p>
<pre><code>// DMA в Circular режиме; IDLE прерывание при паузе на линии
HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rxBuf, sizeof(rxBuf));

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *h, uint16_t size) {
    // size — количество принятых байт
    processPacket(rxBuf, size);
    // DMA продолжает приём автоматически (circular)
}
</code></pre>

<div class="tip">Всегда проверяй: нужны ли операции SCB_CleanDCache / SCB_InvalidateDCache перед/после DMA на Cortex-M7 (кэш может расходиться с памятью).</div>''',
    },
    {
        'order': 6,
        'title': 'Watchdog, Low Power режимы и управление питанием',
        'content': '''<h2>Watchdog, Low Power режимы и управление питанием</h2>
<p>Надёжность встраиваемых систем требует защиты от зависания (watchdog) и экономии энергии (low power). Оба аспекта важны для промышленных и IoT-устройств.</p>

<h3>IWDG — Independent Watchdog</h3>
<p>Тактируется от LSI (~32 кГц), работает даже в режиме сна. Независим от основного тактирования.</p>
<pre><code>IWDG_HandleTypeDef hiwdg;
hiwdg.Instance       = IWDG;
hiwdg.Init.Prescaler = IWDG_PRESCALER_64;  // 32 кГц / 64 = 500 Гц
hiwdg.Init.Reload    = 500;                // 500 / 500 Гц = 1 с
HAL_IWDG_Init(&hiwdg);

// В главном цикле: сбросить счётчик до истечения таймаута
HAL_IWDG_Refresh(&hiwdg);
</code></pre>
<p>Если за 1 с не вызвать Refresh — МК перезагрузится. Обнаружить перезагрузку: <code>__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST)</code>.</p>

<h3>WWDG — Window Watchdog</h3>
<p>Сброс должен произойти в определённом временном окне — слишком рано или слишком поздно вызывает сброс. Обнаруживает «слишком быстрое» выполнение (петли зависания).</p>

<h3>Low Power режимы STM32</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Режим</th><th>CPU</th><th>Периферия</th><th>Ток (типично)</th><th>Выход</th></tr>
  <tr><td>Run</td><td>Работает</td><td>Работает</td><td>10–100 мА</td><td>—</td></tr>
  <tr><td>Sleep</td><td>Стоп</td><td>Работает</td><td>1–10 мА</td><td>Любое прерывание</td></tr>
  <tr><td>Stop 0/1/2</td><td>Стоп</td><td>Частично</td><td>1–100 мкА</td><td>EXTI, LPUART, RTC</td></tr>
  <tr><td>Standby</td><td>Стоп</td><td>Выключена</td><td>1–5 мкА</td><td>WKUP пин, RTC</td></tr>
  <tr><td>Shutdown</td><td>Стоп</td><td>Выключена</td><td>~50 нА</td><td>WKUP пин</td></tr>
</table>

<h3>Переход в Sleep и Stop</h3>
<pre><code>// Sleep mode: CPU останавливается, периферия работает
HAL_PWR_EnableSleepOnExit();  // вернуться в sleep после обработки прерывания
HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);

// Stop 2 mode (STM32L4): потребление ~2 мкА
HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
// После выхода из Stop 2 — переконфигурировать тактирование!
SystemClock_Config();
</code></pre>

<h3>Рекомендации по экономии энергии</h3>
<ul>
  <li>Отключай ненужные тактовые домены (<code>__HAL_RCC_GPIOB_CLK_DISABLE()</code>).</li>
  <li>Используй DMA вместо опроса — CPU спит между прерываниями.</li>
  <li>Выбирай минимальную рабочую частоту (динамическое масштабирование DVFS).</li>
  <li>Снижай опорное напряжение (VOS) на STM32L-серии при низких частотах.</li>
</ul>''',
    },
]

M22_LESSONS = [
    {
        'order': 1,
        'title': 'Язык Си для МК: особенности, типы данных, volatile',
        'content': '''<h2>Язык Си для МК: особенности, типы данных, volatile</h2>
<p>Программирование МК на Си отличается от прикладного. Аппаратный контекст требует точного контроля над типами, выравниванием и оптимизацией компилятора.</p>

<h3>Точные типы (stdint.h)</h3>
<pre><code>#include &lt;stdint.h&gt;

uint8_t  byte  = 0xFF;       //  8 бит, без знака
int16_t  temp  = -200;       // 16 бит, со знаком
uint32_t tick  = 0;          // 32 бит, без знака — для системных счётчиков
uint64_t large = 0xDEADBEEF; // 64 бит (редко на Cortex-M0)
</code></pre>
<p>Никогда не используй <code>int</code> или <code>long</code> для регистровых полей — их размер зависит от платформы.</p>

<h3>volatile — запрет оптимизации</h3>
<pre><code>// Без volatile: компилятор может закэшировать в регистре
// Пример — бесконечный цикл ожидания флага
volatile uint32_t flag = 0;
while (flag == 0);   // без volatile → while(true) — оптимизируется!

// Регистры периферии — всегда volatile
#define GPIOA_IDR  (*((volatile uint32_t *)0x40020010))
uint8_t val = GPIOA_IDR & 0x01;
</code></pre>

<h3>Выравнивание и упаковка структур</h3>
<pre><code>// Проблема выравнивания
typedef struct {
    uint8_t  a;   // offset 0
    // 3 байта padding
    uint32_t b;   // offset 4
} Bad;   // sizeof = 8

// Упакованная структура (для парсинга протокола)
typedef struct __attribute__((packed)) {
    uint8_t  a;   // offset 0
    uint32_t b;   // offset 1 (невыровнен!)
} Packed;   // sizeof = 5
// Внимание: обращение к невыровненным полям на ARM → HardFault или медленно
</code></pre>

<h3>Битовые поля</h3>
<pre><code>typedef union {
    uint32_t reg;
    struct {
        uint32_t MODE0  : 2;
        uint32_t MODE1  : 2;
        uint32_t MODE2  : 2;
        uint32_t MODE3  : 2;
        uint32_t reserved : 24;
    } bits;
} GPIO_MODER_t;

volatile GPIO_MODER_t *MODER = (GPIO_MODER_t *)0x40020000;
MODER->bits.MODE5 = 0b01;  // PA5 → Output
</code></pre>

<h3>const и размещение в Flash</h3>
<pre><code>// Таблица синуса в Flash (экономит RAM)
const uint16_t sineTable[256] = { 2048, 2098, 2148, ... };

// Строки — тоже в .rodata (Flash)
const char *msg = "Hello UART";
</code></pre>

<div class="tip">На ARM Cortex-M невыровненный доступ к uint32_t через байтовый указатель компилируется в LDR (корректно на M3+), но на M0 — HardFault. Используй memcpy для невыровненных данных.</div>''',
    },
    {
        'order': 2,
        'title': 'Указатели, битовые операции и работа с регистрами',
        'content': '''<h2>Указатели, битовые операции и работа с регистрами</h2>
<p>В программировании МК указатели — основной инструмент доступа к аппаратуре. Битовые операции позволяют атомарно изменять отдельные поля регистров.</p>

<h3>Указатели на регистры периферии</h3>
<pre><code>// Способ 1: макрос с прямым адресом
#define RCC_AHB1ENR  (*((volatile uint32_t *)0x40023830))
RCC_AHB1ENR |= (1 << 0);   // включить тактирование GPIOA

// Способ 2: структура периферии (CMSIS)
// В stm32f4xx.h уже определено:
// #define GPIOA  ((GPIO_TypeDef *)0x40020000)
GPIOA->MODER |= (1 << 10);  // PA5 → Output (MODER5 = 01)
</code></pre>

<h3>Битовые операции — шпаргалка</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Операция</th><th>Код</th></tr>
  <tr><td>Установить бит N</td><td><code>reg |= (1u &lt;&lt; N)</code></td></tr>
  <tr><td>Сбросить бит N</td><td><code>reg &amp;= ~(1u &lt;&lt; N)</code></td></tr>
  <tr><td>Инвертировать бит N</td><td><code>reg ^= (1u &lt;&lt; N)</code></td></tr>
  <tr><td>Прочитать бит N</td><td><code>(reg &gt;&gt; N) &amp; 1</code></td></tr>
  <tr><td>Записать поле [M:N]</td><td><code>reg = (reg &amp; ~MASK) | (val &lt;&lt; N)</code></td></tr>
</table>

<h3>Работа с многобитными полями</h3>
<pre><code>// Установить MODER5 = 01 (Output), не трогая остальные биты
#define MODER5_MASK  (0x3u << 10)   // биты 11:10
#define MODER5_OUT   (0x1u << 10)

GPIOA->MODER = (GPIOA->MODER & ~MODER5_MASK) | MODER5_OUT;

// Универсальный макрос
#define WRITE_BITS(reg, mask, val)  ((reg) = ((reg) & ~(mask)) | (val))
WRITE_BITS(GPIOA->MODER, MODER5_MASK, MODER5_OUT);
</code></pre>

<h3>Bit-band (Cortex-M3/M4)</h3>
<p>Bit-band позволяет атомарно читать/писать один бит через специальное отображение:</p>
<pre><code>#define BITBAND_SRAM_BASE   0x22000000
#define BITBAND_PERIPH_BASE 0x42000000
#define BITBAND_PERIPH(addr, bit)  \
    (*(volatile uint32_t *)(BITBAND_PERIPH_BASE + \
     ((uint32_t)(addr) - 0x40000000) * 32 + (bit) * 4))

// Атомарное включение бита без операции read-modify-write
#define GPIOA_ODR  0x40020014
BITBAND_PERIPH(GPIOA_ODR, 5) = 1;   // PA5 = 1, атомарно
</code></pre>

<h3>Барьеры памяти и порядок операций</h3>
<pre><code>// После записи в регистр периферии нужна синхронизация
RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
__DSB();   // Data Synchronization Barrier — ждать завершения записи
__ISB();   // Instruction Synchronization Barrier — сбросить конвейер
// Теперь можно безопасно обращаться к GPIOA
</code></pre>''',
    },
    {
        'order': 3,
        'title': 'Прерывания в Си: обработчики, приоритеты, атомарность',
        'content': '''<h2>Прерывания в Си: обработчики, приоритеты, атомарность</h2>
<p>Прерывания — ключевой механизм реактивного программирования МК. Неправильная работа с прерываниями — источник трудноуловимых ошибок.</p>

<h3>Вектор прерываний в Си (startup)</h3>
<pre><code>// stm32f4xx_it.c — файл обработчиков прерываний
void SysTick_Handler(void) {
    HAL_IncTick();
}

void USART1_IRQHandler(void) {
    HAL_UART_IRQHandler(&huart1);
}

void TIM2_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim2);
}
</code></pre>

<h3>NVIC: приоритеты</h3>
<pre><code>// STM32 HAL использует 4 бита приоритета (0–15, меньше = выше)
HAL_NVIC_SetPriority(USART1_IRQn, 5, 0);
HAL_NVIC_EnableIRQ(USART1_IRQn);

// FreeRTOS: системные прерывания должны иметь приоритет >= configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
// Обычно 5 и выше
HAL_NVIC_SetPriority(USART1_IRQn, 6, 0);  // можно вызывать FromISR API
</code></pre>

<h3>Атомарность и гонки данных</h3>
<pre><code>// ОПАСНО: переменная изменяется в ISR и читается в main
volatile uint32_t count = 0;

void TIM2_IRQHandler(void) { count++; }

// main:
uint32_t local = count;   // несколько инструкций → не атомарно на 32-bit!
</code></pre>

<h3>Критическая секция</h3>
<pre><code>// Вариант 1: запретить все прерывания
__disable_irq();
uint32_t local = count;   // безопасно
__enable_irq();

// Вариант 2: сохранить и восстановить маску (вложимо)
uint32_t primask = __get_PRIMASK();
__disable_irq();
count = 0;
__set_PRIMASK(primask);

// Вариант 3: FreeRTOS
taskENTER_CRITICAL();
sharedData++;
taskEXIT_CRITICAL();
</code></pre>

<h3>ISR — правила написания</h3>
<ul>
  <li>Минимальный код. Тяжёлые вычисления — через флаг или очередь в main.</li>
  <li>Не вызывать HAL_Delay() — использует SysTick, блокирует при отключённых прерываниях.</li>
  <li>Не вызывать printf() — не реентерабелен.</li>
  <li>Все переменные, изменяемые в ISR, — <code>volatile</code>.</li>
  <li>Очищать флаг прерывания в начале обработчика (или доверить HAL).</li>
</ul>

<div class="tip">FreeRTOS: из ISR вызывай функции с суффиксом FromISR (xQueueSendFromISR, xSemaphoreGiveFromISR). Обычные версии блокируют — дедлок.</div>''',
    },
    {
        'order': 4,
        'title': 'Работа с UART, SPI, I2C на Си',
        'content': '''<h2>Работа с UART, SPI, I2C на Си</h2>
<p>Коммуникационные интерфейсы — основа взаимодействия МК с внешними устройствами. STM32 HAL предоставляет три уровня: опрос, прерывания и DMA.</p>

<h3>UART — базовая отправка и приём</h3>
<pre><code>// Отправка строки (блокирующий режим)
uint8_t msg[] = "Hello UART\r\n";
HAL_UART_Transmit(&huart1, msg, sizeof(msg)-1, 100);

// Приём 10 байт (блокирующий)
uint8_t buf[10];
HAL_UART_Receive(&huart1, buf, 10, 1000);

// Приём с прерыванием (неблокирующий)
HAL_UART_Receive_IT(&huart1, buf, 10);
// Callback:
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *h) {
    // buf заполнен, запуск следующего приёма
    HAL_UART_Receive_IT(h, buf, 10);
}
</code></pre>

<h3>printf через UART (retarget)</h3>
<pre><code>// syscalls.c: переопределить _write
int _write(int fd, char *data, int len) {
    HAL_UART_Transmit(&huart1, (uint8_t*)data, len, HAL_MAX_DELAY);
    return len;
}
// Теперь printf → UART
printf("Temp: %d C\r\n", temp);
</code></pre>

<h3>SPI — передача и приём</h3>
<pre><code>// SPI master: отправить и принять 4 байта одновременно
uint8_t txBuf[] = {0x9F, 0x00, 0x00, 0x00};  // команда RDID W25Q
uint8_t rxBuf[4];
HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_RESET);  // CS LOW
HAL_SPI_TransmitReceive(&hspi1, txBuf, rxBuf, 4, 100);
HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET);    // CS HIGH
// rxBuf[1..3] = JEDEC ID
</code></pre>

<h3>I2C — запись и чтение</h3>
<pre><code>// Записать 1 байт в регистр 0x20 устройства с адресом 0x68 (MPU6050)
uint8_t data[2] = {0x20, 0x01};
HAL_I2C_Master_Transmit(&hi2c1, 0x68 << 1, data, 2, 100);

// Прочитать 6 байт из регистра 0x3B (акселерометр MPU6050)
uint8_t reg = 0x3B;
uint8_t raw[6];
HAL_I2C_Master_Transmit(&hi2c1, 0x68 << 1, &reg, 1, 100);
HAL_I2C_Master_Receive(&hi2c1,  0x68 << 1, raw, 6, 100);
int16_t ax = (raw[0] << 8) | raw[1];
</code></pre>

<h3>Частые ошибки</h3>
<ul>
  <li>I2C: адрес устройства сдвигается влево на 1 (<code>addr &lt;&lt; 1</code>). HAL требует 8-битный адрес.</li>
  <li>SPI: CS управляется вручную, HAL не управляет NSS автоматически в большинстве случаев.</li>
  <li>UART: timeout = 0 → немедленный возврат с ошибкой при занятой шине.</li>
  <li>I2C: SCL/SDA требуют подтяжку 4,7 кОм к VCC, иначе нет связи.</li>
</ul>''',
    },
    {
        'order': 5,
        'title': 'FreeRTOS: задачи, очереди, мьютексы',
        'content': '''<h2>FreeRTOS: задачи, очереди, мьютексы</h2>
<p>FreeRTOS — самая популярная RTOS для МК. Встроена в STM32CubeIDE как CMSIS-RTOS v2 обёртка.</p>

<h3>Создание задач</h3>
<pre><code>#include "cmsis_os2.h"  // CMSIS-RTOS2 API поверх FreeRTOS

osThreadId_t sensorTaskHandle;
const osThreadAttr_t sensorTask_attributes = {
    .name       = "sensorTask",
    .stack_size = 256 * 4,   // 1 КБ стека
    .priority   = osPriorityNormal,
};

void sensorTask(void *arg) {
    for (;;) {
        readSensor();
        osDelay(100);   // 100 мс, не блокирует другие задачи
    }
}

// В main, после инициализации:
osKernelInitialize();
sensorTaskHandle = osThreadNew(sensorTask, NULL, &sensorTask_attributes);
osKernelStart();
// Дальше управляет планировщик FreeRTOS
</code></pre>

<h3>Очереди для передачи данных между задачами</h3>
<pre><code>osMessageQueueId_t dataQueue;
dataQueue = osMessageQueueNew(10, sizeof(SensorData_t), NULL);

// Задача-производитель
SensorData_t d = {.temp = readTemp(), .hum = readHum()};
osMessageQueuePut(dataQueue, &d, 0, osWaitForever);

// Задача-потребитель
SensorData_t received;
osMessageQueueGet(dataQueue, &received, 0, osWaitForever);
sendUART(&received);
</code></pre>

<h3>Мьютекс для защиты общего ресурса</h3>
<pre><code>osMutexId_t uartMutex = osMutexNew(NULL);

void task1(void *arg) {
    for (;;) {
        osMutexAcquire(uartMutex, osWaitForever);
        printf("Task1\r\n");
        osMutexRelease(uartMutex);
        osDelay(200);
    }
}

void task2(void *arg) {
    for (;;) {
        osMutexAcquire(uartMutex, osWaitForever);
        printf("Task2\r\n");
        osMutexRelease(uartMutex);
        osDelay(300);
    }
}
</code></pre>

<h3>Семафор для синхронизации с ISR</h3>
<pre><code>osSemaphoreId_t uartSem = osSemaphoreNew(1, 0, NULL);

void USART1_IRQHandler(void) {
    osSemaphoreRelease(uartSem);   // из ISR: "данные готовы"
}

void uartTask(void *arg) {
    for (;;) {
        osSemaphoreAcquire(uartSem, osWaitForever);  // ждать ISR
        processUART();
    }
}
</code></pre>

<div class="tip">Инверсия приоритетов: задача с низким приоритетом держит мьютекс, задача с высоким ждёт. FreeRTOS решает через Priority Inheritance — включить в FreeRTOSConfig.h: configUSE_MUTEXES=1.</div>''',
    },
    {
        'order': 6,
        'title': 'Отладочные средства: SWD, ITM, SWO, printf через RTT',
        'content': '''<h2>Отладочные средства: SWD, ITM, SWO, printf через RTT</h2>
<p>Отладка встраиваемых систем сложнее, чем ПК-разработки. Нет стандартного вывода, нет файловой системы. Специальные инструменты — основа продуктивной работы.</p>

<h3>SWD — Serial Wire Debug</h3>
<p>Двухпроводной отладочный интерфейс ARM. Заменяет JTAG. Минимальное соединение: SWDIO, SWDCLK, GND, VCC (3.3В).</p>
<ul>
  <li>Программаторы: ST-Link V2/V3 (встроен в Discovery/Nucleo), J-Link.</li>
  <li>IDE: STM32CubeIDE (GDB + OpenOCD / ST-Link GDB Server).</li>
  <li>Возможности: точки останова, пошаговое выполнение, просмотр памяти/регистров в реальном времени (Live Watch).</li>
</ul>

<h3>ITM — Instrumentation Trace Macrocell</h3>
<p>Аппаратный механизм вывода трассы через SWO-пин. Не тормозит CPU (в отличие от UART printf).</p>
<pre><code>// Отправить символ через ITM channel 0
static inline void ITM_SendChar_0(char c) {
    while (ITM->PORT[0].u32 == 0);  // ждать готовности
    ITM->PORT[0].u8 = c;
}

// Перенаправить printf через ITM
int _write(int fd, char *buf, int len) {
    for (int i = 0; i < len; i++) ITM_SendChar_0(buf[i]);
    return len;
}
</code></pre>
<p>STM32CubeIDE: Window → Show View → SWV ITM Data Console → включить Channel 0 → запустить сессию отладки.</p>

<h3>Segger RTT — Real-Time Transfer</h3>
<p>Передача данных через отладчик без UART. Нет дополнительных пинов, минимальная задержка (~1 мкс).</p>
<pre><code>#include "SEGGER_RTT.h"

// Вывод строки
SEGGER_RTT_printf(0, "Temp: %d\r\n", temp);

// Приём символа (опрос)
int c = SEGGER_RTT_GetKey();
</code></pre>
<p>Просмотр: J-Link RTT Viewer, или STM32CubeIDE с J-Link / OpenOCD + RTT. Скорость — до нескольких МБ/с.</p>

<h3>Hard Fault Debugger — расшифровка зависаний</h3>
<pre><code>// В обработчике HardFault — читаем стек и определяем адрес ошибки
void HardFault_Handler(void) {
    __asm volatile (
        "TST lr, #4      \n"
        "ITE EQ          \n"
        "MRSEQ r0, MSP   \n"
        "MRSNE r0, PSP   \n"
        "B HardFault_HandlerC \n"
    );
}

void HardFault_HandlerC(uint32_t *stack) {
    printf("PC = 0x%08lX\r\n", stack[6]);  // адрес упавшей инструкции
    printf("LR = 0x%08lX\r\n", stack[5]);
    while(1);
}
</code></pre>

<h3>Полезные инструменты</h3>
<ul>
  <li><strong>STM32CubeMonitor</strong> — мониторинг переменных в реальном времени, построение графиков без остановки МК.</li>
  <li><strong>MAP-файл</strong> (.map) — показывает размер секций, занятость Flash и RAM.</li>
  <li><code>arm-none-eabi-size firmware.elf</code> — быстрая сводка по секциям.</li>
  <li><strong>Logic Analyzer</strong> — анализ SPI/I2C/UART на уровне сигналов (Saleae, DSLOGIC).</li>
</ul>''',
    },
]


class Command(BaseCommand):
    help = 'Expand MCU modules M20, M21, M22 to 6 detailed lessons each'

    def handle(self, *args, **options):
        subject = Subject.objects.get(slug='mcu')

        for mod_order, mod_title, lessons in [
            (20, 'Организация памяти МПС', M20_LESSONS),
            (21, 'Структура и периферия МК STM32', M21_LESSONS),
            (22, 'Язык Си для МК', M22_LESSONS),
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

        self.stdout.write('Done: M20-M22 expanded')
