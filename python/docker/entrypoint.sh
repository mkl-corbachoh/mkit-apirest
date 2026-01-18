#!/bin/sh
set -e

# Migraciones
# Nota: Para usar con psycopg2, asegúrate de que DATABASE_URL en env.py 
# usa psycopg2 o psycopg. Para asyncpg, env.py debe manejo síncrono en migraciones.
alembic upgrade head

# Arranque API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
