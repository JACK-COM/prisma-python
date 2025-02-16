"""
This is a root for all API sub-routes. Export all subrouters from here.
"""
from fastapi import APIRouter

from .auth import router as authRouter
from .users import router as usersRouter

routes = APIRouter()
routes.include_router(authRouter)
routes.include_router(usersRouter)

__all__ = ["routes"]
