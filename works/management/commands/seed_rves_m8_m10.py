"""
Seed: РВЭС — модули M8-M10
КТП: Отладка/рефакторинг/VCS, практикумы подключения компонентов к МК
"""
from django.core.management.base import BaseCommand
from works.models import Subject, TheoryModule, TheoryLesson


MODULES = [
    {
        'order': 8,
        'title': 'Отладка, рефакторинг и контроль версий',
        'icon': 'fas fa-bug',
        'description': 'Методы отладки МК-ПО, рефакторинг кода, Git для встраиваемых проектов',
        'lessons': [
            {
                'order': 1,
                'title': 'Методы отладки встраиваемого ПО',
                'estimated_minutes': 25,
                'content': (
                    '<h2>Отладка встраиваемого ПО</h2>'
                    '<h3>Уровни отладки</h3>'
                    '<table>'
                    '<tr><th>Уровень</th><th>Метод</th><th>Инструменты</th><th>Когда применять</th></tr>'
                    '<tr><td>Вывод в UART</td><td>printf/логирование</td><td>UART + терминал</td><td>Быстрая диагностика, не требует отладчика</td></tr>'
                    '<tr><td>LED-индикация</td><td>Мигание при событиях</td><td>Светодиод + осциллограф</td><td>Определить, выполняется ли код</td></tr>'
                    '<tr><td>GDB + OpenOCD</td><td>Пошаговое выполнение, точки останова</td><td>ST-Link + STM32CubeIDE</td><td>Точная локализация бага</td></tr>'
                    '<tr><td>Анализатор логики</td><td>Захват цифровых сигналов</td><td>Saleae, PulseView</td><td>Отладка протоколов SPI/I2C/UART</td></tr>'
                    '<tr><td>Осциллограф</td><td>Аналоговые сигналы, тайминги</td><td>Rigol, Siglent</td><td>Форма сигнала, помехи, сбои шины</td></tr>'
                    '</table>'
                    '<h3>Printf-отладка на STM32</h3>'
                    '<p>Самый простой способ — перенаправить printf в UART:</p>'
                    '<pre><code>// В syscalls.c или main.c:\n#include "usart.h"\n\nint __io_putchar(int ch) {\n    HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 10);\n    return ch;\n}\n\n// Использование:\nprintf("Temperature: %.1f°C\\r\\n", temp);\nprintf("ADC raw: %d\\r\\n", adc_value);\nprintf("State: %d\\r\\n", state);</code></pre>'
                    '<p>Или через SWO (Serial Wire Output) без занятия UART — только ST-Link V2 с SWO pin.</p>'
                    '<h3>SWO Trace — printf без UART</h3>'
                    '<pre><code>// В STM32CubeIDE: Run → Debug Configurations → Debugger → Serial Wire Viewer (SWV)\n// Включить ITM в коде:\nvoid SWO_print(const char *str) {\n    while (*str) {\n        ITM_SendChar(*str++);\n    }\n}</code></pre>'
                    '<h3>Типичные баги МК и диагностика</h3>'
                    '<table>'
                    '<tr><th>Симптом</th><th>Вероятная причина</th><th>Диагностика</th></tr>'
                    '<tr><td>МК не стартует</td><td>Нет тактирования, нет питания 3.3V</td><td>Мультиметр, осциллограф на CLK</td></tr>'
                    '<tr><td>Периферия не работает</td><td>Не включено тактирование RCC</td><td>Проверить RCC→APBxENR</td></tr>'
                    '<tr><td>UART молчит</td><td>Неверный baud, TX/RX перепутаны</td><td>Анализатор логики на TX-пин</td></tr>'
                    '<tr><td>Сброс через 1 сек</td><td>Watchdog, HardFault</td><td>Проверить IWDG, смотреть CFSR регистр</td></tr>'
                    '<tr><td>Данные АЦП шумят</td><td>Питание не развязано, нет фильтра</td><td>Осциллограф на VDDA/VREF</td></tr>'
                    '</table>'
                    '<div class="tip">HardFault_Handler с выводом стека через UART помогает локализовать аварийный адрес. '
                    'В Cortex-M: при HardFault адрес виновной инструкции находится в стеке (LR-4 для Thumb).</div>'
                ),
            },
            {
                'order': 2,
                'title': 'Рефакторинг кода встраиваемых систем',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Рефакторинг кода встраиваемых систем</h2>'
                    '<p>Рефакторинг — изменение внутренней структуры кода без изменения его внешнего поведения,'
                    ' с целью улучшения читаемости, поддерживаемости и тестируемости.</p>'
                    '<h3>Когда рефакторить</h3>'
                    '<ul>'
                    '<li>Функция длиннее 50 строк</li>'
                    '<li>Вложенность if/switch больше 3 уровней</li>'
                    '<li>Дублирование кода в трёх и более местах</li>'
                    '<li>Магические числа без именованных констант</li>'
                    '<li>Глобальные переменные там, где можно использовать параметры</li>'
                    '</ul>'
                    '<h3>Типичные приёмы рефакторинга для МК</h3>'
                    '<table>'
                    '<tr><th>Приём</th><th>До</th><th>После</th></tr>'
                    '<tr><td>Именованные константы</td><td><code>delay_ms(1000)</code></td><td><code>#define SENSOR_PERIOD_MS 1000<br>delay_ms(SENSOR_PERIOD_MS)</code></td></tr>'
                    '<tr><td>Извлечение функции</td><td>main() 500 строк</td><td>init_gpio(), init_uart(), app_task()</td></tr>'
                    '<tr><td>Конечный автомат</td><td>Вложенные if с флагами</td><td>enum State + switch(state)</td></tr>'
                    '<tr><td>HAL-абстракция</td><td>Прямой доступ к регистрам везде</td><td>Функции hal_gpio_set(), hal_uart_send()</td></tr>'
                    '</table>'
                    '<h3>Пример: до и после рефакторинга</h3>'
                    '<pre><code>// ДО:\nif (GPIOA->IDR & (1<<0)) {\n    GPIOC->ODR |= (1<<13);\n    HAL_Delay(500);\n    GPIOC->ODR &= ~(1<<13);\n    HAL_Delay(500);\n}\n\n// ПОСЛЕ:\n#define BTN_PIN     GPIO_PIN_0\n#define LED_PIN     GPIO_PIN_13\n#define BLINK_MS    500\n\nstatic inline bool button_is_pressed(void) {\n    return (GPIOA->IDR & BTN_PIN) != 0;\n}\n\nstatic void led_blink_once(void) {\n    HAL_GPIO_WritePin(GPIOC, LED_PIN, GPIO_PIN_SET);\n    HAL_Delay(BLINK_MS);\n    HAL_GPIO_WritePin(GPIOC, LED_PIN, GPIO_PIN_RESET);\n    HAL_Delay(BLINK_MS);\n}\n\nif (button_is_pressed()) {\n    led_blink_once();\n}</code></pre>'
                    '<div class="tip">Рефакторинг безопасен только при наличии тестов. '
                    'Сначала напишите тесты, убедитесь что они проходят, затем рефакторьте — и снова запускайте тесты.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'Git для встраиваемых проектов',
                'estimated_minutes': 20,
                'content': (
                    '<h2>Контроль версий Git во встраиваемых проектах</h2>'
                    '<h3>Базовые команды</h3>'
                    '<pre><code># Инициализация репозитория\ngit init\ngit remote add origin https://github.com/user/stm32-project.git\n\n# Первый коммит\ngit add src/ include/ CMakeLists.txt\ngit commit -m "Initial project structure"\ngit push -u origin main\n\n# Рабочий цикл:\ngit pull                    # получить обновления\ngit checkout -b feature/adc # создать ветку\n# ...редактируем код...\ngit add src/adc.c include/adc.h\ngit commit -m "feat: add 12-bit ADC driver with DMA"\ngit push origin feature/adc\n# Создать Pull Request → review → merge</code></pre>'
                    '<h3>Структура .gitignore для STM32</h3>'
                    '<pre><code># Сгенерированные файлы сборки\nDebug/\nRelease/\n*.o\n*.elf\n*.hex\n*.bin\n*.map\n\n# IDE-специфичные файлы (добавить нужные)\n.settings/\n.cproject\n*.launch\n\n# Но НЕ игнорировать:\n# - CMakeLists.txt\n# - *.ioc (STM32CubeMX конфигурация)\n# - linker.ld\n# - startup_*.s</code></pre>'
                    '<h3>Стратегия ветвления (Git Flow для МК)</h3>'
                    '<table>'
                    '<tr><th>Ветка</th><th>Назначение</th></tr>'
                    '<tr><td>main</td><td>Прошивки, выпущенные на производство (теги версий)</td></tr>'
                    '<tr><td>develop</td><td>Интеграционная — все готовые фичи собраны здесь</td></tr>'
                    '<tr><td>feature/xxx</td><td>Разработка новой функции (от develop)</td></tr>'
                    '<tr><td>hotfix/xxx</td><td>Срочное исправление в production-прошивке</td></tr>'
                    '</table>'
                    '<h3>Теги версий прошивки</h3>'
                    '<pre><code># Тег релиза:\ngit tag -a v1.2.3 -m "Release 1.2.3: add temperature alarm"\ngit push origin v1.2.3\n\n# Семантическое версионирование:\n# MAJOR.MINOR.PATCH\n# 1.0.0 → первый стабильный релиз\n# 1.1.0 → новая функция\n# 1.1.1 → исправление бага\n\n# Встроить версию в прошивку:\n#define FW_VERSION_STR "v1.2.3"\n#define FW_BUILD_DATE  __DATE__</code></pre>'
                    '<div class="tip">Всегда храните .ioc файл (STM32CubeMX) в Git — это позволяет воспроизвести конфигурацию периферии. '
                    'Бинарные файлы (.elf, .hex) в Git LFS или в артефакты CI, но не в основной репозиторий.</div>'
                ),
            },
        ],
    },
    {
        'order': 9,
        'title': 'Практикум: подключение компонентов к МК — часть 1',
        'icon': 'fas fa-plug',
        'description': 'ПЗ №1-7: GPIO, кнопки, дисплеи, АЦП, ЦАП, датчики температуры, ШИМ',
        'lessons': [
            {
                'order': 1,
                'title': 'ПЗ №1-2: Мигание LED, кнопки и GPIO',
                'estimated_minutes': 30,
                'content': (
                    '<h2>ПЗ №1: Управление LED через GPIO</h2>'
                    '<p>Базовый навык: инициализация GPIO, управление выходом.</p>'
                    '<h3>Схема подключения</h3>'
                    '<ul>'
                    '<li>LED → резистор 220–330 Ом → GND</li>'
                    '<li>LED анод → PA5 (или PC13 на Blue Pill, где логика инверсная)</li>'
                    '</ul>'
                    '<h3>Код (HAL)</h3>'
                    '<pre><code>// Инициализация (CubeMX генерирует автоматически):\nGPIO_InitTypeDef GPIO_InitStruct = {0};\nRCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);\nGPIO_InitStruct.Pin = GPIO_PIN_5;\nGPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;\nGPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\nHAL_GPIO_Init(GPIOA, &GPIO_InitStruct);\n\n// Основной цикл — мигание 1 Гц:\nwhile (1) {\n    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);\n    HAL_Delay(500);\n}</code></pre>'
                    '<h2>ПЗ №2: Кнопка — опрос и прерывание</h2>'
                    '<h3>Способ 1: Опрос (polling)</h3>'
                    '<pre><code>// Кнопка на PA0, внутренняя подтяжка вверх\nif (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {\n    // Кнопка нажата (0 — нажата при pull-up)\n    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);\n    HAL_Delay(50); // антидребезг\n    while (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET);\n}</code></pre>'
                    '<h3>Способ 2: Прерывание EXTI</h3>'
                    '<pre><code>// В CubeMX: PA0 → GPIO_EXTI0, режим — Falling edge\n// Автоматически генерируется HAL_GPIO_EXTI_Callback\n\nvoid HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {\n    if (GPIO_Pin == GPIO_PIN_0) {\n        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);\n    }\n}</code></pre>'
                    '<h3>Антидребезг</h3>'
                    '<p>Механическая кнопка дребезжит 5–50 мс. Программные методы:</p>'
                    '<ul>'
                    '<li><strong>Задержка:</strong> ждать 10–50 мс после первого события</li>'
                    '<li><strong>Сдвиговый регистр состояний:</strong> считывать 8 раз подряд, кнопка нажата если все 8 = 0</li>'
                    '</ul>'
                ),
            },
            {
                'order': 2,
                'title': 'ПЗ №3-4: LCD-дисплей и I2C',
                'estimated_minutes': 30,
                'content': (
                    '<h2>ПЗ №3: LCD HD44780 (16×2)</h2>'
                    '<h3>Подключение через I2C-адаптер PCF8574</h3>'
                    '<ul>'
                    '<li>SDA → PB7 (I2C1_SDA)</li>'
                    '<li>SCL → PB6 (I2C1_SCL)</li>'
                    '<li>Питание: 5В (часто), адаптер PCF8574 работает с 3.3В логикой</li>'
                    '<li>Адрес по умолчанию: 0x27 или 0x3F</li>'
                    '</ul>'
                    '<h3>Код LCD через I2C</h3>'
                    '<pre><code>#include "lcd_i2c.h"  // Библиотека для HD44780 через PCF8574\n\n// Инициализация:\nlcd_init(&hi2c1, 0x27, 2, 16); // I2C, адрес, строки, столбцы\n\n// Вывод текста:\nlcd_set_cursor(0, 0);\nlcd_print("Temperature:");\nlcd_set_cursor(1, 0);\nlcd_print_float(25.3, 1);\nlcd_print(" C");\n\n// Очистка:\nlcd_clear();</code></pre>'
                    '<h2>ПЗ №4: Работа с I2C вручную (без библиотеки)</h2>'
                    '<pre><code>// Запись одного байта на устройство I2C:\nHAL_StatusTypeDef I2C_write_byte(uint8_t addr, uint8_t reg, uint8_t data) {\n    uint8_t buf[2] = {reg, data};\n    return HAL_I2C_Master_Transmit(&hi2c1, addr << 1, buf, 2, 10);\n}\n\n// Чтение байта:\nHAL_StatusTypeDef I2C_read_byte(uint8_t addr, uint8_t reg, uint8_t *data) {\n    HAL_I2C_Master_Transmit(&hi2c1, addr << 1, &reg, 1, 10);\n    return HAL_I2C_Master_Receive(&hi2c1, addr << 1, data, 1, 10);\n}\n\n// Сканирование I2C-шины (диагностика):\nfor (uint8_t addr = 0x08; addr < 0x78; addr++) {\n    if (HAL_I2C_IsDeviceReady(&hi2c1, addr << 1, 1, 5) == HAL_OK) {\n        printf("Found device at 0x%02X\\r\\n", addr);\n    }\n}</code></pre>'
                    '<h3>Распространённые устройства I2C</h3>'
                    '<table>'
                    '<tr><th>Устройство</th><th>Адрес</th><th>Назначение</th></tr>'
                    '<tr><td>LCD PCF8574</td><td>0x27/0x3F</td><td>LCD-адаптер</td></tr>'
                    '<tr><td>DS3231</td><td>0x68</td><td>RTC часы реального времени</td></tr>'
                    '<tr><td>MPU-6050</td><td>0x68/0x69</td><td>Акселерометр + гироскоп</td></tr>'
                    '<tr><td>BMP280</td><td>0x76/0x77</td><td>Давление, температура</td></tr>'
                    '<tr><td>AT24C32</td><td>0x50–0x57</td><td>EEPROM 4 КБ</td></tr>'
                    '</table>'
                    '<div class="tip">При проблемах I2C: проверьте подтягивающие резисторы (4.7 кОм) на SDA и SCL. '
                    'Без них шина не поднимается. Анализатор логики сразу покажет форму сигнала START/STOP.</div>'
                ),
            },
            {
                'order': 3,
                'title': 'ПЗ №5-6: АЦП, ЦАП и SPI',
                'estimated_minutes': 30,
                'content': (
                    '<h2>ПЗ №5: Аналого-цифровой преобразователь (АЦП)</h2>'
                    '<h3>Внутренний АЦП STM32F103</h3>'
                    '<ul>'
                    '<li>12-битный, до 1 МГц при разрядности 12 бит</li>'
                    '<li>18 каналов: 16 внешних (PA0–PB1) + температурный датчик + VREF</li>'
                    '<li>Режимы: однократный, непрерывный, сканирование нескольких каналов</li>'
                    '</ul>'
                    '<pre><code>// Однократное измерение:\nHAL_ADC_Start(&hadc1);\nif (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {\n    uint32_t raw = HAL_ADC_GetValue(&hadc1);\n    float voltage = raw * 3.3f / 4095.0f;\n    printf("ADC: %lu (%.3f V)\\r\\n", raw, voltage);\n}\n\n// Измерение температуры внутренним датчиком:\n// Формула из datasheet STM32F103:\n// Temp = (V25 - Vsense) / Avg_Slope + 25\n// V25 = 1.43V, Avg_Slope = 4.3 mV/°C\nfloat calc_temp(uint32_t raw) {\n    float vsense = raw * 3.3f / 4095.0f;\n    return (1.43f - vsense) / 0.0043f + 25.0f;\n}</code></pre>'
                    '<h2>ПЗ №6: SPI — датчик и внешние АЦП</h2>'
                    '<pre><code>// SPI передача/приём одного байта:\nuint8_t SPI_transfer(uint8_t tx) {\n    uint8_t rx;\n    HAL_SPI_TransmitReceive(&hspi1, &tx, &rx, 1, 10);\n    return rx;\n}\n\n// Чтение 16-битного АЦП MCP3201 (12 бит, SPI):\nuint16_t MCP3201_read(void) {\n    HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_RESET);\n    uint8_t rx[2];\n    uint8_t tx[2] = {0x00, 0x00};\n    HAL_SPI_TransmitReceive(&hspi1, tx, rx, 2, 10);\n    HAL_GPIO_WritePin(CS_GPIO_Port, CS_Pin, GPIO_PIN_SET);\n    return ((rx[0] & 0x1F) << 7) | (rx[1] >> 1);\n}</code></pre>'
                    '<h3>Сравнение АЦП и SPI интерфейсов</h3>'
                    '<table>'
                    '<tr><th>Параметр</th><th>Внутренний АЦП STM32</th><th>Внешний АЦП (MCP3208)</th></tr>'
                    '<tr><td>Разрядность</td><td>12 бит</td><td>12 бит</td></tr>'
                    '<tr><td>Скорость</td><td>1 МГц</td><td>100 кГц — 2 МГц</td></tr>'
                    '<tr><td>Каналов</td><td>16</td><td>8</td></tr>'
                    '<tr><td>Точность</td><td>±2 LSB типично</td><td>±1 LSB типично</td></tr>'
                    '<tr><td>Требования</td><td>Тихое питание VDDA</td><td>Отдельный кристалл</td></tr>'
                    '</table>'
                    '<div class="tip">Для точных измерений изолируйте аналоговую часть: отдельный дроссель или ферритовая бусина на VDDA, '
                    'разделительные конденсаторы 100 нФ + 10 мкФ рядом с кристаллом.</div>'
                ),
            },
            {
                'order': 4,
                'title': 'ПЗ №7: ШИМ и управление мощностью',
                'estimated_minutes': 25,
                'content': (
                    '<h2>ПЗ №7: ШИМ (PWM) — управление яркостью и мощностью</h2>'
                    '<h3>Что такое ШИМ</h3>'
                    '<p>ШИМ (Широтно-Импульсная Модуляция, PWM) — сигнал с постоянной частотой и переменной скважностью (duty cycle).'
                    ' Среднее напряжение пропорционально скважности: 0% = 0 В, 50% = 1.65 В, 100% = 3.3 В.</p>'
                    '<h3>Применения ШИМ</h3>'
                    '<ul>'
                    '<li>Управление яркостью LED</li>'
                    '<li>Управление скоростью двигателя постоянного тока</li>'
                    '<li>Управление сервоприводом (50 Гц, 1–2 мс импульс)</li>'
                    '<li>Синтез аналогового напряжения (с RC-фильтром = простой ЦАП)</li>'
                    '<li>Управление нагревателем (симистор/MOSFET)</li>'
                    '</ul>'
                    '<h3>Настройка ШИМ на STM32 (CubeMX)</h3>'
                    '<p>Таймер TIM3, канал 1, PA6 (альтернативная функция):</p>'
                    '<pre><code>// CubeMX сгенерирует инициализацию. В main.c:\n// Запуск ШИМ:\nHAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);\n\n// Установка скважности 50%:\n// ARR (Auto Reload Register) = 999 → период 1000 тиков\n__HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, 500); // 50%\n\n// Плавное нарастание (fade in):\nfor (uint32_t duty = 0; duty <= 999; duty++) {\n    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, duty);\n    HAL_Delay(2); // 2 сек на полный цикл\n}\n\n// Частота ШИМ:\n// f_PWM = f_APB1 / ((PSC+1) * (ARR+1))\n// При PSC=71, ARR=999: f_PWM = 36МГц / (72 * 1000) = 500 Гц</code></pre>'
                    '<h3>Управление сервоприводом</h3>'
                    '<pre><code>// Сервопривод: 50 Гц, 1мс=0°, 1.5мс=90°, 2мс=180°\n// ARR=19999, PSC=71 → f=50Гц (период 20мс)\nvoid servo_set_angle(uint8_t angle) {\n    // Маппинг 0–180° → CCR 1000–2000 (при ARR=19999, PSC=71)\n    uint32_t ccr = 1000 + (angle * 1000 / 180);\n    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, ccr);\n}</code></pre>'
                    '<div class="tip">Для управления MOSFET-ом от ШИМ: используй N-канальный (IRFZ44N, AO3400), '
                    'gate через 100 Ом резистор (ограничение броска тока), обратный диод на нагрузку.</div>'
                ),
            },
        ],
    },
    {
        'order': 10,
        'title': 'Практикум: подключение компонентов к МК — часть 2',
        'icon': 'fas fa-network-wired',
        'description': 'ПЗ №8-13: UART, датчики DHT/DS18B20, OLED, RTC, таймеры, RTOS',
        'lessons': [
            {
                'order': 1,
                'title': 'ПЗ №8-9: UART и беспроводные модули',
                'estimated_minutes': 30,
                'content': (
                    '<h2>ПЗ №8: UART — последовательный интерфейс</h2>'
                    '<h3>Параметры UART</h3>'
                    '<ul>'
                    '<li><strong>Baud rate:</strong> 9600, 115200, 921600 бод</li>'
                    '<li><strong>Биты данных:</strong> обычно 8</li>'
                    '<li><strong>Стоп-биты:</strong> 1 или 2</li>'
                    '<li><strong>Чётность:</strong> None/Even/Odd</li>'
                    '</ul>'
                    '<pre><code>// Отправка строки через HAL:\nconst char *msg = "Hello UART!\\r\\n";\nHAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), 100);\n\n// Приём с DMA (не блокирует CPU):\nuint8_t rx_buf[64];\nHAL_UART_Receive_DMA(&huart1, rx_buf, sizeof(rx_buf));\n\n// Callback DMA:\nvoid HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {\n    if (huart->Instance == USART1) {\n        process_received_data(rx_buf, sizeof(rx_buf));\n    }\n}</code></pre>'
                    '<h2>ПЗ №9: Модуль HC-05 (Bluetooth UART)</h2>'
                    '<ul>'
                    '<li>HC-05 — Bluetooth 2.0 SPP (Serial Port Profile)</li>'
                    '<li>Подключение: TX↔RX, RX↔TX (перекрёстно), VCC=3.3–5В</li>'
                    '<li>Скорость по умолчанию: 9600 бод (AT-команды) или 38400 бод (режим работы)</li>'
                    '</ul>'
                    '<pre><code>// AT-команды для настройки HC-05 (вывод EN на 3.3В при подаче питания):\n// AT+NAME=MyDevice  — установить имя\n// AT+PSWD=1234      — установить PIN\n// AT+UART=115200,0,0 — скорость 115200\n\n// В режиме работы — обычный UART:\nHAL_UART_Transmit(&huart1, (uint8_t*)"Temp: 23.5\\r\\n", 13, 100);\n// Данные отправляются на подключённый смартфон через Bluetooth</code></pre>'
                    '<h3>Популярные UART-модули</h3>'
                    '<table>'
                    '<tr><th>Модуль</th><th>Интерфейс</th><th>Стандарт</th><th>Дальность</th></tr>'
                    '<tr><td>HC-05/HC-06</td><td>UART</td><td>Bluetooth 2.0</td><td>10 м</td></tr>'
                    '<tr><td>ESP8266/ESP-01</td><td>UART</td><td>Wi-Fi 802.11 b/g/n</td><td>100 м</td></tr>'
                    '<tr><td>SIM800L</td><td>UART</td><td>GSM/GPRS</td><td>Сотовая сеть</td></tr>'
                    '<tr><td>nRF24L01</td><td>SPI</td><td>2.4 ГГц</td><td>100 м</td></tr>'
                    '</table>'
                    '<div class="tip">ESP8266 по UART: отправьте AT-команду, дождитесь ответа OK. Типовой баг: '
                    'потерял симфолы при высокой скорости — использовать DMA приём или уменьшить baud до 9600.</div>'
                ),
            },
            {
                'order': 2,
                'title': 'ПЗ №10-11: Датчики DHT22 и DS18B20',
                'estimated_minutes': 30,
                'content': (
                    '<h2>ПЗ №10: Датчик DHT22 (температура + влажность)</h2>'
                    '<h3>Интерфейс</h3>'
                    '<ul>'
                    '<li>Однопроводный (не 1-Wire) с собственным протоколом</li>'
                    '<li>40 бит данных: 16 бит RH + 16 бит T + 8 бит контрольная сумма</li>'
                    '<li>Интервал измерений: минимум 2 секунды</li>'
                    '<li>Точность: ±0.5°C, ±2% RH</li>'
                    '</ul>'
                    '<pre><code>// Библиотека DHT (PlatformIO: sensirion/arduino-dht)\n// Или реализация вручную через GPIO + HAL_GetTick:\n\nvoid DHT22_start_signal(void) {\n    // Установить шину как выход\n    GPIO_set_output(DHT_GPIO, DHT_PIN);\n    HAL_GPIO_WritePin(DHT_GPIO, DHT_PIN, GPIO_PIN_RESET);\n    HAL_Delay(1); // 1 мс LOW\n    HAL_GPIO_WritePin(DHT_GPIO, DHT_PIN, GPIO_PIN_SET);\n    // Переключить на вход (pull-up)\n    GPIO_set_input_pullup(DHT_GPIO, DHT_PIN);\n    delay_us(40); // Ждём ответ DHT\n}</code></pre>'
                    '<h2>ПЗ №11: DS18B20 (1-Wire протокол)</h2>'
                    '<ul>'
                    '<li>Dallas 1-Wire: данные, питание и земля — на одном проводе</li>'
                    '<li>Точность: ±0.5°C (от -10 до +85°C)</li>'
                    '<li>До 127 датчиков на одной шине (адресация ROM 64-бит)</li>'
                    '<li>Разрядность: 9–12 бит (настраивается)</li>'
                    '</ul>'
                    '<pre><code>// Использование библиотеки DS18B20:\n#include "ds18b20.h"\n\nfloat DS18B20_read_temp(void) {\n    ds18b20_convert_t(DS18B20_GPIO, DS18B20_PIN);\n    HAL_Delay(750); // Ждём конверсию при 12 бит\n    float temp;\n    ds18b20_read_t(DS18B20_GPIO, DS18B20_PIN, &temp);\n    return temp;\n}\n\n// Считать температуру:\nfloat t = DS18B20_read_temp();\nprintf("Temperature: %.1f C\\r\\n", t);</code></pre>'
                    '<h3>Сравнение датчиков температуры</h3>'
                    '<table>'
                    '<tr><th>Датчик</th><th>Интерфейс</th><th>Точность</th><th>Диапазон</th><th>Стоимость</th></tr>'
                    '<tr><td>DS18B20</td><td>1-Wire</td><td>±0.5°C</td><td>-55..+125°C</td><td>~100 руб</td></tr>'
                    '<tr><td>DHT22</td><td>Собственный</td><td>±0.5°C, ±2% RH</td><td>-40..+80°C</td><td>~150 руб</td></tr>'
                    '<tr><td>BMP280</td><td>I2C/SPI</td><td>±0.5°C</td><td>-40..+85°C</td><td>~100 руб</td></tr>'
                    '<tr><td>LM35</td><td>Аналоговый</td><td>±0.5°C</td><td>-55..+150°C</td><td>~50 руб</td></tr>'
                    '</table>'
                ),
            },
            {
                'order': 3,
                'title': 'ПЗ №12: OLED-дисплей и таймеры',
                'estimated_minutes': 25,
                'content': (
                    '<h2>ПЗ №12: OLED-дисплей SSD1306 (I2C)</h2>'
                    '<h3>Характеристики</h3>'
                    '<ul>'
                    '<li>Разрешение: 128×64 пикселей</li>'
                    '<li>Интерфейс: I2C (0x3C или 0x3D) или SPI</li>'
                    '<li>Питание: 3.3–5В</li>'
                    '<li>Видимость при любом освещении (эмиссивная технология)</li>'
                    '</ul>'
                    '<pre><code>// Библиотека SSD1306 (stm32-ssd1306 от afiskon):\n#include "ssd1306.h"\n\n// Инициализация:\nssd1306_Init();\n\n// Вывод текста:\nssd1306_Fill(Black);\nssd1306_SetCursor(0, 0);\nssd1306_WriteString("AlgorithmMaster", Font_7x10, White);\nssd1306_SetCursor(0, 20);\nssd1306_WriteString("T: 23.5 C", Font_7x10, White);\nssd1306_UpdateScreen(); // Передать буфер в дисплей\n\n// Рисование:\nssd1306_DrawLine(0, 15, 127, 15, White);\nssd1306_DrawRectangle(10, 30, 118, 60, White);\nssd1306_FillRectangle(12, 32, duty*116/100, 58, White); // Прогресс-бар</code></pre>'
                    '<h2>Таймеры STM32 — периодические задачи</h2>'
                    '<pre><code>// Обновлять дисплей каждую секунду через таймер:\n// TIM2: PSC=71, ARR=999 → прерывание каждую 1 мс\n// В CubeMX: TIM2 → mode Counter, Period 999, Prescaler 71\n// Включить NVIC TIM2 global interrupt\n\nuint32_t display_timer = 0;\n\nvoid HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {\n    if (htim->Instance == TIM2) {\n        display_timer++;\n        if (display_timer >= 1000) { // 1000 мс = 1 сек\n            display_timer = 0;\n            update_display_flag = 1; // Флаг для основного цикла\n        }\n    }\n}\n\n// В main loop:\nif (update_display_flag) {\n    update_display_flag = 0;\n    float t = DS18B20_read_temp();\n    // Обновить OLED\n}</code></pre>'
                    '<div class="tip">Не вызывайте HAL_Delay() внутри прерывания — он блокирует SysTick. '
                    'Вместо этого устанавливайте флаг в ISR и обрабатывайте в основном цикле.</div>'
                ),
            },
            {
                'order': 4,
                'title': 'ПЗ №13: FreeRTOS — основы RTOS для МК',
                'estimated_minutes': 30,
                'content': (
                    '<h2>ПЗ №13: FreeRTOS на STM32</h2>'
                    '<p>FreeRTOS — бесплатная RTOS (Real-Time Operating System) для МК. '
                    'Обеспечивает вытесняющую многозадачность, семафоры, очереди.</p>'
                    '<h3>Ключевые концепции</h3>'
                    '<table>'
                    '<tr><th>Концепция</th><th>Назначение</th><th>API</th></tr>'
                    '<tr><td>Задача (Task)</td><td>Независимый поток выполнения</td><td>xTaskCreate, vTaskDelete</td></tr>'
                    '<tr><td>Очередь (Queue)</td><td>Передача данных между задачами</td><td>xQueueCreate, xQueueSend, xQueueReceive</td></tr>'
                    '<tr><td>Семафор (Semaphore)</td><td>Синхронизация задач</td><td>xSemaphoreCreateBinary, xSemaphoreGive/Take</td></tr>'
                    '<tr><td>Мьютекс (Mutex)</td><td>Защита общих ресурсов</td><td>xSemaphoreCreateMutex</td></tr>'
                    '<tr><td>Таймер SW</td><td>Периодические события без таймеров МК</td><td>xTimerCreate, xTimerStart</td></tr>'
                    '</table>'
                    '<h3>Пример: две задачи на STM32 + FreeRTOS</h3>'
                    '<pre><code>#include "FreeRTOS.h"\n#include "task.h"\n#include "queue.h"\n\nQueueHandle_t sensor_queue;\n\n// Задача измерения температуры (высокий приоритет):\nvoid task_sensor(void *arg) {\n    float temp;\n    while (1) {\n        temp = DS18B20_read_temp();\n        xQueueSend(sensor_queue, &temp, 0);\n        vTaskDelay(pdMS_TO_TICKS(1000)); // Ждать 1 сек\n    }\n}\n\n// Задача обновления дисплея (низкий приоритет):\nvoid task_display(void *arg) {\n    float temp;\n    while (1) {\n        if (xQueueReceive(sensor_queue, &temp, pdMS_TO_TICKS(2000))) {\n            char buf[20];\n            sprintf(buf, "T: %.1f C", temp);\n            ssd1306_SetCursor(0, 20);\n            ssd1306_WriteString(buf, Font_7x10, White);\n            ssd1306_UpdateScreen();\n        }\n    }\n}\n\nint main(void) {\n    // ... инициализация ...\n    sensor_queue = xQueueCreate(5, sizeof(float));\n    xTaskCreate(task_sensor,  "Sensor",  256, NULL, 2, NULL);\n    xTaskCreate(task_display, "Display", 512, NULL, 1, NULL);\n    vTaskStartScheduler(); // Запуск планировщика\n    while (1); // Сюда не попадаем\n}</code></pre>'
                    '<h3>Настройка FreeRTOS через STM32CubeMX</h3>'
                    '<ol>'
                    '<li>Middleware → FreeRTOS → Interface: CMSIS_V2</li>'
                    '<li>Tasks and Queues → добавить задачи</li>'
                    '<li>Настроить heap_4 (рекомендуется), размер кучи 4–8 КБ</li>'
                    '<li>Generate Code → FreeRTOS настроен автоматически</li>'
                    '</ol>'
                    '<div class="tip">Минимальный стек задачи: 128 слов (512 байт для Cortex-M). '
                    'Stack overflow → ошибка vApplicationStackOverflowHook. '
                    'Используй uxTaskGetStackHighWaterMark() чтобы определить реальный размер стека.</div>'
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed РВЭС модули M8-M10: отладка/Git, практикумы компонентов к МК'

    def handle(self, *args, **options):
        subject = Subject.objects.filter(slug='rves').first()
        if not subject:
            self.stderr.write('Subject rves not found')
            return

        for mod_data in MODULES:
            lessons_data = mod_data.pop('lessons')
            module, created = TheoryModule.objects.update_or_create(
                subject=subject,
                order=mod_data['order'],
                defaults={**mod_data, 'subject': subject},
            )
            tag = 'created' if created else 'updated'
            self.stdout.write(f'  Module M{mod_data["order"]}: {mod_data["title"]} [{tag}]')

            for lesson in lessons_data:
                TheoryLesson.objects.update_or_create(
                    module=module,
                    order=lesson['order'],
                    defaults={**lesson, 'module': module},
                )
            self.stdout.write(f'    → {len(lessons_data)} lessons')
            mod_data['lessons'] = lessons_data

        self.stdout.write(self.style.SUCCESS('Done: РВЭС M8-M10 seeded'))
