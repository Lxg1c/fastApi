from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from . import crud
from .schemas import ProductSchema, ProductCreate, ProductUpdate, ProductUpdatePartial

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/", response_model=ProductSchema)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=False
    )


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product_partial(
    product_id: int,
    product_update: ProductUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    await crud.delete_product(session=session, product=product)
