"""python manage.py seed_mps_full — расширенный контент для МПС"""
from django.core.management.base import BaseCommand
from works.models import TheoryModule, TheoryLesson, Subject


def tip(t): return f'<div class="tip">💡 {t}</div>'
def warn(t): return f'<div class="warning">⚠️ {t}</div>'
def info(t): return f'<div class="tip" style="background:#e0f2fe;border-color:#0284c7">ℹ️ {t}</div>'

def table(headers, rows):
    th = ''.join(f'<th>{c}</th>' for c in headers)
    trs = ''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)
    return f'<table class="theory-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def diagram(svg, w=640, h=320, caption=''):
    return (
        f'<div style="overflow-x:auto;margin:1.5rem 0;text-align:center">'
        f'<svg viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;'
        f'border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">'
        f'{svg}</svg>'
        f'<p style="text-align:center;color:#64748b;font-size:13px">{caption}</p></div>'
    )


# ─── SVG helpers ───────────────────────────────────────────────────────────────
def box(x, y, w, h, fill, stroke, text, fs=13, fw='normal', tc='#1e293b'):
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


# ══════════════════════════════════════════════════════════════════════════════
# ДАННЫЕ УРОКОВ
# ══════════════════════════════════════════════════════════════════════════════

LESSONS = {

# ─── МОДУЛЬ 1 ─────────────────────────────────────────────────────────────────
1: [
{
'title': 'Что такое микропроцессор и микроконтроллер',
'order': 1, 'estimated_minutes': 50,
'content': '''
<h2>Микропроцессор vs Микроконтроллер</h2>
<p><strong>Микропроцессор (МП)</strong> — интегральная схема, реализующая только вычислительное ядро (АЛУ, регистры, УУ). Для работы требует внешних компонентов: ОЗУ, ПЗУ, периферийных контроллеров, шинных формирователей.</p>
<p><strong>Микроконтроллер (МК)</strong> — однокристальная ЭВМ: ядро + Flash-память программ + SRAM + EEPROM + порты GPIO + таймеры + АЦП + UART/SPI/I2C — всё в одном корпусе.</p>
''' + diagram(
    DEFS +
    # МП box
    box(30,40,260,200,'#fef9c3','#f59e0b','Микропроцессор (МП)',14,'bold','#92400e') +
    box(60,80,80,35,'#fef3c7','#f59e0b','АЛУ',12) +
    box(155,80,80,35,'#fef3c7','#f59e0b','Регистры',12) +
    box(60,130,80,35,'#fef3c7','#f59e0b','УУ',12) +
    box(155,130,80,35,'#fef3c7','#f59e0b','Кэш',12) +
    '<text x="160" y="210" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">+ внешние RAM, ROM, порты…</text>' +
    # МК box
    box(350,40,260,200,'#dcfce7','#16a34a','Микроконтроллер (МК)',14,'bold','#14532d') +
    box(360,80,70,30,'#bbf7d0','#16a34a','Ядро',11) +
    box(440,80,70,30,'#bbf7d0','#16a34a','Flash',11) +
    box(520,80,70,30,'#bbf7d0','#16a34a','SRAM',11) +
    box(360,120,70,30,'#bbf7d0','#16a34a','GPIO',11) +
    box(440,120,70,30,'#bbf7d0','#16a34a','Таймер',11) +
    box(520,120,70,30,'#bbf7d0','#16a34a','АЦП',11) +
    box(360,160,70,30,'#bbf7d0','#16a34a','UART',11) +
    box(440,160,70,30,'#bbf7d0','#16a34a','SPI',11) +
    box(520,160,70,30,'#bbf7d0','#16a34a','I2C',11) +
    '<text x="480" y="215" text-anchor="middle" font-size="11" fill="#14532d" font-family="sans-serif">Всё в одном корпусе!</text>',
    640, 260, 'МП требует обвязки; МК самодостаточен'
) +
table(
    ['Характеристика','Микропроцессор','Микроконтроллер'],
    [
        ['Периферия','Внешняя','Встроенная'],
        ['Стоимость системы','Высокая','Низкая'],
        ['Потребление','Высокое','Низкое (мА)'],
        ['Применение','ПК, серверы','Встраиваемые устройства'],
        ['Примеры','Intel Core, AMD','ATmega328P, STM32'],
    ]
) +
tip('ATmega328P (сердце Arduino Uno) содержит: 32 КБ Flash, 2 КБ SRAM, 1 КБ EEPROM, 23 GPIO, 6-канальный АЦП, 3 таймера.') +
warn('Не путайте: МП ≠ МК. На уроках МПС мы изучаем именно <em>микроконтроллеры</em> AVR/Arduino.'),
'code_example': '''// Первая программа на AVR C
#include <avr/io.h>
#include <util/delay.h>

int main(void) {
    DDRB |= (1 << PB5);   // PB5 = выход (LED на Arduino = pin 13)
    while (1) {
        PORTB |= (1 << PB5);   // LED ON
        _delay_ms(500);
        PORTB &= ~(1 << PB5);  // LED OFF
        _delay_ms(500);
    }
}'''
},

{
'title': 'Архитектура фон Неймана и Гарвардская',
'order': 2, 'estimated_minutes': 45,
'content': '''
<h2>Две фундаментальные архитектуры</h2>
<p>Способ организации памяти определяет всю конструкцию МПС. Существуют две классических схемы.</p>
<h3>Архитектура фон Неймана</h3>
<p>Программа и данные хранятся в <strong>одной памяти</strong>, доступ через <strong>одну шину</strong>. Процессор не может одновременно читать команду и данные — <em>«бутылочное горлышко»</em>.</p>
''' + diagram(
    DEFS +
    box(240,20,160,40,'#dbeafe','#3b82f6','Процессор',13,'bold') +
    arrow(320,60,320,90) +
    box(180,90,280,50,'#e0e7ff','#6366f1','Общая память (код + данные)',13) +
    '<text x="320" y="170" text-anchor="middle" font-size="12" fill="#64748b" font-family="sans-serif">Одна шина — конфликт при одновременном доступе</text>',
    640, 190, 'Архитектура фон Неймана'
) +
'''<h3>Гарвардская архитектура</h3>
<p>Память программ и память данных <strong>физически разделены</strong>, у каждой своя шина. Процессор может одновременно читать следующую команду и обращаться к данным.</p>''' +
diagram(
    DEFS +
    box(240,20,160,40,'#dcfce7','#16a34a','Процессор',13,'bold') +
    arrow(260,60,180,90) +
    arrow(380,60,460,90) +
    box(80,90,200,45,'#bbf7d0','#16a34a','Flash (программа)',12) +
    box(360,90,200,45,'#fef9c3','#f59e0b','SRAM (данные)',12) +
    '<text x="180" y="160" text-anchor="middle" font-size="11" fill="#15803d" font-family="sans-serif">Шина команд</text>' +
    '<text x="460" y="160" text-anchor="middle" font-size="11" fill="#b45309" font-family="sans-serif">Шина данных</text>',
    640, 180, 'Гарвардская архитектура — две независимые шины'
) +
table(
    ['','фон Нейман','Гарвард'],
    [
        ['Шин памяти','1','2'],
        ['Параллельное чтение команды+данных','Нет','Да'],
        ['Производительность','Ниже','Выше'],
        ['Применение','x86, ARM Cortex-A','AVR, PIC, DSP'],
    ]
) +
info('AVR использует <em>модифицированную</em> Гарвардскую архитектуру: Flash для программ, SRAM для данных, но возможно чтение Flash через LPM.') +
tip('На экзамене: «Почему МК быстрее при той же частоте?» — потому что Гарвард позволяет fetch + execute параллельно.'),
'code_example': '''// Чтение константы из Flash (Program Memory) на AVR
#include <avr/pgmspace.h>

// Строка хранится во Flash, не в SRAM
const char msg[] PROGMEM = "Hello AVR!";

char buf[16];
// Копировать из Flash в SRAM
strcpy_P(buf, msg);'''
},

{
'title': 'Структура МПС: шины, память, периферия',
'order': 3, 'estimated_minutes': 50,
'content': '''
<h2>Три кита МПС: шины, память, периферия</h2>
<p>Любая МПС строится из трёх функциональных блоков, соединённых <strong>системными шинами</strong>.</p>
<h3>Системные шины</h3>
''' +
table(
    ['Шина','Разрядность','Назначение'],
    [
        ['Адресная (AB)','8–32 бит','Задаёт адрес ячейки памяти/регистра'],
        ['Данных (DB)','8/16/32 бит','Передаёт данные между блоками'],
        ['Управления (CB)','Несколько линий','RD, WR, CLK, RESET, INT…'],
    ]
) +
diagram(
    DEFS +
    # CPU
    box(20,110,100,60,'#dbeafe','#3b82f6','CPU\n(ядро)',13,'bold') +
    # Memory
    box(230,30,120,60,'#dcfce7','#16a34a','Flash\n(программа)',12) +
    box(230,110,120,60,'#fef9c3','#f59e0b','SRAM\n(данные)',12) +
    box(230,190,120,60,'#fce7f3','#db2777','EEPROM\n(настройки)',12) +
    # Peripheral
    box(460,30,140,45,'#f0fdf4','#22c55e','GPIO (порты)',12) +
    box(460,90,140,45,'#eff6ff','#3b82f6','Таймеры/ШИМ',12) +
    box(460,150,140,45,'#fff7ed','#f97316','UART/SPI/I2C',12) +
    box(460,210,140,45,'#fdf4ff','#a855f7','АЦП/ЦАП',12) +
    # Buses
    '<rect x="130" y="130" width="100" height="8" rx="3" fill="#3b82f6" opacity="0.6"/>' +
    '<rect x="130" y="148" width="100" height="5" rx="2" fill="#f59e0b" opacity="0.6"/>' +
    '<rect x="130" y="162" width="100" height="4" rx="2" fill="#64748b" opacity="0.6"/>' +
    '<text x="180" y="128" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">AB</text>' +
    '<text x="180" y="155" text-anchor="middle" font-size="10" fill="#b45309" font-family="sans-serif">DB</text>' +
    '<rect x="360" y="20" width="5" height="240" fill="#94a3b8" opacity="0.5"/>' +
    arrow(350,55,360,55) + arrow(350,135,360,135) + arrow(350,215,360,215) +
    arrow(365,50,460,50) + arrow(365,112,460,112) + arrow(365,172,460,172) + arrow(365,232,460,232),
    640, 280, 'Структура микроконтроллерной системы'
) +
'''<h3>Карта памяти ATmega328P</h3>''' +
table(
    ['Область','Размер','Адреса','Назначение'],
    [
        ['Flash','32 КБ','0x0000–0x7FFF','Программа (код)'],
        ['SRAM','2 КБ','0x0100–0x08FF','Переменные, стек'],
        ['EEPROM','1 КБ','0x000–0x3FF','Энергонезависимые данные'],
        ['Регистры I/O','64','0x20–0x5F','Управление периферией'],
        ['Ext. I/O','160','0x60–0xFF','Расширенные регистры'],
    ]
) +
tip('Стек AVR растёт вниз от конца SRAM (0x08FF). SP (Stack Pointer) по умолчанию = RAMEND.') +
warn('SRAM всего 2 КБ! При объявлении больших массивов легко получить переполнение стека.'),
'code_example': '''// Работа с EEPROM на ATmega328P
#include <avr/eeprom.h>

uint8_t EEMEM saved_value = 0;  // переменная в EEPROM

int main(void) {
    // Читаем из EEPROM
    uint8_t val = eeprom_read_byte(&saved_value);

    // Изменяем и записываем
    val++;
    eeprom_write_byte(&saved_value, val);
    // Теперь val сохранится при отключении питания
}'''
},

{
'title': 'Жизненный цикл программы МК',
'order': 4, 'estimated_minutes': 40,
'content': '''
<h2>Путь программы: от исходника до МК</h2>
<p>Прежде чем код начнёт работать в МК, он проходит несколько этапов преобразования.</p>
''' + diagram(
    DEFS +
    box(20,130,110,40,'#dbeafe','#3b82f6','Исходный\nкод (.c)',12) +
    arrow(130,150,175,150) +
    box(175,130,110,40,'#dcfce7','#16a34a','Компилятор\n(avr-gcc)',12) +
    arrow(285,150,330,150) +
    box(330,130,110,40,'#fef9c3','#f59e0b','Объектный\nфайл (.o)',12) +
    arrow(440,150,485,150) +
    box(485,130,110,40,'#fce7f3','#db2777','Линковщик\n(avr-ld)',12) +
    arrow(320,170,320,200) +
    box(255,200,130,40,'#f0fdf4','#22c55e','ELF / HEX\n(.hex)',12) +
    arrow(320,240,320,270) +
    box(235,270,170,40,'#eff6ff','#6366f1','avrdude →\nFlash МК',12),
    640, 330, 'Toolchain: исходник → прошивка МК'
) +
'''<h3>Этапы подробно</h3>
<ol>
<li><strong>Написание кода</strong> — .c / .cpp / .asm файлы</li>
<li><strong>Препроцессор</strong> — раскрывает #include, #define, условную компиляцию</li>
<li><strong>Компиляция</strong> — avr-gcc транслирует C → машинный код AVR (.o)</li>
<li><strong>Компоновка</strong> — avr-ld собирает все .o + библиотеки → .elf</li>
<li><strong>Конвертация</strong> — avr-objcopy .elf → .hex (Intel HEX формат)</li>
<li><strong>Прошивка</strong> — avrdude загружает .hex через ISP/UART/USB в Flash МК</li>
</ol>''' +
table(
    ['Инструмент','Функция'],
    [
        ['avr-gcc','Компилятор C/C++ для архитектуры AVR'],
        ['avr-as','Ассемблер AVR'],
        ['avr-ld','Компоновщик'],
        ['avr-objcopy','Конвертер форматов (ELF→HEX)'],
        ['avrdude','Загрузка прошивки в МК'],
        ['avr-size','Показывает размер Flash/SRAM занятой кодом'],
    ]
) +
info('Arduino IDE автоматически запускает весь toolchain. Кнопка «Загрузить» = компиляция + avrdude.') +
tip('Команда <code>avr-size --format=avr firmware.elf</code> показывает, сколько Flash и SRAM занимает программа.'),
'code_example': '''# Компиляция вручную (Makefile-стиль)
# 1. Компилируем
avr-gcc -mmcu=atmega328p -DF_CPU=16000000UL -Os -o main.o -c main.c

# 2. Компонуем
avr-gcc -mmcu=atmega328p -o firmware.elf main.o

# 3. Создаём HEX
avr-objcopy -O ihex firmware.elf firmware.hex

# 4. Прошиваем через Arduino как ISP
avrdude -c arduino -p atmega328p -P /dev/ttyACM0 -b 115200 -U flash:w:firmware.hex

# Проверка размера
avr-size --format=avr firmware.elf'''
},
],

# ─── МОДУЛЬ 2 ─────────────────────────────────────────────────────────────────
2: [
{
'title': 'Регистры и система команд AVR',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>Регистровый файл AVR</h2>
<p>Ядро AVR содержит <strong>32 восьмибитных регистра общего назначения</strong> R0–R31. Они являются основным рабочим пространством: все арифметические и логические операции выполняются именно над ними.</p>
''' + diagram(
    DEFS +
    '<rect x="20" y="20" width="600" height="270" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>' +
    '<text x="320" y="45" text-anchor="middle" font-size="14" fill="#1e293b" font-weight="bold" font-family="sans-serif">Регистровый файл AVR — 32 × 8 бит</text>' +
    # R0-R15
    ''.join(box(30+i*38,60,35,30,'#dbeafe','#3b82f6',f'R{i}',10) for i in range(16)) +
    '<text x="320" y="110" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">R0–R15: только некоторые команды (mul, movw…)</text>' +
    # R16-R31
    ''.join(box(30+i*38,130,35,30,'#dcfce7','#16a34a',f'R{i+16}',10) for i in range(16)) +
    '<text x="320" y="180" text-anchor="middle" font-size="11" fill="#15803d" font-family="sans-serif">R16–R31: полный набор команд (ldi, andi, ori, subi…)</text>' +
    # X Y Z
    box(60,200,80,35,'#fef9c3','#f59e0b','X = R27:R26',11) +
    box(200,200,80,35,'#fef9c3','#f59e0b','Y = R29:R28',11) +
    box(340,200,80,35,'#fef9c3','#f59e0b','Z = R31:R30',11) +
    '<text x="320" y="260" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">X, Y, Z — 16-битные указатели для косвенной адресации памяти</text>',
    640, 290, 'Регистры R0–R31; X/Y/Z — парные 16-битные указатели'
) +
'''<h3>Статусный регистр SREG</h3>
<p>SREG (Status Register) — 8 флагов, автоматически устанавливаемых после операций:</p>''' +
table(
    ['Бит','Флаг','Значение'],
    [
        ['7','I','Глобальное разрешение прерываний'],
        ['6','T','Бит копирования (BLD/BST)'],
        ['5','H','Half Carry (перенос из бит3)'],
        ['4','S','Sign (N⊕V)'],
        ['3','V','Переполнение дополнительного кода'],
        ['2','N','Отрицательный результат'],
        ['1','Z','Нулевой результат'],
        ['0','C','Перенос (Carry)'],
    ]
) +
tip('Флаг Z (Zero) используется в условных переходах: <code>brne</code> — перейти если не ноль, <code>breq</code> — если ноль.'),
'code_example': '''// Работа с регистрами AVR в ассемблере
.include "m328pdef.inc"

.org 0x0000
rjmp main

main:
    ldi  r16, 0xFF    ; R16 = 255 (0xFF)
    ldi  r17, 0x0A    ; R17 = 10
    add  r16, r17     ; R16 = R16 + R17 = 265 → 9 (+ C=1)

    ; Проверка флага Carry
    brcc no_carry     ; перейти если C=0
    ldi  r18, 1       ; есть перенос
no_carry:

    ; Загрузка 16-битного адреса в Z
    ldi  ZL, lo8(data_table)
    ldi  ZH, hi8(data_table)
    ld   r16, Z+      ; загрузить из SRAM[Z], Z++

data_table: .byte 0x11, 0x22, 0x33'''
},

{
'title': 'Группы команд: арифметика, логика, переходы',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>Система команд AVR</h2>
<p>AVR — <strong>RISC</strong>-архитектура: большинство команд выполняется за <strong>1 такт</strong>, фиксированная длина слова команды — <strong>16 бит</strong> (некоторые 32-бит).</p>
''' +
table(
    ['Группа','Команды','Пример'],
    [
        ['Пересылка данных','mov, ldi, ld, st, lds, sts, push, pop','<code>ldi r16, 42</code>'],
        ['Арифметика','add, sub, adc, sbc, inc, dec, mul, neg','<code>add r16, r17</code>'],
        ['Логика','and, or, eor, com, andi, ori','<code>andi r16, 0x0F</code>'],
        ['Сдвиги','lsl, lsr, rol, ror, asr','<code>lsl r16</code> (×2)'],
        ['Биты','sbi, cbi, sbis, sbic, bst, bld','<code>sbi PORTB, 5</code>'],
        ['Переходы','rjmp, jmp, rcall, call, ret, reti','<code>rjmp loop</code>'],
        ['Условные','brne, breq, brcs, brcc, brmi, brpl','<code>brne loop</code>'],
        ['Управление','nop, sleep, wdr, sei, cli','<code>sei</code>'],
    ]
) +
diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="290" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Конвейер AVR: Fetch → Decode → Execute</text>' +
    # Pipeline
    box(30,60,170,50,'#dbeafe','#3b82f6','FETCH\nчитаем команду из Flash',11) +
    box(230,60,170,50,'#dcfce7','#16a34a','DECODE\nдекодируем опкод',11) +
    box(430,60,170,50,'#fef9c3','#f59e0b','EXECUTE\nвыполняем операцию',11) +
    arrow(200,85,230,85) + arrow(400,85,430,85) +
    '<text x="320" y="140" text-anchor="middle" font-size="12" fill="#64748b" font-family="sans-serif">Пока выполняется команда N, считывается команда N+1</text>' +
    # Timing
    '<rect x="30" y="160" width="580" height="120" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="40" y="180" font-size="11" fill="#64748b" font-family="sans-serif">Такт:</text>' +
    ''.join(f'<rect x="{90+i*50}" y="165" width="48" height="20" rx="3" fill="#3b82f6" opacity="0.7"/><text x="{114+i*50}" y="179" text-anchor="middle" font-size="10" fill="white" font-family="sans-serif">{i+1}</text>' for i in range(10)) +
    '<text x="40" y="220" font-size="11" fill="#64748b" font-family="sans-serif">CMD1:</text>' +
    '<rect x="90" y="205" width="48" height="15" rx="2" fill="#3b82f6" opacity="0.5"/>' +
    '<rect x="140" y="205" width="48" height="15" rx="2" fill="#16a34a" opacity="0.5"/>' +
    '<rect x="190" y="205" width="48" height="15" rx="2" fill="#f59e0b" opacity="0.5"/>' +
    '<text x="40" y="255" font-size="11" fill="#64748b" font-family="sans-serif">CMD2:</text>' +
    '<rect x="140" y="240" width="48" height="15" rx="2" fill="#3b82f6" opacity="0.5"/>' +
    '<rect x="190" y="240" width="48" height="15" rx="2" fill="#16a34a" opacity="0.5"/>' +
    '<rect x="240" y="240" width="48" height="15" rx="2" fill="#f59e0b" opacity="0.5"/>' +
    '<text x="320" y="285" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Параллельное выполнение → 1 команда за такт</text>',
    640, 300, 'Двухстадийный конвейер AVR'
) +
tip('Большинство команд AVR = 1 такт при 16 МГц → 16 MIPS. Команды mul, jmp, call = 2 такта.') +
warn('Команды <code>ldi</code>, <code>andi</code>, <code>ori</code>, <code>cpi</code> работают только с R16–R31!'),
'code_example': '''// Все группы команд в одном примере
#include <avr/io.h>

void demo_commands(void) {
    uint8_t a = 10, b = 3;

    // Арифметика
    uint8_t sum  = a + b;   // ADD: sum = 13
    uint8_t diff = a - b;   // SUB: diff = 7
    uint8_t prod = a * b;   // MUL: prod = 30 (8-bit)

    // Логика (битовые маски)
    uint8_t mask = a & 0x0F;  // AND: младшие 4 бита = 0x0A
    uint8_t flags= a | 0x80;  // OR:  установить бит7 = 0x8A
    uint8_t inv  = ~a;         // COM: инверсия = 0xF5
    uint8_t xorv = a ^ b;      // EOR: XOR = 9

    // Сдвиги (=умножение/деление на 2)
    uint8_t x2   = a << 1;    // LSL: 20
    uint8_t div2 = a >> 1;    // LSR: 5

    // Условный переход в C (компилятор → brne/breq)
    if (sum == 13) {
        PORTB |= (1 << PB0);  // SBI: установить бит
    }
}'''
},

{
'title': 'Режимы адресации AVR',
'order': 3, 'estimated_minutes': 45,
'content': '''
<h2>Режимы адресации</h2>
<p>Режим адресации определяет, <em>как</em> команда находит свои операнды.</p>
''' +
table(
    ['Режим','Синтаксис','Операнд находится в…','Пример'],
    [
        ['Регистровый','Rd, Rr','Регистр','<code>add r16, r17</code>'],
        ['Непосредственный','Rd, K','Константа в команде','<code>ldi r16, 42</code>'],
        ['Прямой (SRAM)','Rd, (addr)','Ячейка SRAM по адресу','<code>lds r16, 0x100</code>'],
        ['Косвенный','Rd, (X/Y/Z)','SRAM[X], SRAM[Y], SRAM[Z]','<code>ld r16, X</code>'],
        ['Пост-инкремент','Rd, X+','SRAM[X], затем X++','<code>ld r16, X+</code>'],
        ['Пред-декремент','Rd, -X','X--, затем SRAM[X]','<code>ld r16, -X</code>'],
        ['С смещением','Rd, Y+q','SRAM[Y+q] (0–63)','<code>ldd r16, Y+4</code>'],
        ['Относительный','метка','PC + смещение','<code>rjmp loop</code>'],
    ]
) +
diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="270" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    # Registers
    '<rect x="30" y="30" width="100" height="230" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>' +
    '<text x="80" y="50" text-anchor="middle" font-size="12" fill="#1e40af" font-weight="bold" font-family="sans-serif">Регистры</text>' +
    ''.join(f'<rect x="40" y="{60+i*25}" width="80" height="20" rx="3" fill="#bfdbfe" stroke="#93c5fd"/><text x="80" y="{74+i*25}" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">R{i+16}</text>' for i in range(7)) +
    box(155,30,80,40,'#fef9c3','#f59e0b','X=R27:R26',10) +
    box(155,85,80,40,'#fef9c3','#f59e0b','Y=R29:R28',10) +
    box(155,140,80,40,'#fef9c3','#f59e0b','Z=R31:R30',10) +
    arrow(235,50,300,50) + arrow(235,105,300,105) + arrow(235,160,300,160) +
    # SRAM
    '<rect x="300" y="30" width="120" height="230" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>' +
    '<text x="360" y="50" text-anchor="middle" font-size="12" fill="#14532d" font-weight="bold" font-family="sans-serif">SRAM</text>' +
    ''.join(f'<rect x="310" y="{60+i*22}" width="100" height="18" rx="3" fill="#bbf7d0" stroke="#86efac"/><text x="360" y="{73+i*22}" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">0x{0x100+i*2:04X}</text>' for i in range(8)) +
    '<text x="480" y="50" font-size="11" fill="#64748b" font-family="sans-serif">Режимы:</text>' +
    '<text x="480" y="80" font-size="10" fill="#3b82f6" font-family="sans-serif">ld r16,X → [X]</text>' +
    '<text x="480" y="100" font-size="10" fill="#16a34a" font-family="sans-serif">ld r16,X+ → [X],X++</text>' +
    '<text x="480" y="120" font-size="10" fill="#f59e0b" font-family="sans-serif">ld r16,-X → X--,[X]</text>' +
    '<text x="480" y="140" font-size="10" fill="#db2777" font-family="sans-serif">ldd r16,Y+4 → [Y+4]</text>',
    640, 280, 'Косвенная адресация через регистры X, Y, Z'
) +
tip('Post-increment (<code>X+</code>) идеален для обхода массивов. Pre-decrement (<code>-X</code>) удобен для обратного обхода.') +
warn('<code>ldi</code> работает ТОЛЬКО с R16–R31. Для R0–R15 используйте <code>clr</code> + <code>andi</code>.'),
'code_example': '''// Демонстрация режимов адресации
#include <avr/io.h>

uint8_t array[8] = {1,2,3,4,5,6,7,8};  // в SRAM

uint8_t sum_array(void) {
    uint8_t *ptr = array;   // указатель = косвенная адресация
    uint8_t sum = 0;
    for (uint8_t i = 0; i < 8; i++) {
        sum += *ptr++;        // ld r16, X+  (post-increment)
    }
    return sum;
}

// В ASM — то же самое:
// ldi  XL, lo8(array)
// ldi  XH, hi8(array)
// ldi  r18, 8        ; счётчик
// clr  r17           ; сумма = 0
// loop:
//   ld   r16, X+     ; загрузить [X], X++
//   add  r17, r16    ; sum += val
//   dec  r18
//   brne loop'''
},
],

# ─── МОДУЛЬ 3 ─────────────────────────────────────────────────────────────────
3: [
{
'title': 'GPIO: регистры DDR, PORT, PIN',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>GPIO — General Purpose Input/Output</h2>
<p>GPIO — основа взаимодействия МК с внешним миром. Каждый вывод МК может работать как вход или выход; управление осуществляется тремя 8-битными регистрами на каждый порт.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="280" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="14" fill="#1e293b" font-weight="bold" font-family="sans-serif">Три регистра GPIO на каждый порт</text>' +
    box(30,55,160,50,'#dbeafe','#3b82f6','DDRx\n(Direction)',12,'bold') +
    '<text x="110" y="130" text-anchor="middle" font-size="11" fill="#1e40af" font-family="sans-serif">0=вход, 1=выход</text>' +
    box(230,55,160,50,'#dcfce7','#16a34a','PORTx\n(Output/Pull-up)',12,'bold') +
    '<text x="310" y="130" text-anchor="middle" font-size="11" fill="#14532d" font-family="sans-serif">вывод=0/1 или pull-up</text>' +
    box(430,55,160,50,'#fef9c3','#f59e0b','PINx\n(Input Read)',12,'bold') +
    '<text x="510" y="130" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">читаем состояние вывода</text>' +
    # Logic table
    '<rect x="30" y="150" width="580" height="120" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="170" text-anchor="middle" font-size="12" fill="#64748b" font-weight="bold" font-family="sans-serif">Комбинации DDRx / PORTx</text>' +
    '<text x="50" y="195" font-size="11" fill="#1e293b" font-family="sans-serif">DDR=0, PORT=0 → Вход (Hi-Z, без подтяжки)</text>' +
    '<text x="50" y="215" font-size="11" fill="#1e293b" font-family="sans-serif">DDR=0, PORT=1 → Вход с внутренним pull-up (~50 кОм)</text>' +
    '<text x="50" y="235" font-size="11" fill="#1e293b" font-family="sans-serif">DDR=1, PORT=0 → Выход LOW (0 В)</text>' +
    '<text x="50" y="255" font-size="11" fill="#1e293b" font-family="sans-serif">DDR=1, PORT=1 → Выход HIGH (5 В / 3.3 В)</text>',
    640, 290, 'DDR задаёт направление, PORT — состояние выхода/pull-up, PIN — чтение входа'
) +
'''<h3>Битовые операции с GPIO</h3>
<p>Для управления отдельными битами используют четыре операции:</p>''' +
table(
    ['Действие','Код','Объяснение'],
    [
        ['Установить бит','<code>PORTB |= (1&lt;&lt;PB5)</code>','OR с маской — остальные биты не трогаем'],
        ['Сбросить бит','<code>PORTB &= ~(1&lt;&lt;PB5)</code>','AND с инвертированной маской'],
        ['Инвертировать','<code>PORTB ^= (1&lt;&lt;PB5)</code>','XOR — меняем только один бит'],
        ['Проверить бит','<code>if (PINB &amp; (1&lt;&lt;PB0))</code>','AND — читаем нужный бит входа'],
    ]
) +
tip('На AVR есть специальные команды <code>sbi PORTB, 5</code> и <code>cbi PORTB, 5</code> — они работают только с адресами 0x00–0x1F (I/O space).') +
warn('Максимальный ток одного вывода AVR: 40 мА. Суммарный ток порта: 200 мА. Для мощных нагрузок используйте транзистор или драйвер.'),
'code_example': '''#include <avr/io.h>
#include <util/delay.h>

#define LED  PB5   // pin 13 (Arduino Uno)
#define BTN  PD2   // pin 2

int main(void) {
    // Настройка направления
    DDRB  |=  (1 << LED);   // PB5 = выход
    DDRD  &= ~(1 << BTN);   // PD2 = вход
    PORTD |=  (1 << BTN);   // включить pull-up

    while (1) {
        if (!(PIND & (1 << BTN))) {  // кнопка нажата (LOW при pull-up)
            PORTB |= (1 << LED);      // LED ON
        } else {
            PORTB &= ~(1 << LED);     // LED OFF
        }
    }
}'''
},

{
'title': 'Подключение LED и кнопки',
'order': 2, 'estimated_minutes': 45,
'content': '''
<h2>Практические схемы: LED и кнопка</h2>
<h3>Схема подключения LED</h3>
<p>Светодиод — диод с падением напряжения ~2 В (красный/зелёный) или ~3 В (синий/белый). Ток 10–20 мА. Резистор ограничивает ток:</p>
<p style="background:#f1f5f9;padding:12px;border-radius:8px;font-family:monospace">R = (Vcc − Vled) / Iled = (5 − 2) / 0.015 = 200 Ом → берём 220 Ом</p>
''' + diagram(
    DEFS +
    # MCU pin
    box(20,120,80,40,'#dbeafe','#3b82f6','PB5',13,'bold') +
    # Resistor
    '<line x1="100" y1="140" x2="160" y2="140" stroke="#1e293b" stroke-width="2"/>' +
    '<rect x="160" y="130" width="60" height="20" rx="4" fill="#fef9c3" stroke="#f59e0b" stroke-width="1.5"/>' +
    '<text x="190" y="143" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">220Ω</text>' +
    '<line x1="220" y1="140" x2="280" y2="140" stroke="#1e293b" stroke-width="2"/>' +
    # LED symbol
    '<polygon points="280,125 280,155 310,140" fill="#ef4444" stroke="#dc2626" stroke-width="1.5"/>' +
    '<line x1="310" y1="125" x2="310" y2="155" stroke="#dc2626" stroke-width="2"/>' +
    '<line x1="310" y1="140" x2="370" y2="140" stroke="#1e293b" stroke-width="2"/>' +
    # GND
    '<line x1="370" y1="140" x2="370" y2="180" stroke="#1e293b" stroke-width="2"/>' +
    '<line x1="350" y1="180" x2="390" y2="180" stroke="#1e293b" stroke-width="2.5"/>' +
    '<line x1="358" y1="187" x2="382" y2="187" stroke="#1e293b" stroke-width="2"/>' +
    '<line x1="364" y1="194" x2="376" y2="194" stroke="#1e293b" stroke-width="1.5"/>' +
    '<text x="370" y="215" text-anchor="middle" font-size="12" fill="#64748b" font-family="sans-serif">GND</text>' +
    # Labels
    '<text x="190" y="120" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">токоограничивающий</text>' +
    '<text x="295" y="100" text-anchor="middle" font-size="11" fill="#dc2626" font-family="sans-serif">LED (анод→катод)</text>' +
    # Button part
    box(430,80,80,40,'#dbeafe','#3b82f6','PD2',13,'bold') +
    '<line x1="510" y1="100" x2="550" y2="100" stroke="#1e293b" stroke-width="2"/>' +
    box(550,80,60,40,'#dcfce7','#16a34a','BTN',12) +
    '<line x1="610" y1="100" x2="630" y2="100" stroke="#1e293b" stroke-width="2"/>' +
    '<line x1="630" y1="100" x2="630" y2="200" stroke="#1e293b" stroke-width="2"/>' +
    '<line x1="610" y1="200" x2="650" y2="200" stroke="#1e293b" stroke-width="2"/>' +
    '<text x="630" y="220" text-anchor="middle" font-size="12" fill="#64748b" font-family="sans-serif">GND</text>' +
    '<text x="560" y="70" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">+pull-up на PD2</text>',
    680, 240, 'Схемы подключения LED (слева) и кнопки с pull-up (справа)'
) +
'''<h3>Кнопка: активный LOW vs активный HIGH</h3>''' +
table(
    ['Схема','DDR','PORT (pull-up)','Состояние при нажатии','Чтение'],
    [
        ['Pull-up (рекомендуется)','DDR=0','PORT=1','PIN=0 (LOW)','<code>!(PIND &amp; btn)</code>'],
        ['Pull-down (внешний резистор)','DDR=0','PORT=0','PIN=1 (HIGH)','<code>PIND &amp; btn</code>'],
    ]
) +
tip('Внутренний pull-up (~50 кОм) упрощает схему — не нужен внешний резистор. Большинство кнопок подключают к GND (активный LOW).') +
warn('Без pull-up/pull-down вход «висит в воздухе» — МК будет считывать случайные значения. Всегда подтягивайте!'),
'code_example': '''#include <avr/io.h>
#include <util/delay.h>

#define LED_PORT PORTB
#define LED_DDR  DDRB
#define LED_PIN  PB5

#define BTN_PORT PORTD
#define BTN_DDR  DDRD
#define BTN_IN   PIND
#define BTN_PIN  PD2

void blink(uint8_t times) {
    for (uint8_t i = 0; i < times; i++) {
        LED_PORT |= (1 << LED_PIN);
        _delay_ms(200);
        LED_PORT &= ~(1 << LED_PIN);
        _delay_ms(200);
    }
}

int main(void) {
    LED_DDR  |=  (1 << LED_PIN);   // LED = выход
    BTN_DDR  &= ~(1 << BTN_PIN);   // BTN = вход
    BTN_PORT |=  (1 << BTN_PIN);   // pull-up включён

    uint8_t count = 0;
    while (1) {
        if (!(BTN_IN & (1 << BTN_PIN))) { // кнопка нажата
            _delay_ms(20);                 // debounce
            if (!(BTN_IN & (1 << BTN_PIN))) {
                count++;
                blink(count % 4 + 1);
            }
            while (!(BTN_IN & (1 << BTN_PIN))); // ждём отпускания
        }
    }
}'''
},

{
'title': 'Битовые операции и маски',
'order': 3, 'estimated_minutes': 40,
'content': '''
<h2>Битовые операции — основа работы с регистрами МК</h2>
<p>Регистры МК — это 8-битные числа. Каждый бит управляет отдельной функцией. Умение работать с битами без изменения остальных — ключевой навык.</p>
''' +
table(
    ['Операция','Символ C','Таблица истинности','Применение'],
    [
        ['AND','&amp;','0&amp;x=0, 1&amp;1=1','Маскирование (сбросить/проверить)'],
        ['OR','|','0|x=x, 1|x=1','Установить биты'],
        ['XOR','^','x^0=x, x^1=~x','Инвертировать биты'],
        ['NOT (унарный)','~','~0=1, ~1=0','Инвертировать маску'],
        ['Сдвиг влево','&lt;&lt;','x &lt;&lt; n = x × 2ⁿ','Создание маски: 1&lt;&lt;n'],
        ['Сдвиг вправо','&gt;&gt;','x &gt;&gt; n = x / 2ⁿ','Извлечение поля'],
    ]
) +
diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="260" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Рецепты битовых операций</text>' +
    # Set bit
    '<rect x="30" y="50" width="180" height="55" rx="6" fill="#dcfce7" stroke="#16a34a"/>' +
    '<text x="120" y="70" text-anchor="middle" font-size="12" fill="#14532d" font-weight="bold" font-family="sans-serif">Установить бит N</text>' +
    '<text x="120" y="90" text-anchor="middle" font-size="11" fill="#14532d" font-family="monospace">REG |= (1&lt;&lt;N)</text>' +
    # Clear bit
    '<rect x="230" y="50" width="180" height="55" rx="6" fill="#fee2e2" stroke="#ef4444"/>' +
    '<text x="320" y="70" text-anchor="middle" font-size="12" fill="#991b1b" font-weight="bold" font-family="sans-serif">Сбросить бит N</text>' +
    '<text x="320" y="90" text-anchor="middle" font-size="11" fill="#991b1b" font-family="monospace">REG &amp;= ~(1&lt;&lt;N)</text>' +
    # Toggle
    '<rect x="430" y="50" width="180" height="55" rx="6" fill="#fef9c3" stroke="#f59e0b"/>' +
    '<text x="520" y="70" text-anchor="middle" font-size="12" fill="#92400e" font-weight="bold" font-family="sans-serif">Инвертировать бит N</text>' +
    '<text x="520" y="90" text-anchor="middle" font-size="11" fill="#92400e" font-family="monospace">REG ^= (1&lt;&lt;N)</text>' +
    # Check
    '<rect x="30" y="120" width="180" height="55" rx="6" fill="#dbeafe" stroke="#3b82f6"/>' +
    '<text x="120" y="140" text-anchor="middle" font-size="12" fill="#1e40af" font-weight="bold" font-family="sans-serif">Проверить бит N</text>' +
    '<text x="120" y="160" text-anchor="middle" font-size="11" fill="#1e40af" font-family="monospace">REG &amp; (1&lt;&lt;N)</text>' +
    # Extract field
    '<rect x="230" y="120" width="180" height="55" rx="6" fill="#fdf4ff" stroke="#a855f7"/>' +
    '<text x="320" y="140" text-anchor="middle" font-size="12" fill="#6b21a8" font-weight="bold" font-family="sans-serif">Извлечь поле [M:N]</text>' +
    '<text x="320" y="160" text-anchor="middle" font-size="11" fill="#6b21a8" font-family="monospace">(REG &gt;&gt; N) &amp; mask</text>' +
    # Set field
    '<rect x="430" y="120" width="180" height="55" rx="6" fill="#fff7ed" stroke="#f97316"/>' +
    '<text x="520" y="140" text-anchor="middle" font-size="12" fill="#9a3412" font-weight="bold" font-family="sans-serif">Записать поле</text>' +
    '<text x="520" y="160" text-anchor="middle" font-size="11" fill="#9a3412" font-family="monospace">REG=(REG&amp;~m)|(v&lt;&lt;N)</text>' +
    '<text x="320" y="210" text-anchor="middle" font-size="12" fill="#64748b" font-family="sans-serif">Пример: TCCR0B = (TCCR0B &amp; ~0x07) | prescaler</text>' +
    '<text x="320" y="235" text-anchor="middle" font-size="11" fill="#94a3b8" font-family="sans-serif">— устанавливаем биты CS02:CS00 не трогая остальные</text>',
    640, 260, 'Шаблоны битовых операций для работы с регистрами МК'
) +
tip('Всегда используйте именованные константы: <code>(1&lt;&lt;CS01)</code> вместо <code>0x02</code> — код самодокументируется.') +
warn('Операция присваивания <code>=</code> вместо <code>|=</code> сотрёт все остальные биты регистра! Это частая ошибка.'),
'code_example': '''#include <avr/io.h>

// Работа с регистром TCCR0B таймера 0
// Биты CS02:CS00 задают предделитель

#define PRESCALER_8  2  // CS02:CS00 = 010

void timer_setup(void) {
    // НЕПРАВИЛЬНО — сотрёт остальные биты:
    // TCCR0B = PRESCALER_8;

    // ПРАВИЛЬНО — только меняем CS02:CS00:
    TCCR0B = (TCCR0B & ~((1<<CS02)|(1<<CS01)|(1<<CS00)))
           | (PRESCALER_8 << CS00);
}

// Проверка нескольких битов сразу
uint8_t get_port_state(void) {
    uint8_t val = PINB;
    uint8_t result = 0;
    if (val & (1<<PB0)) result |= 0x01;  // кнопка 1
    if (val & (1<<PB1)) result |= 0x02;  // кнопка 2
    if (val & (1<<PB2)) result |= 0x04;  // кнопка 3
    return result;
}

// Извлечь поле адреса (биты 3:1)
uint8_t get_addr(uint8_t reg) {
    return (reg >> 1) & 0x07;   // биты [3:1] → [2:0]
}'''
},
],

# ─── МОДУЛЬ 4 ─────────────────────────────────────────────────────────────────
4: [
{
'title': 'Механизм прерываний AVR',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>Прерывания — реакция МК в реальном времени</h2>
<p><strong>Прерывание (interrupt)</strong> — аппаратный сигнал, заставляющий процессор приостановить текущую программу и немедленно выполнить специальный обработчик (ISR — Interrupt Service Routine).</p>
<p>Без прерываний МК вынужден постоянно опрашивать (polling) все устройства — это расточительно. Прерывания позволяют МК «спать» и реагировать только на события.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="280" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="14" fill="#1e293b" font-weight="bold" font-family="sans-serif">Жизненный цикл прерывания</text>' +
    # Main program
    '<rect x="30" y="55" width="100" height="200" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>' +
    '<text x="80" y="75" text-anchor="middle" font-size="11" fill="#1e40af" font-weight="bold" font-family="sans-serif">main()</text>' +
    ''.join(f'<rect x="40" y="{85+i*28}" width="80" height="20" rx="3" fill="#bfdbfe"/><text x="80" y="{99+i*28}" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">cmd {i+1}</text>' for i in range(6)) +
    # Event
    '<rect x="180" y="90" width="90" height="35" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="225" y="112" text-anchor="middle" font-size="11" fill="#991b1b" font-weight="bold" font-family="sans-serif">Событие!</text>' +
    arrow(130,135,180,130,'#ef4444') +
    # Save context
    box(290,60,100,35,'#fef9c3','#f59e0b','1.Сохр.\nконтекст',10) +
    arrow(225,107,290,77) +
    # ISR
    '<rect x="410" y="55" width="100" height="130" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>' +
    '<text x="460" y="75" text-anchor="middle" font-size="11" fill="#14532d" font-weight="bold" font-family="sans-serif">ISR()</text>' +
    ''.join(f'<rect x="420" y="{85+i*28}" width="80" height="20" rx="3" fill="#bbf7d0"/><text x="460" y="{99+i*28}" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">isr cmd {i+1}</text>' for i in range(3)) +
    arrow(390,77,410,77) +
    # Restore
    box(290,155,100,35,'#fef9c3','#f59e0b','2.Восст.\nконтекст',10) +
    arrow(460,185,390,172) +
    arrow(390,172,130,150,'#16a34a'),
    640, 290, 'МК прерывает main(), выполняет ISR, восстанавливает контекст и продолжает'
) +
table(
    ['Шаг','Что происходит'],
    [
        ['1. Событие','Источник прерывания (внешний сигнал, переполнение таймера, байт UART…) устанавливает флаг'],
        ['2. Завершение команды','ЦП дожидается окончания текущей команды'],
        ['3. Сохранение PC','Адрес возврата помещается в стек'],
        ['4. Сохранение SREG','(в ручном режиме или автоматически через push)'],
        ['5. Переход в ISR','PC = адрес вектора прерывания из таблицы'],
        ['6. Выполнение ISR','Обработчик обрабатывает событие'],
        ['7. reti','Восстановление PC + I-флаг, возврат в main()'],
    ]
) +
tip('Таблица векторов прерываний начинается с адреса 0x0000 во Flash. Каждый вектор = 2 байта (jmp ISR_addr).') +
warn('В ISR нельзя вызывать функции с длительным ожиданием. ISR должна быть короткой и быстрой!'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>

volatile uint8_t flag = 0;   // volatile обязателен!

// Вектор прерывания INT0 (PD2, pin 2)
ISR(INT0_vect) {
    flag = 1;   // установить флаг — обработать в main()
}

int main(void) {
    DDRD  &= ~(1 << PD2);  // PD2 = вход
    PORTD |=  (1 << PD2);  // pull-up

    // Настройка INT0: прерывание по спадающему фронту
    EICRA |= (1 << ISC01);   // ISC01=1, ISC00=0 → falling edge
    EIMSK |= (1 << INT0);    // разрешить INT0

    sei();  // глобально разрешить прерывания (I-флаг SREG)

    while (1) {
        if (flag) {
            flag = 0;
            PORTB ^= (1 << PB5);   // мигнуть LED
        }
        // Остальная работа...
    }
}'''
},

{
'title': 'INT0/INT1 и PCINT',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>Внешние прерывания AVR</h2>
<p>ATmega328P имеет два типа внешних прерываний:</p>
''' +
table(
    ['Тип','Выводы','Настройка','Особенности'],
    [
        ['INT0','PD2 (pin 2)','EICRA, EIMSK','Настраиваемый фронт/уровень, приоритетнее'],
        ['INT1','PD3 (pin 3)','EICRA, EIMSK','Настраиваемый фронт/уровень'],
        ['PCINT0','PB0–PB7','PCICR, PCMSK0','Любое изменение на любом пине порта B'],
        ['PCINT1','PC0–PC6','PCICR, PCMSK1','Любое изменение на любом пине порта C'],
        ['PCINT2','PD0–PD7','PCICR, PCMSK2','Любое изменение на любом пине порта D'],
    ]
) +
diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="240" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Настройка INT0/INT1 — регистр EICRA</text>' +
    # EICRA bits
    ''.join(box(30+i*75,55,70,40,'#dbeafe','#3b82f6',f'ISC1{1-i%2}\nбит{7-i}',11) for i in range(4)) +
    ''.join(box(330+i*75,55,70,40,'#dcfce7','#16a34a',f'ISC0{1-i%2}\nбит{3-i}',11) for i in range(4)) +
    '<text x="155" y="120" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">INT1</text>' +
    '<text x="455" y="120" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">INT0</text>' +
    # Table
    '<rect x="30" y="135" width="580" height="95" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="320" y="155" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold" font-family="sans-serif">ISCx1:ISCx0 → режим</text>' +
    '<text x="80" y="175" font-size="11" fill="#64748b" font-family="sans-serif">00 = LOW level (низкий уровень)</text>' +
    '<text x="80" y="193" font-size="11" fill="#64748b" font-family="sans-serif">01 = любое изменение (CHANGE)</text>' +
    '<text x="80" y="211" font-size="11" fill="#64748b" font-family="sans-serif">10 = спадающий фронт (FALLING)</text>' +
    '<text x="350" y="175" font-size="11" fill="#64748b" font-family="sans-serif">11 = нарастающий фронт (RISING)</text>' +
    '<text x="350" y="211" font-size="11" fill="#64748b" font-family="sans-serif">⚠ LOW level генерирует непрерывно!</text>',
    640, 250, 'EICRA управляет режимом срабатывания INT0 и INT1'
) +
tip('PCINT срабатывает на ЛЮБОЕ изменение любого из разрешённых выводов. В ISR нужно самому определить, какой именно пин изменился, сохранив предыдущее состояние порта.') +
warn('INT0/INT1 при режиме LOW level будут непрерывно вызывать ISR пока вывод остаётся низким. Обычно используют FALLING.'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>

// ── PCINT: кнопки на нескольких пинах ──────────────────────────
volatile uint8_t prev_state;

ISR(PCINT2_vect) {
    uint8_t curr = PIND;
    uint8_t changed = prev_state ^ curr;   // какие биты изменились
    prev_state = curr;

    if (changed & (1 << PD4)) {            // именно PD4
        if (!(curr & (1 << PD4))) {        // спадающий фронт
            PORTB ^= (1 << PB5);           // мигнуть LED
        }
    }
}

int main(void) {
    // Настройка PCINT2 на PD4
    DDRD  &= ~(1 << PD4);
    PORTD |=  (1 << PD4);   // pull-up

    PCICR  |= (1 << PCIE2);  // разрешить PCINT2 группу
    PCMSK2 |= (1 << PCINT20); // конкретный пин PD4

    prev_state = PIND;
    sei();

    while (1) { /* основной цикл */ }
}'''
},

{
'title': 'Ключевое слово volatile и защита данных',
'order': 3, 'estimated_minutes': 40,
'content': '''
<h2>volatile — защита от оптимизации компилятора</h2>
<p>Компилятор оптимизирует код, кэшируя значения переменных в регистрах. Если переменную изменяет ISR, компилятор не знает об этом и может использовать устаревшее значение.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="240" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    # Without volatile
    '<rect x="20" y="30" width="280" height="190" rx="8" fill="#fee2e2" stroke="#ef4444"/>' +
    '<text x="160" y="52" text-anchor="middle" font-size="12" fill="#991b1b" font-weight="bold" font-family="sans-serif">БЕЗ volatile (ошибка!)</text>' +
    '<text x="35" y="75" font-size="10" fill="#7f1d1d" font-family="monospace">uint8_t flag = 0;</text>' +
    '<text x="35" y="95" font-size="10" fill="#7f1d1d" font-family="monospace">ISR(...) { flag=1; }</text>' +
    '<text x="35" y="120" font-size="10" fill="#7f1d1d" font-family="monospace">main: if(flag) → OK при -O0</text>' +
    '<text x="35" y="145" font-size="10" fill="#ef4444" font-family="monospace">При -Os компилятор видит:</text>' +
    '<text x="35" y="165" font-size="10" fill="#ef4444" font-family="monospace">flag=0 → не меняется → if(0)</text>' +
    '<text x="35" y="185" font-size="10" fill="#ef4444" font-family="monospace">→ УДАЛЯЕТ проверку! BUG!</text>' +
    '<text x="35" y="205" font-size="10" fill="#dc2626" font-family="monospace">Петля while(1) бесконечна</text>' +
    # With volatile
    '<rect x="320" y="30" width="290" height="190" rx="8" fill="#dcfce7" stroke="#16a34a"/>' +
    '<text x="465" y="52" text-anchor="middle" font-size="12" fill="#14532d" font-weight="bold" font-family="sans-serif">С volatile (правильно)</text>' +
    '<text x="335" y="75" font-size="10" fill="#14532d" font-family="monospace">volatile uint8_t flag = 0;</text>' +
    '<text x="335" y="95" font-size="10" fill="#14532d" font-family="monospace">ISR(...) { flag=1; }</text>' +
    '<text x="335" y="120" font-size="10" fill="#14532d" font-family="monospace">main: if(flag) →</text>' +
    '<text x="335" y="140" font-size="10" fill="#14532d" font-family="monospace">Компилятор ВСЕГДА читает</text>' +
    '<text x="335" y="160" font-size="10" fill="#14532d" font-family="monospace">из памяти, не из регистра</text>' +
    '<text x="335" y="185" font-size="10" fill="#15803d" font-family="monospace">→ ISR может изменить, main</text>' +
    '<text x="335" y="205" font-size="10" fill="#15803d" font-family="monospace">   всегда увидит изменение</text>',
    640, 250, 'volatile запрещает компилятору кэшировать переменную'
) +
'''<h3>Атомарный доступ к многобайтным переменным</h3>
<p>16-битная переменная на 8-битном AVR читается/пишется за 2 команды. ISR может вклиниться между ними!</p>''' +
table(
    ['Проблема','Решение'],
    [
        ['Прерывание между чтением старшего и младшего байта','Запрет прерываний на время доступа'],
        ['Компилятор оптимизирует флаг','volatile для всех переменных, изменяемых в ISR'],
        ['Гонка данных в 16-bit переменных','ATOMIC_BLOCK(ATOMIC_RESTORESTATE)'],
    ]
) +
tip('Правило: <em>любая</em> переменная, разделяемая между ISR и основным кодом, должна быть <code>volatile</code>.') +
warn('ATOMIC_BLOCK временно запрещает ВСЕ прерывания. Используйте только для кратких операций чтения/записи.'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/atomic.h>

volatile uint16_t timer_ticks = 0;   // изменяется в ISR

ISR(TIMER1_COMPA_vect) {
    timer_ticks++;   // 16-bit: 2 инструкции AVR!
}

int main(void) {
    // ... настройка таймера ...
    sei();

    while (1) {
        uint16_t t;

        // НЕПРАВИЛЬНО — может прочитать half-updated значение:
        // t = timer_ticks;

        // ПРАВИЛЬНО — атомарное чтение:
        ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
            t = timer_ticks;
        }

        if (t > 1000) {
            // прошло 1000 тиков
        }
    }
}'''
},
],

# ─── МОДУЛЬ 5 ─────────────────────────────────────────────────────────────────
5: [
{
'title': 'Таймеры ATmega328P: Timer0, Timer1, Timer2',
'order': 1, 'estimated_minutes': 60,
'content': '''
<h2>Таймеры/счётчики AVR</h2>
<p>ATmega328P содержит три таймера-счётчика. Таймер — это аппаратный счётчик, тактируемый от системного генератора через предделитель. По достижении заданного значения генерируется прерывание или меняется выход ШИМ.</p>
''' +
table(
    ['Таймер','Разрядность','Векторы','Выводы ШИМ','Особенности'],
    [
        ['Timer0','8 бит','OVF, COMPA, COMPB','OC0A(PD6), OC0B(PD5)','millis(), delay() используют Timer0'],
        ['Timer1','16 бит','OVF, COMPA, COMPB, CAPT','OC1A(PB1), OC1B(PB2)','Точный захват (Input Capture)'],
        ['Timer2','8 бит','OVF, COMPA, COMPB','OC2A(PB3), OC2B(PD3)','Может тактироваться от кварца 32768'],
    ]
) +
diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="260" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Структура таймера (CTC mode)</text>' +
    # Clock source
    box(20,60,90,40,'#dbeafe','#3b82f6','CLK_IO\n16 МГц',11) +
    arrow(110,80,150,80) +
    box(150,60,100,40,'#fef9c3','#f59e0b','Предделитель\n1/8/64/256/1024',10) +
    arrow(250,80,295,80) +
    box(295,55,80,50,'#dcfce7','#16a34a','Счётчик\nTCNTx',12,'bold') +
    arrow(375,80,420,80) +
    '<text x="450" y="75" font-size="11" fill="#64748b" font-family="sans-serif">= OCRxA?</text>' +
    '<rect x="420" y="60" width="80" height="35" rx="5" fill="#eff6ff" stroke="#6366f1"/>' +
    '<text x="460" y="81" text-anchor="middle" font-size="11" fill="#4338ca" font-family="sans-serif">Компаратор</text>' +
    arrow(460,95,460,130) +
    '<text x="460" y="125" font-size="10" fill="#16a34a" font-family="sans-serif">совпало!</text>' +
    box(390,130,140,40,'#dcfce7','#16a34a','Прерывание\nTIMER_COMPA',11) +
    # CTC waveform
    '<rect x="20" y="155" width="580" height="95" rx="6" fill="#fff" stroke="#e2e8f0"/>' +
    '<text x="310" y="175" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">CTC: счётчик растёт до OCR, сбрасывается, ISR срабатывает</text>' +
    '<line x1="40" y1="230" x2="580" y2="230" stroke="#94a3b8" stroke-width="1"/>' +
    '<line x1="40" y1="185" x2="40" y2="235" stroke="#94a3b8" stroke-width="1"/>' +
    ''.join(f'<line x1="{40+i*80}" y1="{230-(i%1)*35}" x2="{40+(i+1)*80}" y2="{230-35}" stroke="#3b82f6" stroke-width="2"/><line x1="{120+i*80}" y1="{195}" x2="{120+i*80}" y2="{230}" stroke="#3b82f6" stroke-width="2"/>' for i in range(6)) +
    '<text x="310" y="248" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">▲ пилообразный счётчик (CTC) ← сброс при совпадении</text>',
    640, 270, 'CTC (Clear Timer on Compare): точный период прерывания'
) +
'''<h3>Расчёт предделителя и OCR</h3>
<p>Для частоты прерывания <strong>f_isr</strong> при тактовой <strong>F_CPU</strong>:</p>
<p style="background:#f1f5f9;padding:12px;border-radius:8px;font-family:monospace;text-align:center">OCR = F_CPU / (предделитель × f_isr) − 1</p>
<p>Пример: F_CPU=16МГц, предделитель=64, нужна f=1000 Гц (каждые 1 мс):<br>
OCR = 16 000 000 / (64 × 1000) − 1 = 249</p>''' +
tip('Для Timer1 (16 бит) можно использовать OCR до 65535, что даёт очень низкие частоты (до 0.24 Гц при предделителе 1024).') +
warn('Timer0 использует Arduino millis() и delay(). Если перенастроить Timer0, эти функции перестанут работать корректно.'),
'code_example': '''#include <avr/io.h>
#include <avr/interrupt.h>

// Timer1 CTC, 1 Гц (мигаем LED каждую секунду)
// F_CPU=16МГц, prescaler=256: OCR1A = 16e6/(256*1) - 1 = 62499

volatile uint8_t led_state = 0;

ISR(TIMER1_COMPA_vect) {
    led_state ^= 1;
    if (led_state) PORTB |=  (1<<PB5);
    else           PORTB &= ~(1<<PB5);
}

void timer1_init_ctc(uint16_t ocr) {
    TCCR1A = 0;               // нормальный режим портов
    TCCR1B = (1<<WGM12)       // CTC mode
           | (1<<CS12);       // prescaler = 256
    OCR1A  = ocr;             // период
    TIMSK1 = (1<<OCIE1A);     // разрешить прерывание по совпадению A
}

int main(void) {
    DDRB |= (1<<PB5);
    timer1_init_ctc(62499);
    sei();
    while (1) { /* спим, работает таймер */ }
}'''
},

{
'title': 'ШИМ (PWM) на AVR',
'order': 2, 'estimated_minutes': 55,
'content': '''
<h2>ШИМ — широтно-импульсная модуляция</h2>
<p><strong>ШИМ (PWM)</strong> — метод управления мощностью путём изменения <strong>скважности</strong> (duty cycle) прямоугольного сигнала. МК генерирует ШИМ аппаратно через таймер.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="200" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">ШИМ сигналы с разной скважностью</text>' +
    # 25%
    '<text x="50" y="65" font-size="11" fill="#64748b" font-family="sans-serif">25%</text>' +
    '<line x1="80" y1="55" x2="80" y2="75" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="80" y1="55" x2="115" y2="55" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="115" y1="55" x2="115" y2="75" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="115" y1="75" x2="195" y2="75" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="195" y1="75" x2="195" y2="55" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="195" y1="55" x2="230" y2="55" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="230" y1="55" x2="230" y2="75" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="230" y1="75" x2="310" y2="75" stroke="#3b82f6" stroke-width="2"/>' +
    # 50%
    '<text x="50" y="125" font-size="11" fill="#64748b" font-family="sans-serif">50%</text>' +
    '<line x1="80" y1="110" x2="80" y2="135" stroke="#16a34a" stroke-width="2"/>' +
    ''.join(f'<line x1="{80+i*115}" y1="110" x2="{138+i*115}" y2="110" stroke="#16a34a" stroke-width="2"/><line x1="{138+i*115}" y1="110" x2="{138+i*115}" y2="135" stroke="#16a34a" stroke-width="2"/><line x1="{138+i*115}" y1="135" x2="{195+i*115}" y2="135" stroke="#16a34a" stroke-width="2"/><line x1="{195+i*115}" y1="135" x2="{195+i*115}" y2="110" stroke="#16a34a" stroke-width="2"/>' for i in range(2)) +
    # 75%
    '<text x="50" y="175" font-size="11" fill="#64748b" font-family="sans-serif">75%</text>' +
    '<line x1="80" y1="160" x2="80" y2="185" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="80" y1="160" x2="195" y2="160" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="195" y1="160" x2="195" y2="185" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="195" y1="185" x2="230" y2="185" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="230" y1="185" x2="230" y2="160" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="230" y1="160" x2="345" y2="160" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="345" y1="160" x2="345" y2="185" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="345" y1="185" x2="380" y2="185" stroke="#f59e0b" stroke-width="2"/>' +
    '<text x="400" y="80" font-size="11" fill="#3b82f6" font-family="sans-serif">→ LED тусклый</text>' +
    '<text x="400" y="130" font-size="11" fill="#16a34a" font-family="sans-serif">→ LED средний</text>' +
    '<text x="400" y="175" font-size="11" fill="#f59e0b" font-family="sans-serif">→ LED яркий</text>',
    640, 210, 'Duty cycle: отношение времени HIGH к периоду'
) +
table(
    ['Режим ШИМ','WGM','Описание','OCR диапазон'],
    [
        ['Fast PWM','WGM=3','Счётчик 0→255→0(сброс). Выше частота','0–255'],
        ['Phase Correct PWM','WGM=1','Счётчик 0→255→0(вниз). Симметричный','0–255'],
        ['Fast PWM 10-bit (T1)','WGM=7','TOP=0x03FF','0–1023'],
        ['Phase+Freq Correct (T1)','WGM=8','TOP=ICR1, симметричный','0–ICR1'],
    ]
) +
tip('analogWrite(pin, val) в Arduino = Fast PWM 8-бит, duty = val/255 × 100%. Частота ~490 Гц для Pin3,9,10,11 и ~980 Гц для Pin5,6.') +
warn('Для управления сервоприводами нужен период 20 мс (50 Гц) и импульс 1–2 мс. Fast PWM на 8-бит даёт слишком высокую частоту — используйте Timer1 с ICR1=39999.'),
'code_example': '''#include <avr/io.h>
// Fast PWM на OC0A (PD6, Arduino pin 6)
// Частота = F_CPU / (prescaler * 256) = 16e6/(64*256) ≈ 977 Гц

void pwm_init(void) {
    DDRD |= (1 << PD6);        // OC0A = выход
    TCCR0A = (1<<COM0A1)       // неинвертирующий ШИМ на OC0A
           | (1<<WGM01)|(1<<WGM00); // Fast PWM
    TCCR0B = (1<<CS01)|(1<<CS00);   // prescaler = 64
    OCR0A = 0;                  // начальная скважность = 0
}

void pwm_set(uint8_t duty) {   // 0–255
    OCR0A = duty;
}

// Плавное мигание LED
int main(void) {
    pwm_init();
    while (1) {
        for (uint8_t i = 0; i < 255; i++) {
            pwm_set(i);
            for (volatile uint16_t d = 0; d < 3000; d++);
        }
        for (uint8_t i = 255; i > 0; i--) {
            pwm_set(i);
            for (volatile uint16_t d = 0; d < 3000; d++);
        }
    }
}'''
},

{
'title': 'Системное время: millis и micros',
'order': 3, 'estimated_minutes': 40,
'content': '''
<h2>Отсчёт времени без блокирующего delay()</h2>
<p>Функция <code>delay()</code> блокирует МК — во время задержки он ничего не делает. Для многозадачного поведения используют <strong>неблокирующие таймеры</strong> на основе <code>millis()</code>.</p>
<h3>Принцип работы millis()</h3>
<p>Arduino Timer0 настроен на прерывание каждые 1.024 мс (при 16 МГц). В ISR инкрементируется глобальный счётчик <code>timer0_millis</code>. <code>millis()</code> возвращает его значение.</p>
''' + diagram(
    DEFS +
    '<rect x="10" y="10" width="620" height="220" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>' +
    '<text x="320" y="35" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Паттерн неблокирующего таймера</text>' +
    # Timeline
    '<line x1="40" y1="100" x2="590" y2="100" stroke="#94a3b8" stroke-width="2"/>' +
    '<text x="40" y="90" font-size="10" fill="#64748b" font-family="sans-serif">0</text>' +
    '<text x="180" y="90" font-size="10" fill="#64748b" font-family="sans-serif">500ms</text>' +
    '<text x="320" y="90" font-size="10" fill="#64748b" font-family="sans-serif">1000ms</text>' +
    '<text x="460" y="90" font-size="10" fill="#64748b" font-family="sans-serif">1500ms</text>' +
    '<line x1="180" y1="95" x2="180" y2="105" stroke="#94a3b8" stroke-width="1.5"/>' +
    '<line x1="320" y1="95" x2="320" y2="105" stroke="#94a3b8" stroke-width="1.5"/>' +
    '<line x1="460" y1="95" x2="460" y2="105" stroke="#94a3b8" stroke-width="1.5"/>' +
    # Events
    '<line x1="40" y1="100" x2="40" y2="120" stroke="#3b82f6" stroke-width="2"/>' +
    '<rect x="30" y="120" width="60" height="25" rx="4" fill="#dbeafe" stroke="#3b82f6"/>' +
    '<text x="60" y="136" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">start</text>' +
    '<line x1="320" y1="100" x2="320" y2="120" stroke="#16a34a" stroke-width="2"/>' +
    '<rect x="295" y="120" width="50" height="25" rx="4" fill="#dcfce7" stroke="#16a34a"/>' +
    '<text x="320" y="136" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">LED!</text>' +
    '<line x1="460" y1="100" x2="460" y2="120" stroke="#16a34a" stroke-width="2"/>' +
    # Interval arrow
    '<line x1="40" y1="160" x2="320" y2="160" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4"/>' +
    '<text x="180" y="155" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">interval = 1000 мс</text>' +
    '<text x="180" y="185" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">millis() - lastTime >= interval → действие</text>' +
    '<text x="180" y="205" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Между проверками МК делает другую работу!</text>',
    640, 230, 'Неблокирующий таймер: действие только при истечении интервала'
) +
tip('Переполнение millis() происходит через 49.7 дней (32-битный счётчик). Правильный код <code>millis() - lastTime >= interval</code> корректно работает даже при переполнении благодаря арифметике беззнаковых чисел.') +
warn('<code>delay()</code> блокирует прерывания и делает МК «глухим» к входным сигналам на время задержки. Избегайте его в продакшн-коде.'),
'code_example': '''// Неблокирующий мигальщик + считывание кнопки
#include <Arduino.h>

const uint8_t LED = 13, BTN = 2;
uint32_t lastBlink = 0;
uint32_t lastDebounce = 0;
bool ledState = false;
bool btnState = false, lastBtnRead = false;

void setup() {
    pinMode(LED, OUTPUT);
    pinMode(BTN, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop() {
    uint32_t now = millis();

    // Мигание каждую секунду — неблокирующее
    if (now - lastBlink >= 1000) {
        lastBlink = now;
        ledState = !ledState;
        digitalWrite(LED, ledState);
    }

    // Debounce кнопки — тоже неблокирующий
    bool read = !digitalRead(BTN);
    if (read != lastBtnRead) lastDebounce = now;
    if (now - lastDebounce > 50) {
        if (read != btnState) {
            btnState = read;
            if (btnState) Serial.println("Button pressed!");
        }
    }
    lastBtnRead = read;
}'''
},
],

}  # конец LESSONS


class Command(BaseCommand):
    help = 'Заполняет расширенный контент для уроков МПС (модули 1–5)'

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

        self.stdout.write(self.style.SUCCESS(f'\nГотово: обработано {total} уроков (модули 1–5)'))
