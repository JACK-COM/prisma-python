from fastapi import APIRouter

from .auth import router as authRouter
from .users import router as usersRouter

apis = APIRouter()
apis.include_router(authRouter)
apis.include_router(usersRouter)

__all__ = ["apis"]
