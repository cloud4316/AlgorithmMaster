from django.db import OperationalError
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserSession, PageView
import time
import threading
import re


class OptimizedTimeTrackingMiddleware(MiddlewareMixin):
    """Оптимизированный middleware для отслеживания времени"""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self._session_timers = {}
        self._last_activity = {}  # Отслеживаем последнюю активность для каждой сессии
        self._skip_paths = {
            '/static/', '/media/', '/favicon.ico', '/api/', 
            '/.well-known/', '/__debug__/', '/admin/'
        }
    
    def should_skip_request(self, request):
        """Проверяем, нужно ли пропустить запрос"""
        if request.method != 'GET':
            return True
            
        for path in self._skip_paths:
            if request.path.startswith(path):
                return True
                
        return False
    
    def process_request(self, request):
        try:
            return self._process_request_safe(request)
        except OperationalError:
            # Таблицы ещё не созданы (migrate не запущен) — пропускаем
            return None
        except Exception:
            return None

    def _process_request_safe(self, request):
        if self.should_skip_request(request):
            return None
            
        if not request.user.is_authenticated:
            return None
            
        # Получаем или создаем активную сессию
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        
        # Проверяем, есть ли активная сессия
        try:
            active_session = UserSession.objects.filter(
                user=request.user,
                session_key=session_key,
                is_active=True
            ).first()
            
            if not active_session:
                # Создаем новую сессию
                active_session = UserSession.objects.create(
                    user=request.user,
                    session_key=session_key,
                    start_time=timezone.now(),
                    is_active=True
                )
            
            # Запускаем таймер для сессии только если его еще нет
            if session_key not in self._session_timers:
                self._session_timers[session_key] = time.time()
                self._last_activity[session_key] = timezone.now()
            
        except Exception:
            # В случае ошибки пропускаем обработку
            pass
    
    def process_response(self, request, response):
        try:
            return self._process_response_safe(request, response)
        except (OperationalError, Exception):
            return response

    def _process_response_safe(self, request, response):
        if self.should_skip_request(request):
            return response
            
        if not request.user.is_authenticated:
            return response
            
        try:
            session_key = request.session.session_key
            if not session_key:
                return response
                
            # Получаем активную сессию
            active_session = UserSession.objects.filter(
                user=request.user,
                session_key=session_key,
                is_active=True
            ).first()
            
            if active_session and session_key in self._session_timers:
                # Обновляем время сессии
                time_spent = time.time() - self._session_timers[session_key]
                active_session.duration_seconds += int(time_spent)
                active_session.page_views += 1
                active_session.save()
                
                # Создаем запись о просмотре страницы
                PageView.objects.create(
                    user=request.user,
                    session=active_session,
                    page_url=request.path,
                    page_title=getattr(response, 'title', ''),
                    time_spent=int(time_spent)
                )
                
                # Обновляем таймер для следующего запроса (НЕ удаляем!)
                self._session_timers[session_key] = time.time()
                self._last_activity[session_key] = timezone.now()
                    
        except Exception:
            # В случае ошибки пропускаем обработку
            pass
            
        return response


class SessionTimeoutMiddleware(MiddlewareMixin):
    """Middleware для автоматического завершения неактивных сессий"""
    
    def process_request(self, request):
        if not request.user.is_authenticated:
            return None
            
        try:
            # Завершаем сессии, которые неактивны более 2 часов (увеличено с 30 минут)
            timeout_threshold = timezone.now() - timezone.timedelta(hours=2)
            
            # Получаем сессии для завершения
            inactive_sessions = UserSession.objects.filter(
                user=request.user,
                is_active=True,
                start_time__lt=timeout_threshold
            )
            
            # Завершаем неактивные сессии
            for session in inactive_sessions:
                session.is_active = False
                session.end_time = timezone.now()
                session.save()

        except Exception:
            pass


# ─── ANSI-цвета для консоли ────────────────────────────────────────────────────
_C = {
    'reset':  '\033[0m',
    'bold':   '\033[1m',
    'cyan':   '\033[36m',
    'yellow': '\033[33m',
    'green':  '\033[32m',
    'blue':   '\033[34m',
    'magenta':'\033[35m',
    'red':    '\033[31m',
    'gray':   '\033[90m',
    'white':  '\033[97m',
}

# URL → читаемое описание (список пар: regex → label)
_URL_LABELS = [
    (r'^/$',                                   'Главная'),
    (r'^/theory/$',                            'Теория — список уроков'),
    (r'^/theory/search/',                      'Поиск по теории'),
    (r'^/theory/lesson/(\d+)/done/',           'Отметил урок изученным'),
    (r'^/theory/lesson/(\d+)/notes/',          'Сохранил конспект'),
    (r'^/theory/lesson/(\d+)/',                'Урок теории'),
    (r'^/works/$',                             'Практические работы'),
    (r'^/works/(\d+)/submit/',                 'Сдаёт работу'),
    (r'^/works/(\d+)/history/',                'История решений'),
    (r'^/works/(\d+)/',                        'Открыл задачу'),
    (r'^/submission/(\d+)/',                   'Сдаёт работу'),
    (r'^/solution/(\d+)/',                     'Просматривает решение'),
    (r'^/solutions/diff/',                     'Сравнение версий'),
    (r'^/quiz/$',                              'Тесты — список'),
    (r'^/quiz/(\d+)/submit/',                  'Сдаёт тест'),
    (r'^/quiz/(\d+)/adaptive/',                'Адаптивный тест'),
    (r'^/quiz/(\d+)/',                         'Открыл тест'),
    (r'^/circuit/editor/(\d+)/',               'Редактор схем — задача'),
    (r'^/circuit/editor/',                     'Редактор схем'),
    (r'^/circuit/submit/',                     'Сдаёт схему'),
    (r'^/circuit/solution/',                   'Просматривает схему'),
    (r'^/circuit/review/',                     'Проверяет схему'),
    (r'^/circuit/solutions/',                  'Список схем'),
    (r'^/profile/',                            'Профиль'),
    (r'^/leaderboard/',                        'Рейтинг'),
    (r'^/results/',                            'Результаты'),
    (r'^/progress/',                           'Мой прогресс'),
    (r'^/playground/',                         'Онлайн-песочница'),
    (r'^/announcements/create/',               'Создаёт объявление'),
    (r'^/announcements/',                      'Объявления'),
    (r'^/subject/',                            'Переключил предмет'),
    (r'^/teacher/grade/',                      'Проверяет работу'),
    (r'^/teacher/analytics/',                  'Аналитика'),
    (r'^/teacher/gradebook/',                  'Журнал'),
    (r'^/teacher/solutions/',                  'Решения студентов'),
    (r'^/teacher/plagiarism/',                 'Проверка на плагиат'),
    (r'^/teacher/export/',                     'Экспорт'),
    (r'^/teacher/',                            'Панель преподавателя'),
    (r'^/about/',                              'О проекте'),
    (r'^/login/',                              'Вход'),
    (r'^/register/',                           'Регистрация'),
]

# Пути, которые НЕ логируем (шум)
_SKIP_LOG_PATHS = (
    '/static/', '/media/', '/favicon', '/api/session-time',
    '/api/activity-data', '/notifications/count', '/__debug__',
    '/api/check-status', '/dev-reload/',
)


def _url_label(path):
    for pattern, label in _URL_LABELS:
        if re.match(pattern, path):
            return label
    return None


def _get_ip(request):
    """Возвращает реальный IP клиента."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '?')


class UserActivityMiddleware:
    """Логирует в консоль: кто зашёл, куда и что сделал (все пользователи)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Фиксируем статус аутентификации ДО выполнения view
        # (нужно для корректного логирования POST /login/)
        was_authenticated = hasattr(request, 'user') and request.user.is_authenticated

        response = self.get_response(request)

        # Пропускаем шумные пути
        path = request.path
        if any(path.startswith(p) for p in _SKIP_LOG_PATHS):
            return response

        # Только GET + POST
        if request.method not in ('GET', 'POST'):
            return response

        self._log(request, response, was_authenticated)
        return response

    def _log(self, request, response, was_authenticated):
        try:
            path   = request.path
            method = request.method
            status = response.status_code
            now    = timezone.localtime().strftime('%H:%M:%S')
            label  = _url_label(path)
            ip     = _get_ip(request)

            # Определяем кто это
            user = request.user
            if user.is_authenticated:
                full_name = user.get_full_name() or user.username
                who = (
                    f"{_C['bold']}{_C['yellow']}{full_name}{_C['reset']}"
                    f"  {_C['gray']}(@{user.username}){_C['reset']}"
                )
            elif path.startswith('/login/') and method == 'POST' and status < 400:
                # Успешный вход — user уже установлен после login()
                full_name = user.get_full_name() or user.username
                who = (
                    f"{_C['bold']}{_C['green']}⟶ ВОШЁЛ: {full_name}{_C['reset']}"
                    f"  {_C['gray']}(@{user.username}){_C['reset']}"
                )
            else:
                # Гость — показываем IP
                who = f"{_C['gray']}Гость  {ip}{_C['reset']}"
                # Гостей логируем только на «важных» страницах (не на /static/ и т.п.)
                if not label:
                    return

            # Цвет статуса
            if status < 300:
                status_color = _C['green']
            elif status < 400:
                status_color = _C['yellow']
            else:
                status_color = _C['red']

            # Метод
            method_color = _C['magenta'] if method == 'POST' else _C['blue']

            parts = [
                f"{_C['gray']}[{now}]{_C['reset']}",
                who,
                f"{method_color}{method}{_C['reset']}",
                f"{_C['cyan']}{path}{_C['reset']}",
                f"{status_color}[{status}]{_C['reset']}",
            ]
            if label:
                parts.append(f"{_C['gray']}— {label}{_C['reset']}")

            print('  '.join(parts), flush=True)
        except Exception:
            pass
