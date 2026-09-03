#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Загрузка данных из SQLite-дампа (только при первом деплое)
echo "LOAD_FIXTURE=$LOAD_FIXTURE"
if [ -f data_dump.json ] && [ "$LOAD_FIXTURE" = "1" ]; then
    echo ">>> Loading data fixture ($(wc -c < data_dump.json) bytes)..."
    python manage.py loaddata data_dump.json
    echo ">>> Data loaded successfully"
else
    echo ">>> Skipping fixture load (LOAD_FIXTURE=$LOAD_FIXTURE, file exists: $([ -f data_dump.json ] && echo yes || echo no))"
fi
