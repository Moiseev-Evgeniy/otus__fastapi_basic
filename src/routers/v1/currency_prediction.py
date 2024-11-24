from fastapi import APIRouter, Depends

from src.dto.schemas.currency_prediction import PredictionResponse, SignsDTO
from src.services.currency_prediction import CurrencyPredictionService

router = APIRouter(prefix="/currency_prediction", tags=["Currency prediction"])


@router.get(
    "/",
    response_model=PredictionResponse,
    summary="Get currency prediction",
    response_description="Currency prediction"
)
async def get_currency_prediction(signs: SignsDTO = Depends()):
    return await CurrencyPredictionService.get_prediction(signs)
