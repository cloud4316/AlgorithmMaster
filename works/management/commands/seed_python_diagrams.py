from django.core.management.base import BaseCommand
from works.models import TheoryLesson, Subject

class Command(BaseCommand):
    help = 'Добавляет SVG диаграммы в Python уроки'

    def handle(self, *args, **options):
        oaip = Subject.objects.get(title='ОАИП')
        lessons = TheoryLesson.objects.filter(module__subject=oaip).order_by('module__order', 'order')

        updated = 0
        for lesson in lessons:
            if lesson.content and '<svg' not in lesson.content:
                # Генерируем диаграмму на основе названия
                title = lesson.title.lower()

                if 'цикл' in title or 'while' in title or 'for' in title:
                    diagram = self.get_loop_diagram()
                elif 'функ' in title:
                    diagram = self.get_function_diagram()
                elif 'список' in title or 'массив' in title:
                    diagram = self.get_list_diagram()
                elif 'условие' in title or 'if' in title:
                    diagram = self.get_if_diagram()
                elif 'словарь' in title or 'dict' in title:
                    diagram = self.get_dict_diagram()
                elif 'ошибка' in title or 'исключение' in title:
                    diagram = self.get_error_diagram()
                else:
                    diagram = self.get_default_diagram()

                # Добавляем диаграмму после первого h2
                if '<h2>' in lesson.content:
                    parts = lesson.content.split('</h2>', 1)
                    lesson.content = parts[0] + '</h2>' + diagram + parts[1]
                else:
                    lesson.content = diagram + lesson.content

                lesson.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f'[+] M{lesson.module.order} L{lesson.order}: {lesson.title[:50]}'
                ))

        self.stdout.write(self.style.SUCCESS(f'\n[DONE] Dobavleno {updated} diagram'))

    def wrap_svg(self, title, svg_str):
        return f'<div style="overflow:auto;margin:1.5rem 0;text-align:center"><svg viewBox="0 0 600 300" style="max-width:100%;height:auto;border-radius:12px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.08))">{svg_str}</svg><p style="color:#64748b;font-size:13px;margin-top:8px">{title}</p></div>'

    def get_loop_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><circle cx="150" cy="150" r="50" fill="#667eea"/><text x="150" y="160" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Начало</text><line x1="200" y1="150" x2="280" y2="150" stroke="#667eea" stroke-width="2"/><circle cx="340" cy="150" r="50" fill="#ea580c"/><text x="340" y="160" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Условие</text><line x1="390" y1="150" x2="450" y2="150" stroke="#ea580c" stroke-width="2"/><circle cx="510" cy="150" r="50" fill="#16a34a"/><text x="510" y="160" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Конец</text><path d="M340,200 Q250,270 340,280" stroke="#ea580c" stroke-width="2" fill="none"/><text x="250" y="240" font-size="11" fill="#1e293b">Повтор</text>'
        return self.wrap_svg('Цикл - повторение кода', svg)

    def get_function_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="50" y="40" width="500" height="80" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/><text x="300" y="70" text-anchor="middle" font-size="13" fill="#1e293b" font-family="monospace" font-weight="bold">def greet(name):</text><text x="300" y="95" text-anchor="middle" font-size="11" fill="#1e293b">Определение функции</text><rect x="50" y="150" width="500" height="60" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="300" y="180" text-anchor="middle" font-size="13" fill="#1e293b" font-family="monospace" font-weight="bold">greet("Alice")</text><text x="300" y="200" text-anchor="middle" font-size="10" fill="#15803d">Вызов функции</text>'
        return self.wrap_svg('Функция - переиспользуемый код', svg)

    def get_list_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="40" y="40" width="520" height="60" rx="6" fill="#f3f4f6" stroke="#9ca3af" stroke-width="2"/><text x="300" y="75" text-anchor="middle" font-size="12" fill="#1e293b" font-family="monospace">arr = [10, 20, 30]</text><text x="60" y="130" font-size="11" fill="#6b7280" font-weight="bold">Индекс:  0    1    2</text><circle cx="80" cy="170" r="15" fill="#667eea"/><text x="80" y="177" text-anchor="middle" font-size="11" fill="white" font-weight="bold">10</text><circle cx="150" cy="170" r="15" fill="#667eea"/><text x="150" y="177" text-anchor="middle" font-size="11" fill="white" font-weight="bold">20</text><circle cx="220" cy="170" r="15" fill="#667eea"/><text x="220" y="177" text-anchor="middle" font-size="11" fill="white" font-weight="bold">30</text><text x="300" y="240" font-size="10" fill="#1e293b">arr[0]=10, arr[2]=30</text>'
        return self.wrap_svg('Список - упорядоченная коллекция', svg)

    def get_if_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><circle cx="300" cy="80" r="40" fill="#ea580c"/><text x="300" y="85" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Условие?</text><line x1="260" y1="120" x2="180" y2="180" stroke="#16a34a" stroke-width="2"/><text x="200" y="160" font-size="11" fill="#15803d">Да</text><rect x="100" y="180" width="160" height="60" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="180" y="215" text-anchor="middle" font-size="12" fill="#15803d" font-weight="bold">Блок if</text><line x1="340" y1="120" x2="420" y2="180" stroke="#dc2626" stroke-width="2"/><text x="400" y="160" font-size="11" fill="#991b1b">Нет</text><rect x="340" y="180" width="160" height="60" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="420" y="215" text-anchor="middle" font-size="12" fill="#991b1b" font-weight="bold">Блок else</text>'
        return self.wrap_svg('If-Else - ветвление кода', svg)

    def get_dict_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="40" y="40" width="520" height="60" rx="6" fill="#f3f4f6" stroke="#9ca3af" stroke-width="2"/><text x="300" y="75" text-anchor="middle" font-size="12" fill="#1e293b" font-family="monospace">d = {"name":"Alice", "age":25}</text><rect x="60" y="140" width="140" height="80" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/><text x="130" y="165" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold">Ключ: "name"</text><text x="130" y="190" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold">Значение: "Alice"</text><rect x="400" y="140" width="140" height="80" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/><text x="470" y="165" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold">Ключ: "age"</text><text x="470" y="190" text-anchor="middle" font-size="11" fill="#1e293b" font-weight="bold">Значение: 25</text>'
        return self.wrap_svg('Словарь - пары ключ-значение', svg)

    def get_error_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="20" y="20" width="560" height="100" rx="6" fill="#1e1e2e" stroke="#374151" stroke-width="2"/><text x="300" y="45" text-anchor="middle" font-size="11" fill="#8be9fd" font-family="monospace" font-weight="bold">Traceback (most recent call last):</text><text x="40" y="70" font-size="10" fill="#f8f8f2" font-family="monospace">File "prog.py", line 5</text><text x="40" y="90" font-size="10" fill="#f8f8f2" font-family="monospace">x = 10 / 0</text><rect x="20" y="140" width="560" height="140" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="300" y="170" text-anchor="middle" font-size="12" fill="#dc2626" font-weight="bold">ZeroDivisionError</text><text x="300" y="195" text-anchor="middle" font-size="11" fill="#991b1b">division by zero</text><text x="300" y="220" text-anchor="middle" font-size="10" fill="#991b1b">Тип ошибки + описание</text><text x="300" y="240" text-anchor="middle" font-size="10" fill="#991b1b">Помогает найти и исправить баг</text>'
        return self.wrap_svg('Исключение - ошибка во время выполнения', svg)

    def get_default_diagram(self):
        svg = '<rect width="600" height="300" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/><rect x="100" y="50" width="400" height="60" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/><text x="300" y="85" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="bold">Входные данные</text><line x1="300" y1="110" x2="300" y2="140" stroke="#3b82f6" stroke-width="2"/><rect x="100" y="140" width="400" height="60" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/><text x="300" y="175" text-anchor="middle" font-size="12" fill="#1e293b" font-weight="bold">Обработка</text><line x1="300" y1="200" x2="300" y2="230" stroke="#0284c7" stroke-width="2"/><rect x="100" y="230" width="400" height="60" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="300" y="265" text-anchor="middle" font-size="12" fill="#15803d" font-weight="bold">Выходные данные</text>'
        return self.wrap_svg('Алгоритм - последовательность действий', svg)
