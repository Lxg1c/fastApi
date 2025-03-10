from fastapi import APIRouter
from .products.views import router as product_router
from .users.views import router as auth_router

router = APIRouter()
router.include_router(product_router)
router.include_router(auth_router)
