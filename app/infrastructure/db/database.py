from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# Объявляем переменные, но НЕ инициализируем
async_engine: AsyncEngine = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] = None


async def init_db():
    """Инициализация БД - вызывается из async main()"""
    global async_engine, AsyncSessionLocal
    
    async_engine = create_async_engine(
        url=settings.database_url,
        echo=False,
        pool_pre_ping=True,
        connect_args={"server_settings": {"jit": "off"}}
    )
    
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine, 
        expire_on_commit=False, 
        autoflush=False
    )
    
    # Создаём таблицы
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Закрытие соединений при остановке"""
    if async_engine:
        await async_engine.dispose()
