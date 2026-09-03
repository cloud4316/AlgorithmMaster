from django.core.management.base import BaseCommand
from works.models import Subject, TheoryLesson

class Command(BaseCommand):
    help = 'Расширяет контент первых 4 введенных модулей ОАИП'

    def handle(self, *args, **options):
        oaip = Subject.objects.get(title='ОАИП')

        # Дополнительный контент для каждого урока модулей 1-4
        expansions = {
            # Модуль 1: Введение в программирование
            ('Введение в программирование', 'Что такое программирование'): '''
            <h3>Подробнее о программировании</h3>
            <p>Программирование — это процесс создания инструкций для компьютера. Компьютер может выполнять миллионы операций в секунду, но ему нужны точные инструкции на понятном ему языке.</p>
            <p><strong>Этапы программирования:</strong></p>
            <ul>
            <li><strong>Понимание проблемы</strong> — определите, что нужно решить</li>
            <li><strong>Планирование алгоритма</strong> — разработайте последовательность шагов</li>
            <li><strong>Написание кода</strong> — переведите алгоритм на язык программирования</li>
            <li><strong>Тестирование</strong> — проверьте, работает ли программа правильно</li>
            <li><strong>Отладка</strong> — найдите и исправьте ошибки</li>
            </ul>
            <p>Хороший программист думает логически и разбивает сложные задачи на простые части.</p>
            ''',

            ('Введение в программирование', 'Python — первый язык программирования'): '''
            <h3>Почему Python?</h3>
            <p>Python выбран не случайно для обучения программированию:</p>
            <ul>
            <li><strong>Простой синтаксис</strong> — код читается почти как английский язык</li>
            <li><strong>Легко учить</strong> — минимум странных правил и символов</li>
            <li><strong>Универсален</strong> — используется в науке, веб, AI, автоматизации</li>
            <li><strong>Большое сообщество</strong> — много примеров и справки онлайн</li>
            </ul>
            <p><strong>История Python:</strong> Создан Гвидо ван Россумом в 1989 году. Название из сериала "Монти Пайтон" (юмор программистов!).</p>
            <p><strong>Где используется:</strong> Google, Instagram, Netflix, Spotify, NASA — все они используют Python.</p>
            ''',

            ('Введение в программирование', 'Как установить Python'): '''
            <h3>Пошаговая установка</h3>
            <ol>
            <li>Перейдите на <code>www.python.org</code></li>
            <li>Нажмите "Downloads" и выберите версию 3.12+ (не 2.x, это старая версия)</li>
            <li>Запустите установщик</li>
            <li><strong>ВАЖНО:</strong> Поставьте галку "Add Python to PATH"</li>
            <li>Нажмите "Install Now"</li>
            </ol>
            <p><strong>Проверка установки:</strong> откройте Command Prompt (Windows) или Terminal (Mac/Linux) и введите:</p>
            <pre>python --version</pre>
            <p>Должна появиться версия Python (например, Python 3.12.0)</p>
            ''',

            ('Введение в программирование', 'Первая программа Hello World'): '''
            <h3>Легенда Hello World</h3>
            <p>Программу "Hello World" создали в 1974 году. Это традиция — первая программа на новом языке всегда выводит "Hello, World!".</p>
            <p><strong>Почему это важно:</strong></p>
            <ul>
            <li>Доказывает что Python установлен и работает</li>
            <li>Показывает как выводить текст</li>
            <li>Учит основной синтаксис</li>
            </ul>
            <p><strong>Расширение программы:</strong> Вместо просто вывода текста, можно:</p>
            <pre>name = input("Как вас зовут? ")
print("Привет, " + name + "!")</pre>
            <p>Теперь программа интерактивна — общается с пользователем!</p>
            ''',
        }

        updated = 0
        skipped = 0

        # Получаем модули 1-4
        modules = list(oaip.modules.order_by('order')[:4])

        for module in modules:
            for lesson in module.lessons.order_by('order'):
                key = (module.title, lesson.title)

                if key in expansions:
                    # Проверяем есть ли уже расширение
                    if expansions[key] not in lesson.content:
                        # Добавляем в конец контента
                        lesson.content += expansions[key]
                        lesson.save()
                        updated += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'[+] M{module.order}L{lesson.order}: {lesson.title[:40]}'
                        ))
                    else:
                        skipped += 1
                        self.stdout.write(f'[SKIP] M{module.order}L{lesson.order}: already expanded')

        self.stdout.write(self.style.SUCCESS(
            f'\n[DONE] Updated: {updated}, Skipped: {skipped}'
        ))
