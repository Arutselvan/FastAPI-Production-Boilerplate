from fastapi import APIRouter

from .categories import categories_router
from .monitoring import monitoring_router
from .tags import tags_router
from .tasks import tasks_router
from .users import users_router

v1_router = APIRouter()
v1_router.include_router(categories_router, prefix="/categories")
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(tags_router, prefix="/tags")
v1_router.include_router(tasks_router, prefix="/tasks")
v1_router.include_router(users_router, prefix="/users")
