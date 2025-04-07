from typing import List, Optional

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api_v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models.image import Image
from core.models.product import Product, ProductSize
from core.services.shared.dependencies import delete_record


# Получить все продукты с изображениями и размерами
async def get_products(session: AsyncSession) -> List[Product]:
    stmt = select(Product).options(selectinload(Product.images), selectinload(Product.sizes))
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


# Получить продукт по ID с изображениями и размерами
async def get_product_by_id(session: AsyncSession, product_id: int) -> Optional[Product]:
    result = await session.execute(
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.sizes))
        .filter(Product.id == product_id)
    )
    return result.scalars().first()


# Создать продукт с изображениями и размерами
async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(
        name=product_in.name,
        price=product_in.price,
        category_id=product_in.category_id,
        description=product_in.description,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    # Добавить изображения
    if product_in.images:
        images = [
            Image(url=img.url, is_primary=img.is_primary, product_id=product.id)
            for img in product_in.images
        ]
        session.add_all(images)
        await session.commit()

    # Добавить размеры
    if product_in.sizes:
        sizes = [ProductSize(size=size, product_id=product.id) for size in product_in.sizes]
        session.add_all(sizes)
        await session.commit()

    # Вернуть продукт с загрузкой связей
    result = await session.execute(
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.sizes))
        .filter(Product.id == product.id)
    )
    return result.scalars().first()


# Обновить продукт и его размеры
async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False,
) -> Product:
    for field, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, field, value)

    # Обновить размеры, если переданы
    if product_update.sizes is not None:
        await session.execute(
            ProductSize.__table__.delete().where(ProductSize.product_id == product.id)
        )
        new_sizes = [ProductSize(size=size, product_id=product.id) for size in product_update.sizes]
        session.add_all(new_sizes)

    await session.commit()
    await session.refresh(product)
    return product


# Удалить продукт
async def delete_product(session: AsyncSession, product: Product):
    await delete_record(record=product, session=session)
