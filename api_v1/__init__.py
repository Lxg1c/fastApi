from fastapi import APIRouter

from .cart.views import router as cart_router
from .category.views import router as category_router
from .favorite.views import router as favorite_router
from .products.views import router as product_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(product_router)
router.include_router(category_router)
router.include_router(users_router)
router.include_router(cart_router)
router.include_router(favorite_router)
