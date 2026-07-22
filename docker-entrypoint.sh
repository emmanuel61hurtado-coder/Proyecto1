#!/bin/sh
set -e

echo "🌙 Iniciando aplicación..."

# Esperar a que PostgreSQL esté disponible si se usa DATABASE_URL
if [ -n "$DATABASE_URL" ]; then
    echo "⏳ Esperando conexión a PostgreSQL..."
    python -c "
import time, sys
try:
    import psycopg2
    from urllib.parse import urlparse
    url = urlparse('$DATABASE_URL')
    retries = 30
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=url.hostname,
                port=url.port or 5432,
                user=url.username,
                password=url.password,
                dbname=url.path.lstrip('/')
            )
            conn.close()
            print('✅ PostgreSQL listo')
            sys.exit(0)
        except Exception as e:
            print(f'   Intento {i+1}/{retries}: {e}')
            time.sleep(2)
    print('❌ No se pudo conectar a PostgreSQL')
    sys.exit(1)
except ImportError:
    print('psycopg2 no instalado, continuando...')
"
fi

echo "🚀 Arrancando Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    "run:app"
