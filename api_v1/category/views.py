from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.category import crud
from api_v1.category.schemas import (
    CategorySchema,
    CategoryCreate,
    CategoryUpdate,
    # CategoryUpdatePartial,
)
from core.models import Category
from core.models.db_helper import db_helper

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/", response_model=list[CategorySchema])
async def get_categories(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_categories(session=session)


@router.post("/", response_model=CategorySchema)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Category:
    return await crud.create_category(session=session, category=category_in)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_category_by_id(session=session, category_id=category_id)


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_update: CategoryUpdate,
    category_in: CategorySchema = Depends(get_category_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        category_in=category_in,
        session=session,
        category_update=category_update,
        partial=False,
    )


# @router.patch("/{product_id}", response_model=CategorySchema)
# async def update_product_partial(
#     category_update: CategoryUpdatePartial,
#     category_in: CategorySchema = Depends(get_category_by_id),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.update_product(
#         category_in=category_in,
#         session=session,
#         category_update=category_update,
#         partial=True,
#     )


@router.delete("/{category_id}")
async def delete_category(
    category: CategorySchema = Depends(get_category_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        await crud.delete_category(category=category, session=session)
        return {
            "message": "Category deleted",
        }
    except Exception as err:
        return {
            "message": "Error when deleting category",
            "Error": err,
        }
