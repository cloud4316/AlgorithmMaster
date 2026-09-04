"""
python manage.py seed_mps_expand_m6_m10
Adds 3 new lessons each to modules 6-10 of MPS subject (15 lessons total).
Uses get_or_create to avoid duplicates.
"""
from django.core.management.base import BaseCommand
from django.db.models import Max
from works.models import TheoryModule, TheoryLesson, Subject


LESSONS_DATA = {

# ======================================================================
# M6: АЦП и ЦАП — 3 new lessons
# ======================================================================
'АЦП и ЦАП': [
{
    'title': 'Многоканальный АЦП и автоматическое сканирование',
    'estimated_minutes': 20,
    'content': '''
<h3>Многоканальный АЦП в AVR</h3>
<p>Микроконтроллеры AVR (ATmega328P) имеют <strong>8 каналов АЦП</strong> (ADC0-ADC7),
мультиплексированных на один 10-битный модуль преобразования. Выбор канала
осуществляется через биты MUX3:MUX0 регистра <code>ADMUX</code>.</p>

<h3>Переключение каналов</h3>
<p>Для считывания нескольких аналоговых сигналов необходимо последовательно
переключать мультиплексор:</p>
<ul>
  <li>Записать номер канала в ADMUX (биты MUX3:0)</li>
  <li>Запустить преобразование битом ADSC в ADCSRA</li>
  <li>Дождаться сброса ADSC (или прерывания ADC)</li>
  <li>Считать результат из ADCL/ADCH</li>
</ul>

<h3>Режим Free Running</h3>
<p>В режиме Free Running (ADFR/ADATE=1, триггер = Free Running) АЦП автоматически
запускает следующее преобразование сразу после завершения текущего. Это даёт
максимальную частоту дискретизации ~15 kSPS при тактовой 16 МГц и делителе 128.</p>

<table class="theory-table">
<thead><tr><th>Параметр</th><th>Значение</th></tr></thead>
<tbody>
<tr><td>Разрядность</td><td>10 бит (0-1023)</td></tr>
<tr><td>Опорное напряжение</td><td>AVCC (5В), внутреннее 1.1В или внешнее AREF</td></tr>
<tr><td>Частота тактирования АЦП</td><td>50-200 кГц (оптимально)</td></tr>
<tr><td>Время преобразования</td><td>13 тактов АЦП (первое — 25)</td></tr>
</tbody>
</table>

<h3>Бит ADLAR — выравнивание результата</h3>
<p>При установке бита <code>ADLAR=1</code> результат выравнивается влево: старшие 8 бит
оказываются в <code>ADCH</code>. Это удобно, если достаточно 8-битной точности — можно
читать только ADCH.</p>

<pre><code>// С ADLAR=1: 10-битный результат сдвинут влево
// ADCH содержит биты 9:2 — фактически 8-битный результат
uint8_t val8 = ADCH;  // достаточно для многих задач</code></pre>
''',
    'code_example': '''#include <avr/io.h>
#include <util/delay.h>

// Инициализация АЦП: AVCC как опорное, делитель 128
void adc_init(void) {
    ADMUX  = (1 << REFS0);                      // AVCC reference
    ADCSRA = (1 << ADEN)                         // Enable ADC
           | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // prescaler 128
}

// Чтение одного канала (0-7)
uint16_t adc_read(uint8_t channel) {
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);  // select channel
    ADCSRA |= (1 << ADSC);                       // start conversion
    while (ADCSRA & (1 << ADSC));                 // wait
    return ADC;                                   // 10-bit result
}

// Автоматическое сканирование 4 каналов
uint16_t readings[4];

void scan_channels(void) {
    for (uint8_t ch = 0; ch < 4; ch++) {
        readings[ch] = adc_read(ch);
        _delay_us(100);  // settling time after mux switch
    }
}

int main(void) {
    adc_init();
    while (1) {
        scan_channels();
        // readings[0..3] now contain values from ADC0..ADC3
        _delay_ms(100);
    }
}
'''
},
{
    'title': 'Практическое применение АЦП',
    'estimated_minutes': 25,
    'content': '''
<h3>Датчики с аналоговым выходом</h3>
<p>АЦП позволяет подключать к микроконтроллеру разнообразные аналоговые датчики.
Рассмотрим три типичных примера.</p>

<h3>1. Датчик температуры LM35</h3>
<p>LM35 выдаёт <strong>10 мВ на каждый градус Цельсия</strong>. При опорном 5В и
10-битном АЦП:</p>
<pre><code>Шаг АЦП = 5000 мВ / 1024 = 4.88 мВ
Температура = (ADC * 4.88) / 10.0 [градусов C]</code></pre>
<p>Схема: VCC(+5В) -> Vs(LM35), GND -> GND(LM35), Vout(LM35) -> ADC0.</p>

<h3>2. Фоторезистор (LDR)</h3>
<p>Фоторезистор включается в делитель напряжения с постоянным резистором (10 кОм).
При увеличении освещённости сопротивление LDR падает, напряжение на ADC растёт.</p>
<pre><code>Схема делителя:
  VCC ---[R=10k]---+---[LDR]--- GND
                   |
                  ADC1</code></pre>

<h3>3. Потенциометр</h3>
<p>Потенциометр — простейший аналоговый вход. Крайние выводы к VCC и GND, средний
(движок) — к каналу АЦП. Полный диапазон 0-1023 при вращении.</p>

<table class="theory-table">
<thead><tr><th>Датчик</th><th>Диапазон выхода</th><th>Формула пересчёта</th></tr></thead>
<tbody>
<tr><td>LM35</td><td>0 - 1.5В (0-150C)</td><td>T = ADC * 500.0 / 1024</td></tr>
<tr><td>LDR + 10k</td><td>0 - 5В</td><td>Lux ~ exp(k * ADC) (нелинейно)</td></tr>
<tr><td>Потенциометр</td><td>0 - 5В</td><td>Угол = ADC * 300.0 / 1024</td></tr>
</tbody>
</table>

<h3>Фильтрация показаний</h3>
<p>Аналоговые сигналы шумят. Простейшие способы фильтрации:</p>
<ul>
  <li><strong>Усреднение</strong> — взять N выборок и поделить сумму на N</li>
  <li><strong>Скользящее среднее</strong> — хранить массив последних N значений</li>
  <li><strong>Экспоненциальный фильтр</strong>: filtered = alpha * new + (1-alpha) * filtered</li>
</ul>
''',
    'code_example': '''#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>

// UART для вывода (упрощённый)
void uart_init(uint16_t ubrr) {
    UBRR0H = (uint8_t)(ubrr >> 8);
    UBRR0L = (uint8_t)ubrr;
    UCSR0B = (1 << TXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); // 8N1
}
void uart_putc(char c) { while (!(UCSR0A & (1 << UDRE0))); UDR0 = c; }
void uart_puts(const char *s) { while (*s) uart_putc(*s++); }

void adc_init(void) {
    ADMUX  = (1 << REFS0);  // AVCC
    ADCSRA = (1 << ADEN) | 0x07; // prescaler 128
}

uint16_t adc_read(uint8_t ch) {
    ADMUX = (ADMUX & 0xF0) | (ch & 0x0F);
    ADCSRA |= (1 << ADSC);
    while (ADCSRA & (1 << ADSC));
    return ADC;
}

// Усреднение N выборок
uint16_t adc_read_avg(uint8_t ch, uint8_t n) {
    uint32_t sum = 0;
    for (uint8_t i = 0; i < n; i++) {
        sum += adc_read(ch);
        _delay_us(100);
    }
    return (uint16_t)(sum / n);
}

int main(void) {
    char buf[64];
    uart_init(103);  // 9600 baud @ 16 MHz
    adc_init();

    while (1) {
        // LM35 on ADC0
        uint16_t raw_temp = adc_read_avg(0, 16);
        uint16_t temp_x10 = (uint16_t)((uint32_t)raw_temp * 5000 / 1024 / 10);

        // Potentiometer on ADC1
        uint16_t pot = adc_read_avg(1, 8);

        // LDR on ADC2
        uint16_t ldr = adc_read_avg(2, 8);

        sprintf(buf, "T=%u.%u C  Pot=%u  LDR=%u\\r\\n",
                temp_x10 / 10, temp_x10 % 10, pot, ldr);
        uart_puts(buf);

        _delay_ms(1000);
    }
}
'''
},
{
    'title': 'Внешние ЦАП: R-2R и SPI DAC',
    'estimated_minutes': 20,
    'content': '''
<h3>Цифро-аналоговое преобразование</h3>
<p>AVR не имеет встроенного ЦАП (в отличие от некоторых ARM). Для генерации
аналогового напряжения используют внешние решения.</p>

<h3>R-2R лестница (резисторная матрица)</h3>
<p>Простейший ЦАП на резисторах двух номиналов: R и 2R. Для N-битного ЦАП нужно
N пинов порта и 2N резисторов.</p>
<pre><code>Схема 4-битного R-2R ЦАП:
  PD3 --[2R]--+--[R]--+--[R]--+--[R]--+-- Vout
  PD2 --[2R]--+       |       |       |
  PD1 --[2R]---------+       |       |
  PD0 --[2R]-----------------+       |
                     [2R]             |
                      |               |
                     GND             GND</code></pre>
<p>Выходное напряжение: <code>Vout = Vcc * (цифровое_значение / 2^N)</code>.</p>
<p>Для 8-битного ЦАП весь порт D (PD0-PD7) подключается к R-2R матрице — получаем
256 уровней напряжения.</p>

<h3>SPI DAC: MCP4921</h3>
<p>MCP4921 — 12-битный одноканальный ЦАП с SPI-интерфейсом. Основные параметры:</p>
<table class="theory-table">
<thead><tr><th>Параметр</th><th>Значение</th></tr></thead>
<tbody>
<tr><td>Разрядность</td><td>12 бит (0-4095)</td></tr>
<tr><td>Интерфейс</td><td>SPI (Mode 0,0)</td></tr>
<tr><td>Скорость SPI</td><td>до 20 МГц</td></tr>
<tr><td>Время установления</td><td>4.5 мкс</td></tr>
<tr><td>Выходное напряжение</td><td>0 - Vref (с усилением x1 или x2)</td></tr>
</tbody>
</table>

<h3>Формат команды MCP4921 (16 бит)</h3>
<pre><code>Бит 15: 0 (канал A)
Бит 14: BUF (буферизация Vref)
Бит 13: GA (0 = x2, 1 = x1 усиление)
Бит 12: SHDN (1 = активен)
Биты 11:0 — 12-битное значение данных</code></pre>

<h3>Подключение MCP4921 к AVR</h3>
<ul>
  <li>SCK (MCP4921) -> PB5 (SCK AVR)</li>
  <li>SDI (MCP4921) -> PB3 (MOSI AVR)</li>
  <li>CS  (MCP4921) -> PB2 (SS AVR)</li>
  <li>LDAC -> GND (немедленное обновление выхода)</li>
</ul>
''',
    'code_example': '''#include <avr/io.h>
#include <util/delay.h>
#include <math.h>

// === Простой R-2R ЦАП на порте D (8 бит) ===
void r2r_init(void) {
    DDRD = 0xFF;   // весь порт D на выход
}

void r2r_write(uint8_t value) {
    PORTD = value; // прямая запись значения 0-255
}

// === SPI DAC MCP4921 ===
#define DAC_CS_LOW()   (PORTB &= ~(1 << PB2))
#define DAC_CS_HIGH()  (PORTB |=  (1 << PB2))

void spi_init(void) {
    // MOSI (PB3), SCK (PB5), SS (PB2) as output
    DDRB |= (1 << PB2) | (1 << PB3) | (1 << PB5);
    DAC_CS_HIGH();
    // Enable SPI, Master, fck/4
    SPCR = (1 << SPE) | (1 << MSTR);
}

uint8_t spi_transfer(uint8_t data) {
    SPDR = data;
    while (!(SPSR & (1 << SPIF)));
    return SPDR;
}

// Write 12-bit value to MCP4921 (0-4095)
void dac_write(uint16_t value) {
    // Bit 15=0 (ch A), 14=0 (unbuf), 13=1 (gain x1), 12=1 (active)
    uint16_t cmd = 0x3000 | (value & 0x0FFF);
    DAC_CS_LOW();
    spi_transfer((uint8_t)(cmd >> 8));
    spi_transfer((uint8_t)(cmd & 0xFF));
    DAC_CS_HIGH();
}

int main(void) {
    spi_init();

    // Generate sine wave via MCP4921
    // 256 samples per period
    while (1) {
        for (uint16_t i = 0; i < 256; i++) {
            // sin(0..2pi) -> 0..4095
            double s = sin(2.0 * M_PI * i / 256.0);
            uint16_t val = (uint16_t)((s + 1.0) * 2047.5);
            dac_write(val);
            _delay_us(50); // ~78 Hz sine wave
        }
    }
}
'''
},
],

# ======================================================================
# M7: Интерфейс UART — 3 new lessons
# ======================================================================
'Интерфейс UART': [
{
    'title': 'Протокол обмена и формат кадра',
    'estimated_minutes': 20,
    'content': '''
<h3>Формат кадра UART</h3>
<p>UART (Universal Asynchronous Receiver-Transmitter) передаёт данные последовательно
по одному биту. Каждый кадр содержит:</p>
<ul>
  <li><strong>Стартовый бит</strong> (всегда 0) — сигнализирует начало передачи</li>
  <li><strong>Биты данных</strong> (5-9 бит, обычно 8)</li>
  <li><strong>Бит чётности</strong> (опционально) — контроль ошибок</li>
  <li><strong>Стоповый бит</strong> (1 или 2, всегда 1) — завершение кадра</li>
</ul>

<pre><code>Idle ___________       ___ ___ ___ ___ ___ ___ ___ ___ ___ ___________
               |Start| D0| D1| D2| D3| D4| D5| D6| D7|Par|Stop|Idle
               |_____|___|___|___|___|___|___|___|___|___|____|</code></pre>

<p>Обозначение формата: <strong>8N1</strong> = 8 бит данных, No parity, 1 стоповый бит.</p>

<h3>Скорость передачи (Baud Rate)</h3>
<p>Стандартные скорости: 9600, 19200, 38400, 57600, 115200 бод. Оба устройства
должны быть настроены на одинаковую скорость.</p>

<h3>Расчёт UBRR</h3>
<p>Для ATmega328P значение регистра UBRR определяет скорость:</p>
<table class="theory-table">
<thead><tr><th>Режим</th><th>Формула UBRR</th></tr></thead>
<tbody>
<tr><td>Нормальный (U2X=0)</td><td>UBRR = F_CPU / (16 * BAUD) - 1</td></tr>
<tr><td>Удвоенная скорость (U2X=1)</td><td>UBRR = F_CPU / (8 * BAUD) - 1</td></tr>
</tbody>
</table>

<table class="theory-table">
<thead><tr><th>Baud</th><th>F_CPU=16 МГц, U2X=0</th><th>Ошибка</th></tr></thead>
<tbody>
<tr><td>9600</td><td>UBRR=103</td><td>0.2%</td></tr>
<tr><td>19200</td><td>UBRR=51</td><td>0.2%</td></tr>
<tr><td>57600</td><td>UBRR=16</td><td>2.1% (!)</td></tr>
<tr><td>115200</td><td>UBRR=8 (U2X=1: 16)</td><td>3.5% / 2.1%</td></tr>
</tbody>
</table>

<h3>Бит чётности (Parity)</h3>
<p>Контроль чётности добавляет один бит, равный XOR всех битов данных (Even)
или его инверсии (Odd). Обнаруживает одиночные ошибки, но не исправляет их.</p>
<ul>
  <li><strong>Even parity</strong>: сумма всех бит данных + бит чётности = чётное число</li>
  <li><strong>Odd parity</strong>: сумма = нечётное число</li>
  <li><strong>None</strong>: бит чётности не передаётся (наиболее распространён)</li>
</ul>
''',
    'code_example': '''#include <avr/io.h>

#define F_CPU 16000000UL
#define BAUD  9600

// Расчёт UBRR с округлением
#define UBRR_VAL  ((F_CPU + 8UL * BAUD) / (16UL * BAUD) - 1)

void uart_init(void) {
    // Set baud rate
    UBRR0H = (uint8_t)(UBRR_VAL >> 8);
    UBRR0L = (uint8_t)(UBRR_VAL);

    // Включить приёмник и передатчик
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);

    // Формат кадра: 8 бит данных, 1 стоповый бит, без чётности (8N1)
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

// Настройка 8E1 (8 бит данных, Even parity, 1 стоп)
void uart_init_8e1(void) {
    UBRR0H = (uint8_t)(UBRR_VAL >> 8);
    UBRR0L = (uint8_t)(UBRR_VAL);
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);
    // UPM01=1 — Even parity; UCSZ01:00=11 — 8 бит данных
    UCSR0C = (1 << UPM01) | (1 << UCSZ01) | (1 << UCSZ00);
}

// Настройка 8N2 (8 бит данных, No parity, 2 стоповых бита)
void uart_init_8n2(void) {
    UBRR0H = (uint8_t)(UBRR_VAL >> 8);
    UBRR0L = (uint8_t)(UBRR_VAL);
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);
    // USBS0=1 — 2 стоповых бита
    UCSR0C = (1 << USBS0) | (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_putc(char c) {
    while (!(UCSR0A & (1 << UDRE0)));  // wait for empty buffer
    UDR0 = c;
}

char uart_getc(void) {
    while (!(UCSR0A & (1 << RXC0)));   // wait for data
    // Check for errors
    uint8_t status = UCSR0A;
    if (status & ((1 << FE0) | (1 << DOR0) | (1 << UPE0))) {
        // FE0 = Frame Error, DOR0 = Data Overrun, UPE0 = Parity Error
        (void)UDR0;  // read and discard
        return 0;
    }
    return UDR0;
}

void uart_puts(const char *s) {
    while (*s) uart_putc(*s++);
}

int main(void) {
    uart_init();
    uart_puts("UART 8N1 @ 9600 ready\\r\\n");
    while (1) {
        char c = uart_getc();
        uart_putc(c);  // echo
    }
}
'''
},
{
    'title': 'Буферизация и кольцевой буфер',
    'estimated_minutes': 25,
    'content': '''
<h3>Проблема блокирующего ввода-вывода</h3>
<p>Простейшие функции <code>uart_putc()</code> и <code>uart_getc()</code> блокируют
выполнение программы, пока данные не будут отправлены/приняты. При работе с
прерываниями и многозадачностью это недопустимо.</p>

<h3>Кольцевой (циклический) буфер</h3>
<p>Кольцевой буфер — структура данных FIFO фиксированного размера с двумя указателями:</p>
<ul>
  <li><strong>head</strong> — позиция записи (куда добавляются новые данные)</li>
  <li><strong>tail</strong> — позиция чтения (откуда извлекаются данные)</li>
</ul>
<p>Когда указатель достигает конца массива, он переходит на начало (циклически).
Размер буфера выбирают степенью двойки (32, 64, 128) для быстрого вычисления
остатка через побитовое И: <code>index & (SIZE - 1)</code>.</p>

<pre><code>Кольцевой буфер (размер 8):
  [0][1][2][3][4][5][6][7]
      T        H
      ^        ^
      tail     head
  Данные: [1], [2], [3] — 3 элемента</code></pre>

<h3>Состояния буфера</h3>
<table class="theory-table">
<thead><tr><th>Состояние</th><th>Условие</th></tr></thead>
<tbody>
<tr><td>Пустой</td><td>head == tail</td></tr>
<tr><td>Полный</td><td>(head + 1) % SIZE == tail</td></tr>
<tr><td>Кол-во элементов</td><td>(head - tail) % SIZE</td></tr>
</tbody>
</table>

<h3>UART на прерываниях с кольцевым буфером</h3>
<p>Алгоритм работы:</p>
<ul>
  <li>Приём: прерывание USART_RX кладёт байт в RX-буфер; главный цикл забирает</li>
  <li>Передача: главный цикл кладёт байт в TX-буфер и включает прерывание UDRE;
      обработчик UDRE отправляет байт и выключает прерывание, когда буфер пуст</li>
</ul>
<p>Такой подход неблокирующий и эффективный: процессор свободен между прерываниями.</p>
''',
    'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL
#define BAUD  9600
#define UBRR_VAL ((F_CPU + 8UL * BAUD) / (16UL * BAUD) - 1)

// --- Ring buffer ---
#define BUF_SIZE 64  // must be power of 2
#define BUF_MASK (BUF_SIZE - 1)

typedef struct {
    volatile uint8_t data[BUF_SIZE];
    volatile uint8_t head;
    volatile uint8_t tail;
} RingBuf;

static RingBuf rx_buf = {{0}, 0, 0};
static RingBuf tx_buf = {{0}, 0, 0};

static inline uint8_t buf_is_empty(const RingBuf *b) {
    return b->head == b->tail;
}
static inline uint8_t buf_is_full(const RingBuf *b) {
    return ((b->head + 1) & BUF_MASK) == b->tail;
}
static inline void buf_put(RingBuf *b, uint8_t c) {
    b->data[b->head] = c;
    b->head = (b->head + 1) & BUF_MASK;
}
static inline uint8_t buf_get(RingBuf *b) {
    uint8_t c = b->data[b->tail];
    b->tail = (b->tail + 1) & BUF_MASK;
    return c;
}

// --- UART init ---
void uart_init(void) {
    UBRR0H = (uint8_t)(UBRR_VAL >> 8);
    UBRR0L = (uint8_t)(UBRR_VAL);
    UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

// --- RX interrupt: store byte in rx_buf ---
ISR(USART_RX_vect) {
    uint8_t c = UDR0;
    if (!buf_is_full(&rx_buf)) {
        buf_put(&rx_buf, c);
    }
}

// --- TX interrupt: send next byte from tx_buf ---
ISR(USART_UDRE_vect) {
    if (!buf_is_empty(&tx_buf)) {
        UDR0 = buf_get(&tx_buf);
    } else {
        UCSR0B &= ~(1 << UDRIE0);  // disable UDRE interrupt
    }
}

// --- Non-blocking API ---
uint8_t uart_available(void) {
    return !buf_is_empty(&rx_buf);
}

uint8_t uart_read(void) {
    while (buf_is_empty(&rx_buf));  // wait
    cli();
    uint8_t c = buf_get(&rx_buf);
    sei();
    return c;
}

void uart_write(uint8_t c) {
    while (buf_is_full(&tx_buf));   // wait if full
    cli();
    buf_put(&tx_buf, c);
    UCSR0B |= (1 << UDRIE0);       // enable UDRE interrupt
    sei();
}

void uart_print(const char *s) {
    while (*s) uart_write(*s++);
}

int main(void) {
    uart_init();
    sei();
    uart_print("Ring buffer UART ready\\r\\n");
    while (1) {
        if (uart_available()) {
            uint8_t c = uart_read();
            uart_write(c);  // echo non-blocking
        }
        // CPU is free for other tasks here
    }
}
'''
},
{
    'title': 'Связь МК с компьютером',
    'estimated_minutes': 20,
    'content': '''
<h3>USB-UART преобразователи</h3>
<p>Микроконтроллер обменивается данными по UART на уровнях TTL (0/5В или 0/3.3В).
Для связи с компьютером нужен преобразователь уровней.</p>

<table class="theory-table">
<thead><tr><th>Микросхема</th><th>Скорость</th><th>Драйвер</th><th>Примечание</th></tr></thead>
<tbody>
<tr><td>CH340G</td><td>до 2 Мбод</td><td>CH341SER</td><td>Дешёвый, популярный в Arduino-клонах</td></tr>
<tr><td>CP2102</td><td>до 1 Мбод</td><td>CP210x</td><td>Надёжный, Silicon Labs</td></tr>
<tr><td>FT232RL</td><td>до 3 Мбод</td><td>FTDI VCP</td><td>Профессиональный, FTDI</td></tr>
<tr><td>PL2303</td><td>до 1.2 Мбод</td><td>PL2303</td><td>Старый, бывают проблемы с драйвером</td></tr>
</tbody>
</table>

<h3>Подключение</h3>
<pre><code>USB-UART          AVR
  TX  ---------> RXD (PD0)
  RX  <--------- TXD (PD1)
  GND ---------- GND
  (5V) --------- VCC (если питание от USB)</code></pre>

<h3>Терминал PuTTY</h3>
<p>PuTTY — популярная программа-терминал для Windows. Настройка:</p>
<ul>
  <li>Connection type: Serial</li>
  <li>Serial line: COMx (номер из Диспетчера устройств)</li>
  <li>Speed: 9600 (или другая, совпадающая с МК)</li>
  <li>Data bits: 8, Stop bits: 1, Parity: None, Flow control: None</li>
</ul>
<p>Альтернативы: Arduino Serial Monitor, RealTerm, CoolTerm, minicom (Linux).</p>

<h3>AT-команды</h3>
<p>Формат команд, пришедший из эпохи модемов. Используется в модулях Bluetooth (HC-05),
Wi-Fi (ESP8266), GSM (SIM800). Каждая команда начинается с <code>AT</code>:</p>
<table class="theory-table">
<thead><tr><th>Команда</th><th>Ответ</th><th>Назначение</th></tr></thead>
<tbody>
<tr><td>AT</td><td>OK</td><td>Проверка связи</td></tr>
<tr><td>AT+VERSION</td><td>+VERSION:...</td><td>Версия прошивки</td></tr>
<tr><td>AT+NAME=MyDev</td><td>OK</td><td>Установить имя устройства</td></tr>
<tr><td>AT+BAUD=4</td><td>OK</td><td>Установить скорость (4=9600)</td></tr>
<tr><td>AT+ROLE=1</td><td>OK</td><td>Режим Master (HC-05)</td></tr>
</tbody>
</table>

<h3>Протокол обмена с ПК</h3>
<p>Для надёжной связи определяют простой протокол: маркер начала, длина, данные,
контрольная сумма. Пример пакета:</p>
<pre><code>[0xAA] [LEN] [CMD] [DATA...] [CRC8]</code></pre>
''',
    'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>
#include <string.h>
#include <stdlib.h>

#define F_CPU 16000000UL
#define BAUD  9600
#define UBRR_VAL ((F_CPU + 8UL * BAUD) / (16UL * BAUD) - 1)

void uart_init(void) {
    UBRR0H = (uint8_t)(UBRR_VAL >> 8);
    UBRR0L = (uint8_t)(UBRR_VAL);
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_putc(char c) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}
char uart_getc(void) {
    while (!(UCSR0A & (1 << RXC0)));
    return UDR0;
}
void uart_puts(const char *s) { while (*s) uart_putc(*s++); }

// Read line into buffer (until CR or LF)
uint8_t uart_getline(char *buf, uint8_t maxlen) {
    uint8_t i = 0;
    while (i < maxlen - 1) {
        char c = uart_getc();
        if (c == '\\r' || c == '\\n') break;
        buf[i++] = c;
    }
    buf[i] = '\\0';
    return i;
}

// Simple AT-command parser
void process_command(const char *cmd) {
    if (strcmp(cmd, "AT") == 0) {
        uart_puts("OK\\r\\n");
    }
    else if (strcmp(cmd, "AT+VERSION") == 0) {
        uart_puts("+VERSION:1.0\\r\\n");
        uart_puts("OK\\r\\n");
    }
    else if (strncmp(cmd, "AT+LED=", 7) == 0) {
        uint8_t state = atoi(cmd + 7);
        if (state) PORTB |= (1 << PB5);
        else       PORTB &= ~(1 << PB5);
        uart_puts("OK\\r\\n");
    }
    else if (strcmp(cmd, "AT+ADC?") == 0) {
        // Read ADC0
        ADMUX  = (1 << REFS0);
        ADCSRA = (1 << ADEN) | 0x07;
        ADCSRA |= (1 << ADSC);
        while (ADCSRA & (1 << ADSC));
        char buf[16];
        itoa(ADC, buf, 10);
        uart_puts("+ADC:");
        uart_puts(buf);
        uart_puts("\\r\\nOK\\r\\n");
    }
    else {
        uart_puts("ERROR\\r\\n");
    }
}

int main(void) {
    DDRB |= (1 << PB5); // LED on PB5
    uart_init();
    uart_puts("AVR AT-Command Interface v1.0\\r\\n");
    uart_puts("Type AT for test\\r\\n");

    char line[64];
    while (1) {
        uart_puts("> ");
        uart_getline(line, sizeof(line));
        process_command(line);
    }
}
'''
},
],

# ======================================================================
# M8: Интерфейсы I2C и SPI — 3 new lessons
# ======================================================================
'Интерфейсы I2C и SPI': [
{
    'title': 'Работа с EEPROM по I2C',
    'estimated_minutes': 22,
    'content': '''
<h3>EEPROM AT24C256</h3>
<p>AT24C256 — микросхема энергонезависимой памяти EEPROM объёмом 256 Кбит (32 КБ)
с интерфейсом I2C. Широко применяется для хранения настроек, логов, калибровок.</p>

<table class="theory-table">
<thead><tr><th>Параметр</th><th>AT24C256</th></tr></thead>
<tbody>
<tr><td>Объём</td><td>256 Кбит = 32768 байт</td></tr>
<tr><td>Адрес I2C</td><td>0x50 - 0x57 (задаётся A0-A2)</td></tr>
<tr><td>Страница записи</td><td>64 байта</td></tr>
<tr><td>Время записи</td><td>5 мс (tWR) на страницу</td></tr>
<tr><td>Ресурс</td><td>1 000 000 циклов перезаписи</td></tr>
<tr><td>Адресация</td><td>2 байта (16-бит, до 65535)</td></tr>
</tbody>
</table>

<h3>Адресация</h3>
<p>В отличие от AT24C02 (8-битная адресация), AT24C256 использует 16-битный адрес,
передаваемый двумя байтами после адреса устройства:</p>
<pre><code>Запись байта:
  START | DevAddr+W | AddrHigh | AddrLow | Data | STOP

Чтение байта (Random Read):
  START | DevAddr+W | AddrHigh | AddrLow | RESTART | DevAddr+R | Data | NACK | STOP</code></pre>

<h3>Постраничная запись</h3>
<p>Запись нескольких байтов эффективнее страницами (до 64 байт за раз). Важно:
запись не должна пересекать границу страницы (адрес кратный 64). После записи
нужно ждать 5 мс (или использовать ACK Polling).</p>

<h3>ACK Polling</h3>
<p>Вместо фиксированной задержки 5 мс можно опрашивать устройство: отправлять
START + адрес, пока не придёт ACK (запись завершена).</p>
''',
    'code_example': '''#include <avr/io.h>
#include <util/delay.h>

#define EEPROM_ADDR 0x50  // A0=A1=A2=GND

// --- I2C (TWI) functions ---
#define F_SCL 100000UL
#define TWI_PRESCALER 1

void i2c_init(void) {
    TWSR = 0;  // prescaler = 1
    TWBR = (uint8_t)((F_CPU / F_SCL - 16) / (2 * TWI_PRESCALER));
}

void i2c_start(void) {
    TWCR = (1 << TWINT) | (1 << TWSTA) | (1 << TWEN);
    while (!(TWCR & (1 << TWINT)));
}

void i2c_stop(void) {
    TWCR = (1 << TWINT) | (1 << TWSTO) | (1 << TWEN);
    _delay_us(10);
}

void i2c_write(uint8_t data) {
    TWDR = data;
    TWCR = (1 << TWINT) | (1 << TWEN);
    while (!(TWCR & (1 << TWINT)));
}

uint8_t i2c_read_ack(void) {
    TWCR = (1 << TWINT) | (1 << TWEN) | (1 << TWEA);
    while (!(TWCR & (1 << TWINT)));
    return TWDR;
}

uint8_t i2c_read_nack(void) {
    TWCR = (1 << TWINT) | (1 << TWEN);
    while (!(TWCR & (1 << TWINT)));
    return TWDR;
}

// --- EEPROM functions ---
void eeprom_write_byte(uint16_t addr, uint8_t data) {
    i2c_start();
    i2c_write((EEPROM_ADDR << 1) | 0);  // Write mode
    i2c_write((uint8_t)(addr >> 8));      // Address high
    i2c_write((uint8_t)(addr & 0xFF));    // Address low
    i2c_write(data);
    i2c_stop();
    _delay_ms(5);  // tWR write cycle time
}

uint8_t eeprom_read_byte(uint16_t addr) {
    i2c_start();
    i2c_write((EEPROM_ADDR << 1) | 0);   // Write mode (set address)
    i2c_write((uint8_t)(addr >> 8));
    i2c_write((uint8_t)(addr & 0xFF));

    i2c_start();                          // Repeated START
    i2c_write((EEPROM_ADDR << 1) | 1);   // Read mode
    uint8_t data = i2c_read_nack();
    i2c_stop();
    return data;
}

// Write page (up to 64 bytes, must not cross page boundary)
void eeprom_write_page(uint16_t addr, const uint8_t *buf, uint8_t len) {
    i2c_start();
    i2c_write((EEPROM_ADDR << 1) | 0);
    i2c_write((uint8_t)(addr >> 8));
    i2c_write((uint8_t)(addr & 0xFF));
    for (uint8_t i = 0; i < len; i++) {
        i2c_write(buf[i]);
    }
    i2c_stop();
    _delay_ms(5);
}

// Sequential read
void eeprom_read_seq(uint16_t addr, uint8_t *buf, uint16_t len) {
    i2c_start();
    i2c_write((EEPROM_ADDR << 1) | 0);
    i2c_write((uint8_t)(addr >> 8));
    i2c_write((uint8_t)(addr & 0xFF));
    i2c_start();
    i2c_write((EEPROM_ADDR << 1) | 1);
    for (uint16_t i = 0; i < len - 1; i++) {
        buf[i] = i2c_read_ack();
    }
    buf[len - 1] = i2c_read_nack();
    i2c_stop();
}

int main(void) {
    i2c_init();
    // Store a string in EEPROM
    const char *msg = "Hello EEPROM!";
    eeprom_write_page(0x0000, (const uint8_t *)msg, 14);

    // Read it back
    char buf[16];
    eeprom_read_seq(0x0000, (uint8_t *)buf, 14);
    // buf now contains "Hello EEPROM!"

    while (1);
}
'''
},
{
    'title': 'Работа с датчиками по I2C',
    'estimated_minutes': 25,
    'content': '''
<h3>Типичные I2C-датчики</h3>
<p>По шине I2C подключается множество датчиков. Рассмотрим два популярных.</p>

<h3>BME280 — температура, влажность, давление</h3>
<table class="theory-table">
<thead><tr><th>Параметр</th><th>Значение</th></tr></thead>
<tbody>
<tr><td>Адрес I2C</td><td>0x76 (SDO=GND) или 0x77 (SDO=VCC)</td></tr>
<tr><td>Температура</td><td>-40...+85 C (точность +/-1 C)</td></tr>
<tr><td>Влажность</td><td>0...100% (точность +/-3%)</td></tr>
<tr><td>Давление</td><td>300...1100 гПа (точность +/-1 гПа)</td></tr>
<tr><td>Напряжение</td><td>1.71 - 3.6 В</td></tr>
</tbody>
</table>

<p>Особенности работы с BME280:</p>
<ul>
  <li>Регистр ID (0xD0) возвращает 0x60 — проверка связи</li>
  <li>Данные хранятся в регистрах 0xF7-0xFE (8 байт: давление, температура, влажность)</li>
  <li>Необходима калибровка по коэффициентам из регистров 0x88-0xA1 и 0xE1-0xE7</li>
  <li>Компенсация температуры выполняется по формулам из даташита (32-битная арифметика)</li>
</ul>

<h3>MPU6050 — акселерометр + гироскоп</h3>
<table class="theory-table">
<thead><tr><th>Параметр</th><th>Значение</th></tr></thead>
<tbody>
<tr><td>Адрес I2C</td><td>0x68 (AD0=GND) или 0x69 (AD0=VCC)</td></tr>
<tr><td>Акселерометр</td><td>+/-2g, +/-4g, +/-8g, +/-16g</td></tr>
<tr><td>Гироскоп</td><td>+/-250, 500, 1000, 2000 dps</td></tr>
<tr><td>АЦП</td><td>16 бит</td></tr>
<tr><td>Регистр WHO_AM_I</td><td>0x75 -> 0x68</td></tr>
</tbody>
</table>

<h3>Общий алгоритм работы с I2C-датчиком</h3>
<ul>
  <li><strong>1. Проверка</strong>: прочитать регистр ID, убедиться что датчик отвечает</li>
  <li><strong>2. Инициализация</strong>: записать режим работы, диапазон, частоту</li>
  <li><strong>3. Калибровка</strong>: прочитать заводские коэффициенты (если нужно)</li>
  <li><strong>4. Чтение</strong>: периодически читать регистры данных</li>
  <li><strong>5. Обработка</strong>: применить калибровку, фильтрацию</li>
</ul>

<h3>Чтение нескольких регистров подряд</h3>
<p>Большинство I2C-датчиков поддерживают автоинкремент адреса: после START и
адреса первого регистра можно читать подряд — адрес увеличивается автоматически.</p>
''',
    'code_example': '''#include <avr/io.h>
#include <util/delay.h>

// I2C functions (i2c_init, i2c_start, etc. — as in previous lesson)
// ... (omitted for brevity, same TWI code)

#define MPU6050_ADDR 0x68

// MPU6050 registers
#define MPU_WHO_AM_I    0x75
#define MPU_PWR_MGMT_1  0x6B
#define MPU_ACCEL_CFG   0x1C
#define MPU_GYRO_CFG    0x1B
#define MPU_ACCEL_XOUT  0x3B  // 6 bytes: XH,XL,YH,YL,ZH,ZL

void i2c_init(void) {
    TWSR = 0;
    TWBR = (uint8_t)((F_CPU / 100000UL - 16) / 2);
}
void i2c_start(void) {
    TWCR = (1<<TWINT)|(1<<TWSTA)|(1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
}
void i2c_stop(void) {
    TWCR = (1<<TWINT)|(1<<TWSTO)|(1<<TWEN);
    _delay_us(10);
}
void i2c_write_byte(uint8_t d) {
    TWDR = d;
    TWCR = (1<<TWINT)|(1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
}
uint8_t i2c_read_ack(void) {
    TWCR = (1<<TWINT)|(1<<TWEN)|(1<<TWEA);
    while (!(TWCR & (1<<TWINT)));
    return TWDR;
}
uint8_t i2c_read_nack(void) {
    TWCR = (1<<TWINT)|(1<<TWEN);
    while (!(TWCR & (1<<TWINT)));
    return TWDR;
}

// Write one register
void mpu_write_reg(uint8_t reg, uint8_t val) {
    i2c_start();
    i2c_write_byte((MPU6050_ADDR << 1) | 0);
    i2c_write_byte(reg);
    i2c_write_byte(val);
    i2c_stop();
}

// Read one register
uint8_t mpu_read_reg(uint8_t reg) {
    i2c_start();
    i2c_write_byte((MPU6050_ADDR << 1) | 0);
    i2c_write_byte(reg);
    i2c_start();
    i2c_write_byte((MPU6050_ADDR << 1) | 1);
    uint8_t val = i2c_read_nack();
    i2c_stop();
    return val;
}

// Read N bytes starting from reg
void mpu_read_burst(uint8_t reg, uint8_t *buf, uint8_t n) {
    i2c_start();
    i2c_write_byte((MPU6050_ADDR << 1) | 0);
    i2c_write_byte(reg);
    i2c_start();
    i2c_write_byte((MPU6050_ADDR << 1) | 1);
    for (uint8_t i = 0; i < n - 1; i++)
        buf[i] = i2c_read_ack();
    buf[n - 1] = i2c_read_nack();
    i2c_stop();
}

typedef struct {
    int16_t ax, ay, az;
    int16_t gx, gy, gz;
} MPU_Data;

uint8_t mpu_init(void) {
    uint8_t id = mpu_read_reg(MPU_WHO_AM_I);
    if (id != 0x68) return 0;  // sensor not found

    mpu_write_reg(MPU_PWR_MGMT_1, 0x00); // wake up
    _delay_ms(100);
    mpu_write_reg(MPU_ACCEL_CFG, 0x00);  // +/- 2g
    mpu_write_reg(MPU_GYRO_CFG, 0x00);   // +/- 250 dps
    return 1;
}

void mpu_read(MPU_Data *d) {
    uint8_t buf[14];
    mpu_read_burst(MPU_ACCEL_XOUT, buf, 14);
    d->ax = (int16_t)((buf[0] << 8) | buf[1]);
    d->ay = (int16_t)((buf[2] << 8) | buf[3]);
    d->az = (int16_t)((buf[4] << 8) | buf[5]);
    // buf[6..7] = temperature (skip)
    d->gx = (int16_t)((buf[8] << 8) | buf[9]);
    d->gy = (int16_t)((buf[10] << 8) | buf[11]);
    d->gz = (int16_t)((buf[12] << 8) | buf[13]);
}

int main(void) {
    i2c_init();
    if (!mpu_init()) while(1);  // halt if not found

    MPU_Data data;
    while (1) {
        mpu_read(&data);
        // data.ax/ay/az: accel raw (div by 16384 -> g)
        // data.gx/gy/gz: gyro raw (div by 131 -> dps)
        _delay_ms(50);
    }
}
'''
},
{
    'title': 'Протокол SPI: подробности',
    'estimated_minutes': 22,
    'content': '''
<h3>Режимы SPI: CPOL и CPHA</h3>
<p>SPI имеет 4 режима, определяемых комбинацией битов CPOL (полярность тактового
сигнала) и CPHA (фаза выборки данных):</p>

<table class="theory-table">
<thead><tr><th>Mode</th><th>CPOL</th><th>CPHA</th><th>Состояние SCK в покое</th><th>Выборка данных</th></tr></thead>
<tbody>
<tr><td>0</td><td>0</td><td>0</td><td>LOW</td><td>По переднему фронту (rising)</td></tr>
<tr><td>1</td><td>0</td><td>1</td><td>LOW</td><td>По заднему фронту (falling)</td></tr>
<tr><td>2</td><td>1</td><td>0</td><td>HIGH</td><td>По заднему фронту (falling)</td></tr>
<tr><td>3</td><td>1</td><td>1</td><td>HIGH</td><td>По переднему фронту (rising)</td></tr>
</tbody>
</table>

<p>Большинство устройств работают в Mode 0 (CPOL=0, CPHA=0). Важно проверять
даташит каждого устройства!</p>

<h3>Мультислейв: несколько устройств на одной шине</h3>
<p>MOSI, MISO и SCK — общие для всех устройств. Каждый слейв имеет свой вывод CS
(Chip Select), управляемый отдельным пином МК:</p>
<pre><code>            SCK  --------+--------+--------+
Master      MOSI --------+--------+--------+
            MISO --------+--------+--------+
            PB2  --------| CS (SD card)
            PB1  --------| CS (DAC MCP4921)
            PD7  --------| CS (Display)</code></pre>

<p>Правила работы с мультислейвом:</p>
<ul>
  <li>В любой момент активен только один CS (LOW)</li>
  <li>Все остальные CS должны быть HIGH</li>
  <li>Перед переключением на другое устройство — завершить текущую транзакцию</li>
  <li>Разные устройства могут требовать разных режимов SPI — переключать SPCR!</li>
</ul>

<h3>Скорость SPI</h3>
<p>Тактовая частота SPI задаётся делителем системной частоты:</p>
<table class="theory-table">
<thead><tr><th>SPI2X</th><th>SPR1</th><th>SPR0</th><th>Делитель</th><th>F_SPI при 16 МГц</th></tr></thead>
<tbody>
<tr><td>0</td><td>0</td><td>0</td><td>/4</td><td>4 МГц</td></tr>
<tr><td>0</td><td>0</td><td>1</td><td>/16</td><td>1 МГц</td></tr>
<tr><td>0</td><td>1</td><td>0</td><td>/64</td><td>250 кГц</td></tr>
<tr><td>0</td><td>1</td><td>1</td><td>/128</td><td>125 кГц</td></tr>
<tr><td>1</td><td>0</td><td>0</td><td>/2</td><td>8 МГц</td></tr>
</tbody>
</table>

<h3>SD-карта по SPI</h3>
<p>SD-карта поддерживает SPI Mode 0. Инициализация требует особой процедуры:</p>
<ul>
  <li>Подать 80+ тактов SCK с CS=HIGH (для перехода в SPI-режим)</li>
  <li>CMD0 (GO_IDLE_STATE) с CS=LOW — карта ответит 0x01</li>
  <li>CMD8 — проверка версии (SD v2)</li>
  <li>ACMD41 — инициализация</li>
  <li>CMD58 — проверка типа (SDHC/SDXC)</li>
</ul>
<p>SD-карта работает на пониженной скорости SPI при инициализации (100-400 кГц),
после чего можно увеличить до максимума (до 25 МГц для SD, обычно ограничивают
до 4-8 МГц).</p>
''',
    'code_example': '''#include <avr/io.h>
#include <util/delay.h>

// SPI pins (ATmega328P)
#define SPI_DDR  DDRB
#define SPI_PORT PORTB
#define SPI_SS   PB2
#define SPI_MOSI PB3
#define SPI_MISO PB4
#define SPI_SCK  PB5

// CS pins for multiple slaves
#define SD_CS_DDR   DDRB
#define SD_CS_PORT  PORTB
#define SD_CS_PIN   PB2

#define DAC_CS_DDR  DDRB
#define DAC_CS_PORT PORTB
#define DAC_CS_PIN  PB1

#define SD_CS_LOW()   (SD_CS_PORT  &= ~(1 << SD_CS_PIN))
#define SD_CS_HIGH()  (SD_CS_PORT  |=  (1 << SD_CS_PIN))
#define DAC_CS_LOW()  (DAC_CS_PORT &= ~(1 << DAC_CS_PIN))
#define DAC_CS_HIGH() (DAC_CS_PORT |=  (1 << DAC_CS_PIN))

void spi_init(void) {
    // Set outputs: MOSI, SCK, SS, DAC_CS
    SPI_DDR |= (1 << SPI_MOSI) | (1 << SPI_SCK) | (1 << SPI_SS);
    DAC_CS_DDR |= (1 << DAC_CS_PIN);

    // All CS high (deselect)
    SD_CS_HIGH();
    DAC_CS_HIGH();

    // Enable SPI, Master, Mode 0, fck/16 (1 MHz)
    SPCR = (1 << SPE) | (1 << MSTR) | (1 << SPR0);
}

// Change SPI speed
void spi_set_speed_slow(void) {
    // fck/128 = 125 kHz (for SD init)
    SPCR = (SPCR & ~0x03) | (1 << SPR1) | (1 << SPR0);
    SPSR &= ~(1 << SPI2X);
}

void spi_set_speed_fast(void) {
    // fck/4 = 4 MHz (for SD data transfer)
    SPCR &= ~0x03;  // SPR1=0, SPR0=0
    SPSR &= ~(1 << SPI2X);
}

uint8_t spi_transfer(uint8_t data) {
    SPDR = data;
    while (!(SPSR & (1 << SPIF)));
    return SPDR;
}

// --- SD Card basic commands ---
uint8_t sd_send_cmd(uint8_t cmd, uint32_t arg) {
    spi_transfer(0x40 | cmd);           // Command byte
    spi_transfer((uint8_t)(arg >> 24));
    spi_transfer((uint8_t)(arg >> 16));
    spi_transfer((uint8_t)(arg >> 8));
    spi_transfer((uint8_t)(arg));

    uint8_t crc = 0xFF;
    if (cmd == 0) crc = 0x95;  // valid CRC for CMD0
    if (cmd == 8) crc = 0x87;  // valid CRC for CMD8
    spi_transfer(crc);

    // Wait for response (up to 8 bytes)
    uint8_t res;
    for (uint8_t i = 0; i < 8; i++) {
        res = spi_transfer(0xFF);
        if (res != 0xFF) break;
    }
    return res;
}

uint8_t sd_init(void) {
    spi_set_speed_slow();  // 125 kHz for init

    SD_CS_HIGH();
    // 80 clock pulses with CS high
    for (uint8_t i = 0; i < 10; i++) spi_transfer(0xFF);

    SD_CS_LOW();
    // CMD0: GO_IDLE_STATE
    uint8_t r = sd_send_cmd(0, 0);
    SD_CS_HIGH();
    spi_transfer(0xFF);
    if (r != 0x01) return 0;  // error

    // CMD8: check voltage
    SD_CS_LOW();
    r = sd_send_cmd(8, 0x000001AA);
    if (r == 0x01) {
        // SD v2 card: read 4 bytes of R7 response
        for (uint8_t i = 0; i < 4; i++) spi_transfer(0xFF);
    }
    SD_CS_HIGH();
    spi_transfer(0xFF);

    spi_set_speed_fast();  // 4 MHz for data
    return 1;
}

int main(void) {
    spi_init();
    sd_init();
    while (1);
}
'''
},
],

# ======================================================================
# M9: Программирование на ассемблере AVR — 3 new lessons
# ======================================================================
'Программирование на ассемблере AVR': [
{
    'title': 'Арифметические и логические операции',
    'estimated_minutes': 20,
    'content': '''
<h3>Арифметические инструкции AVR</h3>
<p>AVR имеет набор 8-битных арифметических инструкций. Для 16-битных операций
используются пары регистров.</p>

<table class="theory-table">
<thead><tr><th>Инструкция</th><th>Операция</th><th>Флаги</th></tr></thead>
<tbody>
<tr><td>ADD Rd, Rr</td><td>Rd = Rd + Rr</td><td>C, Z, N, V, H</td></tr>
<tr><td>ADC Rd, Rr</td><td>Rd = Rd + Rr + C</td><td>C, Z, N, V, H</td></tr>
<tr><td>SUB Rd, Rr</td><td>Rd = Rd - Rr</td><td>C, Z, N, V, H</td></tr>
<tr><td>SBC Rd, Rr</td><td>Rd = Rd - Rr - C</td><td>C, Z, N, V, H</td></tr>
<tr><td>SUBI Rd, K</td><td>Rd = Rd - K (только R16-R31)</td><td>C, Z, N, V, H</td></tr>
<tr><td>INC Rd</td><td>Rd = Rd + 1</td><td>Z, N, V (не C!)</td></tr>
<tr><td>DEC Rd</td><td>Rd = Rd - 1</td><td>Z, N, V (не C!)</td></tr>
<tr><td>MUL Rd, Rr</td><td>R1:R0 = Rd * Rr (unsigned)</td><td>C, Z</td></tr>
<tr><td>MULS Rd, Rr</td><td>R1:R0 = Rd * Rr (signed)</td><td>C, Z</td></tr>
</tbody>
</table>

<h3>Логические инструкции</h3>
<table class="theory-table">
<thead><tr><th>Инструкция</th><th>Операция</th><th>Применение</th></tr></thead>
<tbody>
<tr><td>AND Rd, Rr</td><td>Rd = Rd AND Rr</td><td>Маскирование (сброс) битов</td></tr>
<tr><td>ANDI Rd, K</td><td>Rd = Rd AND K</td><td>Маска с константой (R16-R31)</td></tr>
<tr><td>OR Rd, Rr</td><td>Rd = Rd OR Rr</td><td>Установка битов</td></tr>
<tr><td>ORI Rd, K</td><td>Rd = Rd OR K</td><td>Установка бит с константой</td></tr>
<tr><td>EOR Rd, Rr</td><td>Rd = Rd XOR Rr</td><td>Инвертирование битов</td></tr>
<tr><td>COM Rd</td><td>Rd = 0xFF - Rd</td><td>Побитовое НЕ (дополнение до 1)</td></tr>
<tr><td>NEG Rd</td><td>Rd = 0x00 - Rd</td><td>Дополнение до 2 (смена знака)</td></tr>
</tbody>
</table>

<h3>Инструкции сдвига</h3>
<table class="theory-table">
<thead><tr><th>Инструкция</th><th>Операция</th><th>Описание</th></tr></thead>
<tbody>
<tr><td>LSL Rd</td><td>C &lt;- b7...b0 &lt;- 0</td><td>Логический сдвиг влево (= умножение на 2)</td></tr>
<tr><td>LSR Rd</td><td>0 -> b7...b0 -> C</td><td>Логический сдвиг вправо (= деление на 2)</td></tr>
<tr><td>ROL Rd</td><td>C &lt;- b7...b0 &lt;- C</td><td>Циклический сдвиг влево через перенос</td></tr>
<tr><td>ROR Rd</td><td>C -> b7...b0 -> C</td><td>Циклический сдвиг вправо через перенос</td></tr>
<tr><td>ASR Rd</td><td>b7 -> b7...b0 -> C</td><td>Арифметический сдвиг вправо (сохраняет знак)</td></tr>
</tbody>
</table>

<h3>16-битная арифметика</h3>
<p>Для сложения 16-битных чисел используется пара ADD/ADC:</p>
<pre><code>; R17:R16 = R17:R16 + R19:R18
ADD  R16, R18    ; сложить младшие байты
ADC  R17, R19    ; сложить старшие + перенос</code></pre>
<p>Аналогично вычитание: SUB для младшего байта, SBC для старшего.</p>
''',
    'code_example': '''; ==========================================
; Арифметические и логические операции AVR
; ==========================================
.include "m328pdef.inc"

.org 0x0000
    rjmp    main

main:
    ; --- 8-битное сложение ---
    ldi     r16, 100        ; r16 = 100
    ldi     r17, 55         ; r17 = 55
    add     r16, r17        ; r16 = 155

    ; --- 16-битное сложение ---
    ; r25:r24 = 1000 (0x03E8)
    ldi     r24, 0xE8       ; low byte
    ldi     r25, 0x03       ; high byte
    ; r27:r26 = 2500 (0x09C4)
    ldi     r26, 0xC4
    ldi     r27, 0x09
    ; r25:r24 = r25:r24 + r27:r26
    add     r24, r26        ; add low bytes
    adc     r25, r27        ; add high bytes + carry
    ; Result: r25:r24 = 3500 (0x0DAC)

    ; --- Умножение 8x8 -> 16 ---
    ldi     r16, 25
    ldi     r17, 10
    mul     r16, r17        ; R1:R0 = 250

    ; --- Битовые маски ---
    ldi     r16, 0b11010110
    andi    r16, 0x0F       ; r16 = 0b00000110 (маска нижнего нибла)

    ldi     r17, 0b00001010
    ori     r17, 0b11110000 ; r17 = 0b11111010 (установить верхние 4 бита)

    ; --- Проверка бита ---
    ldi     r16, 0b00100000
    andi    r16, (1 << 5)   ; Z=0 если бит 5 установлен
    breq    bit_clear
    ; bit is set
bit_clear:

    ; --- Сдвиги ---
    ldi     r16, 0b00001100 ; r16 = 12
    lsl     r16              ; r16 = 24 (x2)
    lsl     r16              ; r16 = 48 (x4)
    lsr     r16              ; r16 = 24 (div 2)

    ; --- Умножение на 10 через сдвиги ---
    ; x*10 = x*8 + x*2
    ldi     r16, 7          ; r16 = 7
    mov     r17, r16        ; r17 = 7 (save copy)
    lsl     r16              ; r16 = 14  (x2)
    mov     r18, r16        ; save x*2
    lsl     r16              ; r16 = 28  (x4)
    lsl     r16              ; r16 = 56  (x8)
    add     r16, r18        ; r16 = 56 + 14 = 70 = 7*10

loop:
    rjmp    loop
'''
},
{
    'title': 'Работа с таблицами в Flash (LPM)',
    'estimated_minutes': 20,
    'content': '''
<h3>Инструкция LPM — Load Program Memory</h3>
<p>Данные, хранящиеся в Flash-памяти (программной памяти), нельзя прочитать
обычными инструкциями LD/LDS. Для этого используется <code>LPM</code> (Load Program
Memory).</p>

<h3>Формы инструкции LPM</h3>
<table class="theory-table">
<thead><tr><th>Форма</th><th>Операция</th><th>Описание</th></tr></thead>
<tbody>
<tr><td>LPM</td><td>R0 = Flash[Z]</td><td>Загрузить байт по адресу Z в R0</td></tr>
<tr><td>LPM Rd, Z</td><td>Rd = Flash[Z]</td><td>Загрузить в произвольный регистр</td></tr>
<tr><td>LPM Rd, Z+</td><td>Rd = Flash[Z], Z++</td><td>Загрузить и увеличить Z (пост-инкремент)</td></tr>
</tbody>
</table>

<p>Регистр Z (R31:R30) содержит <strong>байтовый адрес</strong> во Flash. Поскольку
Flash адресуется по словам (2 байта), метка таблицы умножается на 2:</p>
<pre><code>ldi   ZL, low(table * 2)
ldi   ZH, high(table * 2)</code></pre>

<h3>Таблица синусов</h3>
<p>Для генерации синусоидальных сигналов (ЦАП, ШИМ) удобно хранить предвычисленную
таблицу значений sin(x) во Flash. 256 значений (один период) дают разрешение 1.4 градуса.</p>

<h3>Таблица ASCII-символов</h3>
<p>Для вывода на 7-сегментный индикатор или матричный дисплей хранят таблицу
соответствия символов их графическому представлению (какие сегменты включать).</p>

<h3>Директива .db</h3>
<p>Данные во Flash объявляются директивой <code>.db</code> (define byte):</p>
<pre><code>.db 0, 25, 50, 74, 98, 120, ...    ; числовые значения
.db "Hello", 0                       ; строка с нуль-терминатором</code></pre>
<p>Если число байтов нечётное, ассемблер автоматически добавляет нулевой байт
для выравнивания по слову.</p>

<h3>Применение таблиц</h3>
<ul>
  <li>Генерация сигналов произвольной формы (синус, треугольник, пила)</li>
  <li>Линеаризация датчиков (NTC-термистор, фоторезистор)</li>
  <li>Перекодировка (BCD -> 7-сегментный код)</li>
  <li>Текстовые строки и меню для LCD</li>
</ul>
''',
    'code_example': '''; ==========================================
; Работа с таблицами во Flash (LPM)
; ==========================================
.include "m328pdef.inc"

.org 0x0000
    rjmp    main

main:
    ; === Пример 1: Таблица 7-сегментного кода ===
    ; Получить код для цифры 5
    ldi     r16, 5              ; индекс (цифра)
    ldi     ZL, low(seg7_table * 2)
    ldi     ZH, high(seg7_table * 2)
    add     ZL, r16             ; смещение
    clr     r17
    adc     ZH, r17             ; перенос в старший байт
    lpm     r0, Z               ; r0 = код для цифры 5
    ; Вывод на порт (r0 -> PORTD)
    out     DDRD, r16           ; DDRD = 0xFF (все выходы)
    ldi     r16, 0xFF
    out     DDRD, r16
    out     PORTD, r0

    ; === Пример 2: Таблица синусов (256 значений) ===
    ; Прочитать sin_table[i] для генерации ШИМ-синуса
    ldi     ZL, low(sin_table * 2)
    ldi     ZH, high(sin_table * 2)

    clr     r20                 ; index = 0
sine_loop:
    mov     ZL, r20
    clr     ZH
    subi    ZL, low(-(sin_table * 2))
    sbci    ZH, high(-(sin_table * 2))
    lpm     r16, Z              ; r16 = sin_table[index]
    ; Записать в OCR0A для ШИМ
    out     OCR0A, r16

    inc     r20                 ; index++ (0-255, wraps around)
    rjmp    sine_loop

    ; === Пример 3: Строка из Flash ===
print_msg:
    ldi     ZL, low(hello_msg * 2)
    ldi     ZH, high(hello_msg * 2)
print_loop:
    lpm     r16, Z+             ; загрузить байт, Z++
    cpi     r16, 0              ; конец строки?
    breq    print_done
    ; здесь отправить r16 через UART...
    rjmp    print_loop
print_done:
    rjmp    print_done

; ==========================================
; Данные во Flash
; ==========================================

; Коды для 7-сегментного индикатора (общий катод)
; Сегменты: dp g f e d c b a
seg7_table:
    .db 0b00111111  ; 0
    .db 0b00000110  ; 1
    .db 0b01011011  ; 2
    .db 0b01001111  ; 3
    .db 0b01100110  ; 4
    .db 0b01101101  ; 5
    .db 0b01111101  ; 6
    .db 0b00000111  ; 7
    .db 0b01111111  ; 8
    .db 0b01101111  ; 9

; Таблица синуса (первые 16 из 256 значений, 0-255 амплитуда)
sin_table:
    .db 128, 131, 134, 137, 140, 143, 146, 149
    .db 152, 155, 158, 162, 165, 167, 170, 173
    ; ... (полная таблица: 256 значений)

; Строка сообщения
hello_msg:
    .db "AVR LPM Demo", 13, 10, 0
'''
},
{
    'title': 'Смешанное программирование C + ASM',
    'estimated_minutes': 22,
    'content': '''
<h3>Зачем смешивать C и ассемблер?</h3>
<p>Программирование на чистом ассемблере трудоёмко. Но некоторые задачи требуют
точного контроля над тактами и инструкциями:</p>
<ul>
  <li>Протоколы с жёсткими таймингами (WS2812B, SoftwareSerial, 1-Wire)</li>
  <li>Критичные по скорости участки (обработка прерываний, DSP)</li>
  <li>Прямой доступ к специфическим инструкциям (SLEEP, WDR, SWAP)</li>
</ul>

<h3>Inline ASM в avr-gcc</h3>
<p>Компилятор avr-gcc поддерживает встроенный ассемблер через
конструкцию <code>asm()</code> или <code>__asm__</code>:</p>
<pre><code>asm volatile ("инструкция" : выходы : входы : clobbers);</code></pre>

<h3>Синтаксис операндов</h3>
<table class="theory-table">
<thead><tr><th>Элемент</th><th>Описание</th><th>Пример</th></tr></thead>
<tbody>
<tr><td>Выходы</td><td>"=r"(var) — результат в регистре</td><td>"=r"(result)</td></tr>
<tr><td>Входы</td><td>"r"(var) — переменная в регистре</td><td>"r"(value)</td></tr>
<tr><td>Clobbers</td><td>Регистры, изменяемые ASM-кодом</td><td>"r16", "memory"</td></tr>
<tr><td>volatile</td><td>Запрет оптимизации (не удалять)</td><td>asm volatile(...)</td></tr>
</tbody>
</table>

<h3>Ограничения (constraints)</h3>
<ul>
  <li><strong>"r"</strong> — любой регистр (R0-R31)</li>
  <li><strong>"d"</strong> — верхний регистр (R16-R31, для ANDI/ORI/SUBI/LDI)</li>
  <li><strong>"w"</strong> — верхняя пара (R24-R31, для ADIW/SBIW)</li>
  <li><strong>"I"</strong> — константа 0-63</li>
  <li><strong>"M"</strong> — константа 0-255</li>
  <li><strong>"e"</strong> — указатель (X, Y или Z)</li>
</ul>

<h3>Отдельный ASM-файл</h3>
<p>Для крупных ассемблерных модулей лучше выделить код в отдельный .S файл.
Функции объявляются как <code>.global</code> и вызываются из C через обычные
прототипы. Соглашение о вызовах avr-gcc:</p>
<ul>
  <li>Аргументы: R25:R24 (1-й), R23:R22 (2-й), R21:R20 (3-й)...</li>
  <li>Возврат: R25:R24 (16 бит), R24 (8 бит)</li>
  <li>Сохраняемые (callee-saved): R2-R17, R28-R29</li>
  <li>Изменяемые (caller-saved): R18-R27, R30-R31</li>
</ul>
''',
    'code_example': '''// ==========================================
// Смешанное программирование C + ASM (avr-gcc)
// ==========================================
#include <avr/io.h>
#include <util/delay.h>

// === 1. Простые inline asm вставки ===

// NOP - точная задержка в 1 такт
#define NOP() asm volatile ("nop")

// Запрет/разрешение прерываний
#define CLI() asm volatile ("cli" ::: "memory")
#define SEI() asm volatile ("sei" ::: "memory")

// Сброс Watchdog Timer
#define WDR() asm volatile ("wdr")

// Swap nibbles (обмен полубайтов)
static inline uint8_t swap_nibbles(uint8_t x) {
    asm volatile ("swap %0" : "=r"(x) : "0"(x));
    return x;
}

// === 2. Inline asm с операндами ===

// Быстрое умножение 8x8 -> 16 (аппаратное MUL)
static inline uint16_t fast_mul8(uint8_t a, uint8_t b) {
    uint16_t result;
    asm volatile (
        "mul %A1, %A2"  "\\n\\t"
        "movw %0, r0"   "\\n\\t"
        "clr r1"         "\\n\\t"  // gcc expects r1 = 0
        : "=r"(result)
        : "r"(a), "r"(b)
        : "r0", "r1"
    );
    return result;
}

// CRC8 calculation (optimized asm)
static uint8_t crc8_update(uint8_t crc, uint8_t data) {
    uint8_t i = 8;
    asm volatile (
        "eor  %0, %1"       "\\n\\t"
    "1: "
        "lsr  %0"           "\\n\\t"
        "brcc 2f"           "\\n\\t"
        "eor  %0, %3"       "\\n\\t"
    "2: "
        "dec  %2"           "\\n\\t"
        "brne 1b"           "\\n\\t"
        : "=r"(crc), "+r"(data), "+r"(i)
        : "r"((uint8_t)0x8C)  // polynomial
    );
    return crc;
}

// === 3. Precise timing for WS2812B LED ===
// Each bit needs exact timing: T0H=350ns, T1H=900ns, T0L=900ns, T1L=350ns

void ws2812_send_byte(uint8_t byte, volatile uint8_t *port, uint8_t pin) {
    uint8_t mask_hi = *port | pin;
    uint8_t mask_lo = *port & ~pin;
    uint8_t i = 8;

    asm volatile (
    "loop%=:"                   "\\n\\t"
        "st   %a[port], %[hi]"  "\\n\\t"  // pin HIGH
        "sbrs %[byte], 7"       "\\n\\t"  // skip if bit 7 set
        "st   %a[port], %[lo]"  "\\n\\t"  // pin LOW (for 0 bit)
        "lsl  %[byte]"          "\\n\\t"  // shift to next bit
        "nop" "\\n\\t" "nop"    "\\n\\t"
        "st   %a[port], %[lo]"  "\\n\\t"  // pin LOW
        "dec  %[cnt]"           "\\n\\t"
        "brne loop%="           "\\n\\t"
        : [byte] "+r"(byte), [cnt] "+r"(i)
        : [port] "e"(port), [hi] "r"(mask_hi), [lo] "r"(mask_lo)
    );
}

// === 4. External ASM function (in .S file) ===
// In fast_add.S:
//   .global fast_add32
//   fast_add32:
//     add r22, r18
//     adc r23, r19
//     adc r24, r20
//     adc r25, r21
//     ret
// In C: extern uint32_t fast_add32(uint32_t a, uint32_t b);

int main(void) {
    DDRB |= (1 << PB5);  // LED

    uint8_t x = 0xA5;
    uint8_t swapped = swap_nibbles(x);  // 0x5A

    uint16_t product = fast_mul8(25, 10); // 250

    // CRC8 of a message
    uint8_t crc = 0;
    const char msg[] = "Hello";
    for (uint8_t i = 0; msg[i]; i++) {
        crc = crc8_update(crc, msg[i]);
    }

    while (1) {
        PORTB ^= (1 << PB5);
        _delay_ms(500);
    }
}
'''
},
],

# ======================================================================
# M10: Проектирование МПС: от схемы до прошивки — 3 new lessons
# ======================================================================
'Проектирование МПС: от схемы до прошивки': [
{
    'title': 'Разработка печатных плат',
    'estimated_minutes': 20,
    'content': '''
<h3>От макетной платы к печатной</h3>
<p>Макетная плата (breadboard) хороша для прототипирования, но ненадёжна для
готового устройства. Печатная плата (PCB) обеспечивает надёжные соединения,
компактность и воспроизводимость.</p>

<h3>KiCad — свободная САПР для электроники</h3>
<p>KiCad — бесплатная и открытая система проектирования печатных плат. Основные
модули:</p>
<table class="theory-table">
<thead><tr><th>Модуль</th><th>Назначение</th></tr></thead>
<tbody>
<tr><td>Schematic Editor</td><td>Создание принципиальной электрической схемы</td></tr>
<tr><td>Symbol Editor</td><td>Создание и редактирование символов компонентов</td></tr>
<tr><td>PCB Editor</td><td>Разводка печатной платы</td></tr>
<tr><td>Footprint Editor</td><td>Создание посадочных мест компонентов</td></tr>
<tr><td>Gerber Viewer</td><td>Просмотр файлов для производства</td></tr>
<tr><td>3D Viewer</td><td>3D-визуализация платы</td></tr>
</tbody>
</table>

<h3>Процесс проектирования PCB</h3>
<ul>
  <li><strong>1. Схема</strong> — создать принципиальную схему в Schematic Editor</li>
  <li><strong>2. Назначение посадочных мест</strong> — каждому символу привязать footprint</li>
  <li><strong>3. Netlist</strong> — сгенерировать список соединений</li>
  <li><strong>4. Размещение</strong> — расположить компоненты на плате</li>
  <li><strong>5. Трассировка</strong> — проложить дорожки между компонентами</li>
  <li><strong>6. DRC</strong> — проверка правил проектирования</li>
  <li><strong>7. Gerber</strong> — экспорт файлов для производства</li>
</ul>

<h3>Основы трассировки</h3>
<p>Правила разводки для цифровых схем на микроконтроллерах:</p>
<ul>
  <li>Ширина дорожки: <strong>0.25 мм</strong> для сигнальных, <strong>0.5-1 мм</strong> для питания</li>
  <li>Зазор между дорожками: минимум <strong>0.2 мм</strong> (для домашнего изготовления — 0.3 мм)</li>
  <li>Переходные отверстия (via): диаметр 0.3-0.4 мм</li>
  <li>Земляной полигон (ground plane) — залить свободное пространство медью, подключённой к GND</li>
</ul>

<h3>Правила размещения компонентов</h3>
<table class="theory-table">
<thead><tr><th>Правило</th><th>Пояснение</th></tr></thead>
<tbody>
<tr><td>Конденсаторы развязки</td><td>100 нФ максимально близко к VCC/GND каждой ИС</td></tr>
<tr><td>Кварцевый резонатор</td><td>Как можно ближе к выводам XTAL1/XTAL2 МК</td></tr>
<tr><td>Разъёмы</td><td>По краям платы</td></tr>
<tr><td>Силовые компоненты</td><td>Отдельно от чувствительных аналоговых цепей</td></tr>
<tr><td>Длина дорожек</td><td>Минимальная для высокочастотных сигналов (SPI SCK, UART)</td></tr>
</tbody>
</table>
''',
    'code_example': '''// Типичная обвязка ATmega328P для печатной платы
// Этот код определяет пины и инициализацию для custom PCB

#include <avr/io.h>
#include <util/delay.h>

// === Pin assignments for custom PCB ===
// Status LEDs
#define LED_DDR   DDRC
#define LED_PORT  PORTC
#define LED_PWR   PC0   // Green - power indicator
#define LED_ACT   PC1   // Yellow - activity
#define LED_ERR   PC2   // Red - error

// User button
#define BTN_DDR   DDRD
#define BTN_PORT  PORTD
#define BTN_PIN   PIND
#define BTN_USER  PD2   // INT0

// I2C sensor bus
// SDA = PC4, SCL = PC5 (hardware TWI)

// SPI peripheral bus
// MOSI = PB3, MISO = PB4, SCK = PB5
#define SPI_CS_FLASH PB0  // External flash
#define SPI_CS_SD    PB1  // SD card
#define SPI_CS_DAC   PB2  // DAC output

// UART debug port
// TXD = PD1, RXD = PD0

// === Board initialization ===
void board_init(void) {
    // LED outputs
    LED_DDR |= (1 << LED_PWR) | (1 << LED_ACT) | (1 << LED_ERR);
    LED_PORT |= (1 << LED_PWR);  // Power LED on

    // Button input with pull-up
    BTN_DDR &= ~(1 << BTN_USER);
    BTN_PORT |= (1 << BTN_USER); // internal pull-up

    // SPI CS pins as outputs, all high (deselected)
    DDRB |= (1 << SPI_CS_FLASH) | (1 << SPI_CS_SD) | (1 << SPI_CS_DAC);
    PORTB |= (1 << SPI_CS_FLASH) | (1 << SPI_CS_SD) | (1 << SPI_CS_DAC);
}

void led_set(uint8_t led, uint8_t state) {
    if (state) LED_PORT |= (1 << led);
    else       LED_PORT &= ~(1 << led);
}

uint8_t button_pressed(void) {
    if (!(BTN_PIN & (1 << BTN_USER))) {
        _delay_ms(20);  // debounce
        if (!(BTN_PIN & (1 << BTN_USER))) {
            while (!(BTN_PIN & (1 << BTN_USER)));  // wait release
            return 1;
        }
    }
    return 0;
}

// === Power-on self-test ===
void board_self_test(void) {
    // Blink all LEDs
    for (uint8_t i = 0; i < 3; i++) {
        LED_PORT |= (1 << LED_PWR) | (1 << LED_ACT) | (1 << LED_ERR);
        _delay_ms(200);
        LED_PORT &= ~((1 << LED_ACT) | (1 << LED_ERR));
        _delay_ms(200);
    }
    led_set(LED_PWR, 1);  // leave power LED on
}

int main(void) {
    board_init();
    board_self_test();

    while (1) {
        if (button_pressed()) {
            led_set(LED_ACT, 1);
            _delay_ms(500);
            led_set(LED_ACT, 0);
        }
    }
}
'''
},
{
    'title': 'Отладка аппаратуры',
    'estimated_minutes': 22,
    'content': '''
<h3>Инструменты отладки</h3>
<p>Отладка аппаратных проблем требует измерительных приборов. Два основных
инструмента разработчика встраиваемых систем:</p>

<h3>1. Осциллограф</h3>
<p>Осциллограф показывает форму электрического сигнала во времени. Позволяет
увидеть:</p>
<ul>
  <li>Форму и амплитуду сигнала (прямоугольник, синус, пила)</li>
  <li>Частоту и длительность импульсов</li>
  <li>Фронты нарастания/спада</li>
  <li>Шумы, выбросы, звон (ringing)</li>
  <li>Декодирование протоколов (UART, SPI, I2C)</li>
</ul>
<p>Бюджетные USB-осциллографы (Hantek, DSLogic) подходят для учебных целей.
Для серьёзной работы — Rigol DS1054Z (4 канала, 50 МГц).</p>

<h3>2. Логический анализатор</h3>
<p>Логический анализатор фиксирует цифровые сигналы (0/1) на нескольких каналах
одновременно. Идеален для отладки протоколов:</p>
<ul>
  <li>8-16 каналов одновременно</li>
  <li>Частота дискретизации 24-200 МГц</li>
  <li>Декодирование: UART, SPI, I2C, 1-Wire, JTAG и др.</li>
  <li>Популярный: Saleae Logic / клоны (ПО Sigrok/PulseView)</li>
</ul>

<h3>Типичные проблемы и их диагностика</h3>

<table class="theory-table">
<thead><tr><th>Проблема</th><th>Симптомы</th><th>Решение</th></tr></thead>
<tbody>
<tr><td>Плохое питание</td><td>МК зависает, сбрасывается, нестабильная работа</td>
    <td>Конденсатор 100 нФ у каждой ИС, электролит 100 мкФ на входе</td></tr>
<tr><td>Земляная петля</td><td>Шум на аналоговых входах, ложные срабатывания</td>
    <td>Звездообразная разводка земли, разделение AGND и DGND</td></tr>
<tr><td>Развязка питания</td><td>Провалы VCC при переключении нагрузки</td>
    <td>Конденсаторы 100 нФ керамика + 10 мкФ танталовый у каждой ИС</td></tr>
<tr><td>Звон на фронтах</td><td>Ложные срабатывания, ошибки данных</td>
    <td>Последовательный резистор 33-100 Ом в линии сигнала</td></tr>
<tr><td>Дребезг контактов</td><td>Множественные срабатывания кнопки</td>
    <td>RC-фильтр (10к + 100нФ) или программный антидребезг</td></tr>
<tr><td>Наводки</td><td>Случайные данные на длинных линиях</td>
    <td>Экранированный кабель, витая пара, снижение скорости</td></tr>
</tbody>
</table>

<h3>Методика поиска неисправностей</h3>
<ul>
  <li><strong>1. Питание</strong> — проверить VCC мультиметром (5.0 +/- 0.25 В)</li>
  <li><strong>2. Тактирование</strong> — осциллограф на XTAL1 (должен быть синус 16 МГц)</li>
  <li><strong>3. Сброс</strong> — проверить RESET (должен быть HIGH при работе)</li>
  <li><strong>4. Сигналы</strong> — логическим анализатором проверить протокол (UART/SPI/I2C)</li>
  <li><strong>5. Программа</strong> — моргание светодиодом в начале main() = МК запустился</li>
</ul>
''',
    'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

// === Debug helpers for hardware troubleshooting ===

// Debug LED on PB5 (Arduino pin 13)
#define DBG_LED_INIT() (DDRB |= (1 << PB5))
#define DBG_LED_ON()   (PORTB |= (1 << PB5))
#define DBG_LED_OFF()  (PORTB &= ~(1 << PB5))
#define DBG_LED_TOG()  (PORTB ^= (1 << PB5))

// Blink pattern to indicate status
// 1 blink = power OK, 2 = UART OK, 3 = sensor OK
void debug_blink(uint8_t count) {
    for (uint8_t i = 0; i < count; i++) {
        DBG_LED_ON();
        _delay_ms(150);
        DBG_LED_OFF();
        _delay_ms(150);
    }
    _delay_ms(500);  // gap between patterns
}

// === UART debug output ===
void uart_init_debug(void) {
    UBRR0H = 0;
    UBRR0L = 103;  // 9600 @ 16 MHz
    UCSR0B = (1 << TXEN0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_putc(char c) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}

void uart_puts(const char *s) {
    while (*s) uart_putc(*s++);
}

void uart_put_hex(uint8_t val) {
    const char hex[] = "0123456789ABCDEF";
    uart_putc(hex[val >> 4]);
    uart_putc(hex[val & 0x0F]);
}

void uart_put_dec(uint16_t val) {
    char buf[6];
    int8_t i = 0;
    if (val == 0) { uart_putc('0'); return; }
    while (val > 0) {
        buf[i++] = '0' + (val % 10);
        val /= 10;
    }
    while (--i >= 0) uart_putc(buf[i]);
}

// === Voltage measurement (self-test) ===
uint16_t read_vcc_mv(void) {
    // Measure internal 1.1V reference against AVcc
    ADMUX = (1 << REFS0) | 0x0E;  // ref=AVcc, input=1.1V bandgap
    ADCSRA = (1 << ADEN) | 0x07;
    _delay_ms(2);  // settling
    ADCSRA |= (1 << ADSC);
    while (ADCSRA & (1 << ADSC));
    uint16_t adc_val = ADC;
    // Vcc = 1.1V * 1024 / ADC
    return (uint16_t)((1100UL * 1024) / adc_val);
}

// === I2C bus scanner ===
void i2c_scan(void) {
    TWSR = 0;
    TWBR = 72;  // 100 kHz @ 16 MHz
    uart_puts("I2C scan:\\r\\n");
    uint8_t found = 0;
    for (uint8_t addr = 1; addr < 127; addr++) {
        TWCR = (1 << TWINT) | (1 << TWSTA) | (1 << TWEN);
        while (!(TWCR & (1 << TWINT)));
        TWDR = (addr << 1);
        TWCR = (1 << TWINT) | (1 << TWEN);
        while (!(TWCR & (1 << TWINT)));
        if ((TWSR & 0xF8) == 0x18) {  // ACK received
            uart_puts("  0x");
            uart_put_hex(addr);
            uart_puts("\\r\\n");
            found++;
        }
        TWCR = (1 << TWINT) | (1 << TWSTO) | (1 << TWEN);
        _delay_us(10);
    }
    if (!found) uart_puts("  (none)\\r\\n");
}

int main(void) {
    DBG_LED_INIT();
    debug_blink(1);  // Checkpoint 1: MCU started

    uart_init_debug();
    uart_puts("=== Board Self-Test ===\\r\\n");
    debug_blink(2);  // Checkpoint 2: UART OK

    // Check VCC
    uint16_t vcc = read_vcc_mv();
    uart_puts("VCC: ");
    uart_put_dec(vcc);
    uart_puts(" mV\\r\\n");

    // Scan I2C bus
    i2c_scan();

    debug_blink(3);  // Checkpoint 3: self-test complete
    uart_puts("Self-test complete.\\r\\n");

    while (1) {
        DBG_LED_TOG();
        _delay_ms(1000);
    }
}
'''
},
{
    'title': 'Документирование проекта',
    'estimated_minutes': 18,
    'content': '''
<h3>Зачем документировать?</h3>
<p>Документация проекта необходима для:</p>
<ul>
  <li>Передачи проекта другому разработчику или заказчику</li>
  <li>Сопровождения и модификации в будущем</li>
  <li>Производства (сборка, наладка, ремонт)</li>
  <li>Сертификации и допуска к эксплуатации</li>
  <li>Защиты дипломного проекта / курсовой работы</li>
</ul>

<h3>Состав документации проекта МПС</h3>

<table class="theory-table">
<thead><tr><th>Документ</th><th>Содержание</th><th>Формат</th></tr></thead>
<tbody>
<tr><td>Принципиальная схема</td><td>Все компоненты и соединения</td><td>PDF из KiCad/Altium</td></tr>
<tr><td>Перечень элементов</td><td>BOM: номиналы, корпуса, количество</td><td>Таблица (Excel/CSV)</td></tr>
<tr><td>Чертёж печатной платы</td><td>Топология дорожек, слои, размеры</td><td>Gerber / PDF</td></tr>
<tr><td>Описание прошивки</td><td>Алгоритмы, структура кода, API</td><td>Текст + диаграммы</td></tr>
<tr><td>Руководство пользователя</td><td>Подключение, настройка, управление</td><td>Текст + фото</td></tr>
<tr><td>Протокол испытаний</td><td>Результаты тестирования</td><td>Таблица</td></tr>
</tbody>
</table>

<h3>Принципиальная схема</h3>
<p>Схема должна быть читаемой и содержать:</p>
<ul>
  <li>Все компоненты с обозначениями (R1, C1, U1, DD1...)</li>
  <li>Номиналы (10 кОм, 100 нФ, ATmega328P)</li>
  <li>Цепи питания и земли с номиналом напряжения</li>
  <li>Названия сигналов на линиях связи (SDA, SCK, TX, RX...)</li>
  <li>Разъёмы с нумерацией контактов</li>
  <li>Рамку с основной надписью (штамп)</li>
</ul>

<h3>Спецификация (BOM — Bill of Materials)</h3>
<p>Перечень элементов содержит всё необходимое для закупки и сборки:</p>
<pre><code>| Поз. | Обозначение | Наименование        | Кол-во | Корпус  | Примечание |
|------|-------------|---------------------|--------|---------|------------|
| 1    | DD1         | ATmega328P-AU       | 1      | TQFP-32 |            |
| 2    | DD2         | CH340G              | 1      | SOP-16  | USB-UART   |
| 3    | R1-R4       | Резистор 10 кОм     | 4      | 0805    | pull-up    |
| 4    | C1-C4       | Конденсатор 100 нФ  | 4      | 0805    | развязка   |
| 5    | C5          | Конденсатор 10 мкФ  | 1      | 0805    | по питанию |
| 6    | Y1          | Кварц 16 МГц        | 1      | HC-49S  |            |</code></pre>

<h3>Описание прошивки</h3>
<p>Включает:</p>
<ul>
  <li>Общее описание функциональности</li>
  <li>Блок-схему алгоритма (основной цикл, обработчики прерываний)</li>
  <li>Описание модулей и их взаимодействия</li>
  <li>Таблицу используемых ресурсов (таймеры, прерывания, порты)</li>
  <li>Инструкцию по сборке (Makefile, toolchain)</li>
</ul>

<h3>Руководство пользователя</h3>
<p>Пишется для конечного пользователя (не программиста):</p>
<ul>
  <li>Назначение устройства</li>
  <li>Комплектация</li>
  <li>Подключение (схема, фото)</li>
  <li>Порядок включения и работы</li>
  <li>Индикация состояний (что означают светодиоды)</li>
  <li>Устранение неисправностей (FAQ)</li>
  <li>Технические характеристики</li>
</ul>
''',
    'code_example': '''// ==========================================
// Пример: хорошо документированный проект
// Файл: main.c
// Проект: Метеостанция на ATmega328P
// Версия: 1.0
// Дата: 2025-01-15
// Автор: Иванов И.И.
// ==========================================
//
// Описание:
//   Автономная метеостанция с датчиком BME280 (I2C),
//   LCD-дисплеем 16x2 (I2C) и логированием на SD-карту (SPI).
//   Измеряет температуру, влажность и атмосферное давление
//   с интервалом 10 секунд.
//
// Аппаратные ресурсы:
//   Timer1  - интервал измерений (10 с)
//   TWI     - I2C: BME280 (0x76), LCD PCF8574 (0x27)
//   SPI     - SD-карта (CS = PB2)
//   USART0  - отладочный вывод (9600 8N1)
//   ADC0    - напряжение батареи (делитель 2:1)
//   INT0    - кнопка (PD2) переключение экрана
//
// Распиновка:
//   PB2 - SD_CS       PC4 - SDA (I2C)
//   PB3 - MOSI        PC5 - SCL (I2C)
//   PB4 - MISO        PD0 - UART RX
//   PB5 - SCK         PD1 - UART TX
//   PB0 - LED_STATUS  PD2 - BTN (INT0)
//   PC0 - V_BAT (ADC) PD7 - LED_ERROR

#include <avr/io.h>
#include <avr/interrupt.h>

// === Configuration ===
#define MEASURE_INTERVAL_S  10
#define UART_BAUD           9600
#define I2C_FREQ            100000UL
#define BME280_ADDR         0x76
#define LCD_ADDR            0x27

// === Data structures ===
typedef struct {
    int16_t  temperature;  // x100 (e.g., 2350 = 23.50 C)
    uint16_t humidity;     // x100 (e.g., 6520 = 65.20 %)
    uint32_t pressure;     // Pa   (e.g., 101325 = 1013.25 hPa)
    uint16_t battery_mv;   // mV   (e.g., 3700)
    uint32_t timestamp;    // seconds since power-on
} SensorData;

// === Global state ===
volatile uint32_t g_uptime_s = 0;
volatile uint8_t  g_measure_flag = 0;
static SensorData g_last_reading;

// === Timer1 ISR: 1 second tick ===
ISR(TIMER1_COMPA_vect) {
    g_uptime_s++;
    if ((g_uptime_s % MEASURE_INTERVAL_S) == 0) {
        g_measure_flag = 1;
    }
}

// === Function prototypes ===
void system_init(void);
void timer1_init(void);
void bme280_read(SensorData *data);
void lcd_display(const SensorData *data);
void sd_log(const SensorData *data);
void uart_report(const SensorData *data);
uint16_t read_battery(void);

// === Main loop ===
int main(void) {
    system_init();
    timer1_init();
    sei();

    // Initial reading
    g_measure_flag = 1;

    while (1) {
        if (g_measure_flag) {
            g_measure_flag = 0;

            // 1. Read sensors
            bme280_read(&g_last_reading);
            g_last_reading.battery_mv = read_battery();
            g_last_reading.timestamp = g_uptime_s;

            // 2. Display on LCD
            lcd_display(&g_last_reading);

            // 3. Log to SD card
            sd_log(&g_last_reading);

            // 4. Debug output via UART
            uart_report(&g_last_reading);
        }
        // CPU idle between measurements (could enter sleep mode)
    }
}

// Timer1 CTC: 1 Hz interrupt
void timer1_init(void) {
    TCCR1B = (1 << WGM12) | (1 << CS12) | (1 << CS10); // CTC, /1024
    OCR1A = (F_CPU / 1024) - 1;  // 15624 for 16 MHz
    TIMSK1 = (1 << OCIE1A);
}

// Stub implementations (real code in separate modules)
void system_init(void) {
    // init UART, I2C, SPI, GPIO...
}
void bme280_read(SensorData *data) { (void)data; }
void lcd_display(const SensorData *data) { (void)data; }
void sd_log(const SensorData *data) { (void)data; }
void uart_report(const SensorData *data) { (void)data; }
uint16_t read_battery(void) { return 0; }
'''
},
],

}  # end LESSONS_DATA


class Command(BaseCommand):
    help = 'Add 3 new lessons to each of MPS modules 6-10 (15 lessons total)'

    def handle(self, *args, **options):
        try:
            subject = Subject.objects.get(title='Микропроцессорные системы')
        except Subject.DoesNotExist:
            self.stdout.write('ERROR: Subject not found')
            return

        total_created = 0

        for module_title, lessons in LESSONS_DATA.items():
            try:
                module = subject.modules.get(title__icontains=module_title)
            except TheoryModule.DoesNotExist:
                self.stdout.write('  SKIP module not found: ' + module_title)
                continue
            except TheoryModule.MultipleObjectsReturned:
                module = subject.modules.filter(title__icontains=module_title).first()

            # Get max existing order
            max_order = module.lessons.aggregate(Max('order'))['order__max'] or 0

            for lesson_data in lessons:
                obj, created = TheoryLesson.objects.get_or_create(
                    module=module,
                    title=lesson_data['title'],
                    defaults={
                        'content': lesson_data['content'].strip(),
                        'code_example': lesson_data['code_example'].strip(),
                        'order': max_order + 1,
                        'estimated_minutes': lesson_data['estimated_minutes'],
                    }
                )
                if created:
                    max_order += 1
                    total_created += 1
                    self.stdout.write('  + ' + lesson_data['title'])
                else:
                    self.stdout.write('  . exists: ' + lesson_data['title'])

        self.stdout.write('Done. Created: %d lessons' % total_created)
