from typing import List, Dict
from sync_app.database import SessionLocal, init_db
from sync_app.models import Trade

def load_data(data: List[Dict]) -> None:
    """
    Синхронно загружает данные торгов в базу данных.

    Args:
        data (List[Dict]): Список словарей с данными торгов.
    """
    session = SessionLocal()
    try:
        trades = [
            Trade(
                trade_date=record["trade_date"],
                volume=record["volume"],
                price=record["price"]
            ) for record in data
        ]
        session.add_all(trades)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error loading data into DB: {e}")
    finally:
        session.close()