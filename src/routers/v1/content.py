from fastapi import APIRouter, Depends

from db.tables import User
from utils.role_checker import allowed_for_admin, allowed_for_admin_subscriber

router = APIRouter(prefix="/content", tags=["Content"])


@router.get(
    "/admin_content",
    summary="Get admin content",
    response_description="Admin content",
)
async def get_user_data(user: User = Depends(allowed_for_admin)):
    return {"content": "Admin content"}


@router.get(
    "/subscriber_content",
    summary="Get subscriber content",
    response_description="Subscriber content",
)
async def get_user_data(user: User = Depends(allowed_for_admin_subscriber)):
    return {"content": "Subscriber content"}