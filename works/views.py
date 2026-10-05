import json
import logging
import os
import shutil
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.db.models import Count, Q, Avg, Max, Sum, F
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.password_validation import validate_password as _validate_password
from django.core.cache import cache
from .models import (PracticalWork, Solution, UserProgress, UserSession, PageView,
                     CodeCheck, TheoryModule, TheoryLesson, LessonProgress,
                     Quiz, Question, AnswerChoice, QuizAttempt,
                     Notification, TeacherComment,
                     Achievement, UserAchievement, WorkHint, UserHintUnlock,
                     DeadlineExtension, Subject, Announcement,
                     CircuitDraft, CircuitSolution, SubjectAccess, StudentProject,
                     CourseWork, PyGridScore, ReviewRequest)
from .code_runner import run_python_code, run_java_code, run_cpp_code, run_javascript_code
from .ai_checker import AICodeChecker
from .forms import SolutionForm, RegistrationForm, FullNameLoginForm, generate_username
from .utils import fix_file_encoding, save_file_with_correct_encoding
from .group_utils import normalize_group
from datetime import timedelta, datetime, date

logger = logging.getLogger('works')


def _safe_json(value):
    """json.dumps с экранированием </script> для вставки в HTML-страницы."""
    return json.dumps(value, ensure_ascii=False).replace('</', '<\\/')


def _read_solution_code(solution) -> str:
    """Читает текст из файла решения (код или .docx/.pdf)."""
    import os
    try:
        path = solution.code_file.path
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.docx', '.doc'):
            try:
                import docx
                doc = docx.Document(path)
                return '\n'.join(p.text for p in doc.paragraphs)
            except Exception:
                return '[Word-документ — установите python-docx для предпросмотра]'
        if ext == '.pdf':
            return '[PDF-файл — скачайте для просмотра]'
        return fix_file_encoding(path)
    except Exception:
        try:
            with solution.code_file.open('rb') as f:
                return f.read().decode('utf-8', errors='replace')
        except Exception:
            return ''


def _notify_email(user, subject, body):
    """Отправить email-уведомление пользователю (fail-safe)."""
    if not getattr(user, 'email', None):
        return
    try:
        from django.core.mail import send_mail
        from django.conf import settings as _settings
        send_mail(
            subject=subject,
            message=body,
            from_email=getattr(_settings, 'DEFAULT_FROM_EMAIL', 'noreply@algorithmmaster.local'),
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception:
        pass


# ── Достижения ────────────────────────────────────────────────────────────────

_ACHIEVEMENT_DEFS = [
    ('first_solve',      '⭐', 'Первый шаг',         'Сдай первое задание правильно',              10),
    ('five_solves',      '🔥', 'В ударе',             'Реши 5 заданий правильно',                   25),
    ('ten_solves',       '🏆', 'Практик',             'Реши 10 заданий правильно',                  50),
    ('twenty_solves',    '💪', 'Мастер решений',      'Реши 20 заданий правильно',                  80),
    ('theory_start',     '📚', 'Теоретик',            'Изучи первый урок теории',                   5),
    ('theory_ten',       '🧠', 'Знаток теории',       'Изучи 10 уроков теории',                     30),
    ('theory_fifty',     '🎓', 'Эрудит',              'Изучи 50 уроков теории',                     100),
    ('streak_3',         '⚡', 'Серия × 3',           'Заходи 3 дня подряд',                        15),
    ('streak_7',         '🚀', 'Недельная серия',     'Заходи 7 дней подряд',                       40),
    ('streak_14',        '🌟', 'Двухнедельная серия', 'Заходи 14 дней подряд',                      75),
    ('perfect_score',    '🎯', 'Перфекционист',       'Получи максимальный балл за задание',        20),
    ('quiz_first',       '❓', 'Первый тест',         'Пройди первый тест по теории',               10),
    ('quiz_master',      '🧩', 'Мастер тестов',       'Пройди 10 тестов по теории',                 40),
    ('speed_solver',     '⏱', 'Скоростной',          'Сдай задание в первый день публикации',       15),
    ('project_creator',  '🛠', 'Проектировщик',       'Создай и сохрани личный проект',              10),
]

def _ensure_achievements():
    """Создаёт записи Achievement если их нет."""
    for key, icon, title, desc, xp in _ACHIEVEMENT_DEFS:
        Achievement.objects.get_or_create(
            key=key,
            defaults={'title': title, 'description': desc, 'icon': icon, 'xp_reward': xp}
        )

def check_achievements(user):
    """Проверяет и выдаёт новые достижения пользователю."""
    try:
        _ensure_achievements()
        progress = UserProgress.objects.filter(user=user).first()
        if not progress:
            return
        correct_count = Solution.objects.filter(student=user, status='correct').count()
        theory_count  = LessonProgress.objects.filter(user=user, completed=True).count()
        quiz_count    = QuizAttempt.objects.filter(user=user, passed=True).count()
        has_perfect   = Solution.objects.filter(
            student=user, status='correct'
        ).filter(score__gte=F('work__max_score')).exists()
        has_project   = StudentProject.objects.filter(student=user).exists()

        conditions = {
            'first_solve':     correct_count >= 1,
            'five_solves':     correct_count >= 5,
            'ten_solves':      correct_count >= 10,
            'twenty_solves':   correct_count >= 20,
            'theory_start':    theory_count  >= 1,
            'theory_ten':      theory_count  >= 10,
            'theory_fifty':    theory_count  >= 50,
            'streak_3':        progress.streak_days >= 3,
            'streak_7':        progress.streak_days >= 7,
            'streak_14':       progress.streak_days >= 14,
            'perfect_score':   has_perfect,
            'quiz_first':      quiz_count >= 1,
            'quiz_master':     quiz_count >= 10,
            'project_creator': has_project,
        }
        existing = set(
            UserAchievement.objects.filter(user=user)
            .values_list('achievement__key', flat=True)
        )
        xp_gained = 0
        for key, met in conditions.items():
            if met and key not in existing:
                try:
                    ach = Achievement.objects.get(key=key)
                    UserAchievement.objects.create(user=user, achievement=ach)
                    xp_gained += ach.xp_reward
                    Notification.send(
                        user=user,
                        n_type='info',
                        title=f'Новое достижение: {ach.icon} {ach.title}',
                        message=ach.description,
                    )
                except Achievement.DoesNotExist:
                    pass
        if xp_gained and progress:
            progress.current_xp = (progress.current_xp or 0) + xp_gained
            while progress.current_xp >= progress.next_level_xp:
                progress.current_xp -= progress.next_level_xp
                progress.level += 1
                progress.next_level_xp = int(progress.next_level_xp * 1.5)
            progress.save(update_fields=['current_xp', 'level', 'next_level_xp'])
    except Exception:
        pass  # Не ломаем основной поток


def _sync_user_progress(user):
    """Пересчитать total_score, completed_works для пользователя из реальных данных."""
    try:
        progress, _ = UserProgress.objects.get_or_create(user=user)
        completed_works = Solution.objects.filter(
            student=user, status__in=['correct', 'partially_correct']
        ).values('work').distinct().count()
        practice_score = Solution.objects.filter(student=user).aggregate(Sum('score'))['score__sum'] or 0
        # Лучшие результаты тестов: score% / 10 = очки (100% = 10 очков)
        best_per_quiz = (
            QuizAttempt.objects.filter(user=user)
            .values('quiz_id')
            .annotate(best=Max('score'))
        )
        quiz_score = sum(round(r['best'] / 10) for r in best_per_quiz)
        progress.total_works = PracticalWork.objects.filter(is_active=True).count()
        progress.completed_works = completed_works
        progress.total_score = practice_score + quiz_score
        progress.average_score = practice_score / completed_works if completed_works > 0 else 0
        progress.save(update_fields=['total_works', 'completed_works', 'total_score', 'average_score'])
    except Exception:
        pass


def _active_announcements(request):
    """Вернуть активные объявления для текущего предмета + общие."""
    now = timezone.now()
    subject_slug = request.session.get('subject_slug', 'python')
    return Announcement.objects.filter(
        is_active=True
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=now)
    ).filter(
        Q(subject__isnull=True) | Q(subject__slug=subject_slug)
    ).select_related('author', 'subject').order_by('-created_at')[:5]


def home(request):  # Публичная страница — @login_required не нужен
    subjects = Subject.objects.filter(is_active=True)
    announcements = _active_announcements(request) if request.user.is_authenticated else []

    if request.user.is_authenticated:
        subject_slug = request.session.get('subject_slug', 'python')
        try:
            current_subject = Subject.objects.get(slug=subject_slug)
        except Subject.DoesNotExist:
            current_subject = subjects.first()

        # Статистика только по текущему предмету
        subj_works = PracticalWork.objects.filter(is_active=True, subject=current_subject)
        total_works = subj_works.count()
        completed_works = Solution.objects.filter(
            student=request.user,
            status__in=['correct', 'partially_correct'],
            work__subject=current_subject,
        ).values('work').distinct().count()
        total_score = Solution.objects.filter(student=request.user).aggregate(Sum('score'))['score__sum'] or 0

        _sync_user_progress(request.user)
        progress = UserProgress.objects.get(user=request.user)
        progress.streak_days = _calculate_streak_days(request.user)
        progress.save(update_fields=['streak_days'])
        check_achievements(request.user)

        # Реальные счётчики по предмету для быстрых действий
        subj_modules = TheoryModule.objects.filter(is_active=True, subject=current_subject)
        subj_lessons_count = sum(m.lessons.count() for m in subj_modules[:50])
        subj_quizzes_count = Quiz.objects.filter(is_active=True, module__subject=current_subject).count()

        context = {
            'progress': progress,
            'current_subject': current_subject,
            'total_works': total_works,
            'completed_works': completed_works,
            'subj_modules_count': subj_modules.count(),
            'subj_lessons_count': subj_lessons_count,
            'subj_works_count': total_works,
            'subj_quizzes_count': subj_quizzes_count,
            'highlight_works': subj_works.order_by('order')[:3],
            'subjects': subjects,
            'announcements': announcements,
            'current_subject_slug': subject_slug,
        }
    else:
        context = {
            'highlight_works': PracticalWork.objects.filter(is_active=True).order_by('order')[:3],
            'subjects': subjects,
        }
    return render(request, 'works/home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            username = generate_username(d['last_name'], d['first_name'])
            user = User.objects.create_user(
                username=username,
                password=d['password1'],
                first_name=d['first_name'],
                last_name=d['last_name'],
                is_active=False,   # ждёт подтверждения преподавателя
            )
            # Сохраняем группу в профиле
            progress = UserProgress.objects.create(user=user)
            if d.get('group'):
                progress.group = normalize_group(d['group'])
                progress.save()
            messages.success(request, 'Заявка отправлена')
            return render(request, 'works/pending_approval.html', {
                'full_name': f"{d['last_name']} {d['first_name']}",
                'group': d.get('group', ''),
            })
    else:
        form = RegistrationForm()
    return render(request, 'works/register.html', {'form': form})


def custom_login(request):
    """Вход по «Фамилия Имя» + пароль.
    Поддерживает два формата:
    — «Иванов Иван» (Фамилия Имя) — для студентов
    — «admin admin» или просто «admin» — для преподавателя/суперюзера
    """
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    form = FullNameLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        full_name = form.cleaned_data['full_name'].strip()
        password  = form.cleaned_data['password']

        user = None

        # 1. Пробуем FullNameBackend (Фамилия Имя)
        from works.backends import FullNameBackend
        backend = FullNameBackend()
        user = backend._find_user(full_name)

        # 2. Fallback: пробуем по username (для admin и суперюзеров)
        if user is None:
            from django.contrib.auth.models import User as _User
            # Если ввели "admin admin" — пробуем первое слово как username
            username_try = full_name.split()[0] if full_name else full_name
            user = _User.objects.filter(username__iexact=username_try).first()
            # Или точное совпадение всей строки с username
            if user is None:
                user = _User.objects.filter(username__iexact=full_name).first()

        if user is None:
            error = 'Пользователь не найден. Проверьте фамилию и имя.'
        elif not user.check_password(password):
            error = 'Неверный пароль.'
        elif not user.is_active:
            error = 'PENDING'
        else:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            next_url = request.GET.get('next', '')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')

    return render(request, 'works/login.html', {
        'form': form,
        'error': error,
    })


# ── Панель преподавателя ────────────────────────────────────────────────────

GROUP_SUBJECT_MAP = [
    # (substring_upper, [slugs])
    ('ИСП',  ['python']),
    ('ССА',  ['python']),
    ('РЭУ',  ['mcu', 'rves']),
]

def _subjects_for_group(group: str):
    """Вернуть QuerySet Subject по названию группы (автоопределение)."""
    group_up = group.upper()
    slugs = []
    for keyword, kw_slugs in GROUP_SUBJECT_MAP:
        if keyword in group_up:
            slugs.extend(kw_slugs)
    if slugs:
        return Subject.objects.filter(slug__in=slugs)
    return Subject.objects.none()


def _assign_subjects_by_group(user):
    """Назначить SubjectAccess студенту по его группе (если не назначены вручную)."""
    progress = getattr(user, 'userprogress', None)
    if not progress or not progress.group:
        return
    subjects = _subjects_for_group(progress.group)
    for subj in subjects:
        SubjectAccess.objects.get_or_create(user=user, subject=subj, defaults={'role': 'student'})


def _staff_required(view_func):
    """Декоратор: только для is_staff пользователей."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not request.user.is_staff:
            messages.error(request, 'Доступ запрещён.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@_staff_required
def admin_panel(request):
    """Панель преподавателя: управление регистрациями студентов."""
    pending  = User.objects.filter(is_active=False, is_staff=False).order_by('last_name', 'first_name')
    # list() — фиксируем объекты, чтобы шаблон не переоценивал queryset
    approved = list(
        User.objects.filter(is_active=True, is_staff=False)
        .order_by('last_name', 'first_name')
        .prefetch_related('subject_accesses__subject')
    )
    approved_ids = [u.id for u in approved]

    progress_map = {
        p.user_id: p
        for p in UserProgress.objects.filter(user_id__in=approved_ids).select_related('user')
    }

    # Практика: только решённые (correct/partially_correct), сумма баллов
    practice_stats = (
        Solution.objects.filter(
            student_id__in=approved_ids,
            status__in=['correct', 'partially_correct'],
        )
        .values('student_id')
        .annotate(total_score=Sum('score'), solved=Count('work', distinct=True))
    )
    practice_map = {r['student_id']: r for r in practice_stats}

    # Тесты: лучшая попытка по каждому тесту → среднее
    best_per_quiz = (
        QuizAttempt.objects.filter(user_id__in=approved_ids)
        .values('user_id', 'quiz_id')
        .annotate(best=Max('score'))
    )
    quiz_totals: dict[int, int] = {}
    quiz_counts: dict[int, int] = {}
    for r in best_per_quiz:
        uid = r['user_id']
        quiz_totals[uid] = quiz_totals.get(uid, 0) + r['best']
        quiz_counts[uid] = quiz_counts.get(uid, 0) + 1

    # Кол-во работ/тестов по каждому предмету
    works_per_subject: dict[int, int] = {}
    for row in PracticalWork.objects.filter(is_active=True).values('subject_id').annotate(cnt=Count('id')):
        if row['subject_id']:
            works_per_subject[row['subject_id']] = row['cnt']

    quizzes_per_subject: dict[int, int] = {}
    for row in Quiz.objects.filter(is_active=True).values('module__subject_id').annotate(cnt=Count('id')):
        if row['module__subject_id']:
            quizzes_per_subject[row['module__subject_id']] = row['cnt']

    # Подозрительные попытки тестов
    suspicious_map = {
        r['user_id']: r['cnt']
        for r in QuizAttempt.objects.filter(user_id__in=approved_ids, suspicious=True)
        .values('user_id').annotate(cnt=Count('id'))
    }

    for u in approved:
        u.progress = progress_map.get(u.id)
        p = practice_map.get(u.id, {})
        u.practice_solved = p.get('solved') or 0
        total_sc = p.get('total_score') or 0
        u.practice_avg = round(total_sc / u.practice_solved, 1) if u.practice_solved else None
        cnt = quiz_counts.get(u.id, 0)
        u.quiz_solved = cnt
        u.quiz_avg = round(quiz_totals.get(u.id, 0) / cnt, 1) if cnt else None
        # Считаем total по предметам студента
        sids = {sa.subject_id for sa in u.subject_accesses.all()}
        u.total_works   = sum(works_per_subject.get(s, 0) for s in sids)
        u.total_quizzes = sum(quizzes_per_subject.get(s, 0) for s in sids)
        u.suspicious_attempts = suspicious_map.get(u.id, 0)

    all_groups = list(
        UserProgress.objects.filter(group__gt='').values_list('group', flat=True)
        .distinct().order_by('group')
    )
    return render(request, 'works/admin_panel.html', {
        'pending':        pending,
        'approved':       approved,
        'all_subjects':   Subject.objects.filter(is_active=True).order_by('order'),
        'all_groups':     all_groups,
    })


@_staff_required
@require_http_methods(['POST'])
def approve_user(request, user_id):
    """Одобрить регистрацию студента."""
    user = get_object_or_404(User, id=user_id, is_staff=False)
    user.is_active = True
    user.save()
    UserProgress.objects.get_or_create(user=user)
    _assign_subjects_by_group(user)
    Notification.send(
        user=user, n_type='approved',
        title='Регистрация одобрена!',
        message='Преподаватель одобрил вашу регистрацию. Можете войти в систему.',
        link='/login/',
    )
    messages.success(request, f'Студент {user.last_name} {user.first_name} допущен.')
    _notify_email(
        user,
        'Добро пожаловать в AlgorithmMaster!',
        f'Здравствуйте, {user.first_name}!\n\nВаша регистрация одобрена. Можете войти на платформу.',
    )
    return redirect('admin_panel')


@_staff_required
@require_http_methods(['POST'])
def reject_user(request, user_id):
    """Отклонить и удалить заявку."""
    user = get_object_or_404(User, id=user_id, is_staff=False)
    name = f'{user.last_name} {user.first_name}'
    user.delete()
    messages.success(request, f'Заявка студента {name} отклонена.')
    return redirect('admin_panel')


@_staff_required
@require_http_methods(['POST'])
def deactivate_user(request, user_id):
    """Заблокировать студента."""
    user = get_object_or_404(User, id=user_id, is_staff=False)
    user.is_active = False
    user.save()
    messages.success(request, f'Студент {user.last_name} {user.first_name} заблокирован.')
    return redirect('admin_panel')


@_staff_required
def create_user(request):
    """Создать аккаунт студента вручную (без заявки)."""
    subjects = Subject.objects.filter(is_active=True).order_by('order')
    error = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        group      = request.POST.get('group', '').strip()
        password   = request.POST.get('password', '').strip()
        subject_ids = request.POST.getlist('subject_ids')
        role       = request.POST.get('role', 'student')  # 'student' или 'teacher'

        if not first_name or not last_name:
            error = 'Укажите имя и фамилию'
        elif len(password) < 6:
            error = 'Пароль должен быть не менее 6 символов'
        else:
            from .forms import generate_username
            from django.contrib.auth.password_validation import ValidationError as _PwdValidationError
            username = generate_username(last_name, first_name)
            # Временный объект для валидаторов (без сохранения в БД)
            _tmp_user = User(username=username, first_name=first_name, last_name=last_name)
            try:
                _validate_password(password, _tmp_user)
            except _PwdValidationError as _e:
                error = ' '.join(_e.messages)
                return render(request, 'works/create_user.html', {'subjects': subjects, 'error': error})
            new_user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=(role == 'teacher'),
            )
            progress = UserProgress.objects.create(
                user=new_user,
                group=normalize_group(group),
                must_change_password=True,  # пользователь должен сменить стандартный пароль
            )
            # Назначить доступ к предметам
            for sid in subject_ids:
                try:
                    subj = Subject.objects.get(id=int(sid))
                    SubjectAccess.objects.get_or_create(
                        user=new_user, subject=subj,
                        defaults={'role': role},
                    )
                except (Subject.DoesNotExist, ValueError):
                    pass
            # Если предметы не выбраны вручную — автоопределить по группе
            if not subject_ids and group and role == 'student':
                _assign_subjects_by_group(new_user)
            messages.success(request, f'Аккаунт {last_name} {first_name} создан. Логин: {username}')
            return redirect('admin_panel')

    return render(request, 'works/create_user.html', {
        'subjects': subjects,
        'error': error,
    })


@_staff_required
@require_http_methods(['POST'])
def set_subject_access(request, user_id):
    """Назначить/изменить доступ пользователя к предметам."""
    user = get_object_or_404(User, id=user_id)
    subject_ids = request.POST.getlist('subject_ids')
    role = request.POST.get('role', 'student')

    # Удалить старые доступы и назначить новые
    SubjectAccess.objects.filter(user=user).delete()
    for sid in subject_ids:
        try:
            subj = Subject.objects.get(id=int(sid))
            SubjectAccess.objects.create(user=user, subject=subj, role=role)
        except (Subject.DoesNotExist, ValueError):
            pass

    messages.success(request, f'Пользователь {user.last_name} {user.first_name} обновился.')
    return redirect('admin_panel')


@_staff_required
@require_http_methods(['POST'])
def bulk_subject_access(request):
    """Назначить доступ к предметам сразу всей группе."""
    group   = request.POST.get('group', '').strip()
    subject_ids = request.POST.getlist('subject_ids')
    role    = request.POST.get('role', 'student')
    if not group or not subject_ids:
        messages.error(request, 'Укажите группу и хотя бы один предмет.')
        return redirect('admin_panel')
    subjects = list(Subject.objects.filter(id__in=[int(s) for s in subject_ids if s.isdigit()]))
    users_in_group = User.objects.filter(
        is_active=True, is_staff=False,
        userprogress__group=group,
    )
    count = 0
    for u in users_in_group:
        SubjectAccess.objects.filter(user=u).delete()
        for subj in subjects:
            SubjectAccess.objects.create(user=u, subject=subj, role=role)
        count += 1
    messages.success(request, f'Группе {group}: назначено {len(subjects)} предм. для {count} студентов.')
    return redirect('admin_panel')


@_staff_required
@require_http_methods(['POST'])
def reset_password(request, user_id):
    """Сбросить пароль пользователя на заданный администратором."""
    user = get_object_or_404(User, id=user_id, is_staff=False)
    new_pw = request.POST.get('new_password', '').strip()
    if len(new_pw) < 6:
        messages.error(request, 'Пароль должен быть не менее 6 символов')
        return redirect('admin_panel')
    try:
        _validate_password(new_pw, user)
    except Exception as _e:
        messages.error(request, ' '.join(_e.messages) if hasattr(_e, 'messages') else str(_e))
        return redirect('admin_panel')
    user.set_password(new_pw)
    user.save()
    UserProgress.objects.filter(user=user).update(must_change_password=True)
    messages.success(request, f'Пароль {user.last_name} {user.first_name} сброшен.')
    return redirect('admin_panel')


@_staff_required
@require_http_methods(['POST'])
def reset_student_account(request, user_id):
    """Обнуляет прогресс студента: тесты, решения, очки, стрик."""
    from works.models import QuizAttempt, Solution, UserProgress, CodeCheck
    user = get_object_or_404(User, id=user_id, is_staff=False)
    what = request.POST.getlist('what')  # ['quizzes','solutions','progress']

    deleted = []
    if 'quizzes' in what:
        n, _ = QuizAttempt.objects.filter(user=user).delete()
        deleted.append(f'тестов: {n}')
    if 'solutions' in what:
        # удаляем CodeCheck привязанные к решениям студента
        CodeCheck.objects.filter(solution__student=user).delete()
        n, _ = Solution.objects.filter(student=user).delete()
        deleted.append(f'решений: {n}')
    if 'progress' in what or ('quizzes' in what and 'solutions' in what):
        UserProgress.objects.filter(user=user).update(
            total_score=0, level=1, streak_days=0,
        )
        deleted.append('прогресс обнулён')

    logger.warning('ADMIN RESET: %s обнулил аккаунт %s: %s',
                   request.user.username, user.username, ', '.join(deleted))
    messages.success(request, f'Аккаунт {user.last_name} {user.first_name} сброшен: {", ".join(deleted)}.')
    return redirect('admin_panel')


@_staff_required
@require_http_methods(['POST'])
def rename_user(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=False)
    first_name = request.POST.get('first_name', '').strip()
    last_name  = request.POST.get('last_name',  '').strip()
    if not first_name or not last_name:
        messages.error(request, 'Имя и фамилия не могут быть пустыми.')
        return redirect('admin_panel')
    old_name = f'{user.last_name} {user.first_name}'
    user.first_name = first_name
    user.last_name  = last_name
    user.save(update_fields=['first_name', 'last_name'])
    messages.success(request, f'Переименован: {old_name} → {user.last_name} {user.first_name}')
    return redirect('admin_panel')


@login_required
# ИСПРАВЛЕНО: убран @cache_page — кэшировал данные одного пользователя для всех
# и ломал AJAX-ответы (кэшировал первый тип ответа)
def work_list(request):
	is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
	has_filters = any([
		request.GET.get('q'),
		request.GET.get('difficulty') and request.GET.get('difficulty') != 'all',
		request.GET.get('topic') and request.GET.get('topic') != 'all',
		request.GET.get('sort') and request.GET.get('sort') != 'order'
	])
	subject_slug = request.session.get('subject_slug', 'python')
	qs = PracticalWork.objects.filter(is_active=True).select_related('subject').prefetch_related('solution_set')
	try:
		current_subject = Subject.objects.get(slug=subject_slug)
		qs = qs.filter(subject=current_subject)
	except Subject.DoesNotExist:
		current_subject = None
	q = request.GET.get('q')
	if q:
		qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
	difficulty = request.GET.get('difficulty')
	if difficulty in {'easy', 'medium', 'hard'}:
		qs = qs.filter(difficulty=difficulty)
	topic = request.GET.get('topic')
	if topic and topic != 'all':
		qs = qs.filter(topic=topic)
	sort = request.GET.get('sort')
	if sort == 'difficulty':
		qs = qs.order_by('difficulty', 'order')
	elif sort == 'deadline':
		qs = qs.order_by('deadline', 'order')
	else:
		qs = qs.order_by('order')
	user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
	is_mobile = any(device in user_agent for device in ['mobile', 'android', 'iphone', 'ipad'])
	is_tablet = any(device in user_agent for device in ['tablet', 'ipad'])
	if is_mobile:
		items_per_page = 6
	elif is_tablet:
		items_per_page = 9
	else:
		items_per_page = 15
	requested_items = request.GET.get('items_per_page')
	if requested_items and requested_items.isdigit():
		items_per_page = min(int(requested_items), 24)
	paginator = Paginator(qs, items_per_page)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	progress, _ = UserProgress.objects.get_or_create(user=request.user)
	user_solutions_raw = Solution.objects.filter(
		student=request.user,
		work__in=page_obj.object_list
	).select_related('work').order_by('work', '-submitted_at')
	user_solutions = {}
	for sol in user_solutions_raw:
		if sol.work_id not in user_solutions:
			user_solutions[sol.work_id] = sol
	works = list(page_obj.object_list)
	now = timezone.now()
	for work in works:
		user_solution = user_solutions.get(work.id)
		if user_solution:
			work.user_status = user_solution.status
			work.user_score = user_solution.score
			work.last_submission = user_solution.submitted_at
		else:
			work.user_status = 'not_started'
			work.user_score = 0
			work.last_submission = None
		work.is_overdue = bool(work.deadline and work.deadline < now and work.user_status not in ['correct', 'partially_correct'])
	if not has_filters:
		cache_key = f"user_stats_{request.user.id}"
		user_stats = cache.get(cache_key)
		if user_stats is None:
			solved_count = Solution.objects.filter(student=request.user, status__in=['correct', 'partially_correct']).values('work').distinct().count()
			in_progress_count = Solution.objects.filter(student=request.user, status__in=['submitted', 'checking']).values('work').distinct().count()
			user_stats = {'solved_count': solved_count, 'in_progress_count': in_progress_count}
			cache.set(cache_key, user_stats, 300)
		else:
			solved_count = user_stats['solved_count']
			in_progress_count = user_stats['in_progress_count']
	else:
		solved_count = Solution.objects.filter(student=request.user, status__in=['correct', 'partially_correct']).values('work').distinct().count()
		in_progress_count = Solution.objects.filter(student=request.user, status__in=['submitted', 'checking']).values('work').distinct().count()
	total_count = qs.count()
	topic_key_to_name = dict(PracticalWork.TOPIC_CHOICES)
	topics = qs.values('topic').annotate(cnt=Count('id')).order_by('topic')
	topic_filters = [
		{'key': row['topic'], 'name': topic_key_to_name.get(row['topic'], row['topic']), 'count': row['cnt']}
		for row in topics
	]
	context = {
		'works': works,
		'progress': progress,
		'page_obj': page_obj,
		'q': q or '',
		'difficulty': difficulty or 'all',
		'topic': topic or 'all',
		'sort': sort or 'order',
		'solved_count': solved_count,
		'in_progress_count': in_progress_count,
		'total_count': total_count,
		'topic_filters': topic_filters,
		'has_filters': has_filters,
		'items_per_page': items_per_page,
		'is_mobile': is_mobile,
		'is_tablet': is_tablet,
		'current_subject': current_subject,
	}
	if is_ajax:
		ajax_context = {
			'works': works, 'page_obj': page_obj,
			'q': q or '', 'difficulty': difficulty or 'all',
			'topic': topic or 'all', 'sort': sort or 'order',
			'total_count': total_count,
		}
		from django.template.loader import render_to_string
		html_content = render_to_string('works/works_grid.html', ajax_context, request=request)
		pagination_html = render_to_string('works/pagination.html', ajax_context, request=request)
		return JsonResponse({
			'html': html_content,
			'pagination': pagination_html,
			'current_page': page_obj.number,
			'total_pages': page_obj.paginator.num_pages,
			'total_count': total_count,
		})
	return render(request, 'works/work_list.html', context)


@login_required
def work_detail(request, work_id):
	work = get_object_or_404(PracticalWork, id=work_id)
	user_solutions = Solution.objects.filter(student=request.user, work=work).order_by('-submitted_at')
	best_solution = user_solutions.filter(status__in=['correct', 'partially_correct']).first()
	if request.method == 'POST':
		form = SolutionForm(request.POST, request.FILES)
		if form.is_valid():
			solution = form.save(commit=False)
			solution.student = request.user
			solution.work = work
			solution.original_filename = solution.code_file.name
			solution.status = 'submitted'
			solution.attempt_number = Solution.objects.filter(
				student=request.user, work=work
			).count() + 1
			solution.save()
			_fix_encoding_if_text(solution.code_file.path)
			# Автозапуск AI-чекера для docx/pdf
			_ext = os.path.splitext(solution.code_file.path)[1].lower()
			if _ext in ('.docx', '.pdf', '.doc'):
				import threading
				from works.models import CodeCheck
				from works.ai_checker import AICodeChecker
				from django.utils import timezone as _tz
				_cc = CodeCheck.objects.create(
					solution=solution, status='in_progress',
					check_type='auto', created_at=_tz.now()
				)
				def _run_doc_check(_sid, _cid):
					try:
						AICodeChecker().check_solution(_sid, _cid)
					except Exception:
						pass
				threading.Thread(target=_run_doc_check, args=(solution.id, _cc.id), daemon=True).start()
			messages.success(request, 'Решение отправлено')
			return redirect('solution_detail', solution_id=solution.id)
	else:
		form = SolutionForm()
	user_extension = None
	if request.user.is_authenticated and not request.user.is_staff:
		user_extension = DeadlineExtension.objects.filter(
			user=request.user, work=work
		).first()
	# Связанный модуль теории и другие работы модуля
	theory_module = work.theory_module
	module_works = list(
		PracticalWork.objects.filter(theory_module=theory_module, is_active=True).exclude(id=work.id)
	) if theory_module else []
	return render(request, 'works/work_detail.html', {
		'work': work, 'form': form, 'solutions': user_solutions,
		'best_solution': best_solution,
		'total_attempts': user_solutions.count(),
		'successful_attempts': user_solutions.filter(status__in=['correct', 'partially_correct']).count(),
		'now': timezone.now(),
		'user_extension': user_extension,
		'theory_module': theory_module,
		'module_works': module_works,
		'work_input_json': _safe_json(work.input_example or ''),
	})


@login_required
def submission(request, work_id):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'])
	work = get_object_or_404(PracticalWork, id=work_id)
	form = SolutionForm(request.POST, request.FILES)
	if form.is_valid():
		solution = form.save(commit=False)
		solution.student = request.user
		solution.work = work
		solution.original_filename = solution.code_file.name
		solution.status = 'submitted'
		solution.attempt_number = Solution.objects.filter(
			student=request.user, work=work
		).count() + 1
		solution.save()
		_fix_encoding_if_text(solution.code_file.path)
		messages.success(request, 'Решение отправлено')
		return render(request, 'works/submission.html', {'work': work, 'submission': solution})
	else:
		messages.error(request, 'Ошибка при загрузке файла')
		return redirect('work_detail', work_id=work_id)


_BINARY_EXTS = {'.docx', '.doc', '.pdf', '.xlsx', '.xls', '.zip', '.png', '.jpg', '.jpeg'}

def _fix_encoding_if_text(file_path: str) -> None:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in _BINARY_EXTS:
        return
    try:
        corrected = fix_file_encoding(file_path)
        save_file_with_correct_encoding(file_path, corrected)
    except Exception as e:
        print(f"Ошибка исправления кодировки: {e}")


def _calculate_streak_days(user, max_days=365):
    """Дни подряд: считается любой визит (UserSession) или сдача решения.
    Делаем два запроса вместо 2*N — получаем набор дат за max_days и идём по ним."""
    today = timezone.now().date()
    cutoff = today - timedelta(days=max_days)

    active_dates = set()
    active_dates.update(
        UserSession.objects.filter(user=user, start_time__date__gte=cutoff)
        .values_list('start_time__date', flat=True)
    )
    active_dates.update(
        Solution.objects.filter(student=user, submitted_at__date__gte=cutoff)
        .values_list('submitted_at__date', flat=True)
    )

    streak = 0
    check_date = today
    # Если сегодня активности нет — начинаем со вчера
    if check_date not in active_dates:
        check_date -= timedelta(days=1)
    while check_date in active_dates:
        streak += 1
        check_date -= timedelta(days=1)
    return streak


@login_required
def profile(request):
    user = request.user
    _sync_user_progress(user)
    solutions = Solution.objects.filter(student=user)
    total_attempts = solutions.count()
    successful_attempts = solutions.filter(status__in=['correct', 'partially_correct']).count()
    recent_solutions = solutions.select_related('work').order_by('-submitted_at')[:20]
    progress = UserProgress.objects.get(user=user)
    progress.streak_days = _calculate_streak_days(user)
    progress.save(update_fields=['streak_days'])
    total_works = progress.total_works
    completed_works = progress.completed_works
    raw_activity = []
    for i in range(6, -1, -1):
        day_dt = timezone.now() - timedelta(days=i)
        date_start = day_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = day_dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        day_sessions = UserSession.objects.filter(user=user, start_time__gte=date_start, start_time__lte=date_end)
        total_seconds = sum(session.duration_seconds for session in day_sessions)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        count = solutions.filter(submitted_at__date=day_dt.date()).count()
        raw_activity.append({'date': day_dt.strftime('%d.%m'), 'count': count, 'hours': hours, 'minutes': minutes, 'total_seconds': total_seconds})
    max_hours = max((d['hours'] for d in raw_activity), default=0)
    activity_data = []
    for d in raw_activity:
        height = 8 + int(d['hours'] * 92 / max_hours) if max_hours > 0 else 8
        activity_data.append({'date': d['date'], 'count': d['count'], 'hours': d['hours'], 'minutes': d['minutes'], 'height': height})
    topic_key_to_name = dict(PracticalWork.TOPIC_CHOICES)
    total_by_topic = PracticalWork.objects.filter(is_active=True).values('topic').annotate(cnt=Count('id'))
    total_map = {row['topic']: row['cnt'] for row in total_by_topic}
    solved_work_ids = Solution.objects.filter(student=user, status__in=['correct', 'partially_correct']).values_list('work_id', flat=True).distinct()
    solved_by_topic = PracticalWork.objects.filter(id__in=solved_work_ids).values('topic').annotate(cnt=Count('id'))
    solved_map = {row['topic']: row['cnt'] for row in solved_by_topic}
    topics_progress = []
    for topic_key, topic_name in topic_key_to_name.items():
        total = total_map.get(topic_key, 0)
        solved = solved_map.get(topic_key, 0)
        percent = round(solved * 100 / total) if total > 0 else 0
        topics_progress.append({'name': topic_name, 'progress': percent, 'solved': solved, 'total': total})
    user_achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement').order_by('-earned_at')
    all_achievements = Achievement.objects.all()
    earned_keys = set(ua.achievement.key for ua in user_achievements)
    check_achievements(request.user)
    return render(request, 'works/profile.html', {
        'progress': progress,
        'total_attempts': total_attempts,
        'successful_attempts': successful_attempts,
        'success_rate': round((successful_attempts / total_attempts * 100)) if total_attempts > 0 else 0,
        'recent_solutions': recent_solutions,
        'topics_progress': topics_progress,
        'activity_data': activity_data,
        'user_full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
        'user_joined': user.date_joined,
        'level_progress_percent': progress.level_progress,
        'user_achievements': user_achievements,
        'all_achievements': all_achievements,
        'earned_keys': earned_keys,
        'course_works': CourseWork.objects.filter(student=user).select_related('subject').order_by('-assigned_at'),
    })


@login_required
def student_profile(request, user_id):
    if not request.user.is_staff:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    student = get_object_or_404(User, id=user_id, is_staff=False)
    solutions = Solution.objects.filter(student=student).select_related('work').order_by('-submitted_at')
    quiz_attempts = QuizAttempt.objects.filter(user=student).select_related('quiz').order_by('-created_at')

    total_solutions = solutions.count()
    correct_solutions = solutions.filter(status__in=['correct', 'partially_correct']).count()
    total_score = solutions.aggregate(Sum('score'))['score__sum'] or 0
    quizzes_passed = quiz_attempts.filter(passed=True).count()

    def fmt_time(secs):
        if not secs:
            return None
        secs = int(secs)
        m, s = divmod(secs, 60)
        return f"{m}м {s:02d}с" if m else f"{s}с"

    raw_best = (
        QuizAttempt.objects.filter(user=student)
        .values('quiz__id', 'quiz__title')
        .annotate(best_score=Max('score'), attempts=Count('id'), avg_time=Avg('time_spent_seconds'))
        .order_by('quiz__title')
    )
    best_per_quiz = [
        {**row, 'avg_time_fmt': fmt_time(row['avg_time'])}
        for row in raw_best
    ]

    try:
        progress = UserProgress.objects.get(user=student)
    except UserProgress.DoesNotExist:
        progress = None

    return render(request, 'works/student_profile.html', {
        'student': student,
        'solutions': solutions,
        'quiz_attempts': quiz_attempts,
        'best_per_quiz': best_per_quiz,
        'total_solutions': total_solutions,
        'correct_solutions': correct_solutions,
        'total_score': total_score,
        'quizzes_passed': quizzes_passed,
        'progress': progress,
        'success_rate': round(correct_solutions * 100 / total_solutions) if total_solutions else 0,
        'course_works': CourseWork.objects.filter(student=student).select_related('subject').order_by('-assigned_at'),
    })


@login_required
@require_http_methods(["GET"])
def get_session_time(request):
    try:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        active_session = UserSession.objects.filter(user=request.user, session_key=session_key, is_active=True).first()
        if not active_session:
            return JsonResponse({'hours': 0, 'minutes': 0, 'seconds': 0, 'total_seconds': 0, 'status': 'no_session'})
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        today_sessions = UserSession.objects.filter(user=request.user, start_time__gte=today_start, start_time__lte=today_end)
        total_today_seconds = sum(session.duration_seconds for session in today_sessions)
        hours = total_today_seconds // 3600
        minutes = (total_today_seconds % 3600) // 60
        seconds = total_today_seconds % 60
        return JsonResponse({'hours': hours, 'minutes': minutes, 'seconds': seconds, 'total_seconds': total_today_seconds, 'status': 'success'})
    except Exception as e:
        return JsonResponse({'hours': 0, 'minutes': 0, 'seconds': 0, 'total_seconds': 0, 'status': 'error', 'error': str(e)})


@login_required
@require_http_methods(["GET"])
def get_activity_data(request):
    try:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=6)
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        active_session = UserSession.objects.filter(user=request.user, session_key=session_key, is_active=True).first()
        activity_data = []
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            # ИСПРАВЛЕНО: timezone.datetime не существует; используем datetime из stdlib
            day_start = timezone.make_aware(datetime.combine(current_date, datetime.min.time()))
            day_end = timezone.make_aware(datetime.combine(current_date, datetime.max.time()))
            day_sessions = UserSession.objects.filter(user=request.user, start_time__gte=day_start, start_time__lte=day_end)
            total_seconds = sum(session.duration_seconds for session in day_sessions)
            count = day_sessions.count()
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            height = min((total_seconds / (8 * 3600)) * 100, 100)
            activity_data.append({'date': current_date.strftime('%d.%m'), 'count': count, 'hours': hours, 'minutes': minutes, 'height': int(height), 'total_seconds': total_seconds})
        return JsonResponse({'activity_data': activity_data, 'status': 'success'})
    except Exception as e:
        return JsonResponse({'activity_data': [], 'status': 'error', 'error': str(e)})


@login_required
@require_http_methods(["POST"])
def check_code(request, solution_id):
    try:
        if request.user.is_staff:
            solution = Solution.objects.get(id=solution_id)
        else:
            solution = Solution.objects.get(id=solution_id, student=request.user)
        check_type = request.POST.get('check_type', 'auto')
        # Защита от двойного клика: если уже есть in_progress — возвращаем его
        existing = CodeCheck.objects.filter(
            solution=solution, status='in_progress'
        ).order_by('-created_at').first()
        if existing:
            return JsonResponse({'status': 'success', 'check_id': existing.id, 'message': 'Проверка уже запущена'})
        code_check = CodeCheck.objects.create(
            solution=solution, status='in_progress',
            check_type=check_type, created_at=timezone.now()
        )
        import threading
        def run_check():
            checker = AICodeChecker()
            checker.check_solution(solution_id, code_check_id=code_check.id)
        thread = threading.Thread(target=run_check)
        thread.daemon = True
        thread.start()
        return JsonResponse({'status': 'success', 'check_id': code_check.id, 'message': 'Проверка кода запущена'})
    except Solution.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Решение не найдено'})
    except Exception as e:
        logger.exception('check_code internal error')
        return JsonResponse({'status': 'error', 'message': 'Внутренняя ошибка сервера'})


@login_required
@require_http_methods(["GET"])
def get_check_status(request, check_id):
    try:
        code_check = CodeCheck.objects.get(id=check_id)
        if code_check.solution.student != request.user and not request.user.is_staff:
            return JsonResponse({'status': 'error', 'message': 'У вас нет доступа к этой проверке'}, status=403)
        response_data = {
            'status': 'success', 'check_status': code_check.status,
            'score': code_check.score, 'feedback': code_check.feedback,
            'suggestions': code_check.suggestions, 'errors': code_check.errors, 'warnings': code_check.warnings,
        }
        if code_check.completed_at:
            response_data['completed_at'] = code_check.completed_at.isoformat()
        return JsonResponse(response_data)
    except Exception as e:
        logger.exception('get_check_status internal error')
        return JsonResponse({'status': 'error', 'message': 'Внутренняя ошибка сервера'})


@login_required
@require_http_methods(["POST"])
def test_code_locally(request, work_id):
    try:
        work = get_object_or_404(PracticalWork, id=work_id)
        code_content = request.POST.get('code', '')
        if not code_content:
            return JsonResponse({'status': 'error', 'message': 'Код не предоставлен'})
        language = work.language.lower() if work.language else 'python'
        custom_stdin = request.POST.get('stdin', '').strip()
        input_data = custom_stdin if custom_stdin else (work.input_example or None)
        expected_output = (work.output_example or '').strip() if not custom_stdin else ''
        # ИСПРАВЛЕНО: раньше код записывался во временный файл и путь передавался
        # в run_python_code(file_path, work) — конфликт сигнатур с code_runner.
        # Теперь передаём строку с кодом напрямую в функции из code_runner.
        if language == 'python':
            result = run_python_code(code_content, input_data)
        elif language == 'java':
            result = run_java_code(code_content, input_data)
        elif language in ['cpp', 'c']:
            result = run_cpp_code(code_content, input_data)
        elif language == 'javascript':
            result = run_javascript_code(code_content, input_data)
        else:
            return JsonResponse({'status': 'error', 'message': f'Язык {language} не поддерживается'})
        if result['status'] == 'success':
            actual_output = result.get('output', '').strip()
            test_passed = (actual_output == expected_output) if expected_output else True
            return JsonResponse({
                'status': 'success', 'test_passed': test_passed,
                'input': input_data or '',
                'actual_output': actual_output, 'error_output': '',
                'execution_time': '< 1 сек',
                'message': 'Тест пройден!' if test_passed else 'Тест не пройден'
            })
        else:
            return JsonResponse({
                'status': 'error', 'test_passed': False,
                'message': result.get('error', 'Ошибка выполнения'),
                'error_output': result.get('error', ''),
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ошибка при тестировании: {str(e)}'})


@login_required
def results(request):
	solutions = Solution.objects.filter(student=request.user).order_by('-submitted_at')[:20]
	stats = {
		'total': Solution.objects.filter(student=request.user).count(),
		'solved': Solution.objects.filter(student=request.user, status__in=['correct', 'partially_correct']).count(),
	}
	return render(request, 'works/results.html', {'stats': stats, 'last_submissions': solutions})


@login_required
def works_userprogress(request):
    # ИСПРАВЛЕНО: убраны захардкоженные заглушки — теперь реальные данные из БД
    topic_key_to_name = dict(PracticalWork.TOPIC_CHOICES)
    total_by_topic = PracticalWork.objects.filter(is_active=True).values('topic').annotate(cnt=Count('id'))
    total_map = {row['topic']: row['cnt'] for row in total_by_topic}
    solved_work_ids = list(Solution.objects.filter(
        student=request.user, status__in=['correct', 'partially_correct']
    ).values_list('work_id', flat=True).distinct())
    solved_by_topic = PracticalWork.objects.filter(id__in=solved_work_ids).values('topic').annotate(cnt=Count('id'))
    solved_map = {row['topic']: row['cnt'] for row in solved_by_topic}
    topics = []
    for topic_key, topic_name in topic_key_to_name.items():
        total = total_map.get(topic_key, 0)
        solved = solved_map.get(topic_key, 0)
        percent = round(solved * 100 / total) if total > 0 else 0
        topics.append({'name': topic_name, 'percent': percent, 'solved': solved, 'total': total})
    stats = {
        'total': PracticalWork.objects.filter(is_active=True).count(),
        'solved': len(solved_work_ids),
    }
    return render(request, 'works/works_userprogress.html', {'topics': topics, 'stats': stats})


@login_required
def solution_detail(request, solution_id):
    solution = get_object_or_404(Solution, id=solution_id)
    if solution.student_id != request.user.id and not request.user.is_staff:
        return redirect('home')
    code = _read_solution_code(solution)
    user_solutions = Solution.objects.filter(student=solution.student, work=solution.work)
    best = user_solutions.order_by('-score').first()
    avg_score = user_solutions.aggregate(avg=Avg('score'))['avg'] or 0
    max_score = solution.work.max_score or 10
    # score is stored as percentage (0-100), convert to actual points
    user_best_score = round((best.score or 0) * max_score / 100) if best else 0
    user_avg_score = round(avg_score * max_score / 100, 1)
    ext = os.path.splitext(solution.code_file.name)[1].lower()
    is_doc_file = ext in {'.docx', '.doc', '.pdf'}
    if is_doc_file and solution.status == 'incorrect':
        solution.status = 'submitted'
        solution.save(update_fields=['status'])
    from works.models import CodeCheck
    last_check = CodeCheck.objects.filter(solution=solution).order_by('-created_at').first()
    return render(request, 'works/solution_detail.html', {
        'solution': solution,
        'solution_code': code,
        'solution_code_json': _safe_json(code or ''),
        'solution_code_lines': code.splitlines() if code else [],
        'is_teacher': request.user.is_staff,
        'user_attempt_count': user_solutions.count(),
        'user_best_score': user_best_score,
        'user_avg_score': user_avg_score,
        'is_doc_file': is_doc_file,
        'last_check': last_check,
    })


# ══════════════════════════════════════════════════════════════════════════════
# ТЕОРИЯ
# ══════════════════════════════════════════════════════════════════════════════

_PUBLIC_SUBJECT_SLUGS = {'asutps'}

def theory_list(request):
    subject_slug = request.session.get('subject_slug', 'python')
    try:
        current_subject = Subject.objects.get(slug=subject_slug)
    except Subject.DoesNotExist:
        current_subject = None

    is_public = current_subject and current_subject.slug in _PUBLIC_SUBJECT_SLUGS
    if not request.user.is_authenticated and not is_public:
        return redirect(f'/login/?next={request.path}')

    qs = TheoryModule.objects.filter(is_active=True).prefetch_related('lessons', 'quizzes')
    if current_subject:
        qs = qs.filter(subject=current_subject)
    modules = list(qs)

    if request.user.is_authenticated:
        completed_lesson_ids = set(
            LessonProgress.objects.filter(user=request.user, completed=True)
            .values_list('lesson_id', flat=True)
        )
        unlock_status = get_module_unlock_status(request.user, modules)
    else:
        completed_lesson_ids = set()
        unlock_status = {}

    for module in modules:
        total = module.lessons.count()
        done  = sum(1 for l in module.lessons.all() if l.id in completed_lesson_ids)
        module.progress_done  = done
        module.progress_total = total
        module.progress_pct   = round(done * 100 / total) if total else 0
        module.is_completed   = (total > 0 and done == total)
        module.unlock         = unlock_status.get(module.id, {'theory': True, 'quiz': True, 'locked': False})

    total_done    = sum(m.progress_done  for m in modules)
    total_lessons = sum(m.progress_total for m in modules)
    total_pct     = round(total_done * 100 / total_lessons) if total_lessons else 0

    return render(request, 'works/theory_list.html', {
        'modules': modules,
        'current_subject': current_subject,
        'subjects': Subject.objects.filter(is_active=True),
        'total_done': total_done,
        'total_lessons': total_lessons,
        'total_pct': total_pct,
    })


def theory_lesson(request, lesson_id):
    lesson = get_object_or_404(TheoryLesson.objects.select_related('module__subject'), id=lesson_id)
    module = lesson.module

    is_public = module.subject and module.subject.slug in _PUBLIC_SUBJECT_SLUGS
    if not request.user.is_authenticated and not is_public:
        return redirect(f'/login/?next={request.path}')

    # Все уроки модуля для навигации
    all_lessons = list(module.lessons.all())
    current_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson_id), 0)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    # Тесты для этого модуля
    module_quizzes = module.quizzes.filter(is_active=True)

    if request.user.is_authenticated:
        progress_obj = LessonProgress.objects.filter(user=request.user, lesson=lesson).first()
        is_completed = bool(progress_obj and progress_obj.completed)
        user_notes   = progress_obj.notes if progress_obj else ''
        completed_ids = set(LessonProgress.objects.filter(
            user=request.user, completed=True
        ).values_list('lesson_id', flat=True))
    else:
        is_completed = False
        user_notes   = ''
        completed_ids = set()

    done_count = sum(1 for l in all_lessons if l.id in completed_ids)
    total_count = len(all_lessons)
    progress_pct = round(done_count * 100 / total_count) if total_count else 0

    # Определяем язык кода для редактора по содержимому урока / теме модуля
    code = lesson.code_example or ''
    if any(kw in code for kw in ('#include', 'void setup()', 'void loop()', 'int main()', '::',
                                  'AVR', 'DDRD', 'PORTB', 'ISR(')):
        code_lang = 'cpp'
    elif 'public class' in code or 'System.out' in code:
        code_lang = 'java'
    elif 'console.log' in code or '=>' in code and 'def ' not in code:
        code_lang = 'javascript'
    else:
        code_lang = 'python'

    return render(request, 'works/theory_lesson.html', {
        'lesson': lesson,
        'module': module,
        'all_lessons': all_lessons,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'is_completed': is_completed,
        'current_index': current_index,
        'module_quizzes': module_quizzes,
        'completed_ids': completed_ids,
        'done_count': done_count,
        'total_count': total_count,
        'progress_pct': progress_pct,
        'user_notes': user_notes,
        'code_lang': code_lang,
    })


@login_required
@require_http_methods(["POST"])
def mark_lesson_done(request, lesson_id):
    lesson = get_object_or_404(TheoryLesson, id=lesson_id)
    obj, created = LessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson,
        defaults={'completed': True}
    )
    if not obj.completed:
        obj.completed = True
        obj.save()
    check_achievements(request.user)
    return JsonResponse({'status': 'ok', 'lesson_id': lesson_id})


# ── Конспекты ────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(["POST"])
def save_notes(request, lesson_id):
    lesson = get_object_or_404(TheoryLesson, id=lesson_id)
    try:
        data = json.loads(request.body)
        notes_text = data.get('notes', '')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'status': 'error', 'message': 'bad json'}, status=400)

    obj, _ = LessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson,
        defaults={'completed': False}
    )
    obj.notes = notes_text
    obj.save(update_fields=['notes', 'updated_at'])
    return JsonResponse({'status': 'ok', 'saved_at': obj.updated_at.strftime('%H:%M:%S')})


# ── Переключение предмета ─────────────────────────────────────────────────────

def switch_subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug, is_active=True)
    request.session['subject_slug'] = subject.slug
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER', '/')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('/')


# ── Объявления ────────────────────────────────────────────────────────────────

@login_required
def create_announcement(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title      = request.POST.get('title', '').strip()
        body       = request.POST.get('body', '').strip()
        subject_id = request.POST.get('subject_id') or None
        expires    = request.POST.get('expires_at') or None
        if title:
            subj = Subject.objects.filter(id=subject_id).first() if subject_id else None
            exp  = None
            if expires:
                from django.utils.dateparse import parse_datetime
                exp = parse_datetime(expires)
            Announcement.objects.create(
                author=request.user, subject=subj,
                title=title, body=body,
                expires_at=exp,
            )
            messages.success(request, 'Объявление опубликовано.')
        _next = request.POST.get('next', '')
        if _next and url_has_allowed_host_and_scheme(_next, allowed_hosts={request.get_host()}):
            return redirect(_next)
        return redirect('home')
    subjects = Subject.objects.filter(is_active=True)
    return render(request, 'works/announcement_form.html', {'subjects': subjects})


@login_required
@require_http_methods(["POST"])
def deactivate_announcement(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'status': 'forbidden'}, status=403)
    ann = get_object_or_404(Announcement, pk=pk)
    ann.is_active = False
    ann.save(update_fields=['is_active'])
    return JsonResponse({'status': 'ok'})


@login_required
def announcement_list(request):
    if not request.user.is_staff:
        return redirect('home')
    qs = Announcement.objects.select_related('author', 'subject').order_by('-created_at')
    subject_filter = request.GET.get('subject')
    if subject_filter:
        qs = qs.filter(subject__slug=subject_filter)
    active_filter = request.GET.get('active')
    if active_filter == '1':
        qs = qs.filter(is_active=True)
    elif active_filter == '0':
        qs = qs.filter(is_active=False)
    announcements = list(qs[:50])
    now = timezone.now()
    for ann in announcements:
        ann.expired = bool(ann.expires_at and now > ann.expires_at)
    return render(request, 'works/announcement_list.html', {
        'announcements': announcements,
        'subjects': Subject.objects.filter(is_active=True),
        'subject_filter': subject_filter or '',
        'active_filter': active_filter or '',
    })


# ══════════════════════════════════════════════════════════════════════════════
# ТЕСТЫ
# ══════════════════════════════════════════════════════════════════════════════

def _theory_complete_for_quiz(user, quiz) -> tuple[bool, int, int]:
    """
    Проверяет завершение теории для теста.
    Возвращает (разрешено, пройдено, всего).
    Если quiz.module не задан или учитель — всегда разрешено.
    """
    from works.models import LessonProgress
    if not quiz.module_id or user.is_staff:
        return True, 0, 0
    total = quiz.module.lessons.count()
    if total == 0:
        return True, 0, 0
    done = LessonProgress.objects.filter(
        user=user, lesson__module=quiz.module, completed=True
    ).count()
    return done >= total, done, total


@login_required
def quiz_list(request):
    subject_slug = request.session.get('subject_slug', 'python')
    qs = Quiz.objects.filter(is_active=True).select_related('module', 'module__subject').prefetch_related('questions').order_by('module__order', 'order')
    try:
        current_subject = Subject.objects.get(slug=subject_slug)
        qs = qs.filter(module__subject=current_subject)
    except Subject.DoesNotExist:
        current_subject = None
    quizzes = list(qs)

    attempt_map = {}
    for attempt in QuizAttempt.objects.filter(user=request.user).order_by('-score'):
        if attempt.quiz_id not in attempt_map:
            attempt_map[attempt.quiz_id] = attempt

    for quiz in quizzes:
        quiz.best_attempt = attempt_map.get(quiz.id)
        allowed, done, total_lessons = _theory_complete_for_quiz(request.user, quiz)
        quiz.theory_locked = not allowed
        quiz.theory_done = done
        quiz.theory_total = total_lessons

    # Группировка по тематическим блокам — зависит от предмета
    BLOCKS_BY_SUBJECT = {
        'mcu': [
            {'title': 'Основы МПС и GPIO',          'icon': 'fas fa-microchip',  'color': '#0ea5e9', 'bg': '#f0f9ff', 'min': 1,  'max': 3},
            {'title': 'Прерывания и периферия',      'icon': 'fas fa-bolt',       'color': '#7c3aed', 'bg': '#f5f3ff', 'min': 4,  'max': 7},
            {'title': 'Интерфейсы и программирование','icon': 'fas fa-network-wired','color': '#0d9488','bg': '#f0fdfa', 'min': 8, 'max': 999},
        ],
        'asutps': [
            {'title': 'Теория управления ТП',        'icon': 'fas fa-sliders-h',  'color': '#0ea5e9', 'bg': '#f0f9ff', 'min': 1, 'max': 1},
            {'title': 'Техническое обеспечение',     'icon': 'fas fa-microchip',  'color': '#7c3aed', 'bg': '#f5f3ff', 'min': 2, 'max': 2},
            {'title': 'Информационное обеспечение',  'icon': 'fas fa-database',   'color': '#0d9488', 'bg': '#f0fdfa', 'min': 3, 'max': 3},
            {'title': 'Технологии и программирование','icon': 'fas fa-code',      'color': '#3b82f6', 'bg': '#eff6ff', 'min': 4, 'max': 4},
            {'title': 'Интеграция и эффективность',  'icon': 'fas fa-chart-line', 'color': '#f59e0b', 'bg': '#fffbeb', 'min': 5, 'max': 5},
            {'title': 'ИИ и сложные условия',        'icon': 'fas fa-robot',      'color': '#8b5cf6', 'bg': '#f5f3ff', 'min': 6, 'max': 999},
        ],
        'default': [
            {'title': 'Основы Python',            'icon': 'fas fa-seedling',  'color': '#10b981', 'bg': '#ecfdf5', 'min': 1,  'max': 10},
            {'title': 'Структуры и алгоритмы',    'icon': 'fas fa-sitemap',   'color': '#3b82f6', 'bg': '#eff6ff', 'min': 11, 'max': 20},
            {'title': 'Продвинутые темы',          'icon': 'fas fa-rocket',    'color': '#8b5cf6', 'bg': '#f5f3ff', 'min': 21, 'max': 40},
            {'title': 'Экспертный уровень',        'icon': 'fas fa-crown',     'color': '#f59e0b', 'bg': '#fffbeb', 'min': 41, 'max': 999},
        ],
    }
    BLOCKS_DEF = BLOCKS_BY_SUBJECT.get(subject_slug, BLOCKS_BY_SUBJECT['default'])
    blocks = []
    for bd in BLOCKS_DEF:
        block_quizzes = [q for q in quizzes if q.module and bd['min'] <= q.module.order <= bd['max']]
        if not block_quizzes:
            continue
        passed = sum(1 for q in block_quizzes if q.best_attempt and q.best_attempt.passed)
        blocks.append({
            'title': bd['title'], 'icon': bd['icon'],
            'color': bd['color'], 'bg': bd['bg'],
            'quizzes': block_quizzes,
            'total': len(block_quizzes),
            'passed': passed,
            'pct': int(passed * 100 / len(block_quizzes)) if block_quizzes else 0,
        })

    total_passed = sum(1 for q in quizzes if q.best_attempt and q.best_attempt.passed)
    best_scores = [q.best_attempt.score for q in quizzes if q.best_attempt]

    return render(request, 'works/quiz_list.html', {
        'quizzes': quizzes,
        'blocks': blocks,
        'current_subject': current_subject,
        'total_quizzes': len(quizzes),
        'total_passed': total_passed,
        'avg_score': int(sum(best_scores) / len(best_scores)) if best_scores else 0,
    })


import time as _time

MIN_SECONDS_PER_QUESTION = 4   # минимум секунд на вопрос
MAX_ATTEMPTS_PER_HOUR = 10     # максимум попыток одного теста в час


def _record_quiz_start(request, quiz_id):
    """Фиксирует серверное время начала теста в сессии."""
    request.session[f'quiz_start_{quiz_id}'] = _time.time()
    request.session.modified = True


def _check_quiz_rate_limit(user, quiz) -> tuple[bool, int]:
    """Проверяет лимит попыток: не более MAX_ATTEMPTS_PER_HOUR за последние 2 часа,
    только среди проваленных (passed=False). Возвращает (разрешено, попыток)."""
    from django.utils import timezone
    from datetime import timedelta
    two_hours_ago = timezone.now() - timedelta(hours=2)
    count = QuizAttempt.objects.filter(
        user=user, quiz=quiz, created_at__gte=two_hours_ago, passed=False
    ).count()
    return count < MAX_ATTEMPTS_PER_HOUR, count


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    allowed, done, total = _theory_complete_for_quiz(request.user, quiz)
    if not allowed:
        return render(request, 'works/quiz_locked.html', {
            'quiz': quiz, 'done': done, 'total': total,
        })

    _record_quiz_start(request, quiz_id)

    import random as _random
    questions_qs = list(quiz.questions.prefetch_related('choices').all())
    _random.shuffle(questions_qs)  # вопросы в случайном порядке каждую попытку
    for q in questions_qs:
        q.shuffled_choices = list(q.choices.all())
        _random.shuffle(q.shuffled_choices)

    best_attempt = QuizAttempt.objects.filter(
        user=request.user, quiz=quiz
    ).order_by('-score').first()

    return render(request, 'works/quiz.html', {
        'quiz': quiz,
        'questions': questions_qs,
        'best_attempt': best_attempt,
    })


@login_required
def quiz_adaptive(request, quiz_id):
    """Адаптивный режим теста — вопросы по одному, сложность адаптируется."""
    import json as _json
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    allowed, done, total = _theory_complete_for_quiz(request.user, quiz)
    if not allowed:
        return render(request, 'works/quiz_locked.html', {
            'quiz': quiz, 'done': done, 'total': total,
        })

    import random as _random
    questions = list(quiz.questions.prefetch_related('choices').order_by('difficulty', 'order'))
    # Перемешиваем внутри каждой группы сложности
    from itertools import groupby
    shuffled = []
    for _, grp in groupby(questions, key=lambda q: q.difficulty):
        g = list(grp)
        _random.shuffle(g)
        shuffled.extend(g)
    questions = shuffled

    import random as _random
    # Сериализуем вопросы для JS — correct_ids НЕ включаем (проверка только на сервере)
    q_data = []
    for q in questions:
        choices = [{'id': c.id, 'text': c.text} for c in q.choices.all()]
        _random.shuffle(choices)
        q_data.append({
            'id': q.id,
            'text': q.text,
            'code': q.code_snippet,
            'q_type': q.q_type,
            'difficulty': q.difficulty,
            'choices': choices,
        })

    _record_quiz_start(request, quiz_id)

    best_attempt = QuizAttempt.objects.filter(
        user=request.user, quiz=quiz
    ).order_by('-score').first()

    return render(request, 'works/quiz_adaptive.html', {
        'quiz': quiz,
        'questions_json': _safe_json(q_data),
        'total': len(q_data),
        'best_attempt': best_attempt,
    })


@login_required
@require_http_methods(["POST"])
def check_quiz_answer(request, question_id):
    """AJAX: проверяет ответ на один вопрос. Возвращает correct_ids + explanation только после ответа.
    Доступ только для вопросов из теста, который пользователь сейчас проходит (сессионный ключ)."""
    from works.models import Question
    question = get_object_or_404(Question, id=question_id)

    # Проверяем, что пользователь действительно открыл тест с этим вопросом
    quiz = question.quiz
    start_key = f'quiz_start_{quiz.id}'
    if not request.user.is_staff and start_key not in request.session:
        return JsonResponse({'error': 'Тест не начат или время сессии истекло.'}, status=403)

    if question.q_type == 'single':
        chosen_raw = request.POST.get('choice_id')
        chosen_ids = {int(chosen_raw)} if chosen_raw else set()
    else:
        chosen_ids = set(int(v) for v in request.POST.getlist('choice_ids') if v)

    correct_ids = set(question.choices.filter(is_correct=True).values_list('id', flat=True))
    is_correct = chosen_ids == correct_ids

    return JsonResponse({
        'is_correct': is_correct,
        'correct_ids': list(correct_ids),
        'explanation': question.explanation if not is_correct else '',
    })


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
           request.POST.get('_ajax') == '1'


def _quiz_error(request, quiz_id, msg, is_ajax):
    """Вернуть ошибку: JSON для AJAX, redirect+flash для обычного запроса."""
    if is_ajax:
        return JsonResponse({'error': msg}, status=400)
    messages.error(request, msg)
    return redirect('quiz_detail', quiz_id=quiz_id)


@login_required
@require_http_methods(["POST"])
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    is_ajax = _is_ajax(request)

    allowed, done, total_lessons = _theory_complete_for_quiz(request.user, quiz)
    if not allowed:
        return JsonResponse({'error': 'Сначала изучи всю теорию раздела.'}, status=403)

    questions = quiz.questions.prefetch_related('choices').all()
    total = questions.count()

    # Rate limit
    if not request.user.is_staff:
        rate_ok, recent_count = _check_quiz_rate_limit(request.user, quiz)
        if not rate_ok:
            msg = f'Превышен лимит неудачных попыток ({MAX_ATTEMPTS_PER_HOUR} за 2 часа). Попробуй позже.'
            return _quiz_error(request, quiz_id, msg, is_ajax)

    # Серверная проверка времени (клиентский POST-параметр не используем — его легко подделать)
    suspicious = False
    start_key = f'quiz_start_{quiz_id}'
    start_time = request.session.get(start_key)
    if start_time and not request.user.is_staff:
        elapsed = _time.time() - start_time
        min_required = total * MIN_SECONDS_PER_QUESTION
        if elapsed < min_required:
            logger.warning(
                'submit_quiz BLOCKED: user=%s quiz=%s elapsed=%.1fs < min=%ds',
                request.user.username, quiz_id, elapsed, min_required
            )
            msg = f'Тест пройден слишком быстро. Минимальное время — {min_required} секунд ({MIN_SECONDS_PER_QUESTION} сек/вопрос).'
            return _quiz_error(request, quiz_id, msg, is_ajax)
        if elapsed < min_required * 2:
            suspicious = True
    # Очищаем ключ — следующая попытка потребует нового открытия страницы
    request.session.pop(start_key, None)

    try:
        time_spent = int(request.POST.get('time_spent_seconds', 0))
    except (ValueError, TypeError):
        time_spent = 0
    try:
        focus_loss_count = max(0, int(request.POST.get('focus_loss_count', 0)))
    except (ValueError, TypeError):
        focus_loss_count = 0

    correct = 0
    results = {}
    all_chosen_ids = []

    for question in questions:
        correct_ids = set(
            question.choices.filter(is_correct=True).values_list('id', flat=True)
        )
        if question.q_type == 'single':
            chosen_raw = request.POST.get(f'q_{question.id}')
            chosen_ids = {int(chosen_raw)} if chosen_raw else set()
        else:
            chosen_ids = set(
                int(v) for v in request.POST.getlist(f'q_{question.id}')
            )

        is_correct = (chosen_ids == correct_ids)
        if is_correct:
            correct += 1
        all_chosen_ids.append(tuple(sorted(chosen_ids)))

        results[str(question.id)] = {
            'chosen': list(chosen_ids),
            'correct': list(correct_ids),
            'is_correct': is_correct,
            'explanation': question.explanation,
        }

    # Анализ паттерна: все ответы одинаковые или нет ни одного ответа
    if not request.user.is_staff and total > 2:
        unanswered = sum(1 for c in all_chosen_ids if not c)
        if unanswered == total:
            suspicious = True  # никаких ответов — просто нажал отправить
        elif len(set(all_chosen_ids)) == 1 and all_chosen_ids[0]:
            suspicious = True  # все ответы идентичны — явный паттерн

    # Много уходов со вкладки — тоже подозрительно
    if focus_loss_count >= 3 and not request.user.is_staff:
        suspicious = True

    score = round(correct * 100 / total) if total else 0
    passed = score >= quiz.pass_score

    if time_spent < 0 or time_spent > 86400:
        time_spent = 0

    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        passed=passed,
        answers=results,
        time_spent_seconds=time_spent,
        focus_loss_count=focus_loss_count,
        suspicious=suspicious,
    )
    if suspicious:
        logger.warning(
            'SUSPICIOUS ATTEMPT id=%s user=%s quiz=%s score=%d focus_loss=%d',
            attempt.id, request.user.username, quiz_id, score, focus_loss_count
        )
    if is_ajax:
        from django.urls import reverse
        return JsonResponse({'redirect': reverse('quiz_result', args=[attempt.id])})
    return redirect('quiz_result', attempt_id=attempt.id)


@login_required
@require_http_methods(["GET"])
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    quiz = attempt.quiz
    questions = quiz.questions.prefetch_related('choices').all()
    results = attempt.answers or {}
    total = questions.count()
    correct = sum(1 for v in results.values() if v.get('is_correct'))
    # Не раскрываем correct_ids для правильно отвеченных вопросов
    results_safe = {}
    for qid, data in results.items():
        entry = dict(data)
        if entry.get('is_correct'):
            entry.pop('correct', None)
        results_safe[qid] = entry
    return render(request, 'works/quiz_result.html', {
        'quiz': quiz,
        'attempt': attempt,
        'questions': questions,
        'results': results,
        'results_json': json.dumps(results_safe),
        'correct': correct,
        'errors': total - correct,
        'total': total,
        'score': attempt.score,
        'passed': attempt.passed,
    })


@login_required
@require_http_methods(["POST"])
def check_plagiarism(request, solution_id):
    """AJAX: запускает проверку на плагиат для решения (только для staff)."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Доступ запрещён'}, status=403)
    solution = get_object_or_404(Solution, id=solution_id)
    from works.plagiarism import check_solution
    matches = check_solution(solution)
    max_score = max((m.score for m in matches), default=0.0)
    solution.similarity_score = max_score
    solution.similarity_matches = [m._asdict() for m in matches]
    solution.save(update_fields=['similarity_score', 'similarity_matches'])
    return JsonResponse({
        'max_score': max_score,
        'matches': [m._asdict() for m in matches],
    })


@login_required
@require_http_methods(["POST"])
def recheck_doc(request, solution_id):
    """AJAX: повторная ИИ-проверка docx/pdf отчёта. Только staff."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Доступ запрещён'}, status=403)
    solution = get_object_or_404(Solution, id=solution_id)
    ext = os.path.splitext(solution.code_file.name)[1].lower()
    if ext not in ('.docx', '.pdf', '.doc'):
        return JsonResponse({'error': 'Файл не является отчётом (docx/pdf)'}, status=400)
    from works.models import CodeCheck as _CC
    from works.ai_checker import AICodeChecker
    from django.utils import timezone as _tz
    import threading
    cc = _CC.objects.create(
        solution=solution, status='in_progress',
        check_type='auto', created_at=_tz.now()
    )
    def _run(_sid, _cid):
        try:
            AICodeChecker().check_solution(_sid, _cid)
        except Exception:
            pass
    threading.Thread(target=_run, args=(solution.id, cc.id), daemon=True).start()
    return JsonResponse({'ok': True, 'check_id': cc.id})


@login_required
@require_http_methods(["POST"])
def run_code_snippet(request):
    """Запуск кода с выбором языка (Python / C++ / Java / JavaScript)."""
    code = request.POST.get("code", "").strip()
    lang = request.POST.get("language", "python").lower()
    stdin = request.POST.get("stdin", "") or None

    if not code:
        return JsonResponse({"status": "error", "output": "Нет кода для выполнения"})

    RUNNERS = {
        "python":     run_python_code,
        "cpp":        run_cpp_code,
        "c++":        run_cpp_code,
        "java":       run_java_code,
        "javascript": run_javascript_code,
        "js":         run_javascript_code,
    }
    if lang not in RUNNERS:
        return JsonResponse({"status": "error", "output": f"Неподдерживаемый язык: {lang}", "via_cloud": False}, status=400)
    runner = RUNNERS[lang]

    try:
        result = runner(code, input_data=stdin)
        output = result.get("output", "") or result.get("error", "")
        return JsonResponse({
            "status":    result.get("status", "error"),
            "output":    output or "(нет вывода)",
            "via_cloud": result.get("via") in ("wandbox", "piston"),
        })
    except Exception as e:
        logger.exception('run_code_snippet internal error')
        return JsonResponse({"status": "error", "output": "Внутренняя ошибка сервера", "via_cloud": False})


@login_required
def playground(request):
    """Страница онлайн-песочницы для свободного написания и запуска кода."""
    lang = request.GET.get("lang", "python")
    allowed = {"python", "cpp", "java", "javascript"}
    lang = lang if lang in allowed else "python"
    return render(request, "works/playground.html", {"default_lang": lang})


@_staff_required
def pygrid_game(request):
    """PyGrid — обучающая игра (только для преподавателей)."""
    return render(request, "works/pygrid.html")


def pygrid_beta(request):
    """PyGrid — бета-доступ для студентов (только авторизованные)."""
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    return render(request, "works/pygrid.html", {"beta_mode": True})


# ══════════════════════════════════════════════════════════════════════════════
# ХРАНИЛИЩЕ ПРОЕКТОВ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def project_list(request):
    """Список проектов текущего студента."""
    from .models import StudentProject
    projects = StudentProject.objects.filter(student=request.user)
    return render(request, 'works/projects.html', {'projects': projects})


@login_required
def project_editor(request, project_id=None):
    """Редактор проекта — новый или существующий."""
    from .models import StudentProject, Subject
    if project_id:
        project = get_object_or_404(StudentProject, id=project_id, student=request.user)
    else:
        project = None
    subjects = Subject.objects.filter(is_active=True)
    return render(request, 'works/project_editor.html', {
        'project': project,
        'subjects': subjects,
    })


@login_required
@require_http_methods(["POST"])
def project_save(request):
    """API: сохранить/создать проект (JSON)."""
    from .models import StudentProject, Subject
    data = json.loads(request.body)
    project_id = data.get('id')
    title = data.get('title', '').strip() or 'Без названия'
    code = data.get('code', '')
    language = data.get('language', 'python')
    description = data.get('description', '')
    subject_id = data.get('subject_id') or None

    subject = None
    if subject_id:
        subject = Subject.objects.filter(id=subject_id).first()

    allowed_langs = {'python', 'cpp', 'java', 'javascript', 'other'}
    if language not in allowed_langs:
        language = 'python'

    if project_id:
        project = get_object_or_404(StudentProject, id=project_id, student=request.user)
        project.title = title
        project.code = code
        project.language = language
        project.description = description
        project.subject = subject
        project.save()
    else:
        project = StudentProject.objects.create(
            student=request.user,
            title=title,
            code=code,
            language=language,
            description=description,
            subject=subject,
        )
    return JsonResponse({'status': 'ok', 'id': project.id,
                         'saved_at': project.updated_at.strftime('%H:%M:%S')})


@login_required
@require_http_methods(["POST"])
def project_delete(request, project_id):
    """Удалить проект."""
    from .models import StudentProject
    project = get_object_or_404(StudentProject, id=project_id, student=request.user)
    project.delete()
    return JsonResponse({'status': 'ok'})


@login_required
def teacher_projects(request):
    """Преподаватель: просмотр всех проектов студентов."""
    from .models import StudentProject
    from django.contrib.auth.models import User as DjangoUser
    if not request.user.is_staff:
        return redirect('home')

    student_id = request.GET.get('student')
    lang_filter = request.GET.get('lang', '')
    qs = StudentProject.objects.select_related('student', 'subject').order_by('-updated_at')
    if student_id:
        qs = qs.filter(student_id=student_id)
    if lang_filter:
        qs = qs.filter(language=lang_filter)

    students = DjangoUser.objects.filter(projects__isnull=False).distinct().order_by('last_name')
    return render(request, 'works/teacher_projects.html', {
        'projects': qs,
        'students': students,
        'selected_student': student_id,
        'selected_lang': lang_filter,
    })


# ══════════════════════════════════════════════════════════════════════════════
# УВЕДОМЛЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user)
    # Помечаем все прочитанными при открытии страницы
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'works/notifications.html', {'notifications': notifs})


@login_required
@require_http_methods(['POST'])
def mark_notification_read(request, notif_id):
    Notification.objects.filter(id=notif_id, user=request.user).update(is_read=True)
    return JsonResponse({'ok': True})


@login_required
@require_http_methods(['GET'])
def notifications_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})


# ══════════════════════════════════════════════════════════════════════════════
# ЖУРНАЛ УСПЕВАЕМОСТИ (преподаватель)
# ══════════════════════════════════════════════════════════════════════════════

@_staff_required
def gradebook(request):
    group_filter = request.GET.get('group', '')
    students_qs  = User.objects.filter(is_active=True, is_staff=False).order_by('last_name', 'first_name')

    # Фильтрация по группе
    all_groups = list(
        UserProgress.objects.filter(group__gt='')
        .values_list('group', flat=True).distinct().order_by('group')
    )
    if group_filter:
        students_qs = students_qs.filter(userprogress__group=group_filter)

    students  = list(students_qs.select_related('userprogress'))
    works     = list(PracticalWork.objects.filter(is_active=True).order_by('order'))
    total_works_count = len(works)

    # Матрица оценок: {student_id: {work_id: best_score}}
    all_solutions = Solution.objects.filter(
        student__in=students,
        work__in=works,
    ).values('student_id', 'work_id', 'score', 'status').order_by('student_id', 'work_id', '-score')

    matrix = {}
    for sol in all_solutions:
        sid, wid = sol['student_id'], sol['work_id']
        if sid not in matrix:
            matrix[sid] = {}
        if wid not in matrix[sid]:
            matrix[sid][wid] = {'score': sol['score'], 'status': sol['status']}

    # Добавляем progress к студентам
    prog_map = {p.user_id: p for p in UserProgress.objects.filter(user__in=students)}
    for s in students:
        s.progress = prog_map.get(s.id)
        s.row = [matrix.get(s.id, {}).get(w.id) for w in works]
        scores = [c['score'] for c in matrix.get(s.id, {}).values() if c['score']]
        s.avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        s.done_count = sum(1 for w in works if matrix.get(s.id, {}).get(w.id, {}).get('status') in ('correct','partially_correct'))

    export = request.GET.get('export')
    if export == 'csv':
        import csv
        from django.http import HttpResponse as HR
        resp = HR(content_type='text/csv; charset=utf-8-sig')
        resp['Content-Disposition'] = 'attachment; filename="gradebook.csv"'
        writer = csv.writer(resp)
        header = ['Студент', 'Группа'] + [f'ПР{w.order}' for w in works] + ['Среднее', 'Сдано']
        writer.writerow(header)
        for s in students:
            row_scores = []
            for w in works:
                cell = matrix.get(s.id, {}).get(w.id)
                row_scores.append(cell['score'] if cell else '')
            writer.writerow([
                f'{s.last_name} {s.first_name}',
                getattr(s.progress, 'group', ''),
                *row_scores,
                s.avg_score,
                s.done_count,
            ])
        return resp

    return render(request, 'works/gradebook.html', {
        'students': students,
        'works': works,
        'all_groups': all_groups,
        'group_filter': group_filter,
    })


# ══════════════════════════════════════════════════════════════════════════════
# РУЧНАЯ ПРОВЕРКА ПРЕПОДАВАТЕЛЕМ
# ══════════════════════════════════════════════════════════════════════════════

@_staff_required
def teacher_solutions(request):
    """Все решения с фильтрами для преподавателя."""
    qs = Solution.objects.select_related('student', 'work').prefetch_related('student__userprogress', 'teacher_comments').order_by('-submitted_at')
    group   = request.GET.get('group', '')
    status  = request.GET.get('status', '')
    work_id = request.GET.get('work', '')
    if group:
        qs = qs.filter(student__userprogress__group=group)
    if status:
        qs = qs.filter(status=status)
    if work_id:
        qs = qs.filter(work_id=work_id)

    from django.core.paginator import Paginator
    paginator = Paginator(qs, 30)
    page_obj  = paginator.get_page(request.GET.get('page'))

    all_groups = list(UserProgress.objects.filter(group__gt='')
                      .values_list('group', flat=True).distinct().order_by('group'))
    works_list = PracticalWork.objects.filter(is_active=True).order_by('order')

    pending_extensions = DeadlineExtension.objects.filter(status='pending').select_related('user', 'work').order_by('-requested_at')

    return render(request, 'works/teacher_solutions.html', {
        'page_obj': page_obj,
        'all_groups': all_groups,
        'works_list': works_list,
        'group': group,
        'status': status,
        'work_id': work_id,
        'pending_extensions': pending_extensions,
    })


@_staff_required
@require_http_methods(['POST'])
def manual_grade(request, solution_id):
    """Ручная оценка и комментарий от преподавателя."""
    solution = get_object_or_404(Solution, id=solution_id)
    score_raw = request.POST.get('score', '').strip()
    comment   = request.POST.get('comment', '').strip()
    new_status = request.POST.get('status', solution.status)

    score = None
    score_pts = None
    if score_raw.isdigit():
        max_s = solution.work.max_score or 100
        score_pts = min(int(score_raw), max_s)
        score = round(score_pts * 100 / max_s)  # store as percentage
        solution.score = score
    solution.status = new_status
    solution.save()

    if comment:
        TeacherComment.objects.create(
            solution=solution,
            teacher=request.user,
            text=comment,
            score=score,
        )
        # Уведомляем студента
        Notification.send(
            user=solution.student,
            n_type='commented',
            title=f'Комментарий к «{solution.work.title}»',
            message=comment[:200],
            link=f'/solution/{solution.id}/',
        )

    if score is not None:
        Notification.send(
            user=solution.student,
            n_type='graded',
            title=f'Работа «{solution.work.title}» проверена',
            message=f'Оценка: {score_pts}/{solution.work.max_score or 100}',
            link=f'/solution/{solution.id}/',
        )
        _notify_email(
            solution.student,
            f'Работа «{solution.work.title}» проверена',
            f'Оценка: {score}. Откройте решение для просмотра комментариев.',
        )

    # Пересчитать прогресс студента после оценки
    student = solution.student
    progress, _ = UserProgress.objects.get_or_create(user=student)
    progress.completed_works = Solution.objects.filter(
        student=student, status__in=['correct', 'partially_correct']
    ).values('work').distinct().count()
    progress.total_score = Solution.objects.filter(student=student).aggregate(Sum('score'))['score__sum'] or 0
    progress.average_score = (progress.total_score / progress.completed_works
                              if progress.completed_works > 0 else 0)
    progress.save(update_fields=['completed_works', 'total_score', 'average_score'])
    check_achievements(student)

    messages.success(request, f'Оценка сохранена: {score}, статус: {new_status}')
    _next = request.POST.get('next', '')
    if _next and url_has_allowed_host_and_scheme(_next, allowed_hosts={request.get_host()}):
        return redirect(_next)
    return redirect('teacher_solutions')


# ══════════════════════════════════════════════════════════════════════════════
# РЕЙТИНГ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def leaderboard(request):
    # Синхронизируем только текущего пользователя (пересчёт всех — DoS)
    _sync_user_progress(request.user)

    group_filter = request.GET.get('group', '')
    qs = UserProgress.objects.filter(
        user__is_active=True
    ).select_related('user').order_by('-total_score', '-completed_works')

    all_groups = list(
        UserProgress.objects.filter(group__gt='').values_list('group', flat=True)
        .distinct().order_by('group')
    )  # TODO: add cache_page(60) decorator for performance
    if group_filter:
        qs = qs.filter(group=group_filter)

    leaders = list(qs[:50])
    my_rank = None
    for i, p in enumerate(leaders, 1):
        p.rank = i
        if p.user_id == request.user.id:
            my_rank = i

    group_stats = list(
        UserProgress.objects.filter(user__is_active=True, group__gt='')
        .values('group')
        .annotate(
            avg_score=Avg('total_score'),
            student_count=Count('id'),
            avg_works=Avg('completed_works'),
            avg_streak=Avg('streak_days'),
        )
        .order_by('-avg_score')
    )
    for i, g in enumerate(group_stats, 1):
        g['rank'] = i

    return render(request, 'works/leaderboard.html', {
        'leaders': leaders,
        'my_rank': my_rank,
        'all_groups': all_groups,
        'group_filter': group_filter,
        'group_stats': group_stats,
    })


# ══════════════════════════════════════════════════════════════════════════════
# ПОИСК ПО ТЕОРИИ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def theory_search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q and len(q) >= 2:
        from django.db.models import Q as DQ
        lessons = TheoryLesson.objects.filter(
            DQ(title__icontains=q) | DQ(content__icontains=q) | DQ(code_example__icontains=q)
        ).select_related('module')[:20]
        results = list(lessons)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [{'id': l.id, 'title': l.title, 'module': l.module.title,
                 'url': f'/theory/lesson/{l.id}/'} for l in results]
        return JsonResponse({'results': data, 'count': len(data)})

    return render(request, 'works/theory_search.html', {'q': q, 'results': results})




# ══════════════════════════════════════════════════════════════════════════════
# DEV AUTO-RELOAD
# ══════════════════════════════════════════════════════════════════════════════

def dev_reload(request):
    """Возвращает максимальный mtime отслеживаемых файлов. Только при DEBUG=True."""
    from django.conf import settings
    if not settings.DEBUG:
        return JsonResponse({'error': 'not available'}, status=403)

    latest = 0.0
    watch_dirs = [
        str(settings.BASE_DIR / 'works' / 'templates'),
        str(settings.BASE_DIR / 'works' / 'static'),
        str(settings.BASE_DIR / 'works'),
    ]
    skip_dirs = {'__pycache__', '.git', 'migrations', 'node_modules'}
    skip_exts = {'.pyc', '.pyo', '.sqlite3', '.log', '.lock'}

    for watch_dir in watch_dirs:
        if not os.path.exists(watch_dir):
            continue
        for root, dirs, files in os.walk(watch_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for fname in files:
                if os.path.splitext(fname)[1] in skip_exts:
                    continue
                try:
                    m = os.path.getmtime(os.path.join(root, fname))
                    if m > latest:
                        latest = m
                except OSError:
                    pass

    return JsonResponse({'mtime': latest})


def about(request):
    return render(request, 'works/about.html')


@login_required
def quiz_history(request, quiz_id):
    """История всех попыток пользователя по конкретному тесту с разбором ошибок."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-created_at')
    questions = {str(q.id): q for q in quiz.questions.prefetch_related('choices').all()}

    attempts_detail = []
    for attempt in attempts:
        breakdown = []
        for qid, data in attempt.answers.items():
            q = questions.get(qid)
            if not q:
                continue
            choices_map = {str(c.id): c.text for c in q.choices.all()}
            chosen_texts = [choices_map.get(str(cid), str(cid)) for cid in data.get('chosen', [])]
            correct_texts = [choices_map.get(str(cid), str(cid)) for cid in data.get('correct', [])]
            breakdown.append({
                'question': q.text,
                'code': q.code_snippet,
                'is_correct': data.get('is_correct', False),
                'chosen': chosen_texts,
                'correct': correct_texts,
                'explanation': data.get('explanation', ''),
            })
        attempts_detail.append({'attempt': attempt, 'breakdown': breakdown})

    return render(request, 'works/quiz_history.html', {
        'quiz': quiz,
        'attempts_detail': attempts_detail,
    })

# ══════════════════════════════════════════════════════════════════════════════
# СМЕНА ПАРОЛЯ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def change_password(request):
    """Смена пароля для студента и преподавателя."""
    error = None
    success = False

    if request.method == 'POST':
        old_pw  = request.POST.get('old_password', '')
        new_pw1 = request.POST.get('new_password1', '')
        new_pw2 = request.POST.get('new_password2', '')

        if not request.user.check_password(old_pw):
            error = 'Неверный текущий пароль'
        elif len(new_pw1) < 6:
            error = 'Новый пароль должен быть не менее 6 символов'
        elif new_pw1 != new_pw2:
            error = 'Пароли не совпадают'
        else:
            request.user.set_password(new_pw1)
            request.user.save()
            # Переавторизация после смены пароля
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            # Снять флаг "требует смены пароля"
            UserProgress.objects.filter(user=request.user).update(must_change_password=False)
            success = True
            messages.success(request, 'Пароль успешно изменён')


    return render(request, 'works/change_password.html', {
        'error': error,
        'success': success,
    })


# ══════════════════════════════════════════════════════════════════════════════
# ИСТОРИЯ РЕШЕНИЙ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def solution_history(request, work_id):
    """Все попытки сдачи конкретной работы студентом."""
    work = get_object_or_404(PracticalWork, id=work_id)
    # Студент видит только свои, преподаватель — все
    if request.user.is_staff:
        student_id = request.GET.get('student')
        if student_id:
            from django.contrib.auth.models import User as _User
            student = get_object_or_404(_User, id=student_id)
            attempts = Solution.objects.filter(work=work, student=student).order_by('-submitted_at')
        else:
            attempts = Solution.objects.filter(work=work).order_by('-submitted_at').select_related('student')
    else:
        student = request.user
        attempts = Solution.objects.filter(work=work, student=request.user).order_by('-submitted_at')

    attempts_list = list(attempts)
    # Прикрепляем prev_id для кнопки Diff (попытка i сравнивается с i-1)
    for i, sol in enumerate(attempts_list):
        sol.prev_id = attempts_list[i - 1].id if i > 0 else None

    return render(request, 'works/solution_history.html', {
        'work': work,
        'attempts': attempts_list,
        'is_teacher': request.user.is_staff,
    })


@login_required
def solution_diff(request, sol1_id, sol2_id):
    """Diff между двумя попытками сдачи."""
    import difflib
    sol1 = get_object_or_404(Solution, id=sol1_id)
    sol2 = get_object_or_404(Solution, id=sol2_id)
    # Доступ: только свои попытки или преподаватель
    if not request.user.is_staff and (sol1.student != request.user or sol2.student != request.user):
        return redirect('home')

    lines1 = _read_solution_code(sol1).splitlines()
    lines2 = _read_solution_code(sol2).splitlines()

    differ = difflib.HtmlDiff(wrapcolumn=80)
    diff_table = differ.make_table(
        lines1, lines2,
        fromdesc=f'Попытка #{sol1.id} — {sol1.submitted_at.strftime("%d.%m.%Y %H:%M")}',
        todesc=f'Попытка #{sol2.id} — {sol2.submitted_at.strftime("%d.%m.%Y %H:%M")}',
        context=True, numlines=3,
    )
    return render(request, 'works/solution_diff.html', {
        'sol1': sol1, 'sol2': sol2,
        'diff_table': diff_table,
        'work': sol1.work,
    })


@_staff_required
def plagiarism_check(request, work_id):
    """Сравнение решений студентов для обнаружения плагиата."""
    import difflib
    work = get_object_or_404(PracticalWork, id=work_id)

    # Берём последнее решение каждого студента
    from django.db.models import Max
    latest_ids = (Solution.objects
                  .filter(work=work)
                  .values('student')
                  .annotate(last_id=Max('id'))
                  .values_list('last_id', flat=True))
    solutions = list(Solution.objects.filter(id__in=latest_ids)
                     .select_related('student')
                     .order_by('student__last_name'))

    pairs = []
    threshold = int(request.GET.get('threshold', 70))
    for i in range(len(solutions)):
        for j in range(i + 1, len(solutions)):
            a, b = solutions[i], solutions[j]
            ratio = difflib.SequenceMatcher(
                None,
                _read_solution_code(a).strip(),
                _read_solution_code(b).strip(),
            ).ratio()
            pct = round(ratio * 100)
            if pct >= threshold:
                pairs.append({
                    'sol_a': a, 'sol_b': b,
                    'pct': pct,
                    'level': 'danger' if pct >= 85 else 'warning',
                })

    pairs.sort(key=lambda x: -x['pct'])
    return render(request, 'works/plagiarism.html', {
        'work': work,
        'pairs': pairs,
        'solutions': solutions,
        'threshold': threshold,
    })


@_staff_required
def add_line_comment(request, solution_id):
    """Добавить комментарий преподавателя к строке кода."""
    if request.method != 'POST':
        return redirect('home')
    solution = get_object_or_404(Solution, id=solution_id)
    text = request.POST.get('text', '').strip()
    line_number = request.POST.get('line_number')
    if text:
        TeacherComment.objects.create(
            solution=solution,
            teacher=request.user,
            text=text,
            line_number=int(line_number) if line_number else None,
        )
    _next = request.POST.get('next', '')
    if _next and url_has_allowed_host_and_scheme(_next, allowed_hosts={request.get_host()}):
        return redirect(_next)
    return redirect('home')


# ══════════════════════════════════════════════════════════════════════════════
# АНАЛИТИКА ПРЕПОДАВАТЕЛЯ
# ══════════════════════════════════════════════════════════════════════════════

@_staff_required
def teacher_analytics(request):
    """Дашборд с аналитикой успеваемости."""
    from django.utils import timezone
    from datetime import timedelta

    group_filter = request.GET.get('group', '')

    students_qs = UserProgress.objects.filter(
        user__is_active=True, user__is_staff=False
    ).select_related('user')
    if group_filter:
        students_qs = students_qs.filter(group=group_filter)

    all_groups = list(
        UserProgress.objects.filter(group__gt='').values_list('group', flat=True)
        .distinct().order_by('group')
    )

    works = PracticalWork.objects.filter(is_active=True).order_by('order')

    # Средний балл по каждой работе
    work_stats = []
    for w in works:
        sol_qs = Solution.objects.filter(work=w)
        if group_filter:
            sol_qs = sol_qs.filter(student__userprogress__group=group_filter)
        agg = sol_qs.aggregate(avg=Avg('score'), cnt=Count('id'), passed=Count('id', filter=Q(status='correct')))
        work_stats.append({
            'work': w,
            'avg_score':    round(agg['avg'] or 0, 1),
            'total':        agg['cnt'] or 0,
            'passed':       agg['passed'] or 0,
            'pass_rate':    round((agg['passed'] or 0) * 100 / agg['cnt']) if agg['cnt'] else 0,
        })

    # Самые сложные работы (наименьший pass_rate)
    hardest = sorted(work_stats, key=lambda x: x['pass_rate'])[:3]

    # Активность за последние 7 дней
    days = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        cnt = Solution.objects.filter(submitted_at__date=day).count()
        days.append({'date': day.strftime('%d.%m'), 'count': cnt})

    # Общая статистика
    total_students = students_qs.count()
    avg_score_all  = students_qs.aggregate(a=Avg('average_score'))['a'] or 0
    total_solutions = Solution.objects.count()
    passed_solutions = Solution.objects.filter(status='correct').count()

    # === Аналитика ошибок ===
    import json as _json
    from collections import Counter as _Counter

    # Топ-5 заданий с наибольшим кол-вом ошибочных решений
    error_works = (
        Solution.objects.filter(status='incorrect')
        .values('work__title', 'work_id')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:5]
    )

    # Частые ошибки из CodeCheck.errors
    error_counter = _Counter()
    for cc in CodeCheck.objects.exclude(errors=[]).order_by('-created_at')[:300]:
        try:
            errs = cc.errors if isinstance(cc.errors, list) else _json.loads(cc.errors or '[]')
            for e in errs:
                key = str(e)[:80].strip()
                if key:
                    error_counter[key] += 1
        except Exception:
            pass
    top_errors = error_counter.most_common(8)

    # === Статистика тестов по студентам ===
    all_quizzes = list(Quiz.objects.filter(is_active=True).order_by('module__order').select_related('module'))

    students_list = list(
        User.objects.filter(is_active=True, is_staff=False).order_by('last_name', 'first_name')
    )
    if group_filter:
        students_list = [
            u for u in students_list
            if UserProgress.objects.filter(user=u, group=group_filter).exists()
        ]

    # Все попытки одним запросом
    attempts_all = QuizAttempt.objects.filter(
        user__in=students_list
    ).values('user_id', 'quiz_id', 'score', 'passed')

    # Индекс: (user_id, quiz_id) → best attempt
    attempt_index = {}
    for a in attempts_all:
        key = (a['user_id'], a['quiz_id'])
        if key not in attempt_index or a['score'] > attempt_index[key]['score']:
            attempt_index[key] = a

    quiz_student_rows = []
    for u in students_list:
        row_attempts = []
        total_taken = 0
        total_passed = 0
        for q in all_quizzes:
            best = attempt_index.get((u.id, q.id))
            row_attempts.append(best)
            if best:
                total_taken += 1
                if best['passed']:
                    total_passed += 1
        quiz_student_rows.append({
            'user': u,
            'attempts': row_attempts,
            'total_taken': total_taken,
            'total_passed': total_passed,
            'pass_rate': round(total_passed * 100 / total_taken) if total_taken else 0,
        })

    # Per-quiz summary
    quiz_summary = []
    for q in all_quizzes:
        taken = sum(1 for u in students_list if (u.id, q.id) in attempt_index)
        passed = sum(1 for u in students_list if attempt_index.get((u.id, q.id), {}).get('passed'))
        avg_sc = 0
        scores = [attempt_index[(u.id, q.id)]['score'] for u in students_list if (u.id, q.id) in attempt_index]
        if scores:
            avg_sc = round(sum(scores) / len(scores), 1)
        quiz_summary.append({'quiz': q, 'taken': taken, 'passed': passed, 'avg_score': avg_sc})

    # Тепловая карта за 90 дней (GitHub-стиль)
    today = timezone.now().date()
    heatmap_raw = {}
    for i in range(89, -1, -1):
        day = today - timedelta(days=i)
        heatmap_raw[day.isoformat()] = 0
    for sol in Solution.objects.filter(submitted_at__date__gte=today - timedelta(days=89)).values('submitted_at__date').annotate(cnt=Count('id')):
        k = sol['submitted_at__date'].isoformat()
        if k in heatmap_raw:
            heatmap_raw[k] = sol['cnt']
    import json as _json2
    heatmap_json = _json2.dumps(heatmap_raw)

    return render(request, 'works/teacher_analytics.html', {
        'work_stats':         work_stats,
        'hardest':            hardest,
        'days':               days,
        'total_students':     total_students,
        'avg_score_all':      round(avg_score_all, 1),
        'total_solutions':    total_solutions,
        'passed_solutions':   passed_solutions,
        'heatmap_json':       heatmap_json,
        'pass_rate_all':      round(passed_solutions * 100 / total_solutions) if total_solutions else 0,
        'all_groups':         all_groups,
        'group_filter':       group_filter,
        'error_works':        error_works,
        'top_errors':         top_errors,
        'all_quizzes':        all_quizzes,
        'quiz_student_rows':  quiz_student_rows,
        'quiz_summary':       quiz_summary,
        'total_quizzes':      len(all_quizzes),
        'review_requests':    ReviewRequest.objects.filter(status='pending').select_related('student').order_by('-requested_at')[:30],
        'review_pending_count': ReviewRequest.objects.filter(status='pending').count(),
    })


@login_required
@require_http_methods(["POST"])
def unlock_hint(request, hint_id):
    """Открыть подсказку за XP."""
    hint = get_object_or_404(WorkHint, id=hint_id)
    progress, _ = UserProgress.objects.get_or_create(user=request.user)
    already = UserHintUnlock.objects.filter(user=request.user, hint=hint).exists()
    if already:
        return JsonResponse({'text': hint.text, 'title': hint.title, 'already': True})
    if progress.total_score < hint.xp_cost:
        return JsonResponse({'error': f'Недостаточно очков. Нужно {hint.xp_cost}, у вас {progress.total_score}.'}, status=400)
    UserHintUnlock.objects.create(user=request.user, hint=hint)
    progress.total_score = max(0, progress.total_score - hint.xp_cost)
    progress.save(update_fields=['total_score'])
    return JsonResponse({'text': hint.text, 'title': hint.title, 'cost': hint.xp_cost})


@login_required
@require_http_methods(["POST"])
def request_deadline_extension(request, work_id):
    """Студент запрашивает продление дедлайна."""
    work = get_object_or_404(PracticalWork, id=work_id)
    reason = request.POST.get('reason', '').strip()
    if not reason:
        messages.error(request, 'Укажите причину запроса.')
        return redirect('work_detail', work_id=work_id)
    ext, created = DeadlineExtension.objects.get_or_create(
        user=request.user, work=work,
        defaults={'reason': reason, 'status': 'pending'}
    )
    if not created:
        ext.reason = reason
        ext.status = 'pending'
        ext.save(update_fields=['reason', 'status'])
    messages.success(request, 'Запрос отправлен преподавателю.')
    return redirect('work_detail', work_id=work_id)


@_staff_required
@require_http_methods(["POST"])
def approve_deadline_extension(request, ext_id):
    """Преподаватель одобряет или отклоняет продление."""
    ext = get_object_or_404(DeadlineExtension, id=ext_id)
    action = request.POST.get('action', 'approve')
    new_deadline_str = request.POST.get('new_deadline', '')
    if action == 'approve':
        ext.status = 'approved'
        if new_deadline_str:
            try:
                from django.utils.dateparse import parse_datetime
                ext.new_deadline = parse_datetime(new_deadline_str)
                if ext.new_deadline:
                    ext.work.deadline = ext.new_deadline
                    ext.work.save(update_fields=['deadline'])
            except Exception:
                pass
        Notification.send(
            user=ext.user, n_type='info',
            title=f'Продление дедлайна одобрено',
            message=f'Дедлайн по «{ext.work.title}» продлён.',
            link=f'/works/{ext.work.id}/',
        )
    else:
        ext.status = 'rejected'
        Notification.send(
            user=ext.user, n_type='info',
            title=f'Запрос на продление отклонён',
            message=f'Работа: «{ext.work.title}».',
        )
    ext.reviewed_at = timezone.now()
    ext.save(update_fields=['status', 'new_deadline', 'reviewed_at'])
    messages.success(request, 'Решение сохранено.')
    return redirect('teacher_solutions')


@_staff_required
def export_gradebook_excel(request):
    """Экспорт журнала успеваемости в Excel (.xlsx)."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    from django.http import HttpResponse

    group_filter = request.GET.get('group', '')
    students_qs = UserProgress.objects.filter(
        user__is_active=True, user__is_staff=False
    ).select_related('user').order_by('user__last_name', 'user__first_name')
    if group_filter:
        students_qs = students_qs.filter(group=group_filter)

    works = list(PracticalWork.objects.filter(is_active=True).order_by('order'))
    students = list(students_qs)

    # Матрица оценок
    all_solutions = Solution.objects.filter(
        student__in=[s.user for s in students], work__in=works
    ).values('student_id', 'work_id', 'score', 'status').order_by('-score')
    matrix = {}
    for sol in all_solutions:
        key = (sol['student_id'], sol['work_id'])
        if key not in matrix:
            matrix[key] = sol

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Журнал успеваемости"

    # Стили
    header_font  = Font(bold=True, color="FFFFFF", size=11)
    header_fill  = PatternFill("solid", fgColor="4472C4")
    pass_fill    = PatternFill("solid", fgColor="C6EFCE")
    partial_fill = PatternFill("solid", fgColor="FFEB9C")
    fail_fill    = PatternFill("solid", fgColor="FFC7CE")
    center       = Alignment(horizontal="center", vertical="center")
    thin_border  = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"),  bottom=Side(style="thin")
    )

    # Заголовки
    headers = ["№", "Студент", "Группа"] + [f"ПР{w.order}" for w in works] + ["Среднее", "Сдано"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
        cell.border = thin_border

    ws.row_dimensions[1].height = 30
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 10

    # Данные
    for row_idx, prog in enumerate(students, 2):
        user = prog.user
        scores = []
        done = 0

        ws.cell(row=row_idx, column=1, value=row_idx - 1).alignment = center
        ws.cell(row=row_idx, column=2, value=f"{user.last_name} {user.first_name}")
        ws.cell(row=row_idx, column=3, value=prog.group or "—").alignment = center

        for col_idx, work in enumerate(works, 4):
            sol = matrix.get((user.id, work.id))
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.alignment = center
            cell.border = thin_border
            if sol:
                cell.value = sol['score']
                if sol['status'] == 'correct':
                    cell.fill = pass_fill
                    done += 1
                    scores.append(sol['score'])
                elif sol['status'] == 'partially_correct':
                    cell.fill = partial_fill
                    scores.append(sol['score'])
                else:
                    cell.fill = fail_fill
            else:
                cell.value = "—"

        avg = round(sum(scores) / len(scores), 1) if scores else 0
        avg_cell = ws.cell(row=row_idx, column=len(works) + 4, value=avg)
        avg_cell.alignment = center
        avg_cell.font = Font(bold=True)
        ws.cell(row=row_idx, column=len(works) + 5, value=f"{done}/{len(works)}").alignment = center

    # Ширина колонок для работ
    for i in range(len(works)):
        ws.column_dimensions[get_column_letter(4 + i)].width = 7

    # Легенда
    legend_row = len(students) + 3
    ws.cell(row=legend_row, column=1, value="Легенда:")
    for col, (label, fill) in enumerate([("Зачтено", pass_fill), ("Частично", partial_fill), ("Не зачтено", fail_fill)], 2):
        c = ws.cell(row=legend_row, column=col, value=label)
        c.fill = fill
        c.alignment = center

    resp = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    filename = f"gradebook{'_' + group_filter if group_filter else ''}.xlsx"
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(resp)
    return resp


@login_required
def export_gradebook_csv(request):
    """Экспорт журнала успеваемости в CSV (UTF-8 BOM для Excel)."""
    import csv
    if not request.user.is_staff:
        return redirect('home')

    group_filter = request.GET.get('group', '')
    students_qs = UserProgress.objects.filter(
        user__is_active=True, user__is_staff=False
    ).select_related('user').order_by('user__last_name', 'user__first_name')
    if group_filter:
        students_qs = students_qs.filter(group=group_filter)

    works = list(PracticalWork.objects.filter(is_active=True).order_by('order'))
    students = list(students_qs)

    all_solutions = Solution.objects.filter(
        student__in=[s.user for s in students], work__in=works
    ).values('student_id', 'work_id', 'score', 'status').order_by('-score')
    matrix = {}
    for sol in all_solutions:
        key = (sol['student_id'], sol['work_id'])
        if key not in matrix:
            matrix[key] = sol

    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    filename = f"gradebook{'_' + group_filter if group_filter else ''}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # UTF-8 BOM so Excel opens Cyrillic correctly
    response.write('')
    writer = csv.writer(response)

    # Header row
    header = ['№', 'Студент', 'Группа'] + [f'ПР{w.order}' for w in works] + ['Среднее', 'Сдано']
    writer.writerow(header)

    for idx, sp in enumerate(students, 1):
        scores = []
        done = 0
        for w in works:
            sol = matrix.get((sp.user_id, w.id))
            if sol and sol['status'] == 'correct':
                scores.append(sol['score'] or 0)
                done += 1
            elif sol and sol['score']:
                scores.append(sol['score'])
            else:
                scores.append('')
        avg = round(sum(s for s in scores if s != ''), 1) if any(s != '' for s in scores) else ''
        row = [
            idx,
            f"{sp.user.last_name} {sp.user.first_name}",
            getattr(sp, 'group', '') or '',
        ] + scores + [avg, f"{done}/{len(works)}"]
        writer.writerow(row)

    return response


# ══════════════════════════════════════════════════════════════════════════════
# ПРОГРЕСС-БЛОКИРОВКА МОДУЛЕЙ
# ══════════════════════════════════════════════════════════════════════════════

def get_module_unlock_status(user, modules):
    """
    Возвращает dict {module_id: is_unlocked}.
    Теория всегда читаема, тест модуля N требует прохождения теста N-1.
    """
    status = {}
    prev_passed = True  # первый модуль всегда открыт

    passed_quiz_modules = set(
        QuizAttempt.objects.filter(user=user, passed=True)
        .values_list('quiz__module_id', flat=True)
    )

    for module in sorted(modules, key=lambda m: m.order):
        if not module.requires_quiz_pass:
            status[module.id] = {'theory': True, 'quiz': True, 'locked': False}
        else:
            quiz_unlocked = prev_passed
            status[module.id] = {
                'theory': True,       # теория всегда открыта
                'quiz': quiz_unlocked,
                'locked': not quiz_unlocked,
            }
        prev_passed = module.id in passed_quiz_modules
    return status


# ══════════════════════════════════════════════════════════════════════════════
# КОНСТРУКТОР СХЕМ
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def circuit_editor(request, work_id):
    """Открыть симулятор схем для задания."""
    work = get_object_or_404(PracticalWork, id=work_id, is_active=True)
    return render(request, 'works/circuit_simulator.html', {
        'work': work,
        'initial_circuit': None,
    })


def pid_simulator(request):
    """ПИД-симулятор для МДК 03.02 — доступен без регистрации."""
    return render(request, 'works/pid_simulator.html')


@login_required
def circuit_editor_free(request):
    """Свободный симулятор без привязки к заданию."""
    return render(request, 'works/circuit_simulator.html', {
        'work': None,
        'initial_circuit': None,
    })


@login_required
@require_http_methods(['POST'])
def circuit_save(request, work_id):
    """Автосохранение черновика схемы (AJAX)."""
    work = get_object_or_404(PracticalWork, id=work_id, is_active=True)
    try:
        body = request.body.decode('utf-8')
        json.loads(body)  # validate JSON
    except Exception:
        return JsonResponse({'status': 'error', 'msg': 'invalid json'}, status=400)
    draft, _ = CircuitDraft.objects.get_or_create(
        student=request.user, work=work,
        defaults={'circuit_json': body}
    )
    draft.circuit_json = body
    draft.save(update_fields=['circuit_json', 'updated_at'])
    return JsonResponse({'status': 'ok', 'saved_at': draft.updated_at.strftime('%H:%M:%S')})


@login_required
@require_http_methods(['POST'])
def circuit_submit(request, work_id):
    """Сдать схему как решение."""
    work = get_object_or_404(PracticalWork, id=work_id, is_active=True)
    circuit_json = request.POST.get('circuit_json', '{}')
    comment      = request.POST.get('comment', '')
    try:
        json.loads(circuit_json)
    except Exception:
        messages.error(request, 'Некорректные данные схемы.')
        return redirect('circuit_editor', work_id=work_id)

    sol = CircuitSolution.objects.create(
        student=request.user, work=work,
        circuit_json=circuit_json, comment=comment,
        status='submitted',
    )
    # Уведомление преподавателям
    for teacher in User.objects.filter(is_staff=True, is_active=True):
        Notification.objects.create(
            user=teacher,
            title=f'Новая схема от {request.user.last_name} {request.user.first_name}',
            message=f'Работа «{work.title}» — схема отправлена на проверку.',
            n_type='info',
        )
    messages.success(request, 'Схема отправлена на проверку!')
    return redirect('circuit_solution_detail', sol_id=sol.id)


@login_required
def circuit_solution_detail(request, sol_id):
    """Просмотр сданной схемы студентом."""
    sol = get_object_or_404(CircuitSolution, id=sol_id)
    if sol.student != request.user and not request.user.is_staff:
        return redirect('home')
    return render(request, 'works/circuit_solution_view.html', {
        'solution': sol,
        'review_mode': False,
    })


@login_required
def circuit_review(request, sol_id):
    """Преподаватель проверяет и оценивает схему."""
    if not request.user.is_staff:
        return redirect('home')
    sol = get_object_or_404(CircuitSolution, id=sol_id)
    if request.method == 'POST':
        status   = request.POST.get('status', 'reviewed')
        score    = int(request.POST.get('score', 0))
        comment  = request.POST.get('teacher_comment', '')
        sol.status = status
        sol.score  = min(score, sol.work.max_score)
        sol.teacher_comment = comment
        sol.reviewed_at = timezone.now()
        sol.save()
        Notification.objects.create(
            user=sol.student,
            title=f'Схема проверена: {sol.work.title}',
            message=f'Статус: {sol.get_status_display()}. Баллы: {sol.score}/{sol.work.max_score}.'
                    + (f'\nКомментарий: {comment}' if comment else ''),
            n_type='info',
        )
        messages.success(request, 'Оценка сохранена.')
        return redirect('circuit_solutions_list')
    return render(request, 'works/circuit_solution_view.html', {
        'solution': sol,
        'review_mode': True,
    })


@login_required
def circuit_solutions_list(request):
    """Список всех сданных схем для преподавателя."""
    if not request.user.is_staff:
        return redirect('home')
    sols = CircuitSolution.objects.select_related('student', 'work').order_by('-submitted_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        sols = sols.filter(status=status_filter)
    return render(request, 'works/circuit_solutions_list.html', {
        'solutions': sols[:100],
        'status_filter': status_filter,
    })


# ══════════════════════════════════════════════════════════════════════════════
# КУРСОВЫЕ РАБОТЫ
# ══════════════════════════════════════════════════════════════════════════════

@_staff_required
def coursework_list(request):
    """Список всех курсовых работ (учитель)."""
    subject_id = request.GET.get('subject', '')
    qs = CourseWork.objects.select_related('student', 'subject', 'assigned_by').order_by(
        'subject__title', 'student__last_name'
    )
    if subject_id:
        qs = qs.filter(subject_id=subject_id)
    subjects = Subject.objects.filter(is_active=True).order_by('order')
    return render(request, 'works/coursework_list.html', {
        'courseworks': qs,
        'subjects': subjects,
        'selected_subject': subject_id,
    })


@_staff_required
@require_http_methods(['GET', 'POST'])
def coursework_assign(request, cw_id=None):
    """Создать или редактировать назначение курсовой работы."""
    cw = get_object_or_404(CourseWork, id=cw_id) if cw_id else None
    students = User.objects.filter(is_active=True, is_staff=False).order_by('last_name', 'first_name')
    subjects = Subject.objects.filter(is_active=True).order_by('order')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id') or None
        title      = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status     = request.POST.get('status', 'assigned')
        deadline   = request.POST.get('deadline') or None
        teacher_note = request.POST.get('teacher_note', '').strip()
        grade_raw  = request.POST.get('grade', '')
        grade      = int(grade_raw) if grade_raw.isdigit() and 1 <= int(grade_raw) <= 5 else None

        if not title or not student_id:
            messages.error(request, 'Укажи студента и тему.')
        else:
            if cw:
                cw.student_id   = student_id
                cw.subject_id   = subject_id
                cw.title        = title
                cw.description  = description
                cw.status       = status
                cw.deadline     = deadline
                cw.teacher_note = teacher_note
                cw.grade        = grade
                cw.save()
                messages.success(request, 'Курсовая обновлена.')
            else:
                cw = CourseWork.objects.create(
                    student_id=student_id, subject_id=subject_id,
                    title=title, description=description, status=status,
                    deadline=deadline, teacher_note=teacher_note,
                    grade=grade, assigned_by=request.user,
                )
                messages.success(request, f'Курсовая назначена студенту.')
                Notification.send(
                    user=cw.student, n_type='info',
                    title='Назначена курсовая работа',
                    message=f'Тема: «{cw.title}»',
                )
            return redirect('coursework_list')

    return render(request, 'works/coursework_assign.html', {
        'cw': cw,
        'students': students,
        'subjects': subjects,
        'status_choices': CourseWork.STATUS_CHOICES,
    })


@_staff_required
@require_http_methods(['POST'])
def coursework_delete(request, cw_id):
    cw = get_object_or_404(CourseWork, id=cw_id)
    cw.delete()
    messages.success(request, 'Курсовая удалена.')
    return redirect('coursework_list')


# ══════════════════════════════════════════════════════════════════════════════
# АЛГОРИТМ-ВИЗУАЛИЗАТОР
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def algo_visualizer(request):
    return render(request, 'works/algo_visualizer.html')


# ══════════════════════════════════════════════════════════════════════════════
# PYGRID ЛИДЕРБОРД API
# ══════════════════════════════════════════════════════════════════════════════

@login_required
@require_http_methods(['POST'])
def pygrid_score_submit(request):
    """Сохранить результат PyGrid для текущего пользователя."""
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'bad json'}, status=400)
    rounds   = int(data.get('rounds_completed', 0))
    stars    = int(data.get('stars_total', 0))
    steps    = int(data.get('best_steps', 0))
    score, _ = PyGridScore.objects.get_or_create(user=request.user)
    if rounds > score.rounds_completed or (rounds == score.rounds_completed and stars > score.stars_total):
        score.rounds_completed = rounds
        score.stars_total = stars
        score.best_steps = steps
        score.save()
    return JsonResponse({'ok': True, 'rounds': score.rounds_completed, 'stars': score.stars_total})


@login_required
def pygrid_leaderboard(request):
    """Топ-20 игроков PyGrid."""
    top = list(
        PyGridScore.objects.select_related('user')
        .order_by('-rounds_completed', '-stars_total', 'best_steps')[:20]
    )
    rows = []
    me_rank = None
    for i, s in enumerate(top, 1):
        rows.append({
            'rank': i,
            'name': s.user.get_full_name() or s.user.username,
            'rounds': s.rounds_completed,
            'stars': s.stars_total,
            'steps': s.best_steps,
            'is_me': s.user_id == request.user.id,
        })
        if s.user_id == request.user.id:
            me_rank = i
    return JsonResponse({'leaderboard': rows, 'me_rank': me_rank})


@login_required
@require_http_methods(['POST'])
def mark_review_done(request, rr_id):
    """Преподаватель закрывает запрос на проверку."""
    if not request.user.is_staff:
        return JsonResponse({'ok': False}, status=403)
    ReviewRequest.objects.filter(id=rr_id).update(status='done')
    return JsonResponse({'ok': True})


@login_required
@require_http_methods(['POST'])
def submit_all_for_review(request):
    """Студент отправляет все работы на проверку; ИИ запускается для каждого решения без завершённого CodeCheck."""
    all_solutions = Solution.objects.filter(student=request.user)
    solutions_count = all_solutions.count()
    if solutions_count == 0:
        return JsonResponse({'ok': False, 'error': 'Нет сданных работ'}, status=400)

    comment = request.POST.get('comment', '').strip()[:500]

    req = ReviewRequest.objects.create(
        student=request.user,
        solutions_count=solutions_count,
        comment=comment,
    )

    # Запускаем ИИ-проверку для решений без завершённого CodeCheck
    already_checked_ids = set(
        CodeCheck.objects.filter(
            solution__student=request.user,
            status='completed',
        ).values_list('solution_id', flat=True)
    )
    in_progress_ids = set(
        CodeCheck.objects.filter(
            solution__student=request.user,
            status='in_progress',
        ).values_list('solution_id', flat=True)
    )
    to_check = [s for s in all_solutions if s.id not in already_checked_ids and s.id not in in_progress_ids]

    import threading

    def _run(solution_id, cc_id):
        try:
            checker = AICodeChecker()
            checker.check_solution(solution_id, code_check_id=cc_id)
        except Exception:
            logger.exception('submit_all_for_review: AI check failed for solution %s', solution_id)

    launched = 0
    for sol in to_check:
        cc = CodeCheck.objects.create(
            solution=sol,
            status='in_progress',
            check_type='auto',
            created_at=timezone.now(),
        )
        t = threading.Thread(target=_run, args=(sol.id, cc.id), daemon=True)
        t.start()
        launched += 1

    return JsonResponse({
        'ok': True,
        'requested_at': req.requested_at.strftime('%d.%m.%Y %H:%M'),
        'solutions_count': solutions_count,
        'ai_launched': launched,
    })

