from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AuthenticationRequired

from .activity_logs import activity_log_router

activity_logs_router = APIRouter()
activity_logs_router.include_router(
    activity_log_router,
    tags=["Activity Logs"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["activity_logs_router"]
