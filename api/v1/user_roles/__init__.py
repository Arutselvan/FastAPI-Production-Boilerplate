from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .user_roles import user_role_router

user_roles_router = APIRouter()
user_roles_router.include_router(
    user_role_router,
    tags=["User Roles"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["user_roles_router"]
