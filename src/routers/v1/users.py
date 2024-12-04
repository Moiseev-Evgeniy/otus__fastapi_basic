from fastapi import APIRouter, Depends, Request, Response, status

from dto.schemas.currency_prediction import PredictionResponse, SignsDTO
from dto.schemas.users import UserCreate, Tokens, UserAuth
from services.currency_prediction import CurrencyPredictionService
from services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/registration",
    summary="User registration",
    response_description="Tokens in cookie",
    status_code=status.HTTP_201_CREATED,
)
async def user_register(request: Request, response: Response, user: UserCreate):
    await UserService.register(user, request.headers["user-agent"], response)


@router.post(
    "/login",
    summary="User login",
    response_description="Tokens in cookie"
)
async def user_login(request: Request, response: Response, user: UserAuth):
    await UserService.login(user, request.headers["user-agent"], response)

