from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from sqlalchemy.orm import selectinload
from api_v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models.product import Product, ProductSize
from core.models.image import Image


async def get_products(session: AsyncSession) -> List[Product]:
    """Получить список всех продуктов с изображениями и размерами."""
    stmt = select(Product).options(selectinload(Product.images), selectinload(Product.sizes))
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Optional[Product]:
    """Получить продукт по ID с изображениями и размерами."""
    result = await session.execute(
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.sizes))
        .filter(Product.id == product_id)
    )
    return result.scalars().first()


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    """Создать новый продукт с изображениями и размерами."""
    product = Product(
        name=product_in.name,
        price=product_in.price,
        category_id=product_in.category_id,
        description=product_in.description,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    # Добавляем изображения
    if product_in.images:
        images = [
            Image(url=img.url, is_primary=img.is_primary, product_id=product.id)
            for img in product_in.images
        ]
        session.add_all(images)
        await session.commit()

    # Добавляем размеры
    if product_in.sizes:
        sizes = [ProductSize(size=size, product_id=product.id) for size in product_in.sizes]
        session.add_all(sizes)
        await session.commit()

    # Загружаем связанные данные
    result = await session.execute(
        select(Product)
        .options(selectinload(Product.images), selectinload(Product.sizes))
        .filter(Product.id == product.id)
    )
    return result.scalars().first()


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    """Обновить продукт (полностью или частично), включая размеры."""
    for field, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, field, value)

    # Обновляем размеры, если они переданы
    if product_update.sizes is not None:
        # Удаляем старые размеры
        await session.execute(
            ProductSize.__table__.delete().where(ProductSize.product_id == product.id)
        )
        # Добавляем новые
        new_sizes = [ProductSize(size=size, product_id=product.id) for size in product_update.sizes]
        session.add_all(new_sizes)

    await session.commit()
    await session.refresh(product)
    return product



async def delete_product(session: AsyncSession, product: Product):
    """Удалить продукт (автоматически удалятся все связанные фото)."""
    await session.delete(product)
    await session.commit()
