from fastapi import APIRouter

from .activity_logs import activity_logs_router
from .approvals import approvals_router
from .attachments import attachments_router
from .comments import comments_router
from .categories import categories_router
from .milestones import milestones_router
from .monitoring import monitoring_router
from .projects import projects_router
from .tags import tags_router
from .tasks import tasks_router
from .teams import teams_router
from .users import users_router
from .user_roles import user_roles_router

v1_router = APIRouter()
v1_router.include_router(activity_logs_router)
v1_router.include_router(approvals_router)
v1_router.include_router(attachments_router, prefix="/attachments")
v1_router.include_router(comments_router, prefix="/comments")
v1_router.include_router(categories_router, prefix="/categories")
v1_router.include_router(milestones_router, prefix="/milestones")
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(projects_router, prefix="/projects")
v1_router.include_router(tags_router, prefix="/tags")
v1_router.include_router(tasks_router, prefix="/tasks")
v1_router.include_router(teams_router, prefix="/teams")
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(user_roles_router)
