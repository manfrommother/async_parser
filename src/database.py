from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .config import DATABASE_URL, SYNC_DATABASE_URL

#Асинхронный движок и сессия
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

#Синхронный движок и сессия
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SyncSessionLocal = sessionmaker(sync_engine)

async def get_async_session() -> AsyncSession:
    '''Создает асинхронную сессию с БД'''
    async with AsyncSessionLocal() as session:
        yield session

def get_sync_session():
    '''Создает синхронную сессию с БД'''
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()