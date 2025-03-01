from fastapi import APIRouter
from . import crud

router = APIRouter(tags=["Products"])


@router.get("/")
async def get_products(session):
    return await crud.get_products(session=session)


@router.get("/{product_id}")
async def get_product(session, product_id):
    return await crud.get_product_by_id(session=session, id=product_id)
