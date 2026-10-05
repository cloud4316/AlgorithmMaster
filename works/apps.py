import logging
import os
import shutil
import subprocess
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

from django.apps import AppConfig

logger = logging.getLogger('backup')

BACKUP_INTERVAL = 30 * 60   # 30 минут
BACKUP_KEEP_DAYS = 7


def _do_backup(project_dir: Path, backup_root: Path):
    stamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    dest  = backup_root / stamp
    log_file = project_dir / 'backup.log'

    def log(level, msg):
        line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {msg}"
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
        except Exception:
            pass
        if level == 'ERROR':
            logger.error('[BACKUP] %s', msg)
        elif level == 'WARN':
            logger.warning('[BACKUP] %s', msg)
        else:
            logger.info('[BACKUP] %s', msg)

    try:
        dest.mkdir(parents=True, exist_ok=True)

        db_src = project_dir / 'db.sqlite3'
        if not db_src.exists():
            raise FileNotFoundError(f'db.sqlite3 не найден: {db_src}')
        db_size_kb = round(db_src.stat().st_size / 1024, 1)
        shutil.copy2(db_src, dest / 'db.sqlite3')
        log('INFO', f'db.sqlite3 скопирован ({db_size_kb} КБ) -> {dest}')

        media_src = project_dir / 'media'
        if media_src.exists():
            media_dest = dest / 'media'
            shutil.copytree(media_src, media_dest, dirs_exist_ok=True)
            n = sum(1 for _ in media_dest.rglob('*') if _.is_file())
            log('INFO', f'media/ скопирован ({n} файлов)')
        else:
            log('WARN', 'media/ не найден — пропущено')

        # Удаляем бэкапы старше BACKUP_KEEP_DAYS
        cutoff = datetime.now() - timedelta(days=BACKUP_KEEP_DAYS)
        removed = 0
        for d in backup_root.iterdir():
            if d.is_dir() and d != dest:
                try:
                    if datetime.fromtimestamp(d.stat().st_mtime) < cutoff:
                        shutil.rmtree(d)
                        removed += 1
                except Exception:
                    pass
        if removed:
            log('INFO', f'Удалено старых бэкапов: {removed}')

        total_kb = round(sum(f.stat().st_size for f in backup_root.rglob('*') if f.is_file()) / 1024)
        log('INFO', f'Бэкап УСПЕШЕН. Хранилище: {total_kb} КБ ({backup_root})')

    except Exception as exc:
        log('ERROR', f'Бэкап FAILED: {exc}')


def _backup_loop(project_dir: Path, backup_root: Path):
    _do_backup(project_dir, backup_root)
    t = threading.Timer(BACKUP_INTERVAL, _backup_loop, args=(project_dir, backup_root))
    t.daemon = True
    t.start()


def _start_ollama_if_needed():
    """Запускает ollama serve если сервер не отвечает."""
    import urllib.request
    try:
        urllib.request.urlopen('http://localhost:11434/api/tags', timeout=2)
        logger.info('[OLLAMA] Сервер уже запущен.')
        return
    except Exception:
        pass

    try:
        subprocess.Popen(
            ['ollama', 'serve'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        logger.info('[OLLAMA] Запуск ollama serve...')
    except FileNotFoundError:
        logger.warning('[OLLAMA] ollama не найден в PATH — автозапуск невозможен.')
        return
    except Exception as e:
        logger.warning('[OLLAMA] Ошибка автозапуска: %s', e)
        return

    # Ждём старта и сбрасываем кеш доступности
    time.sleep(5)
    try:
        urllib.request.urlopen('http://localhost:11434/api/tags', timeout=3)
        logger.info('[OLLAMA] Сервер запущен успешно.')
        try:
            from works import ai_checker
            ai_checker._ollama_available = None  # сброс кеша — следующий вызов перепроверит
        except Exception:
            pass
    except Exception:
        logger.warning('[OLLAMA] Сервер не ответил за 5 секунд после запуска.')


class WorksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'works'

    def ready(self):
        # Не запускать при manage.py migrate, collectstatic и т.д.
        if os.environ.get('RUN_MAIN') != 'true':
            return

        # Автозапуск Ollama
        t_ollama = threading.Thread(target=_start_ollama_if_needed, daemon=True)
        t_ollama.start()

        # Авто-бэкап
        project_dir = Path(__file__).resolve().parent.parent
        backup_root = project_dir.parent / 'ОАИП_backups'
        t = threading.Timer(5, _backup_loop, args=(project_dir, backup_root))
        t.daemon = True
        t.start()
        logger.info('[BACKUP] Авто-бэкап запущен, интервал %d мин, хранилище: %s',
                    BACKUP_INTERVAL // 60, backup_root)
