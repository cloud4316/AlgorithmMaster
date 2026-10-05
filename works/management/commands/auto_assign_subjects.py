from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from works.models import SubjectAccess, Subject, UserProgress

User = get_user_model()

GROUP_SUBJECT_MAP = [
    ('ИСП', ['python']),
    ('ССА', ['python']),
    ('РЭУ', ['mcu', 'rves']),
]

def slugs_for_group(group):
    g = group.upper()
    result = []
    for kw, slugs in GROUP_SUBJECT_MAP:
        if kw in g:
            result.extend(slugs)
    return result


class Command(BaseCommand):
    help = 'Assign subjects to students based on group name (ИСП/ССА->python, РЭУ->mcu+rves)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be done without saving')
        parser.add_argument('--overwrite', action='store_true', help='Replace existing SubjectAccess records')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        overwrite = options['overwrite']

        students = User.objects.filter(is_active=True, is_staff=False).select_related('userprogress')
        subjects_cache = {s.slug: s for s in Subject.objects.all()}

        assigned = 0
        skipped = 0

        for u in students:
            try:
                group = u.userprogress.group or ''
            except UserProgress.DoesNotExist:
                continue

            if not group:
                self.stdout.write(f'  {u.last_name}: no group — skip')
                skipped += 1
                continue

            slugs = slugs_for_group(group)
            if not slugs:
                self.stdout.write(f'  {u.last_name} [{group}]: no match — skip')
                skipped += 1
                continue

            existing = set(SubjectAccess.objects.filter(user=u).values_list('subject__slug', flat=True))

            for slug in slugs:
                subj = subjects_cache.get(slug)
                if not subj:
                    self.stderr.write(f'  Subject slug={slug} not found')
                    continue

                if slug in existing and not overwrite:
                    self.stdout.write(f'  {u.last_name} [{group}] -> {slug}: already assigned')
                    continue

                if not dry_run:
                    if overwrite:
                        SubjectAccess.objects.update_or_create(
                            user=u, subject=subj,
                            defaults={'role': 'student'},
                        )
                    else:
                        SubjectAccess.objects.get_or_create(
                            user=u, subject=subj,
                            defaults={'role': 'student'},
                        )

                self.stdout.write(
                    f'  {"[DRY]" if dry_run else "[OK] "} {u.last_name} [{group}] -> {slug}'
                )
                assigned += 1

        self.stdout.write(f'\nDone: {assigned} assigned, {skipped} skipped.')
