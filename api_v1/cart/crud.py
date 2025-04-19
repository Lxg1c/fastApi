from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.cart import Cart
from .schemas import CartItemCreate, CartItemUpdate, CartItemBase


async def get_user_cart(session: AsyncSession, user_id: int):
    result = await session.execute(select(Cart).where(Cart.user_id == user_id))
    return result.scalars().all()


async def add_to_cart(session: AsyncSession, user_id: int, item: CartItemCreate):
    cart_item = Cart(
        user_id=user_id,
        product_id=item.product_id,
        size=item.size,
        quantity=item.quantity,
    )
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)
    return cart_item


async def update_cart_item(
    session: AsyncSession,
    product_id: int,
    user_id: int,
    new_data: CartItemUpdate,
):
    await session.execute(
        update(Cart)
        .where(
            Cart.product_id == product_id, Cart.user_id == user_id
        )  # Запятая вместо AND
        .values(quantity=new_data.quantity)
    )
    await session.commit()


async def get_cart_item(
    session: AsyncSession,
    product_id: int,
    user_id: int,
) -> Optional[CartItemBase]:
    result = await session.execute(
        select(Cart).where(Cart.product_id == product_id, Cart.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def delete_cart_item(
    session: AsyncSession, product_id: int, user_id: int, size: str
):
    await session.execute(
        delete(Cart).where(
            Cart.product_id == product_id,
            Cart.user_id == user_id,
            Cart.size == size,
        )
    )
    await session.commit()
