# ─── Etapa de construcción ───────────────────────────────────────────────────
FROM python:3.11-slim

# Evitar archivos .pyc y hacer que los logs salgan en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python primero (capa cacheada)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn==22.0.0

# Copiar el resto del código
COPY . .

# Crear directorio para la base de datos persistente
RUN mkdir -p /app/instance /app/app/static/uploads

# Puerto que expone la app
EXPOSE 5000

# Script de arranque
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
