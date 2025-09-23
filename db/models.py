from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from db.base import Base

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    trading_symbol = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    instrument_token = Column(Integer, unique=True, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    pnl = Column(Float, nullable=True)
    pnl_percentage = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    comments = Column(Text, nullable=True)
