from fastapi import APIRouter

from routers.v1.currency_prediction import router as currency_prediction_router


router = APIRouter(prefix="/api/v1")

router.include_router(currency_prediction_router)
