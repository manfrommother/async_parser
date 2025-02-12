from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sync_app.models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/spimex"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    """
    Инициализирует базу данных (создаёт таблицы).
    """
    Base.metadata.create_all(bind=engine)