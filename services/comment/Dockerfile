# Build stage
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential && \
    pip install --no-cache-dir --user --no-warn-script-location -r requirements.txt && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Final stage
FROM python:3.10-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appuser /app && \
    chmod +x /app/wait-for-it.sh && \
    chmod +x /app/entrypoint.sh
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"
ENTRYPOINT ["./entrypoint.sh"]