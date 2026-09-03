"""python manage.py seed_mps_patch2
Расширяет тонкие уроки МПС (< 4500 символов) богатым контентом и диаграммами.
Патчит: M3L1, M4L3, M5L3, M7L2, M8L2, M9L1, M9L3, M10L2, M13L1, M15L2
"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject


def tip(t): return f'<div class="tip">💡 {t}</div>'
def warn(t): return f'<div class="warning">⚠️ {t}</div>'
def info(t): return f'<div class="tip" style="background:#e0f2fe;border-color:#0284c7">ℹ️ {t}</div>'

def table(headers, rows):
    th = ''.join(f'<th>{c}</th>' for c in headers)
    trs = ''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def diagram(svg, w=640, h=300, caption=''):
    return (f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;'
            f'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">'
            f'{svg}</svg>'
            f'<p style="text-align:center;color:#64748b;font-size:13px">{caption}</p></div>')

def box(x, y, w, h, fill, stroke, text, fs=12, fw='normal', tc='#1e293b'):
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    lines = text.split('\n')
    lh = fs + 3
    y0 = y + h // 2 - (lh * len(lines)) // 2 + fs
    spans = ''.join(f'<tspan x="{x+w//2}" dy="{0 if i==0 else lh}">{l}</tspan>' for i, l in enumerate(lines))
    return rect + f'<text x="{x+w//2}" y="{y0}" text-anchor="middle" font-size="{fs}" fill="{tc}" font-weight="{fw}" font-family="sans-serif">{spans}</text>'

def arrow(x1, y1, x2, y2, c='#64748b'):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.5" marker-end="url(#arr)"/>'

DEFS = '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'

def BG(h): return f'<rect width="640" height="{h}" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'


PATCHES = {

# ─── M3 L1: GPIO DDR/PORT/PIN ─────────────────────────────────────────────────
(3,1): {
'title': 'GPIO: регистры DDR, PORT, PIN',
'estimated_minutes': 55,
'content': '''
<h2>GPIO — General Purpose Input/Output</h2>
<p>Каждый порт AVR управляется тремя 8-битными регистрами. Понимание их взаимодействия — основа всей работы с периферией МК.</p>
''' + diagram(
    DEFS + BG(310) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Три регистра одного порта AVR и их взаимодействие</text>' +
    box(20,50,180,50,'#dbeafe','#3b82f6','DDRx\n(Data Direction Register)',11,'bold') +
    box(230,50,180,50,'#dcfce7','#16a34a','PORTx\n(Data Output Register)',11,'bold') +
    box(440,50,180,50,'#fef9c3','#f59e0b','PINx\n(Port Input Pins)',11,'bold') +
    '<text x="110" y="122" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">0 = вход</text>' +
    '<text x="110" y="136" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">1 = выход</text>' +
    '<text x="320" y="122" text-anchor="middle" font-size="10" fill="#15803d" font-family="sans-serif">DDR=1: 0=LOW, 1=HIGH</text>' +
    '<text x="320" y="136" text-anchor="middle" font-size="10" fill="#15803d" font-family="sans-serif">DDR=0: 0=Hi-Z, 1=pull-up</text>' +
    '<text x="530" y="122" text-anchor="middle" font-size="10" fill="#b45309" font-family="sans-serif">Читать ТОЛЬКО для входов</text>' +
    '<text x="530" y="136" text-anchor="middle" font-size="10" fill="#b45309" font-family="sans-serif">Запись в PINx: XOR PORT</text>' +
    # GPIO cell diagram
    '<rect x="20" y="160" width="600" height="130" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="182" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Внутренняя структура одного пина GPIO</text>' +
    box(30,192,80,30,'#dbeafe','#3b82f6','DDRxn=1\nвыход',9) +
    box(30,232,80,30,'#dcfce7','#16a34a','PORTxn\nданные',9) +
    box(130,192,80,40,'#fdf4ff','#a855f7','Выходной\nбуфер',10) +
    '<line x1="110" y1="207" x2="130" y2="212" stroke="#1e293b" stroke-width="1.5"/>' +
    '<line x1="110" y1="247" x2="130" y2="222" stroke="#1e293b" stroke-width="1.5"/>' +
    '<line x1="210" y1="212" x2="270" y2="212" stroke="#1e293b" stroke-width="2"/>' +
    '<circle cx="270" cy="212" r="4" fill="#1e293b"/>' +
    box(280,192,80,40,'#fef9c3','#f59e0b','Pull-up\n~50 кОм',10) +
    '<line x1="270" y1="212" x2="280" y2="212" stroke="#1e293b" stroke-width="1.5"/>' +
    box(380,192,80,40,'#dcfce7','#16a34a','Входной\nбуфер',10) +
    '<line x1="360" y1="212" x2="380" y2="212" stroke="#1e293b" stroke-width="1.5"/>' +
    '<line x1="460" y1="212" x2="510" y2="212" stroke="#1e293b" stroke-width="2"/>' +
    box(510,192,80,30,'#fef9c3','#f59e0b','PINxn\nчтение',9) +
    '<line x1="270" y1="196" x2="270" y2="168" stroke="#1e293b" stroke-width="2"/>' +
    '<text x="270" y="163" text-anchor="middle" font-size="11" fill="#1e293b" font-family="sans-serif">Физический вывод МК</text>',
    640, 310, 'Каждый пин — мультиплексор: выход (буфер), pull-up, или вход'
) +
table(
    ['DDRxn','PORTxn','Режим','Поведение'],
    [
        ['0','0','Вход, Hi-Z','Высокое сопротивление, "висящий вход"'],
        ['0','1','Вход + pull-up','~50 кОм к VCC — стабильный HIGH без нажатия'],
        ['1','0','Выход LOW','Активно тянет вывод к GND, ток до 40 мА'],
        ['1','1','Выход HIGH','Активно тянет вывод к VCC, ток до 40 мА'],
    ]
) +
'''<h3>Атомарные команды SBI/CBI</h3>
<p>AVR имеет специальные однотактные команды для работы с битами регистров I/O (адреса 0x00–0x1F):</p>''' +
table(
    ['Команда','C-аналог','Такты','Применение'],
    [
        ['<code>sbi PORT, n</code>','<code>PORTB |= (1&lt;&lt;n)</code>','1','Установить бит n (атомарно)'],
        ['<code>cbi PORT, n</code>','<code>PORTB &amp;= ~(1&lt;&lt;n)</code>','1','Сбросить бит n (атомарно)'],
        ['<code>sbis PIN, n</code>','if (PINB &amp; (1&lt;&lt;n))','1','Пропустить следующую команду если бит = 1'],
        ['<code>sbic PIN, n</code>','if (!(PINB &amp; (1&lt;&lt;n)))','1','Пропустить следующую команду если бит = 0'],
    ]
) +
info('Запись в PINx (не PORTx!) выполняет аппаратный XOR: <code>PINB = (1&lt;&lt;PB5)</code> инвертирует бит PB5 без чтения-модификации-записи. Это быстрее и атомарно.') +
tip('Всегда инициализируйте DDRx явно в setup(). Не полагайтесь на значения по умолчанию (они 0 = вход, но после загрузчика Arduino могут отличаться).') +
warn('Никогда не читайте PINx сразу после изменения PORTx: данные стабилизируются через один такт. Вставьте команду NOP или читайте в следующем такте.'),
'code_example': '''#include <avr/io.h>
#include <util/delay.h>

// Полный пример работы с GPIO на уровне регистров
int main(void) {
    // === Настройка ===
    DDRB  |=  (1<<PB5);   // PB5 = выход (LED, Arduino pin 13)
    DDRD  &= ~(1<<PD2);   // PD2 = вход (кнопка, pin 2)
    PORTD |=  (1<<PD2);   // включить pull-up на PD2

    // PD3 = вход без pull-up (подключён внешний датчик)
    DDRD  &= ~(1<<PD3);
    PORTD &= ~(1<<PD3);   // Hi-Z

    uint8_t last = 0;

    while (1) {
        // Чтение кнопки (активный LOW — pull-up схема)
        uint8_t btn = !(PIND & (1<<PD2));

        // SBI/CBI — атомарные операции, 1 такт
        if (btn) {
            sbi(PORTB, PB5);   // LED ON (macros из avr/io.h)
        } else {
            cbi(PORTB, PB5);   // LED OFF
        }

        // Мигание при удержании: аппаратный XOR через PINB
        if (btn && btn != last) {
            // Каждое нажатие инвертирует PB4 атомарно
            PINB = (1<<PB4);  // XOR через PINx!
        }
        last = btn;
        _delay_ms(10);
    }
}'''
},

# ─── M4 L3: volatile ──────────────────────────────────────────────────────────
(4,3): {
'title': 'Ключевое слово volatile и защита данных',
'estimated_minutes': 50,
'content': '''
<h2>volatile — гарантия видимости данных между ISR и основным кодом</h2>
<p>Когда переменную изменяет ISR, а читает основной цикл, компилятор не знает о такой «невидимой» модификации. Ключевое слово <code>volatile</code> сообщает компилятору: <em>«каждый раз читай из памяти, не кэшируй в регистр»</em>.</p>
''' + diagram(
    DEFS + BG(270) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Проблема кэширования без volatile</text>' +
    box(20,50,290,100,'#fee2e2','#ef4444','БЕЗ volatile — ОШИБКА',12,'bold','#7f1d1d') +
    '<text x="165" y="95" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="monospace">uint8_t flag = 0;</text>' +
    '<text x="165" y="113" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="monospace">// Компилятор -Os видит:</text>' +
    '<text x="165" y="129" text-anchor="middle" font-size="10" fill="#ef4444" font-family="monospace">// flag = 0, не меняется → while(flag) = false</text>' +
    '<text x="165" y="145" text-anchor="middle" font-size="10" fill="#ef4444" font-family="monospace">// → УДАЛЯЕТ весь while-цикл!</text>' +
    box(330,50,290,100,'#dcfce7','#16a34a','С volatile — ПРАВИЛЬНО',12,'bold','#14532d') +
    '<text x="475" y="95" text-anchor="middle" font-size="10" fill="#14532d" font-family="monospace">volatile uint8_t flag = 0;</text>' +
    '<text x="475" y="113" text-anchor="middle" font-size="10" fill="#14532d" font-family="monospace">// Компилятор ВСЕГДА</text>' +
    '<text x="475" y="129" text-anchor="middle" font-size="10" fill="#15803d" font-family="monospace">// читает flag из SRAM</text>' +
    '<text x="475" y="145" text-anchor="middle" font-size="10" fill="#15803d" font-family="monospace">// ISR меняет → main видит</text>' +
    # Memory model
    '<rect x="20" y="165" width="600" height="90" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="185" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Модель памяти: с volatile и без</text>' +
    box(40,193,240,50,'#fef9c3','#f59e0b','БЕЗ: R16=flag (кэш)\nISR: SRAM[flag]=1\nmain видит R16=0 (устарело)',9) +
    box(360,193,240,50,'#dcfce7','#16a34a','С volatile: ld R16, SRAM[flag]\nISR: SRAM[flag]=1\nmain: ld R16, SRAM[flag]=1 OK',9),
    640, 270, 'volatile = запрет кэширования: каждое обращение — чтение из памяти'
) +
table(
    ['Ситуация','Нужен volatile?','Почему'],
    [
        ['Переменная изменяется в ISR','Да','ISR — независимый поток, компилятор не видит зависимость'],
        ['Переменная изменяется в другом потоке (RTOS)','Да','Аналогично ISR — скрытая модификация'],
        ['Регистр аппаратного устройства (MMIO)','Да','Аппаратура меняет значение без ведома компилятора'],
        ['Локальная переменная внутри функции','Нет','Компилятор видит все изменения'],
        ['Константа','Нет','Неизменяема по определению'],
    ]
) +
'''<h3>Атомарный доступ к составным переменным</h3>
<p>На 8-битном AVR операции с 16/32-битными переменными состоят из нескольких инструкций. ISR может вклиниться между ними:</p>''' +
diagram(
    DEFS + BG(180) +
    '<text x="320" y="25" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="bold" font-family="sans-serif">Гонка данных для 16-битной переменной на 8-битном AVR</text>' +
    box(20,40,180,50,'#fef9c3','#f59e0b','main читает ticks',11) +
    '<text x="110" y="70" text-anchor="middle" font-size="10" fill="#92400e" font-family="monospace">lds R24, ticks_L  ← здесь</text>' +
    '<text x="110" y="85" text-anchor="middle" font-size="10" fill="#dc2626" font-family="monospace">!!! ISR вклинивается</text>' +
    '<text x="110" y="100" text-anchor="middle" font-size="10" fill="#92400e" font-family="monospace">lds R25, ticks_H</text>' +
    box(220,40,180,50,'#fee2e2','#ef4444','ISR меняет ticks',11) +
    '<text x="310" y="70" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="monospace">ticks_L = 0x00</text>' +
    '<text x="310" y="85" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="monospace">ticks_H = 0x01 (перенос!)</text>' +
    box(420,40,200,50,'#dcfce7','#16a34a','Решение: ATOMIC_BLOCK',11) +
    '<text x="520" y="70" text-anchor="middle" font-size="10" fill="#14532d" font-family="monospace">cli();</text>' +
    '<text x="520" y="85" text-anchor="middle" font-size="10" fill="#14532d" font-family="monospace">t = ticks; // безопасно</text>' +
    '<text x="520" y="100" text-anchor="middle" font-size="10" fill="#14532d" font-family="monospace">sei();</text>' +
    '<text x="320" y="155" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">main читает ticks_L=0xFF (старое), ticks_H=0x01 (новое) → ticks=0x01FF вместо 0x00FF или 0x0100!</text>',
    640, 180, 'Между двумя инструкциями чтения LSB и MSB может вклиниться ISR'
) +
tip('Правило: если переменная > 8 бит и разделяется с ISR — защищайте чтение/запись через ATOMIC_BLOCK или временный запрет прерываний cli()/sei().') +
warn('ATOMIC_BLOCK запрещает все прерывания на время блока. Держите блок минимальным — только чтение/запись переменной. Никаких delay() или длинных вычислений внутри!'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/atomic.h>

volatile uint16_t timer_ms = 0;   // изменяется в ISR каждую мс

ISR(TIMER0_COMPA_vect) {
    timer_ms++;    // 16-бит, но ISR не прерывается сама собой — OK
}

// Многобайтная volatile структура
volatile struct {
    uint16_t adc_val;
    uint8_t  new_data;
} sensor;

ISR(ADC_vect) {
    sensor.adc_val = ADC;     // 16-бит атомарно внутри ISR
    sensor.new_data = 1;
}

int main(void) {
    sei();

    while (1) {
        // НЕПРАВИЛЬНО: может прочитать "рваные" данные
        // uint16_t t = timer_ms;

        // ПРАВИЛЬНО: атомарное чтение
        uint16_t t;
        ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
            t = timer_ms;
        }

        // Проверка флага и чтение данных
        if (sensor.new_data) {
            uint16_t val;
            ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
                val = sensor.adc_val;
                sensor.new_data = 0;
            }
            // работаем с val
            (void)val;
        }

        (void)t;
    }
}'''
},

# ─── M5 L3: millis ────────────────────────────────────────────────────────────
(5,3): {
'title': 'Системное время: millis и micros',
'estimated_minutes': 45,
'content': '''
<h2>Функции времени Arduino: millis() и micros()</h2>
<p>Arduino реализует счётчик времени через Timer0, прерывающийся каждые 1.024 мс. Функции millis() и micros() позволяют организовать неблокирующие задержки и периодические задачи.</p>
''' + table(
    ['Функция','Разрешение','Переполнение','Использование'],
    [
        ['<code>millis()</code>','~1 мс','через 49.7 дней','Задержки от 1 мс, периодические задачи'],
        ['<code>micros()</code>','4 мкс (при 16МГц)','через 71.6 минут','Точные короткие задержки'],
        ['<code>_delay_ms(N)</code>','зависит от F_CPU','нет','Блокирующая задержка (compile-time)'],
        ['<code>_delay_us(N)</code>','зависит от F_CPU','нет','Блокирующая задержка в мкс'],
    ]
) + diagram(
    DEFS + BG(240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">delay() vs millis(): разница в поведении</text>' +
    # delay() - blocking
    box(20,50,280,80,'#fee2e2','#ef4444','delay(1000) — БЛОКИРУЕТ',12,'bold','#7f1d1d') +
    '<text x="160" y="90" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">МК ничего не делает 1 секунду</text>' +
    '<text x="160" y="108" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">Кнопки, датчики — не реагирует</text>' +
    '<text x="160" y="124" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">Последовательная обработка</text>' +
    # millis() - non-blocking
    box(340,50,280,80,'#dcfce7','#16a34a','millis() — НЕБЛОКИРУЮЩИЙ',12,'bold','#14532d') +
    '<text x="480" y="90" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">МК работает между проверками</text>' +
    '<text x="480" y="108" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Кнопки, датчики — обрабатывает</text>' +
    '<text x="480" y="124" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Параллельные задачи</text>' +
    # Timeline
    '<rect x="20" y="148" width="600" height="75" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="168" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Переполнение millis() — правильная обработка</text>' +
    '<text x="40" y="190" font-size="10" fill="#64748b" font-family="sans-serif">uint32_t: 0 ... 4 294 967 295 ... 0 (переполнение через 49.7 дней)</text>' +
    '<text x="40" y="208" font-size="10" fill="#16a34a" font-family="monospace">if (millis() - lastTime >= period)  // правильно! работает при переполнении</text>' +
    '<text x="40" y="222" font-size="10" fill="#ef4444" font-family="monospace">if (millis() >= lastTime + period)  // НЕПРАВИЛЬНО! сломается при переполнении',
    640, 245, 'millis()-lastTime корректен при переполнении за счёт арифметики по модулю 2^32'
) +
'''<h3>Паттерн «неблокирующий таймер»</h3>
<p>Основной паттерн для периодических задач без блокировки:</p>
<pre style="background:#1e293b;color:#e2e8f0;padding:14px;border-radius:8px;font-size:12px">
uint32_t lastRun = 0;
const uint32_t PERIOD = 1000;  // мс

void loop() {
    if (millis() - lastRun >= PERIOD) {
        lastRun += PERIOD;     // не = millis()! — точный период
        doTask();
    }
}
</pre>''' +
tip('millis() внутри использует 32-битный счётчик, который прерывание Timer0 инкрементирует каждые ~1 мс. Само прерывание занимает &lt;1 мкс — почти незаметно.') +
warn('micros() имеет разрешение 4 мкс при 16 МГц (каждые 4 такта). При отключённых прерываниях (cli()) счётчик Timer0 не обновляется и micros()/millis() возвращают неверные значения.'),
'code_example': '''#include <Arduino.h>

// Несколько неблокирующих таймеров
struct Timer {
    uint32_t last;
    uint32_t period;
    bool check() {
        if (millis() - last >= period) {
            last += period;
            return true;
        }
        return false;
    }
};

Timer t_led   = {0, 500};    // мигать каждые 500 мс
Timer t_uart  = {0, 1000};   // печатать каждую секунду
Timer t_adc   = {0, 100};    // читать АЦП каждые 100 мс
Timer t_watch = {0, 5000};   // "я жив" каждые 5 сек

bool led_state = false;

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    if (t_led.check()) {
        led_state = !led_state;
        digitalWrite(LED_BUILTIN, led_state);
    }
    if (t_uart.check()) {
        Serial.print("Uptime: ");
        Serial.print(millis() / 1000);
        Serial.println(" sec");
    }
    if (t_adc.check()) {
        int v = analogRead(A0);
        (void)v;  // обработать значение
    }
    if (t_watch.check()) {
        Serial.println("[ALIVE]");
    }

    // Весь loop() выполняется тысячи раз в секунду
    // каждый Timer.check() занимает ~1 мкс
}'''
},

# ─── M7 L2: UART отладка ──────────────────────────────────────────────────────
(7,2): {
'title': 'UART: отладка и протоколы передачи данных',
'estimated_minutes': 50,
'content': '''
<h2>Serial как инструмент отладки</h2>
<p>UART Serial — самый мощный инструмент отладки МК-систем. Когда нет осциллографа или JTAG, Serial.print() позволяет «видеть» внутреннее состояние программы в реальном времени.</p>
''' + diagram(
    DEFS + BG(240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Стратегии UART-отладки</text>' +
    box(20,50,185,55,'#dcfce7','#16a34a','1. Значения переменных\nSerial.print(val)',10) +
    box(220,50,185,55,'#dbeafe','#3b82f6','2. Метки выполнения\nSerial.println("HERE")',10) +
    box(420,50,200,55,'#fef9c3','#f59e0b','3. Временны́е метки\nSerial.print(micros())',10) +
    box(20,115,185,55,'#fdf4ff','#a855f7','4. Состояния FSM\nSerial.print(state)',10) +
    box(220,115,185,55,'#fee2e2','#ef4444','5. Бинарные флаги\nSerial.println(reg,BIN)',10) +
    box(420,115,200,55,'#dcfce7','#16a34a','6. JSON-поток\n{"t":23,"h":65}',10) +
    '<rect x="20" y="182" width="600" height="50" rx="6" fill="#fef9c3" stroke="#f59e0b"/>' +
    '<text x="320" y="202" text-anchor="middle" font-size="11" fill="#92400e" font-weight="bold" font-family="sans-serif">ВАЖНО: Serial.print() занимает время!</text>' +
    '<text x="320" y="220" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">При 9600 бод 1 байт = 1 мс. 10 символов = 10 мс — это нарушает таймеры и ШИМ</text>',
    640, 245, 'Чем выше baud rate, тем меньше влияние Serial.print() на тайминг'
) +
'''<h3>Структурированные протоколы поверх UART</h3>''' +
table(
    ['Протокол','Формат','Преимущества','Применение'],
    [
        ['Текстовый','"T=23.5,H=65\\r\\n"','Читаем человеком, легко парсить','Мониторинг, отладка'],
        ['JSON','\'{"t":23.5,"h":65}\'','Стандарт, много парсеров','IoT, веб-интеграция'],
        ['CSV','"23.5,65,1013\\r\\n"','Минимальный оверхед','Логирование данных'],
        ['Бинарный','[0xAA][LEN][DATA][CRC]','Компактно, быстро','Встраиваемые системы'],
        ['AT-команды','AT+CMD=VAL\\r\\n','Стандарт модемов','BT, Wi-Fi, GSM модули'],
        ['SLIP/COBS','Кадрирование байтами','Надёжное разделение пакетов','Бинарные протоколы'],
    ]
) +
'''<h3>Бинарный протокол с кадрированием</h3>
<p>Для надёжной передачи структур данных используют пакеты с заголовком и CRC:</p>
<pre style="background:#1e293b;color:#e2e8f0;padding:12px;border-radius:8px;font-size:12px">
[0xAA][0x55][LEN_L][LEN_H][CMD][DATA × LEN][CRC8]
  ↑___ magic bytes (синхронизация) ___↑       ↑
</pre>''' +
tip('Serial Plotter в Arduino IDE (Инструменты → Serial Plotter) строит график при выводе чисел через Serial.println(). Удобно для АЦП, гироскопа, температуры.') +
warn('Никогда не вызывайте Serial.print() внутри ISR — функция не является реентерабельной и использует буфер. Из ISR только устанавливайте volatile-флаг, а печатайте в loop().'),
'code_example': '''#include <Arduino.h>

// Отладочные макросы (отключаются в релизе)
#define DEBUG 1
#if DEBUG
  #define LOG(msg)         Serial.println(F(msg))
  #define LOG_VAL(k,v)     do{ Serial.print(F(k)); Serial.println(v); }while(0)
  #define LOG_TIME(msg)    do{ Serial.print(micros()); Serial.print(F(" ")); Serial.println(F(msg)); }while(0)
#else
  #define LOG(msg)
  #define LOG_VAL(k,v)
  #define LOG_TIME(msg)
#endif

// Простой CRC8
uint8_t crc8(uint8_t *data, uint8_t len) {
    uint8_t crc = 0xFF;
    for (uint8_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (uint8_t b = 0; b < 8; b++)
            crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : (crc << 1);
    }
    return crc;
}

// Отправка бинарного пакета
void send_packet(uint8_t cmd, uint8_t *data, uint8_t len) {
    Serial.write(0xAA); Serial.write(0x55);  // magic
    Serial.write(len);   Serial.write(cmd);
    for (int i = 0; i < len; i++) Serial.write(data[i]);
    Serial.write(crc8(data, len));
}

void setup() {
    Serial.begin(115200);
    LOG("Boot OK");
    LOG_TIME("setup done");
}

void loop() {
    float t = 23.5;
    LOG_VAL("Temp=", t);

    // JSON поток для Serial Monitor / Node-RED
    Serial.print("{\"t\":");  Serial.print(t, 1);
    Serial.print(",\"ms\":"); Serial.print(millis());
    Serial.println("}");

    delay(1000);
}'''
},

# ─── M8 L2: SPI ───────────────────────────────────────────────────────────────
(8,2): {
'title': 'Интерфейс SPI — полный дуплекс',
'estimated_minutes': 50,
'content': '''
<h2>SPI — Serial Peripheral Interface</h2>
<p>SPI — синхронный последовательный интерфейс с четырьмя линиями. Разработан Motorola. Главное преимущество над I2C: полный дуплекс (одновременная передача в оба направления) и скорость до 10+ МГц.</p>
''' + diagram(
    DEFS + BG(270) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">SPI: временная диаграмма (Mode 0: CPOL=0, CPHA=0)</text>' +
    # SCK
    '<text x="35" y="65" font-size="10" fill="#3b82f6" font-family="sans-serif">SCK</text>' +
    '<line x1="60" y1="60" x2="60" y2="80" stroke="#3b82f6" stroke-width="2"/>' +
    ''.join(f'<line x1="{60+i*50}" y1="60" x2="{110+i*50}" y2="60" stroke="#3b82f6" stroke-width="2"/>'
            f'<line x1="{110+i*50}" y1="60" x2="{110+i*50}" y2="80" stroke="#3b82f6" stroke-width="2"/>'
            f'<line x1="{110+i*50}" y1="80" x2="{160+i*50}" y2="80" stroke="#3b82f6" stroke-width="2"/>'
            f'<line x1="{160+i*50}" y1="80" x2="{160+i*50}" y2="60" stroke="#3b82f6" stroke-width="2"/>'
            for i in range(8)) +
    # MOSI bits
    '<text x="35" y="120" font-size="10" fill="#16a34a" font-family="sans-serif">MOSI</text>' +
    ''.join(f'<rect x="{60+i*50}" y="100" width="50" height="20" fill="{"#bbf7d0" if (0b10110100 >> (7-i)) & 1 else "#fee2e2"}" stroke="#94a3b8" stroke-width="1"/>'
            f'<text x="{85+i*50}" y="114" text-anchor="middle" font-size="10" fill="#1e293b" font-family="monospace">{(0b10110100 >> (7-i)) & 1}</text>'
            for i in range(8)) +
    '<text x="475" y="114" font-size="10" fill="#16a34a" font-family="sans-serif">= 0xB4</text>' +
    # MISO bits
    '<text x="35" y="165" font-size="10" fill="#f59e0b" font-family="sans-serif">MISO</text>' +
    ''.join(f'<rect x="{60+i*50}" y="145" width="50" height="20" fill="{"#fef3c7" if (0b01001101 >> (7-i)) & 1 else "#fff"}" stroke="#94a3b8" stroke-width="1"/>'
            f'<text x="{85+i*50}" y="159" text-anchor="middle" font-size="10" fill="#1e293b" font-family="monospace">{(0b01001101 >> (7-i)) & 1}</text>'
            for i in range(8)) +
    '<text x="475" y="159" font-size="10" fill="#f59e0b" font-family="sans-serif">= 0x4D</text>' +
    # SS
    '<text x="35" y="210" font-size="10" fill="#ef4444" font-family="sans-serif">SS</text>' +
    '<line x1="60" y1="195" x2="70" y2="195" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="70" y1="195" x2="70" y2="215" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="70" y1="215" x2="460" y2="215" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="460" y1="215" x2="460" y2="195" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="460" y1="195" x2="490" y2="195" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="265" y="235" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">SS=LOW: ведомый активен</text>' +
    '<text x="320" y="255" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">MOSI и MISO меняются одновременно: полный дуплекс за один такт SCK</text>',
    640, 270, 'SPI Mode 0: данные стробируются по нарастающему фронту SCK'
) +
table(
    ['Режим','CPOL','CPHA','Активный фронт','Устройства'],
    [
        ['Mode 0','0','0','Нарастающий (↑)','SD-карта, большинство датчиков'],
        ['Mode 1','0','1','Спадающий (↓)','MAX7219, некоторые АЦП'],
        ['Mode 2','1','0','Спадающий (↓)','Редко'],
        ['Mode 3','1','1','Нарастающий (↑)','ADXL345, некоторые Flash'],
    ]
) +
table(
    ['','I2C','SPI'],
    [
        ['Проводов (без питания)','2','4 (+ 1 на каждый ведомый CS)'],
        ['Скорость','до 400 кбит/с','до 10 МГц (AVR: до F_CPU/2)'],
        ['Несколько ведомых','По адресу','Отдельный CS на каждого'],
        ['Дуплекс','Полу (один пин данных)','Полный (MOSI + MISO одновременно)'],
        ['Подтяжка','4.7 кОм к VCC','Не нужна'],
        ['Протокол','Адрес + ACK','Нет адресации, нет ACK'],
    ]
) +
tip('Скорость SPI на AVR: SPI.setClockDivider(SPI_CLOCK_DIV2) = 8 МГц при 16 МГц тактовой. Это в 20 раз быстрее I2C 400 кГц. SD-карты требуют медленный старт (400 кГц), затем можно ускорить.') +
warn('SS (Chip Select) должен оставаться LOW всё время транзакции. Если несколько устройств на шине — убедитесь что CS «чужих» устройств в HIGH. Иначе они будут слушать и мешать.'),
'code_example': '''#include <SPI.h>

// Прямой доступ к регистрам SPI (без библиотеки)
void spi_init_raw(void) {
    // MOSI(PB3), SCK(PB5), SS(PB2) = выходы
    DDRB |= (1<<PB3)|(1<<PB5)|(1<<PB2);
    DDRB &= ~(1<<PB4);  // MISO = вход

    // SPCR: SPE=1(вкл), MSTR=1(мастер), SPR0=1 → делитель /16 = 1 МГц
    SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR0);
    // SPSR: SPI2X=1 → двойная скорость (опционально)
    // SPSR |= (1<<SPI2X);
}

uint8_t spi_transfer_raw(uint8_t data) {
    SPDR = data;                   // начать передачу
    while (!(SPSR & (1<<SPIF)));   // ждать завершения
    return SPDR;                   // принятый байт
}

// Пример: чтение регистра MAX6675 (термопара SPI)
float max6675_read_temp(uint8_t cs_pin) {
    digitalWrite(cs_pin, LOW);
    uint8_t high = SPI.transfer(0);
    uint8_t low  = SPI.transfer(0);
    digitalWrite(cs_pin, HIGH);

    uint16_t raw = ((uint16_t)high << 8) | low;
    if (raw & 0x04) return -1;  // ошибка: термопара не подключена
    return (raw >> 3) * 0.25;   // 12-бит, шаг 0.25°C
}

void setup() {
    SPI.begin();
    SPI.setClockDivider(SPI_CLOCK_DIV4);  // 4 МГц
    SPI.setDataMode(SPI_MODE0);
    pinMode(10, OUTPUT); digitalWrite(10, HIGH);
    Serial.begin(115200);
}

void loop() {
    float t = max6675_read_temp(10);
    Serial.print("Temp: "); Serial.println(t);
    delay(250);
}'''
},

# ─── M9 L3: C + ASM ───────────────────────────────────────────────────────────
(9,3): {
'title': 'Смешанное программирование C + AVR Assembler',
'estimated_minutes': 50,
'content': '''
<h2>Зачем использовать ASM в C проектах?</h2>
<p>В 99% случаев достаточно C с оптимизацией -Os. Но иногда нужна <strong>абсолютная точность тайминга</strong> (несколько тактов) или доступ к специфическим инструкциям AVR, которых нет в C. Тогда используют inline assembler.</p>
''' + diagram(
    DEFS + BG(230) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Когда C достаточно, а когда нужен ASM?</text>' +
    box(20,50,280,150,'#dcfce7','#16a34a','C с -Os обычно достаточно',12,'bold','#14532d') +
    '<text x="160" y="95" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Логика программы</text>' +
    '<text x="160" y="113" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Алгоритмы и структуры данных</text>' +
    '<text x="160" y="131" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Работа с периферией через регистры</text>' +
    '<text x="160" y="149" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Задержки _delay_ms/_delay_us</text>' +
    '<text x="160" y="167" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Математика (avr-libc имеет всё)</text>' +
    '<text x="160" y="185" text-anchor="middle" font-size="10" fill="#15803d" font-family="sans-serif">~95% всех проектов</text>' +
    box(340,50,280,150,'#fef9c3','#f59e0b','ASM нужен когда...',12,'bold','#78350f') +
    '<text x="480" y="95" text-anchor="middle" font-size="10" fill="#78350f" font-family="sans-serif">Точность ±1 такт (видео, 1-Wire вручную)</text>' +
    '<text x="480" y="113" text-anchor="middle" font-size="10" fill="#78350f" font-family="sans-serif">Инструкции без C-аналога (swap, lpm)</text>' +
    '<text x="480" y="131" text-anchor="middle" font-size="10" fill="#78350f" font-family="sans-serif">Критическая ISR с минимумом тактов</text>' +
    '<text x="480" y="149" text-anchor="middle" font-size="10" fill="#78350f" font-family="sans-serif">Атомарные операции без библиотек</text>' +
    '<text x="480" y="167" text-anchor="middle" font-size="10" fill="#78350f" font-family="sans-serif">Изучение архитектуры AVR</text>' +
    '<text x="480" y="185" text-anchor="middle" font-size="10" fill="#b45309" font-family="sans-serif">~5% — специфические задачи</text>',
    640, 235, 'Для большинства задач компилятор генерирует оптимальный код. ASM — хирургический инструмент'
) +
'''<h3>Синтаксис Extended Inline ASM</h3>
<p>Синтаксис GCC inline assembler: <code>asm volatile ("инструкции" : выходы : входы : затронутые_регистры)</code></p>''' +
table(
    ['Ограничение','Значение','Пример использования'],
    [
        ['"r"','Любой регистр R0–R31','Входной параметр'],
        ['"d"','Регистры R16–R31 (для ldi/subi)','Константные операции'],
        ['"w"','Пара регистров X/Y/Z','16-битные указатели'],
        ['"I"','Константа 0–63 (для out/in)','Адреса I/O регистров'],
        ['"M"','Константа 0–255 (для ldi)','8-битные константы'],
        ['"=r"','Выходной регистр (запись)','Результат операции'],
        ['"&"','Ранний регистр (не совпадает с входом)','Когда выход ≠ вход'],
    ]
) +
diagram(
    DEFS + BG(180) +
    '<text x="320" y="25" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="bold" font-family="sans-serif">Полная форма extended asm</text>' +
    '<rect x="20" y="40" width="600" height="130" rx="6" fill="#1e293b"/>' +
    '<text x="40" y="65" font-size="11" fill="#7dd3fc" font-family="monospace">asm volatile (</text>' +
    '<text x="40" y="85" font-size="11" fill="#86efac" font-family="monospace">    "swap %0    \\n\\t"    // инструкция, %0=первый операнд</text>' +
    '<text x="40" y="103" font-size="11" fill="#86efac" font-family="monospace">    "andi %0, 0x0F \\n\\t" // второй оператор</text>' +
    '<text x="40" y="121" font-size="11" fill="#fcd34d" font-family="monospace">    : "=d"(result)       // выход: d=R16-R31</text>' +
    '<text x="40" y="139" font-size="11" fill="#f9a8d4" font-family="monospace">    : "0"(input)         // вход: тот же регистр что result</text>' +
    '<text x="40" y="157" font-size="11" fill="#fca5a5" font-family="monospace">);                       // затронутые регистры — нет</text>',
    640, 185, 'Extended asm: компилятор сам выбирает регистры, подставляет в шаблон'
) +
tip('Директива <code>__builtin_avr_nop()</code>, <code>__builtin_avr_sei()</code>, <code>__builtin_avr_cli()</code> позволяют вызвать специфические инструкции AVR без полного inline-asm — чище и безопаснее.') +
warn('Всегда указывайте затронутые регистры в clobber-списке! Если ASM меняет r0 или SREG — напишите <code>: "r0", "cc"</code>. Иначе компилятор не знает об изменениях и сгенерирует неверный код.'),
'code_example': '''#include <avr/io.h>

// 1. Простой inline ASM: NOP
void precise_delay_2cycles(void) {
    asm volatile ("nop" ::);
    asm volatile ("nop" ::);
}

// 2. Extended ASM: swap nibbles (нет в C)
uint8_t swap_nibbles(uint8_t x) {
    asm volatile ("swap %0" : "=d"(x) : "0"(x));
    return x;
}

// 3. Подсчёт бит (popcount) через ASM
uint8_t popcount8(uint8_t v) {
    uint8_t count = 0;
    asm volatile (
        "clr %0          \\n\\t"   // count = 0
        "1: tst %1       \\n\\t"   // v == 0?
        "   breq 2f      \\n\\t"   // да — выход
        "   bst %1, 0    \\n\\t"   // T = v[0]
        "   bld r0, 0    \\n\\t"   // r0[0] = T
        "   andi r0, 1   \\n\\t"
        "   add %0, r0   \\n\\t"   // count += v[0]
        "   lsr %1       \\n\\t"   // v >>= 1
        "   rjmp 1b      \\n\\t"
        "2:              \\n\\t"
        : "=r"(count), "=r"(v)
        : "0"(count), "1"(v)
        : "r0"
    );
    return count;
}

// 4. Точная задержка 10 тактов
#define DELAY_10_CYCLES() asm volatile ( \
    "nop\\n nop\\n nop\\n nop\\n nop\\n" \
    "nop\\n nop\\n nop\\n nop\\n nop\\n" ::)

// 5. Атомарная инкрементация без util/atomic.h
static inline void atomic_inc_u8(volatile uint8_t *p) {
    asm volatile (
        "in  r24, 0x3F   \\n\\t"   // сохранить SREG
        "cli             \\n\\t"   // запрет прерываний
        "ld  r25, %a0    \\n\\t"   // загрузить *p
        "inc r25         \\n\\t"   // инкрементировать
        "st  %a0, r25    \\n\\t"   // сохранить
        "out 0x3F, r24   \\n\\t"   // восстановить SREG
        : : "e"(p) : "r24","r25"
    );
}

int main(void) {
    uint8_t x = 0xAB;
    uint8_t s = swap_nibbles(x);   // s = 0xBA
    (void)s;
    uint8_t b = popcount8(0b10110101);  // b = 5
    (void)b;
}'''
},

# ─── M9 L1: ASM синтаксис ────────────────────────────────────────────────────
(9,1): {
'title': 'Синтаксис AVR Assembler',
'estimated_minutes': 55,
'content': '''
<h2>Язык ассемблера AVR: синтаксис и структура</h2>
<p>Ассемблер AVR — язык, в котором каждая строка = одна машинная инструкция или директива ассемблера. Программа на ASM максимально эффективна по размеру и скорости, но требует детального знания архитектуры.</p>
''' + diagram(
    DEFS + BG(210) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Структура строки AVR Assembler</text>' +
    box(20,50,590,60,'#dbeafe','#3b82f6','метка:     мнемоника  операнд1, операнд2   ; комментарий',11,'bold') +
    '<text x="85" y="130" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">необязательна</text>' +
    '<text x="200" y="130" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">команда AVR</text>' +
    '<text x="350" y="130" text-anchor="middle" font-size="10" fill="#f59e0b" font-family="sans-serif">регистры / константы</text>' +
    '<text x="540" y="130" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">текст</text>' +
    '<line x1="40" y1="110" x2="40" y2="120" stroke="#1e40af" stroke-width="1.5"/>' +
    '<line x1="160" y1="110" x2="200" y2="120" stroke="#16a34a" stroke-width="1.5"/>' +
    '<line x1="320" y1="110" x2="350" y2="120" stroke="#f59e0b" stroke-width="1.5"/>' +
    '<line x1="520" y1="110" x2="540" y2="120" stroke="#64748b" stroke-width="1.5"/>' +
    # Directives
    '<rect x="20" y="150" width="590" height="50" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="168" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Ключевые директивы avr-as</text>' +
    '<text x="40" y="187" font-size="10" fill="#64748b" font-family="monospace">.include "m328pdef.inc"  .org addr  .def alias=Rn  .equ K=val  .byte .word  .cseg .dseg .eseg</text>',
    640, 210, 'Каждая строка ASM: метка (имя адреса) + мнемоника + операнды + комментарий'
) +
table(
    ['Категория','Примеры команд','Описание'],
    [
        ['Пересылка','mov, ldi, ld, st, lds, sts, push, pop, in, out','Перемещение данных'],
        ['Арифметика','add, sub, adc, sbc, inc, dec, neg, mul, muls','Арифметические операции'],
        ['Логика','and, or, eor, com, andi, ori, cbr, sbr','Побитовые логические операции'],
        ['Сдвиги','lsl, lsr, rol, ror, asr','Битовые сдвиги и вращения'],
        ['Биты','sbi, cbi, bst, bld, sbis, sbic, sbrs, sbrc','Работа с отдельными битами'],
        ['Ветвление','rjmp, jmp, rcall, call, ret, reti, ijmp','Безусловные переходы'],
        ['Условные','brcc, brcs, breq, brne, brlt, brge, brmi, brpl','Условные переходы по флагам'],
        ['Управление','nop, sleep, wdr, sei, cli, break','Системные команды'],
    ]
) +
diagram(
    DEFS + BG(200) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Таблица векторов прерываний ATmega328P (начало Flash)</text>' +
    '<rect x="20" y="45" width="200" height="140" rx="6" fill="#1e293b"/>' +
    '<text x="120" y="65" text-anchor="middle" font-size="10" fill="#94a3b8" font-family="monospace">addr  vector</text>' +
    '<text x="120" y="83" text-anchor="middle" font-size="10" fill="#7dd3fc" font-family="monospace">0x0000  RESET</text>' +
    '<text x="120" y="99" text-anchor="middle" font-size="10" fill="#86efac" font-family="monospace">0x0002  INT0</text>' +
    '<text x="120" y="115" text-anchor="middle" font-size="10" fill="#86efac" font-family="monospace">0x0004  INT1</text>' +
    '<text x="120" y="131" text-anchor="middle" font-size="10" fill="#fcd34d" font-family="monospace">0x0006  PCINT0</text>' +
    '<text x="120" y="147" text-anchor="middle" font-size="10" fill="#fcd34d" font-family="monospace">...(26 векторов)</text>' +
    '<text x="120" y="163" text-anchor="middle" font-size="10" fill="#f9a8d4" font-family="monospace">0x0034  SPM_RDY</text>' +
    box(250,55,360,120,'#f8fafc','#e2e8f0','Каждый вектор = 2 байта\n(jmp ISR_addr = 4 байта)\nRESET: 0x0000 — точка входа\nrjmp main (2 байта = 1 слово)\nПри прерывании: PC = адрес вектора',10) +
    '<text x="430" y="190" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">ATmega328P: 26 источников прерываний</text>',
    640, 205, 'Таблица векторов — начало Flash. RESET всегда 0x0000'
) +
tip('Полный список инструкций AVR: "AVR Instruction Set Manual" (Atmel/Microchip, doc0856). Каждая команда описана с тактами, флагами и примерами. Незаменимый справочник!') +
warn('Ассемблер AVRA (avra.sf.net) и avr-as (из avr-gcc toolchain) имеют разный синтаксис! avr-as использует AT&T синтаксис с префиксами, AVRA — Intel синтаксис. Не перепутайте.'),
'code_example': '''; Полный рабочий пример: мигание LED на чистом AVR ASM
; ATmega328P @ 16 МГц, LED на PB5 (Arduino pin 13)
; Компиляция: avr-as -mmcu=atmega328p blink.S -o blink.o
;             avr-ld -m avr5 blink.o -o blink.elf
;             avr-objcopy -O ihex blink.elf blink.hex

.include "m328pdef.inc"

; Псевдонимы регистров
.def temp  = r16
.def cnt_a = r24
.def cnt_b = r25
.def cnt_c = r26

    .text
    .org 0x0000
    rjmp reset          ; вектор RESET

    ; Остальные векторы = rjmp . (бесконечный цикл = игнор)
    .org 0x0002
    rjmp .  ; INT0
    .org 0x0034
    rjmp .  ; последний вектор

reset:
    ; Инициализация стека
    ldi  temp, HIGH(RAMEND)
    out  SPH, temp
    ldi  temp, LOW(RAMEND)
    out  SPL, temp

    ; PB5 = выход
    ldi  temp, (1 << PB5)
    out  DDRB, temp
    clr  temp
    out  PORTB, temp

main_loop:
    ; Включить LED
    sbi  PORTB, PB5
    rcall delay_500ms

    ; Выключить LED
    cbi  PORTB, PB5
    rcall delay_500ms
    rjmp main_loop

; Задержка ~500 мс при 16 МГц
; Считаем 3-тактовые циклы: 16e6 / (2*3) ≈ 2 666 667 итераций
delay_500ms:
    ldi  cnt_c, 20          ; внешний счётчик (×)
outer:
    ldi  cnt_b, HIGH(133333)
    ldi  cnt_a, LOW(133333)
inner:
    sbiw cnt_a, 1           ; 2 такта: dec 16-bit
    brne inner              ; 1/2 такта
    dec  cnt_c
    brne outer
    ret'''
},

# ─── M10 L2: Отладка ──────────────────────────────────────────────────────────
(10,2): {
'title': 'Отладка и тестирование МК систем',
'estimated_minutes': 55,
'content': '''
<h2>Систематический подход к отладке МК</h2>
<p>Отладка встраиваемых систем сложнее PC-программ: нет ОС, нет исключений, код может «зависнуть» незаметно. Нужен системный подход.</p>
''' + diagram(
    DEFS + BG(250) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Инструменты отладки МК: от простого к сложному</text>' +
    box(20,55,130,40,'#dcfce7','#16a34a','LED\nмигание',11,'bold') +
    box(165,55,130,40,'#dbeafe','#3b82f6','Serial\nprint',11,'bold') +
    box(310,55,130,40,'#fef9c3','#f59e0b','Логический\nанализатор',11,'bold') +
    box(455,55,155,40,'#fdf4ff','#a855f7','JTAG / debugWIRE\n+ GDB',11,'bold') +
    arrow(150,75,165,75) + arrow(295,75,310,75) + arrow(440,75,455,75) +
    '<text x="85" y="115" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Всегда доступно</text>' +
    '<text x="230" y="115" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Нет доп. оборудования</text>' +
    '<text x="375" y="115" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Нужен LA-прибор</text>' +
    '<text x="532" y="115" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">ATMEL-ICE / J-Link</text>' +
    # Checklist
    '<rect x="20" y="135" width="600" height="100" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="155" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Чеклист при зависании программы</text>' +
    '<text x="40" y="175" font-size="10" fill="#64748b" font-family="sans-serif">[ ] LED heartbeat мигает? Если нет — crash в main loop или переполнение стека</text>' +
    '<text x="40" y="193" font-size="10" fill="#64748b" font-family="sans-serif">[ ] Serial.print() работает? Если нет — crash до setup() или зависание в ISR</text>' +
    '<text x="40" y="211" font-size="10" fill="#64748b" font-family="sans-serif">[ ] WDT сработал? Проверить MCUSR → WDRF флаг при старте</text>' +
    '<text x="40" y="229" font-size="10" fill="#64748b" font-family="sans-serif">[ ] avr-size: сколько SRAM занято? Если &gt;80% — риск переполнения стека</text>',
    640, 250, 'Начинай с LED и Serial — они работают всегда и везде'
) +
table(
    ['Симптом','Вероятная причина','Как проверить'],
    [
        ['МК не стартует','Неверное питание, неверные fuse bits, испорченный загрузчик','Измерить питание, попробовать другой МК'],
        ['Программа зависает','Бесконечный цикл, переполнение стека, segfault-подобное','Serial до/после, уменьшить массивы'],
        ['Неверные показания датчика','Неверное подключение, неверный Vref, помехи','Осциллограф на линии, проверить схему'],
        ['UART мусор','Несовпадение baud rate, неверный F_CPU в fuse','Проверить fuse, другой baud'],
        ['I2C не работает','Нет подтяжки, неверный адрес, нет питания 3.3В','I2C scanner скетч'],
        ['Сброс каждые N секунд','WDT без wdt_disable(), низкое питание (BOD)','Проверить MCUSR при старте'],
    ]
) +
'''<h3>avr-size: анализ использования памяти</h3>
<pre style="background:#1e293b;color:#e2e8f0;padding:12px;border-radius:8px;font-size:12px">
$ avr-size --format=avr firmware.elf
AVR Memory Usage
----------------
Device: atmega328p

Program:   14782 bytes (45.1% Full)
(.text + .data + .bootloader)

Data:       1024 bytes (50.0% Full)
(.data + .bss + .noinit)
</pre>
<p>Правило: при Data &gt; 80% (1640 байт из 2048) — высокий риск переполнения стека. Стек и heap не учтены в avr-size!</p>''' +
tip('Для поиска утечки SRAM: в начале setup() заполните SRAM паттерном 0x55, через некоторое время проверьте — где 0x55 затёрлось, там был стек. Высота «воронки» = максимальная глубина стека.') +
warn('F_CPU в коде должен точно совпадать с реальной тактовой частотой МК (задаётся fuse bits). Несовпадение → UART мусор, неверные _delay_ms(), неверные Timer периоды. Проверяйте fuse bits!'),
'code_example': '''#include <Arduino.h>

// Диагностический класс для мониторинга состояния системы
class SystemDiag {
public:
    static void printResetCause() {
        uint8_t mcusr = MCUSR;
        MCUSR = 0;
        wdt_disable();
        Serial.print(F("[DIAG] Reset: "));
        if (mcusr & (1<<PORF))  Serial.print(F("POWER-ON "));
        if (mcusr & (1<<EXTRF)) Serial.print(F("EXTERNAL "));
        if (mcusr & (1<<BORF))  Serial.print(F("BROWN-OUT "));
        if (mcusr & (1<<WDRF))  Serial.print(F("WATCHDOG "));
        Serial.println();
    }

    static int freeRAM() {
        extern int __heap_start, *__brkval;
        int v;
        return (int)&v - (__brkval == 0
                         ? (int)&__heap_start
                         : (int)__brkval);
    }

    static void printMemory() {
        Serial.print(F("[DIAG] Free RAM: "));
        Serial.print(freeRAM());
        Serial.println(F(" bytes"));
    }

    // Заполнить стек паттерном для измерения глубины
    static void fillStackPattern() {
        uint8_t *p = (uint8_t*)0x0100;
        extern uint8_t _end;
        while (p < &_end) *p++ = 0x55;
    }
};

void setup() {
    Serial.begin(115200);
    SystemDiag::printResetCause();
    SystemDiag::printMemory();
    Serial.println(F("[DIAG] Boot complete"));
}

void loop() {
    static uint32_t t = 0;
    if (millis() - t >= 5000) {
        t = millis();
        SystemDiag::printMemory();
    }
}'''
},

# ─── M13 L1: WDT ─────────────────────────────────────────────────────────────
(13,1): {
'title': 'Watchdog Timer (WDT) — сторожевой таймер',
'estimated_minutes': 50,
'content': '''
<h2>Watchdog Timer — защита от зависаний</h2>
<p>WDT — аппаратный таймер на независимом RC-генераторе (~128 кГц). Работает даже когда основная тактовая схема остановлена. Два применения: <strong>защита от зависания</strong> и <strong>периодическое пробуждение из сна</strong>.</p>
''' + diagram(
    DEFS + BG(260) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">WDT: два режима работы</text>' +
    box(20,50,285,90,'#dcfce7','#16a34a','Reset Mode (WDE=1, WDIE=0)',11,'bold','#14532d') +
    '<text x="162" y="92" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">WDT считает до таймаута</text>' +
    '<text x="162" y="108" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">→ аппаратный RESET</text>' +
    '<text x="162" y="124" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">wdt_reset() сбрасывает счётчик</text>' +
    box(335,50,285,90,'#dbeafe','#3b82f6','Interrupt+Reset Mode (WDE=1, WDIE=1)',11,'bold','#1e40af') +
    '<text x="477" y="92" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">1й таймаут: ISR(WDT_vect)</text>' +
    '<text x="477" y="108" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">2й таймаут (если ISR не сбросила):</text>' +
    '<text x="477" y="124" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">→ аппаратный RESET</text>' +
    # Registers
    '<rect x="20" y="155" width="600" height="90" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="175" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Регистр WDTCSR — управление WDT</text>' +
    ''.join(box(25+i*72,185,68,35,'#dbeafe','#3b82f6',['WDIF','WDIE','WDP3','WDCE','WDE','WDP2','WDP1','WDP0'][i],10) for i in range(8)) +
    '<text x="320" y="237" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">WDP3:WDP0 задают таймаут | WDE=Reset режим | WDIE=Interrupt режим | WDCE=изменение WDT</text>',
    640, 260, 'WDT управляется регистром WDTCSR. Изменение требует специальной последовательности'
) +
table(
    ['WDP3','WDP2','WDP1','WDP0','Таймаут','Константа avr/wdt.h'],
    [
        ['0','0','0','0','16 мс','WDTO_15MS'],
        ['0','0','0','1','32 мс','WDTO_30MS'],
        ['0','0','1','0','64 мс','WDTO_60MS'],
        ['0','0','1','1','125 мс','WDTO_120MS'],
        ['0','1','0','0','250 мс','WDTO_250MS'],
        ['0','1','0','1','500 мс','WDTO_500MS'],
        ['0','1','1','0','1 сек','WDTO_1S'],
        ['1','0','0','1','8 сек','WDTO_8S'],
    ]
) +
tip('WDT использует отдельный RC-генератор, не зависящий от основной тактовой. Он работает даже в Power-down режиме. Именно поэтому WDT — основной механизм пробуждения из сна.') +
warn('Критически важно: после сброса по WDT МК стартует с включённым WDT и коротким таймаутом (16 мс). Без wdt_disable() в начале кода МК будет непрерывно сбрасываться! Всегда добавляйте wdt_disable() первой строкой.'),
'code_example': '''#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

// WDT в режиме Interrupt (для пробуждения из сна)
volatile bool wdt_fired = false;

ISR(WDT_vect) {
    wdt_fired = true;
    // НЕ сбрасываем WDT здесь — он автоматически переходит
    // в Interrupt-only режим после первого срабатывания
}

void wdt_setup_interrupt(uint8_t timeout_bits) {
    cli();
    MCUSR &= ~(1<<WDRF);   // сбросить флаг WDT reset
    // Специальная последовательность (timed sequence):
    WDTCSR |= (1<<WDCE)|(1<<WDE);    // разрешить изменение (4 такта)
    WDTCSR  = (1<<WDIE) | timeout_bits; // только interrupt, без reset
    sei();
}

void setup() {
    // ПЕРВЫМ ДЕЛОМ — отключить WDT (мог остаться от прошлого запуска)
    MCUSR &= ~(1<<WDRF);
    wdt_disable();

    // Настроить WDT: прерывание каждые 8 секунд
    wdt_setup_interrupt((1<<WDP3)|(1<<WDP0));  // 8 сек

    // Настроить сон
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
}

void loop() {
    wdt_fired = false;

    // Засыпаем
    sleep_enable();
    sleep_cpu();
    sleep_disable();

    // Просыпаемся здесь через 8 сек
    if (wdt_fired) {
        // Сделать полезную работу
        // Перенастроить WDT для следующего цикла
        wdt_setup_interrupt((1<<WDP3)|(1<<WDP0));
    }
}'''
},

# ─── M15 L2: Button debounce ─────────────────────────────────────────────────
(15,2): {
'title': 'Антидребезг и работа с кнопками',
'estimated_minutes': 50,
'content': '''
<h2>Дребезг контактов: физическая природа</h2>
<p>Механические контакты кнопки при замыкании вибрируют 5–50 мс. МК с тактовой 16 МГц успевает обработать тысячи «нажатий» за это время. Результат — счётчик накрутился до 50 вместо 1.</p>
''' + diagram(
    DEFS + BG(240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Три метода антидребезга — сравнение</text>' +
    box(20,50,180,60,'#fee2e2','#ef4444','delay() метод\n— блокирующий',11,'bold','#7f1d1d') +
    '<text x="110" y="130" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">if pressed: delay(50); check again</text>' +
    '<text x="110" y="145" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">Блокирует loop() на 50 мс</text>' +
    box(230,50,180,60,'#dbeafe','#3b82f6','millis() метод\n— неблокирующий',11,'bold','#1e40af') +
    '<text x="320" y="130" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Таймер стабильности по millis()</text>' +
    '<text x="320" y="145" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Рекомендуется для Arduino</text>' +
    box(440,50,180,60,'#dcfce7','#16a34a','Счётчик стабильности\n— аппаратоподобный',11,'bold','#14532d') +
    '<text x="530" y="130" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">N подряд одинаковых значений</text>' +
    '<text x="530" y="145" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Более устойчив к шуму</text>' +
    # Timing diagram
    '<rect x="20" y="163" width="600" height="65" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="180" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">millis()-метод: отсчёт от первого изменения</text>' +
    '<line x1="40" y1="215" x2="580" y2="215" stroke="#94a3b8" stroke-width="1"/>' +
    '<line x1="120" y1="215" x2="120" y2="200" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="120" y="196" text-anchor="middle" font-size="9" fill="#ef4444" font-family="sans-serif">изменение</text>' +
    '<line x1="120" y1="215" x2="220" y2="215" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="220" y1="215" x2="220" y2="200" stroke="#16a34a" stroke-width="2"/>' +
    '<text x="170" y="196" text-anchor="middle" font-size="9" fill="#f59e0b" font-family="sans-serif">50 мс таймаут</text>' +
    '<text x="220" y="196" text-anchor="middle" font-size="9" fill="#16a34a" font-family="sans-serif">событие!',
    640, 245, 'millis()-debounce: событие фиксируется через N мс стабильного состояния'
) +
table(
    ['Паттерн','Описание','Применение'],
    [
        ['wasPressed()','Возвращает true ОДИН РАЗ при нажатии','Счётчик кликов, запуск действия'],
        ['wasReleased()','Возвращает true ОДИН РАЗ при отпускании','Действие при отпускании'],
        ['isPressed()','Возвращает true пока кнопка нажата','Удержание, длинное нажатие'],
        ['holdTime()','Сколько мс кнопка удерживается','Длинное нажатие vs короткое'],
    ]
) +
'''<h3>Обнаружение длинного нажатия</h3>''' +
diagram(
    DEFS + BG(160) +
    '<text x="320" y="25" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="bold" font-family="sans-serif">Короткое vs длинное нажатие — временная диаграмма</text>' +
    '<line x1="30" y1="80" x2="580" y2="80" stroke="#94a3b8" stroke-width="1.5"/>' +
    # Short press
    '<line x1="60" y1="80" x2="60" y2="110" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="60" y1="110" x2="130" y2="110" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="130" y1="110" x2="130" y2="80" stroke="#3b82f6" stroke-width="2"/>' +
    '<text x="95" y="130" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">&lt;500 мс</text>' +
    '<text x="95" y="145" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">КОРОТКОЕ</text>' +
    # Long press
    '<line x1="250" y1="80" x2="250" y2="110" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="250" y1="110" x2="480" y2="110" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="480" y1="110" x2="480" y2="80" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="250" y1="75" x2="380" y2="75" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5"/>' +
    '<text x="315" y="70" text-anchor="middle" font-size="9" fill="#f59e0b" font-family="sans-serif">500 мс — порог длинного</text>' +
    '<text x="365" y="130" text-anchor="middle" font-size="10" fill="#ef4444" font-family="sans-serif">&gt;500 мс</text>' +
    '<text x="365" y="145" text-anchor="middle" font-size="10" fill="#ef4444" font-family="sans-serif">ДЛИННОЕ (HOLD)</text>',
    640, 165, 'Один и тот же пин — разные действия в зависимости от длины нажатия'
) +
tip('Профессиональный совет: добавьте визуальную обратную связь на длинное нажатие — мигните LED через 300 мс как «предупреждение» что сейчас сработает длинное нажатие.') +
warn('Для матрицы кнопок 4×4 нельзя использовать отдельный объект Button на каждую — не хватит памяти. Используйте двумерный массив флагов и общую функцию антидребезга.'),
'code_example': '''#include <Arduino.h>

// Продвинутый класс кнопки: короткое/длинное нажатие
class AdvButton {
    uint8_t  pin;
    uint16_t debounce_ms;
    uint32_t press_start;
    uint32_t last_change;
    bool     raw, state;
    bool     ev_short, ev_long, ev_release;
    bool     long_fired;

public:
    static const uint16_t LONG_PRESS = 600; // мс

    AdvButton(uint8_t p, uint16_t d=30)
        : pin(p), debounce_ms(d), press_start(0),
          last_change(0), raw(false), state(false),
          ev_short(false), ev_long(false),
          ev_release(false), long_fired(false) {
        pinMode(pin, INPUT_PULLUP);
    }

    void update() {
        ev_short = ev_long = ev_release = false;
        bool cur = !digitalRead(pin);

        if (cur != raw) {
            last_change = millis();
            raw = cur;
        }

        if (millis() - last_change >= debounce_ms) {
            if (cur != state) {
                state = cur;
                if (state) {
                    press_start = millis();
                    long_fired = false;
                } else {
                    ev_release = true;
                    if (!long_fired)
                        ev_short = (millis() - press_start < LONG_PRESS);
                }
            }
        }

        // Длинное нажатие — во время удержания
        if (state && !long_fired &&
            millis() - press_start >= LONG_PRESS) {
            ev_long = true;
            long_fired = true;
        }
    }

    bool shortPress()  const { return ev_short; }
    bool longPress()   const { return ev_long; }
    bool released()    const { return ev_release; }
    bool isHeld()      const { return state; }
    uint32_t holdMs()  const { return state ? millis()-press_start : 0; }
};

AdvButton btn(2);
int counter = 0;

void setup() { Serial.begin(115200); }

void loop() {
    btn.update();
    if (btn.shortPress())  { counter++; Serial.print("Count: "); Serial.println(counter); }
    if (btn.longPress())   { counter = 0; Serial.println("RESET"); }
    if (btn.isHeld() && btn.holdMs() > 2000) Serial.println("Very long hold!");
}'''
},

}  # конец PATCHES


class Command(BaseCommand):
    help = 'Расширяет тонкие уроки МПС (patch2)'

    def handle(self, *args, **options):
        subj = Subject.objects.get(slug='mcu')
        mods = {m.order: m for m in TheoryModule.objects.filter(subject=subj)}
        total = 0

        for (mod_order, lesson_order), data in PATCHES.items():
            module = mods.get(mod_order)
            if not module:
                self.stderr.write(f'M{mod_order} не найден')
                continue
            before = TheoryLesson.objects.filter(module=module, order=lesson_order).values_list('content', flat=True).first()
            before_len = len(before) if before else 0

            obj, created = TheoryLesson.objects.update_or_create(
                module=module, order=lesson_order,
                defaults={
                    'title': data['title'],
                    'content': data['content'],
                    'code_example': data.get('code_example', ''),
                    'estimated_minutes': data['estimated_minutes'],
                }
            )
            after_len = len(data['content'])
            diff = after_len - before_len
            self.stdout.write(
                f'M{mod_order}L{lesson_order}: {before_len} -> {after_len} ch '
                f'(+{diff}) [{data["title"][:35]}]'
            )
            total += 1

        self.stdout.write(self.style.SUCCESS(f'\nГотово: обновлено {total} уроков'))
