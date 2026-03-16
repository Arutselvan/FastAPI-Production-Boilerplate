from fastapi import APIRouter, Depends

from app.controllers.activity_log import ActivityLogController
from app.schemas.responses.activity_logs import ActivityLogResponse
from core.factory import Factory

activity_log_router = APIRouter()


@activity_log_router.get(
    "/projects/{project_uuid}/activity",
    response_model=list[ActivityLogResponse],
)
async def get_project_activity(
    project_uuid: str,
    activity_log_controller: ActivityLogController = Depends(
        Factory().get_activity_log_controller
    ),
) -> list[ActivityLogResponse]:
    return await activity_log_controller.get_for_project(project_uuid)
