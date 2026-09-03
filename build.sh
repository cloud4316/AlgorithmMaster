#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Загрузка данных из SQLite-дампа (только при первом деплое)
if [ -f data_dump.json ] && [ "$LOAD_FIXTURE" = "1" ]; then
    echo ">>> Loading data fixture..."
    python manage.py loaddata data_dump.json
    echo ">>> Data loaded successfully"
fi
