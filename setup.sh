#!/usr/bin/env bash
# Установка и первоначальная настройка сайта ОАИП
# Запуск: bash setup.sh
set -e

echo "============================================================"
echo " Установка сайта ОАИП"
echo "============================================================"

# ── Определяем Python ────────────────────────────────────────────
echo ""
echo "[1/6] Проверка Python..."
PYTHON=""
for cmd in python python3; do
    if $cmd --version &>/dev/null; then
        VER=$($cmd -c "import sys; print('%d.%d' % sys.version_info[:2])")
        MAJOR=$(echo $VER | cut -d. -f1)
        MINOR=$(echo $VER | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "ОШИБКА: Требуется Python 3.10 или выше. Установите с python.org"
    exit 1
fi
echo "OK: $($PYTHON --version)"

# ── Зависимости ──────────────────────────────────────────────────
echo ""
echo "[2/6] Установка зависимостей..."
$PYTHON -m pip install -r requirements.txt --quiet --disable-pip-version-check
echo "OK: зависимости установлены"

# ── Миграции ─────────────────────────────────────────────────────
echo ""
echo "[3/6] Миграции базы данных..."
if ! migrate_out=$($PYTHON manage.py migrate --verbosity=0 2>&1); then
    echo "$migrate_out" | grep -av "^DEBUG" >&2
    echo "ОШИБКА: миграция завершилась с ошибкой"
    exit 1
fi
echo "OK: база данных готова"

# ── Данные ───────────────────────────────────────────────────────
echo ""
echo "[4/6] Заполнение данными..."

run_seed() {
    local cmd=$1
    local label=$2
    if $PYTHON manage.py $cmd --verbosity=0 2>/dev/null; then
        echo "  OK: $label"
    else
        # Повтор с выводом ошибки (не прерываем установку)
        echo "  WARN: $label — запускаем повторно с выводом ошибки..."
        $PYTHON manage.py $cmd 2>&1 | grep -av "^DEBUG" | tail -5 || true
    fi
}

run_seed seed_works   "практические работы"
run_seed seed_theory  "теория ОАИП"
run_seed seed_quizzes "тесты ОАИП"
run_seed seed_mps_full  "теория МПС (часть 1)" 2>/dev/null || true
run_seed seed_mps_full2 "теория МПС (часть 2)" 2>/dev/null || true

$PYTHON manage.py create_default_admin --verbosity=0 2>/dev/null || \
$PYTHON manage.py create_default_admin 2>&1 | grep -av "^DEBUG" || true

echo "  OK: администратор"

# ── Статика ──────────────────────────────────────────────────────
echo ""
echo "[5/6] Сбор статических файлов..."
$PYTHON manage.py collectstatic --noinput --clear --verbosity=0
echo "OK: статика собрана"

# ── Итог ─────────────────────────────────────────────────────────
echo ""
echo "[6/6] Проверка конфигурации..."
$PYTHON manage.py check --verbosity=0 2>&1 | grep -av "^DEBUG" | grep -av "staticfiles.W004" || true
echo "OK: конфигурация в порядке"

echo ""
echo "============================================================"
echo " Установка завершена!"
echo ""
echo "  Запуск сервера:  bash start.sh"
echo ""
echo "  Данные для входа (смените пароль после первого входа!):"
echo "    Поле входа : admin admin"
echo "    Пароль     : admin"
echo "============================================================"
