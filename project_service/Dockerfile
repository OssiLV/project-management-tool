# Build stage
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential && \
    pip install --no-cache-dir --user -r requirements.txt && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Final stage
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chmod +x /app/wait-for-it.sh && \
    chmod +x entrypoint.sh
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"
ENTRYPOINT ["./entrypoint.sh"]