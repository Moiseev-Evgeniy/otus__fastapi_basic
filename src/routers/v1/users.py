from fastapi import APIRouter, Depends, Request

from dto.schemas.currency_prediction import PredictionResponse, SignsDTO
from dto.schemas.users import UserCreate, Tokens
from services.currency_prediction import CurrencyPredictionService
from services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/registration",
    response_model=Tokens,
    summary="User registration",
    response_description="Tokens"
)
async def get_currency_prediction(request: Request, user: UserCreate):
    return await UserService.register_user(user, request.headers["user-agent"])
