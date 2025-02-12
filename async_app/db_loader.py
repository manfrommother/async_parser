from typing import List, Dict
from async_app.database import async_session, init_db
from async_app.models import Trade

async def load_data(data: List[Dict]) -> None:
    """
    Асинхронно загружает данные торгов в базу данных.

    Args:
        data (List[Dict]): Список словарей с данными торгов.
    """
    async with async_session() as session:
        async with session.begin():
            trades = [
                Trade(
                    trade_date=record["trade_date"],
                    volume=record["volume"],
                    price=record["price"]
                ) for record in data
            ]
            session.add_all(trades)
        await session.commit()
