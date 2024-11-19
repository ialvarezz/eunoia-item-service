from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.order import Base


class ProductsOrdered(Base):
    __tablename__ = 'products_ordered'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_id = Column(Integer, index=True)
    order = relationship("Order", back_populates="products")