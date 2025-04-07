from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.models.cart import Cart


async def add_to_cart(session: AsyncSession, user_id: int, product_id: int, quantity: int = 1):
    """Добавить товар в корзину пользователя"""
    cart_item = await session.execute(
        select(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id)
    )
    cart_item = cart_item.scalars().first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(cart_item)

    await session.commit()
    await session.refresh(cart_item)
    return cart_item


async def get_cart(session: AsyncSession, user_id: int):
    """Получить содержимое корзины пользователя"""
    result = await session.execute(
        select(Cart).options(selectinload(Cart.product)).filter(Cart.user_id == user_id)
    )
    return result.scalars().all()


async def remove_from_cart(session: AsyncSession, user_id: int, product_id: int):
    """Удалить товар из корзины"""
    await session.execute(
        Cart.__table__.delete().where(Cart.user_id == user_id, Cart.product_id == product_id)
    )
    await session.commit()


async def clear_cart(session: AsyncSession, user_id: int):
    """Очистить корзину пользователя"""
    await session.execute(Cart.__table__.delete().where(Cart.user_id == user_id))
    await session.commit()
