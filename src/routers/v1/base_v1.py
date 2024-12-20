from fastapi import APIRouter

from routers.v1.currency_prediction import router as currency_prediction_router
from routers.v1.content import router as content_router
from routers.v1.users import router as user_router


router = APIRouter(prefix="/api/v1")

router.include_router(currency_prediction_router)
router.include_router(user_router)
router.include_router(content_router)
