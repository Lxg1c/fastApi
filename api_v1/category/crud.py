from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from core.services.shared.dependencies import (
    get_all_records,
    create_record,
    update_record,
    delete_record,
)
from .schemas import (
    CategoryCreate,
    CategorySchema,
    CategoryUpdatePartial,
    CategoryUpdate,
)


# Получить список всех категорий
async def get_categories(
    session: AsyncSession,
) -> List[Category]:
    return await get_all_records(session, Category)


# Создать новую категорию
async def create_category(
    session: AsyncSession,
    category: CategoryCreate,
) -> Category:
    # Преобразуем Pydantic-схему в словарь и создаём запись
    return await create_record(session, Category, category.model_dump())


# Получить категорию по её ID
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


# Удалить категорию
async def delete_category(
    session: AsyncSession,
    category: CategorySchema,
):
    await session.delete(category)
    await session.commit()
