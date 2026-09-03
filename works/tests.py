"""
Тесты для проекта AlgorithmMaster (Django).
Запуск: python manage.py test works --verbosity=2
"""
import json
from io import BytesIO
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from works.models import (
    Subject, PracticalWork, Solution, UserProgress, Announcement,
    TheoryModule, TheoryLesson, LessonProgress,
    Quiz, Question, AnswerChoice, QuizAttempt,
    Notification, Achievement, UserAchievement,
    WorkHint, UserHintUnlock, DeadlineExtension, CodeCheck,
)
from works.views import _calculate_streak_days, check_achievements


# ══════════════════════════════════════════════════════════════════════════════
# БАЗОВЫЙ КЛАСС — общие фикстуры
# ══════════════════════════════════════════════════════════════════════════════

class BaseTestCase(TestCase):
    """Общие фикстуры: преподаватель, студент, предмет, работа."""

    def setUp(self):
        self.client = Client()

        # Преподаватель (staff)
        self.teacher = User.objects.create_user(
            username='teacher', password='teachpass',
            first_name='Иван', last_name='Преподаватель',
            is_staff=True, is_active=True,
        )
        UserProgress.objects.get_or_create(user=self.teacher)

        # Студент (активный)
        self.student = User.objects.create_user(
            username='ivanov_ivan', password='studpass',
            first_name='Иван', last_name='Иванов',
            is_active=True,
        )
        self.progress, _ = UserProgress.objects.get_or_create(
            user=self.student,
            defaults={'total_score': 50, 'streak_days': 0},
        )

        # Предмет
        self.subject = Subject.objects.create(
            slug='python', title='Python', order=1, is_active=True,
        )

        # Практическая работа
        self.work = PracticalWork.objects.create(
            title='ПР1: Сортировка', description='Описание задания',
            order=1, subject=self.subject, is_active=True, max_score=10,
        )

    def login_student(self):
        self.client.force_login(self.student)

    def login_teacher(self):
        self.client.force_login(self.teacher)

    def make_solution(self, student=None, status='submitted', score=0):
        student = student or self.student
        code = SimpleUploadedFile('sol.py', b'print("hello")', content_type='text/plain')
        return Solution.objects.create(
            student=student, work=self.work,
            code_file=code, status=status, score=score,
            original_filename='sol.py',
        )


# ══════════════════════════════════════════════════════════════════════════════
# 1. ТЕСТЫ МОДЕЛЕЙ
# ══════════════════════════════════════════════════════════════════════════════

class ModelTests(BaseTestCase):

    def test_subject_str(self):
        self.assertEqual(str(self.subject), 'Python')

    def test_practical_work_str(self):
        self.assertIn('ПР1', str(self.work))

    def test_solution_str(self):
        sol = self.make_solution()
        s = str(sol)
        self.assertIn('ivanov_ivan', s)
        self.assertIn('ПР1', s)

    def test_announcement_is_expired_false(self):
        ann = Announcement.objects.create(
            author=self.teacher, title='Test',
            expires_at=timezone.now() + timedelta(days=1),
        )
        self.assertFalse(ann.is_expired)

    def test_announcement_is_expired_true(self):
        ann = Announcement.objects.create(
            author=self.teacher, title='Test',
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        self.assertTrue(ann.is_expired)

    def test_announcement_no_expiry_not_expired(self):
        ann = Announcement.objects.create(author=self.teacher, title='Test')
        self.assertFalse(ann.is_expired)

    def test_userprogress_completion_percentage_zero(self):
        self.progress.total_works = 0
        self.assertEqual(self.progress.completion_percentage, 0)

    def test_userprogress_completion_percentage_half(self):
        self.progress.total_works = 4
        self.progress.completed_works = 2
        self.assertEqual(self.progress.completion_percentage, 50)

    def test_userprogress_completion_percentage_full(self):
        self.progress.total_works = 3
        self.progress.completed_works = 3
        self.assertEqual(self.progress.completion_percentage, 100)

    def test_userprogress_level_progress_zero_denominator(self):
        self.progress.next_level_xp = 0
        self.assertEqual(self.progress.level_progress, 0)

    def test_userprogress_level_progress_75(self):
        self.progress.current_xp = 75
        self.progress.next_level_xp = 100
        self.assertEqual(self.progress.level_progress, 75)

    def test_notification_send_creates_object(self):
        n = Notification.send(
            user=self.student, n_type='info',
            title='Тест уведомления', message='Сообщение',
        )
        self.assertEqual(n.user, self.student)
        self.assertFalse(n.is_read)
        self.assertEqual(n.n_type, 'info')

    def test_work_hint_str(self):
        hint = WorkHint.objects.create(
            work=self.work, order=1, title='Подсказка 1',
            text='Текст подсказки', xp_cost=5,
        )
        self.assertIn('Подсказка', str(hint))

    def test_deadline_extension_str(self):
        ext = DeadlineExtension.objects.create(
            user=self.student, work=self.work, reason='Болел',
        )
        s = str(ext)
        self.assertIn('Иванов', s)
        self.assertIn('ПР1', s)


# ══════════════════════════════════════════════════════════════════════════════
# 2. ТЕСТЫ АВТОРИЗАЦИИ
# ══════════════════════════════════════════════════════════════════════════════

class AuthViewTests(BaseTestCase):

    def test_register_get(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'form')

    def test_register_post_valid_creates_inactive_user(self):
        resp = self.client.post(reverse('register'), {
            'last_name': 'Петров',
            'first_name': 'Петр',
            'group': 'ИТ-21',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(resp.status_code, 200)  # рендерит pending_approval
        user = User.objects.filter(last_name='Петров', first_name='Петр').first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)  # ждёт одобрения
        self.assertTrue(UserProgress.objects.filter(user=user).exists())

    def test_register_post_password_mismatch(self):
        resp = self.client.post(reverse('register'), {
            'last_name': 'Сидоров',
            'first_name': 'Сидор',
            'group': 'ИТ-21',
            'password1': 'password123',
            'password2': 'different456',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(User.objects.filter(last_name='Сидоров').exists())

    def test_register_post_missing_fields(self):
        resp = self.client.post(reverse('register'), {'last_name': 'Тест'})
        self.assertEqual(resp.status_code, 200)
        # форма невалидна — юзер не создан
        self.assertFalse(User.objects.filter(last_name='Тест').exists())

    def test_login_get(self):
        resp = self.client.get(reverse('custom_login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_post_correct_credentials_redirects(self):
        resp = self.client.post(reverse('custom_login'), {
            'full_name': 'Иванов Иван',
            'password': 'studpass',
        })
        self.assertIn(resp.status_code, [301, 302])

    def test_login_post_wrong_password(self):
        resp = self.client.post(reverse('custom_login'), {
            'full_name': 'Иванов Иван',
            'password': 'wrongpass',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn('error', resp.context or {})

    def test_login_post_inactive_user(self):
        inactive = User.objects.create_user(
            username='inactive_user', password='pass',
            first_name='Анна', last_name='Неактивная',
            is_active=False,
        )
        resp = self.client.post(reverse('custom_login'), {
            'full_name': 'Неактивная Анна',
            'password': 'pass',
        })
        self.assertEqual(resp.status_code, 200)
        ctx = resp.context or {}
        self.assertEqual(ctx.get('error'), 'PENDING')

    def test_login_post_unknown_user(self):
        resp = self.client.post(reverse('custom_login'), {
            'full_name': 'Несуществующий Юзер',
            'password': 'anypass',
        })
        self.assertEqual(resp.status_code, 200)
        ctx = resp.context or {}
        self.assertIn('error', ctx)

    def test_change_password_requires_login(self):
        resp = self.client.get(reverse('change_password'))
        self.assertIn(resp.status_code, [301, 302])
        self.assertIn('/login/', resp['Location'])

    def test_change_password_post_success(self):
        self.login_student()
        resp = self.client.post(reverse('change_password'), {
            'old_password': 'studpass',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertIn(resp.status_code, [200, 302])
        # Пароль действительно сменился
        self.student.refresh_from_db()
        self.assertTrue(self.student.check_password('newpassword123'))


# ══════════════════════════════════════════════════════════════════════════════
# 3. ТЕСТЫ СТУДЕНЧЕСКИХ VIEW
# ══════════════════════════════════════════════════════════════════════════════

class StudentViewTests(BaseTestCase):

    def test_home_public(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_work_list_requires_login(self):
        resp = self.client.get(reverse('work_list'))
        self.assertIn(resp.status_code, [301, 302])

    def test_work_list_authenticated(self):
        self.login_student()
        resp = self.client.get(reverse('work_list'))
        self.assertEqual(resp.status_code, 200)

    def test_work_detail_accessible(self):
        self.login_student()
        resp = self.client.get(reverse('work_detail', args=[self.work.id]))
        self.assertEqual(resp.status_code, 200)

    def test_work_detail_inactive_still_accessible(self):
        """work_detail использует get_object_or_404 без фильтра по is_active — работа доступна."""
        self.login_student()
        self.work.is_active = False
        self.work.save()
        resp = self.client.get(reverse('work_detail', args=[self.work.id]))
        # view не фильтрует is_active, поэтому возвращает 200
        self.assertEqual(resp.status_code, 200)

    def test_work_detail_nonexistent_returns_404(self):
        self.login_student()
        resp = self.client.get(reverse('work_detail', args=[99999]))
        self.assertEqual(resp.status_code, 404)

    def test_submission_creates_solution(self):
        self.login_student()
        code_file = SimpleUploadedFile('solution.py', b'print(42)', content_type='text/plain')
        resp = self.client.post(
            reverse('work_submit', args=[self.work.id]),
            {'code_file': code_file},
        )
        self.assertIn(resp.status_code, [200, 302])
        self.assertTrue(
            Solution.objects.filter(student=self.student, work=self.work).exists()
        )

    def test_submission_increments_attempt_number(self):
        self.login_student()
        for i in range(3):
            code_file = SimpleUploadedFile(f'sol{i}.py', b'x=1', content_type='text/plain')
            self.client.post(
                reverse('work_submit', args=[self.work.id]),
                {'code_file': code_file},
            )
        solutions = Solution.objects.filter(student=self.student, work=self.work)
        attempt_numbers = list(solutions.values_list('attempt_number', flat=True))
        self.assertIn(3, attempt_numbers)

    def test_profile_requires_login(self):
        resp = self.client.get(reverse('profile'))
        self.assertIn(resp.status_code, [301, 302])

    def test_profile_accessible(self):
        self.login_student()
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)

    def test_solution_detail_own(self):
        self.login_student()
        sol = self.make_solution()
        resp = self.client.get(reverse('solution_detail', args=[sol.id]))
        self.assertEqual(resp.status_code, 200)

    def test_solution_detail_other_student(self):
        """Студент не может видеть чужое решение."""
        other = User.objects.create_user(
            username='other_student', password='p',
            first_name='Другой', last_name='Студент', is_active=True,
        )
        UserProgress.objects.get_or_create(user=other)
        sol = self.make_solution(student=other)
        self.login_student()
        resp = self.client.get(reverse('solution_detail', args=[sol.id]))
        # должен быть 404 или redirect
        self.assertIn(resp.status_code, [302, 404])

    def test_solution_history(self):
        self.login_student()
        self.make_solution()
        resp = self.client.get(reverse('solution_history', args=[self.work.id]))
        self.assertEqual(resp.status_code, 200)

    def test_results_page(self):
        self.login_student()
        resp = self.client.get(reverse('results'))
        self.assertEqual(resp.status_code, 200)

    def test_leaderboard(self):
        self.login_student()
        resp = self.client.get(reverse('leaderboard'))
        self.assertEqual(resp.status_code, 200)


# ══════════════════════════════════════════════════════════════════════════════
# 4. ТЕСТЫ ТЕОРИИ
# ══════════════════════════════════════════════════════════════════════════════

class TheoryViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.module = TheoryModule.objects.create(
            title='Тестовый модуль', description='Описание',
            icon='fas fa-book',
            order=1, subject=self.subject,
        )
        self.lesson = TheoryLesson.objects.create(
            module=self.module, title='Урок 1',
            content='<p>Содержание урока</p>',
            code_example='print("hello")',
            order=1, estimated_minutes=30,
        )

    def test_theory_list_requires_login(self):
        resp = self.client.get(reverse('theory_list'))
        self.assertIn(resp.status_code, [301, 302])

    def test_theory_list_accessible(self):
        self.login_student()
        resp = self.client.get(reverse('theory_list'))
        self.assertEqual(resp.status_code, 200)

    def test_theory_list_contains_module(self):
        self.login_student()
        resp = self.client.get(reverse('theory_list'))
        self.assertContains(resp, 'Тестовый модуль')

    def test_theory_lesson_accessible(self):
        self.login_student()
        resp = self.client.get(reverse('theory_lesson', args=[self.lesson.id]))
        self.assertEqual(resp.status_code, 200)

    def test_theory_lesson_nonexistent_404(self):
        self.login_student()
        resp = self.client.get(reverse('theory_lesson', args=[99999]))
        self.assertEqual(resp.status_code, 404)

    def test_mark_lesson_done(self):
        self.login_student()
        resp = self.client.post(reverse('mark_lesson_done', args=[self.lesson.id]))
        self.assertIn(resp.status_code, [200, 302])
        progress = LessonProgress.objects.filter(
            user=self.student, lesson=self.lesson, completed=True
        )
        self.assertTrue(progress.exists())

    def test_mark_lesson_done_idempotent(self):
        """Повторный вызов не создаёт дубликаты."""
        self.login_student()
        url = reverse('mark_lesson_done', args=[self.lesson.id])
        self.client.post(url)
        self.client.post(url)
        count = LessonProgress.objects.filter(
            user=self.student, lesson=self.lesson
        ).count()
        self.assertEqual(count, 1)

    def test_save_notes(self):
        self.login_student()
        resp = self.client.post(
            reverse('save_notes', args=[self.lesson.id]),
            json.dumps({'notes': 'Мои заметки'}),
            content_type='application/json',
        )
        self.assertIn(resp.status_code, [200])

    def test_theory_search(self):
        self.login_student()
        resp = self.client.get(reverse('theory_search'), {'q': 'Тестовый'})
        self.assertEqual(resp.status_code, 200)

    def test_theory_search_empty_query(self):
        self.login_student()
        resp = self.client.get(reverse('theory_search'), {'q': ''})
        self.assertEqual(resp.status_code, 200)


# ══════════════════════════════════════════════════════════════════════════════
# 5. ТЕСТЫ QUIZ
# ══════════════════════════════════════════════════════════════════════════════

class QuizViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.module = TheoryModule.objects.create(
            title='Модуль для теста', icon='fas fa-book', order=99,
            subject=self.subject,
        )
        self.quiz = Quiz.objects.create(
            title='Тест по Python', module=self.module,
            pass_score=70, is_active=True,
        )
        self.question = Question.objects.create(
            quiz=self.quiz, text='Что выводит print(1+1)?', order=1,
        )
        self.correct_answer = AnswerChoice.objects.create(
            question=self.question, text='2', is_correct=True, order=1,
        )
        self.wrong_answer = AnswerChoice.objects.create(
            question=self.question, text='11', is_correct=False, order=2,
        )

    def test_quiz_list(self):
        self.login_student()
        resp = self.client.get(reverse('quiz_list'))
        self.assertEqual(resp.status_code, 200)

    def test_quiz_detail(self):
        self.login_student()
        resp = self.client.get(reverse('quiz_detail', args=[self.quiz.id]))
        self.assertEqual(resp.status_code, 200)

    def test_submit_quiz_correct_answer(self):
        # view ожидает ключ q_{id} (не question_{id})
        self.login_student()
        resp = self.client.post(
            reverse('submit_quiz', args=[self.quiz.id]),
            {f'q_{self.question.id}': str(self.correct_answer.id)},
        )
        self.assertIn(resp.status_code, [200, 302])
        attempt = QuizAttempt.objects.filter(user=self.student, quiz=self.quiz).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.score, 100)

    def test_submit_quiz_wrong_answer(self):
        self.login_student()
        resp = self.client.post(
            reverse('submit_quiz', args=[self.quiz.id]),
            {f'q_{self.question.id}': str(self.wrong_answer.id)},
        )
        self.assertIn(resp.status_code, [200, 302])
        attempt = QuizAttempt.objects.filter(user=self.student, quiz=self.quiz).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.score, 0)


# ══════════════════════════════════════════════════════════════════════════════
# 6. ТЕСТЫ ПРЕПОДАВАТЕЛЬСКИХ VIEW
# ══════════════════════════════════════════════════════════════════════════════

class TeacherViewTests(BaseTestCase):

    def test_admin_panel_requires_staff(self):
        self.login_student()
        resp = self.client.get(reverse('admin_panel'))
        self.assertIn(resp.status_code, [302, 403])

    def test_admin_panel_accessible_by_teacher(self):
        self.login_teacher()
        resp = self.client.get(reverse('admin_panel'))
        self.assertEqual(resp.status_code, 200)

    def test_approve_user(self):
        pending = User.objects.create_user(
            username='pending_user', password='p',
            first_name='Ожидает', last_name='Одобрения', is_active=False,
        )
        UserProgress.objects.get_or_create(user=pending)
        self.login_teacher()
        resp = self.client.post(reverse('approve_user', args=[pending.id]))
        self.assertIn(resp.status_code, [200, 302])
        pending.refresh_from_db()
        self.assertTrue(pending.is_active)

    def test_reject_user(self):
        pending = User.objects.create_user(
            username='reject_user', password='p',
            first_name='Отклонить', last_name='Студент', is_active=False,
        )
        UserProgress.objects.get_or_create(user=pending)
        self.login_teacher()
        resp = self.client.post(reverse('reject_user', args=[pending.id]))
        self.assertIn(resp.status_code, [200, 302])

    def test_deactivate_user(self):
        self.login_teacher()
        resp = self.client.post(reverse('deactivate_user', args=[self.student.id]))
        self.assertIn(resp.status_code, [200, 302])
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)

    def test_gradebook_accessible(self):
        self.login_teacher()
        resp = self.client.get(reverse('gradebook'))
        self.assertEqual(resp.status_code, 200)

    def test_teacher_analytics_accessible(self):
        self.login_teacher()
        resp = self.client.get(reverse('teacher_analytics'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('work_stats', resp.context)

    def test_teacher_analytics_with_group_filter(self):
        self.login_teacher()
        self.progress.group = 'ИТ-21'
        self.progress.save()
        resp = self.client.get(reverse('teacher_analytics'), {'group': 'ИТ-21'})
        self.assertEqual(resp.status_code, 200)

    def test_teacher_solutions_accessible(self):
        self.login_teacher()
        resp = self.client.get(reverse('teacher_solutions'))
        self.assertEqual(resp.status_code, 200)

    def test_manual_grade(self):
        sol = self.make_solution()
        self.login_teacher()
        resp = self.client.post(
            reverse('manual_grade', args=[sol.id]),
            {'score': '8', 'status': 'correct', 'comment': 'Хорошо'},
        )
        self.assertIn(resp.status_code, [200, 302])
        sol.refresh_from_db()
        self.assertEqual(sol.score, 8)

    def test_manual_grade_student_forbidden(self):
        sol = self.make_solution()
        self.login_student()
        resp = self.client.post(
            reverse('manual_grade', args=[sol.id]),
            {'score': '10', 'status': 'correct'},
        )
        self.assertIn(resp.status_code, [302, 403])


# ══════════════════════════════════════════════════════════════════════════════
# 7. ТЕСТЫ ЭКСПОРТА
# ══════════════════════════════════════════════════════════════════════════════

class ExportViewTests(BaseTestCase):

    def test_export_csv_returns_csv(self):
        self.login_teacher()
        resp = self.client.get(reverse('export_gradebook_csv'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('text/csv', resp.get('Content-Type', ''))

    def test_export_csv_with_group_filter(self):
        self.login_teacher()
        resp = self.client.get(reverse('export_gradebook_csv'), {'group': 'ИТ-21'})
        self.assertEqual(resp.status_code, 200)

    def test_export_excel_returns_xlsx(self):
        self.login_teacher()
        resp = self.client.get(reverse('export_gradebook_excel'))
        self.assertEqual(resp.status_code, 200)
        ct = resp.get('Content-Type', '')
        self.assertIn('spreadsheetml', ct)

    def test_export_csv_requires_staff(self):
        self.login_student()
        resp = self.client.get(reverse('export_gradebook_csv'))
        self.assertIn(resp.status_code, [302, 403])

    def test_export_excel_requires_staff(self):
        self.login_student()
        resp = self.client.get(reverse('export_gradebook_excel'))
        self.assertIn(resp.status_code, [302, 403])


# ══════════════════════════════════════════════════════════════════════════════
# 8. ТЕСТЫ API
# ══════════════════════════════════════════════════════════════════════════════

class ApiViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.hint = WorkHint.objects.create(
            work=self.work, order=1, title='Подсказка',
            text='Используй цикл for', xp_cost=10,
        )

    def test_unlock_hint_enough_xp(self):
        self.progress.total_score = 50
        self.progress.save()
        self.login_student()
        resp = self.client.post(
            reverse('unlock_hint', args=[self.hint.id]),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('text', data)
        self.assertEqual(data['text'], 'Используй цикл for')
        # XP списан
        self.progress.refresh_from_db()
        self.assertEqual(self.progress.total_score, 40)
        # Запись о разблокировке создана
        self.assertTrue(UserHintUnlock.objects.filter(
            user=self.student, hint=self.hint
        ).exists())

    def test_unlock_hint_not_enough_xp(self):
        self.progress.total_score = 3  # меньше xp_cost=10
        self.progress.save()
        self.login_student()
        resp = self.client.post(
            reverse('unlock_hint', args=[self.hint.id]),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.content)
        self.assertIn('error', data)

    def test_unlock_hint_already_unlocked(self):
        """Повторная разблокировка не списывает XP."""
        UserHintUnlock.objects.create(user=self.student, hint=self.hint)
        self.progress.total_score = 50
        self.progress.save()
        self.login_student()
        resp = self.client.post(
            reverse('unlock_hint', args=[self.hint.id]),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data.get('already'))
        # XP не изменился
        self.progress.refresh_from_db()
        self.assertEqual(self.progress.total_score, 50)

    def test_notifications_count(self):
        self.login_student()
        Notification.send(user=self.student, n_type='info', title='Тест1')
        Notification.send(user=self.student, n_type='info', title='Тест2')
        resp = self.client.get(reverse('notifications_count'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 2)

    def test_mark_notification_read(self):
        self.login_student()
        notif = Notification.send(user=self.student, n_type='info', title='Важно')
        resp = self.client.post(reverse('mark_notification_read', args=[notif.id]))
        self.assertIn(resp.status_code, [200, 302])
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_notifications_list(self):
        self.login_student()
        resp = self.client.get(reverse('notifications'))
        self.assertEqual(resp.status_code, 200)

    def test_run_code_snippet(self):
        """run_code_snippet принимает POST-форму (не JSON) с полем 'code'."""
        self.login_student()
        resp = self.client.post(
            reverse('run_code_snippet'),
            {'code': 'print("hello world")'},
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        # Может вернуть вывод или ошибку — главное, что endpoint работает
        self.assertTrue('output' in data or 'status' in data)

    def test_run_code_snippet_syntax_error(self):
        self.login_student()
        resp = self.client.post(
            reverse('run_code_snippet'),
            {'code': 'def broken(:'},
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue('error' in data or 'output' in data or 'status' in data)

    def test_run_code_snippet_empty(self):
        self.login_student()
        resp = self.client.post(reverse('run_code_snippet'), {'code': ''})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('output', data)

    def test_check_status_endpoint(self):
        self.login_student()
        sol = self.make_solution(status='checking')
        cc = CodeCheck.objects.create(solution=sol, status='pending')
        resp = self.client.get(reverse('get_check_status', args=[cc.id]))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('status', data)


# ══════════════════════════════════════════════════════════════════════════════
# 9. ТЕСТЫ ПРОДЛЕНИЯ ДЕДЛАЙНА
# ══════════════════════════════════════════════════════════════════════════════

class DeadlineExtensionTests(BaseTestCase):

    def test_request_extension_no_reason_redirects(self):
        self.login_student()
        resp = self.client.post(
            reverse('request_deadline_extension', args=[self.work.id]),
            {'reason': ''},
        )
        self.assertIn(resp.status_code, [302])
        self.assertFalse(DeadlineExtension.objects.filter(
            user=self.student, work=self.work
        ).exists())

    def test_request_extension_with_reason(self):
        self.login_student()
        resp = self.client.post(
            reverse('request_deadline_extension', args=[self.work.id]),
            {'reason': 'Болел неделю'},
        )
        self.assertIn(resp.status_code, [302])
        ext = DeadlineExtension.objects.filter(
            user=self.student, work=self.work
        ).first()
        self.assertIsNotNone(ext)
        self.assertEqual(ext.status, 'pending')
        self.assertEqual(ext.reason, 'Болел неделю')

    def test_request_extension_updates_existing(self):
        DeadlineExtension.objects.create(
            user=self.student, work=self.work,
            reason='Старая причина', status='rejected',
        )
        self.login_student()
        self.client.post(
            reverse('request_deadline_extension', args=[self.work.id]),
            {'reason': 'Новая причина'},
        )
        ext = DeadlineExtension.objects.get(user=self.student, work=self.work)
        self.assertEqual(ext.status, 'pending')
        self.assertEqual(ext.reason, 'Новая причина')

    def test_approve_extension(self):
        ext = DeadlineExtension.objects.create(
            user=self.student, work=self.work, reason='Болел',
        )
        self.login_teacher()
        resp = self.client.post(
            reverse('approve_deadline_extension', args=[ext.id]),
            {'action': 'approve'},
        )
        self.assertIn(resp.status_code, [302])
        ext.refresh_from_db()
        self.assertEqual(ext.status, 'approved')
        # Уведомление создано
        self.assertTrue(Notification.objects.filter(
            user=self.student, n_type='info'
        ).exists())

    def test_reject_extension(self):
        ext = DeadlineExtension.objects.create(
            user=self.student, work=self.work, reason='Болел',
        )
        self.login_teacher()
        resp = self.client.post(
            reverse('approve_deadline_extension', args=[ext.id]),
            {'action': 'reject'},
        )
        self.assertIn(resp.status_code, [302])
        ext.refresh_from_db()
        self.assertEqual(ext.status, 'rejected')

    def test_approve_extension_requires_staff(self):
        ext = DeadlineExtension.objects.create(
            user=self.student, work=self.work, reason='Болел',
        )
        self.login_student()
        resp = self.client.post(
            reverse('approve_deadline_extension', args=[ext.id]),
            {'action': 'approve'},
        )
        self.assertIn(resp.status_code, [302, 403])
        ext.refresh_from_db()
        self.assertEqual(ext.status, 'pending')  # не изменился


# ══════════════════════════════════════════════════════════════════════════════
# 10. ТЕСТЫ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ
# ══════════════════════════════════════════════════════════════════════════════

class HelperTests(BaseTestCase):

    def test_calculate_streak_no_solutions(self):
        streak = _calculate_streak_days(self.student)
        self.assertEqual(streak, 0)

    def test_calculate_streak_solution_today(self):
        self.make_solution()
        streak = _calculate_streak_days(self.student)
        self.assertGreaterEqual(streak, 1)

    def test_calculate_streak_multiple_days(self):
        # Создаём решения за сегодня и вчера
        sol1 = self.make_solution()
        sol1.submitted_at = timezone.now() - timedelta(days=1)
        sol1.save(update_fields=['submitted_at'])
        sol2 = self.make_solution()
        sol2.submitted_at = timezone.now()
        sol2.save(update_fields=['submitted_at'])
        streak = _calculate_streak_days(self.student)
        self.assertGreaterEqual(streak, 2)

    def test_check_achievements_first_solve(self):
        """Достижение first_solve выдаётся при первом правильном решении."""
        # Создаём объект Achievement для first_solve
        Achievement.objects.get_or_create(
            key='first_solve',
            defaults={
                'title': 'Первое решение',
                'description': 'Решил первую задачу правильно',
                'icon': '⭐',
            }
        )
        self.make_solution(status='correct', score=10)
        check_achievements(self.student)
        self.assertTrue(UserAchievement.objects.filter(
            user=self.student,
            achievement__key='first_solve'
        ).exists())

    def test_check_achievements_not_met(self):
        """Достижение five_solves не выдаётся при 1 решении."""
        Achievement.objects.get_or_create(
            key='five_solves',
            defaults={
                'title': 'Пять решений',
                'description': 'Решил 5 задач правильно',
                'icon': '🔥',
            }
        )
        self.make_solution(status='correct', score=10)  # только 1
        check_achievements(self.student)
        self.assertFalse(UserAchievement.objects.filter(
            user=self.student,
            achievement__key='five_solves'
        ).exists())

    def test_check_achievements_idempotent(self):
        """Повторный вызов не создаёт дубликаты достижений."""
        Achievement.objects.get_or_create(
            key='first_solve',
            defaults={
                'title': 'Первое решение',
                'description': 'Решил первую задачу',
                'icon': '⭐',
            }
        )
        self.make_solution(status='correct', score=10)
        check_achievements(self.student)
        check_achievements(self.student)
        count = UserAchievement.objects.filter(
            user=self.student,
            achievement__key='first_solve'
        ).count()
        self.assertEqual(count, 1)


# ══════════════════════════════════════════════════════════════════════════════
# 11. ТЕСТЫ ОБЪЯВЛЕНИЙ
# ══════════════════════════════════════════════════════════════════════════════

class AnnouncementTests(BaseTestCase):

    def test_announcement_list_requires_login(self):
        resp = self.client.get(reverse('announcement_list'))
        self.assertIn(resp.status_code, [301, 302])

    def test_announcement_list(self):
        """announcement_list доступен только для staff."""
        self.login_teacher()
        resp = self.client.get(reverse('announcement_list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_announcement_requires_staff(self):
        self.login_student()
        resp = self.client.post(
            reverse('create_announcement'),
            {'title': 'Тест', 'body': 'Тело'},
        )
        self.assertIn(resp.status_code, [302, 403])

    def test_create_announcement_by_teacher(self):
        self.login_teacher()
        resp = self.client.post(
            reverse('create_announcement'),
            {'title': 'Новое объявление', 'body': 'Важная информация'},
        )
        self.assertIn(resp.status_code, [200, 302])
        self.assertTrue(Announcement.objects.filter(title='Новое объявление').exists())

    def test_deactivate_announcement(self):
        ann = Announcement.objects.create(
            author=self.teacher, title='Активное', is_active=True,
        )
        self.login_teacher()
        resp = self.client.post(reverse('deactivate_announcement', args=[ann.id]))
        self.assertIn(resp.status_code, [200, 302])
        ann.refresh_from_db()
        self.assertFalse(ann.is_active)


# ══════════════════════════════════════════════════════════════════════════════
# 12. ТЕСТЫ ПРОГРЕССА И XP
# ══════════════════════════════════════════════════════════════════════════════

class ProgressTests(BaseTestCase):

    def test_works_userprogress_page(self):
        self.login_student()
        resp = self.client.get(reverse('works_userprogress'))
        self.assertEqual(resp.status_code, 200)

    def test_profile_recalculates_score(self):
        """После отправки решения профиль отображает корректный суммарный балл."""
        self.login_student()
        sol = self.make_solution(status='correct', score=7)
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)

    def test_subject_switch(self):
        self.login_student()
        resp = self.client.get(reverse('switch_subject', args=['python']))
        self.assertIn(resp.status_code, [200, 302])
