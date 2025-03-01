"""
Create
Read
Update
Delete
"""

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreate
from core.models import Product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product: ProductCreate) -> Product:
    product = Product(**product.model_dump())
    session.add(product)
    await session.commit()
    return product
