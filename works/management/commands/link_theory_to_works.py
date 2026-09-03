"""
Автоматически привязывает практические работы к модулям теории
по ключевым словам в названиях.
Запуск: python manage.py link_theory_to_works
"""
import re
from difflib import SequenceMatcher
from django.core.management.base import BaseCommand
from works.models import PracticalWork, TheoryModule, Subject


def normalize(text):
    """Нормализуем текст для сравнения."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def keyword_score(work_text, module_text):
    """Считаем score совпадения ключевых слов."""
    wt = set(normalize(work_text).split())
    mt = set(normalize(module_text).split())
    # Убираем стоп-слова
    stop = {'и', 'в', 'на', 'с', 'по', 'для', 'к', 'от', 'из', 'об',
            'пр', 'лр', 'работа', 'задание', 'модуль', 'урок', 'тема',
            'основы', 'введение', 'python', 'mps', 'оаип'}
    wt -= stop
    mt -= stop
    if not wt or not mt:
        return 0
    inter = wt & mt
    return len(inter) / max(len(wt), len(mt))


def seq_score(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


# Ручные маппинги: (subject_slug, work_order) -> keyword для поиска модуля
MANUAL_MAP = {
    # Python
    ('python', 1):  'переменные типы',
    ('python', 2):  'переменные типы',
    ('python', 3):  'цикл while',
    ('python', 4):  'цикл for',
    ('python', 5):  'функции',
    ('python', 6):  'строки символы',
    ('python', 7):  'словари множества',
    ('python', 8):  'сортировка алгоритмы',
    ('python', 9):  'сортировка алгоритмы',
    ('python', 10): 'поиск алгоритмы',
    ('python', 11): 'поиск алгоритмы',
    ('python', 12): 'рекурсия',
    ('python', 13): 'рекурсия',
    ('python', 14): 'связанные списки деревья',
    ('python', 15): 'файлы',
    # МПС / МК
    ('mcu', 1):  'gpio кнопки порты',
    ('mcu', 2):  'порты ввод вывод gpio',
    ('mcu', 3):  'uart',
    ('mcu', 4):  'шим таймеры прерывания',
    ('mcu', 5):  'дисплеи индикаторы',
    ('mcu', 6):  'дисплеи lcd',
    ('mcu', 7):  'i2c spi',
    ('mcu', 8):  'uart',
    ('mcu', 9):  'spi i2c',
    ('mcu', 10): 'измерение adc',
}


class Command(BaseCommand):
    help = 'Привязывает практические работы к модулям теории'

    def handle(self, *args, **options):
        linked = 0
        skipped = 0

        works = PracticalWork.objects.filter(is_active=True).select_related('subject')
        modules_by_subj = {}
        for m in TheoryModule.objects.filter(is_active=True).select_related('subject'):
            slug = m.subject.slug if m.subject else 'none'
            modules_by_subj.setdefault(slug, []).append(m)

        for work in works:
            subj_slug = work.subject.slug if work.subject else 'none'
            modules = modules_by_subj.get(subj_slug, [])
            if not modules:
                skipped += 1
                continue

            # Ищем ручной маппинг
            manual_kw = MANUAL_MAP.get((subj_slug, work.order))

            best_module = None
            best_score = 0.0

            for m in modules:
                if manual_kw:
                    # score по ручным ключевым словам
                    sc = keyword_score(manual_kw, m.title + ' ' + m.description)
                    sc2 = seq_score(manual_kw, m.title)
                    score = max(sc, sc2 * 0.8)
                else:
                    # автоматический скор
                    score = max(
                        keyword_score(work.title + ' ' + work.description[:200], m.title),
                        seq_score(work.title, m.title) * 0.7,
                    )
                if score > best_score:
                    best_score = score
                    best_module = m

            if best_module and best_score > 0.05:
                work.theory_module = best_module
                work.save(update_fields=['theory_module'])
                self.stdout.write(
                    f'  [{subj_slug}] #{work.order} "{work.title[:35]}"'
                    f'  ->  "{best_module.title[:40]}" ({best_score:.2f})'
                )
                linked += 1
            else:
                self.stdout.write(f'  [{subj_slug}] #{work.order} "{work.title[:35]}" -> не найдено')
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nGOTOVO: привязано {linked}, пропущено {skipped}'
        ))
