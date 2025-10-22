# Dockerfile
FROM python:3.11-slim

# Set timezone untuk Celery
ENV TZ Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set work directory
WORKDIR /app

# Copy requirements dan install dependencies (buat caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua code
COPY . .

# Command entrypoint buat app (FastAPI) dan worker (Celery)
# Kita akan override command ini di `docker run`
