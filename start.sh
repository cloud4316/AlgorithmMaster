#!/usr/bin/env bash
# Запуск сервера ОАИП
# Режимы:
#   bash start.sh         — разработка: авто-релоад при изменении файлов
#   bash start.sh --prod  — продакшн:   Waitress, 8 потоков, без авто-релоада

PYTHON=python; python --version &>/dev/null || PYTHON=python3
PORT=${PORT:-8000}
MODE="dev"
[[ "$*" == *"--prod"* ]] && MODE="prod"

# ── Проверяем наличие зависимостей ───────────────────────────────
if ! $PYTHON -c "import django" &>/dev/null; then
    echo "[!] Зависимости не установлены. Запустите setup.sh"
    exit 1
fi

# ── Первичная настройка если БД не готова ────────────────────────
if ! $PYTHON manage.py migrate --check --verbosity=0 &>/dev/null; then
    echo "[!] БД не настроена. Запускаем первичную установку..."
    $PYTHON manage.py migrate --verbosity=0
    $PYTHON manage.py seed_works      --verbosity=0 2>/dev/null || true
    $PYTHON manage.py seed_theory     --verbosity=0 2>/dev/null || true
    $PYTHON manage.py seed_quizzes    --verbosity=0 2>/dev/null || true
    $PYTHON manage.py seed_mps_full   --verbosity=0 2>/dev/null || true
    $PYTHON manage.py seed_mps_full2  --verbosity=0 2>/dev/null || true
    $PYTHON manage.py create_default_admin --verbosity=0 2>/dev/null || true
    $PYTHON manage.py collectstatic --noinput --clear --verbosity=0 2>/dev/null || true
    echo "[OK] Первичная установка завершена."
fi

# ── Чистим устаревшие сессии из БД ──────────────────────────────
$PYTHON manage.py clearsessions --verbosity=0 2>/dev/null || true

# ── Определяем локальный IP ──────────────────────────────────────
LOCAL_IP=$($PYTHON -c "
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    print(s.getsockname()[0])
    s.close()
except:
    print('127.0.0.1')
" 2>/dev/null)

echo "============================================================"
echo " AlgorithmMaster — Сервер запускается  [$MODE]"
echo ""
echo "  На этом компьютере : http://127.0.0.1:$PORT/"
echo "  В локальной сети   : http://$LOCAL_IP:$PORT/"
echo "  Панель препод.     : http://127.0.0.1:$PORT/teacher/"
if [[ "$MODE" == "dev" ]]; then
echo ""
echo "  Авто-релоад: ВКЛЮЧЁН — сервер перезапустится"
echo "  при изменении любого .py файла"
fi
echo ""
echo "  Для остановки: Ctrl+C"
echo "============================================================"
echo ""

if [[ "$MODE" == "dev" ]]; then
    # Django runserver: встроенный авто-релоад, доступен по сети
    $PYTHON manage.py runserver 0.0.0.0:$PORT
else
    # Waitress: многопоточный, без авто-релоада
    $PYTHON -m waitress \
        --host=0.0.0.0 \
        --port=$PORT \
        --threads=8 \
        algorithm_site.wsgi:application
fi
