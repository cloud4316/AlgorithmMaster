"""
Расширение модулей 11-15 МПС до 6 уроков каждый.
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


LESSONS = {
    'Дисплеи и индикаторы': [
        {
            'title': 'OLED-дисплеи SSD1306',
            'estimated_minutes': 20,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include "ssd1306.h"\n\n'
                'void oled_init(void) {\n'
                '    i2c_init();\n'
                '    ssd1306_command(0xAE); // Display OFF\n'
                '    ssd1306_command(0xD5); // Clock div\n'
                '    ssd1306_command(0x80);\n'
                '    ssd1306_command(0xA8); // Multiplex\n'
                '    ssd1306_command(0x3F); // 64 lines\n'
                '    ssd1306_command(0xD3); // Offset\n'
                '    ssd1306_command(0x00);\n'
                '    ssd1306_command(0x40); // Start line\n'
                '    ssd1306_command(0x8D); // Charge pump\n'
                '    ssd1306_command(0x14);\n'
                '    ssd1306_command(0xAF); // Display ON\n'
                '}\n\n'
                'void oled_print(uint8_t x, uint8_t y, const char *str) {\n'
                '    ssd1306_set_cursor(x, y);\n'
                '    while (*str) {\n'
                '        ssd1306_putchar(*str++);\n'
                '    }\n'
                '}\n\n'
                'int main(void) {\n'
                '    oled_init();\n'
                '    oled_print(0, 0, "Hello, OLED!");\n'
                '    oled_print(0, 2, "Temp: 25.3 C");\n'
                '    while (1);\n'
                '}'
            ),
            'content': (
                '<h3>OLED-дисплей SSD1306</h3>'
                '<p>SSD1306 -- популярный монохромный OLED-контроллер с разрешением 128x64 или 128x32 пикселей. '
                'Подключается по I2C (адрес 0x3C) или SPI.</p>'
                '<h3>Особенности</h3>'
                '<ul>'
                '<li><strong>Самосветящиеся пиксели</strong> -- не нужна подсветка, отличная контрастность</li>'
                '<li><strong>Низкое потребление</strong> -- 10-20 мА в зависимости от заполнения</li>'
                '<li><strong>Широкий угол обзора</strong> -- почти 180 градусов</li>'
                '<li><strong>Быстрая перерисовка</strong> -- до 100 FPS</li>'
                '</ul>'
                '<h3>Архитектура памяти</h3>'
                '<p>Дисплей имеет встроенную GDDRAM (Graphic Display Data RAM) размером 128x64 бит = 1024 байт. '
                'Память разбита на 8 страниц по 128 столбцов. Каждый байт описывает 8 вертикальных пикселей.</p>'
                '<table><tr><th>Страница</th><th>Строки</th><th>Адреса</th></tr>'
                '<tr><td>PAGE0</td><td>0-7</td><td>0x00-0x7F</td></tr>'
                '<tr><td>PAGE1</td><td>8-15</td><td>0x80-0xFF</td></tr>'
                '<tr><td>...</td><td>...</td><td>...</td></tr>'
                '<tr><td>PAGE7</td><td>56-63</td><td>0x380-0x3FF</td></tr></table>'
                '<h3>Инициализация по I2C</h3>'
                '<p>Последовательность команд: выключить дисплей, настроить тактирование, мультиплексирование, '
                'смещение, charge pump (встроенный DC-DC), включить дисплей.</p>'
                '<h3>Вывод текста</h3>'
                '<p>Для вывода символов нужен шрифт -- массив битовых масок 5x7 или 8x8 пикселей на символ. '
                'Каждый символ отправляется побайтно в GDDRAM через I2C.</p>'
            ),
        },
        {
            'title': 'TFT-дисплеи и графические библиотеки',
            'estimated_minutes': 20,
            'code_example': (
                '// Работа с TFT ILI9341 по SPI\n'
                '#include <avr/io.h>\n'
                '#include "ili9341.h"\n\n'
                '#define TFT_WIDTH  240\n'
                '#define TFT_HEIGHT 320\n\n'
                '// Цвета в формате RGB565\n'
                '#define RED    0xF800\n'
                '#define GREEN  0x07E0\n'
                '#define BLUE   0x001F\n'
                '#define WHITE  0xFFFF\n'
                '#define BLACK  0x0000\n\n'
                'void tft_fill_rect(uint16_t x, uint16_t y,\n'
                '                   uint16_t w, uint16_t h,\n'
                '                   uint16_t color) {\n'
                '    tft_set_window(x, y, x+w-1, y+h-1);\n'
                '    for (uint32_t i = 0; i < (uint32_t)w * h; i++) {\n'
                '        spi_send16(color);\n'
                '    }\n'
                '}\n\n'
                'int main(void) {\n'
                '    spi_init();\n'
                '    tft_init();\n'
                '    tft_fill_rect(0, 0, TFT_WIDTH, TFT_HEIGHT, BLACK);\n'
                '    tft_fill_rect(10, 10, 100, 50, RED);\n'
                '    tft_fill_rect(10, 70, 100, 50, GREEN);\n'
                '    while (1);\n'
                '}'
            ),
            'content': (
                '<h3>TFT-дисплеи на контроллере ILI9341</h3>'
                '<p>Цветные TFT-дисплеи 240x320 (2.4"-3.2") подключаются по SPI на скоростях до 40 МГц. '
                'Формат цвета -- RGB565 (16 бит на пиксель): 5 бит красного, 6 зелёного, 5 синего.</p>'
                '<h3>Подключение по SPI</h3>'
                '<table><tr><th>TFT</th><th>AVR</th><th>Назначение</th></tr>'
                '<tr><td>SCK</td><td>PB5</td><td>Тактовый сигнал SPI</td></tr>'
                '<tr><td>MOSI</td><td>PB3</td><td>Данные</td></tr>'
                '<tr><td>CS</td><td>PB2</td><td>Выбор дисплея</td></tr>'
                '<tr><td>DC</td><td>PB1</td><td>Данные/Команда</td></tr>'
                '<tr><td>RST</td><td>PB0</td><td>Сброс</td></tr></table>'
                '<h3>Буфер кадра</h3>'
                '<p>Полный буфер 240x320x2 = 153600 байт -- не помещается в RAM AVR (2 КБ). '
                'Решения: рисовать сразу на дисплей (без буфера), использовать частичный буфер (1 строка = 480 байт), '
                'или перейти на ARM (STM32 с 64+ КБ RAM).</p>'
                '<h3>Оптимизация скорости</h3>'
                '<ul>'
                '<li>Максимальная частота SPI (F_CPU/2)</li>'
                '<li>Пакетная отправка -- задать окно, затем поток данных</li>'
                '<li>Перерисовывать только изменившиеся области</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Звуковая индикация',
            'estimated_minutes': 15,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <util/delay.h>\n\n'
                '// Пьезоизлучатель на OC1A (PB1)\n'
                'void tone(uint16_t freq_hz, uint16_t duration_ms) {\n'
                '    // CTC mode, toggle OC1A\n'
                '    TCCR1A = (1 << COM1A0);\n'
                '    TCCR1B = (1 << WGM12) | (1 << CS11); // prescaler 8\n'
                '    OCR1A = (F_CPU / 8 / 2 / freq_hz) - 1;\n'
                '    DDRB |= (1 << PB1);\n\n'
                '    // Ждём duration_ms\n'
                '    for (uint16_t i = 0; i < duration_ms; i++)\n'
                '        _delay_ms(1);\n\n'
                '    TCCR1A = 0; // Выключить звук\n'
                '    TCCR1B = 0;\n'
                '}\n\n'
                '// Мелодия: нота До-Ре-Ми\n'
                'int main(void) {\n'
                '    tone(262, 300); _delay_ms(50);  // До\n'
                '    tone(294, 300); _delay_ms(50);  // Ре\n'
                '    tone(330, 300); _delay_ms(50);  // Ми\n'
                '    tone(349, 300); _delay_ms(50);  // Фа\n'
                '    tone(392, 600); _delay_ms(100); // Соль\n'
                '    while (1);\n'
                '}'
            ),
            'content': (
                '<h3>Звуковая индикация в МПС</h3>'
                '<p>Пьезоизлучатель -- простейший способ звуковой обратной связи. Два типа:</p>'
                '<ul>'
                '<li><strong>Активный (со встроенным генератором)</strong> -- подал напряжение = пищит. Нельзя менять тон.</li>'
                '<li><strong>Пассивный</strong> -- нужен внешний сигнал (прямоугольная волна). Можно задавать частоту = ноту.</li>'
                '</ul>'
                '<h3>Генерация тона через таймер</h3>'
                '<p>Режим CTC (Clear Timer on Compare) с переключением вывода OC1A. '
                'Частота звука: <code>f = F_CPU / (2 * prescaler * (OCR1A + 1))</code></p>'
                '<table><tr><th>Нота</th><th>Частота (Гц)</th><th>OCR1A (16 МГц, /8)</th></tr>'
                '<tr><td>До (C4)</td><td>262</td><td>3816</td></tr>'
                '<tr><td>Ре (D4)</td><td>294</td><td>3400</td></tr>'
                '<tr><td>Ми (E4)</td><td>330</td><td>3029</td></tr>'
                '<tr><td>Ля (A4)</td><td>440</td><td>2272</td></tr></table>'
                '<h3>Применение</h3>'
                '<ul>'
                '<li>Подтверждение нажатия кнопки (короткий бип)</li>'
                '<li>Сигнал ошибки (серия коротких тонов)</li>'
                '<li>Будильник, таймер</li>'
                '<li>Простые мелодии (таблица нот + длительностей)</li>'
                '</ul>'
            ),
        },
    ],

    'Управление двигателями': [
        {
            'title': 'Шаговые двигатели',
            'estimated_minutes': 25,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <util/delay.h>\n\n'
                '// Драйвер A4988: STEP на PD2, DIR на PD3\n'
                '#define STEP_PIN PD2\n'
                '#define DIR_PIN  PD3\n\n'
                'void stepper_init(void) {\n'
                '    DDRD |= (1 << STEP_PIN) | (1 << DIR_PIN);\n'
                '}\n\n'
                'void stepper_step(uint16_t steps, uint8_t dir, uint16_t delay_us) {\n'
                '    if (dir)\n'
                '        PORTD |= (1 << DIR_PIN);\n'
                '    else\n'
                '        PORTD &= ~(1 << DIR_PIN);\n\n'
                '    for (uint16_t i = 0; i < steps; i++) {\n'
                '        PORTD |= (1 << STEP_PIN);\n'
                '        _delay_us(10);\n'
                '        PORTD &= ~(1 << STEP_PIN);\n'
                '        for (uint16_t d = 0; d < delay_us / 10; d++)\n'
                '            _delay_us(10);\n'
                '    }\n'
                '}\n\n'
                'int main(void) {\n'
                '    stepper_init();\n'
                '    stepper_step(200, 1, 2000); // 1 оборот вперед\n'
                '    _delay_ms(500);\n'
                '    stepper_step(200, 0, 1000); // 1 оборот назад быстрее\n'
                '    while (1);\n'
                '}'
            ),
            'content': (
                '<h3>Шаговые двигатели</h3>'
                '<p>Шаговый двигатель поворачивается на фиксированный угол (шаг) при каждом импульсе. '
                'Типичный шаг: 1.8 градуса = 200 шагов на оборот.</p>'
                '<h3>Типы</h3>'
                '<table><tr><th>Тип</th><th>Обмотки</th><th>Провода</th><th>Драйвер</th></tr>'
                '<tr><td>Униполярный</td><td>С отводом от середины</td><td>5-6</td><td>ULN2003</td></tr>'
                '<tr><td>Биполярный</td><td>Две независимые</td><td>4</td><td>A4988, DRV8825</td></tr></table>'
                '<h3>Режимы управления</h3>'
                '<ul>'
                '<li><strong>Полный шаг</strong> -- 200 шагов/оборот, максимальный момент</li>'
                '<li><strong>Полушаг</strong> -- 400 шагов/оборот, плавнее</li>'
                '<li><strong>Микрошаг (1/16, 1/32)</strong> -- до 6400 шагов/оборот, очень плавное вращение</li>'
                '</ul>'
                '<h3>Драйвер A4988</h3>'
                '<p>Управляется двумя сигналами: STEP (импульс = один шаг) и DIR (направление). '
                'Микрошаг задаётся выводами MS1-MS3. Ток ограничивается подстроечным резистором.</p>'
            ),
        },
        {
            'title': 'Энкодеры и обратная связь',
            'estimated_minutes': 20,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <avr/interrupt.h>\n\n'
                'volatile int16_t encoder_count = 0;\n\n'
                '// Инкрементальный энкодер: A на PD2 (INT0), B на PD3\n'
                'void encoder_init(void) {\n'
                '    DDRD &= ~((1 << PD2) | (1 << PD3));\n'
                '    PORTD |= (1 << PD2) | (1 << PD3); // pull-up\n'
                '    EICRA |= (1 << ISC00); // любое изменение INT0\n'
                '    EIMSK |= (1 << INT0);\n'
                '    sei();\n'
                '}\n\n'
                'ISR(INT0_vect) {\n'
                '    uint8_t a = (PIND >> PD2) & 1;\n'
                '    uint8_t b = (PIND >> PD3) & 1;\n'
                '    if (a == b)\n'
                '        encoder_count++;\n'
                '    else\n'
                '        encoder_count--;\n'
                '}\n\n'
                'int main(void) {\n'
                '    encoder_init();\n'
                '    // encoder_count содержит позицию\n'
                '    while (1) {\n'
                '        int16_t pos = encoder_count;\n'
                '        // Используем pos для управления\n'
                '    }\n'
                '}'
            ),
            'content': (
                '<h3>Инкрементальные энкодеры</h3>'
                '<p>Энкодер -- датчик положения и скорости вращения. Выдаёт два сигнала (A и B) '
                'со сдвигом фазы 90 градусов (квадратура).</p>'
                '<h3>Принцип работы</h3>'
                '<ul>'
                '<li>Вращение по часовой: A опережает B</li>'
                '<li>Вращение против часовой: B опережает A</li>'
                '<li>Число импульсов = угол поворота</li>'
                '<li>Частота импульсов = скорость вращения</li>'
                '</ul>'
                '<h3>Квадратурное декодирование</h3>'
                '<p>При изменении сигнала A: если A == B -- вращение вперёд, если A != B -- назад. '
                'Это простейший алгоритм x1. Для x4 (максимальная точность) обрабатывают оба фронта обоих каналов.</p>'
                '<h3>PID-регулирование скорости</h3>'
                '<p>Измеряем скорость (импульсы за период), сравниваем с заданной, '
                'корректируем ШИМ через PID-формулу: <code>u = Kp*e + Ki*integral + Kd*derivative</code></p>'
            ),
        },
        {
            'title': 'Силовая электроника для МК',
            'estimated_minutes': 20,
            'code_example': (
                '#include <avr/io.h>\n\n'
                '// MOSFET-ключ на PB1 (OC1A) -- управление нагрузкой через ШИМ\n'
                'void mosfet_pwm_init(void) {\n'
                '    DDRB |= (1 << PB1);\n'
                '    // Fast PWM, 8-bit, non-inverting\n'
                '    TCCR1A = (1 << COM1A1) | (1 << WGM10);\n'
                '    TCCR1B = (1 << WGM12) | (1 << CS11); // prescaler 8\n'
                '    OCR1A = 0; // 0% duty\n'
                '}\n\n'
                'void set_power(uint8_t percent) {\n'
                '    if (percent > 100) percent = 100;\n'
                '    OCR1A = (uint16_t)percent * 255 / 100;\n'
                '}\n\n'
                'int main(void) {\n'
                '    mosfet_pwm_init();\n'
                '    set_power(50);  // 50% мощности\n'
                '    while (1);\n'
                '}'
            ),
            'content': (
                '<h3>Силовая электроника</h3>'
                '<p>МК не может напрямую управлять мощной нагрузкой (моторы, лампы, нагреватели). '
                'Нужны силовые ключи.</p>'
                '<h3>MOSFET-транзисторы</h3>'
                '<table><tr><th>Параметр</th><th>IRLZ44N</th><th>IRF540N</th></tr>'
                '<tr><td>Напряжение</td><td>55 В</td><td>100 В</td></tr>'
                '<tr><td>Ток</td><td>47 А</td><td>33 А</td></tr>'
                '<tr><td>Rds(on)</td><td>0.022 Ом</td><td>0.044 Ом</td></tr>'
                '<tr><td>Logic level</td><td>Да</td><td>Нет</td></tr></table>'
                '<p><strong>Logic-level MOSFET</strong> (IRLZ44N) открывается от 3.3-5 В -- можно управлять '
                'напрямую с МК. Обычный MOSFET (IRF540N) требует драйвер (IR2104).</p>'
                '<h3>Защита</h3>'
                '<ul>'
                '<li><strong>Обратный диод</strong> (flyback) -- обязателен для индуктивных нагрузок (моторы, реле)</li>'
                '<li><strong>Резистор на затворе</strong> (100-470 Ом) -- ограничение тока заряда ёмкости затвора</li>'
                '<li><strong>Pull-down 10 кОм</strong> -- удерживает MOSFET закрытым при сбросе МК</li>'
                '</ul>'
            ),
        },
    ],

    'Режимы сна и питание': [
        {
            'title': 'Проектирование с батарейным питанием',
            'estimated_minutes': 20,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <avr/sleep.h>\n'
                '#include <avr/interrupt.h>\n\n'
                '// Измерение напряжения батареи через АЦП\n'
                '// Делитель: BAT--[100k]--ADC--[100k]--GND\n'
                'uint16_t read_battery_mv(void) {\n'
                '    ADMUX = (1 << REFS0) | 0; // AVcc ref, ADC0\n'
                '    ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1);\n'
                '    ADCSRA |= (1 << ADSC);\n'
                '    while (ADCSRA & (1 << ADSC));\n'
                '    // Делитель 1:2, Vref=5V\n'
                '    return (uint32_t)ADC * 5000 * 2 / 1024;\n'
                '}\n\n'
                'int main(void) {\n'
                '    uint16_t bat = read_battery_mv();\n'
                '    if (bat < 3300) {\n'
                '        // Низкий заряд -- спать!\n'
                '        set_sleep_mode(SLEEP_MODE_PWR_DOWN);\n'
                '        sleep_mode();\n'
                '    }\n'
                '    while (1);\n'
                '}'
            ),
            'content': (
                '<h3>Батарейное питание МПС</h3>'
                '<p>При проектировании устройства на батарейках ключевой показатель -- '
                'средний ток потребления, определяющий время автономной работы.</p>'
                '<h3>Расчёт времени работы</h3>'
                '<p><code>T(часы) = C(мАч) / I_avg(мА)</code></p>'
                '<table><tr><th>Режим ATmega328P</th><th>Ток (3.3 В)</th></tr>'
                '<tr><td>Active, 8 МГц</td><td>~4 мА</td></tr>'
                '<tr><td>Idle</td><td>~1 мА</td></tr>'
                '<tr><td>Power-save</td><td>~1 мкА</td></tr>'
                '<tr><td>Power-down</td><td>~0.1 мкА</td></tr></table>'
                '<h3>Снижение потребления</h3>'
                '<ul>'
                '<li>Снизить тактовую частоту (8 МГц вместо 16)</li>'
                '<li>Питание 3.3 В вместо 5 В</li>'
                '<li>Отключить неиспользуемую периферию (PRR регистр)</li>'
                '<li>Отключить АЦП, BOD перед сном</li>'
                '<li>Использовать режим Power-down с пробуждением по прерыванию</li>'
                '</ul>'
            ),
        },
        {
            'title': 'Сторожевой таймер в режимах сна',
            'estimated_minutes': 15,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <avr/sleep.h>\n'
                '#include <avr/wdt.h>\n'
                '#include <avr/interrupt.h>\n\n'
                'volatile uint8_t wdt_fired = 0;\n\n'
                'ISR(WDT_vect) {\n'
                '    wdt_fired = 1;\n'
                '}\n\n'
                'void sleep_8s(void) {\n'
                '    // WDT interrupt mode, 8 sec\n'
                '    cli();\n'
                '    wdt_reset();\n'
                '    WDTCSR |= (1 << WDCE) | (1 << WDE);\n'
                '    WDTCSR = (1 << WDIE) | (1 << WDP3) | (1 << WDP0);\n'
                '    sei();\n\n'
                '    set_sleep_mode(SLEEP_MODE_PWR_DOWN);\n'
                '    sleep_mode(); // Спим 8 секунд\n'
                '}\n\n'
                'int main(void) {\n'
                '    DDRB |= (1 << PB0); // LED\n'
                '    while (1) {\n'
                '        PORTB |= (1 << PB0);   // LED ON\n'
                '        _delay_ms(100);\n'
                '        PORTB &= ~(1 << PB0);  // LED OFF\n'
                '        sleep_8s();             // Спим 8 сек\n'
                '    }\n'
                '}'
            ),
            'content': (
                '<h3>WDT как будильник</h3>'
                '<p>Watchdog Timer (WDT) можно использовать не только для сброса зависшей программы, '
                'но и как будильник для периодического пробуждения из Power-down.</p>'
                '<h3>Периоды WDT</h3>'
                '<table><tr><th>WDP3:0</th><th>Период</th></tr>'
                '<tr><td>0000</td><td>16 мс</td></tr>'
                '<tr><td>0101</td><td>0.5 с</td></tr>'
                '<tr><td>0110</td><td>1 с</td></tr>'
                '<tr><td>0111</td><td>2 с</td></tr>'
                '<tr><td>1001</td><td>8 с (макс.)</td></tr></table>'
                '<h3>Duty cycle</h3>'
                '<p>Пример: просыпаемся каждые 8 секунд, читаем датчик (50 мс), отправляем данные (200 мс), спим. '
                'Duty cycle = 250 мс / 8250 мс = 3%. Потребление: 0.97 * 0.1 мкА + 0.03 * 5 мА = 150 мкА. '
                'Батарея CR2032 (220 мАч) проработает ~60 дней.</p>'
            ),
        },
        {
            'title': 'Практика: метеостанция на батарейке',
            'estimated_minutes': 25,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <avr/sleep.h>\n'
                '#include <avr/wdt.h>\n'
                '#include <avr/interrupt.h>\n'
                '#include "bme280.h"\n'
                '#include "ssd1306.h"\n\n'
                'volatile uint8_t wake_count = 0;\n'
                '#define MEASURE_EVERY 8 // каждые 8*8=64 сек\n\n'
                'ISR(WDT_vect) { wake_count++; }\n\n'
                'void enter_sleep(void) {\n'
                '    ADCSRA &= ~(1 << ADEN); // АЦП выкл\n'
                '    set_sleep_mode(SLEEP_MODE_PWR_DOWN);\n'
                '    sleep_mode();\n'
                '    ADCSRA |= (1 << ADEN);  // АЦП вкл\n'
                '}\n\n'
                'int main(void) {\n'
                '    i2c_init();\n'
                '    bme280_init();\n'
                '    oled_init();\n\n'
                '    // WDT 8 сек interrupt\n'
                '    cli();\n'
                '    wdt_reset();\n'
                '    WDTCSR |= (1 << WDCE) | (1 << WDE);\n'
                '    WDTCSR = (1 << WDIE) | (1 << WDP3) | (1 << WDP0);\n'
                '    sei();\n\n'
                '    while (1) {\n'
                '        if (wake_count >= MEASURE_EVERY) {\n'
                '            wake_count = 0;\n'
                '            int16_t temp = bme280_read_temp();\n'
                '            uint16_t hum = bme280_read_humidity();\n'
                '            oled_clear();\n'
                '            oled_printf(0, 0, "T: %d.%d C", temp/100, temp%100);\n'
                '            oled_printf(0, 2, "H: %d %%", hum/100);\n'
                '        }\n'
                '        enter_sleep();\n'
                '    }\n'
                '}'
            ),
            'content': (
                '<h3>Проект: автономная метеостанция</h3>'
                '<p>Полный пример устройства на батарейке: ATmega328P + BME280 + OLED SSD1306.</p>'
                '<h3>Схема</h3>'
                '<ul>'
                '<li>ATmega328P на внутреннем RC 8 МГц, питание 3.3 В</li>'
                '<li>BME280 (I2C) -- температура, влажность, давление</li>'
                '<li>SSD1306 OLED 128x32 (I2C) -- отображение</li>'
                '<li>Питание: 2x AA (3 В) через LDO MCP1700-33</li>'
                '</ul>'
                '<h3>Алгоритм работы</h3>'
                '<ol>'
                '<li>Просыпаемся по WDT каждые 8 секунд</li>'
                '<li>Счётчик пробуждений -- измерение каждую минуту</li>'
                '<li>Читаем BME280 (forced mode -- 1 измерение)</li>'
                '<li>Обновляем OLED</li>'
                '<li>Засыпаем в Power-down</li>'
                '</ol>'
                '<h3>Расчёт автономности</h3>'
                '<p>Сон: 0.1 мкА (59.7 сек). Активно: 15 мА (0.3 сек). '
                'Среднее: ~75 мкА. Батарея 2x AA (2500 мАч): ~33000 часов = ~3.8 года (без OLED). '
                'С OLED (20 мА * 0.3 сек / 60 сек): ~175 мкА средне = ~1.6 года.</p>'
            ),
        },
    ],

    'Протоколы: 1-Wire и CAN': [
        {
            'title': 'Протокол 1-Wire: подробности',
            'estimated_minutes': 20,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <util/delay.h>\n\n'
                '#define OW_PORT PORTD\n'
                '#define OW_DDR  DDRD\n'
                '#define OW_PIN  PIND\n'
                '#define OW_BIT  PD4\n\n'
                'uint8_t ow_reset(void) {\n'
                '    OW_DDR |= (1 << OW_BIT);   // Low\n'
                '    OW_PORT &= ~(1 << OW_BIT);\n'
                '    _delay_us(480);\n'
                '    OW_DDR &= ~(1 << OW_BIT);  // Release\n'
                '    _delay_us(70);\n'
                '    uint8_t presence = !(OW_PIN & (1 << OW_BIT));\n'
                '    _delay_us(410);\n'
                '    return presence;\n'
                '}\n\n'
                'void ow_write_bit(uint8_t bit) {\n'
                '    OW_DDR |= (1 << OW_BIT);\n'
                '    OW_PORT &= ~(1 << OW_BIT);\n'
                '    _delay_us(bit ? 6 : 60);\n'
                '    OW_DDR &= ~(1 << OW_BIT);\n'
                '    _delay_us(bit ? 64 : 10);\n'
                '}\n\n'
                'void ow_write_byte(uint8_t data) {\n'
                '    for (uint8_t i = 0; i < 8; i++) {\n'
                '        ow_write_bit(data & 1);\n'
                '        data >>= 1;\n'
                '    }\n'
                '}'
            ),
            'content': (
                '<h3>Протокол 1-Wire</h3>'
                '<p>Однопроводный протокол Dallas/Maxim. Данные и питание по одному проводу + земля.</p>'
                '<h3>Временные слоты</h3>'
                '<table><tr><th>Операция</th><th>Master Low</th><th>Общее время</th></tr>'
                '<tr><td>Reset</td><td>480 мкс</td><td>960 мкс</td></tr>'
                '<tr><td>Write 1</td><td>6 мкс</td><td>70 мкс</td></tr>'
                '<tr><td>Write 0</td><td>60 мкс</td><td>70 мкс</td></tr>'
                '<tr><td>Read</td><td>6 мкс</td><td>70 мкс</td></tr></table>'
                '<h3>Несколько устройств на одной линии</h3>'
                '<p>Каждое устройство имеет уникальный 64-битный ROM-код. '
                'Алгоритм Search ROM позволяет найти все устройства на шине. '
                'Команда Match ROM (0x55) + 8 байт ROM адресует конкретное устройство.</p>'
                '<h3>Паразитное питание</h3>'
                '<p>Устройство заряжает внутренний конденсатор от линии данных (когда она HIGH). '
                'Ограничение: нельзя подавать данные во время преобразования (нужен strong pullup).</p>'
            ),
        },
        {
            'title': 'Протокол CAN: физический уровень',
            'estimated_minutes': 20,
            'code_example': (
                '// MCP2515 -- SPI CAN-контроллер\n'
                '#include <avr/io.h>\n'
                '#include "spi.h"\n'
                '#include "mcp2515.h"\n\n'
                'void can_init(uint16_t speed_kbps) {\n'
                '    mcp2515_reset();\n'
                '    // Настройка битрейта для кварца 8 МГц\n'
                '    switch (speed_kbps) {\n'
                '        case 500:\n'
                '            mcp2515_write(CNF1, 0x00);\n'
                '            mcp2515_write(CNF2, 0x90);\n'
                '            mcp2515_write(CNF3, 0x02);\n'
                '            break;\n'
                '        case 250:\n'
                '            mcp2515_write(CNF1, 0x01);\n'
                '            mcp2515_write(CNF2, 0x90);\n'
                '            mcp2515_write(CNF3, 0x02);\n'
                '            break;\n'
                '    }\n'
                '    mcp2515_write(CANINTE, 0x01); // RX0 interrupt\n'
                '    mcp2515_set_mode(MODE_NORMAL);\n'
                '}\n\n'
                'void can_send(uint16_t id, uint8_t *data, uint8_t len) {\n'
                '    mcp2515_write(TXB0SIDH, id >> 3);\n'
                '    mcp2515_write(TXB0SIDL, id << 5);\n'
                '    mcp2515_write(TXB0DLC, len);\n'
                '    for (uint8_t i = 0; i < len; i++)\n'
                '        mcp2515_write(TXB0D0 + i, data[i]);\n'
                '    mcp2515_rts(0);\n'
                '}'
            ),
            'content': (
                '<h3>Шина CAN</h3>'
                '<p>Controller Area Network -- промышленный протокол, разработанный Bosch для автомобилей. '
                'Используется в автопроме, промышленной автоматике, робототехнике.</p>'
                '<h3>Физический уровень</h3>'
                '<ul>'
                '<li><strong>Дифференциальная пара</strong>: CAN_H и CAN_L</li>'
                '<li><strong>Доминантный бит (0)</strong>: CAN_H=3.5V, CAN_L=1.5V (разность 2V)</li>'
                '<li><strong>Рецессивный бит (1)</strong>: CAN_H=CAN_L=2.5V (разность 0V)</li>'
                '<li><strong>Терминация</strong>: резисторы 120 Ом на обоих концах шины</li>'
                '</ul>'
                '<h3>Скорости и расстояния</h3>'
                '<table><tr><th>Скорость</th><th>Макс. длина</th></tr>'
                '<tr><td>1 Мбит/с</td><td>40 м</td></tr>'
                '<tr><td>500 Кбит/с</td><td>100 м</td></tr>'
                '<tr><td>125 Кбит/с</td><td>500 м</td></tr>'
                '<tr><td>10 Кбит/с</td><td>5 км</td></tr></table>'
                '<h3>Арбитраж</h3>'
                '<p>Побитовый арбитраж: устройство с меньшим ID выигрывает (его доминантные биты '
                'перекрывают рецессивные). Без коллизий и потерь данных.</p>'
            ),
        },
        {
            'title': 'Реализация CAN на AVR с MCP2515',
            'estimated_minutes': 25,
            'code_example': (
                '#include <avr/io.h>\n'
                '#include <avr/interrupt.h>\n'
                '#include "mcp2515.h"\n\n'
                'typedef struct {\n'
                '    uint16_t id;\n'
                '    uint8_t  len;\n'
                '    uint8_t  data[8];\n'
                '} can_msg_t;\n\n'
                'volatile can_msg_t rx_msg;\n'
                'volatile uint8_t msg_received = 0;\n\n'
                '// INT на PD2 от MCP2515\n'
                'ISR(INT0_vect) {\n'
                '    rx_msg.id = mcp2515_read_id(RXB0SIDH);\n'
                '    rx_msg.len = mcp2515_read(RXB0DLC) & 0x0F;\n'
                '    for (uint8_t i = 0; i < rx_msg.len; i++)\n'
                '        rx_msg.data[i] = mcp2515_read(RXB0D0 + i);\n'
                '    mcp2515_bit_modify(CANINTF, 0x01, 0x00);\n'
                '    msg_received = 1;\n'
                '}\n\n'
                'int main(void) {\n'
                '    can_init(500);\n'
                '    EICRA |= (1 << ISC01); // INT0 falling edge\n'
                '    EIMSK |= (1 << INT0);\n'
                '    sei();\n\n'
                '    // Отправка температуры каждую секунду\n'
                '    while (1) {\n'
                '        int16_t temp = read_temperature();\n'
                '        uint8_t data[2] = {temp >> 8, temp & 0xFF};\n'
                '        can_send(0x100, data, 2);\n'
                '        _delay_ms(1000);\n\n'
                '        if (msg_received) {\n'
                '            msg_received = 0;\n'
                '            // Обработка входящего сообщения\n'
                '        }\n'
                '    }\n'
                '}'
            ),
            'content': (
                '<h3>MCP2515 -- внешний CAN-контроллер</h3>'
                '<p>AVR не имеет встроенного CAN (в отличие от STM32). Решение -- внешний контроллер MCP2515 по SPI '
                'плюс трансивер MCP2551 или TJA1050.</p>'
                '<h3>Схема подключения</h3>'
                '<table><tr><th>MCP2515</th><th>AVR</th></tr>'
                '<tr><td>SCK</td><td>PB5 (SCK)</td></tr>'
                '<tr><td>SI</td><td>PB3 (MOSI)</td></tr>'
                '<tr><td>SO</td><td>PB4 (MISO)</td></tr>'
                '<tr><td>CS</td><td>PB2 (SS)</td></tr>'
                '<tr><td>INT</td><td>PD2 (INT0)</td></tr></table>'
                '<h3>Фильтрация сообщений</h3>'
                '<p>MCP2515 имеет 6 фильтров и 2 маски. Маска определяет какие биты ID проверять, '
                'фильтр -- какие значения принимать. Это разгружает МК -- прерывание только на нужные сообщения.</p>'
                '<h3>Пример: автомобильный OBD-II</h3>'
                '<p>OBD-II использует CAN 500 Кбит/с. Запрос: ID=0x7DF, данные [0x02, 0x01, PID]. '
                'Ответ: ID=0x7E8. PID 0x0C = обороты двигателя, 0x0D = скорость.</p>'
            ),
        },
    ],

    'Паттерны и архитектура ПО МК': [
        {
            'title': 'Суперцикл vs RTOS',
            'estimated_minutes': 25,
            'code_example': (
                '// Кооперативная многозадачность на таймере\n'
                '#include <avr/io.h>\n'
                '#include <avr/interrupt.h>\n\n'
                'volatile uint32_t millis_counter = 0;\n\n'
                'ISR(TIMER0_COMPA_vect) {\n'
                '    millis_counter++;\n'
                '}\n\n'
                'uint32_t millis(void) {\n'
                '    uint32_t ms;\n'
                '    cli();\n'
                '    ms = millis_counter;\n'
                '    sei();\n'
                '    return ms;\n'
                '}\n\n'
                'typedef struct {\n'
                '    void (*func)(void);\n'
                '    uint32_t period_ms;\n'
                '    uint32_t last_run;\n'
                '} task_t;\n\n'
                'void task_led(void)    { PORTB ^= (1 << PB0); }\n'
                'void task_sensor(void) { /* read sensor */ }\n'
                'void task_uart(void)   { /* send data */ }\n\n'
                'task_t tasks[] = {\n'
                '    { task_led,    500, 0 },\n'
                '    { task_sensor, 1000, 0 },\n'
                '    { task_uart,   2000, 0 },\n'
                '};\n'
                '#define NUM_TASKS (sizeof(tasks)/sizeof(tasks[0]))\n\n'
                'int main(void) {\n'
                '    // Timer0 CTC, 1 ms tick\n'
                '    TCCR0A = (1 << WGM01);\n'
                '    TCCR0B = (1 << CS01) | (1 << CS00); // /64\n'
                '    OCR0A = 249; // 16MHz/64/250 = 1kHz\n'
                '    TIMSK0 = (1 << OCIE0A);\n'
                '    DDRB |= (1 << PB0);\n'
                '    sei();\n\n'
                '    while (1) {\n'
                '        uint32_t now = millis();\n'
                '        for (uint8_t i = 0; i < NUM_TASKS; i++) {\n'
                '            if (now - tasks[i].last_run >= tasks[i].period_ms) {\n'
                '                tasks[i].last_run = now;\n'
                '                tasks[i].func();\n'
                '            }\n'
                '        }\n'
                '    }\n'
                '}'
            ),
            'content': (
                '<h3>Архитектуры встраиваемого ПО</h3>'
                '<h3>1. Суперцикл (bare-metal)</h3>'
                '<p>Простейшая архитектура: <code>while(1) { task1(); task2(); task3(); }</code>. '
                'Подходит для простых устройств. Проблема: одна задержка блокирует все остальные задачи.</p>'
                '<h3>2. Кооперативная многозадачность</h3>'
                '<p>Таблица задач с периодами. Планировщик на таймере вызывает задачи по расписанию. '
                'Задачи не должны блокироваться (никаких _delay_ms внутри!).</p>'
                '<h3>3. RTOS (FreeRTOS)</h3>'
                '<p>Полноценная вытесняющая многозадачность: каждая задача -- отдельный стек, '
                'приоритеты, семафоры, очереди. Минус: расход RAM (~200 байт на задачу).</p>'
                '<table><tr><th>Критерий</th><th>Суперцикл</th><th>Кооперативная</th><th>RTOS</th></tr>'
                '<tr><td>RAM</td><td>Минимум</td><td>Мало</td><td>200+ байт/задача</td></tr>'
                '<tr><td>Отзывчивость</td><td>Плохая</td><td>Средняя</td><td>Хорошая</td></tr>'
                '<tr><td>Сложность</td><td>Низкая</td><td>Средняя</td><td>Высокая</td></tr>'
                '<tr><td>Применение</td><td>Простое</td><td>Среднее</td><td>Сложное</td></tr></table>'
            ),
        },
        {
            'title': 'Драйверы периферии и HAL',
            'estimated_minutes': 20,
            'code_example': (
                '// HAL-слой для UART -- переносимый код\n\n'
                '// === uart_hal.h ===\n'
                'typedef struct {\n'
                '    void (*init)(uint32_t baud);\n'
                '    void (*send_byte)(uint8_t data);\n'
                '    uint8_t (*recv_byte)(void);\n'
                '    uint8_t (*available)(void);\n'
                '} uart_driver_t;\n\n'
                '// === uart_avr.c (AVR-реализация) ===\n'
                'static void avr_uart_init(uint32_t baud) {\n'
                '    uint16_t ubrr = F_CPU / 16 / baud - 1;\n'
                '    UBRR0H = ubrr >> 8;\n'
                '    UBRR0L = ubrr;\n'
                '    UCSR0B = (1 << RXEN0) | (1 << TXEN0);\n'
                '    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);\n'
                '}\n\n'
                'static void avr_uart_send(uint8_t data) {\n'
                '    while (!(UCSR0A & (1 << UDRE0)));\n'
                '    UDR0 = data;\n'
                '}\n\n'
                'static uint8_t avr_uart_recv(void) {\n'
                '    while (!(UCSR0A & (1 << RXC0)));\n'
                '    return UDR0;\n'
                '}\n\n'
                'static uint8_t avr_uart_avail(void) {\n'
                '    return (UCSR0A & (1 << RXC0)) ? 1 : 0;\n'
                '}\n\n'
                'const uart_driver_t uart_avr = {\n'
                '    .init = avr_uart_init,\n'
                '    .send_byte = avr_uart_send,\n'
                '    .recv_byte = avr_uart_recv,\n'
                '    .available = avr_uart_avail,\n'
                '};'
            ),
            'content': (
                '<h3>HAL -- Hardware Abstraction Layer</h3>'
                '<p>Слой абстракции аппаратуры отделяет логику приложения от конкретного МК. '
                'Это позволяет:</p>'
                '<ul>'
                '<li>Переносить код между платформами (AVR -> STM32)</li>'
                '<li>Тестировать логику на ПК (mock-драйверы)</li>'
                '<li>Разделить работу: один человек пишет драйверы, другой -- логику</li>'
                '</ul>'
                '<h3>Структура драйвера</h3>'
                '<p>Драйвер описывается структурой с указателями на функции. '
                'Каждая платформа предоставляет свою реализацию. '
                'Приложение работает через интерфейс, не зная деталей.</p>'
                '<h3>Пример архитектуры</h3>'
                '<pre>'
                'app.c          -- логика приложения\n'
                '  |\n'
                'uart_hal.h     -- интерфейс (структура с указателями)\n'
                '  |\n'
                '+-- uart_avr.c    -- реализация для AVR\n'
                '+-- uart_stm32.c  -- реализация для STM32\n'
                '+-- uart_mock.c   -- заглушка для тестов на ПК'
                '</pre>'
            ),
        },
        {
            'title': 'Тестирование встраиваемого ПО',
            'estimated_minutes': 20,
            'code_example': (
                '// Unit-тест на ПК (без железа)\n'
                '#include <stdio.h>\n'
                '#include <assert.h>\n\n'
                '// Тестируемый модуль -- парсер CAN-сообщений\n'
                'typedef struct {\n'
                '    uint16_t rpm;\n'
                '    uint8_t  speed_kmh;\n'
                '    int8_t   coolant_temp;\n'
                '} engine_data_t;\n\n'
                'engine_data_t parse_obd(uint8_t pid, uint8_t *data) {\n'
                '    engine_data_t e = {0};\n'
                '    switch (pid) {\n'
                '        case 0x0C: // RPM\n'
                '            e.rpm = ((uint16_t)data[0] << 8 | data[1]) / 4;\n'
                '            break;\n'
                '        case 0x0D: // Speed\n'
                '            e.speed_kmh = data[0];\n'
                '            break;\n'
                '        case 0x05: // Coolant temp\n'
                '            e.coolant_temp = data[0] - 40;\n'
                '            break;\n'
                '    }\n'
                '    return e;\n'
                '}\n\n'
                '// Тесты\n'
                'void test_parse_rpm(void) {\n'
                '    uint8_t data[] = {0x1A, 0xF8}; // 6904/4 = 1726 RPM\n'
                '    engine_data_t e = parse_obd(0x0C, data);\n'
                '    assert(e.rpm == 1726);\n'
                '    printf("  [OK] RPM parsing\\n");\n'
                '}\n\n'
                'void test_parse_temp(void) {\n'
                '    uint8_t data[] = {130}; // 130-40 = 90 C\n'
                '    engine_data_t e = parse_obd(0x05, data);\n'
                '    assert(e.coolant_temp == 90);\n'
                '    printf("  [OK] Temp parsing\\n");\n'
                '}\n\n'
                'int main(void) {\n'
                '    printf("Running tests...\\n");\n'
                '    test_parse_rpm();\n'
                '    test_parse_temp();\n'
                '    printf("All tests passed!\\n");\n'
                '    return 0;\n'
                '}'
            ),
            'content': (
                '<h3>Тестирование встраиваемого ПО</h3>'
                '<p>Отладка на реальном железе медленная и сложная. '
                'Правильный подход: разделить код на аппаратно-зависимый (драйверы) и независимый (логика), '
                'и тестировать логику на ПК.</p>'
                '<h3>Стратегии тестирования</h3>'
                '<table><tr><th>Уровень</th><th>Где</th><th>Что тестируем</th></tr>'
                '<tr><td>Unit-тесты</td><td>ПК</td><td>Логика, парсеры, алгоритмы</td></tr>'
                '<tr><td>HIL (Hardware-in-the-Loop)</td><td>Стенд</td><td>Драйверы + логика</td></tr>'
                '<tr><td>Системные тесты</td><td>Устройство</td><td>Всё вместе</td></tr></table>'
                '<h3>Mock-объекты</h3>'
                '<p>Заглушки для аппаратуры: вместо реального UART -- массив в памяти. '
                'Вместо реального АЦП -- предзаданные значения. Это позволяет тестировать '
                'граничные случаи, которые сложно воспроизвести на железе.</p>'
                '<h3>Статический анализ</h3>'
                '<ul>'
                '<li><strong>-Wall -Wextra -Werror</strong> -- все предупреждения как ошибки</li>'
                '<li><strong>cppcheck</strong> -- находит утечки памяти, неинициализированные переменные</li>'
                '<li><strong>MISRA C</strong> -- стандарт для safety-critical систем (автомобили, медтехника)</li>'
                '</ul>'
            ),
        },
    ],
}


class Command(BaseCommand):
    help = 'Expand MPS modules 11-15 to 6 lessons each'

    def handle(self, *args, **options):
        try:
            subj = Subject.objects.get(title='Микропроцессорные системы')
        except Subject.DoesNotExist:
            self.stdout.write('[ERROR] Subject not found')
            return

        created = 0
        for module_title, lessons in LESSONS.items():
            try:
                module = subj.modules.get(title=module_title)
            except TheoryModule.DoesNotExist:
                self.stdout.write(f'[SKIP] Module not found: {module_title}')
                continue

            max_order = module.lessons.order_by('-order').values_list('order', flat=True).first() or 0

            for i, lesson_data in enumerate(lessons):
                obj, is_new = TheoryLesson.objects.get_or_create(
                    module=module,
                    title=lesson_data['title'],
                    defaults={
                        'content': lesson_data['content'],
                        'code_example': lesson_data.get('code_example', ''),
                        'order': max_order + i + 1,
                        'estimated_minutes': lesson_data.get('estimated_minutes', 20),
                    }
                )
                if is_new:
                    created += 1
                    self.stdout.write(f'  [+] {module_title}: {lesson_data["title"]}')
                else:
                    self.stdout.write(f'  [.] exists: {lesson_data["title"]}')

        self.stdout.write(f'\nDone. Created: {created} lessons')
