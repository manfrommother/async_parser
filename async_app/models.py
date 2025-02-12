from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime

Base = declarative_base()

class Trade(Base):
    """
    ORM model representing a trade record.
    """
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_date = Column(DateTime, nullable=False)
    volume = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Trade(id={self.id}, trade_date={self.trade_date}, volume={self.volume}, price={self.price})>"