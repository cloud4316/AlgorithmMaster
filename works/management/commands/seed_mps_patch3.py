# -*- coding: utf-8 -*-
"""Patch 3 — expand last 4 thin lessons to 5000+ chars."""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson

def box(x, y, w, h, fill, stroke, text, fs=13, fw='normal', tc='#1e293b'):
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    lines = text.split('\n')
    lh = fs + 3
    y0 = y + h // 2 - (lh * len(lines)) // 2 + fs
    spans = ''.join(f'<tspan x="{x+w//2}" dy="{0 if i==0 else lh}">{l}</tspan>' for i, l in enumerate(lines))
    txt = (f'<text x="{x+w//2}" y="{y0}" text-anchor="middle" font-size="{fs}" '
           f'fill="{tc}" font-weight="{fw}" font-family="sans-serif">{spans}</text>')
    return rect + txt

DEFS = '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'

def arr(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#64748b" stroke-width="1.5" marker-end="url(#arr)"/>'

def diagram(svg, w=640, h=280, caption=''):
    return (f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
            f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;'
            f'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">'
            f'{svg}</svg>'
            f'<p style="text-align:center;color:#64748b;font-size:13px">{caption}</p></div>')

def tip(text):
    return f'<div class="tip">{text}</div>'

def warn(text):
    return f'<div class="warning">{text}</div>'

def info(text):
    return f'<div class="info">{text}</div>'

def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''
    for r in rows:
        trs += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def code(lang, src):
    return f'<pre><code class="language-{lang}">{src}</code></pre>'


# ── M6L3: АЦП прерывания и Free Running ──────────────────────────────────────
M6L3_EXTRA = '''
<h2>Регистры АЦП: детали</h2>
''' + table(
    ['Регистр', 'Биты', 'Назначение'],
    [
        ('ADMUX', 'REFS1:0', 'Выбор опорного напряжения: 00=AREF, 01=AVCC, 11=Int 1.1V'),
        ('ADMUX', 'MUX3:0', 'Выбор канала: 0000=A0 ... 0111=A7'),
        ('ADCSRA', 'ADEN', 'Включить АЦП'),
        ('ADCSRA', 'ADSC', 'Запустить одиночное преобразование'),
        ('ADCSRA', 'ADATE', 'Auto Trigger Enable (для Free Running)'),
        ('ADCSRA', 'ADIF', 'Флаг завершения (сбрасывается записью 1)'),
        ('ADCSRA', 'ADIE', 'Разрешить прерывание АЦП'),
        ('ADCSRA', 'ADPS2:0', 'Предделитель: 111 = /128 (125 kHz при F=16 MHz)'),
        ('ADCSRB', 'ADTS2:0', 'Источник Auto Trigger: 000 = Free Running'),
        ('ADCH/ADCL', '—', '10-битный результат (ADLAR=0: ADCL[7:0] + ADCH[1:0])'),
    ]
) + '''
<h3>Диаграмма: Free Running vs одиночное преобразование</h3>
''' + diagram(
    DEFS +
    '<rect width="640" height="220" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'
    '<text x="320" y="24" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">АЦП: режимы запуска</text>'
    + box(20, 40, 280, 60, '#dbeafe', '#3b82f6', 'Single Conversion\n(ADSC=1 вручную)', 11, 'normal', '#1e40af')
    + box(340, 40, 280, 60, '#dcfce7', '#16a34a', 'Free Running\n(ADATE=1, ADTS=000)', 11, 'normal', '#14532d')
    + '<text x="160" y="125" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Запуск: ADCSRA |= (1&lt;&lt;ADSC);</text>'
    '<text x="160" y="140" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Ожидание: while(ADCSRA &amp; (1&lt;&lt;ADSC));</text>'
    '<text x="160" y="155" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Чтение: val = ADC;</text>'
    '<text x="480" y="125" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Запуск: ADCSRA |= (1&lt;&lt;ADSC);</text>'
    '<text x="480" y="140" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Новое значение в ISR(ADC_vect)</text>'
    '<text x="480" y="155" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">Не блокирует loop()!</text>'
    + box(20, 170, 280, 40, '#fee2e2', '#ef4444', 'Минус: блокирует CPU ~104 мкс', 10, 'normal', '#7f1d1d')
    + box(340, 170, 280, 40, '#dcfce7', '#16a34a', 'Плюс: данные всегда свежие', 10, 'normal', '#14532d'),
    640, 220, 'Сравнение режимов запуска АЦП'
) + '''
<h3>ISR-шаблон для Free Running</h3>
''' + code('cpp', '''#include <avr/io.h>
#include <avr/interrupt.h>

volatile uint16_t adc_val = 0;

void adc_init_free_run() {
    ADMUX  = (1<<REFS0);           // AVCC как опора, канал A0
    ADCSRA = (1<<ADEN)|(1<<ADIE)  // включить + прерывание
           |(1<<ADATE)            // Auto Trigger
           |(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0); // делитель /128
    ADCSRB = 0;                   // Free Running
    ADCSRA |= (1<<ADSC);          // первый запуск
    sei();
}

ISR(ADC_vect) {
    adc_val = ADC;   // аппаратно перезапускается автоматически
}

int main(void) {
    adc_init_free_run();
    while(1) {
        uint16_t v = adc_val; // читаем атомарно (16-бит на AVR!)
        // использовать v ...
    }
}''') + tip('&#128161; Для атомарного чтения 16-битного <code>adc_val</code> на AVR отключите прерывания: <code>ATOMIC_BLOCK(ATOMIC_RESTORESTATE){ v = adc_val; }</code>') + warn('&#9888;&#65039; При смене канала в Free Running нужно сделать одно "холостое" преобразование после изменения MUX — первый результат после смены канала может быть некорректным.')


# ── M9L2: Подпрограммы в ASM ──────────────────────────────────────────────────
M9L2_EXTRA = '''
<h2>Передача параметров и ABI</h2>
<p>AVR-GCC использует соглашение о вызовах (ABI): первые параметры передаются в регистрах r24–r25 (16-бит), r22–r23, r20–r21... Возвращаемое значение — в r24:r25 (16-бит) или r24 (8-бит).</p>
''' + table(
    ['Регистры', 'Роль', 'Сохранять?'],
    [
        ('r0', 'Временный (используется mul/lpm)', 'Нет'),
        ('r1', 'Всегда ноль (zero reg)', 'Да (восстановить в 0)'),
        ('r2–r17', 'Call-saved (callee сохраняет)', 'Да'),
        ('r18–r27', 'Call-clobbered (caller сохраняет)', 'Нет'),
        ('r28:r29', 'Y-pointer (frame pointer)', 'Да'),
        ('r30:r31', 'Z-pointer (свободно)', 'Нет'),
        ('r24:r25', '1-й аргумент / возврат 16-бит', 'Нет'),
    ]
) + '''
<h3>Диаграмма стека при вызове подпрограммы</h3>
''' + diagram(
    DEFS +
    '<rect width="640" height="240" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'
    '<text x="320" y="24" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Стек AVR при CALL/RET</text>'
    + box(240, 40, 160, 36, '#dbeafe', '#3b82f6', 'SP перед CALL', 11, 'normal', '#1e40af')
    + arr(320, 76, 320, 100)
    + box(240, 100, 160, 36, '#fef3c7', '#f59e0b', 'SP после CALL\n(−2: адрес возврата)', 11, 'normal', '#92400e')
    + arr(320, 136, 320, 160)
    + box(240, 160, 160, 36, '#fee2e2', '#ef4444', 'SP после PUSH rX\n(−1 за каждый PUSH)', 11, 'normal', '#7f1d1d')
    + arr(320, 196, 320, 220)
    + box(240, 220, 160, 32, '#dcfce7', '#16a34a', 'RET: SP += 2', 11, 'normal', '#14532d')
    + '<text x="80" y="65" font-size="10" fill="#64748b" font-family="sans-serif">Высокий адрес</text>'
    + '<text x="80" y="235" font-size="10" fill="#64748b" font-family="sans-serif">Низкий адрес</text>'
    + '<line x1="170" y1="40" x2="170" y2="250" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4"/>',
    640, 260, 'Движение SP при вызове подпрограммы и возврате'
) + '''
<h3>Пример: подпрограмма умножения 8x8 → 16</h3>
''' + code('nasm', '''; mul8: r24 * r22 -> r25:r24
; Входные: r24 = a, r22 = b
; Выходные: r25:r24 = результат
mul8:
    mul  r24, r22       ; r1:r0 = r24 * r22
    movw r24, r0        ; r25:r24 = r1:r0
    clr  r1             ; обязательно восстановить r1=0
    ret

; Вызов из C: uint16_t result = mul8(5, 7);
; Компилятор поместит 5 в r24, 7 в r22''') + tip('&#128161; Используйте директиву <code>.global имя</code> чтобы функция на asm была видна из C-файлов. Пример: <code>.global mul8</code> перед меткой.') + '''
<h3>Макросы в AVR Assembler</h3>
''' + code('nasm', '''; Макрос для задержки N тактов (N <= 255)
.macro DELAY_TICKS cycles
    ldi  r18, \\cycles
1:  dec  r18
    brne 1b
.endmacro

; Использование:
    DELAY_TICKS 100    ; ~100 тактов = 6.25 мкс при 16 MHz''') + info('&#128712; Макросы в AVR ASM не создают вызов подпрограммы — код вставляется inline. Это полезно для мелких часто-используемых паттернов без оверхеда CALL/RET.')


# ── M11L1: LCD HD44780 ────────────────────────────────────────────────────────
M11L1_EXTRA = '''
<h2>Шина данных: 4-битный режим</h2>
<p>HD44780 поддерживает 8-битный (DB0–DB7) и 4-битный (DB4–DB7) интерфейс. 4-битный экономит 4 пина микроконтроллера — каждый байт передаётся двумя нибблами (старший первым).</p>
''' + diagram(
    DEFS +
    '<rect width="640" height="220" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'
    '<text x="320" y="24" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Передача байта в 4-битном режиме HD44780</text>'
    + box(20, 50, 140, 40, '#dbeafe', '#3b82f6', 'RS=1 (данные)\nили RS=0 (команда)', 10, 'normal', '#1e40af')
    + arr(160, 70, 200, 70)
    + box(200, 50, 130, 40, '#fef3c7', '#f59e0b', 'DB7:4 = старший\nниббл (биты 7-4)', 10, 'normal', '#92400e')
    + arr(330, 70, 370, 70)
    + box(370, 50, 100, 40, '#dcfce7', '#16a34a', 'EN: 1->0\n(строб)', 10, 'normal', '#14532d')
    + arr(470, 70, 510, 70)
    + box(510, 50, 110, 40, '#fef3c7', '#f59e0b', 'DB7:4 = младший\nниббл (биты 3-0)', 10, 'normal', '#92400e')
    + box(200, 130, 130, 40, '#fee2e2', '#ef4444', 'Задержка\n>37 мкс', 10, 'normal', '#7f1d1d')
    + box(370, 130, 100, 40, '#dcfce7', '#16a34a', 'EN: 1->0\n(строб)', 10, 'normal', '#14532d')
    + '<text x="320" y="195" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Итого 2 строба EN на каждый байт. Пауза 37+ мкс между командами.</text>',
    640, 210, '4-битный режим: каждый байт = 2 нибля + 2 строба EN'
) + table(
    ['Команда', 'RS', 'D7:D4', 'D3:D0', 'Время'],
    [
        ('Очистить дисплей', '0', '0000', '0001', '1.52 мс'),
        ('Домой (курсор в 0,0)', '0', '0000', '0010', '1.52 мс'),
        ('Установить режим', '0', '0000', '01xx', '37 мкс'),
        ('Вкл/выкл дисплея', '0', '0000', '1xxx', '37 мкс'),
        ('Смещение курсора/экрана', '0', '0001', 'xxxx', '37 мкс'),
        ('Установить DDRAM адрес', '0', '1xxx', 'xxxx', '37 мкс'),
        ('Записать данные', '1', 'D7:D4', 'D3:D0', '37 мкс'),
    ]
) + '''
<h3>DDRAM: адресация позиций символов</h3>
''' + code('cpp', '''// Адреса начала строк для 16x2 LCD
// Строка 0: адреса 0x00 – 0x0F
// Строка 1: адреса 0x40 – 0x4F
// Для 20x4: строки 0/1/2/3 -> 0x00/0x40/0x14/0x54

#include <LiquidCrystal.h>
// RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
    lcd.begin(16, 2);
    lcd.setCursor(0, 0);
    lcd.print("Hello, World!");
    lcd.setCursor(0, 1);
    lcd.print("ATmega328P");
}

// Пользовательский символ (CGR)
byte heart[8] = {0b00000,0b01010,0b11111,0b11111,
                 0b01110,0b00100,0b00000,0b00000};
void createCustomChar() {
    lcd.createChar(0, heart);  // слот 0 из 8
    lcd.write(byte(0));        // вывести
}''') + tip('&#128161; Адрес строки 1 начинается с 0x40, а не 0x10. Это особенность HD44780 — строки в DDRAM не расположены последовательно. Библиотека LiquidCrystal учитывает это автоматически.')


# ── M13L3: Снижение потребления в практических схемах ────────────────────────
M13L3_EXTRA = '''
<h2>Практические цифры потребления ATmega328P</h2>
''' + table(
    ['Режим', 'Типичный ток', 'Что работает'],
    [
        ('Active @ 16 MHz, 5V', '~12 мА', 'Всё'),
        ('Active @ 8 MHz, 3.3V', '~4 мА', 'Всё (меньше скорость)'),
        ('Idle @ 8 MHz', '~1 мА', 'Периферия, прерывания'),
        ('Power-save (Timer2 async)', '~0.9 мкА + Timer2', 'RTC на 32 кГц кварце'),
        ('Power-down', '~0.1 мкА', 'Только WDT или INT0/INT1'),
        ('ADC Noise Reduction', 'Idle − шум ЦАП', 'АЦП + прерывания'),
    ]
) + '''
<h3>Схема: пробуждение по внешнему прерыванию</h3>
''' + diagram(
    DEFS +
    '<rect width="640" height="230" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'
    '<text x="320" y="24" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Power-Down: пробуждение по INT0 (PD2)</text>'
    + box(20, 50, 160, 50, '#dbeafe', '#3b82f6', 'loop()\nработа 100 мс', 11, 'normal', '#1e40af')
    + arr(180, 75, 230, 75)
    + box(230, 50, 160, 50, '#fef3c7', '#f59e0b', 'sleep_enable()\nsleep_cpu()\n→ Power-Down', 10, 'normal', '#92400e')
    + arr(390, 75, 440, 75)
    + box(440, 50, 180, 50, '#fee2e2', '#ef4444', 'Ждем...\n~0.1 мкА', 11, 'normal', '#7f1d1d')
    + box(440, 140, 180, 50, '#dcfce7', '#16a34a', 'INT0 срабатывает\n(кнопка/PIR)', 11, 'normal', '#14532d')
    + arr(530, 140, 530, 100)
    + arr(440, 165, 390, 165)
    + box(230, 140, 160, 50, '#dcfce7', '#16a34a', 'ISR: sleep_disable()\nустановить флаг', 10, 'normal', '#14532d')
    + arr(230, 165, 180, 165)
    + arr(110, 140, 110, 100),
    640, 210, 'Power-Down с пробуждением по INT0: пин PD2'
) + code('cpp', '''#include <avr/sleep.h>
#include <avr/interrupt.h>

volatile bool wakeup = false;

ISR(INT0_vect) {
    wakeup = true;
    sleep_disable();           // запрет повторного сна в ISR
}

void setup() {
    Serial.begin(9600);
    pinMode(2, INPUT_PULLUP);  // INT0 = PD2

    // Настройка INT0 на FALLING edge
    EICRA = (1<<ISC01);        // falling edge
    EIMSK = (1<<INT0);         // разрешить INT0
    sei();
}

void loop() {
    if (wakeup) {
        wakeup = false;
        Serial.println("Woke up!");
        delay(100);
        Serial.flush();        // дать UART завершить передачу
    }

    // Уходим спать
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    sleep_enable();
    sleep_cpu();               // CPU останавливается здесь
    // Выполнение продолжается здесь после пробуждения
}''') + tip('&#128161; Перед вызовом <code>sleep_cpu()</code> вызовите <code>Serial.flush()</code> — иначе UART может оборвать текущую передачу в момент остановки тактирования.') + '''
<h3>Рекомендации по снижению потребления</h3>
''' + table(
    ['Приём', 'Экономия', 'Метод'],
    [
        ('Понизить частоту', 'до 8x', 'Prescaler CLK/8 или 3.3V @ 8MHz'),
        ('Отключить АЦП', '~0.3 мА', 'ADCSRA &= ~(1<<ADEN)'),
        ('Отключить UART', '~0.5 мА', 'Отключить TX-пин и UCSR0B'),
        ('Отключить Brown-out', '~0.2 мА', 'Программировать fuses (осторожно!)'),
        ('Power-Down режим', '99%+', 'set_sleep_mode(SLEEP_MODE_PWR_DOWN)'),
        ('Внешние компоненты', 'varies', 'Подтяжки, светодиоды через MOSFET'),
    ]
)


PATCHES = {
    (6, 3): M6L3_EXTRA,
    (9, 2): M9L2_EXTRA,
    (11, 1): M11L1_EXTRA,
    (13, 3): M13L3_EXTRA,
}


class Command(BaseCommand):
    help = 'Patch 3 — expand 4 remaining thin lessons'

    def handle(self, *args, **kwargs):
        mcu_mods = TheoryModule.objects.filter(subject__slug='mcu').order_by('order')
        mod_by_order = {m.order: m for m in mcu_mods}

        for (mo, lo), extra in PATCHES.items():
            mod = mod_by_order.get(mo)
            if not mod:
                self.stdout.write(f'Module M{mo} not found')
                continue
            try:
                lesson = TheoryLesson.objects.get(module=mod, order=lo)
            except TheoryLesson.DoesNotExist:
                self.stdout.write(f'Lesson M{mo}L{lo} not found')
                continue
            old_len = len(lesson.content)
            lesson.content += extra
            lesson.estimated_minutes = max(lesson.estimated_minutes or 0, 45)
            lesson.save()
            new_len = len(lesson.content)
            self.stdout.write(
                f'M{mo}L{lo}: {old_len} -> {new_len} ch (+{new_len-old_len}) [{lesson.title[:40]}]'
            )

        self.stdout.write('Done: expanded 4 thin lessons')
