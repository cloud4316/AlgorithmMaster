from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson

# M1 — expand 6 existing lessons (avg was 1310 chars → target 3000+)
M1_LESSONS = [
    {'order': 1, 'title': 'Что такое встраиваемая система',
     'content': '''<h2>Что такое встраиваемая система</h2>
<p>Встраиваемая система (embedded system) — специализированная компьютерная система, встроенная в более крупное устройство и выполняющая конкретную функцию. В отличие от универсального ПК, встраиваемая система оптимизирована под одну задачу.</p>
<h3>Примеры встраиваемых систем</h3>
<ul>
  <li>Стиральная машина — МК управляет нагревом, двигателем, клапанами по программе.</li>
  <li>Автомобильный ABS — МК реагирует на датчики скорости колёс за микросекунды.</li>
  <li>Кардиостимулятор — МК с жёсткими требованиями реального времени и надёжности.</li>
  <li>Роутер — Linux на MIPS/ARM, но со специализированными задачами.</li>
  <li>Датчик температуры на шине Modbus — AVR/STM32 с одной функцией.</li>
</ul>
<h3>Отличия от ПК</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Параметр</th><th>ПК</th><th>Встраиваемая система</th></tr>
  <tr><td>Задача</td><td>Универсальная</td><td>Специализированная</td></tr>
  <tr><td>ОС</td><td>Windows/Linux</td><td>RTOS или Bare Metal</td></tr>
  <tr><td>RAM</td><td>ГБ</td><td>КБ – МБ</td></tr>
  <tr><td>Flash/ROM</td><td>ТБ (HDD/SSD)</td><td>КБ – МБ</td></tr>
  <tr><td>Интерфейс</td><td>Клавиатура, дисплей</td><td>GPIO, UART, I2C, SPI</td></tr>
  <tr><td>Питание</td><td>Сотни Вт</td><td>мкВт – Вт</td></tr>
  <tr><td>Реальное время</td><td>Не гарантировано</td><td>Часто жёсткое RT</td></tr>
</table>
<h3>Классификация по требованиям к реальному времени</h3>
<ul>
  <li><strong>Жёсткое реальное время (Hard RT)</strong> — пропуск дедлайна = катастрофа (АБС, авиация, медицина).</li>
  <li><strong>Мягкое реальное время (Soft RT)</strong> — пропуск дедлайна ухудшает качество (видео, аудио).</li>
  <li><strong>Фирменное (Firm RT)</strong> — пропуск дедлайна делает результат бесполезным (биржевые данные).</li>
</ul>
<h3>Архитектуры процессоров во встраиваемых системах</h3>
<ul>
  <li><strong>ARM Cortex-M</strong> — доминирует в рынке МК: STM32, nRF52, LPC, SAMD.</li>
  <li><strong>AVR (8-bit)</strong> — Arduino, ATmega. Прост в освоении.</li>
  <li><strong>RISC-V</strong> — открытая архитектура, быстро растёт: CH32, ESP32-C3.</li>
  <li><strong>Xtensa (ESP32)</strong> — IoT с WiFi/Bluetooth.</li>
  <li><strong>PIC (Microchip)</strong> — промышленные применения.</li>
</ul>
<div class="tip">Для изучения основ встраиваемых систем: STM32 (Cortex-M4) + STM32CubeIDE. Бесплатный инструментарий, огромная документация, плата Nucleo-F411RE стоит ~700 руб.</div>'''},
    {'order': 2, 'title': 'Инструменты разработки: компилятор и IDE',
     'content': '''<h2>Инструменты разработки: компилятор и IDE</h2>
<p>Цепочка инструментов (toolchain) для встраиваемых систем включает редактор, кросс-компилятор, компоновщик и отладчик. Понимание каждого звена позволяет решать проблемы сборки самостоятельно.</p>
<h3>Кросс-компиляция</h3>
<p>Код пишется на host-машине (x86 ПК), компилируется для target-архитектуры (ARM, AVR). Это называется кросс-компиляцией. Компилятор <strong>arm-none-eabi-gcc</strong>:</p>
<pre><code>arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -O2 -c main.c -o main.o
arm-none-eabi-gcc -T linker.ld -o firmware.elf main.o
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
arm-none-eabi-size firmware.elf
# text = Flash, data = инициализированные, bss = нулевые (RAM)</code></pre>
<h3>STM32CubeIDE</h3>
<p>Официальная IDE от ST Microelectronics. Включает:</p>
<ul>
  <li>CubeMX — конфигурация периферии через GUI, генерация кода.</li>
  <li>Eclipse + CDT — редактор с автодополнением.</li>
  <li>arm-none-eabi-gcc — компилятор GNU.</li>
  <li>OpenOCD + GDB — отладчик.</li>
  <li>SWV — трассировка через SWO пин.</li>
</ul>
<h3>Альтернативы</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>IDE</th><th>Плюсы</th><th>Минусы</th></tr>
  <tr><td>STM32CubeIDE</td><td>Бесплатно, официальная поддержка</td><td>Тяжёлый Eclipse</td></tr>
  <tr><td>VS Code + PlatformIO</td><td>Лёгкий, удобный</td><td>Настройка вручную</td></tr>
  <tr><td>Keil MDK</td><td>Лучший профилировщик</td><td>Дорогая лицензия</td></tr>
  <tr><td>IAR EWARM</td><td>Лучший компилятор ARM</td><td>Дорогая лицензия</td></tr>
</table>
<h3>Структура проекта STM32CubeIDE</h3>
<pre><code>MyProject/
├── Core/
│   ├── Inc/     # заголовки (.h)
│   └── Src/     # исходники (main.c, stm32f4xx_it.c, ...)
├── Drivers/
│   ├── CMSIS/   # стандарт ARM, не менять
│   └── STM32F4xx_HAL_Driver/  # HAL библиотека
├── MyProject.ioc   # конфигурация CubeMX
└── Makefile / .cproject</code></pre>
<h3>Типичные ошибки при сборке</h3>
<ul>
  <li><code>undefined reference to 'HAL_GPIO_Init'</code> — не включён HAL-модуль в CubeMX или не добавлен файл в сборку.</li>
  <li><code>section '.text' will not fit in region 'FLASH'</code> — прошивка не влезает. Оптимизация <code>-Os</code> или убрать лишние модули.</li>
  <li><code>HardFault_Handler</code> при запуске — неверный линкер-скрипт или повреждён стек.</li>
</ul>
<div class="tip">Всегда обновляй HAL-библиотеку через CubeMX, а не вручную. Ручная правка Drivers/ затирается при регенерации проекта.</div>'''},
    {'order': 3, 'title': 'Структура программы для МК',
     'content': '''<h2>Структура программы для МК</h2>
<p>Программа для МК на языке Си имеет специфическую структуру, отличающуюся от консольных программ. Нет функции <code>main()</code> в привычном смысле — она не возвращает управление никогда.</p>
<h3>Минимальная структура (HAL)</h3>
<pre><code>#include "stm32f4xx_hal.h"

int main(void) {
    HAL_Init();             // инициализация HAL (SysTick, NVIC приоритеты)
    SystemClock_Config();   // настройка PLL и тактирования
    GPIO_Init();            // настройка портов

    while (1) {             // бесконечный суперцикл — никогда не выходим
        doWork();
        HAL_Delay(100);
    }
    // return никогда не достигается
}</code></pre>
<h3>Последовательность запуска МК (startup)</h3>
<ol>
  <li>Reset → CPU читает MSP из вектора 0x00000000.</li>
  <li>CPU читает адрес Reset_Handler из вектора 0x00000004.</li>
  <li>Reset_Handler копирует .data из Flash в RAM, заполняет .bss нулями.</li>
  <li>Вызывает SystemInit() (настройка Flash latency).</li>
  <li>Вызывает main().</li>
</ol>
<pre><code>/* startup_stm32f411xe.s — упрощённо */
Reset_Handler:
    ldr  sp, =_estack         /* загрузить стек */
    bl   SystemInit           /* системная инициализация */
    bl   __libc_init_array    /* инициализация C++ статиков */
    bl   main                 /* вызвать main */
    b    .                    /* если main вернулась — зависнуть */</code></pre>
<h3>Модульная структура проекта</h3>
<pre><code>/* main.c — только инициализация и суперцикл */
#include "sensor.h"
#include "display.h"
#include "uart_log.h"

int main(void) {
    HAL_Init();
    SystemClock_Config();
    Sensor_Init();
    Display_Init();
    UART_Init();

    while (1) {
        float t = Sensor_Read();
        Display_ShowTemp(t);
        UART_SendJSON(t);
        HAL_Delay(1000);
    }
}</code></pre>
<h3>Паттерны главного цикла</h3>
<ul>
  <li><strong>Суперцикл</strong> — простейший. Подходит для простых задач без жёсткого RT.</li>
  <li><strong>Суперцикл + таймерные флаги</strong> — ISR ставит флаги, main их обрабатывает.</li>
  <li><strong>Событийная машина состояний</strong> — main обрабатывает очередь событий.</li>
  <li><strong>RTOS</strong> — отдельные задачи для каждой функции.</li>
</ul>
<h3>Обработка ошибок</h3>
<pre><code>void Error_Handler(void) {
    __disable_irq();           // запретить прерывания
    // Мигать LED — сигнализировать об ошибке
    while (1) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        for (volatile int i = 0; i < 1000000; i++);
    }
}
// Вызов: if (HAL_UART_Init(&huart1) != HAL_OK) Error_Handler();</code></pre>'''},
    {'order': 4, 'title': 'Регистры периферии и битовые операции',
     'content': '''<h2>Регистры периферии и битовые операции</h2>
<p>Управление аппаратурой МК происходит через регистры периферии — ячейки памяти, отображённые в адресное пространство (Memory-Mapped I/O). Каждый бит регистра имеет конкретное значение.</p>
<h3>Регистры GPIO STM32</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Регистр</th><th>Адрес (GPIOA)</th><th>Назначение</th></tr>
  <tr><td>MODER</td><td>0x40020000</td><td>Режим пина (вход/выход/AF/аналог)</td></tr>
  <tr><td>OTYPER</td><td>0x40020004</td><td>Тип выхода (push-pull / open-drain)</td></tr>
  <tr><td>OSPEEDR</td><td>0x40020008</td><td>Скорость выхода</td></tr>
  <tr><td>PUPDR</td><td>0x4002000C</td><td>Подтяжка (none/pull-up/pull-down)</td></tr>
  <tr><td>IDR</td><td>0x40020010</td><td>Входные данные (только чтение)</td></tr>
  <tr><td>ODR</td><td>0x40020014</td><td>Выходные данные</td></tr>
  <tr><td>BSRR</td><td>0x40020018</td><td>Атомарная установка/сброс</td></tr>
</table>
<h3>Прямой доступ к регистрам (без HAL)</h3>
<pre><code>// Через структуру CMSIS (уже определена в stm32f4xx.h)
// #define GPIOA  ((GPIO_TypeDef *)0x40020000)

// Включить тактирование GPIOA
RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

// PA5 → Output push-pull (MODER5 = 01)
GPIOA->MODER &= ~(3u << 10);   // сбросить биты 11:10
GPIOA->MODER |=  (1u << 10);   // установить 01

// Управление GPIO через BSRR (атомарно, один цикл)
GPIOA->BSRR = (1u << 5);          // PA5 = HIGH
GPIOA->BSRR = (1u << 5) << 16;   // PA5 = LOW</code></pre>
<h3>Битовые операции — шпаргалка</h3>
<pre><code>// Установить бит N
reg |= (1u << N);

// Сбросить бит N
reg &= ~(1u << N);

// Инвертировать бит N
reg ^= (1u << N);

// Проверить бит N
if (reg & (1u << N)) { /* бит установлен */ }

// Записать поле [M:N] значением val
uint32_t mask = ((1u << (M-N+1)) - 1) << N;
reg = (reg & ~mask) | ((val << N) & mask);</code></pre>
<h3>Работа с флагами состояния</h3>
<pre><code>// Ждать готовности SPI (флаг TXE — Tx buffer empty)
while (!(SPI1->SR & SPI_SR_TXE));
SPI1->DR = data;

// Ждать завершения передачи (BSY — busy)
while (SPI1->SR & SPI_SR_BSY);

// ВАЖНО: всегда добавляй таймаут!
uint32_t t = HAL_GetTick();
while (!(SPI1->SR & SPI_SR_TXE)) {
    if (HAL_GetTick() - t > 10) return ERR_TIMEOUT;
}</code></pre>
<div class="tip">BSRR (Bit Set/Reset Register) позволяет атомарно изменять один пин без read-modify-write, что важно в многозадачных и ISR-контекстах. Всегда предпочитай BSRR прямой работе с ODR для GPIO.</div>'''},
    {'order': 5, 'title': 'Отладка встраиваемого ПО',
     'content': '''<h2>Отладка встраиваемого ПО</h2>
<p>Отладка МК сложнее, чем прикладных программ: нет удобного вывода, ошибки зависят от аппаратного состояния, некоторые баги воспроизводятся только в определённых условиях.</p>
<h3>SWD-отладка через STM32CubeIDE</h3>
<ul>
  <li>Подключить ST-Link (встроен в Nucleo): SWDIO, SWDCLK, GND, VCC.</li>
  <li>Run → Debug → STM32 Cortex-M C/C++ Application.</li>
  <li>Точки останова: двойной клик на полях редактора.</li>
  <li>Просмотр переменных: Variables / Expressions view.</li>
  <li>Регистры периферии: SFRs view (Peripherals → добавить).</li>
  <li>Live Watch: обновление переменных без остановки программы.</li>
</ul>
<h3>Printf-отладка через UART</h3>
<pre><code>// Перенаправить printf на UART
int _write(int fd, char *data, int len) {
    HAL_UART_Transmit(&huart1, (uint8_t*)data, len, 100);
    return len;
}

// Использование
printf("[DEBUG] temp = %.2f\r\n", temp);
printf("[DEBUG] ISR count = %lu\r\n", isrCount);</code></pre>
<h3>Анализ HardFault</h3>
<pre><code>void HardFault_Handler(void) {
    // Читать регистры состояния
    volatile uint32_t hfsr = SCB->HFSR;   // причина HardFault
    volatile uint32_t cfsr = SCB->CFSR;   // тип ошибки
    volatile uint32_t bfar = SCB->BFAR;   // адрес шинной ошибки
    volatile uint32_t mmfar = SCB->MMFAR; // адрес нарушения памяти
    (void)hfsr; (void)cfsr; (void)bfar; (void)mmfar;
    // Поставить точку останова здесь и посмотреть значения
    while(1);
}</code></pre>
<h3>Типичные причины HardFault</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Причина</th><th>Симптом</th><th>Лечение</th></tr>
  <tr><td>Разыменование NULL</td><td>MMFAR = 0x00000000</td><td>Проверить указатели</td></tr>
  <tr><td>Стек переполнен</td><td>MSP вышел за _estack</td><td>Увеличить стек, MPU StackGuard</td></tr>
  <tr><td>Невыровненный доступ</td><td>CFSR.UNALIGNED=1</td><td>Использовать memcpy</td></tr>
  <tr><td>Выполнение из RAM (XN)</td><td>CFSR.IACCVIOL=1</td><td>Проверить MPU настройки</td></tr>
</table>
<h3>Watermark стека</h3>
<pre><code>// Заполнить стек паттерном при старте
extern uint32_t _sstack, _estack;
uint32_t *p = &_sstack;
while (p < &_estack) *p++ = 0xDEADDEAD;

// Проверить использование
uint32_t *check = &_sstack;
while (*check == 0xDEADDEAD) check++;
uint32_t usedBytes = (&_estack - check) * 4;
printf("Stack used: %lu bytes\r\n", usedBytes);</code></pre>
<div class="tip">Золотое правило: первым делом при зависании — проверить не переполнен ли стек. Второй шаг — убедиться, что все тактирования включены (RCC_CLK_ENABLE).</div>'''},
    {'order': 6, 'title': 'Язык C для встраиваемых систем',
     'content': '''<h2>Язык C для встраиваемых систем</h2>
<p>Программирование МК на языке C имеет существенные отличия от прикладного программирования. Понимание этих особенностей предотвращает трудноуловимые ошибки.</p>
<h3>Точные типы данных</h3>
<pre><code>#include &lt;stdint.h&gt;
#include &lt;stdbool.h&gt;

uint8_t  byte  = 0xFF;     // 8 бит, без знака — байт регистра
int16_t  temp  = -200;     // 16 бит, со знаком — температура
uint32_t tick  = 0;        // 32 бит — системный счётчик
bool     ready = false;    // логический тип

// НИКОГДА для регистров и коммуникации не используй:
int i;    // размер зависит от платформы (16 или 32 бит)
long l;   // аналогично</code></pre>
<h3>volatile — запрет оптимизации</h3>
<pre><code>// Переменные, изменяемые в ISR или аппаратурой
volatile uint32_t sysTickCount = 0;
volatile uint8_t  uartRxReady  = 0;

// Регистры периферии — всегда volatile в CMSIS:
// typedef struct { volatile uint32_t MODER; ... } GPIO_TypeDef;

// Без volatile: компилятор закэширует в регистре CPU
// while (flag == 0);  ← без volatile = while(true) после оптимизации
// while (flag == 0);  ← с volatile = правильный опрос</code></pre>
<h3>Атрибуты GCC для МК</h3>
<pre><code>// Разместить функцию в RAM (для работы при программировании Flash)
void __attribute__((section(".RamFunc"))) Flash_Erase(void) { ... }

// Запретить оптимизацию конкретной функции
void __attribute__((optimize("O0"))) delay_soft(uint32_t n) {
    while (n--);  // без этого GCC удалит цикл при -O2
}

// Упакованная структура (без выравнивания)
typedef struct __attribute__((packed)) {
    uint8_t  id;
    uint32_t data;   // по адресу +1, невыровнено
} Packet_t;

// Слабый символ — можно переопределить в другом файле
void __attribute__((weak)) HAL_UART_RxCpltCallback(UART_HandleTypeDef *h) {
    // реализация по умолчанию (пустая)
}</code></pre>
<h3>inline-функции vs макросы</h3>
<pre><code>// ПЛОХО: макрос без типовой безопасности
#define ABS(x) ((x) < 0 ? -(x) : (x))
int r = ABS(a++);  // a инкрементируется дважды!

// ХОРОШО: inline-функция
static inline int32_t abs32(int32_t x) { return x < 0 ? -x : x; }
int r = abs32(a++);  // безопасно</code></pre>
<h3>Управление размером кода</h3>
<pre><code>// Строки в Flash (не занимают RAM)
const char msg[] = "Hello UART";  // → секция .rodata (Flash)

// Большие константные массивы — явно в Flash
const uint16_t sinTable[256] __attribute__((section(".rodata"))) = { ... };

// Проверить размер прошивки
arm-none-eabi-size firmware.elf
#   text    data     bss
#  28064     324    2048    ← text+data ≤ Flash, data+bss ≤ RAM</code></pre>
<div class="tip">Правила встраиваемого C: используй stdint.h типы, volatile для ISR-переменных и регистров, const для данных в Flash, static для модульных переменных (скрыть от других файлов).</div>'''},
]

# M2 — expand 5 existing + add lesson 6
M2_LESSONS = [
    {'order': 1, 'title': 'NVIC и приоритеты прерываний',
     'content': '''<h2>NVIC и приоритеты прерываний</h2>
<p>NVIC (Nested Vectored Interrupt Controller) — аппаратный контроллер прерываний ARM Cortex-M. Поддерживает вложенные прерывания, векторную таблицу и гибкие приоритеты.</p>
<h3>Основные концепции</h3>
<ul>
  <li><strong>Векторная таблица</strong> — массив адресов обработчиков в начале Flash. Cortex-M4: до 240 внешних прерываний.</li>
  <li><strong>Приоритет</strong> — определяет, какое прерывание обработается первым при одновременном срабатывании. Меньше число = выше приоритет.</li>
  <li><strong>Вложенные прерывания (preemption)</strong> — ISR с высоким приоритетом прерывает ISR с низким.</li>
  <li><strong>Subpriority</strong> — порядок при одинаковом приоритете вытеснения.</li>
</ul>
<h3>STM32: 4-битные приоритеты (16 уровней)</h3>
<pre><code>// Настройка групп приоритетов (4 бита preemption, 0 бит sub)
HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);

// Настройка приоритета конкретного прерывания
HAL_NVIC_SetPriority(USART1_IRQn, 5, 0);  // preempt=5, sub=0
HAL_NVIC_EnableIRQ(USART1_IRQn);

// Критическая секция — запрет всех прерываний
__disable_irq();
shared_data++;
__enable_irq();

// Запрет конкретного прерывания
HAL_NVIC_DisableIRQ(USART1_IRQn);
// ... критическая работа ...
HAL_NVIC_EnableIRQ(USART1_IRQn);</code></pre>
<h3>FreeRTOS и NVIC</h3>
<p>FreeRTOS требует: прерывания, вызывающие API <code>FromISR</code>, должны иметь приоритет ≥ <code>configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY</code> (обычно 5). Прерывания с приоритетом 0–4 не могут вызывать FreeRTOS API — они слишком важны для системы.</p>
<pre><code>// FreeRTOSConfig.h
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY 5

// ISR с приоритетом 6 — может вызывать xQueueSendFromISR
void USART1_IRQHandler(void) {
    xQueueSendFromISR(queue, &byte, &woken);  // OK
    portYIELD_FROM_ISR(woken);
}

// ISR с приоритетом 3 — НЕ может вызывать FreeRTOS API
// Используется для критичных по времени задач (encoder)</code></pre>
<h3>Pending и активные прерывания</h3>
<pre><code>// Принудительно вызвать прерывание программно
NVIC_SetPendingIRQ(TIM2_IRQn);

// Проверить, активно ли прерывание
if (NVIC_GetActive(TIM2_IRQn)) { /* в ISR */ }

// Сбросить pending флаг (если ISR не обрабатывает)
NVIC_ClearPendingIRQ(TIM2_IRQn);</code></pre>
<div class="tip">Правило: системные прерывания SysTick, PendSV, SVCall должны иметь наинизший приоритет (15) для корректной работы FreeRTOS. HAL_Init() устанавливает SysTick приоритет 15 автоматически.</div>'''},
    {'order': 2, 'title': 'Таймеры: базовые режимы',
     'content': '''<h2>Таймеры: базовые режимы</h2>
<p>Таймеры STM32 — мощный аппаратный ресурс. Базовые режимы: счёт времени, генерация прерываний, измерение периода. STM32F4 имеет до 14 таймеров.</p>
<h3>Принцип работы счётчика</h3>
<pre><code>// Частота таймера = TIM_CLK / (PSC+1)
// Период переполнения = (ARR+1) / Частота_таймера
// Пример: TIM2, APB1=42МГц, TIM_CLK=84МГц
// PSC=8399 → 84МГц/(8400) = 10000 Гц
// ARR=9999 → 10000/10000 = 1 Гц (переполнение каждую секунду)</code></pre>
<h3>Настройка TIM2 с прерыванием 1 Гц</h3>
<pre><code>TIM_HandleTypeDef htim2;

void TIM2_Init(void) {
    __HAL_RCC_TIM2_CLK_ENABLE();

    htim2.Instance           = TIM2;
    htim2.Init.Prescaler     = 8399;    // TIM_CLK / (PSC+1) = 10 кГц
    htim2.Init.CounterMode   = TIM_COUNTERMODE_UP;
    htim2.Init.Period        = 9999;    // переполнение каждые 1 с
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_Base_Init(&htim2);

    HAL_NVIC_SetPriority(TIM2_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(TIM2_IRQn);
    HAL_TIM_Base_Start_IT(&htim2);   // запустить с прерыванием
}

void TIM2_IRQHandler(void) { HAL_TIM_IRQHandler(&htim2); }

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // мигание 1 Гц
    }
}</code></pre>
<h3>Точная задержка через таймер (не HAL_Delay)</h3>
<pre><code>// Использование SysTick напрямую для мкс-задержки
void delay_us(uint32_t us) {
    uint32_t start = DWT->CYCCNT;
    uint32_t ticks = us * (SystemCoreClock / 1000000UL);
    while ((DWT->CYCCNT - start) < ticks);
}

// Инициализация DWT (один раз в main):
CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
DWT->CYCCNT = 0;
DWT->CTRL  |= DWT_CTRL_CYCCNTENA_Msk;</code></pre>
<h3>One-pulse mode — однократный импульс</h3>
<pre><code>// TIM3: сгенерировать импульс длиной 500 мкс по команде
htim3.Init.Period = 500 - 1;   // 500 тактов при 1 МГц таймера
// В One-pulse mode таймер остановится после ARR
HAL_TIM_OnePulse_Init(&htim3, TIM_OPMODE_SINGLE);
// Запустить по триггеру:
HAL_TIM_OnePulse_Start(&htim3, TIM_CHANNEL_1);</code></pre>
<div class="tip">TIM2 и TIM5 на STM32F4 — 32-битные счётчики. Остальные — 16-битные. Для долгих интервалов (>65 мс при малом PSC) используй 32-битный таймер или увеличивай PSC.</div>'''},
    {'order': 3, 'title': 'ШИМ (PWM) на таймерах',
     'content': '''<h2>ШИМ (PWM) на таймерах</h2>
<p>PWM (Pulse-Width Modulation) — цифровое управление аналоговыми устройствами: яркость LED, скорость двигателя, нагрев. Аппаратный PWM STM32 не нагружает CPU.</p>
<h3>Принцип PWM</h3>
<pre><code>Период T = ARR+1 такт таймера
Скважность = CCR / (ARR+1) × 100%

Примеры:
  CCR=0           → 0%   (всегда LOW)
  CCR=(ARR+1)/2   → 50%  (половину периода HIGH)
  CCR=ARR+1       → 100% (всегда HIGH)</code></pre>
<h3>PWM на TIM3 CH1 (PA6), 1 кГц</h3>
<pre><code>TIM_HandleTypeDef htim3;

void PWM_Init(void) {
    __HAL_RCC_TIM3_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    GPIO_InitTypeDef gpio = {
        .Pin = GPIO_PIN_6, .Mode = GPIO_MODE_AF_PP,
        .Speed = GPIO_SPEED_FREQ_HIGH, .Alternate = GPIO_AF2_TIM3
    };
    HAL_GPIO_Init(GPIOA, &gpio);

    // TIM3_CLK=84МГц, PSC=83, ARR=999 → 84М/(84×1000)=1кГц
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 83;
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 999;
    HAL_TIM_PWM_Init(&htim3);

    TIM_OC_InitTypeDef oc = {
        .OCMode = TIM_OCMODE_PWM1,
        .Pulse = 0,  // начальная скважность 0%
        .OCPolarity = TIM_OCPOLARITY_HIGH
    };
    HAL_TIM_PWM_ConfigChannel(&htim3, &oc, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
}

// Установить скважность 0–100%
void PWM_SetDuty(uint8_t pct) {
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, pct * 10);
}</code></pre>
<h3>3-фазный PWM для BLDC (TIM1)</h3>
<p>TIM1 — расширенный таймер с поддержкой комплементарных выходов и dead-time для управления инверторами:</p>
<pre><code>// CH1/CH1N, CH2/CH2N, CH3/CH3N — три пары комплементарных каналов
// Dead-time — задержка перед включением нижнего ключа
TIM_BreakDeadTimeConfigTypeDef bdt = {
    .DeadTime = 50,   // такты таймера (~500 нс при 100 МГц)
    .BreakState = TIM_BREAK_ENABLE,
    .BreakPolarity = TIM_BREAKPOLARITY_HIGH,
};
HAL_TIMEx_ConfigBreakDeadTime(&htim1, &bdt);</code></pre>
<h3>Управление сервоприводом</h3>
<pre><code>// Сервопривод SG90: 50 Гц, импульс 1–2 мс
// PSC=1679, ARR=999 → 50 Гц
// 1 мс = 50 единиц, 1.5 мс = 75, 2 мс = 100

void Servo_Angle(uint8_t deg) {
    uint32_t ccr = 50 + deg * 50 / 180;  // 50..100
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, ccr);
}</code></pre>
<div class="tip">Измерение частоты PWM: частота = TIM_CLK / ((PSC+1) × (ARR+1)). Для нагрузки (двигатели): 1–20 кГц. Для аудио DAC: 44.1–192 кГц. Для сервоприводов: 50 Гц.</div>'''},
    {'order': 4, 'title': 'SysTick и системное время',
     'content': '''<h2>SysTick и системное время</h2>
<p>SysTick — 24-битный таймер обратного отсчёта, встроенный в ядро ARM Cortex-M. Используется как системные часы HAL и как источник тиков RTOS.</p>
<h3>SysTick в HAL</h3>
<pre><code>// HAL_Init() настраивает SysTick на 1 мс
// SysTick_Config(SystemCoreClock / 1000) → прерывание каждые 1 мс

// Обработчик SysTick (в stm32f4xx_it.c)
void SysTick_Handler(void) {
    HAL_IncTick();   // увеличивает глобальный счётчик uwTick
    // FreeRTOS: osSystickHandler() вызывается здесь же
}

// Получить текущее время в мс
uint32_t ms = HAL_GetTick();

// Задержка
HAL_Delay(100);  // ждёт 100 тиков SysTick

// Измерить время выполнения
uint32_t t0 = HAL_GetTick();
heavyFunction();
uint32_t elapsed = HAL_GetTick() - t0;
printf("Elapsed: %lu ms\r\n", elapsed);</code></pre>
<h3>Проблемы HAL_Delay в ISR</h3>
<pre><code>// НЕЛЬЗЯ вызывать HAL_Delay() в ISR!
// SysTick прерывание не может прервать другой ISR того же приоритета
// → бесконечное ожидание

void EXTI0_IRQHandler(void) {
    HAL_Delay(10);   // ЗАВИСНЕТ — SysTick не выполняется
}

// ПРАВИЛЬНО: флаг + обработка в main
volatile uint8_t btnPressed = 0;
void EXTI0_IRQHandler(void) { btnPressed = 1; }
// В main: if (btnPressed) { HAL_Delay(10); btnPressed=0; }</code></pre>
<h3>Неблокирующие задержки (программный таймер)</h3>
<pre><code>// Паттерн: сохранить время начала и проверять истечение
uint32_t ledTimer = 0;
uint8_t  ledState = 0;

void LED_Update(void) {
    if (HAL_GetTick() - ledTimer >= 500) {  // каждые 500 мс
        ledTimer = HAL_GetTick();
        ledState ^= 1;
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, ledState);
    }
}

// main:
while (1) {
    LED_Update();    // не блокирует
    UART_Update();   // не блокирует
    Sensor_Update(); // не блокирует
    // Все задачи "параллельны" без RTOS
}</code></pre>
<h3>DWT как мкс-таймер</h3>
<pre><code>// DWT->CYCCNT считает такты CPU (168 МГц на STM32F4)
// 1 мкс = 168 тактов

void delay_us(uint32_t us) {
    uint32_t start = DWT->CYCCNT;
    uint32_t cnt   = us * (SystemCoreClock / 1000000);
    while ((DWT->CYCCNT - start) < cnt);
}

// Точная задержка для 1-Wire, DHT22
delay_us(480);  // Reset pulse DS18B20</code></pre>'''},
    {'order': 5, 'title': 'DMA: передача данных без CPU',
     'content': '''<h2>DMA: передача данных без CPU</h2>
<p>DMA (Direct Memory Access) передаёт данные между периферией и памятью, пока CPU выполняет другую работу. Обязательный инструмент для ADC, UART, SPI при высоких скоростях.</p>
<h3>Зачем DMA</h3>
<pre><code>// БЕЗ DMA: CPU читает каждый байт UART → записывает в RAM
void USART1_IRQHandler(void) {
    rxBuf[rxIdx++] = USART1->DR;   // прерывание на каждый байт
}
// При 115200 Бод → 11520 прерываний/с → 11520 × ~10 тактов = 115200 тактов/с
// При 168 МГц CPU → 0.07% нагрузки (немного, но растёт с частотой)

// С DMA: одна настройка → CPU свободен
// При 1 МБит/с UART + DMA → почти 0% нагрузки CPU</code></pre>
<h3>DMA для UART Rx (кольцевой буфер)</h3>
<pre><code>uint8_t rxDMA[256];

void UART_DMA_Init(void) {
    // Настройка DMA2 Stream2 Channel4 для USART1_RX
    DMA_HandleTypeDef hdma = {
        .Instance = DMA2_Stream2,
        .Init = {
            .Channel = DMA_CHANNEL_4,
            .Direction = DMA_PERIPH_TO_MEMORY,
            .PeriphInc = DMA_PINC_DISABLE,
            .MemInc    = DMA_MINC_ENABLE,
            .PeriphDataAlignment = DMA_PDATAALIGN_BYTE,
            .MemDataAlignment    = DMA_MDATAALIGN_BYTE,
            .Mode     = DMA_CIRCULAR,   // кольцевой режим
            .Priority = DMA_PRIORITY_HIGH,
        }
    };
    HAL_DMA_Init(&hdma);
    __HAL_LINKDMA(&huart1, hdmarx, hdma);

    // Запустить приём
    HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rxDMA, sizeof(rxDMA));
}

// Callback при паузе (IDLE) или заполнении буфера
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *h, uint16_t size) {
    processData(rxDMA, size);
    // DMA продолжает автоматически (Circular mode)
}</code></pre>
<h3>DMA для ADC (непрерывный захват)</h3>
<pre><code>uint16_t adcBuf[512];

// ADC + DMA Circular: непрерывное заполнение буфера
HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adcBuf, 512);

// Обработка половины (Double Buffer в программном виде)
void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef *h) {
    processADC(adcBuf, 256);        // первые 256 готовы
}
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *h) {
    processADC(adcBuf + 256, 256);  // вторые 256 готовы
}</code></pre>
<div class="tip">Cortex-M7 (STM32H7/F7): при DMA + D-cache нужно вручную вызывать SCB_CleanDCache_by_Addr() перед DMA TX и SCB_InvalidateDCache_by_Addr() после DMA RX, иначе данные из кэша расходятся с памятью.</div>'''},
    {'order': 6, 'title': 'Внешние прерывания EXTI и события',
     'content': '''<h2>Внешние прерывания EXTI и события</h2>
<p>EXTI (External Interrupt/Event Controller) позволяет реагировать на изменение логического уровня на пинах GPIO. Это основной механизм обработки кнопок, сигналов энкодеров и внешних устройств без постоянного опроса.</p>
<h3>Линии EXTI в STM32</h3>
<p>STM32F4 имеет 23 линии EXTI. Линии 0–15 привязаны к пинам GPIO: EXTI0 → Px0, EXTI1 → Px1, ... EXTI15 → Px15. Каждая линия может быть привязана только к одному порту (PA, PB, PC...) через SYSCFG_EXTICRx.</p>
<pre><code>// Пример: кнопка PC13 → EXTI13 → IRQ EXTI15_10

void EXTI_Init(void) {
    __HAL_RCC_GPIOC_CLK_ENABLE();

    GPIO_InitTypeDef gpio = {
        .Pin  = GPIO_PIN_13,
        .Mode = GPIO_MODE_IT_FALLING,  // прерывание по спаду
        .Pull = GPIO_PULLUP,
    };
    HAL_GPIO_Init(GPIOC, &gpio);

    HAL_NVIC_SetPriority(EXTI15_10_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
}

void EXTI15_10_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);  // очищает флаг
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_13) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // переключить LED
    }
}</code></pre>
<h3>Режимы срабатывания</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Режим HAL</th><th>Описание</th><th>Применение</th></tr>
  <tr><td>GPIO_MODE_IT_RISING</td><td>Нарастающий фронт</td><td>Кнопка с нижней подтяжкой</td></tr>
  <tr><td>GPIO_MODE_IT_FALLING</td><td>Спадающий фронт</td><td>Кнопка с верхней подтяжкой</td></tr>
  <tr><td>GPIO_MODE_IT_RISING_FALLING</td><td>Оба фронта</td><td>Энкодер, любое изменение</td></tr>
  <tr><td>GPIO_MODE_EVT_RISING</td><td>Событие (не ISR)</td><td>Вывод из Sleep WFE</td></tr>
</table>
<h3>EXTI как источник пробуждения из Sleep</h3>
<pre><code>// Сконфигурировать пин как источник пробуждения
// и перевести МК в Sleep — пробудится по нажатию кнопки
GPIO_InitTypeDef gpio = {
    .Pin  = GPIO_PIN_13,
    .Mode = GPIO_MODE_IT_FALLING,
    .Pull = GPIO_PULLUP,
};
HAL_GPIO_Init(GPIOC, &gpio);

// Войти в Sleep mode
HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
// После пробуждения по EXTI — продолжить выполнение</code></pre>
<h3>Программная генерация прерывания EXTI</h3>
<pre><code>// Программно сгенерировать EXTI13
EXTI->SWIER |= EXTI_SWIER_SWIER13;
// Использование: самотестирование, события между задачами</code></pre>
<div class="tip">Каждая линия EXTI0–EXTI4 имеет свой IRQ. EXTI5–EXTI9 разделяют один IRQ (EXTI9_5_IRQn). EXTI10–EXTI15 разделяют EXTI15_10_IRQn. Всегда проверяй GPIO_Pin в callback при общем обработчике.</div>'''},
]

# M3 — expand + add lesson 6
M3_LESSONS = [
    {'order': 1, 'title': 'UART: настройка и работа через HAL',
     'content': '''<h2>UART: настройка и работа через HAL</h2>
<p>UART (Universal Asynchronous Receiver/Transmitter) — самый простой интерфейс связи МК. Асинхронный: нет тактового сигнала, стороны договариваются о скорости заранее.</p>
<h3>Параметры UART</h3>
<ul>
  <li><strong>Baud Rate</strong> — скорость в битах/с (бодах). Стандартные: 9600, 19200, 38400, 115200, 921600.</li>
  <li><strong>8N1</strong> — 8 бит данных, No parity, 1 стоп-бит. Самый распространённый формат.</li>
  <li><strong>Flow control</strong> — аппаратный (RTS/CTS) или программный (XON/XOFF).</li>
</ul>
<h3>Инициализация USART1 (PA9=TX, PA10=RX)</h3>
<pre><code>UART_HandleTypeDef huart1;

void UART1_Init(void) {
    __HAL_RCC_USART1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    GPIO_InitTypeDef gpio = {
        .Pin = GPIO_PIN_9 | GPIO_PIN_10,
        .Mode = GPIO_MODE_AF_PP,
        .Speed = GPIO_SPEED_FREQ_HIGH,
        .Alternate = GPIO_AF7_USART1
    };
    HAL_GPIO_Init(GPIOA, &gpio);

    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    HAL_UART_Init(&huart1);
}

// printf через UART (retarget _write)
int _write(int fd, char *data, int len) {
    HAL_UART_Transmit(&huart1, (uint8_t*)data, len, 100);
    return len;
}</code></pre>
<h3>Три режима работы HAL</h3>
<pre><code>// 1. Блокирующий (Polling) — ждать завершения
HAL_UART_Transmit(&huart1, buf, len, 1000);
HAL_UART_Receive(&huart1, buf, len, 1000);

// 2. С прерыванием (IT) — вернуться немедленно
HAL_UART_Transmit_IT(&huart1, buf, len);
HAL_UART_Receive_IT(&huart1, buf, len);
// Callback по завершению:
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *h) { /* TX готов */ }
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *h) { /* RX готов */ }

// 3. DMA — без участия CPU
HAL_UART_Transmit_DMA(&huart1, buf, len);
HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rxBuf, sizeof(rxBuf));</code></pre>
<h3>Простой текстовый протокол</h3>
<pre><code>void processCmd(char *cmd) {
    int val;
    if (sscanf(cmd, "SET LED %d", &val) == 1) {
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, val ? GPIO_PIN_SET : GPIO_PIN_RESET);
        printf("OK: LED=%d\r\n", val);
    } else {
        printf("ERR: unknown cmd\r\n");
    }
}</code></pre>
<div class="tip">RS-485: полудуплексная шина на основе UART. Нужен дополнительный пин DE/RE для управления направлением. Дальность до 1200 м, до 32 устройств на шине. Применяется в Modbus RTU.</div>'''},
    {'order': 2, 'title': 'SPI: быстрая синхронная передача',
     'content': '''<h2>SPI: быстрая синхронная передача</h2>
<p>SPI (Serial Peripheral Interface) — синхронный последовательный интерфейс. Скорости до 45 МБит/с на STM32F4. Используется для: Flash-памяти, дисплеев, SD-карт, АЦП.</p>
<h3>Сигналы SPI</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Сигнал</th><th>Направление</th><th>Описание</th></tr>
  <tr><td>SCK</td><td>Master → Slave</td><td>Тактовый сигнал</td></tr>
  <tr><td>MOSI</td><td>Master → Slave</td><td>Master Out Slave In</td></tr>
  <tr><td>MISO</td><td>Slave → Master</td><td>Master In Slave Out</td></tr>
  <tr><td>CS/NSS</td><td>Master → Slave</td><td>Выбор устройства (LOW=активен)</td></tr>
</table>
<h3>Режимы SPI (CPOL/CPHA)</h3>
<pre><code>// CPOL=0, CPHA=0 (Mode 0) — наиболее распространён
// CPOL=0, CPHA=1 (Mode 1)
// CPOL=1, CPHA=0 (Mode 2)
// CPOL=1, CPHA=1 (Mode 3)

hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;   // CPOL=0
hspi1.Init.CLKPhase    = SPI_PHASE_1EDGE;    // CPHA=0 → Mode 0</code></pre>
<h3>Инициализация SPI1 Master</h3>
<pre><code>SPI_HandleTypeDef hspi1;

void SPI1_Init(void) {
    __HAL_RCC_SPI1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    // PA5=SCK, PA6=MISO, PA7=MOSI, PA4=CS (GPIO Output)
    GPIO_InitTypeDef gpio = {
        .Pin = GPIO_PIN_5|GPIO_PIN_6|GPIO_PIN_7,
        .Mode = GPIO_MODE_AF_PP, .Speed = GPIO_SPEED_FREQ_HIGH,
        .Alternate = GPIO_AF5_SPI1
    };
    HAL_GPIO_Init(GPIOA, &gpio);
    gpio.Pin = GPIO_PIN_4; gpio.Mode = GPIO_MODE_OUTPUT_PP;
    HAL_GPIO_Init(GPIOA, &gpio);
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_SET);  // CS HIGH

    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
    hspi1.Init.NSS = SPI_NSS_SOFT;
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_8;  // 84/8=10.5 МГц
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
    HAL_SPI_Init(&hspi1);
}

// Транзакция SPI
void SPI_Transfer(uint8_t *tx, uint8_t *rx, uint16_t len) {
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_RESET);  // CS LOW
    HAL_SPI_TransmitReceive(&hspi1, tx, rx, len, 100);
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_SET);    // CS HIGH
}</code></pre>
<div class="tip">CS (Chip Select) не управляется автоматически HAL при NSS_SOFT — нужно делать вручную. При NSS_HARD — STM32 управляет, но нельзя иметь несколько slave-устройств. Всегда используй NSS_SOFT для гибкости.</div>'''},
    {'order': 3, 'title': 'I2C: адресная шина датчиков',
     'content': '''<h2>I2C: адресная шина датчиков</h2>
<p>I2C (Inter-Integrated Circuit) — двухпроводная шина (SDA, SCL). Поддерживает до 127 устройств на одной шине. Используется для: датчиков (BME280, MPU6050), OLED-дисплеев, EEPROM, ЦАП/АЦП.</p>
<h3>Характеристики I2C</h3>
<ul>
  <li>Standard Mode: 100 кбит/с</li>
  <li>Fast Mode: 400 кбит/с</li>
  <li>Fast Mode Plus: 1 Мбит/с</li>
  <li>Обязательны подтягивающие резисторы к VCC: 4,7 кОм (SM) или 2,2 кОм (FM)</li>
  <li>Адрес устройства — 7 бит (0x08–0x77)</li>
</ul>
<h3>Инициализация I2C1 (PB6=SCL, PB7=SDA)</h3>
<pre><code>I2C_HandleTypeDef hi2c1;

void I2C1_Init(void) {
    __HAL_RCC_I2C1_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();

    GPIO_InitTypeDef gpio = {
        .Pin = GPIO_PIN_6|GPIO_PIN_7,
        .Mode = GPIO_MODE_AF_OD,      // Open-Drain обязательно для I2C
        .Pull = GPIO_PULLUP,          // или внешние резисторы
        .Speed = GPIO_SPEED_FREQ_HIGH,
        .Alternate = GPIO_AF4_I2C1
    };
    HAL_GPIO_Init(GPIOB, &gpio);

    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 400000;   // 400 кГц
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
    hi2c1.Init.OwnAddress1 = 0;
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    HAL_I2C_Init(&hi2c1);
}

// Запись в регистр устройства
void I2C_WriteReg(uint8_t devAddr, uint8_t reg, uint8_t val) {
    uint8_t buf[2] = {reg, val};
    HAL_I2C_Master_Transmit(&hi2c1, devAddr<<1, buf, 2, 100);
}

// Чтение N байт из регистра
void I2C_ReadRegs(uint8_t devAddr, uint8_t reg, uint8_t *data, uint16_t len) {
    HAL_I2C_Master_Transmit(&hi2c1, devAddr<<1, &reg, 1, 100);
    HAL_I2C_Master_Receive(&hi2c1,  devAddr<<1, data, len, 100);
    // Или одной командой:
    // HAL_I2C_Mem_Read(&hi2c1, devAddr<<1, reg, 1, data, len, 100);
}</code></pre>
<h3>Поиск I2C устройств на шине (I2C Scanner)</h3>
<pre><code>void I2C_Scan(void) {
    printf("I2C scan:\r\n");
    for (uint8_t addr = 0x08; addr <= 0x77; addr++) {
        HAL_StatusTypeDef st = HAL_I2C_IsDeviceReady(&hi2c1, addr<<1, 1, 10);
        if (st == HAL_OK) printf("  Found: 0x%02X\r\n", addr);
    }
}</code></pre>
<div class="tip">Ошибка I2C HAL_BUSY: если шина "застряла" (SDA держится LOW устройством после сброса питания). Решение: подать 9 тактов SCL вручную (software I2C recovery), затем STOP-условие. STM32: HAL_I2C_DeInit() + переинициализация после 9 SCL тактов через GPIO.</div>'''},
    {'order': 4, 'title': 'USB и виртуальный COM-порт',
     'content': '''<h2>USB и виртуальный COM-порт</h2>
<p>USB CDC (Communication Device Class) позволяет STM32 выглядеть для ПК как виртуальный COM-порт. Драйвер встроен в Windows/Linux/macOS — дополнительная установка не нужна.</p>
<h3>Настройка USB CDC в CubeMX</h3>
<ol>
  <li>Connectivity → USB_OTG_FS → Device_Only.</li>
  <li>Middleware → USB_DEVICE → Class: CDC.</li>
  <li>Clock Configuration: убедиться, что USB Clock = 48 МГц.</li>
  <li>Generate Code.</li>
</ol>
<h3>Отправка данных через USB CDC</h3>
<pre><code>#include "usbd_cdc_if.h"

// Отправить строку
void USB_SendString(const char *str) {
    CDC_Transmit_FS((uint8_t*)str, strlen(str));
}

// printf через USB CDC
int _write(int fd, char *data, int len) {
    CDC_Transmit_FS((uint8_t*)data, len);
    HAL_Delay(1);   // дать время USB отправить
    return len;
}

// Использование
printf("Hello USB CDC!\r\n");
printf("ADC = %lu, T = %.2f C\r\n", adcRaw, temp);</code></pre>
<h3>Приём данных от ПК</h3>
<pre><code>// В usbd_cdc_if.c — callback при приёме данных
static int8_t CDC_Receive_FS(uint8_t *Buf, uint32_t *Len) {
    // Buf содержит принятые данные, Len — длину
    Buf[*Len] = '\0';
    processCommand((char*)Buf);
    USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &Buf[0]);
    USBD_CDC_ReceivePacket(&hUsbDeviceFS);
    return USBD_OK;
}</code></pre>
<h3>Настройка на стороне ПК (Python)</h3>
<pre><code>import serial
ser = serial.Serial('COM5', 115200, timeout=1)  # USB CDC обычно виден как COMx
# На Linux: /dev/ttyACM0

ser.write(b"STATUS\r\n")
response = ser.readline().decode()
print(response)</code></pre>
<h3>USB CDC vs UART: когда что выбрать</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Критерий</th><th>UART + USB-UART</th><th>USB CDC</th></tr>
  <tr><td>Дополнительные компоненты</td><td>CH340/CP2102</td><td>Нет</td></tr>
  <tr><td>Скорость</td><td>до 3 Мбод</td><td>до 12 Мбит/с (FS)</td></tr>
  <tr><td>Питание с ПК</td><td>Только через USB-адаптер</td><td>5 В прямо с USB</td></tr>
  <tr><td>Сложность</td><td>Простая</td><td>Нужна инициализация USB стека</td></tr>
</table>'''},
    {'order': 5, 'title': 'Протоколы прикладного уровня',
     'content': '''<h2>Протоколы прикладного уровня</h2>
<p>Поверх физических интерфейсов (UART, SPI, I2C) реализуются прикладные протоколы — форматы сообщений, адресации, обнаружения ошибок.</p>
<h3>JSON для IoT и отладки</h3>
<pre><code>// Формирование JSON строки (без парсера)
void sendJSON(float t, float h, uint32_t ts) {
    char buf[128];
    snprintf(buf, sizeof(buf),
        "{\"temp\":%.2f,\"hum\":%.1f,\"ts\":%lu}\r\n", t, h, ts);
    HAL_UART_Transmit(&huart1, (uint8_t*)buf, strlen(buf), 100);
}

// Парсинг простых JSON на МК (без библиотеки)
// Искать подстроку "\"val\":"
char *p = strstr(rxBuf, "\"led\":");
if (p) {
    int val = atoi(p + 6);
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, val);
}</code></pre>
<h3>Modbus RTU (промышленный стандарт)</h3>
<pre><code>// Кадр Modbus RTU: [Addr][FC][Data...][CRC_L][CRC_H]
// CRC16 Modbus
uint16_t ModbusCRC16(uint8_t *buf, uint16_t len) {
    uint16_t crc = 0xFFFF;
    while (len--) {
        crc ^= *buf++;
        for (int i = 0; i < 8; i++)
            crc = (crc & 1) ? (crc >> 1) ^ 0xA001 : crc >> 1;
    }
    return crc;
}

// Запрос чтения 2 holding registers (FC=03)
// 01 03 00 00 00 02 CRC_L CRC_H
uint8_t request[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x02};
uint16_t crc = ModbusCRC16(request, 6);
uint8_t frame[8];
memcpy(frame, request, 6);
frame[6] = crc & 0xFF;
frame[7] = crc >> 8;</code></pre>
<h3>Простой бинарный протокол с контрольной суммой</h3>
<pre><code>// Кадр: [0xAA][CMD][LEN][DATA...][XOR]
#define FRAME_START 0xAA

uint8_t calcXOR(uint8_t *buf, uint8_t len) {
    uint8_t xor = 0;
    for (uint8_t i = 0; i < len; i++) xor ^= buf[i];
    return xor;
}

void sendFrame(uint8_t cmd, uint8_t *data, uint8_t len) {
    uint8_t frame[64];
    frame[0] = FRAME_START;
    frame[1] = cmd;
    frame[2] = len;
    memcpy(frame+3, data, len);
    frame[3+len] = calcXOR(frame+1, 2+len);
    HAL_UART_Transmit(&huart1, frame, 4+len, 100);
}</code></pre>
<h3>AT-команды (GSM, WiFi модули)</h3>
<pre><code>// ESP8266/ESP32 через UART с AT-командами
void AT_Send(const char *cmd) {
    HAL_UART_Transmit(&huart1, (uint8_t*)cmd, strlen(cmd), 100);
    HAL_Delay(100);
}

AT_Send("AT\r\n");            // проверка связи → OK
AT_Send("AT+CWMODE=1\r\n");  // режим Station
AT_Send("AT+CWJAP=\"SSID\",\"pass\"\r\n");  // подключение к WiFi</code></pre>'''},
    {'order': 6, 'title': 'CAN Bus: основы промышленной сети МК',
     'content': '''<h2>CAN Bus: основы промышленной сети МК</h2>
<p>CAN (Controller Area Network) — промышленный протокол связи, разработанный Bosch для автомобилей. Используется в автомобилях, промышленной автоматике, медицинском оборудовании. Дифференциальная пара, скорость до 1 Мбит/с, до 1 км дальности.</p>
<h3>Особенности CAN</h3>
<ul>
  <li>Многоуровневый арбитраж без коллизий: узел с меньшим ID "выигрывает" шину.</li>
  <li>Широковещательная передача: все узлы получают все сообщения, фильтрация по ID.</li>
  <li>Встроенное обнаружение ошибок: CRC, bit stuffing, ACK, 5 видов error frames.</li>
  <li>STM32F4: встроенный bxCAN контроллер.</li>
</ul>
<h3>Инициализация CAN (STM32F4, 500 кбит/с)</h3>
<pre><code>CAN_HandleTypeDef hcan1;

void CAN1_Init(void) {
    __HAL_RCC_CAN1_CLK_ENABLE();
    // PA11=CAN_RX, PA12=CAN_TX (AF9)

    hcan1.Instance = CAN1;
    hcan1.Init.Mode = CAN_MODE_NORMAL;
    // 500 кбит/с при PCLK1=42МГц: Prescaler=6, BS1=7, BS2=6
    // Bit time = (1+BS1+BS2) × tq = 14tq, tq=1/(42МГц/6)=142нс
    // 14 × 142нс ≈ 2 мкс = 500 кбит/с
    hcan1.Init.Prescaler = 6;
    hcan1.Init.TimeSeg1 = CAN_BS1_7TQ;
    hcan1.Init.TimeSeg2 = CAN_BS2_6TQ;
    hcan1.Init.SJW = CAN_SJW_1TQ;
    hcan1.Init.AutoBusOff = ENABLE;
    hcan1.Init.AutoRetransmission = ENABLE;
    HAL_CAN_Init(&hcan1);

    // Фильтр — принять все сообщения (маска 0)
    CAN_FilterTypeDef f = {.FilterActivation = ENABLE,
                            .FilterMode = CAN_FILTERMODE_IDMASK,
                            .FilterScale = CAN_FILTERSCALE_32BIT,
                            .FilterIdHigh = 0, .FilterIdLow = 0,
                            .FilterMaskIdHigh = 0, .FilterMaskIdLow = 0,
                            .FilterFIFOAssignment = CAN_RX_FIFO0,
                            .FilterBank = 0};
    HAL_CAN_ConfigFilter(&hcan1, &f);
    HAL_CAN_Start(&hcan1);
    HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING);
}

// Отправка сообщения
void CAN_Send(uint32_t id, uint8_t *data, uint8_t len) {
    CAN_TxHeaderTypeDef hdr = {.StdId=id, .IDE=CAN_ID_STD,
                                .RTR=CAN_RTR_DATA, .DLC=len};
    uint32_t mailbox;
    HAL_CAN_AddTxMessage(&hcan1, &hdr, data, &mailbox);
}

// Приём
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *h) {
    CAN_RxHeaderTypeDef hdr;
    uint8_t data[8];
    HAL_CAN_GetRxMessage(h, CAN_RX_FIFO0, &hdr, data);
    // data[0..hdr.DLC-1] — принятые данные
}</code></pre>
<div class="tip">Для разработки CAN-сети без реального железа используй loopback режим: hcan1.Init.Mode = CAN_MODE_LOOPBACK. МК видит свои же сообщения — полезно для отладки протокола без второго устройства.</div>'''},
]

# M4 — expand + add lesson 6
M4_LESSONS = [
    {'order': 1, 'title': 'Введение в FreeRTOS',
     'content': '''<h2>Введение в FreeRTOS</h2>
<p>FreeRTOS — самая популярная RTOS (Real-Time Operating System) для МК. MIT-лицензия, поддержка 40+ архитектур, встроена в STM32CubeIDE как CMSIS-RTOS v2.</p>
<h3>Зачем RTOS</h3>
<ul>
  <li>Несколько независимых задач выполняются "параллельно" (вытесняющая многозадачность).</li>
  <li>Приоритеты: критичная задача (аларм) не ждёт медленной (логирование).</li>
  <li>Стандартные примитивы синхронизации: очереди, семафоры, мьютексы.</li>
  <li>Управление временем: vTaskDelay — точная задержка без блокировки других задач.</li>
</ul>
<h3>Создание задач</h3>
<pre><code>#include "FreeRTOS.h"
#include "task.h"

// Задача — функция с бесконечным циклом
void vLedTask(void *pvParams) {
    for (;;) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        vTaskDelay(pdMS_TO_TICKS(500));  // 500 мс, не блокирует другие
    }
}

void vSensorTask(void *pvParams) {
    for (;;) {
        float t = readTemperature();
        sendUART(t);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

int main(void) {
    HAL_Init(); SystemClock_Config();

    xTaskCreate(vLedTask,    "LED",    128, NULL, 1, NULL);
    xTaskCreate(vSensorTask, "Sensor", 256, NULL, 2, NULL);

    vTaskStartScheduler();  // запустить планировщик
    while(1);               // сюда не доходим
}</code></pre>
<h3>Планировщик и приоритеты</h3>
<p>FreeRTOS использует вытесняющую многозадачность с Round-Robin для одинаковых приоритетов:</p>
<ul>
  <li>Задача с наивысшим приоритетом выполняется первой.</li>
  <li>Задача блокируется (vTaskDelay, ожидание очереди) → планировщик выбирает следующую.</li>
  <li>SysTick — источник тиков планировщика (1 мс по умолчанию).</li>
</ul>
<h3>Мониторинг задач</h3>
<pre><code>// Показать состояние всех задач
void printTaskInfo(void) {
    TaskStatus_t tasks[10];
    uint32_t total;
    uint8_t n = uxTaskGetSystemState(tasks, 10, &total);
    printf("Name          State  Prio  Stack_HWM\r\n");
    for (int i = 0; i < n; i++) {
        printf("%-14s %c      %lu     %u\r\n",
            tasks[i].pcTaskName,
            "RBESD"[tasks[i].eCurrentState],
            tasks[i].uxCurrentPriority,
            tasks[i].usStackHighWaterMark);
    }
}
// HWM — High Water Mark стека. Если < 20 — стек слишком мал.</code></pre>
<div class="tip">configMINIMAL_STACK_SIZE в FreeRTOSConfig.h задаётся в СЛОВАХ (4 байта), а xTaskCreate — тоже в словах. 128 слов = 512 байт. Для задачи с printf или сложными вычислениями — минимум 256–512 слов.</div>'''},
    {'order': 2, 'title': 'Очереди и семафоры',
     'content': '''<h2>Очереди и семафоры</h2>
<p>Очереди и семафоры — основные примитивы синхронизации FreeRTOS. Обеспечивают безопасный обмен данными и синхронизацию между задачами и ISR.</p>
<h3>Очередь (Queue)</h3>
<pre><code>// Очередь хранит копии элементов (не указатели!)
// Потокобезопасна: можно писать из ISR и читать из задачи

QueueHandle_t xDataQueue;

typedef struct {
    float temperature;
    uint32_t timestamp;
} SensorData_t;

// Создать очередь на 10 элементов типа SensorData_t
xDataQueue = xQueueCreate(10, sizeof(SensorData_t));

// Задача-производитель (ISR или другая задача)
SensorData_t data = {.temperature=25.3f, .timestamp=HAL_GetTick()};
xQueueSend(xDataQueue, &data, pdMS_TO_TICKS(100));  // ждать 100 мс

// Из ISR (не блокирует):
BaseType_t woken = pdFALSE;
xQueueSendFromISR(xDataQueue, &data, &woken);
portYIELD_FROM_ISR(woken);  // переключить задачу если нужно

// Задача-потребитель
SensorData_t received;
if (xQueueReceive(xDataQueue, &received, pdMS_TO_TICKS(2000)) == pdTRUE) {
    processData(&received);
} else {
    // Таймаут — нет данных 2 с
    handleTimeout();
}</code></pre>
<h3>Семафор двоичный (Binary Semaphore)</h3>
<pre><code>// Синхронизация: ISR сигнализирует задаче о готовности данных
SemaphoreHandle_t xUartSem = xSemaphoreCreateBinary();

// В ISR:
void USART1_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    xSemaphoreGiveFromISR(xUartSem, &woken);
    portYIELD_FROM_ISR(woken);
}

// Задача ждёт сигнала от ISR:
void vUartTask(void *p) {
    for (;;) {
        xSemaphoreTake(xUartSem, portMAX_DELAY);  // ждать бесконечно
        processUART();
    }
}</code></pre>
<h3>Счётный семафор (Counting Semaphore)</h3>
<pre><code>// Для ресурсов с лимитом (например, пул буферов)
SemaphoreHandle_t xBufSem = xSemaphoreCreateCounting(5, 5);  // 5 буферов

void vProducer(void *p) {
    for (;;) {
        xSemaphoreTake(xBufSem, portMAX_DELAY);  // занять буфер
        useBuf();
        xSemaphoreGive(xBufSem);  // вернуть буфер
    }
}</code></pre>
<h3>Сравнение: очередь vs семафор</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Примитив</th><th>Для чего</th></tr>
  <tr><td>Queue</td><td>Передача данных (значения, структуры)</td></tr>
  <tr><td>Binary Semaphore</td><td>Синхронизация (уведомление без данных)</td></tr>
  <tr><td>Counting Semaphore</td><td>Управление пулом ресурсов</td></tr>
  <tr><td>Mutex</td><td>Взаимное исключение (защита общего ресурса)</td></tr>
</table>'''},
    {'order': 3, 'title': 'Управление памятью в FreeRTOS',
     'content': '''<h2>Управление памятью в FreeRTOS</h2>
<p>FreeRTOS предоставляет 5 реализаций кучи (heap_1 – heap_5) с разными компромиссами между функциональностью и безопасностью.</p>
<h3>Схемы кучи FreeRTOS</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Схема</th><th>Особенности</th><th>Применение</th></tr>
  <tr><td>heap_1</td><td>Только выделение, без освобождения</td><td>Статические системы</td></tr>
  <tr><td>heap_2</td><td>Best-fit, без объединения блоков</td><td>Фиксированные размеры</td></tr>
  <tr><td>heap_3</td><td>Обёртка над malloc/free (не потокобезопасно)</td><td>Редко</td></tr>
  <tr><td>heap_4</td><td>First-fit + объединение соседних блоков</td><td>Рекомендуется</td></tr>
  <tr><td>heap_5</td><td>heap_4 + несколько областей RAM</td><td>Сложные МК (H7)</td></tr>
</table>
<h3>Мониторинг кучи</h3>
<pre><code>// Текущий свободный размер кучи
size_t freeHeap = xPortGetFreeHeapSize();
printf("Free heap: %u bytes\r\n", freeHeap);

// Минимальный исторический свободный остаток
size_t minEver = xPortGetMinimumEverFreeHeapSize();
printf("Min ever free: %u bytes\r\n", minEver);

// FreeRTOSConfig.h:
// configTOTAL_HEAP_SIZE — общий размер кучи FreeRTOS (например, 20480)
// Куча FreeRTOS отдельна от кучи C (malloc)</code></pre>
<h3>Статическое создание задач (без кучи)</h3>
<pre><code>// Задать стек и TCB статически — нет malloc, детерминировано
static StackType_t  ledStack[128];
static StaticTask_t ledTCB;

xTaskCreateStatic(
    vLedTask, "LED", 128, NULL, 1,
    ledStack, &ledTCB   // статические буферы
);

// В FreeRTOSConfig.h включить:
// #define configSUPPORT_STATIC_ALLOCATION 1</code></pre>
<h3>Проблемы с памятью в FreeRTOS</h3>
<ul>
  <li><strong>Стек задачи мал</strong>: HWM → 0 → HardFault при переполнении. Диагностика: uxTaskGetStackHighWaterMark().</li>
  <li><strong>Куча исчерпана</strong>: xTaskCreate вернёт NULL. Всегда проверяй возврат!</li>
  <li><strong>Фрагментация</strong>: при частом create/delete задач с heap_2/heap_4. Решение: создавать задачи один раз при старте.</li>
</ul>
<pre><code>// Проверка успешного создания задачи
TaskHandle_t h = NULL;
BaseType_t r = xTaskCreate(vTask, "T", 256, NULL, 2, &h);
if (r != pdPASS || h == NULL) {
    Error_Handler();  // нет памяти!
}</code></pre>
<div class="tip">Для критических систем: configSUPPORT_STATIC_ALLOCATION=1 + создание всех задач статически. Нет dynamic malloc → нет фрагментации → детерминированное потребление памяти.</div>'''},
    {'order': 4, 'title': 'Паттерны FreeRTOS',
     'content': '''<h2>Паттерны FreeRTOS</h2>
<p>Устоявшиеся паттерны программирования FreeRTOS решают типичные задачи встраиваемых систем: реактивную обработку событий, периодические задачи, защиту общих ресурсов.</p>
<h3>Паттерн: задача-производитель / задача-потребитель</h3>
<pre><code>// Sensor → Queue → Display
// Sensor → Queue → UART Logger
// Одна очередь, несколько потребителей (каждый копирует данные)

QueueHandle_t xDisplayQ, xUARTQ;

void vSensorTask(void *p) {
    SensorData_t d;
    for (;;) {
        d.temp = readTemp(); d.ts = HAL_GetTick();
        xQueueSend(xDisplayQ, &d, 0);   // не ждать: если полна — пропустить
        xQueueSend(xUARTQ, &d, 0);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}</code></pre>
<h3>Паттерн: мьютекс для общего ресурса</h3>
<pre><code>MutexHandle_t xI2CMutex = xSemaphoreCreateMutex();

void vDisplayTask(void *p) {
    for (;;) {
        // Захватить I2C шину
        if (xSemaphoreTake(xI2CMutex, pdMS_TO_TICKS(100)) == pdTRUE) {
            LCD_Update();
            xSemaphoreGive(xI2CMutex);
        }
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void vSensorTask(void *p) {
    for (;;) {
        if (xSemaphoreTake(xI2CMutex, pdMS_TO_TICKS(100)) == pdTRUE) {
            float t = BME280_Read();  // использует I2C
            xSemaphoreGive(xI2CMutex);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}</code></pre>
<h3>Паттерн: таймер FreeRTOS (без задачи)</h3>
<pre><code>// Программный таймер — callback выполняется в Timer Task
TimerHandle_t xLedTimer;

void ledTimerCb(TimerHandle_t xTimer) {
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
}

// Создать и запустить таймер 500 мс, периодический
xLedTimer = xTimerCreate("LED", pdMS_TO_TICKS(500),
                          pdTRUE, NULL, ledTimerCb);
xTimerStart(xLedTimer, 0);</code></pre>
<h3>Паттерн: Event Group (группа событий)</h3>
<pre><code>EventGroupHandle_t xEvents = xEventGroupCreate();
#define EVT_SENSOR_READY  (1 << 0)
#define EVT_UART_DONE     (1 << 1)

// Задача ждёт несколько событий одновременно
void vProcessTask(void *p) {
    for (;;) {
        // Ждать оба события (AND)
        EventBits_t bits = xEventGroupWaitBits(
            xEvents,
            EVT_SENSOR_READY | EVT_UART_DONE,
            pdTRUE,   // очистить после выхода
            pdTRUE,   // AND (оба должны быть)
            pdMS_TO_TICKS(5000)
        );
        if (bits & (EVT_SENSOR_READY | EVT_UART_DONE)) {
            processAll();
        }
    }
}</code></pre>
<div class="tip">Инверсия приоритетов: низкоприоритетная задача держит мьютекс → высокоприоритетная ждёт → средняя вытесняет низкую → дедлайн нарушен. FreeRTOS мьютекс (не семафор) решает это через Priority Inheritance. Включить: configUSE_MUTEXES=1.</div>'''},
    {'order': 5, 'title': 'Отладка и профилирование FreeRTOS',
     'content': '''<h2>Отладка и профилирование FreeRTOS</h2>
<p>Отладка многозадачных программ сложнее однопоточных. FreeRTOS предоставляет инструменты для анализа поведения системы во время выполнения.</p>
<h3>Run-Time Stats — загрузка CPU по задачам</h3>
<pre><code>// FreeRTOSConfig.h:
#define configGENERATE_RUN_TIME_STATS          1
#define configUSE_STATS_FORMATTING_FUNCTIONS   1
#define portCONFIGURE_TIMER_FOR_RUN_TIME_STATS() init_timer_for_stats()
#define portGET_RUN_TIME_COUNTER_VALUE()        getTimerValue()

// Вывод статистики (через UART)
void printCPUStats(void) {
    char buf[512];
    vTaskGetRunTimeStats(buf);
    printf("Task\t\tAbs Time\t%%\r\n");
    printf("%s\r\n", buf);
}
// Вывод:
// IDLE            1234567    70%
// SensorTask      350000     20%
// DisplayTask     170000     10%</code></pre>
<h3>Трассировка через Percepio Tracealyzer</h3>
<p>Профессиональный инструмент для анализа поведения FreeRTOS. Записывает все события: переключения задач, очереди, прерывания. Интеграция через RTT или UART.</p>
<pre><code>// FreeRTOSConfig.h — добавить Tracealyzer
#include "trcRecorder.h"
// В main() перед vTaskStartScheduler():
xTraceEnable(TRC_START);</code></pre>
<h3>Типичные ошибки FreeRTOS и их диагностика</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Ошибка</th><th>Симптом</th><th>Диагностика</th></tr>
  <tr><td>Стек задачи переполнен</td><td>HardFault, случайные сбои</td><td>uxTaskGetStackHighWaterMark</td></tr>
  <tr><td>Дедлок мьютекса</td><td>Система зависает</td><td>Tracealyzer, watchdog</td></tr>
  <tr><td>Приоритетное голодание</td><td>Низкоприоритетная задача не работает</td><td>Run-Time Stats</td></tr>
  <tr><td>Вызов обычного API из ISR</td><td>HardFault или непредсказуемое поведение</td><td>Код-ревью, configASSERT</td></tr>
</table>
<h3>configASSERT — встроенные проверки</h3>
<pre><code>// FreeRTOSConfig.h
#define configASSERT(x) do { \
    if (!(x)) { \
        taskDISABLE_INTERRUPTS(); \
        printf("ASSERT FAILED: %s:%d\r\n", __FILE__, __LINE__); \
        while(1); \
    } \
} while(0)
// FreeRTOS использует configASSERT для проверки параметров API
// Включи в Debug-сборке — ловит большинство ошибок использования API</code></pre>
<div class="tip">Золотое правило FreeRTOS: никогда не вызывай функцию без суффикса FromISR из ISR-контекста. Даже если "кажется что работает" — это неопределённое поведение, ломающееся при обновлении FreeRTOS или изменении приоритетов.</div>'''},
    {'order': 6, 'title': 'Task Notifications и продвинутые техники FreeRTOS',
     'content': '''<h2>Task Notifications и продвинутые техники FreeRTOS</h2>
<p>Task Notifications — лёгкая альтернатива семафорам и очередям, когда данные нужно передать конкретной задаче. Не требуют отдельного объекта — уведомление встроено в Task Control Block.</p>
<h3>Task Notifications vs Semaphore</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Параметр</th><th>Semaphore</th><th>Task Notification</th></tr>
  <tr><td>Скорость</td><td>Базовая</td><td>На 45% быстрее</td></tr>
  <tr><td>RAM</td><td>Отдельный объект (~8 байт)</td><td>Часть TCB (0 доп. памяти)</td></tr>
  <tr><td>Несколько получателей</td><td>Да</td><td>Только одна задача</td></tr>
  <tr><td>Значение</td><td>Счётчик</td><td>32-битное слово</td></tr>
</table>
<h3>Использование Task Notifications</h3>
<pre><code>TaskHandle_t xProcessTask;

// В ISR: уведомить задачу о готовности данных
void USART1_IRQHandler(void) {
    BaseType_t woken = pdFALSE;
    vTaskNotifyGiveFromISR(xProcessTask, &woken);
    portYIELD_FROM_ISR(woken);
}

// Задача ждёт уведомление
void vProcessTask(void *p) {
    xProcessTask = xTaskGetCurrentTaskHandle();
    for (;;) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);  // ждать
        processUART();
    }
}

// Передать значение через уведомление
xTaskNotify(xProcessTask, receivedValue, eSetValueWithOverwrite);
// Задача читает:
uint32_t val;
xTaskNotifyWait(0, ULONG_MAX, &val, portMAX_DELAY);</code></pre>
<h3>Совместное выполнение (Co-routine) — устаревший подход</h3>
<p>Сопрограммы (co-routines) в FreeRTOS устарели. Используй задачи с небольшим стеком вместо них.</p>
<h3>Watchdog + FreeRTOS</h3>
<pre><code>// Паттерн: каждая задача сбрасывает свой бит в маске
// IWDG сбрасывается только когда все задачи "живы"

volatile uint32_t wdgMask = 0;
#define WDG_BIT_SENSOR  (1 << 0)
#define WDG_BIT_DISPLAY (1 << 1)
#define WDG_ALL         (WDG_BIT_SENSOR | WDG_BIT_DISPLAY)

void vWatchdogTask(void *p) {
    for (;;) {
        if ((wdgMask & WDG_ALL) == WDG_ALL) {
            HAL_IWDG_Refresh(&hiwdg);  // все задачи живы
            wdgMask = 0;               // сбросить маску
        }
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void vSensorTask(void *p) {
    for (;;) {
        doSensor();
        wdgMask |= WDG_BIT_SENSOR;   // отметить что живы
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}</code></pre>
<h3>Порядок запуска задач при старте</h3>
<pre><code>// Гарантировать порядок инициализации:
// 1. Создать все задачи заблокированными (приоритет 0)
// 2. Запустить планировщик
// 3. Задача инициализации (приоритет configMAX_PRIORITIES-1) делает всё, потом удаляет себя

void vInitTask(void *p) {
    Sensor_Init();
    Display_Init();
    UART_Init();

    // Разблокировать рабочие задачи
    vTaskPrioritySet(xSensorHandle, 3);
    vTaskPrioritySet(xDisplayHandle, 2);

    vTaskDelete(NULL);  // удалить себя
}</code></pre>'''},
]


class Command(BaseCommand):
    help = 'Expand RVES M1-M4 to 6 detailed lessons each'

    def handle(self, *args, **options):
        subject = Subject.objects.get(slug='rves')

        for mod_order, lessons in [
            (1, M1_LESSONS), (2, M2_LESSONS),
            (3, M3_LESSONS), (4, M4_LESSONS),
        ]:
            module = TheoryModule.objects.filter(subject=subject, order=mod_order).first()
            if not module:
                self.stderr.write(f'Module M{mod_order} not found')
                continue
            for lesson in lessons:
                obj, created = TheoryLesson.objects.update_or_create(
                    module=module, order=lesson['order'],
                    defaults={**lesson, 'module': module},
                )
                status = 'created' if created else 'updated'
                self.stdout.write(
                    f'  M{mod_order} урок {lesson["order"]}: {lesson["title"][:50]} [{status}]'
                )
            self.stdout.write(f'Module M{mod_order}: {len(lessons)} lessons done')

        self.stdout.write('Done: RVES M1-M4 expanded')
