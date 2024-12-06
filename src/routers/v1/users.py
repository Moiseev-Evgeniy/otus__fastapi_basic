from fastapi import APIRouter, Depends, Request, Response, status

from db.tables import User
from dto.schemas.users import UserCreate, UserAuth, UserBase, RefreshToken
from services.user import UserService
from utils.role_checker import allowed_for_admin_subscriber_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/registration",
    response_model=RefreshToken,
    summary="User registration",
    response_description="Tokens in cookie and in body",
    status_code=status.HTTP_201_CREATED,
)
async def user_register(request: Request, response: Response, user: UserCreate):
    return await UserService.register(user, request.headers["user-agent"], response)


@router.post(
    "/login",
    response_model=RefreshToken,
    summary="User login",
    response_description="Tokens in cookie and in body",
)
async def user_login(request: Request, response: Response, user: UserAuth):
    return await UserService.login(user, request.headers["user-agent"], response)


@router.post(
    "/logout",
    summary="User logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def user_logout(request: Request, response: Response, user: User = Depends(allowed_for_admin_subscriber_user)):
    await UserService.logout(user, request.headers["user-agent"], response)


@router.post(
    "/refresh",
    # response_model=RefreshToken,
    summary="Refresh tokens",
    response_description="Tokens in cookie and in body",
)
async def refresh_tokens(request: Request, response: Response, refresh_token: RefreshToken):
    return await UserService.refresh(refresh_token, request.headers["user-agent"], response)


@router.get(
    "/me",
    response_model=UserBase,
    summary="Get current user data",
    response_description="User data",
)
async def get_user_data(user: User = Depends(allowed_for_admin_subscriber_user)):
    return user
