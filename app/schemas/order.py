from typing import List
from datetime import datetime
from pydantic import BaseModel
from app.schemas.productsOrdered import ProductsOrdered

class OrderBase(BaseModel):
    user_id: int
    state: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    date: datetime
    products: List[ProductsOrdered]  # Represents related products

    class Config:
        orm_mode: True
