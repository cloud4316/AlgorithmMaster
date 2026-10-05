from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0028_pygrid_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='Запрошено')),
                ('seen_at', models.DateTimeField(blank=True, null=True, verbose_name='Просмотрено')),
                ('status', models.CharField(
                    choices=[('pending', 'Ожидает проверки'), ('seen', 'Просмотрено'), ('done', 'Проверено')],
                    default='pending', max_length=20, verbose_name='Статус',
                )),
                ('solutions_count', models.PositiveIntegerField(default=0, verbose_name='Кол-во решений')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий студента')),
                ('student', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='review_requests',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Студент',
                )),
            ],
            options={
                'verbose_name': 'Запрос на проверку',
                'verbose_name_plural': 'Запросы на проверку',
                'ordering': ['-requested_at'],
            },
        ),
    ]
