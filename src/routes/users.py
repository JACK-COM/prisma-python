# from typing import List
from fastapi import APIRouter, Depends

# internal
from src.utils.auth import JWTBearer, decodeJWT
from src.models import SafeUser

router = APIRouter()


@router.get("/users/", tags=["users"])
async def list_users():
    users = await SafeUser.prisma().find_many()
    print("users", users)

    return users


@router.get("/users/me", tags=["users"])
async def get_authenticated_user(token=Depends(JWTBearer())):
    decoded = decodeJWT(token)

    if "userId" in decoded:
        userId = decoded["userId"]
        return await SafeUser.prisma().find_unique(where={"id": userId})
    return None


@router.get("/users/{userId}", tags=["users"])
async def get_user(userId: str):
    user = await SafeUser.prisma().find_unique(where={"id": userId})

    return user
