# Dockerfile (Python CLI)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Paquetes básicos (opcional pero útil en slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY . /app

# La app es interactiva de consola
# Si más adelante tienes API Flask/FastAPI, cambia a uvicorn/python app.py
CMD ["python", "main.py"]
