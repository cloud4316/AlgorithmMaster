"""
Нормализует поле group у всех UserProgress к каноническому списку групп.
Запуск: python manage.py normalize_groups [--dry-run]
"""
from django.core.management.base import BaseCommand
from works.models import UserProgress
from works.group_utils import normalize_group, CANONICAL_GROUPS


class Command(BaseCommand):
    help = 'Нормализует названия групп студентов к каноническому списку'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Показать что изменится, не сохранять')

    def handle(self, *args, **options):
        dry = options['dry_run']
        changed = 0
        unknown = []

        for p in UserProgress.objects.exclude(group='').select_related('user'):
            original = p.group
            normalized = normalize_group(original)
            if normalized != original:
                self.stdout.write(
                    f"  [{p.user.last_name} {p.user.first_name}] "
                    f"{original!r} → {normalized!r}"
                )
                if not dry:
                    p.group = normalized
                    p.save(update_fields=['group'])
                changed += 1
            elif normalized not in CANONICAL_GROUPS and normalized:
                unknown.append((p.user.get_full_name(), normalized))

        if unknown:
            self.stdout.write(self.style.WARNING(
                f'\nНе удалось нормализовать ({len(unknown)} шт.):'
            ))
            for name, grp in unknown:
                self.stdout.write(f'  {name}: {grp!r}')

        suffix = ' (dry-run, не сохранено)' if dry else ''
        self.stdout.write(self.style.SUCCESS(
            f'\nИзменено: {changed}{suffix}'
        ))
