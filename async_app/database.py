from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from async_app.models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:12345678@localhost:5432/spimex"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    """
    Инициализировать базу данных (создать таблицы).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)