from pydantic import BaseModel

class ProductsOrderedBase(BaseModel):
    order_id: int
    item_id: int


class ProductsOrderedCreate(ProductsOrderedBase):
    pass


class ProductsOrdered(ProductsOrderedBase):
    id: int

    class Config:
        orm_mode: True
