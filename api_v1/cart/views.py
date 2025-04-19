from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.cart.crud import (
    get_user_cart,
    add_to_cart,
    update_cart_item,
    delete_cart_item,
    get_cart_item,
)
from api_v1.cart.schemas import (
    CartItemRead,
    CartItemCreate,
    CartItemUpdate,
    CartItemBase,
)
from core.models.db_helper import db_helper

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=List[CartItemRead])
async def get_cart_items(
    user_id: int,  # В реальном приложении — получай из токена
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_user_cart(session, user_id)


@router.post("/", response_model=CartItemRead)
async def add_item_to_cart(
    item: CartItemCreate,
    user_id: int,  # В реальном приложении — получай из токена
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await add_to_cart(session, user_id, item)


@router.put("/", response_model=CartItemBase)
async def update_cart_quantity(
    product_id: int,
    user_id: int,
    item_data: CartItemUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> CartItemBase:
    # Обновляем запись
    await update_cart_item(
        session=session,
        product_id=product_id,
        user_id=user_id,
        new_data=item_data,
    )

    # Получаем обновлённую запись
    updated_item = await get_cart_item(
        session=session, product_id=product_id, user_id=user_id
    )

    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return updated_item


@router.delete("/", response_model=None)
async def remove_cart_item(
    product_id: int,
    user_id: int,
    size: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> CartItemBase:

    deleted_item = await get_cart_item(
        session=session,
        product_id=product_id,
        user_id=user_id,
    )

    if not deleted_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await delete_cart_item(
        session=session, user_id=user_id, product_id=product_id, size=size
    )

    return deleted_item
