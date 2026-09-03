import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── СЕКРЕТНЫЙ КЛЮЧ ────────────────────────────────────────────────────────────
_KEY_FILE = BASE_DIR / 'secret_key.txt'
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if _KEY_FILE.exists():
        SECRET_KEY = _KEY_FILE.read_text(encoding='utf-8').strip()
    else:
        SECRET_KEY = secrets.token_urlsafe(50)
        _KEY_FILE.write_text(SECRET_KEY, encoding='utf-8')

# ─── РЕЖИМ ─────────────────────────────────────────────────────────────────────
_debug_env = os.environ.get('DEBUG')
if _debug_env is not None:
    DEBUG = _debug_env.lower() in ('1', 'true', 'yes')
else:
    DEBUG = (BASE_DIR / 'DEBUG.lock').exists()

# ─── РАЗРЕШЁННЫЕ ХОСТЫ ─────────────────────────────────────────────────────────
ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost']

# ─── CSRF ──────────────────────────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://192.168.0.0:8000',
    'http://10.0.0.0:8000',
]

# ─── ПРИЛОЖЕНИЯ ────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'works',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'works.optimized_middleware.OptimizedTimeTrackingMiddleware',
    'works.optimized_middleware.SessionTimeoutMiddleware',
    'works.optimized_middleware.UserActivityMiddleware',
]

ROOT_URLCONF = 'algorithm_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'works.context_processors.subjects',
            ],
        },
    },
]

WSGI_APPLICATION = 'algorithm_site.wsgi.application'

# ─── БАЗА ДАННЫХ ───────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,
            'init_command': (
                "PRAGMA journal_mode=WAL;"
                "PRAGMA synchronous=NORMAL;"
                "PRAGMA cache_size=10000;"
                "PRAGMA temp_store=MEMORY;"
                "PRAGMA foreign_keys=ON;"
            ),
        },
    }
}

# ─── КЭШ ──────────────────────────────────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'oaip-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}


# ─── БЭКЕНДЫ АВТОРИЗАЦИИ ────────────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'works.backends.FullNameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ─── ПАРОЛИ ────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── ЛОКАЛИЗАЦИЯ ───────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ─── СТАТИКА И МЕДИА ───────────────────────────────────────────────────────────
STATIC_URL = '/static/'
_static_dir = BASE_DIR / 'static'
STATICFILES_DIRS = [_static_dir] if _static_dir.is_dir() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── СЕССИИ ────────────────────────────────────────────────────────────────────
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 604800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ─── АУТЕНТИФИКАЦИЯ ────────────────────────────────────────────────────────────
LOGIN_REDIRECT_URL  = 'home'
LOGIN_URL           = '/login/'
LOGOUT_REDIRECT_URL = 'home'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ─── ЛОГИРОВАНИЕ ───────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {process:d} {thread:d}: {message}',
            'style': '{',
        },
        'simple': {'format': '{levelname}: {message}', 'style': '{'},
        'error_fmt': {
            'format': '[{asctime}] {levelname} {name}\n  URL: {message}\n',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'errors_file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'errors.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG' if DEBUG else 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['errors_file', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['errors_file', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'works': {
            'handlers': ['errors_file', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# ─── EMAIL ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD', '')
DEFAULT_FROM_EMAIL = f'AlgorithmMaster <{EMAIL_HOST_USER or "noreply@algorithmmaster.local"}>'
