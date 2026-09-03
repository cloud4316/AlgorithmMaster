"""
Создаёт администратора если его ещё нет.
Запуск: python manage.py create_default_admin
"""
import os
import secrets
import string

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from works.models import UserProgress


def _generate_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class Command(BaseCommand):
    help = 'Создаёт администратора (если не существует)'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write('  Администратор admin уже существует -- пропускаем')
            return

        password = os.environ.get('DJANGO_ADMIN_PASSWORD') or _generate_password()

        admin = User.objects.create_superuser(
            username='admin',
            password=password,
            first_name='admin',
            last_name='admin',
            email='',
        )
        UserProgress.objects.get_or_create(user=admin, defaults={'must_change_password': True})
        self.stdout.write(self.style.SUCCESS(
            f'OK Создан администратор:\n'
            f'   Поле входа  : admin admin  (Фамилия Имя через пробел)\n'
            f'   Пароль      : {password}\n'
            f'   Смените пароль через кнопку в шапке сайта!'
        ))
