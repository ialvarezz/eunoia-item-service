from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from typing import List

from app.models import Order, ProductsOrdered
from app.schemas import OrderCreate, ProductsOrderedCreate


# Create a new order
async def create_order(db: AsyncSession, order: OrderCreate) -> Order:
    new_order = Order(user_id=order.user_id, state=order.state, date=order.date)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


# Insert products into an order
async def add_products_to_order(db: AsyncSession, order_id: int, products: List[ProductsOrderedCreate]) -> List[ProductsOrdered]:
    added_products = []
    for product in products:
        new_product = ProductsOrdered(order_id=order_id, item_id=product.item_id)
        db.add(new_product)
        added_products.append(new_product)
    await db.commit()
    return added_products


# Retrieve all orders from a specific user
async def get_orders_by_user(db: AsyncSession, user_id: int) -> List[Order]:
    result = await db.execute(
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.products))
    )
    return result.scalars().all()


# Retrieve all orders
async def get_all_orders(db: AsyncSession) -> List[Order]:
    result = await db.execute(select(Order).options(selectinload(Order.products)))
    return result.scalars().all()


# Change the state of an order
async def update_order_state(db: AsyncSession, order_id: int, new_state: str) -> Order:
    await db.execute(
        update(Order)
        .where(Order.id == order_id)
        .values(state=new_state)
    )
    await db.commit()
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


# Get the list of products for a specific order
async def get_products_by_order(db: AsyncSession, order_id: int) -> List[ProductsOrdered]:
    result = await db.execute(select(ProductsOrdered).where(ProductsOrdered.order_id == order_id))
    return result.scalars().all()
