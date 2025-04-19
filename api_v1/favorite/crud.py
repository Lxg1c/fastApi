from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.favorite.schemas import FavoriteItemBase
from core.models.favorite import Favorite


async def get_user_favorite(
    session: AsyncSession,
    user_id: int,
):
    result = await session.execute(
        select(Favorite).where(
            Favorite.user_id == user_id,
        )
    )
    return result.scalars().all()


async def add_to_favorite(
    session: AsyncSession,
    user_id: int,
    item: FavoriteItemBase,
):
    favorite_item = Favorite(
        user_id=user_id,
        product_id=item.product_id,
    )
    session.add(favorite_item)
    await session.commit()
    await session.refresh(favorite_item)
    return favorite_item


async def get_favorite_item(
    session: AsyncSession,
    product_id: int,
    user_id: int,
) -> Optional[FavoriteItemBase]:
    result = await session.execute(
        select(Favorite).where(
            Favorite.product_id == product_id,
            Favorite.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def delete_favorite_item(
    session: AsyncSession,
    product_id: int,
    user_id: int,
):
    await session.execute(
        delete(Favorite).where(
            Favorite.product_id == product_id,
            Favorite.user_id == user_id,
        )
    )
    await session.commit()
