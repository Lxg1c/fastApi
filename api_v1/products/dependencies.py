from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from api_v1.products import crud
from core.models import Product
from core.models.db_helper import db_helper


async def get_product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
