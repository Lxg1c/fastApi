from typing import List
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Category, Product
from core.services.dependencies import get_all_records, create_record, update_record
from .schemas import (
    CategoryCreate,
    CategorySchema,
    CategoryUpdatePartial,
    CategoryUpdate,
)


async def get_categories(
    session: AsyncSession,
) -> List[Category]:
    return await get_all_records(session, Category)


async def create_category(
    session: AsyncSession,
    category: CategoryCreate,
) -> Category:
    return await create_record(session, Category, category.model_dump())


async def get_category_by_id(
    session: AsyncSession,
    category_id: int,
) -> Category | None:
    return await session.get(Category, category_id)


async def update_product(
    session: AsyncSession,
    category_in: CategorySchema,
    category_update: CategoryUpdate | CategoryUpdatePartial,
    partial: bool = False,
) -> CategorySchema:
    return await update_record(
        session, category_in, category_update.model_dump(exclude_unset=partial), partial
    )


# Рабочий метод
async def delete_category(
    session: AsyncSession,
    category: CategorySchema,
):
    await session.delete(category)
    await session.commit()
