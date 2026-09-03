"""python manage.py seed_mps_full2 — расширенный контент МПС модули 6–10"""
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
    return (
        f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
        f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;'
        f'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">'
        f'{svg}</svg>'
        f'<p style="text-align:center;color:#64748b;font-size:13px">{caption}</p></div>'
    )

def box(x, y, w, h, fill, stroke, text, fs=12, fw='normal', tc='#1e293b'):
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    lines = text.split('\n')
    lh = fs + 3
    total_h = lh * len(lines)
    y0 = y + h // 2 - total_h // 2 + fs
    spans = ''.join(
        f'<tspan x="{x + w // 2}" dy="{0 if i == 0 else lh}">{l}</tspan>'
        for i, l in enumerate(lines)
    )
    txt = (f'<text x="{x + w // 2}" y="{y0}" text-anchor="middle" font-size="{fs}" '
           f'fill="{tc}" font-weight="{fw}" font-family="sans-serif">{spans}</text>')
    return rect + txt

def arrow(x1, y1, x2, y2, color='#64748b'):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#arr)"/>'

DEFS = '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'


LESSONS = {

# ─── МОДУЛЬ 6: АЦП ────────────────────────────────────────────────────────────
6: [
{
'title': 'АЦП ATmega328P: принцип и настройка',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>АЦП — аналого-цифровой преобразователь</h2>
<p>ATmega328P содержит 10-битный АЦП с последовательным приближением (SAR). Он преобразует аналоговое напряжение (0…Vref) в цифровое число 0…1023.</p>
<p><strong>Формула преобразования:</strong></p>
<p style="background:#f1f5f9;padding:10px;border-radius:8px;font-family:monospace;text-align:center">
ADC = Vin × 1024 / Vref &nbsp;&nbsp;|&nbsp;&nbsp; Vin = ADC × Vref / 1024
</p>
''' + table(
    ['Параметр','Значение'],
    [
        ['Разрядность','10 бит (0–1023)'],
        ['Каналов','6 (PC0–PC5, Arduino A0–A5)'],
        ['Источник опорного напряжения','AVCC (5V), внутренний 1.1V, внешний AREF'],
        ['Тактовая частота АЦП','F_CPU / предделитель (50–200 кГц оптимально)'],
        ['Время преобразования','13–260 мкс (при 50–200 кГц)'],
        ['Режимы','Одиночный запуск, свободный режим (Free Running)'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="260" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Структура 10-битного АЦП SAR</text>' +
    # Analog input
    box(20,60,80,40,'#fef9c3','#f59e0b','Vin\n(A0–A5)',11) +
    arrow(100,80,140,80) +
    box(140,60,80,40,'#dbeafe','#3b82f6','MUX\n(выбор канала)',10) +
    arrow(220,80,260,80) +
    box(260,55,80,50,'#dcfce7','#16a34a','S&H\n(выборка и\nхранение)',10) +
    arrow(340,80,380,80) +
    box(380,55,100,50,'#fdf4ff','#a855f7','SAR\n(последоват.\nприближение)',10) +
    arrow(480,80,520,80) +
    box(520,60,90,40,'#fee2e2','#ef4444','ADCH:ADCL\n(рез-т 10 бит)',10) +
    # Vref
    box(260,135,80,35,'#fef9c3','#f59e0b','Vref\n(опорное)',10) +
    arrow(300,135,300,105) +
    # Process
    '<rect x="20" y="185" width="580" height="65" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="310" y="205" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Алгоритм SAR (10 итераций):</text>' +
    '<text x="40" y="225" font-size="10" fill="#64748b" font-family="sans-serif">Бит9=1? Vin &gt; Vref/2? → да: оставить, нет: сбросить. Бит8=1?... и так 10 раз</text>' +
    '<text x="40" y="242" font-size="10" fill="#64748b" font-family="sans-serif">Каждая итерация = 1 такт АЦП. Итого 13 тактов (12 + 1 на выборку)</text>',
    640, 260, 'АЦП с последовательным приближением — 10 шагов → 10-битный результат'
) + '''
<h3>Ключевые регистры АЦП</h3>
''' + table(
    ['Регистр','Биты','Назначение'],
    [
        ['ADMUX','REFS1:REFS0','Источник Vref (00=AREF, 01=AVCC, 11=1.1V int)'],
        ['ADMUX','ADLAR','Выравнивание результата (0=правое, 1=левое)'],
        ['ADMUX','MUX3:MUX0','Выбор канала (0000=ADC0 … 0111=ADC7)'],
        ['ADCSRA','ADEN','Включить АЦП'],
        ['ADCSRA','ADSC','Запустить преобразование'],
        ['ADCSRA','ADFR/ADATE','Режим Free Running'],
        ['ADCSRA','ADIF','Флаг завершения преобразования'],
        ['ADCSRA','ADIE','Разрешить прерывание АЦП'],
        ['ADCSRA','ADPS2:ADPS0','Предделитель (000=2 … 111=128)'],
    ]
) + tip('При F_CPU=16 МГц используйте предделитель 128 (ADPS=111) → f_ADC=125 кГц. Это даёт точность 10 бит за ~104 мкс.') +
warn('Не читайте ADC (ADCH:ADCL) пока флаг ADSC=1 — преобразование ещё идёт. Всегда ждите ADSC→0 или используйте прерывание.'),
'code_example': '''#include <avr/io.h>

void adc_init(void) {
    // Vref = AVCC (5V), канал ADC0, правое выравнивание
    ADMUX  = (1 << REFS0);
    // Включить АЦП, предделитель = 128 (125 кГц при 16 МГц)
    ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
    // Первое преобразование (расширенное) — отброс результата
    ADCSRA |= (1 << ADSC);
    while (ADCSRA & (1 << ADSC));
}

uint16_t adc_read(uint8_t ch) {
    // Установить канал (MUX3:0)
    ADMUX = (ADMUX & 0xF0) | (ch & 0x0F);
    // Запустить преобразование
    ADCSRA |= (1 << ADSC);
    // Ждать завершения
    while (ADCSRA & (1 << ADSC));
    return ADC;   // 10-битный результат (ADCL + ADCH)
}

int main(void) {
    adc_init();
    while (1) {
        uint16_t val = adc_read(0);       // читаем A0
        float voltage = val * 5.0 / 1023; // перевод в вольты
        (void)voltage;
    }
}'''
},

{
'title': 'Чтение датчиков через АЦП',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>Практика: датчики на аналоговых входах</h2>
<p>АЦП ATmega328P позволяет подключать разнообразные аналоговые датчики: потенциометры, термисторы, фоторезисторы, датчики давления и другие.</p>
''' + table(
    ['Датчик','Принцип','Схема подключения','Формула'],
    [
        ['Потенциометр','Делитель напряжения','Средний вывод → A0, крайние → VCC/GND','V = ADC × Vref / 1023'],
        ['Термистор NTC','Сопротивление ↓ при нагреве','Термистор + резистор → делитель','T = 1/(A+B×ln(R)+C×ln(R)³) − 273'],
        ['Фоторезистор LDR','Сопротивление ↓ при освещении','LDR + резистор → делитель','Lux ≈ f(ADC)'],
        ['LM35','10 мВ/°C','Прямо на A0','T = ADC × 500 / 1023 (°C)'],
        ['TMP36','750мВ@25°C, 10мВ/°C','Прямо на A0','T = (ADC × 500/1023) − 50'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="240" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Делитель напряжения для аналоговых датчиков</text>' +
    # VCC
    '<line x1="200" y1="40" x2="200" y2="60" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="200" y="38" text-anchor="middle" font-size="12" fill="#ef4444" font-family="sans-serif">VCC (5В)</text>' +
    # R1
    '<rect x="180" y="60" width="40" height="50" rx="4" fill="#fef9c3" stroke="#f59e0b" stroke-width="1.5"/>' +
    '<text x="200" y="89" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">R1</text>' +
    '<text x="235" y="89" font-size="10" fill="#64748b" font-family="sans-serif">(или датчик)</text>' +
    '<line x1="200" y1="110" x2="200" y2="130" stroke="#1e293b" stroke-width="2"/>' +
    # Node
    '<circle cx="200" cy="130" r="5" fill="#3b82f6"/>' +
    '<line x1="200" y1="130" x2="300" y2="130" stroke="#3b82f6" stroke-width="2"/>' +
    box(300,118,70,25,'#dbeafe','#3b82f6','→ A0 МК',11) +
    # R2
    '<rect x="180" y="130" width="40" height="50" rx="4" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>' +
    '<text x="200" y="159" text-anchor="middle" font-size="11" fill="#14532d" font-family="sans-serif">R2</text>' +
    '<line x1="200" y1="180" x2="200" y2="200" stroke="#1e293b" stroke-width="2"/>' +
    '<line x1="180" y1="200" x2="220" y2="200" stroke="#1e293b" stroke-width="2.5"/>' +
    '<line x1="188" y1="207" x2="212" y2="207" stroke="#1e293b" stroke-width="2"/>' +
    '<text x="200" y="222" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">GND</text>' +
    # Formula
    '<rect x="390" y="60" width="210" height="90" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="495" y="82" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="bold" font-family="sans-serif">Vout = VCC × R2/(R1+R2)</text>' +
    '<text x="495" y="105" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">R1=датчик, R2=10кОм:</text>' +
    '<text x="495" y="125" text-anchor="middle" font-size="11" fill="#3b82f6" font-family="sans-serif">ADC↑ = датчик охладился</text>' +
    '<text x="495" y="142" text-anchor="middle" font-size="11" fill="#ef4444" font-family="sans-serif">ADC↓ = датчик нагрелся</text>' +
    # Smoothing
    '<rect x="390" y="165" width="210" height="60" rx="6" fill="#fef9c3" stroke="#f59e0b"/>' +
    '<text x="495" y="183" text-anchor="middle" font-size="11" fill="#92400e" font-weight="bold" font-family="sans-serif">Усреднение (сглаживание)</text>' +
    '<text x="495" y="203" text-anchor="middle" font-size="10" fill="#92400e" font-family="monospace">avg = (avg*7+new) / 8</text>' +
    '<text x="495" y="218" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">или среднее 16 измерений</text>',
    640, 250, 'Делитель напряжения — основная схема для аналоговых датчиков'
) + tip('Для уменьшения шума: делайте 16 измерений и усредняйте. Это эквивалентно увеличению разрядности АЦП на 2 бита (12 эффективных бит).') +
warn('Внутренний Vref=1.1В даёт лучшее разрешение для слабых сигналов (например, LM35 при комнатной температуре ~0.25В). При Vref=5В шаг 4.9 мВ, при Vref=1.1В — 1.07 мВ.'),
'code_example': '''#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>

// Усреднение 16 отсчётов (увеличивает разрядность до 12 бит)
uint16_t adc_read_avg(uint8_t ch, uint8_t n) {
    uint32_t sum = 0;
    for (uint8_t i = 0; i < n; i++) {
        ADMUX = (ADMUX & 0xF0) | (ch & 0x0F);
        ADCSRA |= (1<<ADSC);
        while (ADCSRA & (1<<ADSC));
        sum += ADC;
    }
    return sum / n;
}

// Температура LM35 (10 мВ/°C, Vref=5В)
float lm35_celsius(uint8_t ch) {
    uint16_t raw = adc_read_avg(ch, 16);
    return raw * 500.0f / 1023.0f;
}

// Термистор NTC 10кОм (B=3950, T0=25°C)
float ntc_celsius(uint8_t ch) {
    uint16_t raw = adc_read_avg(ch, 16);
    if (raw == 0 || raw == 1023) return -999;
    float R = 10000.0f * raw / (1023.0f - raw);  // R термистора
    float lnR = __builtin_log(R / 10000.0f);
    // Уравнение Стейнхарта-Харта (упрощённое)
    float T = 1.0f / (1.0f/298.15f + lnR/3950.0f);
    return T - 273.15f;
}

int main(void) {
    // ADMUX: Vref=AVCC
    ADMUX  = (1<<REFS0);
    ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
    // Прогревочное преобразование
    ADCSRA |= (1<<ADSC); while(ADCSRA & (1<<ADSC));

    while (1) {
        float t = lm35_celsius(0);
        (void)t;
        _delay_ms(500);
    }
}'''
},

{
'title': 'АЦП в режиме прерывания и Free Running',
'order': 3, 'estimated_minutes': 45,
'content': '''
<h2>Режимы запуска АЦП</h2>
<p>Помимо одиночного запуска (по ADSC), АЦП поддерживает автоматические режимы и прерывания — это освобождает ЦП от опроса.</p>
''' + table(
    ['Режим','ADATE','ADTS2:0','Поведение'],
    [
        ['Одиночный','0','—','Ручной запуск через ADSC'],
        ['Free Running','1','000','Автозапуск сразу после завершения'],
        ['Analog Comparator','1','001','Запуск от аналогового компаратора'],
        ['External INT0','1','010','Запуск от внешнего прерывания INT0'],
        ['Timer0 CompA','1','011','Запуск при совпадении Timer0 COMPA'],
        ['Timer0 Overflow','1','100','Запуск при переполнении Timer0'],
        ['Timer1 CompB','1','101','Запуск при совпадении Timer1 COMPB'],
        ['Timer1 Overflow','1','110','Запуск при переполнении Timer1'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="220" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Free Running vs Прерывание</text>' +
    # Free running
    '<rect x="20" y="50" width="280" height="150" rx="8" fill="#dcfce7" stroke="#16a34a"/>' +
    '<text x="160" y="72" text-anchor="middle" font-size="12" fill="#14532d" font-weight="bold" font-family="sans-serif">Free Running Mode</text>' +
    '<text x="35" y="95" font-size="10" fill="#14532d" font-family="sans-serif">1. ADSC=1 → первый запуск</text>' +
    '<text x="35" y="113" font-size="10" fill="#14532d" font-family="sans-serif">2. АЦП завершает → ADIF=1</text>' +
    '<text x="35" y="131" font-size="10" fill="#14532d" font-family="sans-serif">3. Автоматически запускает следующий</text>' +
    '<text x="35" y="149" font-size="10" fill="#14532d" font-family="sans-serif">4. Читаем ADC в ISR(ADC_vect)</text>' +
    '<text x="35" y="170" font-size="10" fill="#16a34a" font-family="sans-serif">✓ Постоянный поток данных</text>' +
    '<text x="35" y="186" font-size="10" fill="#dc2626" font-family="sans-serif">✗ Нельзя переключать каналы</text>' +
    # ISR mode
    '<rect x="330" y="50" width="280" height="150" rx="8" fill="#dbeafe" stroke="#3b82f6"/>' +
    '<text x="470" y="72" text-anchor="middle" font-size="12" fill="#1e40af" font-weight="bold" font-family="sans-serif">Прерывание (ADIE=1)</text>' +
    '<text x="345" y="95" font-size="10" fill="#1e40af" font-family="sans-serif">1. Запускаем ADSC вручную</text>' +
    '<text x="345" y="113" font-size="10" fill="#1e40af" font-family="sans-serif">2. ЦП занимается другой работой</text>' +
    '<text x="345" y="131" font-size="10" fill="#1e40af" font-family="sans-serif">3. АЦП готов → вызов ISR(ADC_vect)</text>' +
    '<text x="345" y="149" font-size="10" fill="#1e40af" font-family="sans-serif">4. В ISR: читаем + запускаем след.</text>' +
    '<text x="345" y="170" font-size="10" fill="#15803d" font-family="sans-serif">✓ Можно менять канал в ISR</text>' +
    '<text x="345" y="186" font-size="10" fill="#15803d" font-family="sans-serif">✓ ЦП не заблокирован</text>',
    640, 230, 'Free Running — непрерывный поток; прерывание — ЦП свободен между измерениями'
) + tip('В ISR(ADC_vect) всегда читайте ADCL <strong>перед</strong> ADCH (или просто используйте ADC) — это гарантирует атомарность 16-битного чтения.') +
warn('Free Running нельзя использовать одновременно с переключением каналов — канал в MUX должен быть стабилен минимум за 1 такт АЦП до запуска.'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>

volatile uint16_t adc_val[3] = {0,0,0};  // каналы 0,1,2
volatile uint8_t  adc_ch = 0;

ISR(ADC_vect) {
    adc_val[adc_ch] = ADC;          // читаем результат
    adc_ch = (adc_ch + 1) % 3;      // следующий канал
    ADMUX = (ADMUX & 0xF0) | adc_ch;
    ADCSRA |= (1<<ADSC);             // запускаем следующее
}

void adc_interrupt_init(void) {
    ADMUX  = (1<<REFS0);             // Vref=AVCC, канал 0
    ADCSRA = (1<<ADEN)|(1<<ADIE)    // вкл + разрешить прерывание
           |(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);  // /128
    // Первый запуск
    ADCSRA |= (1<<ADSC);
    sei();
}

int main(void) {
    adc_interrupt_init();
    while (1) {
        // ЦП свободен, данные обновляются в ISR
        uint16_t pot = adc_val[0];
        uint16_t ldr = adc_val[1];
        (void)pot; (void)ldr;
    }
}'''
},
],

# ─── МОДУЛЬ 7: UART ───────────────────────────────────────────────────────────
7: [
{
'title': 'UART: формат кадра и настройка',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>UART — Universal Asynchronous Receiver/Transmitter</h2>
<p>UART — простейший последовательный интерфейс без тактового сигнала. Обе стороны заранее договариваются о <strong>скорости (baud rate)</strong> и формате кадра.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="180" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Формат UART кадра (8N1 — самый распространённый)</text>' +
    # Idle line
    '<line x1="20" y1="80" x2="60" y2="80" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<text x="40" y="70" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">IDLE</text>' +
    # Start bit
    '<line x1="60" y1="80" x2="60" y2="120" stroke="#ef4444" stroke-width="2.5"/>' +
    '<line x1="60" y1="120" x2="105" y2="120" stroke="#ef4444" stroke-width="2.5"/>' +
    '<rect x="62" y="90" width="40" height="28" rx="2" fill="#fee2e2" opacity="0.7"/>' +
    '<text x="82" y="109" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">START</text>' +
    # Data bits D0-D7
    ''.join([
        f'<line x1="{105+i*45}" y1="120" x2="{105+i*45}" y2="{80 if i%2 else 120}" stroke="#16a34a" stroke-width="2"/>'
        f'<line x1="{105+i*45}" y1="{80 if i%2 else 120}" x2="{150+i*45}" y2="{80 if i%2 else 120}" stroke="#16a34a" stroke-width="2"/>'
        f'<rect x="{107+i*45}" y="88" width="40" height="24" rx="2" fill="#dcfce7" opacity="0.7"/>'
        f'<text x="{127+i*45}" y="104" text-anchor="middle" font-size="9" fill="#14532d" font-family="sans-serif">D{i}</text>'
        for i in range(8)
    ]) +
    # Stop bit
    '<line x1="465" y1="80" x2="465" y2="80" stroke="#6366f1" stroke-width="2.5"/>' +
    '<line x1="465" y1="80" x2="515" y2="80" stroke="#6366f1" stroke-width="2.5"/>' +
    '<line x1="515" y1="80" x2="515" y2="80" stroke="#6366f1" stroke-width="2.5"/>' +
    '<rect x="467" y="68" width="45" height="20" rx="2" fill="#e0e7ff" opacity="0.7"/>' +
    '<text x="490" y="82" text-anchor="middle" font-size="10" fill="#4338ca" font-family="sans-serif">STOP</text>' +
    # Labels
    '<text x="320" y="150" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">8N1: 8 бит данных, No parity, 1 стоп-бит. Всего 10 бит на байт.</text>' +
    '<text x="320" y="168" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">При 9600 бод: 1 бит = 104 мкс, 1 байт = 1.04 мс → ~960 байт/с</text>',
    640, 185, 'UART кадр: 1 старт-бит (LOW) + 8 бит данных (LSB first) + 1 стоп-бит (HIGH)'
) + table(
    ['Скорость (baud)','Применение','Погрешность при 16 МГц'],
    [
        ['9600','Медленные датчики, отладка','0.0%'],
        ['19200','Стандартная отладка','0.0%'],
        ['38400','GPS, Bluetooth модули','0.0%'],
        ['57600','Быстрые модули','0.8%'],
        ['115200','Arduino загрузчик, отладка','2.1%'],
    ]
) + '''<h3>Расчёт UBRR (делитель UART)</h3>
<p style="background:#f1f5f9;padding:10px;border-radius:8px;font-family:monospace">
UBRR = F_CPU / (16 × baud) − 1 &nbsp;&nbsp;(нормальный режим U2X=0)<br>
UBRR = F_CPU / (8 × baud) − 1 &nbsp;&nbsp;&nbsp;(двойная скорость U2X=1)
</p>''' + tip('При 115200 бод погрешность 2.1% — это близко к пределу 4%. Если есть сбои — попробуйте 57600 бод или используйте кварц 11.0592 МГц (даёт 0% погрешность).') +
warn('UART на AVR: TXD=PD1, RXD=PD0. Это же используется для загрузки через USB. Отключите внешнее устройство от RX при прошивке!'),
'code_example': '''#include <avr/io.h>
#include <stdio.h>

#define F_CPU 16000000UL
#define BAUD  9600
#define UBRR_VAL (F_CPU/16/BAUD - 1)

void uart_init(void) {
    UBRR0H = (UBRR_VAL >> 8);
    UBRR0L =  UBRR_VAL;
    UCSR0B = (1<<TXEN0)|(1<<RXEN0);    // вкл TX и RX
    UCSR0C = (1<<UCSZ01)|(1<<UCSZ00);  // 8 бит, 1 стоп, без паритета
}

void uart_putchar(char c) {
    while (!(UCSR0A & (1<<UDRE0)));     // ждём пустой буфер
    UDR0 = c;
}

char uart_getchar(void) {
    while (!(UCSR0A & (1<<RXC0)));      // ждём байт
    return UDR0;
}

void uart_puts(const char *s) {
    while (*s) uart_putchar(*s++);
}

// Привязка к printf
int uart_putchar_printf(char c, FILE *f) {
    (void)f;
    uart_putchar(c);
    return 0;
}
FILE uart_stdout = FDEV_SETUP_STREAM(uart_putchar_printf, NULL, _FDEV_SETUP_WRITE);

int main(void) {
    uart_init();
    stdout = &uart_stdout;
    printf("Hello AVR! ADC=%d\\r\\n", 512);
}'''
},

{
'title': 'UART отладка и протоколы',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>UART как инструмент отладки</h2>
<p>Serial Monitor в Arduino IDE и любой терминал (PuTTY, minicom) позволяют выводить отладочную информацию через UART — это самый простой и универсальный способ отладки МК.</p>
''' + table(
    ['Инструмент','ОС','Настройки'],
    [
        ['Arduino Serial Monitor','Любая','Инструменты → Serial Monitor, выбрать baud'],
        ['PuTTY','Windows','Serial, COM-порт, baud, 8N1'],
        ['minicom','Linux','minicom -b 9600 -o -D /dev/ttyACM0'],
        ['screen','macOS/Linux','screen /dev/tty.usbmodem 9600'],
        ['CoolTerm','Любая','Graphical, logs, hex view'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="220" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Уровни протоколов над UART</text>' +
    box(20,55,580,40,'#fee2e2','#ef4444','Приложение (прикладной протокол): AT-команды, NMEA GPS, Modbus RTU, JSON…',11) +
    box(20,105,580,40,'#fef9c3','#f59e0b','Кадрирование: STX/ETX, длина+данные+CRC, COBS…',11) +
    box(20,155,580,40,'#dcfce7','#16a34a','UART физический уровень: биты, бод, 8N1',11) +
    '<text x="320" y="212" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Каждый уровень добавляет надёжность и структуру</text>',
    640, 225, 'UART — физический уровень; выше строятся прикладные протоколы'
) + '''<h3>Простой бинарный протокол</h3>
<p>Для надёжной передачи структурированных данных используют кадрирование:</p>
<pre style="background:#1e293b;color:#e2e8f0;padding:12px;border-radius:8px;font-size:13px">
[STX=0x02][LEN=N][DATA×N][CRC=XOR всех байт][ETX=0x03]
</pre>''' + tip('Отладочный вывод стоит обернуть в макрос: <code>#ifdef DEBUG ... #endif</code>. Так он не попадёт в релизную прошивку и не замедлит работу.') +
warn('UART буфер AVR = 1 байт. Если вы не успеваете читать (нет RX ISR), следующий байт затрёт предыдущий. Используйте кольцевой буфер в ISR(USART_RX_vect).'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>

// Кольцевой буфер для UART RX
#define RX_BUF_SIZE 64
volatile uint8_t rx_buf[RX_BUF_SIZE];
volatile uint8_t rx_head = 0, rx_tail = 0;

ISR(USART_RX_vect) {
    uint8_t c = UDR0;
    uint8_t next = (rx_head + 1) % RX_BUF_SIZE;
    if (next != rx_tail) {   // буфер не полон
        rx_buf[rx_head] = c;
        rx_head = next;
    }
}

uint8_t uart_available(void) {
    return rx_head != rx_tail;
}

char uart_read(void) {
    while (!uart_available());
    char c = rx_buf[rx_tail];
    rx_tail = (rx_tail + 1) % RX_BUF_SIZE;
    return c;
}

void uart_init_irq(uint16_t ubrr) {
    UBRR0 = ubrr;
    UCSR0B = (1<<RXEN0)|(1<<TXEN0)|(1<<RXCIE0); // RX interrupt
    UCSR0C = (1<<UCSZ01)|(1<<UCSZ00);
    sei();
}

int main(void) {
    uart_init_irq(103);  // 9600 @ 16MHz
    while (1) {
        if (uart_available()) {
            char c = uart_read();
            // эхо
            while (!(UCSR0A & (1<<UDRE0)));
            UDR0 = c;
        }
    }
}'''
},

{
'title': 'Bluetooth и Wi-Fi модули через UART',
'order': 3, 'estimated_minutes': 45,
'content': '''
<h2>Беспроводная связь через UART-модули</h2>
<p>Большинство популярных беспроводных модулей подключаются к МК через UART и управляются AT-командами или прозрачным режимом.</p>
''' + table(
    ['Модуль','Интерфейс','Скорость по умолчанию','Применение'],
    [
        ['HC-05/HC-06','UART (AT+UART)','9600 / 38400 бод','Bluetooth Classic, пара с телефоном'],
        ['HM-10','UART (AT)','9600 бод','Bluetooth LE (BLE), iOS/Android'],
        ['ESP8266 (AT)','UART','115200 бод','Wi-Fi, TCP/UDP, HTTP'],
        ['ESP01','UART','115200 бод','Wi-Fi мини-модуль'],
        ['SIM800L','UART','9600–115200','GSM/GPRS, SMS, звонки'],
        ['nRF24L01','SPI','—','2.4 ГГц, нет UART, только SPI'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="210" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Подключение HC-05 к Arduino</text>' +
    box(20,60,120,100,'#dbeafe','#3b82f6','Arduino\nUno',13,'bold') +
    '<text x="80" y="100" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">TX(PD1) →</text>' +
    '<text x="80" y="118" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">← RX(PD0)</text>' +
    '<text x="80" y="136" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">5V, GND</text>' +
    box(360,60,120,100,'#dcfce7','#16a34a','HC-05\nBluetooth',13,'bold') +
    '<text x="420" y="100" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">→ RX</text>' +
    '<text x="420" y="118" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">TX →</text>' +
    '<text x="420" y="136" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">VCC, GND</text>' +
    # Connections
    '<line x1="140" y1="100" x2="360" y2="100" stroke="#ef4444" stroke-width="2" stroke-dasharray="5"/>' +
    '<line x1="140" y1="118" x2="360" y2="118" stroke="#16a34a" stroke-width="2" stroke-dasharray="5"/>' +
    '<text x="250" y="96" text-anchor="middle" font-size="10" fill="#ef4444" font-family="sans-serif">TX→RX</text>' +
    '<text x="250" y="132" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">RX←TX (делитель!)</text>' +
    # Voltage divider warning
    '<rect x="180" y="140" width="140" height="30" rx="4" fill="#fef9c3" stroke="#f59e0b"/>' +
    '<text x="250" y="153" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">⚠ HC-05 RX: 3.3В!</text>' +
    '<text x="250" y="166" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">Делитель 1кОм+2кОм</text>' +
    '<text x="320" y="195" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Bluetooth телефон ↔ HC-05 ↔ UART ↔ Arduino</text>',
    640, 215, 'Уровень RX у HC-05 = 3.3В: нужен делитель напряжения с TX(5В) Arduino'
) + tip('SoftwareSerial в Arduino позволяет создать второй UART на любых двух цифровых пинах — оставив аппаратный UART для отладки через Serial Monitor.') +
warn('ESP8266 работает от 3.3В! Подключение к 5В выходу Arduino уничтожит модуль. Используйте питание от 3.3В вывода Arduino и делитель для TX линии.'),
'code_example': '''#include <Arduino.h>
#include <SoftwareSerial.h>

// Аппаратный UART (Serial) → PC для отладки
// SoftwareSerial → HC-05 Bluetooth
SoftwareSerial btSerial(8, 9); // RX=8, TX=9

void setup() {
    Serial.begin(9600);       // отладка
    btSerial.begin(9600);     // HC-05 по умолчанию 9600

    // Настройка HC-05 (держать EN=HIGH при включении)
    // btSerial.println("AT");            // → OK
    // btSerial.println("AT+NAME=MyBot"); // → OK
    // btSerial.println("AT+PSWD=1234"); // → OK

    Serial.println("BT ready");
}

void loop() {
    // Данные от Bluetooth → Serial Monitor
    if (btSerial.available()) {
        char c = btSerial.read();
        Serial.write(c);
        // Простые команды
        if (c == '1') { Serial.println("LED ON");  }
        if (c == '0') { Serial.println("LED OFF"); }
    }
    // Serial Monitor → Bluetooth
    if (Serial.available()) {
        btSerial.write(Serial.read());
    }
}'''
},
],

# ─── МОДУЛЬ 8: I2C / SPI ──────────────────────────────────────────────────────
8: [
{
'title': 'Интерфейс I2C (TWI)',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>I2C — двухпроводная шина</h2>
<p><strong>I2C (Inter-Integrated Circuit)</strong>, в AVR называемый TWI (Two Wire Interface), использует всего два провода: <strong>SCL</strong> (тактовый) и <strong>SDA</strong> (данные). Поддерживает до 127 ведомых устройств на одной шине.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="230" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">I2C шина: мастер и несколько ведомых</text>' +
    # Power rails
    '<line x1="20" y1="60" x2="600" y2="60" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="610" y="64" font-size="10" fill="#ef4444" font-family="sans-serif">VCC</text>' +
    '<line x1="20" y1="220" x2="600" y2="220" stroke="#64748b" stroke-width="2"/>' +
    '<text x="610" y="224" font-size="10" fill="#64748b" font-family="sans-serif">GND</text>' +
    # SCL SDA
    '<line x1="20" y1="90" x2="600" y2="90" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<text x="8" y="94" font-size="10" fill="#3b82f6" font-family="sans-serif">SCL</text>' +
    '<line x1="20" y1="115" x2="600" y2="115" stroke="#16a34a" stroke-width="2.5"/>' +
    '<text x="8" y="119" font-size="10" fill="#16a34a" font-family="sans-serif">SDA</text>' +
    # Pull-ups
    '<line x1="100" y1="60" x2="100" y2="90" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3"/>' +
    '<text x="103" y="78" font-size="9" fill="#94a3b8" font-family="sans-serif">4.7k</text>' +
    '<line x1="130" y1="60" x2="130" y2="115" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3"/>' +
    '<text x="133" y="90" font-size="9" fill="#94a3b8" font-family="sans-serif">4.7k</text>' +
    # Master
    box(160,130,100,60,'#dbeafe','#3b82f6','Master\n(Arduino)',12,'bold') +
    '<line x1="210" y1="130" x2="210" y2="115" stroke="#16a34a" stroke-width="1.5"/>' +
    '<line x1="210" y1="130" x2="210" y2="90" stroke="#3b82f6" stroke-width="1.5"/>' +
    # Slaves
    box(300,130,80,50,'#dcfce7','#16a34a','0x3C\nOLED',11) +
    '<line x1="340" y1="130" x2="340" y2="102" stroke="#1e293b" stroke-width="1.5"/>' +
    box(400,130,80,50,'#fef9c3','#f59e0b','0x68\nMPU6050',11) +
    '<line x1="440" y1="130" x2="440" y2="102" stroke="#1e293b" stroke-width="1.5"/>' +
    box(500,130,80,50,'#fdf4ff','#a855f7','0x77\nBMP280',11) +
    '<line x1="540" y1="130" x2="540" y2="102" stroke="#1e293b" stroke-width="1.5"/>' +
    '<text x="320" y="210" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Все устройства на одной паре проводов, каждое имеет 7-битный адрес</text>',
    640, 235, 'I2C: один мастер управляет несколькими ведомыми по адресу'
) + table(
    ['Параметр','Стандартный','Быстрый','Быстрый+'],
    [
        ['Скорость','100 кбит/с','400 кбит/с','1 Мбит/с'],
        ['Подтяжка SCL/SDA','4.7 кОм','2.2 кОм','1 кОм'],
        ['Макс. ёмкость шины','400 пФ','400 пФ','550 пФ'],
        ['Поддержка AVR','Да','Да','Нет (TWI до 400 кГц)'],
    ]
) + tip('Wire.begin() в Arduino настраивает TWI на 100 кГц. Для 400 кГц: <code>Wire.setClock(400000)</code>. Это ускоряет OLED/датчики в 4 раза.') +
warn('I2C требует подтягивающих резисторов 4.7 кОм на SCL и SDA (к VCC). Без них шина не работает. На некоторых breakout-платах они уже встроены.'),
'code_example': '''#include <Wire.h>  // Arduino I2C (TWI)

// Пример: чтение MPU-6050 (гироскоп+акселерометр)
#define MPU_ADDR 0x68

int16_t ax, ay, az, gx, gy, gz;

void mpu_init(void) {
    Wire.begin();
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x6B);  // регистр PWR_MGMT_1
    Wire.write(0);     // выход из сна
    Wire.endTransmission(true);
}

void mpu_read(void) {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);  // начало регистров акселерометра
    Wire.endTransmission(false);  // repeated start
    Wire.requestFrom(MPU_ADDR, 14, true); // 14 байт

    ax = (Wire.read()<<8) | Wire.read();
    ay = (Wire.read()<<8) | Wire.read();
    az = (Wire.read()<<8) | Wire.read();
    Wire.read(); Wire.read();  // температура (пропуск)
    gx = (Wire.read()<<8) | Wire.read();
    gy = (Wire.read()<<8) | Wire.read();
    gz = (Wire.read()<<8) | Wire.read();
}

void setup() {
    Serial.begin(115200);
    mpu_init();
}
void loop() {
    mpu_read();
    Serial.print("AX="); Serial.print(ax);
    Serial.print(" AY="); Serial.print(ay);
    Serial.print(" AZ="); Serial.println(az);
    delay(100);
}'''
},

{
'title': 'Интерфейс SPI',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>SPI — Serial Peripheral Interface</h2>
<p>SPI — синхронный последовательный интерфейс с 4 проводами. Быстрее I2C, но требует отдельный CS (Chip Select) для каждого ведомого.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="220" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">SPI: 4 провода мастер ↔ ведомый</text>' +
    box(60,70,140,120,'#dbeafe','#3b82f6','Master\n(ATmega)',13,'bold') +
    box(400,70,140,120,'#dcfce7','#16a34a','Slave\n(SD/дисплей)',13,'bold') +
    # Lines
    '<line x1="200" y1="100" x2="400" y2="100" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="300" y="96" text-anchor="middle" font-size="10" fill="#ef4444" font-family="sans-serif">SCK (PB5)</text>' +
    '<line x1="200" y1="120" x2="400" y2="120" stroke="#3b82f6" stroke-width="2"/>' +
    '<text x="300" y="116" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">MOSI (PB3) master→slave</text>' +
    '<line x1="200" y1="140" x2="400" y2="140" stroke="#16a34a" stroke-width="2"/>' +
    '<text x="300" y="136" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">MISO (PB4) slave→master</text>' +
    '<line x1="200" y1="160" x2="400" y2="160" stroke="#f59e0b" stroke-width="2"/>' +
    '<text x="300" y="156" text-anchor="middle" font-size="10" fill="#b45309" font-family="sans-serif">SS/CS (PB2) active LOW</text>' +
    '<text x="320" y="205" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Полный дуплекс: MOSI и MISO одновременно. Скорость до F_CPU/2 (8 МГц @ 16 МГц)</text>',
    640, 220, 'SPI: MOSI выход мастера, MISO вход мастера, SCK тактовый, SS выбор ведомого'
) + table(
    ['','I2C','SPI'],
    [
        ['Проводов','2 (SCL, SDA)','4 (SCK, MOSI, MISO, SS)'],
        ['Скорость','до 400 кбит/с','до 8 Мбит/с (AVR)'],
        ['Несколько ведомых','По адресу (одна шина)','По CS (отдельный провод каждому)'],
        ['Дуплекс','Полу','Полный'],
        ['Применение','Датчики, OLED, EEPROM','SD карты, дисплеи, АЦП, Flash'],
        ['Сложность','Выше (адресация, ACK)','Ниже (простой протокол)'],
    ]
) + tip('Несколько SPI-устройств на одной шине SCK/MOSI/MISO, но у каждого свой CS вывод. Выбираем нужное устройство, подтягивая его CS к LOW.') +
warn('SPI не имеет стандартного протокола подтверждения (ACK). Если ведомый не отвечает, мастер не узнает об этом автоматически — нужна проверка на прикладном уровне.'),
'code_example': '''#include <SPI.h>   // Arduino SPI

// Пример: чтение SD карты через SPI
// CS = pin 10 (SS, PB2)
#define SD_CS 10

void spi_demo(void) {
    SPI.begin();
    SPI.setClockDivider(SPI_CLOCK_DIV16);  // 16МГц/16 = 1 МГц
    SPI.setDataMode(SPI_MODE0);             // CPOL=0, CPHA=0
    SPI.setBitOrder(MSBFIRST);

    // Ручное управление CS
    digitalWrite(SD_CS, LOW);   // выбрать ведомого
    uint8_t response = SPI.transfer(0xFF); // отправить 0xFF, получить ответ
    SPI.transfer(0x40);          // CMD0
    SPI.transfer(0x00);
    SPI.transfer(0x00);
    SPI.transfer(0x00);
    SPI.transfer(0x00);
    SPI.transfer(0x95);          // CRC для CMD0
    digitalWrite(SD_CS, HIGH);  // снять выбор
    (void)response;
}

// Прямой доступ к регистрам SPI (без Arduino библиотеки)
void spi_raw_init(void) {
    DDRB |= (1<<PB3)|(1<<PB5)|(1<<PB2);  // MOSI, SCK, SS = выходы
    DDRB &= ~(1<<PB4);                     // MISO = вход
    SPCR = (1<<SPE)|(1<<MSTR)|(1<<SPR0);  // SPI вкл, мастер, /16
}

uint8_t spi_raw_transfer(uint8_t data) {
    SPDR = data;
    while (!(SPSR & (1<<SPIF)));  // ждём завершения
    return SPDR;
}'''
},

{
'title': 'Популярные I2C/SPI устройства',
'order': 3, 'estimated_minutes': 45,
'content': '''
<h2>Экосистема датчиков и дисплеев</h2>
<p>Современные проекты на AVR используют богатую экосистему готовых модулей. Вот самые популярные.</p>
''' + table(
    ['Устройство','Интерфейс','Адрес/CS','Библиотека Arduino','Что умеет'],
    [
        ['OLED SSD1306','I2C','0x3C или 0x3D','Adafruit_SSD1306','128×64 пикселей, текст, графика'],
        ['BMP280','I2C или SPI','0x76/0x77','Adafruit_BMP280','Давление, температура, высота'],
        ['MPU-6050','I2C','0x68/0x69','MPU6050','Акселерометр + гироскоп 6DOF'],
        ['DS3231','I2C','0x68','RTClib','Часы реального времени (RTC)'],
        ['AT24C32','I2C','0x50–0x57','Wire','EEPROM 32 Кбит'],
        ['SD карта','SPI','Любой CS','SD.h','FAT16/FAT32 файловая система'],
        ['MAX7219','SPI','CS','LedControl','Матрица 8×8 LED или 7-сегм. дисплей'],
        ['NRF24L01','SPI','CE+CS','RF24','2.4 ГГц радио до 100 м'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="230" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Типичный проект: Arduino + OLED + BMP280 + SD</text>' +
    box(240,55,160,60,'#dbeafe','#3b82f6','Arduino Uno\nATmega328P',13,'bold') +
    # I2C bus
    '<line x1="200" y1="80" x2="80" y2="80" stroke="#16a34a" stroke-width="2"/>' +
    '<line x1="80" y1="80" x2="80" y2="150" stroke="#16a34a" stroke-width="2"/>' +
    '<text x="140" y="73" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">I2C (SDA/SCL)</text>' +
    box(20,150,120,50,'#dcfce7','#16a34a','OLED 0x3C',12) +
    '<line x1="80" y1="150" x2="80" y2="200" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4"/>' +
    box(20,200,120,25,'#dcfce7','#16a34a','BMP280 0x76',11) +
    # SPI bus
    '<line x1="400" y1="80" x2="520" y2="80" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="520" y1="80" x2="520" y2="150" stroke="#3b82f6" stroke-width="2"/>' +
    '<text x="460" y="73" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">SPI (MOSI/MISO/SCK)</text>' +
    box(460,150,120,50,'#dbeafe','#3b82f6','SD Card\nCS=pin10',12) +
    # UART
    '<line x1="320" y1="115" x2="320" y2="160" stroke="#f59e0b" stroke-width="2"/>' +
    box(260,160,120,35,'#fef9c3','#f59e0b','Serial Monitor\nUSB-UART',11),
    640, 245, 'Один МК управляет несколькими устройствами на разных шинах'
) + tip('Библиотека Wire позволяет сканировать I2C шину: перебирайте адреса 1–127 и вызывайте beginTransmission/endTransmission. Если endTransmission() вернул 0 — устройство найдено.') +
warn('При использовании нескольких I2C устройств с одним адресом (например, два SSD1306) нужно аппаратно изменить адрес (пин ADDR на GND/VCC) или использовать I2C мультиплексор TCA9548A.'),
'code_example': '''#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BMP280.h>

Adafruit_SSD1306 oled(128, 64, &Wire);
Adafruit_BMP280 bmp;

void setup() {
    Wire.begin();
    oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    bmp.begin(0x76);

    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(WHITE);
}

void loop() {
    float temp = bmp.readTemperature();
    float pres = bmp.readPressure() / 100.0f;  // Па → гПа

    oled.clearDisplay();
    oled.setCursor(0, 0);
    oled.print("Temp: ");
    oled.print(temp, 1);
    oled.println(" C");
    oled.print("Pres: ");
    oled.print(pres, 1);
    oled.println(" hPa");
    oled.display();

    delay(2000);
}

// Сканер I2C — для диагностики
void i2c_scan(void) {
    for (uint8_t addr = 1; addr < 127; addr++) {
        Wire.beginTransmission(addr);
        if (Wire.endTransmission() == 0) {
            Serial.print("Found: 0x");
            Serial.println(addr, HEX);
        }
    }
}'''
},
],

# ─── МОДУЛЬ 9: АССЕМБЛЕР ─────────────────────────────────────────────────────
9: [
{
'title': 'Синтаксис AVR Assembler',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>Язык ассемблера AVR</h2>
<p>Ассемблер — язык программирования, в котором каждая строка соответствует одной машинной команде. Знание ассемблера AVR позволяет писать оптимальный по скорости и размеру код и понимать, что реально делает МК.</p>
''' + table(
    ['Элемент','Синтаксис','Пример','Описание'],
    [
        ['Метка','name:','loop:','Имя адреса в программе'],
        ['Команда','мнемоника операнды','ldi r16, 42','Инструкция процессора'],
        ['Директива','.директива','<code>.org 0x0000</code>','Управление ассемблером'],
        ['Комментарий','; текст','<code>; инициализация</code>','Игнорируется'],
        ['Константа','.equ NAME = VAL','<code>.equ LED = 5</code>','Именованная константа'],
        ['Данные','.byte .word .db','<code>.byte 0x55</code>','Данные в памяти'],
        ['Сегменты','.cseg .dseg .eseg','<code>.cseg</code>','Code/Data/EEPROM сегменты'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="230" rx="10" fill="#1e293b" stroke="#334155"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#e2e8f0" font-weight="bold" font-family="monospace">Структура ASM программы для ATmega328P</text>' +
    '<text x="30" y="58" font-size="12" fill="#94a3b8" font-family="monospace">.include "m328pdef.inc"   ; определения регистров</text>' +
    '<text x="30" y="78" font-size="12" fill="#7dd3fc" font-family="monospace">.org 0x0000              ; вектор RESET</text>' +
    '<text x="30" y="96" font-size="12" fill="#86efac" font-family="monospace">    rjmp main            ; переход к main</text>' +
    '<text x="30" y="116" font-size="12" fill="#7dd3fc" font-family="monospace">.org 0x0004              ; вектор INT0</text>' +
    '<text x="30" y="134" font-size="12" fill="#86efac" font-family="monospace">    rjmp int0_isr</text>' +
    '<text x="30" y="154" font-size="12" fill="#fcd34d" font-family="monospace">main:</text>' +
    '<text x="30" y="172" font-size="12" fill="#86efac" font-family="monospace">    ldi  r16, HIGH(RAMEND)</text>' +
    '<text x="30" y="190" font-size="12" fill="#86efac" font-family="monospace">    out  SPH, r16        ; инициализация стека</text>' +
    '<text x="30" y="208" font-size="12" fill="#86efac" font-family="monospace">    ldi  r16, LOW(RAMEND)</text>' +
    '<text x="30" y="226" font-size="12" fill="#86efac" font-family="monospace">    out  SPL, r16</text>',
    640, 240, 'Типичная структура AVR ASM программы'
) + tip('Директива <code>.include "m328pdef.inc"</code> подключает файл с именами всех регистров ATmega328P. Без неё пришлось бы писать числовые адреса вместо PORTB, DDRB и т.д.') +
warn('AVR ASM использует Little Endian: младший байт по меньшему адресу. При записи 16-битных данных в память сначала пишется LOW-байт, потом HIGH.'),
'code_example': '''; Мигание LED на чистом ASM (ATmega328P, 16 МГц)
.include "m328pdef.inc"
.def temp  = r16
.def cnt_l = r24
.def cnt_h = r25

.org 0x0000
    rjmp main

main:
    ; Инициализация стека
    ldi  temp, HIGH(RAMEND)
    out  SPH, temp
    ldi  temp, LOW(RAMEND)
    out  SPL, temp

    ; PB5 = выход (LED)
    ldi  temp, (1<<PB5)
    out  DDRB, temp

loop:
    ; LED включить
    sbi  PORTB, PB5
    rcall delay_500ms
    ; LED выключить
    cbi  PORTB, PB5
    rcall delay_500ms
    rjmp loop

delay_500ms:
    ; 500мс при 16 МГц: 8 000 000 тактов = 0x7A120
    ldi  cnt_h, HIGH(8000000/3)
    ldi  cnt_l, LOW(8000000/3)
dly_loop:
    sbiw cnt_l, 1     ; dec 16-bit (2 такта)
    brne dly_loop     ; (1 такт если =0, 2 если ≠0)
    ret'''
},

{
'title': 'Подпрограммы и стек в ASM',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>Вызов подпрограмм и работа со стеком</h2>
<p>Стек в AVR — область SRAM от RAMEND вниз. Используется для сохранения адреса возврата при вызове подпрограмм (call/rcall) и явного сохранения регистров (push/pop).</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="250" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Стек AVR при вызове подпрограммы</text>' +
    # SRAM layout
    '<rect x="40" y="50" width="120" height="180" rx="4" fill="#dbeafe" stroke="#3b82f6"/>' +
    '<text x="100" y="70" text-anchor="middle" font-size="11" fill="#1e40af" font-weight="bold" font-family="sans-serif">SRAM</text>' +
    '<rect x="44" y="75" width="112" height="20" rx="2" fill="#bfdbfe"/>' +
    '<text x="100" y="88" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">0x0100 (RAMSTART)</text>' +
    ''.join(f'<rect x="44" y="{100+i*18}" width="112" height="16" rx="2" fill="#eff6ff"/>' for i in range(4)) +
    '<rect x="44" y="173" width="112" height="20" rx="2" fill="#fee2e2" stroke="#ef4444"/>' +
    '<text x="100" y="186" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">→ addr_ret (push)</text>' +
    '<rect x="44" y="195" width="112" height="20" rx="2" fill="#fee2e2" stroke="#ef4444"/>' +
    '<text x="100" y="208" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">r16 saved (push)</text>' +
    '<rect x="44" y="215" width="112" height="12" rx="2" fill="#bbf7d0"/>' +
    '<text x="100" y="224" text-anchor="middle" font-size="10" fill="#15803d" font-family="sans-serif">← SP (0x08FF)</text>' +
    # SP arrow
    '<text x="170" y="228" font-size="11" fill="#ef4444" font-family="sans-serif">↑ SP растёт вниз</text>' +
    # Call flow
    '<rect x="280" y="50" width="300" height="190" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="430" y="72" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Последовательность вызова</text>' +
    '<text x="295" y="95" font-size="10" fill="#3b82f6" font-family="monospace">1. rcall subr    ; push PC, jump</text>' +
    '<text x="295" y="113" font-size="10" fill="#16a34a" font-family="monospace">2. push r16       ; сохранить reg</text>' +
    '<text x="295" y="131" font-size="10" fill="#16a34a" font-family="monospace">3. ... работа ...'  '</text>' +
    '<text x="295" y="149" font-size="10" fill="#f59e0b" font-family="monospace">4. pop r16        ; восстановить</text>' +
    '<text x="295" y="167" font-size="10" fill="#ef4444" font-family="monospace">5. ret             ; pop PC, return</text>' +
    '<text x="430" y="195" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">push/pop должны быть симметричны!</text>' +
    '<text x="430" y="212" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">Дисбаланс → стек испорчен → crash</text>',
    640, 260, 'Стек растёт вниз; call кладёт адрес возврата, ret снимает его'
) + tip('Соглашение AVR: r0, r1 — временные (портят вызываемые), r18–r27, r30–r31 — свободно используемые, r2–r17, r28–r29 — должны быть сохранены вызываемыми.') +
warn('Если подпрограмма использует прерывания, SREG тоже нужно сохранять: <code>in r0, SREG / push r0 … pop r0 / out SREG, r0</code>.'),
'code_example': '''; Подпрограмма умножения 8x8 = 16 бит
; Вход: r16 = a, r17 = b
; Выход: r25:r24 = результат (старший:младший)
; Использует: r0, r1 (mul результат), r16, r17

mul8x8:
    push r16          ; сохранить аргументы (опционально)
    push r17
    mul  r16, r17     ; r1:r0 = r16 × r17
    mov  r24, r0      ; младший байт результата
    mov  r25, r1      ; старший байт
    clr  r1           ; AVR ABI: r1 всегда = 0 после mul
    pop  r17
    pop  r16
    ret

; Пример вызова:
;   ldi r16, 12
;   ldi r17, 25
;   rcall mul8x8
;   ; r25:r24 = 300 (0x012C)

; Рекурсия (факториал, n<=5 чтобы не переполнить стек)
; Вход/выход: r16 = n/n!
factorial:
    cpi  r16, 1
    brlo fact_done    ; n <= 0: возврат 1
    breq fact_done    ; n == 1: возврат 1
    push r16          ; сохранить n
    dec  r16          ; n-1
    rcall factorial   ; r16 = (n-1)!
    pop  r17          ; восстановить n в r17
    mul  r16, r17     ; r16 * n
    mov  r16, r0
    clr  r1
    ret
fact_done:
    ldi  r16, 1
    ret'''
},

{
'title': 'Смешанное программирование C + ASM',
'order': 3, 'estimated_minutes': 45,
'content': '''
<h2>Inline ASM в C-коде (avr-gcc)</h2>
<p>Иногда нужно вставить несколько ассемблерных команд прямо в C-код — для критичных по скорости участков или недоступных из C инструкций.</p>
''' + table(
    ['Способ','Применение','Синтаксис'],
    [
        ['asm volatile','Одна-несколько команд в C','<code>asm volatile("nop\\n");</code>'],
        ['Extended asm','С переменными C','<code>asm volatile(...:...:..);</code>'],
        ['Отдельный .S файл','Большие ASM модули','Линкуется вместе с .c файлами'],
        ['__attribute__((naked))','Функция без пролога','Только asm, без push/pop'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="210" rx="10" fill="#1e293b" stroke="#334155"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#e2e8f0" font-weight="bold" font-family="monospace">Extended Inline ASM — синтаксис</text>' +
    '<text x="30" y="58" font-size="11" fill="#7dd3fc" font-family="monospace">asm volatile (</text>' +
    '<text x="30" y="76" font-size="11" fill="#86efac" font-family="monospace">    "команда1 \\n\\t"     // ассемблерный шаблон</text>' +
    '<text x="30" y="94" font-size="11" fill="#86efac" font-family="monospace">    "команда2 %0 \\n\\t"  // %0 = первый операнд</text>' +
    '<text x="30" y="112" font-size="11" fill="#fcd34d" font-family="monospace">    : "=r"(output)       // выходные операнды</text>' +
    '<text x="30" y="130" font-size="11" fill="#f9a8d4" font-family="monospace">    : "r"(input1), "r"(input2)  // входные</text>' +
    '<text x="30" y="148" font-size="11" fill="#fca5a5" font-family="monospace">    : "r0", "r1"          // clobbered (испорченные)</text>' +
    '<text x="30" y="166" font-size="11" fill="#7dd3fc" font-family="monospace">);</text>' +
    '<text x="30" y="190" font-size="11" fill="#94a3b8" font-family="monospace">// Ограничения: "r"=регистр, "I"=конст 0-63, "M"=конст 0-255</text>',
    640, 210, 'Синтаксис extended inline ASM для avr-gcc'
) + tip('Директива <code>asm volatile("nop")</code> вставляет один пустой такт — полезно для точных задержек или синхронизации с периферией.') +
warn('<code>volatile</code> запрещает оптимизатору удалять или перемещать ASM-вставку. Без него компилятор может выкинуть "бесполезный" код.'),
'code_example': '''#include <avr/io.h>

// Быстрый обмен байтов (swap nibbles) через ASM
uint8_t swap_nibbles(uint8_t x) {
    uint8_t result;
    asm volatile (
        "swap %0"       // AVR команда swap nibbles
        : "=r"(result)  // выход: result = любой регистр
        : "0"(x)        // вход: x в том же регистре что result
    );
    return result;
}

// Точная задержка в тактах (без _delay_ms)
void delay_cycles(uint16_t n) {
    asm volatile (
        "1: sbiw %0, 1  \\n\\t"   // dec 16-bit (2 такта)
        "   brne 1b     \\n\\t"   // branch (1/2 такта)
        : "=w"(n)                  // "w" = регистровая пара (X,Y,Z)
        : "0"(n)
    );
}

// Атомарная операция (запрет прерываний на время)
static inline void atomic_inc(volatile uint8_t *p) {
    asm volatile (
        "cli        \\n\\t"    // запрет прерываний
        "ld  r24, %a0 \\n\\t"  // загрузить *p
        "inc r24     \\n\\t"   // инкремент
        "st  %a0, r24 \\n\\t"  // сохранить
        "sei         \\n\\t"   // разрешить прерывания
        :
        : "e"(p)               // "e" = указатель X/Y/Z
        : "r24"
    );
}

int main(void) {
    uint8_t x = 0xAB;
    uint8_t s = swap_nibbles(x);  // s = 0xBA
    (void)s;
    delay_cycles(1000);            // 1000 тактов = 62.5 мкс @ 16МГц
}'''
},
],

# ─── МОДУЛЬ 10: ПРОЕКТ ────────────────────────────────────────────────────────
10: [
{
'title': 'Критерии выбора микроконтроллера',
'order': 1, 'estimated_minutes': 50,
'content': '''
<h2>Как выбрать МК под задачу</h2>
<p>Неправильный выбор МК на начальном этапе — частая и дорогостоящая ошибка. Рассмотрим ключевые критерии.</p>
''' + table(
    ['Критерий','Вопросы для анализа','Влияние на выбор'],
    [
        ['Производительность','Сколько операций/с нужно?','8-бит AVR (20MIPS) vs 32-бит ARM (>100MIPS)'],
        ['Периферия','UART/SPI/I2C/CAN/USB/Ethernet?','Разные МК имеют разные наборы'],
        ['Flash/RAM','Размер программы и данных?','AVR: 2–256 КБ Flash, 0.1–16 КБ RAM'],
        ['Напряжение','3.3В или 5В система?','AVR: 1.8–5.5В (ATmega328P: 2.7–5.5В)'],
        ['Потребление','Батарейное питание?','ATmega328P sleep <1 мкА'],
        ['Корпус','Пайка вручную или автоматически?','DIP=легко, TQFP=паяльная станция'],
        ['Стоимость','Серийный продукт?','AVR: $1–5, STM32: $1–10, ESP32: $2–5'],
        ['Экосистема','Библиотеки, поддержка?','Arduino IDE = огромная экосистема'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="230" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Популярные МК: сравнение</text>' +
    box(20,50,130,160,'#dbeafe','#3b82f6','ATmega328P\n(Arduino Uno)',12,'bold') +
    '<text x="85" y="105" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">8 бит, 20 МГц</text>' +
    '<text x="85" y="121" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">32 КБ Flash</text>' +
    '<text x="85" y="137" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">23 GPIO</text>' +
    '<text x="85" y="153" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Прост в изучении</text>' +
    '<text x="85" y="169" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">$2–3 (DIP28)</text>' +
    box(165,50,130,160,'#dcfce7','#16a34a','STM32F103\n(Blue Pill)',12,'bold') +
    '<text x="230" y="105" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">32 бит, 72 МГц</text>' +
    '<text x="230" y="121" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">64 КБ Flash</text>' +
    '<text x="230" y="137" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">37 GPIO, USB</text>' +
    '<text x="230" y="153" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Высокая произв.</text>' +
    '<text x="230" y="169" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">$1–2 (LQFP48)</text>' +
    box(310,50,130,160,'#fef9c3','#f59e0b','ESP32\n(Wi-Fi+BT)',12,'bold') +
    '<text x="375" y="105" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">32 бит, 240 МГц</text>' +
    '<text x="375" y="121" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">4 МБ Flash</text>' +
    '<text x="375" y="137" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">Wi-Fi + BT</text>' +
    '<text x="375" y="153" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">IoT проекты</text>' +
    '<text x="375" y="169" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">$3–5 (модуль)</text>' +
    box(455,50,150,160,'#fdf4ff','#a855f7','ATtiny85\n(малый МК)',12,'bold') +
    '<text x="530" y="105" text-anchor="middle" font-size="10" fill="#6b21a8" font-family="sans-serif">8 бит, 20 МГц</text>' +
    '<text x="530" y="121" text-anchor="middle" font-size="10" fill="#6b21a8" font-family="sans-serif">8 КБ Flash</text>' +
    '<text x="530" y="137" text-anchor="middle" font-size="10" fill="#6b21a8" font-family="sans-serif">6 GPIO</text>' +
    '<text x="530" y="153" text-anchor="middle" font-size="10" fill="#6b21a8" font-family="sans-serif">Для простых задач</text>' +
    '<text x="530" y="169" text-anchor="middle" font-size="10" fill="#6b21a8" font-family="sans-serif">$0.5–1 (SOIC8)</text>',
    640, 240, 'Каждый МК оптимален для своего класса задач'
) + tip('Для учебных проектов оптимален ATmega328P (Arduino Uno): достаточная периферия, простой DIP-корпус, огромная документация. Для IoT — ESP32.') +
warn('Не берите "про запас" более мощный МК — это увеличивает стоимость, потребление и сложность. Выбирайте под задачу.'),
'code_example': '''// Таблица сравнения ATmega328P vs STM32F103

// ATmega328P (8-бит, 5В)
// ✓ Простота, 5В совместимость
// ✓ DIP-корпус, легко паять
// ✓ Arduino экосистема
// ✗ 8-бит, 20 МГц
// ✗ Нет USB нативного

// STM32F103 (32-бит, 3.3В)
// ✓ Мощный ARM Cortex-M3
// ✓ Нативный USB, CAN, I2S
// ✓ Дешевле при серийном выпуске
// ✗ 3.3В (нужны преобразователи для 5В датчиков)
// ✗ Сложнее toolchain

// Правило выбора:
// - Учёба, хобби, простые устройства → ATmega328P/Arduino
// - Моторный контроль, точные таймеры → ATmega/ATtiny
// - Серийный продукт, мощность нужна → STM32
// - IoT, Wi-Fi/BT → ESP32/ESP8266
// - Очень малый размер → ATtiny85, STM32F030F'''
},

{
'title': 'Отладка и тестирование МК систем',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>Стратегии отладки встраиваемых систем</h2>
<p>Отладка МК сложнее, чем отладка PC-программ: нет операционной системы, нет стандартного вывода, код выполняется в реальном времени. Рассмотрим доступные инструменты.</p>
''' + table(
    ['Метод','Инструменты','Плюсы','Минусы'],
    [
        ['Serial print','UART + терминал','Прост, не нужно оборудование','Замедляет программу, засоряет код'],
        ['LED индикация','Встроенный LED','Без доп. оборудования','Только 1 бит информации'],
        ['Логический анализатор','Saleae, DSLogic','Видит все сигналы шин','Нужен прибор'],
        ['Осциллограф','Аналоговые + цифровые','Точные временны́е измерения','Дорогой прибор'],
        ['JTAG/debugWIRE','avr-gdb + avarice','Точечные брейкпоинты','Нужен адаптер, не все МК'],
        ['Симулятор','Proteus, SimulIDE','Без железа','Не всегда точен'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="230" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Пирамида отладки: от простого к сложному</text>' +
    # Pyramid layers
    '<polygon points="320,55 450,180 190,180" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>' +
    '<line x1="248" y1="105" x2="392" y2="105" stroke="#16a34a" stroke-width="1.5"/>' +
    '<line x1="270" y1="140" x2="370" y2="140" stroke="#16a34a" stroke-width="1.5"/>' +
    '<text x="320" y="90" text-anchor="middle" font-size="11" fill="#14532d" font-weight="bold" font-family="sans-serif">LED</text>' +
    '<text x="320" y="127" text-anchor="middle" font-size="11" fill="#14532d" font-family="sans-serif">Serial.print()</text>' +
    '<text x="320" y="162" text-anchor="middle" font-size="11" fill="#14532d" font-family="sans-serif">Логический анализатор</text>' +
    '<text x="320" y="197" text-anchor="middle" font-size="11" fill="#14532d" font-family="sans-serif">JTAG / debugWIRE + GDB</text>' +
    '<text x="80" y="95" font-size="10" fill="#64748b" font-family="sans-serif">← быстро,</text>' +
    '<text x="80" y="110" font-size="10" fill="#64748b" font-family="sans-serif">   всегда</text>' +
    '<text x="80" y="165" font-size="10" fill="#64748b" font-family="sans-serif">← нужен прибор</text>' +
    '<text x="80" y="200" font-size="10" fill="#64748b" font-family="sans-serif">← полная власть</text>' +
    '<text x="500" y="95" font-size="10" fill="#64748b" font-family="sans-serif">просто →</text>' +
    '<text x="500" y="165" font-size="10" fill="#64748b" font-family="sans-serif">сложнее →</text>',
    640, 240, 'Начинайте с простого — чаще всего LED + Serial достаточно'
) + tip('Техника «мигающего кода» (heartbeat): заставьте LED мигать с заданной частотой в main loop. Если он мигает — программа жива. Изменение частоты сигнализирует о застревании в цикле.') +
warn('Никогда не используйте delay() в сложных проектах для «временной» отладки — он нарушает временны́е соотношения и маскирует проблемы с прерываниями.'),
'code_example': '''#include <Arduino.h>

// Отладочные макросы — отключаются в релизе
#define DEBUG 1

#if DEBUG
  #define DBG_PRINT(x)   Serial.print(x)
  #define DBG_PRINTLN(x) Serial.println(x)
  #define DBG_PRINTF(...) Serial.print(__VA_ARGS__)
#else
  #define DBG_PRINT(x)
  #define DBG_PRINTLN(x)
  #define DBG_PRINTF(...)
#endif

// Heartbeat: мигание LED каждые 500 мс
// Если остановилось — программа зависла
class Heartbeat {
    uint32_t last;
    uint8_t  pin, state;
    uint32_t interval;
public:
    Heartbeat(uint8_t p, uint32_t ms=500): pin(p), state(0), interval(ms) {
        pinMode(pin, OUTPUT);
        last = millis();
    }
    void update() {
        if (millis() - last >= interval) {
            last += interval;
            state ^= 1;
            digitalWrite(pin, state);
        }
    }
};

Heartbeat hb(LED_BUILTIN);

void setup() {
    Serial.begin(115200);
    DBG_PRINTLN("Boot OK");
}

void loop() {
    hb.update();   // должен вызываться ≥2 раз в секунду
    // ... ваш код ...
    DBG_PRINTF("ADC0="); DBG_PRINTLN(analogRead(A0));
}'''
},

{
'title': 'Финальный проект: метеостанция',
'order': 3, 'estimated_minutes': 60,
'content': '''
<h2>Финальный проект: цифровая метеостанция</h2>
<p>Объединим все изученные темы в одном проекте: ATmega328P читает датчики температуры/давления через I2C, выводит данные на OLED, отправляет через UART/Bluetooth и реагирует на кнопки без блокирующего кода.</p>
''' + table(
    ['Компонент','Интерфейс','Функция в проекте'],
    [
        ['BMP280','I2C 0x76','Температура (°C) + атмосферное давление (гПа)'],
        ['DHT22','1-wire GPIO','Влажность (%) + температура'],
        ['SSD1306 OLED','I2C 0x3C','Отображение данных 128×64'],
        ['HC-05 BT','UART SoftSerial','Отправка данных на смартфон'],
        ['Кнопка × 2','GPIO + PCINT','Переключение экранов'],
        ['LED × 1','GPIO','Индикатор работы (heartbeat)'],
    ]
) + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="260" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="32" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Архитектура проекта: конечный автомат</text>' +
    # States
    box(20,70,120,50,'#dbeafe','#3b82f6','SCREEN_TEMP\nТемпература',11,'bold') +
    box(250,70,120,50,'#dcfce7','#16a34a','SCREEN_PRES\nДавление',11,'bold') +
    box(480,70,120,50,'#fef9c3','#f59e0b','SCREEN_HUM\nВлажность',11,'bold') +
    # Transitions
    arrow(140,95,250,95,'#3b82f6') +
    arrow(370,95,480,95,'#16a34a') +
    arrow(480,120,140,120,'#f59e0b') +
    '<text x="195" y="88" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">BTN1</text>' +
    '<text x="425" y="88" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">BTN1</text>' +
    '<text x="310" y="138" text-anchor="middle" font-size="10" fill="#f59e0b" font-family="sans-serif">wrap around</text>' +
    # Tasks
    '<rect x="20" y="160" width="580" height="90" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="310" y="180" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">Неблокирующие задачи (millis-based)</text>' +
    '<text x="40" y="200" font-size="10" fill="#64748b" font-family="sans-serif">каждые 2000 мс: читать BMP280 + DHT22</text>' +
    '<text x="40" y="218" font-size="10" fill="#64748b" font-family="sans-serif">каждые 1000 мс: обновить OLED</text>' +
    '<text x="40" y="236" font-size="10" fill="#64748b" font-family="sans-serif">каждые 5000 мс: отправить данные по BT</text>' +
    '<text x="310" y="200" font-size="10" fill="#64748b" font-family="sans-serif">по PCINT: переключить экран</text>' +
    '<text x="310" y="218" font-size="10" fill="#64748b" font-family="sans-serif">каждые 500 мс: heartbeat LED</text>',
    640, 270, 'Конечный автомат экранов + неблокирующие таймеры'
) + tip('Архитектура «кооперативный scheduler»: каждая задача проверяет свой таймер в loop() и выполняется если пришло время. Простая альтернатива RTOS для МК.') +
warn('DHT22 требует строгих временны́х задержек при чтении. Нельзя разрешать прерывания во время чтения — используйте cli()/sei() или библиотеку DHT.'),
'code_example': '''#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BMP280.h>
#include <SoftwareSerial.h>
#include <DHT.h>

Adafruit_SSD1306 oled(128, 64, &Wire);
Adafruit_BMP280  bmp;
DHT              dht(7, DHT22);
SoftwareSerial   bt(8, 9);

enum Screen { SCREEN_TEMP, SCREEN_PRES, SCREEN_HUM };
volatile Screen screen = SCREEN_TEMP;

float temp_bmp, pres, temp_dht, hum;
uint32_t t_sensor=0, t_oled=0, t_bt=0, t_heart=0;
bool heart=false;

void setup() {
    Serial.begin(115200);
    bt.begin(9600);
    Wire.begin();
    oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    bmp.begin(0x76);
    dht.begin();
    pinMode(LED_BUILTIN, OUTPUT);
    // PCINT для кнопок на PC0, PC1
    PCICR  |= (1<<PCIE1);
    PCMSK1 |= (1<<PCINT8)|(1<<PCINT9);
    sei();
}

ISR(PCINT1_vect) {
    static uint8_t prev = 0xFF;
    uint8_t curr = PINC;
    if ((prev & 1) && !(curr & 1))  // PC0 спад
        screen = (Screen)((screen + 1) % 3);
    prev = curr;
}

void loop() {
    uint32_t now = millis();

    // Чтение датчиков каждые 2 сек
    if (now - t_sensor >= 2000) {
        t_sensor = now;
        temp_bmp = bmp.readTemperature();
        pres     = bmp.readPressure() / 100.0f;
        hum      = dht.readHumidity();
        temp_dht = dht.readTemperature();
    }

    // Обновление OLED каждую секунду
    if (now - t_oled >= 1000) {
        t_oled = now;
        oled.clearDisplay();
        oled.setTextColor(WHITE);
        oled.setTextSize(2);
        oled.setCursor(0,0);
        switch(screen) {
            case SCREEN_TEMP:
                oled.println("Temp:");
                oled.print(temp_bmp,1); oled.println(" C");
                break;
            case SCREEN_PRES:
                oled.println("Pres:");
                oled.print(pres,1); oled.println("hPa");
                break;
            case SCREEN_HUM:
                oled.println("Hum:");
                oled.print(hum,1); oled.println(" %");
                break;
        }
        oled.display();
    }

    // Отправка по BT каждые 5 сек
    if (now - t_bt >= 5000) {
        t_bt = now;
        bt.print("{\"t\":"); bt.print(temp_bmp,1);
        bt.print(",\"p\":"); bt.print(pres,1);
        bt.print(",\"h\":"); bt.print(hum,1);
        bt.println("}");
    }

    // Heartbeat
    if (now - t_heart >= 500) {
        t_heart = now;
        heart = !heart;
        digitalWrite(LED_BUILTIN, heart);
    }
}'''
},
],

}  # конец LESSONS


class Command(BaseCommand):
    help = 'Заполняет расширенный контент МПС модули 6–10'

    def handle(self, *args, **options):
        try:
            subj = Subject.objects.get(slug='mcu')
        except Subject.DoesNotExist:
            self.stderr.write('Subject mcu не найден. Запустите seed_mps сначала.')
            return

        total = 0
        for mod_order, lessons in LESSONS.items():
            module = TheoryModule.objects.filter(subject=subj, order=mod_order).first()
            if not module:
                self.stderr.write(f'Модуль {mod_order} не найден, пропускаем')
                continue
            for ld in lessons:
                obj, created = TheoryLesson.objects.update_or_create(
                    module=module,
                    order=ld['order'],
                    defaults={
                        'title': ld['title'],
                        'content': ld['content'],
                        'code_example': ld.get('code_example', ''),
                        'estimated_minutes': ld['estimated_minutes'],
                    }
                )
                status = 'создан' if created else 'обновлён'
                self.stdout.write(f'  M{mod_order} L{ld["order"]}: {ld["title"][:40]} [{status}]')
                total += 1

        self.stdout.write(self.style.SUCCESS(f'\nГотово: обработано {total} уроков (модули 6–10)'))
