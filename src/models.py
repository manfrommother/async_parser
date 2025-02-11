from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class SpimexData(Base):
    '''Модель для Spimex'''
    __tablename__ = 'spimex_data'

    id = Column(Integer, primary_key=True)
    trade_date = Column(DateTime, nullable=False)
    product = Column(String, nullable=False)
    delivery_basis = Column(String, nullable=False)
    delivery_type = Column(String, nullable=False)
    volume = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f'<SpimexData(trade_date={self.trade_date}, product={self.product})>'
    
