from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    state = Column(String, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    products = relationship("ProductsOrdered", back_populates="order")