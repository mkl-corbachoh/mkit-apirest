from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

# Async driver (asyncpg)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,            # pon True si quieres ver SQL en consola
    pool_pre_ping=True,
)

# Alternativa con psycopg2 (síncrono) - requiere cambiar toda la lógica a síncrona
# from sqlalchemy import create_engine
# engine = create_engine(
#     settings.DATABASE_URL,
#     echo=False,
#     pool_pre_ping=True,
# )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Alias para compatibilidad
SessionLocal = AsyncSessionLocal
