from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.products.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
    ProductSchema,
)
from core.models import Product
from core.services.dependencies import get_all_records, create_record, update_record


async def get_products(session: AsyncSession) -> List[Product]:
    return await get_all_records(session, Product)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    return await create_record(session, Product, product_in.model_dump())


async def update_product(
    session: AsyncSession,
    product_in: ProductSchema,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> ProductSchema:
    return await update_record(
        session, product_in, product_update.model_dump(exclude_unset=partial), partial
    )


async def delete_product(session: AsyncSession, product: ProductSchema) -> None:
    await session.delete(product)
    await session.commit()
