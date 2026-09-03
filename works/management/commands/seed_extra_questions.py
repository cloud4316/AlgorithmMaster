from django.core.management.base import BaseCommand
from works.models import Quiz, Question, AnswerChoice

# Extra questions (6 per quiz) to bring totals from 4 to 10
EXTRA_QUESTIONS = {
    1: [  # Переменные и типы данных
        {'text': 'Какой тип данных используется для хранения вещественных чисел?', 'exp': 'float используется для чисел с плавающей точкой.', 'choices': [('float', True), ('int', False), ('str', False), ('bool', False)]},
        {'text': 'Что выведет: type(3.14)?', 'exp': 'type() возвращает класс объекта; 3.14 — это float.', 'choices': [('<class \'float\'>', True), ('<class \'int\'>', False), ('<class \'str\'>', False), ('<class \'number\'>', False)]},
        {'text': 'Как преобразовать строку в число?', 'exp': 'int("5") или float("3.14") преобразуют строки в числа.', 'choices': [('int("5")', True), ('number("5")', False), ('"5".toInt()', False), ('convert("5")', False)]},
        {'text': 'Какое значение имеет переменная x после: x = 10; x = x + 5?', 'exp': 'x было 10, добавляем 5 → x = 15.', 'choices': [('15', True), ('10', False), ('5', False), ('Ошибка', False)]},
        {'text': 'Что такое неизменяемый тип данных?', 'exp': 'Неизменяемый (immutable) — не может быть изменен после создания (str, tuple, int).', 'choices': [('Тип, значение которого нельзя изменить после создания', True), ('Тип, который нельзя удалить', False), ('Тип, который нельзя копировать', False), ('Тип, который работает быстрее', False)]},
        {'text': 'Какой будет результат: "5" + "3"?', 'exp': 'Конкатенация строк дает "53", не арифметическое сложение.', 'choices': [('\'53\'', True), ('8', False), ('Error', False), ('5.3', False)]},
    ],
    2: [  # Условные операторы
        {'text': 'Что выведет: if 5 > 3: print("да"); else: print("нет")?', 'exp': '5 > 3 истинно, выполнится первый блок.', 'choices': [('да', True), ('нет', False), ('5 > 3', False), ('Ошибка', False)]},
        {'text': 'Какой оператор проверяет неравенство в Python?', 'exp': '!= используется для проверки "не равно".', 'choices': [('!=', True), ('!==', False), ('<>', False), ('~=', False)]},
        {'text': 'Что вернет: 10 < 5 and 3 > 1?', 'exp': 'Первое ложно → весь and вернет False.', 'choices': [('False', True), ('True', False), ('None', False), ('Error', False)]},
        {'text': 'Что такое elif?', 'exp': 'elif — "else if"; проверяет дополнительное условие если предыдущее ложно.', 'choices': [('Второе условие if', True), ('Конец цикла', False), ('Else и if вместе', False), ('Выход из функции', False)]},
        {'text': 'Сколько значений в кортеже (True, False, None)?', 'exp': 'Это кортеж из трех значений, но в условиях учитывается только истинность.', 'choices': [('3', True), ('2', False), ('1', False), ('0', False)]},
        {'text': 'Что выведет: if not False: print("истина")?', 'exp': 'not False = True, блок if выполнится.', 'choices': [('истина', True), ('ложь', False), ('False', False), ('None', False)]},
    ],
    3: [  # Циклы
        {'text': 'Что выведет: for i in range(3): print(i)?', 'exp': 'range(3) → 0, 1, 2.', 'choices': [('0 1 2', True), ('1 2 3', False), ('0 1 2 3', False), ('3', False)]},
        {'text': 'Как выйти из цикла досрочно?', 'exp': 'break немедленно завершает цикл.', 'choices': [('break', True), ('exit', False), ('stop', False), ('return', False)]},
        {'text': 'Сколько раз выполнится цикл: for i in range(1, 5)?', 'exp': 'range(1, 5) → 1, 2, 3, 4 (четыре итерации).', 'choices': [('4 раза', True), ('5 раз', False), ('3 раза', False), ('Бесконечно', False)]},
        {'text': 'Что делает pass внутри цикла?', 'exp': 'pass — пустой оператор, ничего не делает (используется как заглушка).', 'choices': [('Ничего, это пустой оператор', True), ('Выходит из цикла', False), ('Пропускает итерацию', False), ('Повторяет цикл', False)]},
        {'text': 'Какой результат: x = 0; for _ in range(3): x += 2; print(x)?', 'exp': 'Три раза добавляем 2 → 0+2+2+2 = 6.', 'choices': [('6', True), ('2', False), ('3', False), ('0', False)]},
        {'text': 'Может ли цикл for иметь else блок?', 'exp': 'Да, else выполнится если цикл завершился нормально (без break).', 'choices': [('Да', True), ('Нет', False), ('Только для while', False), ('Только если есть if', False)]},
    ],
    4: [  # Функции
        {'text': 'Как объявить функцию в Python?', 'exp': 'def имя_функции(): — ключевое слово def для определения функции.', 'choices': [('def имя():', True), ('function имя():', False), ('func имя():', False), ('lambda имя():', False)]},
        {'text': 'Что возвращает функция без return?', 'exp': 'Функция без return возвращает None.', 'choices': [('None', True), ('Ошибка', False), ('0', False), ('пусто', False)]},
        {'text': 'Какой максимум параметров может быть у функции?', 'exp': 'Теоретически неограниченное количество (в Python 3.8+ до ~255-256 позиционных).', 'choices': [('Неограниченное', True), ('Максимум 10', False), ('Максимум 5', False), ('Только 1', False)]},
        {'text': 'Что такое параметр со значением по умолчанию?', 'exp': 'def func(x=5): — если x не передан, используется 5.', 'choices': [('Параметр с предустановленным значением', True), ('Параметр обязателен', False), ('Параметр константа', False), ('Параметр передается по ссылке', False)]},
        {'text': 'Что выведет: def f(x): return x*2; print(f(5))?', 'exp': 'f(5) возвращает 5*2 = 10.', 'choices': [('10', True), ('5', False), ('2', False), ('x*2', False)]},
        {'text': 'Может ли функция вызывать саму себя?', 'exp': 'Да, это называется рекурсией.', 'choices': [('Да, это рекурсия', True), ('Нет, это ошибка', False), ('Только внутри класса', False), ('Только один раз', False)]},
    ],
    5: [  # Алгоритмы сортировки
        {'text': 'Какова сложность сортировки вставками в среднем?', 'exp': 'Сортировка вставками — O(n²) в среднем и худшем случае.', 'choices': [('O(n²)', True), ('O(n)', False), ('O(n log n)', False), ('O(1)', False)]},
        {'text': 'Какой метод используется в быстрой сортировке (QuickSort)?', 'exp': 'QuickSort использует принцип "разделяй и властвуй" с выбором опорного элемента.', 'choices': [('Разделяй и властвуй', True), ('Слияние', False), ('Линейный поиск', False), ('Итерация', False)]},
        {'text': 'Какая сортировка гарантирует O(n log n) в любом случае?', 'exp': 'MergeSort гарантирует O(n log n) всегда.', 'choices': [('Сортировка слиянием', True), ('Быстрая сортировка', False), ('Пузырьковая сортировка', False), ('Сортировка выбором', False)]},
        {'text': 'Сколько операций нужно для сортировки массива из 100 элементов пузырьком (худший случай)?', 'exp': 'Пузырьковая O(n²) → примерно 10000 операций.', 'choices': [('~10000', True), ('~100', False), ('~700', False), ('~1000', False)]},
        {'text': 'Какая сортировка самая неэффективная?', 'exp': 'Пузырьковая сортировка считается самой простой, но неэффективной O(n²).', 'choices': [('Пузырьковая', True), ('Быстрая', False), ('Слияние', False), ('Вставками', False)]},
        {'text': 'Сортировка, которая требует дополнительное место O(n)?', 'exp': 'Сортировка слиянием требует дополнительное место для слияния.', 'choices': [('Слияние', True), ('Быстрая сортировка', False), ('Пузырьковая сортировка', False), ('Сортировка выбором', False)]},
    ],
}

class Command(BaseCommand):
    help = 'Добавляет дополнительные вопросы в тесты (6 вопросов на каждый тест для Python)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quiz-ids',
            type=str,
            default='1-5',
            help='Диапазон ID квизов (例: 1-5 или просто 1,2,3)'
        )

    def handle(self, *args, **options):
        quiz_ids = options['quiz_ids']

        # Парсим диапазон
        if '-' in quiz_ids:
            start, end = map(int, quiz_ids.split('-'))
            target_ids = range(start, end + 1)
        else:
            target_ids = [int(x.strip()) for x in quiz_ids.split(',')]

        added_count = 0
        for quiz_id in target_ids:
            if quiz_id not in EXTRA_QUESTIONS:
                self.stdout.write(f'[SKIP] Quiz {quiz_id} не в списке для добавления')
                continue

            quiz = Quiz.objects.filter(id=quiz_id).first()
            if not quiz:
                self.stdout.write(f'[ERROR] Quiz {quiz_id} не найден')
                continue

            current_count = quiz.questions.count()

            # Добавляем вопросы
            for idx, q_data in enumerate(EXTRA_QUESTIONS[quiz_id], start=1):
                q = Question.objects.create(
                    quiz=quiz,
                    text=q_data['text'],
                    explanation=q_data['exp'],
                    order=current_count + idx,
                )

                for choice_text, is_correct in q_data['choices']:
                    AnswerChoice.objects.create(
                        question=q,
                        text=choice_text,
                        is_correct=is_correct,
                    )
                added_count += 1

            new_count = quiz.questions.count()
            self.stdout.write(
                self.style.SUCCESS(f'[OK] Quiz {quiz_id} ({quiz.title[:40]}): '
                                 f'{current_count} -> {new_count} вопросов')
            )

        self.stdout.write(self.style.SUCCESS(f'\n[DONE] Всего добавлено {added_count} вопросов'))
