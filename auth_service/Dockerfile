FROM python:3.10-slim

# Cài gói phụ trợ
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Tạo virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Tạo user không phải root
RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app

# Entry point cho migration
COPY entrypoint.sh /app
RUN chmod +x entrypoint.sh

# Alembic migrations
RUN alembic init migrations
COPY migrations/ ./migrations

# Phân quyền cho user
RUN chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["./entrypoint.sh"]