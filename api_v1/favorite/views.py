from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.favorite.crud import (
    get_user_favorite,
    add_to_favorite,
    get_favorite_item,
    delete_favorite_item,
)
from api_v1.favorite.schemas import (
    FavoriteItemRead,
    FavoriteItemBase,
    FavoriteItemCreate,
)
from core.models.db_helper import db_helper

router = APIRouter(prefix="/favorite", tags=["Favorite"])


@router.get("/", response_model=List[FavoriteItemRead])
async def get_cart_items(
    user_id: int,  # В реальном приложении — получай из токена
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_user_favorite(session, user_id)


@router.post("/", response_model=FavoriteItemRead)
async def add_item_to_cart(
    item: FavoriteItemCreate,
    user_id: int,  # В реальном приложении — получай из токена
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await add_to_favorite(session, user_id, item)


@router.delete("/", response_model=None)
async def remove_cart_item(
    product_id: int,
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> FavoriteItemBase:

    deleted_item = await get_favorite_item(
        session=session,
        product_id=product_id,
        user_id=user_id,
    )

    if not deleted_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await delete_favorite_item(
        session=session,
        user_id=user_id,
        product_id=product_id,
    )

    return deleted_item
