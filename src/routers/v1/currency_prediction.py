from fastapi import APIRouter, Depends

from db.tables import User
from dto.schemas.currency_prediction import PredictionResponse, SignsDTO
from services.currency_prediction import CurrencyPredictionService
from utils.role_checker import allowed_for_admin_subscriber

router = APIRouter(prefix="/currency_prediction", tags=["Currency prediction"])


@router.get(
    "/",
    response_model=PredictionResponse,
    summary="Get currency prediction",
    response_description="Currency prediction"
)
async def get_currency_prediction(user: User = Depends(allowed_for_admin_subscriber), signs: SignsDTO = Depends()):
    return await CurrencyPredictionService.get_prediction(signs)
