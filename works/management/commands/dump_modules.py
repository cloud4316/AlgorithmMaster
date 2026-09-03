from django.core.management.base import BaseCommand
from works.models import Subject

class Command(BaseCommand):
    help = 'Dump module/lesson structure to file'

    def handle(self, *args, **options):
        oaip = Subject.objects.get(title__contains='ОАИП')
        out = []
        for m in oaip.modules.order_by('order'):
            ls = list(m.lessons.order_by('order'))
            total = sum(len(l.content or '') for l in ls)
            out.append(f'M{m.order}: {m.title} | lessons={len(ls)} | chars={total}')
            for l in ls:
                clen = len(l.content or '')
                out.append(f'  L{l.order}: {l.title} | {clen} chars')

        with open('module_dump.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(out))
        self.stdout.write('[DONE] Written to module_dump.txt')
