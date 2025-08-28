#!/bin/bash

# Wait for MariaDB using wait-for-it.sh
echo "[DOING] - Waiting for MariaDB..."
/app/wait-for-it.sh "${MYSQL_HOST:-db}:${MYSQL_PORT:-3306}" --timeout=30 -- echo "[DONE] - MariaDB is ready!"

# Ensure migrations/versions directory exists
if [ ! -d "migrations/versions" ]; then
    echo "[DOING] - Creating migrations/versions folder..."
    mkdir -p /app/migrations/versions
fi

# Check if versions folder is empty
if [ -z "$(ls -A migrations/versions)" ]; then
    echo "[DOING] - Generating initial migration..."
    alembic revision --autogenerate -m "Initial auth schema"
fi

# Apply migrations
echo "[DOING] - Applying migrations..."
alembic upgrade head || { echo "Migration failed"; exit 1; }

# Start application
echo "[DOING] - Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4