# views.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial, ProductSchema
from core.models.db_helper import db_helper
from . import crud
from .dependencies import get_product_by_id
from fastapi import status

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.post("/", response_model=ProductSchema)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product: ProductSchema = Depends(get_product_by_id),
):
    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_update: ProductUpdate,
    product_in: ProductSchema = Depends(get_product),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        product_in=product_in,
        session=session,
        product_update=product_update,
        partial=False,  # Полное обновление
    )


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product_in: ProductSchema = Depends(get_product),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        product_in=product_in,
        session=session,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: ProductSchema = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
