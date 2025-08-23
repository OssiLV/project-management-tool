#!/bin/bash

# Chờ DB ready
python - <<END
import time, os, pymysql

DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_PORT = int(os.getenv("MYSQL_PORT", 3306))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "")

while True:
    try:
        conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
        conn.close()
        print("✅ MariaDB is ready!")
        break
    except Exception:
        print("Waiting for MariaDB...")
        time.sleep(2)
END

# Check nếu migrations chưa init (folder versions rỗng hoặc không tồn tại)
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions)" ]; then
    echo "Generating initial migration..."
    alembic revision --autogenerate -m "Initial project schema"
fi

# Apply migrations
echo "Applying migrations..."
alembic upgrade head

# Start app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000