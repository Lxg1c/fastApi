from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.category import crud
from api_v1.category.schemas import (
    CategorySchema,
    CategoryCreate,
    CategoryUpdate,
)
from core.models import Category
from core.models.db_helper import db_helper
from core.services.shared.dependencies import get_object_by_id_or_404

# Создаём роутер для всех эндпоинтов, связанных с категориями
router = APIRouter(prefix="/category", tags=["Category"])


# Эндпоинт: Получить список всех категорий
@router.get("/", response_model=list[CategorySchema])
async def get_categories(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_categories(session=session)


# Эндпоинт: Создать новую категорию
@router.post("/", response_model=CategorySchema)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Category:
    return await crud.create_category(session=session, category=category_in)


# Эндпоинт: Получить категорию по ID
@router.get("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_category_by_id(session=session, category_id=category_id)


# Эндпоинт: Обновить существующую категорию по ID (полное обновление — PUT)
@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_update: CategoryUpdate,  # Новые данные
    category_in: CategorySchema = Depends(
        get_category_by_id
    ),  # Текущая категория из БД
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(  # 💡 Лучше переименовать в update_category
        category_in=category_in,
        session=session,
        category_update=category_update,
        partial=False,  # Обновляем все поля (PUT)
    )


# Эндпоинт: Удалить категорию по ID
@router.delete("/{category_id}/")
async def delete_category(
    category: Category = Depends(
        get_object_by_id_or_404(
            model=Category,
            id_name="category_id",
            get_func=crud.get_category_by_id,
        )
    ),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await crud.delete_category(category=category, session=session)
        return {
            "message": "Category deleted",
        }
    except Exception as err:
        # Обработка ошибок при удалении (например, внешние ключи мешают удалению)
        return {
            "message": "Error when deleting category",
            "error": str(err),
        }
