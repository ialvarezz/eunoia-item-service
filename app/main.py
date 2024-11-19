from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from dotenv import load_dotenv
import os

from app.database import get_db
from app.schemas.order import OrderCreate, Order
from app.schemas.productsOrdered import ProductsOrderedCreate, ProductsOrdered
from app.crud import (
    create_order,
    add_products_to_order,
    get_orders_by_user,
    get_all_orders,
    update_order_state,
    get_products_by_order
)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Orders Service", version="1.0.0")


@app.post("/orders/", response_model=Order, status_code=201)
async def create_new_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new order.
    """
    new_order = await create_order(db=db, order=order)
    return new_order


@app.post("/orders/{order_id}/products/", response_model=List[ProductsOrdered], status_code=201)
async def add_products(order_id: int, products: List[ProductsOrderedCreate], db: AsyncSession = Depends(get_db)):
    """
    Add products to an order.
    """
    existing_order = await get_products_by_order(db=db, order_id=order_id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    added_products = await add_products_to_order(db=db, order_id=order_id, products=products)
    return added_products


@app.get("/orders/user/{user_id}", response_model=List[Order])
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all orders for a specific user.
    """
    orders = await get_orders_by_user(db=db, user_id=user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders


@app.get("/orders/", response_model=List[Order])
async def get_all_user_orders(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all orders in the system.
    """
    orders = await get_all_orders(db=db)
    return orders


@app.patch("/orders/{order_id}/state/", response_model=Order)
async def update_order_status(order_id: int, new_state: str, db: AsyncSession = Depends(get_db)):
    """
    Update the state of an order.
    """
    updated_order = await update_order_state(db=db, order_id=order_id, new_state=new_state)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@app.get("/orders/{order_id}/products/", response_model=List[ProductsOrdered])
async def get_order_products(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all products for a specific order.
    """
    products = await get_products_by_order(db=db, order_id=order_id)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this order")
    return products
