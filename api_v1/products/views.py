# views.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models.db_helper import db_helper
from . import crud
from .dependencies import get_product_by_id

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_products(session=session)


@router.post("/", response_model=Product)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product: Product = Depends(get_product_by_id),
):
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_update: ProductUpdate,
    product_in: Product = Depends(get_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_product(
        product_in=product_in,
        session=session,
        product_update=product_update,
        partial=False,  # Полное обновление
    )


@router.patch("/{product_id}", response_model=Product)
async def update_product_partial(
    product_update: ProductUpdatePartial,  # Для частичных обновлений используем ProductUpdatePartial
    product_in: Product = Depends(get_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_product(
        product_in=product_in,
        session=session,
        product_update=product_update,
        partial=True,  # Частичное обновление
    )


from fastapi import HTTPException, status


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
