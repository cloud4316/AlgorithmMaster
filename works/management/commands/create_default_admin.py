"""
Создаёт администратора admin/admin если его ещё нет.
Запуск: python manage.py create_default_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from works.models import UserProgress


class Command(BaseCommand):
    help = 'Создаёт администратора admin/admin (если не существует)'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write('  Администратор admin уже существует — пропускаем')
            return

        # first_name и last_name = 'admin', чтобы вход "admin admin" работал
        admin = User.objects.create_superuser(
            username='admin',
            password='admin',
            first_name='admin',
            last_name='admin',
            email='',
        )
        # Флаг: требует смены стандартного пароля
        UserProgress.objects.get_or_create(user=admin, defaults={'must_change_password': True})
        self.stdout.write(self.style.SUCCESS(
            'OK Создан администратор:\n'
            '   Поле входа  : admin admin  (Фамилия Имя через пробел)\n'
            '   Пароль      : admin\n'
            '   Смените пароль через кнопку в шапке сайта!'
        ))
