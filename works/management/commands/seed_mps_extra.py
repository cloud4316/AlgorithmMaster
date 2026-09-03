"""python manage.py seed_mps_extra — новые модули M11-M15 + патч тонких уроков"""
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
    spans = ''.join(f'<tspan x="{x+w//2}" dy="{0 if i==0 else lh}">{l}</tspan>' for i,l in enumerate(lines))
    return rect + f'<text x="{x+w//2}" y="{y0}" text-anchor="middle" font-size="{fs}" fill="{tc}" font-weight="{fw}" font-family="sans-serif">{spans}</text>'

def arrow(x1,y1,x2,y2,c='#64748b'):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.5" marker-end="url(#arr)"/>'

DEFS = '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748b"/></marker></defs>'

BG = '<rect width="640" height="{h}" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>'


# ══════════════════════════════════════════════════════════════════
# НОВЫЕ МОДУЛИ M11–M15
# ══════════════════════════════════════════════════════════════════

NEW_MODULES = [
    {'order':11,'title':'Дисплеи и индикаторы','icon':'fas fa-desktop',
     'description':'LCD HD44780, OLED SSD1306, TFT-дисплеи. Вывод текста и графики.'},
    {'order':12,'title':'Управление двигателями','icon':'fas fa-cog',
     'description':'DC-двигатели с H-мостом L298N, сервоприводы, шаговые двигатели.'},
    {'order':13,'title':'Режимы сна и питание','icon':'fas fa-battery-half',
     'description':'Watchdog Timer, режимы сна AVR, оптимизация потребления для батарейных устройств.'},
    {'order':14,'title':'Протоколы: 1-Wire и CAN','icon':'fas fa-project-diagram',
     'description':'Протокол 1-Wire, датчик DS18B20, введение в CAN-шину.'},
    {'order':15,'title':'Паттерны и архитектура ПО МК','icon':'fas fa-sitemap',
     'description':'Конечные автоматы, планировщик задач, разделение логики, антидребезг.'},
]

LESSONS = {

# ─── МОДУЛЬ 11: ДИСПЛЕИ ───────────────────────────────────────────
11: [
{
'title': 'LCD HD44780 — символьный дисплей 16x2',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>Символьный ЖКД HD44780</h2>
<p>HD44780 — самый распространённый контроллер символьных ЖК-дисплеев. Типичные размеры: 16x2 (16 символов, 2 строки) и 20x4. Подключается к МК напрямую (6–8 линий данных) или через I2C-адаптер PCF8574.</p>
''' + diagram(
    DEFS + BG.format(h=260) +
    '<text x="320" y="30" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Распиновка LCD HD44780 и режимы подключения</text>' +
    box(20,50,280,80,'#dbeafe','#3b82f6','Прямое подключение (8 бит)\nRS, RW, EN + D0-D7 = 11 пинов',11) +
    box(340,50,280,80,'#dcfce7','#16a34a','Через I2C-адаптер PCF8574\nSDA + SCL = только 2 пина',11) +
    box(20,150,280,80,'#fef9c3','#f59e0b','4-битный режим (рекомендуется)\nRS, RW, EN + D4-D7 = 6 пинов',11) +
    box(340,150,280,80,'#fdf4ff','#a855f7','Контраст — потенциометр 10кОм\nмежду VCC, V0, GND',11),
    640, 260, 'Предпочтительный вариант для Ардуино: I2C-адаптер (только 2 провода)'
) +
table(
    ['Вывод','Имя','Функция'],
    [
        ['1','VSS','GND'],
        ['2','VDD','+5В питание'],
        ['3','V0','Контраст (0–5В через потенциометр)'],
        ['4','RS','Register Select: 0=команда, 1=данные'],
        ['5','RW','0=запись, 1=чтение (обычно на GND)'],
        ['6','EN','Enable — строб для фиксации данных'],
        ['7–14','D0–D7','Шина данных (4-бит: используем D4–D7)'],
        ['15','A','Анод подсветки (+5В через 220 Ом)'],
        ['16','K','Катод подсветки (GND)'],
    ]
) +
'''<h3>Система команд HD44780</h3>''' +
table(
    ['Команда','RS','Байт','Действие'],
    [
        ['Clear Display','0','0x01','Очистить экран, курсор в начало'],
        ['Return Home','0','0x02','Курсор в позицию 0,0'],
        ['Set Cursor','0','0x80+addr','Переместить курсор (addr=0–0x27)'],
        ['Display On','0','0x0C','Включить дисплей, курсор скрыт'],
        ['Write Char','1','ASCII','Вывести символ в текущей позиции'],
    ]
) +
tip('Адреса строк для 16x2: строка 0 = 0x00–0x0F, строка 1 = 0x40–0x4F. Для 20x4: строка 2 = 0x14, строка 3 = 0x54.') +
warn('Команда Clear Display занимает 1.52 мс — не вызывайте её каждый кадр. Лучше перезаписывать отдельные символы командой Set Cursor.'),
'code_example': '''// I2C LCD: библиотека LiquidCrystal_I2C
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Адрес 0x27 или 0x3F — зависит от адаптера PCF8574
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Кастомный символ — градус °
uint8_t degree[8] = {0b00110,0b01001,0b01001,0b00110,
                     0b00000,0b00000,0b00000,0b00000};

void setup() {
    lcd.init();
    lcd.backlight();
    lcd.createChar(0, degree);  // сохранить в CGRAM[0]

    lcd.setCursor(0, 0);
    lcd.print("Temp: 23");
    lcd.write(byte(0));         // вывести символ °
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("Hum:  65%");
}

void loop() {
    // Обновляем только число, не весь экран
    static float temp = 23.0;
    temp += 0.1;
    lcd.setCursor(6, 0);
    lcd.print(temp, 1);
}'''
},

{
'title': 'OLED SSD1306 — графический дисплей',
'order': 2, 'estimated_minutes': 55,
'content': '''
<h2>OLED SSD1306 128x64</h2>
<p>OLED-дисплей на контроллере SSD1306 — 128x64 пикселей, монохромный, I2C или SPI. Каждый пиксель — самосветящийся органический диод, не требует подсветки. Отличная контрастность даже при ярком освещении.</p>
''' + diagram(
    DEFS + BG.format(h=240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Организация видеопамяти SSD1306</text>' +
    # Screen grid
    ''.join(f'<rect x="{30+i*8}" y="45" width="7" height="7" rx="1" fill="{chr(35)}{"3b82f6" if (i+j)%3==0 else "e2e8f0"}" />' for j in range(1) for i in range(76)) +
    '<text x="30" y="65" font-size="10" fill="#64748b" font-family="sans-serif">← 128 пикселей (колонок) →</text>' +
    box(30,75,580,35,'#dcfce7','#16a34a','Page 0 (строки 0–7)',11) +
    box(30,115,580,35,'#dbeafe','#3b82f6','Page 1 (строки 8–15)',11) +
    box(30,155,580,15,'#fef9c3','#f59e0b','...',10) +
    box(30,175,580,35,'#fdf4ff','#a855f7','Page 7 (строки 56–63)',11) +
    '<text x="18" y="100" text-anchor="middle" font-size="9" fill="#64748b" font-family="sans-serif" transform="rotate(-90,18,120)">8 страниц x 8 пикс</text>' +
    '<text x="320" y="225" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Страница = 128 байт. Каждый байт = вертикальная полоска 1x8 пикселей (бит 0 = верх)</text>',
    640, 240, 'SSD1306: 8 страниц x 128 колонок. 1 страница = 8 строк пикселей'
) +
table(
    ['Режим','Пиксели','Память','Скорость'],
    [
        ['Горизонтальная адресация','x слева→право, y страница→следующая','1024 байт','Быстрый для текста'],
        ['Вертикальная адресация','x страница→следующая, y↓','1024 байт','Для вертикальных полос'],
        ['Страничная адресация','В пределах одной страницы','128 байт','Обновление одной строки'],
    ]
) +
'''<h3>Шрифты и графика</h3>
<p>Библиотека Adafruit GFX предоставляет:</p>''' +
table(
    ['Функция','Описание'],
    [
        ['<code>drawPixel(x,y,c)</code>','Нарисовать пиксель'],
        ['<code>drawLine(x0,y0,x1,y1,c)</code>','Линия (алгоритм Брезенхема)'],
        ['<code>drawRect / fillRect</code>','Прямоугольник (контур / заливка)'],
        ['<code>drawCircle / fillCircle</code>','Окружность'],
        ['<code>setTextSize(n)</code>','Размер шрифта (1=6x8, 2=12x16…)'],
        ['<code>setFont(&font)</code>','Пользовательский шрифт (из массива)'],
        ['<code>display()</code>','Отправить буфер на экран'],
    ]
) +
tip('Adafruit SSD1306 хранит полный буфер (1 КБ) в SRAM Arduino. У ATmega328P всего 2 КБ SRAM — буфер занимает половину! Если памяти не хватает, используйте U8g2 с потоковым режимом.') +
warn('display() занимает ~20 мс при I2C 100 кГц. При I2C 400 кГц — 5 мс. Частые вызовы display() будут замедлять программу.'),
'code_example': '''#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_ADDR 0x3C
Adafruit_SSD1306 oled(128, 64, &Wire);

// Анимация отскока шарика
int bx=10, by=10, vx=2, vy=1;

void setup() {
    oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
    oled.setTextColor(WHITE);
}

void loop() {
    oled.clearDisplay();

    // Рамка
    oled.drawRect(0, 0, 128, 64, WHITE);

    // Шарик
    oled.fillCircle(bx, by, 5, WHITE);
    bx += vx; by += vy;
    if (bx <= 6  || bx >= 122) vx = -vx;
    if (by <= 6  || by >= 58 ) vy = -vy;

    // Текст
    oled.setTextSize(1);
    oled.setCursor(35, 26);
    oled.print("AVR OLED!");

    // Прогресс-бар
    static int prog = 0;
    prog = (prog + 1) % 100;
    oled.drawRect(14, 50, 100, 8, WHITE);
    oled.fillRect(15, 51, prog, 6, WHITE);

    oled.display();
    delay(20);
}'''
},

{
'title': 'TFT-дисплеи и цветная графика',
'order': 3, 'estimated_minutes': 50,
'content': '''
<h2>TFT LCD — цветные дисплеи</h2>
<p>TFT (Thin Film Transistor) LCD — полноцветные дисплеи с SPI интерфейсом. Популярные контроллеры: ILI9341 (240x320, 65K цветов), ST7735 (128x160), ILI9488 (320x480).</p>
''' + table(
    ['Контроллер','Разрешение','Цветов','Шина','Популярный модуль'],
    [
        ['ILI9341','240x320','65536 (RGB565)','SPI / параллельная','2.8" TFT Shield'],
        ['ST7735','128x160','65536','SPI','1.8" Adafruit'],
        ['ST7789','240x240','65536','SPI','1.3" круглый'],
        ['ILI9486','320x480','65536','SPI','3.5" TFT'],
        ['SSD1351','128x128','262144 (RGB666)','SPI','1.5" OLED цветной'],
    ]
) + diagram(
    DEFS + BG.format(h=220) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">RGB565 — формат цвета TFT (16 бит на пиксель)</text>' +
    # Bit fields
    ''.join(box(20+i*38, 50, 36, 35, '#fee2e2','#ef4444',f'R{4-i}',10) for i in range(5)) +
    ''.join(box(210+i*30,50, 28, 35, '#dcfce7','#16a34a',f'G{5-i}',10) for i in range(6)) +
    ''.join(box(390+i*38,50, 36, 35, '#dbeafe','#3b82f6',f'B{4-i}',10) for i in range(5)) +
    '<text x="100" y="105" text-anchor="middle" font-size="11" fill="#dc2626" font-family="sans-serif">5 бит красный (0–31)</text>' +
    '<text x="285" y="105" text-anchor="middle" font-size="11" fill="#15803d" font-family="sans-serif">6 бит зелёный (0–63)</text>' +
    '<text x="490" y="105" text-anchor="middle" font-size="11" fill="#1d4ed8" font-family="sans-serif">5 бит синий (0–31)</text>' +
    box(20,125,580,35,'#fef9c3','#f59e0b','Перевод RGB888 → RGB565: (r>>3)<<11 | (g>>2)<<5 | (b>>3)',11) +
    '<text x="320" y="190" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Готовые константы: ILI9341_RED=0xF800, ILI9341_GREEN=0x07E0, ILI9341_BLUE=0x001F</text>' +
    '<text x="320" y="210" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">240x320 x 2 байта = 150 КБ буфер — НЕ помещается в SRAM AVR! Пишем напрямую в дисплей.</text>',
    640, 220, 'RGB565: 16 бит = 65536 цветов. Нет буфера в RAM — рисуем по-пиксельно через SPI'
) +
tip('Для AVR с 2 КБ SRAM используйте <em>прямую запись</em> в дисплей без буферизации. Adafruit_ILI9341 делает именно это: каждый вызов fillRect() сразу пишет в дисплей по SPI.') +
warn('SPI скорость влияет на FPS: при 8 МГц и 240x320 полное обновление занимает ~150 мс (~6 FPS). Для анимации рисуйте только изменившиеся области.'),
'code_example': '''#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

#define TFT_CS  10
#define TFT_DC   9
#define TFT_RST  8
Adafruit_ILI9341 tft(TFT_CS, TFT_DC, TFT_RST);

// RGB888 → RGB565
uint16_t rgb(uint8_t r, uint8_t g, uint8_t b) {
    return ((r>>3)<<11) | ((g>>2)<<5) | (b>>3);
}

void setup() {
    tft.begin();
    tft.setRotation(1);          // альбомная (320x240)
    tft.fillScreen(ILI9341_BLACK);

    // Градиентный фон
    for (int x = 0; x < 320; x++) {
        uint16_t c = rgb(x*255/320, 50, 255-x*255/320);
        tft.drawFastVLine(x, 0, 40, c);
    }

    tft.setTextColor(ILI9341_WHITE);
    tft.setTextSize(3);
    tft.setCursor(30, 10);
    tft.print("AVR TFT!");

    tft.fillCircle(160, 140, 60, rgb(255,200,0));
    tft.drawCircle(160, 140, 62, ILI9341_WHITE);
    tft.setTextColor(ILI9341_BLACK);
    tft.setTextSize(2);
    tft.setCursor(125, 132);
    tft.print("HELLO");
}

void loop() {}'''
},
],

# ─── МОДУЛЬ 12: ДВИГАТЕЛИ ─────────────────────────────────────────
12: [
{
'title': 'DC-двигатели и H-мост L298N',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>Управление DC-двигателем через H-мост</h2>
<p>DC-двигатель не подключают напрямую к выводу МК — ток до 1–5 А превышает возможности GPIO (40 мА). Используют H-мост: схему из 4 ключей, позволяющую менять направление тока через двигатель.</p>
''' + diagram(
    DEFS + BG.format(h=250) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">H-мост: принцип работы</text>' +
    # H-bridge schematic
    box(20,50,80,35,'#dbeafe','#3b82f6','S1 (Q1)\nвкл',10) +
    box(20,150,80,35,'#fee2e2','#ef4444','S3 (Q3)\nвыкл',10) +
    box(540,50,80,35,'#fee2e2','#ef4444','S2 (Q2)\nвыкл',10) +
    box(540,150,80,35,'#dbeafe','#3b82f6','S4 (Q4)\nвкл',10) +
    '<line x1="100" y1="67" x2="300" y2="67" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="300" y1="67" x2="300" y2="110" stroke="#3b82f6" stroke-width="2"/>' +
    box(250,110,100,40,'#dcfce7','#16a34a','Мотор\nM',13,'bold') +
    '<line x1="300" y1="150" x2="300" y2="167" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="300" y1="167" x2="540" y2="167" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="100" y1="167" x2="200" y2="167" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4"/>' +
    '<line x1="400" y1="167" x2="540" y2="167" stroke="#94a3b8" stroke-width="1"/>' +
    arrow(300,67,300,110,'#3b82f6') + arrow(300,150,300,167,'#ef4444') +
    '<text x="320" y="225" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">S1+S4 вкл → ток слева-направо → вперёд</text>' +
    '<text x="320" y="242" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">S2+S3 вкл → ток справа-налево → назад</text>',
    640, 255, 'H-мост: 4 ключа управляют направлением тока через двигатель'
) +
table(
    ['IN1','IN2','ENA','Двигатель'],
    [
        ['HIGH','LOW','HIGH','Вперёд (полная скорость)'],
        ['LOW','HIGH','HIGH','Назад (полная скорость)'],
        ['HIGH','LOW','PWM','Вперёд (скорость = duty%)'],
        ['LOW','LOW','любой','Свободное вращение (стоп)'],
        ['HIGH','HIGH','любой','Торможение (короткое замыкание)'],
    ]
) +
'''<h3>L298N — готовый модуль H-моста</h3>''' +
table(
    ['Вывод L298N','Подключение к Arduino','Назначение'],
    [
        ['IN1','D4','Направление канал A'],
        ['IN2','D5','Направление канал A'],
        ['ENA','D3 (PWM)','Скорость канал A (ШИМ)'],
        ['IN3','D6','Направление канал B'],
        ['IN4','D7','Направление канал B'],
        ['ENB','D9 (PWM)','Скорость канал B (ШИМ)'],
        ['VIN','Батарея 7–35В','Питание двигателей'],
        ['5V out','—','Встроенный регулятор 5В (если нет jumper)'],
    ]
) +
tip('L298N теряет 1.4–2В на внутренних транзисторах. При питании 6В двигатель получит только 4–4.6В. Для питания 6В двигателей подайте 7.5–8В на VIN.') +
warn('Никогда не подключайте двигатель напрямую к GPIO AVR! Бросок ЭДС при остановке может уничтожить МК. L298N имеет встроенные защитные диоды.'),
'code_example': '''// Управление DC двигателем через L298N
#define IN1 4
#define IN2 5
#define ENA 3   // PWM pin

void motor_forward(uint8_t speed) {  // speed 0-255
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, speed);
}
void motor_backward(uint8_t speed) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, speed);
}
void motor_stop(void) {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);
}
void motor_brake(void) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, HIGH);
}

void setup() {
    pinMode(IN1,OUTPUT); pinMode(IN2,OUTPUT); pinMode(ENA,OUTPUT);
}
void loop() {
    motor_forward(200);  delay(1000);
    motor_stop();        delay(500);
    motor_backward(150); delay(1000);
    motor_brake();       delay(500);
}'''
},

{
'title': 'Сервопривод и ШИМ управление',
'order': 2, 'estimated_minutes': 50,
'content': '''
<h2>Сервоприводы</h2>
<p>Сервопривод — двигатель с обратной связью по положению. Управляется ШИМ-сигналом с периодом <strong>20 мс (50 Гц)</strong>: длительность импульса 1–2 мс задаёт угол поворота 0°–180°.</p>
''' + diagram(
    DEFS + BG.format(h=200) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Управляющий сигнал сервопривода</text>' +
    '<line x1="30" y1="100" x2="610" y2="100" stroke="#94a3b8" stroke-width="1"/>' +
    '<line x1="30" y1="60" x2="30" y2="160" stroke="#94a3b8" stroke-width="1"/>' +
    # 1ms pulse (0°)
    '<line x1="50" y1="100" x2="50" y2="65" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="50" y1="65" x2="100" y2="65" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="100" y1="65" x2="100" y2="100" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="100" y1="100" x2="450" y2="100" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="450" y1="100" x2="450" y2="65" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="450" y1="65" x2="500" y2="65" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="500" y1="65" x2="500" y2="100" stroke="#3b82f6" stroke-width="2.5"/>' +
    '<line x1="500" y1="100" x2="610" y2="100" stroke="#3b82f6" stroke-width="2.5"/>' +
    # Labels
    '<text x="75" y="55" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">1мс=0°</text>' +
    '<text x="475" y="55" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">1мс</text>' +
    '<line x1="50" y1="140" x2="450" y2="140" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5"/>' +
    '<text x="250" y="155" text-anchor="middle" font-size="11" fill="#92400e" font-family="sans-serif">Период = 20 мс (50 Гц)</text>' +
    box(30,170,170,22,'#dcfce7','#16a34a','1.0 мс → 0°',10) +
    box(220,170,170,22,'#fef9c3','#f59e0b','1.5 мс → 90°',10) +
    box(420,170,170,22,'#fee2e2','#ef4444','2.0 мс → 180°',10),
    640, 200, 'Длительность импульса определяет угол: 1.0 мс=0°, 1.5 мс=90°, 2.0 мс=180°'
) +
table(
    ['Тип серво','Угол','Ток (нагрузка)','Момент','Применение'],
    [
        ['SG90 (micro)','0–180°','200–600 мА','1.8 кг·см','Мелкая робототехника'],
        ['MG996R (стандарт)','0–180°','500–900 мА','9.4 кг·см','Машинки, роботы'],
        ['Непрерывное вращение','360°','По нагрузке','—','Колёса роботов'],
    ]
) +
'''<h3>Ручное управление через Timer1 (без Servo.h)</h3>
<p>Timer1 (16 бит) на Fast PWM с ICR1=39999 при предделителе 8 → период = 20 мс:</p>
<p style="background:#f1f5f9;padding:10px;border-radius:8px;font-family:monospace">ICR1 = F_CPU/(prescalerxf) − 1 = 16e6/(8x50) − 1 = 39999</p>
<p>OCR1A = 1000–2000 (мкс) → угол 0°–180°. Формула: <code>OCR1A = 1000 + angle*1000/180</code></p>''' +
tip('Библиотека Arduino Servo.h занимает Timer1. Если используете servo, Timer1 недоступен для других целей (например, точного ШИМ). Подключайте серво к pin 9 или 10.') +
warn('Не питайте серво напрямую от 5В пина Arduino USB! Ток серво под нагрузкой достигает 500–900 мА — USB-порт даёт только 500 мА. Используйте внешний источник питания.'),
'code_example': '''#include <Servo.h>
Servo servo1;

// Плавное движение между позициями
void servo_sweep(Servo &s, int from, int to, int step_ms=15) {
    if (from < to)
        for (int a=from; a<=to; a++) { s.write(a); delay(step_ms); }
    else
        for (int a=from; a>=to; a--) { s.write(a); delay(step_ms); }
}

void setup() {
    servo1.attach(9);   // pin 9 = Timer1 OC1A
    servo1.write(90);   // центр
    delay(500);
}

void loop() {
    servo_sweep(servo1, 90, 0);    // 90° → 0°
    delay(300);
    servo_sweep(servo1, 0, 180);   // 0° → 180°
    delay(300);
    servo_sweep(servo1, 180, 90);  // 180° → 90°
    delay(1000);
}

// Управление потенциометром
void pot_control(void) {
    int pot = analogRead(A0);             // 0-1023
    int angle = map(pot, 0, 1023, 0, 180);
    servo1.write(angle);
}'''
},

{
'title': 'Шаговый двигатель и драйвер A4988',
'order': 3, 'estimated_minutes': 55,
'content': '''
<h2>Шаговые двигатели</h2>
<p>Шаговый двигатель вращается дискретными шагами (обычно 200 шагов/оборот = 1.8°/шаг). Не требует обратной связи — каждый шаг точно позиционирует ротор. Используется в 3D-принтерах, ЧПУ, сканерах.</p>
''' + table(
    ['Тип','Фаз','Провода','Управление','Особенности'],
    [
        ['Однополярный','4','5–6','Простое, одна катушка','Меньший момент, простой драйвер'],
        ['Биполярный','2','4','H-мост на каждую фазу','Больший момент, нужен A4988/DRV8825'],
        ['Гибридный','2','4','A4988, TMC2208','Высокая точность (1/16 шага), 3D-принтеры'],
    ]
) + diagram(
    DEFS + BG.format(h=240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Последовательность шагов биполярного мотора</text>' +
    box(20,50,120,30,'#dbeafe','#3b82f6','Полный шаг (2-фаз)',10) +
    # Step sequence table
    ''.join([
        box(160+i*90,50,85,30,'#dcfce7','#16a34a',f'Шаг {i+1}',10)
        for i in range(4)
    ]) +
    '<text x="80" y="100" text-anchor="middle" font-size="10" fill="#1e293b" font-family="sans-serif">Катушка A+</text>' +
    '<text x="80" y="120" text-anchor="middle" font-size="10" fill="#1e293b" font-family="sans-serif">Катушка A−</text>' +
    '<text x="80" y="140" text-anchor="middle" font-size="10" fill="#1e293b" font-family="sans-serif">Катушка B+</text>' +
    '<text x="80" y="160" text-anchor="middle" font-size="10" fill="#1e293b" font-family="sans-serif">Катушка B−</text>' +
    # Values
    ''.join([
        f'<rect x="{162+i*90}" y="{88+j*20}" width="83" height="18" rx="3" fill="{chr(35)}{"bbf7d0" if v else "fee2e2"}"/>'
        f'<text x="{203+i*90}" y="{101+j*20}" text-anchor="middle" font-size="11" fill="{chr(35)}{"15803d" if v else "991b1b"}" font-family="sans-serif">{"1" if v else "0"}</text>'
        for i,(a,b,c,d) in enumerate([(1,0,0,1),(1,0,1,0),(0,1,1,0),(0,1,0,1)])
        for j,v in enumerate([a,b,c,d])
    ]) +
    box(20,200,580,30,'#fef9c3','#f59e0b','A4988: STEP↑ = один микрошаг. DIR=HIGH/LOW задаёт направление. ENABLE=LOW включает драйвер.',10),
    640, 245, 'Каждый импульс STEP на A4988 = один микрошаг (до 1/16 шага)'
) +
tip('A4988 поддерживает микрошаги: 1, 1/2, 1/4, 1/8, 1/16 — через пины MS1/MS2/MS3. При 1/16 шага мотор NEMA17 даёт 3200 шагов/оборот — плавное и тихое движение.') +
warn('Обязательно установите ток ограничения на A4988 подстроечным резистором (Vref = Ix8xRsense). Перегрев или неправильный ток = потеря шагов или выход из строя драйвера.'),
'code_example': '''// A4988: управление шаговым двигателем
#define STEP_PIN 3
#define DIR_PIN  4
#define EN_PIN   8

void stepper_init(void) {
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN,  OUTPUT);
    pinMode(EN_PIN,   OUTPUT);
    digitalWrite(EN_PIN, LOW);   // включить драйвер
}

// steps>0 = вперёд, steps<0 = назад
void stepper_move(int steps, uint16_t step_us=1000) {
    digitalWrite(DIR_PIN, steps > 0 ? HIGH : LOW);
    steps = abs(steps);
    for (int i = 0; i < steps; i++) {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(step_us);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(step_us);
    }
}

// Трапециевидный разгон (ускорение + постоянная скорость + торможение)
void stepper_accel(int total, int min_us=500, int max_us=2000) {
    int ramp = total / 3;
    for (int i = 0; i < total; i++) {
        int us;
        if      (i < ramp)          us = map(i, 0, ramp, max_us, min_us);
        else if (i > total - ramp)  us = map(i, total-ramp, total, min_us, max_us);
        else                        us = min_us;
        digitalWrite(STEP_PIN, HIGH); delayMicroseconds(us);
        digitalWrite(STEP_PIN, LOW);  delayMicroseconds(us);
    }
}

void setup() { stepper_init(); }
void loop()  {
    stepper_accel(3200);  // 1 оборот с разгоном
    delay(500);
    stepper_accel(-3200);
    delay(500);
}'''
},
],

# ─── МОДУЛЬ 13: СОН И ПИТАНИЕ ─────────────────────────────────────
13: [
{
'title': 'Watchdog Timer (WDT)',
'order': 1, 'estimated_minutes': 50,
'content': '''
<h2>Watchdog Timer — сторожевой таймер</h2>
<p>WDT — независимый таймер на отдельном RC-генераторе (~128 кГц). Если программа не сбрасывает его вовремя (зависла), WDT перезагружает МК. Также используется для периодического пробуждения из режима сна.</p>
''' + diagram(
    DEFS + BG.format(h=220) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Watchdog: нормальная работа vs зависание</text>' +
    # Normal
    box(20,50,280,150,'#dcfce7','#16a34a','Нормальная работа',12,'bold') +
    '<text x="160" y="90" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">loop() выполняется каждые 200 мс</text>' +
    '<text x="160" y="108" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">wdt_reset() сбрасывает счётчик</text>' +
    '<text x="160" y="126" text-anchor="middle" font-size="10" fill="#14532d" font-family="sans-serif">WDT timeout = 1 сек</text>' +
    '<text x="160" y="148" text-anchor="middle" font-size="10" fill="#15803d" font-family="sans-serif">✓ Перезагрузки нет</text>' +
    # Hung
    box(340,50,280,150,'#fee2e2','#ef4444','Зависание программы',12,'bold') +
    '<text x="480" y="90" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">loop() застряла в ожидании</text>' +
    '<text x="480" y="108" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">wdt_reset() не вызывается</text>' +
    '<text x="480" y="126" text-anchor="middle" font-size="10" fill="#7f1d1d" font-family="sans-serif">WDT считает до timeout</text>' +
    '<text x="480" y="148" text-anchor="middle" font-size="10" fill="#dc2626" font-family="sans-serif">→ RESET! МК перезагружается</text>' +
    '<text x="320" y="215" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">WDT работает от независимого 128 кГц RC-генератора — не зависит от тактовой МК</text>',
    640, 225, 'Watchdog: защита от зависания. Не сбросил — получи перезагрузку'
) +
table(
    ['WDTO_xxx','Время','Применение'],
    [
        ['WDTO_15MS','15 мс','Очень критичные системы'],
        ['WDTO_120MS','120 мс','Быстрые циклы'],
        ['WDTO_500MS','500 мс','Стандартная защита'],
        ['WDTO_1S','1 сек','Основное применение'],
        ['WDTO_4S','4 сек','Медленные системы'],
        ['WDTO_8S','8 сек','Сон + редкие пробуждения'],
    ]
) +
info('WDT можно использовать в двух режимах: <b>Reset mode</b> (перезагрузка при истечении) и <b>Interrupt mode</b> (сначала прерывание, затем перезагрузка). Второй режим используют для сна.') +
warn('После перезагрузки по WDT флаг WDRF в регистре MCUSR устанавливается в 1. Проверяйте его в начале программы чтобы знать причину перезагрузки — WDT или RESET.'),
'code_example': '''#include <avr/wdt.h>

void setup() {
    // Проверить причину сброса
    uint8_t mcusr = MCUSR;
    MCUSR = 0;
    wdt_disable();  // ВАЖНО: сразу отключить WDT после сброса

    Serial.begin(9600);
    if (mcusr & (1<<WDRF)) Serial.println("WDT reset!");
    if (mcusr & (1<<PORF)) Serial.println("Power-on reset");

    // Включить WDT с таймаутом 2 секунды
    wdt_enable(WDTO_2S);
    Serial.println("WDT enabled, timeout=2s");
}

void loop() {
    // Сброс WDT в начале каждой итерации
    wdt_reset();

    // Имитация работы
    Serial.println("Working...");
    delay(500);

    // Раскомментируйте чтобы проверить WDT:
    // delay(3000);  // зависание → WDT сбросит через 2с
}'''
},

{
'title': 'Режимы сна AVR',
'order': 2, 'estimated_minutes': 55,
'content': '''
<h2>Режимы сна — экономия энергии</h2>
<p>ATmega328P поддерживает 6 режимов сна. В режиме Power-down потребление падает с ~15 мА до <strong>0.1–1 мкА</strong> — принципиально важно для батарейных устройств.</p>
''' + table(
    ['Режим','Потребление','Что работает','Пробуждение'],
    [
        ['Idle','~6 мА','Таймеры, UART, SPI, I2C','Любое прерывание'],
        ['ADC Noise Reduction','~1 мА','АЦП, некоторые прерывания','АЦП, INT0, TWI, WDT'],
        ['Power-save','~1 мкА','Timer2, RTC','Timer2, INT, TWI, WDT'],
        ['Power-down','~0.1 мкА','Только WDT, INT','INT0/INT1, PCINT, TWI, WDT'],
        ['Standby','~0.1 мкА','Генератор (быстрый старт)','Как Power-down'],
        ['Extended Standby','~1 мкА','Генератор + Timer2','Как Power-save'],
    ]
) + diagram(
    DEFS + BG.format(h=230) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Цикл сон–пробуждение (Power-down + WDT)</text>' +
    box(20,55,130,40,'#dcfce7','#16a34a','Активная\nработа\n~15 мА',11) +
    arrow(150,75,190,75) +
    box(190,55,130,40,'#fef9c3','#f59e0b','Подготовка\nк сну\n(sei, sleep)',11) +
    arrow(320,75,360,75) +
    box(360,55,130,40,'#dbeafe','#3b82f6','СОН\nPower-down\n0.1 мкА',11,'bold') +
    arrow(490,75,530,75) +
    box(530,55,90,40,'#fee2e2','#ef4444','WDT ISR\nпробужд.',11) +
    # Loop arrow back
    '<path d="M 575,95 Q 575,160 300,160 Q 25,160 25,95" stroke="#94a3b8" stroke-width="1.5" fill="none" stroke-dasharray="6,3"/>' +
    arrow(25,95,20,85,'#94a3b8') +
    '<text x="300" y="178" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Цикл повторяется: пробудился → выполнил работу → снова спать</text>' +
    # Current bar chart
    box(30,195,80,25,'#ef4444','#dc2626','15 мА',10,'bold','white') +
    box(200,210,80,10,'#f59e0b','#d97706','1 мА',9,'normal','white') +
    box(370,218,80,2,'#3b82f6','#2563eb','0.1 мкА',8,'normal','white') +
    '<text x="70" y="228" text-anchor="middle" font-size="9" fill="#64748b" font-family="sans-serif">Активный</text>' +
    '<text x="240" y="228" text-anchor="middle" font-size="9" fill="#64748b" font-family="sans-serif">Idle</text>' +
    '<text x="410" y="228" text-anchor="middle" font-size="9" fill="#64748b" font-family="sans-serif">Power-down</text>',
    640, 235, 'Power-down: экономия 150000x. Батарея AA вместо часов — месяцы!'
) +
tip('Расчёт времени работы: CR2032 = 220 мАч. При 15 мА активности и 99% времени во сне средний ток ≈ 0.15 мА + 0.01x15 = 0.30 мА. Время = 220/0.30 = 730 часов ≈ 30 дней.') +
warn('Перед сном убедитесь что UART закончил передачу (Serial.flush()). Уход в сон во время передачи может повредить данные.'),
'code_example': '''#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>

volatile bool woke = false;

ISR(WDT_vect) {
    woke = true;   // просто устанавливаем флаг
}

void setup_wdt_8s(void) {
    cli();
    MCUSR &= ~(1<<WDRF);
    // Включить WDT в режиме прерывания, 8 сек
    WDTCSR |= (1<<WDCE)|(1<<WDE);
    WDTCSR  = (1<<WDIE)|(1<<WDP3)|(1<<WDP0);  // interrupt, 8s
    sei();
}

void go_sleep(void) {
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    sleep_enable();
    sleep_cpu();        // ← спим здесь
    sleep_disable();    // ← просыпаемся здесь
}

void setup() {
    Serial.begin(9600);
    setup_wdt_8s();
}

void loop() {
    // Работаем
    Serial.println("Awake! Doing work...");
    Serial.flush();

    // Засыпаем до следующего WDT (8 сек)
    woke = false;
    go_sleep();

    // Сюда попадаем после WDT прерывания
    if (woke) Serial.println("WDT wakeup");
}'''
},

{
'title': 'Батарейное питание и оптимизация тока',
'order': 3, 'estimated_minutes': 45,
'content': '''
<h2>Практические советы для батарейных устройств</h2>
''' + table(
    ['Приём','Экономия','Как реализовать'],
    [
        ['Power-down сон','99%+','sleep.h + WDT/прерывания'],
        ['Снизить F_CPU','До 8x','8 МГц вместо 16 МГц (fuse bits)'],
        ['Отключить ADC','0.3 мА','ADCSRA &= ~(1<<ADEN)'],
        ['Отключить BOD во сне','0.025 мА','sleep_bod_disable() перед sleep'],
        ['Отключить UART','0.5 мА','UCSR0B = 0 (отключить TX/RX)'],
        ['Отключить SPI/I2C','0.1 мА','PRR |= (1<<PRTWI)|(1<<PRSPI)'],
        ['Подтяжки входов','~0.1 мА','Не оставлять входы висящими'],
        ['Светодиоды','10–20 мА','Не оставлять включёнными в сне'],
    ]
) + diagram(
    DEFS + BG.format(h=200) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Сравнение источников питания</text>' +
    box(20,50,130,130,'#dcfce7','#16a34a','AA (1.5В)\n2700 мАч\nНеперезар.',11) +
    box(170,50,130,130,'#dbeafe','#3b82f6','AAA (1.5В)\n1200 мАч\nНеперезар.',11) +
    box(320,50,130,130,'#fef9c3','#f59e0b','LiPo 3.7В\n500–3000\nмАч, перез.',11) +
    box(470,50,130,130,'#fdf4ff','#a855f7','CR2032 3В\n220 мАч\n«таблетка»',11) +
    '<text x="85" y="195" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Мин. 0.9В→нужен DC-DC</text>' +
    '<text x="235" y="195" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Мин. 0.9В</text>' +
    '<text x="385" y="195" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Прямо к AVR 3.3В</text>' +
    '<text x="535" y="195" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">Мало тока!</text>',
    640, 205, 'Выбор источника зависит от тока потребления и размера устройства'
) +
tip('Два элемента AA + повышающий DC-DC MCP1640 (3.3В/300 мА) — оптимальная связка для IoT узлов на АВР. Ёмкость 2700 мАч x КПД 90% = 2430 мАч @3.3В.') +
warn('AVR не работает ниже 1.8В (ATmega328P) или 2.7В (без Low Voltage версии). При питании от батарей добавьте схему контроля разряда через АЦП или компаратор.'),
'code_example': '''#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/wdt.h>

// Максимальная экономия: отключить всю периферию
void power_down_all(void) {
    // Отключить все периферийные блоки через PRR
    power_all_disable();     // ADC, SPI, USART, TWI, Timer1, Timer2
    power_timer0_enable();   // Timer0 нужен для millis (если используем)

    // Отключить ADC отдельно (power_all_disable может не хватить)
    ADCSRA &= ~(1<<ADEN);
}

// Минимальная настройка GPIO (не оставлять висячих входов)
void gpio_minimize(void) {
    // Все выводы — входы с pull-up (меньше тока чем Hi-Z)
    DDRB = DDRC = DDRD = 0x00;
    PORTB = PORTC = PORTD = 0xFF;
    // Только то, что реально нужно — переопределить
    DDRB |= (1<<PB5);    // LED выход
    PORTB &= ~(1<<PB5);  // LED выключен
}

void ultra_sleep_8s(void) {
    power_down_all();
    // BOD disable во сне (сохранить 0.025 мА)
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    cli();
    sleep_enable();
    sleep_bod_disable();  // только ATmega328P!
    sei();
    sleep_cpu();
    sleep_disable();
    power_all_enable();
    ADCSRA |= (1<<ADEN); // включить обратно если нужен АЦП
}'''
},
],

# ─── МОДУЛЬ 14: 1-WIRE И DS18B20 ─────────────────────────────────
14: [
{
'title': 'Протокол 1-Wire и датчик DS18B20',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>1-Wire — однопроводной протокол Dallas</h2>
<p>1-Wire (разработан Dallas Semiconductor) передаёт данные, питание и тактовую частоту по <strong>одному проводу</strong>. Мастер — МК, ведомые — датчики температуры DS18B20, ключи iButton и др. Каждое устройство имеет уникальный 64-битный ROM-код.</p>
''' + diagram(
    DEFS + BG.format(h=220) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Тайм-слоты 1-Wire протокола</text>' +
    '<line x1="20" y1="90" x2="620" y2="90" stroke="#94a3b8" stroke-width="1"/>' +
    '<text x="15" y="85" font-size="10" fill="#64748b" font-family="sans-serif">HIGH</text>' +
    '<text x="15" y="115" font-size="10" fill="#64748b" font-family="sans-serif">LOW</text>' +
    # Reset pulse
    '<text x="80" y="55" text-anchor="middle" font-size="10" fill="#ef4444" font-family="sans-serif">RESET (480 мкс LOW)</text>' +
    '<line x1="30" y1="90" x2="30" y2="130" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="30" y1="130" x2="160" y2="130" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="160" y1="130" x2="160" y2="90" stroke="#ef4444" stroke-width="2"/>' +
    # Presence pulse
    '<text x="215" y="55" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">PRESENCE (60 мкс)</text>' +
    '<line x1="160" y1="90" x2="190" y2="90" stroke="#1e293b" stroke-width="2"/>' +
    '<line x1="190" y1="90" x2="190" y2="115" stroke="#16a34a" stroke-width="2"/>' +
    '<line x1="190" y1="115" x2="260" y2="115" stroke="#16a34a" stroke-width="2"/>' +
    '<line x1="260" y1="115" x2="260" y2="90" stroke="#16a34a" stroke-width="2"/>' +
    # Write 1
    '<text x="320" y="55" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">Write 1 (1-15 мкс LOW)</text>' +
    '<line x1="300" y1="90" x2="300" y2="115" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="300" y1="115" x2="315" y2="115" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="315" y1="115" x2="315" y2="90" stroke="#3b82f6" stroke-width="2"/>' +
    '<line x1="315" y1="90" x2="370" y2="90" stroke="#3b82f6" stroke-width="2"/>' +
    # Write 0
    '<text x="440" y="55" text-anchor="middle" font-size="10" fill="#f59e0b" font-family="sans-serif">Write 0 (60+ мкс LOW)</text>' +
    '<line x1="400" y1="90" x2="400" y2="115" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="400" y1="115" x2="500" y2="115" stroke="#f59e0b" stroke-width="2"/>' +
    '<line x1="500" y1="115" x2="500" y2="90" stroke="#f59e0b" stroke-width="2"/>' +
    '<text x="320" y="175" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">Подтягивающий резистор 4.7 кОм: шина в HIGH по умолчанию</text>' +
    '<text x="320" y="195" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">«Паразитное питание»: DS18B20 питается от шины через конденсатор</text>',
    640, 210, '1-Wire: мастер тянет шину LOW на разное время → логика 0 или 1'
) +
'''<h3>DS18B20 — цифровой датчик температуры</h3>''' +
table(
    ['Параметр','Значение'],
    [
        ['Диапазон','−55°C … +125°C'],
        ['Точность','±0.5°C в диапазоне −10°C…+85°C'],
        ['Разрядность','9–12 бит (0.5°C / 0.25°C / 0.125°C / 0.0625°C)'],
        ['Время преобразования','94 мс (9 бит) … 750 мс (12 бит)'],
        ['Напряжение питания','3.0–5.5В или паразитное (от шины)'],
        ['ROM-код','64-битный уникальный номер (семейный код 0x28)'],
    ]
) +
tip('На одной шине 1-Wire можно подключить десятки DS18B20. Мастер опрашивает каждый по уникальному ROM-коду командой MATCH ROM или все сразу командой SKIP ROM (если один датчик).') +
warn('При паразитном питании для команды Convert T нужна сильная подтяжка (transistor pull-up) — 4.7 кОм недостаточно. При нормальном питании (3 провода) этой проблемы нет.'),
'code_example': '''#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_PIN 2
OneWire oneWire(ONE_WIRE_PIN);
DallasTemperature sensors(&oneWire);

void setup() {
    Serial.begin(9600);
    sensors.begin();

    // Сколько датчиков найдено
    int count = sensors.getDeviceCount();
    Serial.print("Датчиков: "); Serial.println(count);

    // Установить разрядность 12 бит для всех
    sensors.setResolution(12);
    sensors.setWaitForConversion(false);  // неблокирующий режим
}

void loop() {
    sensors.requestTemperatures();  // запустить преобразование
    delay(750);                     // ждём 12-бит конверсию

    float t0 = sensors.getTempCByIndex(0);
    float t1 = sensors.getTempCByIndex(1);

    Serial.print("T0="); Serial.print(t0, 2);
    Serial.print("°C  T1="); Serial.print(t1, 2);
    Serial.println("°C");

    // Прямая работа с протоколом (без библиотеки)
    // oneWire.reset();
    // oneWire.write(0xCC);  // SKIP ROM
    // oneWire.write(0x44);  // Convert T
    delay(1000);
}'''
},

{
'title': 'Многодатчиковые системы 1-Wire',
'order': 2, 'estimated_minutes': 45,
'content': '''
<h2>Несколько DS18B20 на одной шине</h2>
<p>Протокол 1-Wire позволяет подключить десятки датчиков на один пин МК. Каждый датчик идентифицируется 64-битным ROM-кодом, записанным при производстве.</p>
''' + table(
    ['Команда ROM','Байт','Назначение'],
    [
        ['SEARCH ROM','0xF0','Перечислить все устройства на шине'],
        ['READ ROM','0x33','Прочитать ROM одного устройства (если оно одно)'],
        ['MATCH ROM','0x55','Выбрать конкретное устройство по ROM-коду'],
        ['SKIP ROM','0xCC','Адресовать все устройства (broadcast)'],
        ['ALARM SEARCH','0xEC','Найти датчики с сработавшей тревогой'],
    ]
) + diagram(
    DEFS + BG.format(h=210) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Три DS18B20 на одной шине</text>' +
    box(20,60,100,40,'#dbeafe','#3b82f6','Arduino\npin 2',11,'bold') +
    '<line x1="120" y1="80" x2="180" y2="80" stroke="#1e293b" stroke-width="2.5"/>' +
    '<line x1="180" y1="50" x2="180" y2="170" stroke="#1e293b" stroke-width="2.5"/>' +
    '<line x1="150" y1="55" x2="180" y2="55" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3"/>' +
    '<text x="140" y="52" text-anchor="end" font-size="9" fill="#ef4444" font-family="sans-serif">4.7k</text>' +
    '<line x1="120" y1="55" x2="150" y2="55" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3"/>' +
    box(210,50,110,40,'#dcfce7','#16a34a','DS18B20 #1\n28:AA:11:22',9) +
    '<line x1="180" y1="75" x2="210" y2="70" stroke="#1e293b" stroke-width="1.5"/>' +
    box(210,110,110,40,'#fef9c3','#f59e0b','DS18B20 #2\n28:BB:33:44',9) +
    '<line x1="180" y1="115" x2="210" y2="130" stroke="#1e293b" stroke-width="1.5"/>' +
    box(210,165,110,35,'#fdf4ff','#a855f7','DS18B20 #3\n28:CC:55:66',9) +
    '<line x1="180" y1="160" x2="210" y2="182" stroke="#1e293b" stroke-width="1.5"/>' +
    '<text x="430" y="80" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">SKIP ROM → Convert T</text>' +
    '<text x="430" y="98" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">все датчики преобразуют</text>' +
    '<text x="430" y="120" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">MATCH ROM [28:AA:11:22]</text>' +
    '<text x="430" y="138" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">→ READ SCRATCHPAD</text>' +
    '<text x="430" y="158" text-anchor="middle" font-size="11" fill="#64748b" font-family="sans-serif">получаем температуру #1</text>',
    640, 215, 'Все датчики на одном проводе; опрашиваем по очереди через ROM-код'
) +
tip('ROM-коды удобно хранить в EEPROM МК или в массиве Flash. Функция <code>sensors.getAddress(addr, index)</code> возвращает ROM-код датчика с индексом index.') +
warn('Длина шины 1-Wire: до 30–50 м при 4.7 кОм подтяжке. При большой длине уменьшайте подтяжку (2.2 кОм) или используйте активный драйвер DS2480B.'),
'code_example': '''#include <OneWire.h>
#include <DallasTemperature.h>

OneWire ow(2);
DallasTemperature dt(&ow);

// Хранить адреса датчиков
DeviceAddress addr[8];
int sensor_count;

void setup() {
    Serial.begin(9600);
    dt.begin();
    sensor_count = dt.getDeviceCount();

    // Запомнить адреса
    for (int i = 0; i < sensor_count; i++) {
        dt.getAddress(addr[i], i);
        Serial.print("Sensor "); Serial.print(i);
        Serial.print(": ");
        for (int b = 0; b < 8; b++) {
            Serial.print(addr[i][b], HEX);
            if (b < 7) Serial.print(":");
        }
        Serial.println();
    }
    dt.setResolution(12);
}

void loop() {
    dt.requestTemperatures();
    delay(750);

    for (int i = 0; i < sensor_count; i++) {
        float t = dt.getTempC(addr[i]);
        Serial.print("T"); Serial.print(i);
        Serial.print("="); Serial.print(t, 1);
        Serial.print("C  ");
    }
    Serial.println();
    delay(2000);
}'''
},

{
'title': 'Введение в CAN-шину',
'order': 3, 'estimated_minutes': 50,
'content': '''
<h2>CAN — Controller Area Network</h2>
<p>CAN — промышленный протокол для надёжной связи между МК в условиях помех. Применяется в автомобилях, промышленных системах, медицинском оборудовании. Разработан Bosch (1983).</p>
''' + table(
    ['Параметр','Значение'],
    [
        ['Скорость','До 1 Мбит/с (1 Мбит/с при длине ≤ 40 м)'],
        ['Топология','Шина с терминирующими резисторами 120 Ом'],
        ['Провода','Дифференциальная пара: CANH, CANL'],
        ['Узлов','До 127 на одной шине'],
        ['Обнаружение ошибок','CRC, ACK, bit stuffing, frame check'],
        ['Приоритеты','Выигрывает кадр с меньшим ID (битовый арбитраж)'],
    ]
) + diagram(
    DEFS + BG.format(h=220) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Структура стандартного CAN кадра (11-bit ID)</text>' +
    box(20,55,30,40,'#dbeafe','#3b82f6','SOF',9) +
    box(55,55,55,40,'#dcfce7','#16a34a','ID\n11 бит',9) +
    box(115,55,25,40,'#fef9c3','#f59e0b','RTR',9) +
    box(145,55,25,40,'#fdf4ff','#a855f7','IDE\nRES',8) +
    box(175,55,35,40,'#fee2e2','#ef4444','DLC\n4 бит',9) +
    box(215,55,200,40,'#dcfce7','#16a34a','Данные 0–8 байт',11) +
    box(420,55,80,40,'#dbeafe','#3b82f6','CRC\n15 бит',9) +
    box(505,55,30,40,'#fef9c3','#f59e0b','ACK',9) +
    box(540,55,40,40,'#fee2e2','#ef4444','EOF\n7 бит',9) +
    '<text x="320" y="120" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">SOF=Start of Frame, RTR=Remote Transmission Request, DLC=Data Length Code</text>' +
    # Topology
    '<line x1="40" y1="160" x2="600" y2="160" stroke="#1e293b" stroke-width="3"/>' +
    '<text x="40" y="150" font-size="10" fill="#ef4444" font-family="sans-serif">120Ω</text>' +
    '<text x="570" y="150" font-size="10" fill="#ef4444" font-family="sans-serif">120Ω</text>' +
    ''.join(box(80+i*130, 170, 90, 35, '#dbeafe','#3b82f6', f'MCP2515\nNode {i+1}',9) for i in range(4)) +
    ''.join(f'<line x1="{125+i*130}" y1="160" x2="{125+i*130}" y2="170" stroke="#1e293b" stroke-width="1.5"/>' for i in range(4)),
    640, 225, 'CAN: дифференциальная шина с арбитражем по приоритету ID'
) +
info('Для Arduino CAN доступен через модуль MCP2515 (SPI интерфейс). Он содержит CAN-контроллер и трансивер TJA1050. Библиотека: <strong>mcp_can</strong> или <strong>arduino-CAN</strong>.') +
tip('CAN отличается от SPI/I2C принципом арбитража: если два узла начинают передавать одновременно, выигрывает тот, у кого меньше ID. Никаких коллизий и потерь данных.') +
warn('ATmega328P не имеет встроенного CAN. Нужен внешний контроллер MCP2515 (SPI). Встроенный CAN есть в AT90CAN, STM32, dsPIC, ESP32 (TWAI).'),
'code_example': '''// MCP2515 + TJA1050: CAN шина с Arduino
#include <mcp_can.h>
#include <SPI.h>

MCP_CAN can(10);  // CS = pin 10

void setup() {
    Serial.begin(115200);
    if (can.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) != CAN_OK) {
        Serial.println("CAN init FAIL");
        while(1);
    }
    can.setMode(MCP_NORMAL);
    Serial.println("CAN OK @ 500 kbps");
}

void loop() {
    // Отправка кадра: ID=0x123, 4 байта данных
    uint8_t data[4] = {0x10, 0x20, 0x30, 0x40};
    can.sendMsgBuf(0x123, 0, 4, data);  // ID, ext, len, data

    // Приём
    uint32_t id; uint8_t len, buf[8];
    if (can.checkReceive() == CAN_MSGAVAIL) {
        can.readMsgBuf(&id, &len, buf);
        Serial.print("ID: 0x"); Serial.print(id, HEX);
        Serial.print(" Data: ");
        for (int i=0; i<len; i++) {
            Serial.print(buf[i], HEX); Serial.print(" ");
        }
        Serial.println();
    }
    delay(100);
}'''
},
],

# ─── МОДУЛЬ 15: ПАТТЕРНЫ ──────────────────────────────────────────
15: [
{
'title': 'Конечные автоматы (FSM) в МК',
'order': 1, 'estimated_minutes': 55,
'content': '''
<h2>Конечный автомат — FSM</h2>
<p>Конечный автомат (Finite State Machine) — модель программы как набора <strong>состояний</strong> и <strong>переходов</strong> между ними по событиям. Идеально подходит для МК: чётко структурирует поведение, устраняет «лапшу» из if/else и флагов.</p>
''' + diagram(
    DEFS + BG.format(h=240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">FSM: светофор</text>' +
    box(60,60,110,45,'#fee2e2','#ef4444','RED\n(Красный)',12,'bold','#7f1d1d') +
    box(265,60,110,45,'#fef9c3','#f59e0b','YELLOW\n(Жёлтый)',12,'bold','#78350f') +
    box(465,60,110,45,'#dcfce7','#16a34a','GREEN\n(Зелёный)',12,'bold','#14532d') +
    arrow(170,82,265,82) +
    '<text x="218" y="75" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">5с истекло</text>' +
    arrow(375,82,465,82) +
    '<text x="420" y="75" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">2с истекло</text>' +
    # Green to Yellow back
    '<path d="M 520,105 Q 520,165 320,165 Q 120,165 115,105" stroke="#64748b" stroke-width="1.5" fill="none"/>' +
    arrow(115,105,115,107,'#64748b') +
    '<text x="320" y="180" text-anchor="middle" font-size="10" fill="#64748b" font-family="sans-serif">4с истекло → (через Yellow)</text>' +
    # State details
    box(20,200,175,30,'#fee2e2','#ef4444','RED: LED_R=ON, 5 сек',10) +
    box(233,200,175,30,'#fef9c3','#f59e0b','YELLOW: LED_Y=ON, 2 сек',10) +
    box(445,200,175,30,'#dcfce7','#16a34a','GREEN: LED_G=ON, 4 сек',10),
    640, 240, 'FSM: каждое состояние — отдельная логика; переход по событию'
) +
table(
    ['Элемент FSM','В коде МК','Пример'],
    [
        ['Состояние','enum State','STATE_RED, STATE_GREEN…'],
        ['Текущее состояние','static/global переменная','State current = STATE_RED'],
        ['Событие','Условие в loop()','millis()-t0 >= timeout'],
        ['Переход','Присваивание нового состояния','current = STATE_GREEN'],
        ['Действие при входе','Код при смене состояния','digitalWrite(LED_G, HIGH)'],
        ['Действие при выходе','Код перед сменой','digitalWrite(LED_R, LOW)'],
    ]
) +
tip('FSM легко расширять: добавляете новое состояние в enum и описываете переходы. Никаких изменений в остальном коде — принцип Open/Closed.') +
warn('Не путайте FSM с «большим switch в loop()». Правильный FSM явно хранит состояние, обрабатывает каждое состояние независимо и не имеет скрытых взаимозависимостей.'),
'code_example': '''#include <Arduino.h>

enum State { RED, YELLOW_TO_GREEN, GREEN, YELLOW_TO_RED };
State state = RED;
uint32_t state_timer = 0;

const uint16_t TIMEOUT[] = { 5000, 2000, 4000, 2000 };
const uint8_t  LED_PIN[] = { 4, 5, 6, 5 };  // R, Y, G, Y

void enter_state(State s) {
    // Выключить все светофорные огни
    digitalWrite(4, LOW); digitalWrite(5, LOW); digitalWrite(6, LOW);
    // Включить нужный
    digitalWrite(LED_PIN[s], HIGH);
    state_timer = millis();
    state = s;
    Serial.print("→ State: "); Serial.println(s);
}

void setup() {
    Serial.begin(9600);
    pinMode(4,OUTPUT); pinMode(5,OUTPUT); pinMode(6,OUTPUT);
    enter_state(RED);
}

void loop() {
    if (millis() - state_timer >= TIMEOUT[state]) {
        // Переход к следующему состоянию
        enter_state((State)((state + 1) % 4));
    }
    // Остальной код программы работает здесь без блокирования
}'''
},

{
'title': 'Антидребезг и паттерн Button',
'order': 2, 'estimated_minutes': 45,
'content': '''
<h2>Дребезг контактов кнопки</h2>
<p>При нажатии механической кнопки контакты несколько миллисекунд «дребезжат» — замыкаются и размыкаются несколько раз. МК воспринимает это как множество нажатий. Нужна программная (или аппаратная) фильтрация.</p>
''' + diagram(
    DEFS + BG.format(h=210) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Дребезг кнопки при нажатии</text>' +
    '<line x1="20" y1="90" x2="620" y2="90" stroke="#94a3b8" stroke-width="1"/>' +
    '<text x="15" y="75" font-size="9" fill="#64748b" font-family="sans-serif">HIGH</text>' +
    '<text x="15" y="115" font-size="9" fill="#64748b" font-family="sans-serif">LOW</text>' +
    # Ideal
    '<line x1="30" y1="75" x2="170" y2="75" stroke="#16a34a" stroke-width="2"/>' +
    '<line x1="170" y1="75" x2="170" y2="110" stroke="#16a34a" stroke-width="2"/>' +
    '<line x1="170" y1="110" x2="400" y2="110" stroke="#16a34a" stroke-width="2"/>' +
    '<text x="200" y="65" font-size="10" fill="#16a34a" font-family="sans-serif">Идеальный сигнал</text>' +
    # Real (bouncy)
    '<line x1="30" y1="145" x2="170" y2="145" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="170" y1="145" x2="170" y2="165" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="170" y1="165" x2="185" y2="165" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="185" y1="165" x2="185" y2="145" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="185" y1="145" x2="195" y2="145" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="195" y1="145" x2="195" y2="165" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="195" y1="165" x2="210" y2="165" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="210" y1="165" x2="210" y2="145" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="210" y1="145" x2="220" y2="145" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="220" y1="145" x2="220" y2="165" stroke="#ef4444" stroke-width="2"/>' +
    '<line x1="220" y1="165" x2="400" y2="165" stroke="#ef4444" stroke-width="2"/>' +
    '<text x="200" y="135" font-size="10" fill="#ef4444" font-family="sans-serif">Реальный (дребезг)</text>' +
    '<rect x="168" y="130" width="55" height="50" rx="3" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4"/>' +
    '<text x="196" y="195" text-anchor="middle" font-size="10" fill="#92400e" font-family="sans-serif">↑ зона дребезга 5–50 мс</text>',
    640, 210, 'Реальная кнопка при нажатии — несколько ложных срабатываний в зоне дребезга'
) +
table(
    ['Метод','Сложность','Надёжность','Описание'],
    [
        ['Задержка delay()','Простой','Средняя','Ждать 50 мс — блокирует программу'],
        ['millis() дебаунс','Средний','Хорошая','Неблокирующий таймер'],
        ['Счётчик стабильности','Средний','Отличная','N подряд одинаковых значений'],
        ['Аппаратный RC + триггер','Сложный','Отличная','Конденсатор + триггер Шмитта'],
    ]
) +
tip('Класс Button с millis()-debounce — лучший выбор для большинства проектов. Он неблокирующий, надёжно определяет нажатие/отпускание и легко масштабируется на много кнопок.') +
warn('Время дребезга зависит от типа кнопки: тактовые (5–10 мс), кнопки на плате (20–50 мс), геркон (до 100 мс). Устанавливайте таймаут исходя из конкретного компонента.'),
'code_example': '''// Универсальный класс кнопки с антидребезгом
class Button {
    uint8_t  pin;
    uint16_t debounce_ms;
    bool     state, last_read, pressed_event, released_event;
    uint32_t last_change;

public:
    Button(uint8_t p, uint16_t d=30)
        : pin(p), debounce_ms(d), state(false),
          last_read(false), pressed_event(false),
          released_event(false), last_change(0) {
        pinMode(pin, INPUT_PULLUP);
    }

    void update() {
        pressed_event = released_event = false;
        bool read = !digitalRead(pin);   // активный LOW

        if (read != last_read) {
            last_change = millis();
            last_read = read;
        }
        if (millis() - last_change >= debounce_ms && read != state) {
            state = read;
            if (state) pressed_event  = true;
            else       released_event = true;
        }
    }

    bool isPressed()  const { return state; }
    bool wasPressed() const { return pressed_event; }
    bool wasReleased()const { return released_event; }
};

Button btn1(2), btn2(3);
uint8_t counter = 0;

void setup() { Serial.begin(9600); }

void loop() {
    btn1.update(); btn2.update();

    if (btn1.wasPressed())  { counter++; Serial.println(counter); }
    if (btn2.wasPressed())  { counter--; Serial.println(counter); }
    if (btn1.isPressed() && btn2.isPressed()) {
        counter = 0; Serial.println("Reset!");
    }
}'''
},

{
'title': 'Планировщик задач для МК',
'order': 3, 'estimated_minutes': 50,
'content': '''
<h2>Кооперативный планировщик задач</h2>
<p>Полноценная RTOS (FreeRTOS) избыточна для многих МК-проектов. Простой кооперативный планировщик на millis() решает 90% задач: каждая «задача» — функция, вызываемая с заданным периодом.</p>
''' + diagram(
    DEFS + BG.format(h=240) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Временная диаграмма планировщика</text>' +
    '<line x1="30" y1="200" x2="610" y2="200" stroke="#94a3b8" stroke-width="1.5"/>' +
    '<text x="20" y="198" font-size="9" fill="#64748b" font-family="sans-serif">0</text>' +
    ''.join(f'<line x1="{30+i*95}" y1="195" x2="{30+i*95}" y2="205" stroke="#94a3b8" stroke-width="1"/><text x="{30+i*95}" y="215" text-anchor="middle" font-size="9" fill="#64748b" font-family="sans-serif">{i*100}мс</text>' for i in range(1,7)) +
    # Task A (100ms)
    ''.join(f'<rect x="{30+i*95}" y="50" width="18" height="20" rx="3" fill="#3b82f6" opacity="0.85"/>' for i in range(6)) +
    '<text x="15" y="63" font-size="9" fill="#3b82f6" font-family="sans-serif">A</text>' +
    '<text x="330" y="45" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="sans-serif">Задача A: каждые 100 мс (датчики)</text>' +
    # Task B (500ms)
    ''.join(f'<rect x="{30+i*475}" y="90" width="25" height="20" rx="3" fill="#16a34a" opacity="0.85"/>' for i in range(2)) +
    '<text x="15" y="103" font-size="9" fill="#16a34a" font-family="sans-serif">B</text>' +
    '<text x="330" y="85" text-anchor="middle" font-size="10" fill="#16a34a" font-family="sans-serif">Задача B: каждые 500 мс (дисплей)</text>' +
    # Task C (1000ms)
    '<rect x="30" y="130" width="30" height="20" rx="3" fill="#f59e0b" opacity="0.85"/>' +
    '<text x="15" y="143" font-size="9" fill="#f59e0b" font-family="sans-serif">C</text>' +
    '<text x="330" y="125" text-anchor="middle" font-size="10" fill="#f59e0b" font-family="sans-serif">Задача C: каждые 1000 мс (BT отправка)</text>' +
    # idle
    '<text x="330" y="175" text-anchor="middle" font-size="10" fill="#94a3b8" font-family="sans-serif">МК свободен остальное время → можно уходить в сон</text>',
    640, 225, 'Кооперативный планировщик: каждая задача работает в своё «окно»'
) +
table(
    ['Тип планировщика','Описание','Применение'],
    [
        ['Кооперативный (millis)','Задачи сами отдают управление','Простые проекты, без RTOS'],
        ['FreeRTOS (вытесняющий)','ОС переключает задачи по таймеру','Сложные системы, Arduino Mega/ESP32'],
        ['Interrupt-driven','Логика в ISR','Только для очень быстрых реакций'],
    ]
) +
tip('Золотое правило планировщика: ни одна задача не должна вызывать delay(). Если задача занимает > 1–2% от своего периода — она слишком тяжёлая, разбейте её на шаги с помощью FSM.') +
warn('Кооперативный планировщик не гарантирует точность — если какая-то задача завис или заняла слишком много времени, все остальные сдвинутся. Для жёстких временны́х требований нужна RTOS или прерывания.'),
'code_example': '''#include <Arduino.h>

// Простой Task Scheduler на millis()
struct Task {
    void (*func)();
    uint32_t period;
    uint32_t last_run;
};

// Объявления задач
void task_sensors();
void task_display();
void task_bluetooth();
void task_heartbeat();

Task tasks[] = {
    { task_sensors,   200,  0 },
    { task_display,   1000, 0 },
    { task_bluetooth, 5000, 0 },
    { task_heartbeat, 500,  0 },
};
const int NUM_TASKS = sizeof(tasks)/sizeof(tasks[0]);

void scheduler_run() {
    uint32_t now = millis();
    for (int i = 0; i < NUM_TASKS; i++) {
        if (now - tasks[i].last_run >= tasks[i].period) {
            tasks[i].last_run += tasks[i].period;  // не now! — точный период
            tasks[i].func();
        }
    }
}

// Реализации задач
void task_sensors()   { /* читать АЦП, температуру */ }
void task_display()   { /* обновить OLED */ }
void task_bluetooth() { /* отправить данные */ }
void task_heartbeat() { static bool s; s=!s; digitalWrite(13,s); }

void setup() { pinMode(13,OUTPUT); }
void loop()  { scheduler_run(); }'''
},
],

}  # конец LESSONS


# ══════════════════════════════════════════════════════════════════
# ПАТЧ ТОНКИХ УРОКОВ
# ══════════════════════════════════════════════════════════════════

PATCHES = {
    # M2 L4: было 728 символов
    (2, 4): {
        'title': 'Стек и подпрограммы AVR (ассемблер)',
        'estimated_minutes': 45,
        'content': '''
<h2>Стек в AVR — LIFO структура в SRAM</h2>
<p>Стек — область SRAM, работающая по принципу LIFO (Last In, First Out). Stack Pointer (SP) хранится в регистрах SPH:SPL и указывает на верхушку стека. При инициализации SP = RAMEND (конец SRAM).</p>
''' + diagram(
    DEFS + BG.format(h=220) +
    '<text x="320" y="28" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold" font-family="sans-serif">Стек ATmega328P: push/pop</text>' +
    box(20,50,140,155,'#dbeafe','#3b82f6','SRAM\n0x0100–0x08FF',12,'bold') +
    box(30,75,120,20,'#bfdbfe','#3b82f6','0x08FF = RAMEND',9) +
    box(30,100,120,20,'#bfdbfe','#3b82f6','← r16 (push)',9) +
    box(30,125,120,20,'#bfdbfe','#3b82f6','← r17 (push)',9) +
    box(30,155,120,20,'#fee2e2','#ef4444','← SP (0x08FC)',9,'bold') +
    '<text x="90" y="195" text-anchor="middle" font-size="10" fill="#1e40af" font-family="sans-serif">Стек растёт ВНИЗ</text>' +
    arrow(190,130,250,130) +
    box(250,80,340,120,'#dcfce7','#16a34a','Операции стека',12,'bold') +
    '<text x="270" y="120" font-size="11" fill="#14532d" font-family="monospace">push r16  ; [SP]=r16, SP--</text>' +
    '<text x="270" y="140" font-size="11" fill="#14532d" font-family="monospace">pop  r16  ; SP++, r16=[SP]</text>' +
    '<text x="270" y="165" font-size="11" fill="#14532d" font-family="monospace">rcall sub ; push PC, jmp</text>' +
    '<text x="270" y="185" font-size="11" fill="#14532d" font-family="monospace">ret       ; pop PC</text>',
    640, 225, 'SP начинается у RAMEND (0x08FF) и уменьшается при push'
) + table(
    ['Операция','Такты','Действие с SP и памятью'],
    [
        ['push Rr','2','SRAM[SP] = Rr; SP -= 1'],
        ['pop Rd','2','SP += 1; Rd = SRAM[SP]'],
        ['rcall k','3','push PC (2 байта); PC = PC+k+1'],
        ['call k','4','push PC (2 байта); PC = k (дальний)'],
        ['ret','4','pop PC (2 байта); переход на PC'],
        ['reti','4','pop PC; I-флаг = 1 (возврат из ISR)'],
    ]
) + tip('Перед использованием стека всегда инициализируйте SP: <code>ldi r16, HIGH(RAMEND) / out SPH, r16 / ldi r16, LOW(RAMEND) / out SPL, r16</code>. Иначе стек начнётся с адреса 0 и перезапишет регистры I/O.') +
warn('Каждый push должен иметь соответствующий pop. Дисбаланс → SP указывает неверно → ret прыгает по случайному адресу → зависание. Это классическая ошибка в ASM.'),
        'code_example': '''; Демонстрация стека и подпрограмм AVR
.include "m328pdef.inc"

.org 0x0000
    rjmp init

init:
    ; Инициализация SP
    ldi  r16, HIGH(RAMEND)
    out  SPH, r16
    ldi  r16, LOW(RAMEND)
    out  SPL, r16

    ldi  r16, 10
    ldi  r17, 20
    rcall add_and_save    ; вызов подпрограммы
    ; После возврата: r18 = 30

loop:
    rjmp loop

; Подпрограмма: r18 = r16 + r17
; Сохраняет r16, r17 (callee-saved)
add_and_save:
    push r16              ; сохранить r16
    push r17              ; сохранить r17
    push SREG             ; сохранить флаги (хорошая практика в ISR)

    add  r16, r17         ; r16 = r16 + r17
    mov  r18, r16         ; результат в r18

    pop  SREG             ; восстановить флаги
    pop  r17
    pop  r16
    ret                   ; вернуться'''
    },
}


class Command(BaseCommand):
    help = 'Новые модули M11-M15 + патч тонких уроков МПС'

    def handle(self, *args, **options):
        try:
            subj = Subject.objects.get(slug='mcu')
        except Subject.DoesNotExist:
            self.stderr.write('Subject mcu не найден.')
            return

        # 1. Создать новые модули
        for md in NEW_MODULES:
            module, created = TheoryModule.objects.get_or_create(
                subject=subj, order=md['order'],
                defaults={
                    'title': md['title'],
                    'description': md['description'],
                    'icon': md['icon'],
                    'is_active': True,
                }
            )
            status = 'создан' if created else 'уже есть'
            self.stdout.write(f'Модуль M{md["order"]} [{status}]: {md["title"]}')

            for ld in LESSONS[md['order']]:
                obj, lc = TheoryLesson.objects.update_or_create(
                    module=module, order=ld['order'],
                    defaults={
                        'title': ld['title'],
                        'content': ld['content'],
                        'code_example': ld.get('code_example', ''),
                        'estimated_minutes': ld['estimated_minutes'],
                    }
                )
                self.stdout.write(f'  L{ld["order"]}: {ld["title"][:45]} [{"создан" if lc else "обновлён"}]')

        # 2. Патч тонких уроков
        self.stdout.write('\n--- Патч существующих уроков ---')
        for (mod_order, lesson_order), data in PATCHES.items():
            module = TheoryModule.objects.filter(subject=subj, order=mod_order).first()
            if not module:
                self.stderr.write(f'M{mod_order} не найден')
                continue
            obj, created = TheoryLesson.objects.update_or_create(
                module=module, order=lesson_order,
                defaults={
                    'title': data['title'],
                    'content': data['content'],
                    'code_example': data.get('code_example', ''),
                    'estimated_minutes': data['estimated_minutes'],
                }
            )
            self.stdout.write(f'  M{mod_order} L{lesson_order}: {data["title"][:45]} [{"создан" if created else "обновлён"}]')

        self.stdout.write(self.style.SUCCESS('\nГотово!'))
