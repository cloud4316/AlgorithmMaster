from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson

M8_LESSONS = [
    {
        'order': 1,
        'title': 'Отладка ПО МК: виды ошибок и методы поиска',
        'content': '''<h2>Отладка ПО МК: виды ошибок и методы поиска</h2>
<p>Отладка встраиваемого ПО отличается от отладки прикладных программ: нет stdin/stdout, ограничены ресурсы вывода, ошибки могут зависеть от аппаратного состояния.</p>

<h3>Классификация ошибок в ПО МК</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Тип ошибки</th><th>Описание</th><th>Как проявляется</th></tr>
  <tr><td>Синтаксические</td><td>Ошибки компилятора</td><td>Не компилируется</td></tr>
  <tr><td>Логические</td><td>Неверный алгоритм</td><td>Неправильный результат</td></tr>
  <tr><td>Временные (timing)</td><td>Нарушение таймингов</td><td>Нестабильная работа</td></tr>
  <tr><td>Аппаратные</td><td>Неверная настройка периферии</td><td>Периферия не отвечает</td></tr>
  <tr><td>Переполнение стека</td><td>Stack overflow</td><td>HardFault, зависание</td></tr>
  <tr><td>Гонка данных</td><td>Race condition в ISR</td><td>Случайные сбои</td></tr>
  <tr><td>Утечки ресурсов</td><td>Нет освобождения памяти/мьютексов</td><td>Деградация через время</td></tr>
</table>

<h3>Метод "делением пополам" (Binary Search Debug)</h3>
<p>Классический метод поиска ошибки в большом объёме кода:</p>
<ol>
  <li>Поставить точку останова в середине кода.</li>
  <li>Если ошибки нет — проблема во второй половине. Иначе — в первой.</li>
  <li>Повторить для выбранной половины.</li>
  <li>O(log N) итераций — находим точку ошибки.</li>
</ol>

<h3>Printf-отладка для МК</h3>
<pre><code>// Быстро и грязно, но работает
#define DEBUG 1

#if DEBUG
  #define DBG(fmt, ...) printf("[DBG] " fmt "\r\n", ##__VA_ARGS__)
#else
  #define DBG(fmt, ...) do {} while(0)
#endif

// Использование:
DBG("temp = %.2f, state = %d", temp, state);
DBG("ISR count: %lu", isrCount);

// Отключение: #define DEBUG 0 → нулевой оверхед
</code></pre>

<h3>Анализ HardFault</h3>
<pre><code>// Декодировать причину HardFault
void HardFault_Handler(void) {
    volatile uint32_t hfsr = SCB->HFSR;  // HardFault Status Register
    volatile uint32_t cfsr = SCB->CFSR;  // Configurable Fault Status
    volatile uint32_t mmfar = SCB->MMFAR; // MemManage fault address
    volatile uint32_t bfar  = SCB->BFAR;  // BusFault address
    (void)hfsr; (void)cfsr; (void)mmfar; (void)bfar;
    // В отладчике: посмотреть значения этих переменных
    // CFSR.MMARVALID=1 → mmfar содержит адрес нарушителя
    // CFSR.BFARVALID=1 → bfar содержит адрес шины
    while(1);
}
</code></pre>

<h3>Watchdog как инструмент отладки</h3>
<p>IWDG позволяет определить, в какой части кода зависает программа:</p>
<pre><code>// Расставить "чекпоинты" — если до следующего не дойдём, WDG сбросит
HAL_IWDG_Refresh(&hiwdg);   // checkpoint A
doPartA();
HAL_IWDG_Refresh(&hiwdg);   // checkpoint B
doPartB();
HAL_IWDG_Refresh(&hiwdg);   // checkpoint C
// Если МК перезагрузился — ошибка в partB (дошли до B, не дошли до C)
</code></pre>

<div class="tip">Самый распространённый источник зависаний МК: бесконечный цикл ожидания флага готовности без таймаута. Пример: while(SPI->SR & SPI_SR_BSY); — если периферия не инициализирована, вечный цикл.</div>''',
    },
    {
        'order': 2,
        'title': 'Рефакторинг: принципы, техники, безопасность',
        'content': '''<h2>Рефакторинг: принципы, техники, безопасность</h2>
<p>Рефакторинг — изменение внутренней структуры кода без изменения внешнего поведения. Во встраиваемой разработке критично: неосторожный рефакторинг может нарушить реальное время или порядок инициализации.</p>

<h3>Признаки кода, требующего рефакторинга ("Code Smells")</h3>
<ul>
  <li><strong>Длинная функция</strong> — более 40–50 строк трудно читать и тестировать.</li>
  <li><strong>Дублирование кода</strong> — один и тот же алгоритм в нескольких местах.</li>
  <li><strong>Магические числа</strong> — <code>delay(750)</code> вместо <code>delay(DS18B20_CONVERSION_TIME_MS)</code>.</li>
  <li><strong>God Function</strong> — функция, делающая всё сразу (init + calculate + send + log).</li>
  <li><strong>Глобальные переменные</strong> — затрудняют тестирование и понимание.</li>
  <li><strong>Глубокая вложенность</strong> — if внутри if внутри for внутри while.</li>
</ul>

<h3>Техники рефакторинга</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Техника</th><th>До</th><th>После</th></tr>
  <tr><td>Извлечение функции</td><td>Длинная функция</td><td>Несколько коротких, именованных</td></tr>
  <tr><td>Замена магических чисел</td><td><code>750</code></td><td><code>DS18B20_CONV_MS</code></td></tr>
  <tr><td>Инверсия условия</td><td><code>if (!error) { много кода }</code></td><td><code>if (error) return; ... основной код...</code></td></tr>
  <tr><td>Объединение дублирующихся функций</td><td><code>readSensor1(), readSensor2()</code></td><td><code>readSensor(uint8_t addr)</code></td></tr>
  <tr><td>Замена флага на перечисление</td><td><code>uint8_t state = 2;</code></td><td><code>DeviceState state = STATE_RUNNING;</code></td></tr>
</table>

<h3>Пример рефакторинга функции инициализации</h3>
<pre><code>// ДО: God Function
void init(void) {
    RCC->AHB1ENR |= 1;
    GPIOA->MODER |= (1<<10);
    // ... 80 строк инициализации ...
    TIM2->PSC = 8399;
    TIM2->ARR = 9999;
    TIM2->CR1 |= 1;
    USART1->BRR = 0x683;
    USART1->CR1 |= (1<<13)|(1<<3)|(1<<2);
}

// ПОСЛЕ: разбито по ответственности
void GPIO_Init(void) { ... }
void TIM2_Init(void) { ... }
void UART1_Init(uint32_t baud) { ... }

void SystemInit(void) {
    GPIO_Init();
    TIM2_Init();
    UART1_Init(9600);
}
</code></pre>

<h3>Безопасный рефакторинг МК-кода</h3>
<ol>
  <li>Написать тесты до рефакторинга (если нет — написать сейчас).</li>
  <li>Изменять небольшими шагами — один рефакторинг за раз.</li>
  <li>После каждого шага — компиляция + запуск тестов.</li>
  <li>Проверить, что реальное время не нарушено (осциллограф, если есть критичные тайминги).</li>
  <li>Коммит в git после каждого успешного шага.</li>
</ol>

<h3>Особенности рефакторинга в реальном времени</h3>
<pre><code>// ОПАСНО: вынос кода из ISR в функцию без проверки времени
// Было: 10 инструкций в ISR → 1 мкс
// Стало: вызов функции с пролог/эпилог → 3 мкс
// Если ISR вызывается 1 МГц → CPU загружен на 300%!

// Безопасно: измерить время GPIO-методом до и после рефакторинга
GPIOB->BSRR = PIN0; // start
doRefactoredCode();
GPIOB->BSRR = PIN0 << 16; // end
// Осциллограф покажет изменение времени
</code></pre>''',
    },
    {
        'order': 3,
        'title': 'Git: ветвление, слияние, работа в команде',
        'content': '''<h2>Git: ветвление, слияние, работа в команде</h2>
<p>Git — стандарт управления версиями в разработке ПО, включая встраиваемые системы. Правильное использование ветвей позволяет параллельно разрабатывать функции и управлять релизами прошивки.</p>

<h3>Базовые операции</h3>
<pre><code># Статус и история
git status
git log --oneline --graph --all

# Создание ветки и переключение
git checkout -b feature/i2c-sensor
# или (современный синтаксис)
git switch -c feature/i2c-sensor

# Сохранение изменений
git add Core/Src/i2c_sensor.c Core/Inc/i2c_sensor.h
git commit -m "feat: add DS3231 RTC driver over I2C"

# Публикация ветки
git push -u origin feature/i2c-sensor
</code></pre>

<h3>Стратегии ветвления для МК-проектов</h3>
<p><strong>Git Flow</strong> — подходит для проектов с версионированными релизами прошивки:</p>
<pre><code>main          ← стабильные релизы (теги v1.0, v1.1)
develop       ← интеграционная ветка
feature/xxx   ← новые функции (от develop)
release/1.1   ← подготовка релиза (от develop)
hotfix/xxx    ← срочные исправления (от main)
</code></pre>

<p><strong>GitHub Flow</strong> — проще, подходит для непрерывной разработки:</p>
<pre><code>main          ← всегда рабочая
feature/xxx   ← от main, PR → main, удаляется после слияния
</code></pre>

<h3>Слияние и разрешение конфликтов</h3>
<pre><code># Слияние feature-ветки в develop
git checkout develop
git merge feature/i2c-sensor

# Если конфликт в main.c:
# <<<<<<< HEAD (develop)
# uint8_t sensorAddr = 0x48;
# =======
# uint8_t sensorAddr = 0x3C;
# >>>>>>> feature/i2c-sensor

# Редактируем файл вручную → выбираем нужное значение
git add Core/Src/main.c
git commit   # завершение слияния

# Предпочтительно: rebase вместо merge (линейная история)
git checkout feature/i2c-sensor
git rebase develop
git checkout develop
git merge feature/i2c-sensor   # fast-forward
</code></pre>

<h3>Теги и релизы прошивки</h3>
<pre><code># Создать тег для релиза прошивки
git tag -a v1.2.0 -m "Release 1.2.0
- Added I2C RTC DS3231 support
- Fixed alarm threshold bug (BUG-047)
- Reduced sleep current to 5 uA"

git push origin v1.2.0

# Просмотр тегов
git tag -l "v1.*"

# Создать .bin для конкретного тега
git checkout v1.1.0
make clean && make
cp build/firmware.bin release/firmware_v1.1.0.bin
</code></pre>

<h3>Git Hooks для автоматизации</h3>
<pre><code># .git/hooks/pre-commit — запуск тестов перед коммитом
#!/bin/bash
echo "Running unit tests..."
make test
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
echo "Tests passed."
exit 0
</code></pre>
<pre><code># .git/hooks/commit-msg — проверка формата сообщения
#!/bin/bash
MSG=$(cat "$1")
if ! echo "$MSG" | grep -qE "^(feat|fix|refactor|docs|test|chore): .+"; then
    echo "Invalid commit message format."
    echo "Use: feat|fix|refactor|docs|test|chore: description"
    exit 1
fi
</code></pre>''',
    },
    {
        'order': 4,
        'title': 'Code Review: процесс, критерии, Pull Request',
        'content': '''<h2>Code Review: процесс, критерии, Pull Request</h2>
<p>Code Review — процесс проверки кода другим разработчиком до слияния в основную ветку. Один из самых эффективных методов поиска ошибок и распространения знаний в команде.</p>

<h3>Зачем Code Review</h3>
<ul>
  <li>Находит ошибки, которые автор не видит (эффект "свежего взгляда").</li>
  <li>Распространяет знание о кодовой базе между разработчиками.</li>
  <li>Проверяет соответствие архитектурным решениям.</li>
  <li>Обеспечивает единый стиль кода.</li>
  <li>Для МК: критично проверять корректность работы с аппаратурой (тактирование, прерывания, DMA).</li>
</ul>

<h3>Критерии Code Review для МК-кода</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Категория</th><th>Что проверять</th></tr>
  <tr><td>Корректность</td><td>Логика алгоритма, граничные значения, обработка ошибок</td></tr>
  <tr><td>Аппаратура</td><td>Включено тактирование, volatile на регистры/ISR-переменные</td></tr>
  <tr><td>Реальное время</td><td>Нет блокирующих вызовов в ISR, таймауты везде</td></tr>
  <tr><td>Безопасность</td><td>Нет переполнений буфера, проверка входных данных</td></tr>
  <tr><td>Тесты</td><td>Новая функциональность покрыта тестами</td></tr>
  <tr><td>Документация</td><td>Обновлены комментарии, ТЗ если нужно</td></tr>
  <tr><td>Стиль</td><td>Соответствует .clang-format, нет магических чисел</td></tr>
</table>

<h3>Создание Pull Request (GitHub)</h3>
<pre><code># 1. Публикуем ветку
git push -u origin feature/can-driver

# 2. На GitHub → Compare & pull request
# Заполняем:
# Title: feat: add CAN bus driver for STM32F4
#
# Description:
# ## Changes
# - Added bxCAN driver with 500 kbit/s configuration
# - Implemented Tx mailbox management with priority queue
# - Added Rx filter for message IDs 0x100-0x1FF
#
# ## Testing
# - [ ] Loopback test (single node)
# - [ ] Two-node communication test
# - [ ] Bus-off recovery test
#
# ## Related issues
# Closes #23
</code></pre>

<h3>Комментарии в Code Review</h3>
<pre><code>// Плохой комментарий ревьюера (непонятно, что делать):
"Это неправильно"

// Хороший комментарий (конкретный, объясняет почему):
"Здесь нет таймаута в цикле ожидания флага BSY.
Если SPI не инициализирован или нагрузка на шине,
процесс зависнет. Добавь:
  uint32_t t = HAL_GetTick();
  while (SPI1->SR & SPI_SR_BSY) {
      if (HAL_GetTick() - t > 100) return ERR_TIMEOUT;
  }"
</code></pre>

<h3>Автоматические проверки в PR</h3>
<p>GitHub Actions выполняет при каждом PR:</p>
<ul>
  <li>Компиляция прошивки (arm-none-eabi-gcc).</li>
  <li>Юнит-тесты на ПК (Unity).</li>
  <li>Статический анализ (Cppcheck).</li>
  <li>Проверка форматирования (clang-format --dry-run --Werror).</li>
  <li>Проверка размера прошивки (не превышает Flash МК).</li>
</ul>

<div class="tip">Правило двух глаз (Four-Eyes Principle): ни один код не попадает в main без проверки вторым разработчиком. На критических системах — требование стандартов IEC 61508, ISO 26262.</div>''',
    },
    {
        'order': 5,
        'title': 'Профилирование производительности МК-программ',
        'content': '''<h2>Профилирование производительности МК-программ</h2>
<p>Профилирование — поиск узких мест в производительности. Для МК это особенно важно: ресурсы ограничены, а реальное время критично.</p>

<h3>Зачем профилировать МК-код</h3>
<ul>
  <li>Найти функции, потребляющие больше всего CPU-времени.</li>
  <li>Убедиться, что ISR завершается за допустимое время.</li>
  <li>Оптимизировать алгоритм для достижения нужного FPS (дисплей) или частоты дискретизации (АЦП).</li>
  <li>Выявить Cache Miss или pipeline stall на Cortex-M7.</li>
</ul>

<h3>Метод GPIO-меток (простейший)</h3>
<pre><code>// Измерение времени функции
void GPIOB_Set(void)   { GPIOB->BSRR = GPIO_PIN_0; }
void GPIOB_Clear(void) { GPIOB->BSRR = GPIO_PIN_0 << 16; }

void someHeavyFunction(void) {
    GPIOB_Set();
    // ... тяжёлый код ...
    GPIOB_Clear();
}
// Осциллограф → ширина импульса = время выполнения
</code></pre>

<h3>SysTick профилирование</h3>
<pre><code>static inline uint32_t profStart(void) {
    return DWT->CYCCNT;   // счётчик тактов CPU
}

static inline uint32_t profStop(uint32_t start) {
    return DWT->CYCCNT - start;
}

// Инициализация DWT (один раз)
CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
DWT->CYCCNT = 0;
DWT->CTRL  |= DWT_CTRL_CYCCNTENA_Msk;

// Замер
uint32_t t0 = profStart();
FFT_compute(data, 256);
uint32_t cycles = profStop(t0);
printf("FFT 256: %lu cycles = %.1f us @ 168MHz\r\n",
       cycles, cycles / 168.0f);
</code></pre>

<h3>ITM Trace — статистика вызовов</h3>
<p>STM32CubeIDE + SWV: вкладка Software Counters показывает число исключений, тактов в ISR, контекстных переключений FreeRTOS в реальном времени.</p>

<h3>Оптимизация горячих участков кода</h3>
<pre><code>// 1. Перенести код в ITCM RAM (Cortex-M7, 0 задержек)
void __attribute__((section(".itcmram"))) fastISR(void) { ... }

// 2. Использовать аппаратный FPU вместо программной математики
// -mfloat-abi=hard → float-операции через FPU (1–3 такта vs 20–100)

// 3. Развернуть цикл (loop unrolling)
// GCC: __attribute__((optimize("unroll-loops")))

// 4. Lookup-таблица вместо вычисления
// sin(x) → table[x * 256 / (2*PI)] — чтение из Flash/RAM

// 5. DMA вместо побайтового копирования
// memcpy → DMA_Memcpy — CPU свободен во время копирования

// 6. Включить кэш (Cortex-M7)
SCB_EnableICache();
SCB_EnableDCache();
</code></pre>

<h3>Анализ MAP-файла</h3>
<pre><code># Найти самые большие функции
arm-none-eabi-nm --size-sort -t d firmware.elf | tail -20

# Анализ секций
arm-none-eabi-size --format=sysv firmware.elf | sort -k2 -rn | head -20

# Дизассемблер конкретной функции
arm-none-eabi-objdump -d firmware.elf | grep -A 30 "&lt;FFT_compute&gt;:"
</code></pre>''',
    },
    {
        'order': 6,
        'title': 'Архитектурные паттерны надёжного ПО МК',
        'content': '''<h2>Архитектурные паттерны надёжного ПО МК</h2>
<p>Надёжность встраиваемого ПО обеспечивается не только тестированием, но и правильной архитектурой. Проверенные паттерны позволяют создавать предсказуемый, тестируемый и сопровождаемый код.</p>

<h3>Слоистая архитектура (Layered Architecture)</h3>
<pre><code>┌──────────────────────────────────────┐
│         Application Layer            │  ← бизнес-логика
├──────────────────────────────────────┤
│         Middleware / RTOS            │  ← FreeRTOS, протоколы
├──────────────────────────────────────┤
│         HAL / Driver Layer           │  ← драйверы периферии
├──────────────────────────────────────┤
│         Hardware (MCU)               │  ← регистры, прерывания
└──────────────────────────────────────┘
</code></pre>
<p>Каждый слой общается только с соседним. Верхние слои не знают о конкретном МК — это позволяет портировать логику на другое железо.</p>

<h3>State Machine (Конечный автомат)</h3>
<pre><code>typedef enum {
    STATE_IDLE,
    STATE_MEASURING,
    STATE_ALARM,
    STATE_SLEEP,
} DeviceState;

static DeviceState currentState = STATE_IDLE;

void processState(Event event) {
    switch (currentState) {
        case STATE_IDLE:
            if (event == EVENT_TIMER_1S) {
                startMeasurement();
                currentState = STATE_MEASURING;
            }
            break;

        case STATE_MEASURING:
            if (event == EVENT_MEAS_DONE) {
                if (isAlarm()) currentState = STATE_ALARM;
                else           currentState = STATE_IDLE;
            }
            break;

        case STATE_ALARM:
            if (event == EVENT_ALARM_ACK) {
                stopAlarm();
                currentState = STATE_IDLE;
            }
            break;

        case STATE_SLEEP:
            if (event == EVENT_WAKEUP) {
                wakeUp();
                currentState = STATE_IDLE;
            }
            break;
    }
}
</code></pre>

<h3>Event Queue (Очередь событий)</h3>
<pre><code>// ISR публикует событие в очередь
// Main обрабатывает события без busy-wait

typedef enum { EVT_UART_RX, EVT_TIMER, EVT_GPIO } EventType;

static volatile EventType eventQueue[16];
static volatile uint8_t head = 0, tail = 0;

void pushEvent(EventType e) {
    eventQueue[head++ % 16] = e;
}

EventType popEvent(void) {
    return eventQueue[tail++ % 16];
}

// В ISR (простая, без задержек):
void USART1_IRQHandler(void) { pushEvent(EVT_UART_RX); }

// В main:
while(1) {
    if (head != tail) {
        processState(popEvent());
    }
    // Можно уснуть: __WFE()
}
</code></pre>

<h3>Defensive Programming (Защитное программирование)</h3>
<pre><code>// Всегда проверяй NULL
uint8_t* allocateBuffer(uint32_t size) {
    uint8_t *buf = malloc(size);
    if (buf == NULL) {
        errorHandler(ERR_OUT_OF_MEMORY);
        return NULL;
    }
    return buf;
}

// Всегда проверяй возврат HAL
HAL_StatusTypeDef st = HAL_UART_Transmit(&huart1, buf, len, 100);
if (st != HAL_OK) {
    logError("UART TX failed: %d", st);
    return ERR_COMM;
}

// Assert для инвариантов разработки
#define ASSERT(cond) do { if(!(cond)) { errorHandler(ERR_ASSERT); } } while(0)
ASSERT(len <= sizeof(txBuffer));   // поймает ошибку при разработке
</code></pre>

<h3>Правило единственной точки выхода vs Early Return</h3>
<pre><code>// MISRA рекомендует единую точку выхода (один return)
// Практически: Early Return при ошибках — читабельнее

int processPacket(uint8_t *buf, uint16_t len) {
    if (buf == NULL) return ERR_NULL;      // ранний выход
    if (len < 4)     return ERR_TOO_SHORT; // ранний выход
    if (buf[0] != MAGIC_BYTE) return ERR_INVALID; // ранний выход

    // Основная логика без глубокой вложенности
    process(buf + 1, len - 1);
    return OK;
}
</code></pre>''',
    },
]

M9_LESSONS = [
    {
        'order': 1,
        'title': 'Практикум GPIO: управление LED, кнопки, дребезг',
        'content': '''<h2>Практикум GPIO: управление LED, кнопки, дребезг</h2>
<p>Практическая работа с GPIO — первый шаг в освоении STM32. Правильная работа с кнопками и устранение дребезга — основа надёжного ввода.</p>

<h3>Схема подключения</h3>
<pre><code>PA5  ─── [220 Ом] ─── LED ─── GND    (выход, активный HIGH)
PC13 ─── КНОПКА ─── GND              (вход, подтяжка к VCC, PULLUP)
</code></pre>

<h3>Инициализация GPIO (HAL)</h3>
<pre><code>void GPIO_Init(void) {
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();

    GPIO_InitTypeDef gpio = {0};

    // LED PA5 — Output Push-Pull
    gpio.Pin   = GPIO_PIN_5;
    gpio.Mode  = GPIO_MODE_OUTPUT_PP;
    gpio.Pull  = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &gpio);

    // Кнопка PC13 — Input с подтяжкой
    gpio.Pin  = GPIO_PIN_13;
    gpio.Mode = GPIO_MODE_INPUT;
    gpio.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOC, &gpio);
}
</code></pre>

<h3>Простое управление LED</h3>
<pre><code>HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);    // включить
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);  // выключить
HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);                 // переключить

// Мигание с периодом 500 мс
while(1) {
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    HAL_Delay(500);
}
</code></pre>

<h3>Дребезг кнопки (bouncing)</h3>
<p>Механический контакт при нажатии создаёт серию импульсов на протяжении 5–30 мс. Без устранения дребезга одно нажатие регистрируется как несколько.</p>

<h3>Программное устранение дребезга</h3>
<pre><code>// Метод 1: задержка после обнаружения нажатия
uint8_t ButtonRead(void) {
    if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET) {
        HAL_Delay(20);   // ждать окончания дребезга
        if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET) {
            return 1;    // кнопка нажата
        }
    }
    return 0;
}

// Метод 2: счётчик стабильных состояний (неблокирующий)
typedef struct {
    uint8_t prevState;
    uint8_t stableState;
    uint8_t count;
} Button_t;

uint8_t Button_Update(Button_t *btn, uint8_t raw) {
    if (raw == btn->prevState) {
        if (++btn->count >= 5) {   // 5 одинаковых опросов (5×5мс=25мс)
            btn->stableState = raw;
            btn->count = 5;
        }
    } else {
        btn->count = 0;
    }
    btn->prevState = raw;
    return btn->stableState;
}
</code></pre>

<h3>Детектирование нажатия (событие, не уровень)</h3>
<pre><code>uint8_t prevBtn = 0;
while(1) {
    uint8_t btn = ButtonRead();
    if (btn && !prevBtn) {          // передний фронт — момент нажатия
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
    prevBtn = btn;
    HAL_Delay(5);   // период опроса 5 мс
}
</code></pre>

<div class="tip">Для промышленных применений: аппаратный RC-фильтр (R=10кОм, C=100нФ) на линии кнопки убирает дребезг на уровне схемы. Программное устранение — дополнительный уровень защиты.</div>''',
    },
    {
        'order': 2,
        'title': 'Практикум LCD: вывод на ЖКИ по I2C (PCF8574 + HD44780)',
        'content': '''<h2>Практикум LCD: вывод на ЖКИ по I2C (PCF8574 + HD44780)</h2>
<p>Символьный ЖКИ 16×2 с контроллером HD44780 — стандартный дисплей для встраиваемых проектов. I2C-адаптер PCF8574 сокращает число пинов с 7 до 2.</p>

<h3>Аппаратная схема</h3>
<pre><code>STM32       PCF8574-адаптер      HD44780
PB6 (SDA) ──── SDA ────────────── /
PB7 (SCL) ──── SCL ────────────── /
3.3В ──────── VCC ─────────────── /
GND ───────── GND ─────────────── /

Адрес PCF8574: 0x27 (A0=A1=A2=1) или 0x3F (зависит от пайки джамперов)
</code></pre>

<h3>Драйвер LCD — инициализация (HD44780 в 4-битном режиме)</h3>
<pre><code>#define LCD_ADDR  0x27
#define LCD_RS    0x01  // бит RS на PCF8574
#define LCD_EN    0x04  // бит E
#define LCD_BL    0x08  // подсветка
#define LCD_D4    0x10
#define LCD_D5    0x20
#define LCD_D6    0x40
#define LCD_D7    0x80

void LCD_SendNibble(uint8_t nibble, uint8_t rs) {
    uint8_t data = LCD_BL | rs;
    data |= (nibble & 0x01) ? LCD_D4 : 0;
    data |= (nibble & 0x02) ? LCD_D5 : 0;
    data |= (nibble & 0x04) ? LCD_D6 : 0;
    data |= (nibble & 0x08) ? LCD_D7 : 0;

    HAL_I2C_Master_Transmit(&hi2c1, LCD_ADDR<<1, &data, 1, 10);
    data |= LCD_EN;
    HAL_I2C_Master_Transmit(&hi2c1, LCD_ADDR<<1, &data, 1, 10);
    HAL_Delay(1);
    data &= ~LCD_EN;
    HAL_I2C_Master_Transmit(&hi2c1, LCD_ADDR<<1, &data, 1, 10);
}

void LCD_SendByte(uint8_t byte, uint8_t rs) {
    LCD_SendNibble(byte >> 4, rs);
    LCD_SendNibble(byte & 0x0F, rs);
}

void LCD_Init(void) {
    HAL_Delay(50);
    LCD_SendNibble(0x03, 0); HAL_Delay(5);
    LCD_SendNibble(0x03, 0); HAL_Delay(1);
    LCD_SendNibble(0x03, 0); HAL_Delay(1);
    LCD_SendNibble(0x02, 0); // 4-bit mode
    LCD_SendByte(0x28, 0);   // 2 строки, 5×8
    LCD_SendByte(0x0C, 0);   // Display on, cursor off
    LCD_SendByte(0x06, 0);   // Increment cursor
    LCD_SendByte(0x01, 0);   // Clear display
    HAL_Delay(2);
}
</code></pre>

<h3>Вывод текста</h3>
<pre><code>void LCD_SetCursor(uint8_t row, uint8_t col) {
    uint8_t addr = (row == 0) ? 0x80 : 0xC0;
    LCD_SendByte(addr + col, 0);
}

void LCD_Print(const char *str) {
    while (*str) LCD_SendByte(*str++, LCD_RS);
}

void LCD_Printf(uint8_t row, uint8_t col, const char *fmt, ...) {
    char buf[17];
    va_list args;
    va_start(args, fmt);
    vsnprintf(buf, sizeof(buf), fmt, args);
    va_end(args);
    LCD_SetCursor(row, col);
    LCD_Print(buf);
}

// Использование:
LCD_Init();
LCD_Printf(0, 0, "T = %+6.1f C", 23.5f);
LCD_Printf(1, 0, "Tmax=%-3d Tmin=%-3d", 40, 10);
</code></pre>

<h3>Пользовательские символы</h3>
<pre><code>// Определить символ "градус" в CGRAM (ячейка 0)
uint8_t degree[8] = {0x06, 0x09, 0x09, 0x06, 0x00, 0x00, 0x00, 0x00};

void LCD_CreateChar(uint8_t slot, uint8_t *pattern) {
    LCD_SendByte(0x40 | (slot << 3), 0);  // CGRAM addr
    for (int i = 0; i < 8; i++) LCD_SendByte(pattern[i], LCD_RS);
}

LCD_CreateChar(0, degree);
LCD_SetCursor(0, 5);
LCD_SendByte(0x00, LCD_RS);  // вывести символ #0 (градус)
</code></pre>''',
    },
    {
        'order': 3,
        'title': 'Практикум АЦП: измерение напряжения и датчики',
        'content': '''<h2>Практикум АЦП: измерение напряжения и датчики</h2>
<p>АЦП (ADC) преобразует аналоговый сигнал в цифровой. Практическое применение: измерение температуры (NTC-термистор, LM35), напряжения батареи, освещённости (фоторезистор).</p>

<h3>Инициализация ADC1 (STM32F4, канал 1 = PA1)</h3>
<pre><code>ADC_HandleTypeDef hadc1;

void ADC1_Init(void) {
    __HAL_RCC_ADC1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    // PA1 — Analog mode
    GPIO_InitTypeDef gpio = {.Pin = GPIO_PIN_1, .Mode = GPIO_MODE_ANALOG};
    HAL_GPIO_Init(GPIOA, &gpio);

    hadc1.Instance                   = ADC1;
    hadc1.Init.Resolution            = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode          = DISABLE;
    hadc1.Init.ContinuousConvMode    = DISABLE;
    hadc1.Init.ExternalTrigConvEdge  = ADC_EXTERNALTRIGCONVEDGE_NONE;
    hadc1.Init.DataAlign             = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion       = 1;
    HAL_ADC_Init(&hadc1);

    ADC_ChannelConfTypeDef ch = {
        .Channel      = ADC_CHANNEL_1,
        .Rank         = 1,
        .SamplingTime = ADC_SAMPLETIME_84CYCLES,
    };
    HAL_ADC_ConfigChannel(&hadc1, &ch);
}

uint32_t ADC_Read(void) {
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, 10);
    return HAL_ADC_GetValue(&hadc1);
}
</code></pre>

<h3>Измерение напряжения</h3>
<pre><code>// Перевод кода в вольты
// VREF = 3.3V, 12-bit (0..4095)
float readVoltage(void) {
    uint32_t raw = ADC_Read();
    return raw * 3.3f / 4095.0f;
}

// Делитель напряжения для батареи 12 В (R1=10кОм, R2=3.3кОм)
// Коэффициент: (R1+R2)/R2 = 13.3/3.3 ≈ 4.03
float readBatteryVoltage(void) {
    return readVoltage() * 4.03f;
}
</code></pre>

<h3>NTC-термистор (10 кОм, B=3950)</h3>
<pre><code>#define R_NTC_25C  10000.0f    // сопротивление при 25°C
#define R_FIXED    10000.0f    // подтягивающий резистор
#define B_COEFF    3950.0f     // коэффициент B термистора
#define T0         298.15f     // 25°C в Кельвинах

float NTC_ReadTemperature(void) {
    uint32_t raw = ADC_Read();
    // Делитель: VCC --- R_FIXED --- A --- NTC --- GND
    float Vadc = raw * 3.3f / 4095.0f;
    float R_ntc = R_FIXED * Vadc / (3.3f - Vadc);

    // Уравнение Стейнхарта-Харта (упрощённое)
    float invT = 1.0f/T0 + (1.0f/B_COEFF) * logf(R_ntc / R_NTC_25C);
    return (1.0f / invT) - 273.15f;
}
</code></pre>

<h3>Аналоговый датчик LM35 (10 мВ/°C)</h3>
<pre><code>// LM35: Vout = 0.01 * T (вольт), T в градусах Цельсия
float LM35_ReadTemperature(void) {
    float V = readVoltage();
    return V / 0.01f;   // 10 мВ на градус
}
// При V = 0.250 V → T = 25.0°C
</code></pre>

<h3>Усреднение для снижения шума</h3>
<pre><code>float ADC_ReadAveraged(uint8_t samples) {
    uint32_t sum = 0;
    for (uint8_t i = 0; i < samples; i++) {
        sum += ADC_Read();
        HAL_Delay(1);
    }
    return (float)sum / samples * 3.3f / 4095.0f;
}
// 16 отсчётов → шум снижается в √16 = 4 раза
</code></pre>''',
    },
    {
        'order': 4,
        'title': 'Практикум ШИМ: управление яркостью LED и сервоприводом',
        'content': '''<h2>Практикум ШИМ: управление яркостью LED и сервоприводом</h2>
        <p>ШИМ (PWM — Pulse-Width Modulation) — широтно-импульсная модуляция. Управляет аналоговыми устройствами цифровым сигналом: яркостью LED, скоростью двигателя, положением сервопривода.</p>

<h3>Принцип ШИМ</h3>
<pre><code>Период T = 1/f (например, 1 кГц → T = 1 мс)

Скважность (Duty Cycle):
  0%  → сигнал всегда LOW  → устройство выключено
  50% → HIGH половину периода → средняя мощность
  100%→ сигнал всегда HIGH → максимальная мощность

Формула: Duty = (Pulse / Period) × 100%
</code></pre>

<h3>ШИМ на STM32: TIM3 CH1 (PA6)</h3>
<pre><code>// Частота ШИМ = TIM_CLK / ((PSC+1) × (ARR+1))
// TIM3_CLK = 84 МГц (APB1 × 2)
// PSC=83, ARR=999 → 84МГц / (84×1000) = 1 кГц

TIM_HandleTypeDef htim3;

void PWM_Init(void) {
    __HAL_RCC_TIM3_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    // PA6 → Alternate Function TIM3_CH1
    GPIO_InitTypeDef gpio = {
        .Pin       = GPIO_PIN_6,
        .Mode      = GPIO_MODE_AF_PP,
        .Speed     = GPIO_SPEED_FREQ_HIGH,
        .Alternate = GPIO_AF2_TIM3,
    };
    HAL_GPIO_Init(GPIOA, &gpio);

    htim3.Instance               = TIM3;
    htim3.Init.Prescaler         = 83;
    htim3.Init.CounterMode       = TIM_COUNTERMODE_UP;
    htim3.Init.Period            = 999;    // ARR
    htim3.Init.ClockDivision     = TIM_CLOCKDIVISION_DIV1;
    HAL_TIM_PWM_Init(&htim3);

    TIM_OC_InitTypeDef oc = {
        .OCMode    = TIM_OCMODE_PWM1,
        .Pulse     = 0,     // CCR: начальная скважность 0%
        .OCPolarity= TIM_OCPOLARITY_HIGH,
    };
    HAL_TIM_PWM_ConfigChannel(&htim3, &oc, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
}

void PWM_SetDuty(uint8_t percent) {
    uint32_t ccr = (999 * percent) / 100;
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, ccr);
}
</code></pre>

<h3>Плавное изменение яркости (breathing effect)</h3>
<pre><code>void LED_Breathe(void) {
    for (int i = 0; i <= 100; i++) {
        PWM_SetDuty(i);
        HAL_Delay(10);   // нарастание 1 с
    }
    for (int i = 100; i >= 0; i--) {
        PWM_SetDuty(i);
        HAL_Delay(10);   // спад 1 с
    }
}
</code></pre>

<h3>Управление сервоприводом</h3>
<p>Сервопривод типа SG90 управляется ШИМ с периодом 20 мс (50 Гц). Ширина импульса задаёт угол:</p>
<pre><code>// PSC=1679, ARR=999 → 84МГц/(1680×1000) = 50 Гц
// Период 20 мс → ARR=999 единиц = 20 мс
// 1 мс = 50 единиц, 2 мс = 100 единиц

#define SERVO_MIN_PULSE  50   //  0°:  1 мс
#define SERVO_MID_PULSE  75   // 90°: 1.5 мс
#define SERVO_MAX_PULSE  100  //180°:  2 мс

void Servo_SetAngle(uint8_t angle) {
    uint32_t pulse = SERVO_MIN_PULSE +
                     (angle * (SERVO_MAX_PULSE - SERVO_MIN_PULSE)) / 180;
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, pulse);
}

// Использование:
Servo_SetAngle(0);    HAL_Delay(500);   //   0°
Servo_SetAngle(90);   HAL_Delay(500);   //  90°
Servo_SetAngle(180);  HAL_Delay(500);   // 180°
</code></pre>''',
    },
    {
        'order': 5,
        'title': 'Практикум UART: приём и отправка данных, протоколы',
        'content': '''<h2>Практикум UART: приём и отправка данных, протоколы</h2>
<p>UART (Universal Asynchronous Receiver/Transmitter) — самый простой интерфейс для связи МК с ПК, GPS, GSM-модулями, Bluetooth. Нет тактового сигнала — стороны должны договориться о скорости (baud rate).</p>

<h3>Параметры UART</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Параметр</th><th>Типичное значение</th><th>Описание</th></tr>
  <tr><td>Baud Rate</td><td>9600, 115200</td><td>Бит/с</td></tr>
  <tr><td>Data bits</td><td>8</td><td>Разрядность данных</td></tr>
  <tr><td>Parity</td><td>None / Even / Odd</td><td>Бит чётности</td></tr>
  <tr><td>Stop bits</td><td>1 / 2</td><td>Стоп-биты</td></tr>
  <tr><td>Flow control</td><td>None / RTS-CTS</td><td>Управление потоком</td></tr>
</table>
<p>Запись: 9600 8N1 = 9600 Бод, 8 бит данных, No parity, 1 стоп-бит.</p>

<h3>Инициализация UART1 (PA9=TX, PA10=RX)</h3>
<pre><code>UART_HandleTypeDef huart1;

void UART1_Init(void) {
    __HAL_RCC_USART1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    GPIO_InitTypeDef gpio = {
        .Pin       = GPIO_PIN_9 | GPIO_PIN_10,
        .Mode      = GPIO_MODE_AF_PP,
        .Speed     = GPIO_SPEED_FREQ_HIGH,
        .Alternate = GPIO_AF7_USART1,
    };
    HAL_GPIO_Init(GPIOA, &gpio);

    huart1.Instance          = USART1;
    huart1.Init.BaudRate     = 115200;
    huart1.Init.WordLength   = UART_WORDLENGTH_8B;
    huart1.Init.StopBits     = UART_STOPBITS_1;
    huart1.Init.Parity       = UART_PARITY_NONE;
    huart1.Init.Mode         = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl    = UART_HWCONTROL_NONE;
    HAL_UART_Init(&huart1);
}
</code></pre>

<h3>Отправка и приём</h3>
<pre><code>// Отправить строку
void UART_SendString(const char *str) {
    HAL_UART_Transmit(&huart1, (uint8_t*)str, strlen(str), 100);
}

// Printf через UART
int _write(int fd, char *data, int len) {
    HAL_UART_Transmit(&huart1, (uint8_t*)data, len, HAL_MAX_DELAY);
    return len;
}

// Приём с IDLE-прерыванием (пакеты переменной длины)
uint8_t rxBuf[64];
HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rxBuf, sizeof(rxBuf));

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *h, uint16_t size) {
    rxBuf[size] = '\0';   // завершить строку
    processCommand((char*)rxBuf);
    HAL_UARTEx_ReceiveToIdle_DMA(h, rxBuf, sizeof(rxBuf));
}
</code></pre>

<h3>Простой текстовый протокол</h3>
<pre><code>// Формат команды: "CMD arg1 arg2\r\n"
void processCommand(char *cmd) {
    char name[16]; int arg1, arg2;
    if (sscanf(cmd, "SET %s %d", name, &arg1) == 2) {
        if (strcmp(name, "Tmax") == 0) setTmax(arg1);
        else if (strcmp(name, "Tmin") == 0) setTmin(arg1);
        printf("OK: %s = %d\r\n", name, arg1);
    }
    else if (strcmp(cmd, "STATUS\r\n") == 0) {
        printf("T=%.1f Tmax=%d Tmin=%d\r\n", getTemp(), getTmax(), getTmin());
    }
    else {
        printf("ERR: unknown command\r\n");
    }
}
</code></pre>

<h3>Кольцевой буфер для приёма</h3>
<pre><code>// Кольцевой буфер для ISR-приёма без блокировок
#define RX_BUF_SIZE 256
uint8_t rxRingBuf[RX_BUF_SIZE];
volatile uint16_t rxHead = 0, rxTail = 0;

void USART1_IRQHandler(void) {
    if (USART1->SR & USART_SR_RXNE) {
        rxRingBuf[rxHead++ % RX_BUF_SIZE] = USART1->DR;
    }
}

uint8_t UART_ReadByte(uint8_t *byte) {
    if (rxHead == rxTail) return 0;   // буфер пуст
    *byte = rxRingBuf[rxTail++ % RX_BUF_SIZE];
    return 1;
}
</code></pre>''',
    },
    {
        'order': 6,
        'title': 'Практикум I2C/SPI: датчики температуры, давления, OLED',
        'content': '''<h2>Практикум I2C/SPI: датчики температуры, давления, OLED</h2>
<p>I2C и SPI — два наиболее распространённых интерфейса для работы с датчиками и периферией. Практический опыт работы с реальными устройствами.</p>

<h3>BME280 — датчик температуры, давления, влажности (I2C)</h3>
<pre><code>// I2C адрес BME280: 0x76 (SDO=GND) или 0x77 (SDO=VCC)
#define BME280_ADDR  0x76

// Инициализация: перевод в Normal mode, OSR×1, фильтр выключен
uint8_t reg[2];
reg[0] = 0xF4; reg[1] = 0x27;   // ctrl_meas: T×1, P×1, Normal
HAL_I2C_Master_Transmit(&hi2c1, BME280_ADDR<<1, reg, 2, 100);

// Чтение компенсированных данных
uint8_t data[8];
uint8_t startReg = 0xF7;
HAL_I2C_Master_Transmit(&hi2c1, BME280_ADDR<<1, &startReg, 1, 100);
HAL_I2C_Master_Receive(&hi2c1,  BME280_ADDR<<1, data, 8, 100);

// Сырые данные давления и температуры (20 бит)
int32_t adc_P = ((int32_t)data[0]<<12)|((int32_t)data[1]<<4)|(data[2]>>4);
int32_t adc_T = ((int32_t)data[3]<<12)|((int32_t)data[4]<<4)|(data[5]>>4);

// Компенсация по формулам из datasheet BME280 (используй готовую библиотеку)
float temperature = BME280_CompensateTemperature(adc_T); // °C
float pressure    = BME280_CompensatePressure(adc_P);    // Па
</code></pre>

<h3>OLED SSD1306 128×64 (I2C)</h3>
<pre><code>#include "ssd1306.h"   // популярная библиотека: afiskon/stm32-ssd1306

// Инициализация (адрес 0x3C)
ssd1306_Init();

// Вывод текста
ssd1306_SetCursor(0, 0);
ssd1306_WriteString("Hello STM32!", Font_11x18, White);

// Вывод числа
char buf[16];
snprintf(buf, sizeof(buf), "T=%+.1f C", 23.5f);
ssd1306_SetCursor(0, 20);
ssd1306_WriteString(buf, Font_7x10, White);

// Рисование фигур
ssd1306_DrawRectangle(0, 0, 127, 63, White);     // рамка
ssd1306_DrawLine(0, 32, 127, 32, White);          // горизонталь
ssd1306_DrawCircle(64, 32, 20, White);            // круг

// Обновить дисплей (отправить буфер)
ssd1306_UpdateScreen();
</code></pre>

<h3>SPI Flash W25Q64 (8 МБ)</h3>
<pre><code>// W25Q64: CS=PA4, SPI1 (PA5=SCK, PA6=MISO, PA7=MOSI)
#define W25Q_CS_LOW()   HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_RESET)
#define W25Q_CS_HIGH()  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_SET)

// Прочитать JEDEC ID (0xEF4017 для W25Q64)
uint32_t W25Q_ReadID(void) {
    uint8_t tx[] = {0x9F, 0,0,0};
    uint8_t rx[4];
    W25Q_CS_LOW();
    HAL_SPI_TransmitReceive(&hspi1, tx, rx, 4, 100);
    W25Q_CS_HIGH();
    return (rx[1]<<16)|(rx[2]<<8)|rx[3];
}

// Стереть сектор 4 КБ по адресу 0x000000
void W25Q_EraseSector(uint32_t addr) {
    uint8_t tx[] = {0x20, addr>>16, addr>>8, addr};
    W25Q_CS_LOW();
    HAL_SPI_Transmit(&hspi1, (uint8_t[]){0x06}, 1, 10);  // Write Enable
    W25Q_CS_HIGH();
    W25Q_CS_LOW();
    HAL_SPI_Transmit(&hspi1, tx, 4, 100);
    W25Q_CS_HIGH();
    HAL_Delay(100);  // ждать стирание ~50 мс
}
</code></pre>

<h3>Итоговый проект: термостат с OLED и UART</h3>
<ul>
  <li>BME280 → I2C → температура и давление каждые 1 с.</li>
  <li>OLED SSD1306 → I2C → отображение данных.</li>
  <li>UART → JSON → отправка на ПК.</li>
  <li>TIM2 → прерывание 1 с → цикл измерений.</li>
  <li>IWDG → защита от зависания.</li>
</ul>''',
    },
]

M10_LESSONS = [
    {
        'order': 1,
        'title': 'Практикум UART расширенный: парсинг команд, протокол Modbus RTU',
        'content': '''<h2>Практикум UART расширенный: парсинг команд, протокол Modbus RTU</h2>
<p>Промышленные системы часто используют стандартный протокол Modbus RTU поверх RS-485/UART. Понимание парсинга бинарных протоколов — важный навык.</p>

<h3>Конечный автомат парсинга UART</h3>
<pre><code>typedef enum {
    PARSE_WAIT_STX,    // ожидание стартового байта 0x02
    PARSE_READ_CMD,    // команда
    PARSE_READ_DATA,   // данные
    PARSE_READ_ETX,    // конечный байт 0x03
} ParseState;

typedef struct {
    ParseState state;
    uint8_t cmd;
    uint8_t data[32];
    uint8_t dataLen;
} Parser;

void Parser_Feed(Parser *p, uint8_t byte) {
    switch (p->state) {
        case PARSE_WAIT_STX:
            if (byte == 0x02) p->state = PARSE_READ_CMD;
            break;
        case PARSE_READ_CMD:
            p->cmd = byte;
            p->dataLen = 0;
            p->state = PARSE_READ_DATA;
            break;
        case PARSE_READ_DATA:
            if (byte == 0x03) {
                processPacket(p);
                p->state = PARSE_WAIT_STX;
            } else {
                if (p->dataLen < 32) p->data[p->dataLen++] = byte;
            }
            break;
    }
}
</code></pre>

<h3>Modbus RTU — структура кадра</h3>
<pre><code>+--------+---------+---------+-------+-------+
|  Addr  |   Func  |  Data   | CRC_L | CRC_H |
| 1 байт | 1 байт  | N байт  |     2 байта    |
+--------+---------+---------+----------------+

Пример запроса чтения регистров (FC=0x03):
  01 03 00 00 00 01 84 0A
  │  │  │──────│  │─────│
  │  │  начало  кол-во  CRC16
  │  FC=Read Holding Registers
  адрес устройства
</code></pre>

<h3>Реализация Modbus RTU Slave</h3>
<pre><code>#define MODBUS_ADDR  1

uint16_t holdingRegs[10] = {0};  // регистры Modbus

uint16_t CRC16(uint8_t *buf, uint16_t len) {
    uint16_t crc = 0xFFFF;
    for (uint16_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (uint8_t j = 0; j < 8; j++)
            crc = (crc & 1) ? (crc >> 1) ^ 0xA001 : crc >> 1;
    }
    return crc;
}

void Modbus_Process(uint8_t *req, uint16_t len) {
    if (req[0] != MODBUS_ADDR) return;   // не наш адрес
    uint16_t rxCRC = req[len-2] | (req[len-1]<<8);
    if (CRC16(req, len-2) != rxCRC) return;  // ошибка CRC

    uint8_t fc      = req[1];
    uint16_t regAddr = (req[2]<<8)|req[3];
    uint16_t regCount= (req[4]<<8)|req[5];

    if (fc == 0x03) {  // Read Holding Registers
        uint8_t resp[5 + regCount*2];
        resp[0] = MODBUS_ADDR;
        resp[1] = 0x03;
        resp[2] = regCount * 2;
        for (uint16_t i = 0; i < regCount; i++) {
            resp[3 + i*2] = holdingRegs[regAddr+i] >> 8;
            resp[4 + i*2] = holdingRegs[regAddr+i] & 0xFF;
        }
        uint16_t crc = CRC16(resp, 3 + regCount*2);
        resp[3+regCount*2] = crc & 0xFF;
        resp[4+regCount*2] = crc >> 8;
        HAL_UART_Transmit(&huart1, resp, 5+regCount*2, 100);
    }
}
</code></pre>

<h3>RS-485 vs RS-232</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>Параметр</th><th>RS-232</th><th>RS-485</th></tr>
  <tr><td>Число устройств</td><td>2 (point-to-point)</td><td>32–256 (мультидроп)</td></tr>
  <tr><td>Дальность</td><td>15 м</td><td>1200 м</td></tr>
  <tr><td>Скорость</td><td>до 115.2 кбит/с</td><td>до 10 Мбит/с</td></tr>
  <tr><td>Помехозащита</td><td>Низкая</td><td>Высокая (дифференциальная)</td></tr>
  <tr><td>Направление</td><td>Full-duplex</td><td>Half-duplex (один провод)</td></tr>
</table>''',
    },
    {
        'order': 2,
        'title': 'Практикум датчики: DS18B20 (1-Wire), DHT22, MPU6050',
        'content': '''<h2>Практикум датчики: DS18B20 (1-Wire), DHT22, MPU6050</h2>
<p>Работа с датчиками — ключевой навык разработчика встраиваемых систем. Каждый датчик имеет свой протокол и нюансы реализации.</p>

<h3>DS18B20 — цифровой термометр (1-Wire)</h3>
<pre><code>// 1-Wire: один провод + подтяжка 4.7 кОм к VCC
// Тайминги критичны (±2 мкс), нужен таймер или DWT

// Reset pulse
HAL_GPIO_WritePin(OW_PORT, OW_PIN, 0);  // LOW 480 мкс
delay_us(480);
HAL_GPIO_WritePin(OW_PORT, OW_PIN, 1);  // отпустить
delay_us(70);
uint8_t presence = !HAL_GPIO_ReadPin(OW_PORT, OW_PIN); // 0=нет устройства
delay_us(410);

// Команды DS18B20
#define OW_SKIP_ROM    0xCC  // один датчик на шине
#define OW_CONVERT_T   0x44  // начать преобразование
#define OW_READ_SCRATCH 0xBE  // прочитать данные

// Последовательность
DS18B20_Reset();
DS18B20_WriteByte(OW_SKIP_ROM);
DS18B20_WriteByte(OW_CONVERT_T);
HAL_Delay(750);   // ждать преобразование 12 бит (750 мс)

DS18B20_Reset();
DS18B20_WriteByte(OW_SKIP_ROM);
DS18B20_WriteByte(OW_READ_SCRATCH);
uint8_t lsb = DS18B20_ReadByte();
uint8_t msb = DS18B20_ReadByte();
float temp = (int16_t)((msb<<8)|lsb) / 16.0f;
</code></pre>

<h3>DHT22 — температура и влажность</h3>
<pre><code>// DHT22: один провод, специфический протокол (не 1-Wire!)
// Запрос: HIGH 250 мс → LOW 20 мс → HIGH → ждать ответ

void DHT22_Read(float *temp, float *hum) {
    uint8_t data[5] = {0};

    // Стартовый импульс
    GPIO_SetOutput(DHT_PORT, DHT_PIN);
    HAL_GPIO_WritePin(DHT_PORT, DHT_PIN, 0);
    HAL_Delay(20);
    HAL_GPIO_WritePin(DHT_PORT, DHT_PIN, 1);
    delay_us(30);

    // Ждать ответный сигнал от DHT22
    GPIO_SetInput(DHT_PORT, DHT_PIN);
    while (!HAL_GPIO_ReadPin(DHT_PORT, DHT_PIN));  // LOW 80 мкс
    while (HAL_GPIO_ReadPin(DHT_PORT, DHT_PIN));   // HIGH 80 мкс

    // Читать 40 бит (5 байт)
    for (int i = 0; i < 40; i++) {
        while (!HAL_GPIO_ReadPin(DHT_PORT, DHT_PIN));  // LOW 50 мкс
        delay_us(35);  // ждать в середине HIGH
        int bit = HAL_GPIO_ReadPin(DHT_PORT, DHT_PIN);
        data[i/8] = (data[i/8] << 1) | bit;
        while (HAL_GPIO_ReadPin(DHT_PORT, DHT_PIN));
    }

    // Контрольная сумма
    if ((data[0]+data[1]+data[2]+data[3]) == data[4]) {
        *hum  = ((data[0]<<8)|data[1]) / 10.0f;
        *temp = (((data[2]&0x7F)<<8)|data[3]) / 10.0f;
        if (data[2] & 0x80) *temp = -*temp;  // отрицательная
    }
}
</code></pre>

<h3>MPU6050 — акселерометр + гироскоп (I2C)</h3>
<pre><code>#define MPU6050_ADDR   0x68   // AD0=GND
#define MPU_PWR_MGMT_1 0x6B
#define MPU_ACCEL_XOUT 0x3B

// Инициализация: выход из сна
uint8_t reg[2] = {MPU_PWR_MGMT_1, 0x00};
HAL_I2C_Master_Transmit(&hi2c1, MPU6050_ADDR<<1, reg, 2, 100);

// Чтение 6 байт акселерометра
uint8_t startReg = MPU_ACCEL_XOUT;
uint8_t raw[6];
HAL_I2C_Master_Transmit(&hi2c1, MPU6050_ADDR<<1, &startReg, 1, 100);
HAL_I2C_Master_Receive(&hi2c1,  MPU6050_ADDR<<1, raw, 6, 100);

int16_t ax = (raw[0]<<8)|raw[1];  // Range ±2g → делитель 16384
int16_t ay = (raw[2]<<8)|raw[3];
int16_t az = (raw[4]<<8)|raw[5];

float ax_g = ax / 16384.0f;  // в единицах g
float ay_g = ay / 16384.0f;
float az_g = az / 16384.0f;

// Угол наклона (упрощённо, без компл. фильтра)
float pitch = atan2f(ax_g, az_g) * 180.0f / 3.14159f;
float roll  = atan2f(ay_g, az_g) * 180.0f / 3.14159f;
</code></pre>''',
    },
    {
        'order': 3,
        'title': 'Практикум OLED и графика: анимация, графики, меню',
        'content': '''<h2>Практикум OLED и графика: анимация, графики, меню</h2>
<p>OLED-дисплей SSD1306 позволяет создавать полноценный пользовательский интерфейс для встраиваемых устройств: графики в реальном времени, меню, анимации.</p>

<h3>График температуры в реальном времени</h3>
<pre><code>// Буфер последних 128 значений (по ширине дисплея)
float tempHistory[128] = {0};
uint8_t histIdx = 0;

void updateGraph(float newTemp) {
    // Сдвинуть буфер
    memmove(tempHistory, tempHistory+1, 127*sizeof(float));
    tempHistory[127] = newTemp;

    ssd1306_Fill(Black);   // очистить буфер

    // Нарисовать оси
    ssd1306_DrawLine(0, 63, 127, 63, White);   // ось X
    ssd1306_DrawLine(0, 0,  0,   63, White);   // ось Y

    // Нарисовать график
    float tMin = 0.0f, tMax = 50.0f;
    for (int x = 1; x < 128; x++) {
        // Масштаб: 0°C → y=63, 50°C → y=10
        uint8_t y1 = 63 - (uint8_t)((tempHistory[x-1]-tMin) / (tMax-tMin) * 53);
        uint8_t y2 = 63 - (uint8_t)((tempHistory[x]  -tMin) / (tMax-tMin) * 53);
        ssd1306_DrawLine(x-1, y1, x, y2, White);
    }

    // Текущее значение
    char buf[12];
    snprintf(buf, sizeof(buf), "%.1f C", newTemp);
    ssd1306_SetCursor(70, 0);
    ssd1306_WriteString(buf, Font_7x10, White);

    ssd1306_UpdateScreen();
}
</code></pre>

<h3>Простое текстовое меню</h3>
<pre><code>const char *menuItems[] = {
    "1. Измерение",
    "2. Настройки",
    "3. Архив",
    "4. О программе"
};
uint8_t selectedItem = 0;

void Menu_Draw(void) {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(0, 0);
    ssd1306_WriteString("=== МЕНЮ ===", Font_7x10, White);

    for (uint8_t i = 0; i < 4; i++) {
        ssd1306_SetCursor(0, 16 + i*12);
        if (i == selectedItem) {
            ssd1306_WriteString(">", Font_7x10, White);
        } else {
            ssd1306_WriteString(" ", Font_7x10, White);
        }
        ssd1306_WriteString(menuItems[i]+3, Font_7x10, White);
    }
    ssd1306_UpdateScreen();
}

void Menu_Navigate(uint8_t up) {
    if (up && selectedItem > 0) selectedItem--;
    if (!up && selectedItem < 3) selectedItem++;
    Menu_Draw();
}

uint8_t Menu_Select(void) {
    return selectedItem;
}
</code></pre>

<h3>Анимация загрузки</h3>
<pre><code>void Splash_Screen(void) {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(20, 10);
    ssd1306_WriteString("Thermometer", Font_11x18, White);
    ssd1306_SetCursor(40, 35);
    ssd1306_WriteString("v1.2.0", Font_7x10, White);

    // Прогресс-бар
    for (uint8_t w = 0; w <= 128; w += 4) {
        ssd1306_DrawFilledRectangle(0, 55, w, 63, White);
        ssd1306_UpdateScreen();
        HAL_Delay(30);
    }

    HAL_Delay(500);
}
</code></pre>

<h3>Битмап-изображение</h3>
<pre><code>// Конвертируй PNG в битмап: LCD Image Converter / image2cpp
// Для иконки 16×16 (32 байта)
const uint8_t thermometerIcon[32] = {
    0x03, 0xC0, 0x04, 0x20, 0x04, 0x20, 0x07, 0xE0,
    // ... 24 байта ...
};

ssd1306_DrawBitmap(56, 24, thermometerIcon, 16, 16, White);
ssd1306_UpdateScreen();
</code></pre>''',
    },
    {
        'order': 4,
        'title': 'Практикум FreeRTOS: многозадачность на STM32',
        'content': '''<h2>Практикум FreeRTOS: многозадачность на STM32</h2>
<p>FreeRTOS позволяет структурировать сложное ПО как набор независимых задач. Каждая задача — отдельный поток выполнения с приоритетом и собственным стеком.</p>

<h3>Структура проекта с FreeRTOS</h3>
<pre><code>// main.c — инициализация и запуск планировщика
int main(void) {
    HAL_Init();
    SystemClock_Config();
    GPIO_Init();
    UART1_Init();
    I2C1_Init();

    // Создать задачи
    xTaskCreate(vSensorTask,  "Sensor",  256, NULL, 3, NULL);
    xTaskCreate(vDisplayTask, "Display", 256, NULL, 2, NULL);
    xTaskCreate(vUARTTask,    "UART",    512, NULL, 1, NULL);
    xTaskCreate(vAlarmTask,   "Alarm",   128, NULL, 4, NULL);

    vTaskStartScheduler();   // запустить планировщик
    while(1);                // никогда не достигается
}
</code></pre>

<h3>Задача измерения (Sensor Task)</h3>
<pre><code>// Очередь для передачи данных между задачами
QueueHandle_t xSensorQueue;

typedef struct {
    float temperature;
    float humidity;
    uint32_t timestamp;
} SensorData_t;

void vSensorTask(void *pvParams) {
    SensorData_t data;
    TickType_t xLastWake = xTaskGetTickCount();

    for (;;) {
        data.temperature = BME280_ReadTemperature();
        data.humidity    = BME280_ReadHumidity();
        data.timestamp   = HAL_GetTick();

        // Отправить в очередь (не блокировать дольше 10 мс)
        xQueueSend(xSensorQueue, &data, pdMS_TO_TICKS(10));

        // Точная задержка 1 с (учитывает время выполнения задачи)
        vTaskDelayUntil(&xLastWake, pdMS_TO_TICKS(1000));
    }
}
</code></pre>

<h3>Задача дисплея (Display Task)</h3>
<pre><code>void vDisplayTask(void *pvParams) {
    SensorData_t data;
    char buf[17];

    ssd1306_Init();

    for (;;) {
        // Ждать данные из очереди до 2 с
        if (xQueueReceive(xSensorQueue, &data, pdMS_TO_TICKS(2000)) == pdTRUE) {
            ssd1306_Fill(Black);
            snprintf(buf, sizeof(buf), "T=%+5.1f C", data.temperature);
            ssd1306_SetCursor(0, 0);
            ssd1306_WriteString(buf, Font_11x18, White);
            snprintf(buf, sizeof(buf), "H=%4.1f%%", data.humidity);
            ssd1306_SetCursor(0, 24);
            ssd1306_WriteString(buf, Font_7x10, White);
            ssd1306_UpdateScreen();
        } else {
            // Нет данных — показать ошибку
            ssd1306_SetCursor(0, 0);
            ssd1306_WriteString("Sensor Error!", Font_7x10, White);
            ssd1306_UpdateScreen();
        }
    }
}
</code></pre>

<h3>Мониторинг FreeRTOS</h3>
<pre><code>// Высота стека задачи (чем меньше, тем лучше выбран размер стека)
void printTaskStats(void) {
    TaskStatus_t tasks[10];
    uint32_t totalTime;
    uint8_t count = uxTaskGetSystemState(tasks, 10, &totalTime);
    printf("Task Name       Stack HWM\r\n");
    for (uint8_t i = 0; i < count; i++) {
        printf("%-15s %5u\r\n",
               tasks[i].pcTaskName,
               tasks[i].usStackHighWaterMark);
    }
}
// HWM (High Water Mark) — минимальный остаток стека за всё время работы
// Если HWM < 20 → стек слишком маленький → увеличить
</code></pre>

<div class="tip">Правило выбора размера стека: запусти задачу с большим стеком (512), дай поработать, проверь HWM. Если HWM=200, минимальный безопасный размер ≈ (512-200)+запас20% ≈ 400 слов.</div>''',
    },
    {
        'order': 5,
        'title': 'Практикум: система мониторинга на FreeRTOS (итоговый проект)',
        'content': '''<h2>Практикум: система мониторинга на FreeRTOS (итоговый проект)</h2>
<p>Полный пример встраиваемой системы мониторинга микроклимата на STM32 с FreeRTOS, OLED, UART и аппаратным таймером.</p>

<h3>Состав системы</h3>
<ul>
  <li>STM32F411 (Nucleo-F411RE или Black Pill)</li>
  <li>BME280 — температура, влажность, давление (I2C)</li>
  <li>SSD1306 128×64 OLED (I2C, тот же I2C1)</li>
  <li>UART1 115200 — JSON-вывод и приём команд</li>
  <li>LED PA5 — индикатор аларма</li>
  <li>Кнопка PC13 — переключение страниц дисплея</li>
  <li>IWDG — защита от зависания</li>
</ul>

<h3>Карта задач FreeRTOS</h3>
<pre><code>┌──────────────────────────────────────────────────────────────┐
│                   FreeRTOS Scheduler                         │
├─────────────┬──────────────┬──────────────┬─────────────────┤
│ SensorTask  │ DisplayTask  │  UARTTask    │  AlarmTask      │
│ Prio=3      │ Prio=2       │  Prio=1      │  Prio=4 (HIGH)  │
│ Stack=256   │ Stack=512    │  Stack=512   │  Stack=128      │
│ Period=1s   │ Period=500ms │  Period=1s   │  Event-driven   │
└─────────────┴──────────────┴──────────────┴─────────────────┘
         │            ▲             ▲               ▲
         └─xQueue─────┘             │               │
                    xQueue──────────┘   xSemaphore──┘
</code></pre>

<h3>Полная архитектура</h3>
<pre><code>// Общие ресурсы FreeRTOS
static QueueHandle_t    xDataQueue;    // SensorData_t × 5
static SemaphoreHandle_t xAlarmSem;   // сигнал тревоги
static SemaphoreHandle_t xI2CMutex;   // защита I2C шины

void main(void) {
    // Инициализация
    HAL_Init(); SystemClock_Config();
    GPIO_Init(); UART1_Init(); I2C1_Init(); IWDG_Init();

    // Ресурсы FreeRTOS
    xDataQueue  = xQueueCreate(5, sizeof(SensorData_t));
    xAlarmSem   = xSemaphoreCreateBinary();
    xI2CMutex   = xSemaphoreCreateMutex();

    // Задачи
    xTaskCreate(vSensorTask,  "Sensor",  256, NULL, 3, NULL);
    xTaskCreate(vDisplayTask, "Display", 512, NULL, 2, NULL);
    xTaskCreate(vUARTTask,    "UART",    512, NULL, 1, NULL);
    xTaskCreate(vAlarmTask,   "Alarm",   128, NULL, 4, NULL);

    vTaskStartScheduler();
}
</code></pre>

<h3>JSON-вывод по UART</h3>
<pre><code>void vUARTTask(void *pvParams) {
    SensorData_t data;
    char jsonBuf[128];

    for (;;) {
        if (xQueuePeek(xDataQueue, &data, pdMS_TO_TICKS(2000)) == pdTRUE) {
            snprintf(jsonBuf, sizeof(jsonBuf),
                "{\"t\":%.2f,\"h\":%.1f,\"p\":%.1f,\"ts\":%lu}\r\n",
                data.temperature, data.humidity,
                data.pressure, data.timestamp);
            HAL_UART_Transmit(&huart1, (uint8_t*)jsonBuf, strlen(jsonBuf), 100);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
</code></pre>

<h3>Проверка системы (тест-сценарии)</h3>
<ol>
  <li>Нагреть BME280 феном → T>40°C → LED мигает + "ALARM HIGH" на OLED + JSON с флагом.</li>
  <li>Отправить UART "STATUS" → ответ в 200 мс.</li>
  <li>Отключить BME280 → "Sensor Error" на OLED, WDG не перезагружает систему.</li>
  <li>72 часа непрерывной работы → нет зависаний, стек HWM > 20 для всех задач.</li>
</ol>''',
    },
    {
        'order': 6,
        'title': 'Итоговый практикум: сборка проекта и защита',
        'content': '''<h2>Итоговый практикум: сборка проекта и защита</h2>
<p>Финальный этап — сборка полного проекта, документирование, тестирование и подготовка к защите. Этот урок обобщает весь практический курс.</p>

<h3>Чек-лист готовности проекта</h3>
<table border="1" cellpadding="6" cellspacing="0">
  <tr><th>№</th><th>Критерий</th><th>Как проверить</th></tr>
  <tr><td>1</td><td>Проект компилируется без ошибок и предупреждений</td><td>make 2>&1 | grep -c warning → 0</td></tr>
  <tr><td>2</td><td>Все модульные тесты проходят</td><td>make test → OK</td></tr>
  <tr><td>3</td><td>Статический анализ без ошибок</td><td>cppcheck → 0 errors</td></tr>
  <tr><td>4</td><td>Прошивка умещается в Flash</td><td>arm-none-eabi-size: text+data < Flash</td></tr>
  <tr><td>5</td><td>RAM не переполнен</td><td>data+bss+heap+stack < RAM</td></tr>
  <tr><td>6</td><td>WDG не перезагружает при нормальной работе</td><td>RCC_FLAG_IWDGRST = 0 после запуска</td></tr>
  <tr><td>7</td><td>72 ч непрерывной работы без сбоев</td><td>Логирование на ПК</td></tr>
  <tr><td>8</td><td>Документация оформлена по ГОСТ 19</td><td>ТЗ + ОП + ПМИ + РП</td></tr>
  <tr><td>9</td><td>Код в Git с тегом версии</td><td>git tag -l v*.*.* → 1 тег</td></tr>
  <tr><td>10</td><td>Схема алгоритма по ГОСТ 19.701</td><td>Блок-схема main() и ISR</td></tr>
</table>

<h3>Подготовка к защите: демонстрация</h3>
<p>Стандартная структура демонстрации проекта:</p>
<ol>
  <li><strong>Введение</strong> (1–2 мин): назначение устройства, решаемая задача, область применения.</li>
  <li><strong>Архитектура</strong> (2–3 мин): схема блоков, используемые интерфейсы, задачи FreeRTOS.</li>
  <li><strong>Демонстрация</strong> (5–7 мин):
    <ul>
      <li>Включение устройства, инициализация.</li>
      <li>Нормальный режим работы (измерение, вывод данных).</li>
      <li>Срабатывание аларма (нагреть датчик).</li>
      <li>Управление через UART (SET команды).</li>
      <li>Вывод JSON на ПК-терминале.</li>
    </ul>
  </li>
  <li><strong>Тестирование</strong> (2–3 мин): запустить Python-тесты, показать результат.</li>
  <li><strong>Документация</strong> (1–2 мин): показать ТЗ, ОП, ПМИ.</li>
</ol>

<h3>Типичные вопросы на защите</h3>
<ul>
  <li>Почему выбран FreeRTOS, а не bare-metal суперцикл?</li>
  <li>Как защищена шина I2C от одновременного доступа двух задач?</li>
  <li>Что произойдёт при зависании SensorTask?</li>
  <li>Как работает устранение дребезга кнопки?</li>
  <li>Чему равен приоритет прерывания UART по отношению к FreeRTOS?</li>
  <li>Как проверить, что Stack не переполняется?</li>
  <li>Объясни алгоритм компенсации BME280.</li>
</ul>

<h3>Типичные ошибки, которые проверяет комиссия</h3>
<pre><code>// Ошибка 1: нет volatile на переменную из ISR
uint32_t flag;   // должно быть: volatile uint32_t flag;
void TIM2_IRQHandler(void) { flag = 1; }
// main: while(!flag); → без volatile → бесконечный цикл после оптимизации

// Ошибка 2: вызов HAL_Delay() в ISR
void EXTI0_IRQHandler(void) {
    HAL_Delay(20);   // НЕЛЬЗЯ! SysTick → NVIC → ISR не выполняется
}

// Ошибка 3: нет таймаута
while (I2C1->SR2 & I2C_SR2_BUSY);  // зависнет если I2C stuck

// Правильно:
uint32_t t = HAL_GetTick();
while (I2C1->SR2 & I2C_SR2_BUSY) {
    if (HAL_GetTick()-t > 100) { return ERR_TIMEOUT; }
}
</code></pre>

<div class="tip">Главный принцип надёжного встраиваемого ПО: любое ожидание должно иметь таймаут. Любая переменная, разделяемая с ISR, должна быть volatile и защищена критической секцией.</div>''',
    },
]


class Command(BaseCommand):
    help = 'Expand RVES modules M8, M9, M10 to 6 detailed lessons each'

    def handle(self, *args, **options):
        subject = Subject.objects.get(slug='rves')

        for mod_order, mod_title, lessons in [
            (8,  'Отладка, рефакторинг и Git', M8_LESSONS),
            (9,  'Практикум ч.1 GPIO/LCD/АЦП/ШИМ/UART', M9_LESSONS),
            (10, 'Практикум ч.2 UART/датчики/OLED/FreeRTOS', M10_LESSONS),
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

        self.stdout.write('Done: RVES M8-M10 expanded')
