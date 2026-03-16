from fastapi import APIRouter, Depends, Query

from app.controllers.activity_log import ActivityLogController
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.responses.activity_logs import ActivityLogResponse
from core.factory import Factory

activity_log_router = APIRouter()


@activity_log_router.get(
    "/projects/{project_uuid}/activity",
    response_model=PaginatedResponse[ActivityLogResponse],
)
async def get_project_activity(
    project_uuid: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    activity_log_controller: ActivityLogController = Depends(
        Factory().get_activity_log_controller
    ),
) -> PaginatedResponse[ActivityLogResponse]:
    items = await activity_log_controller.get_for_project_paginated(
        project_uuid, limit=limit, offset=offset
    )
    total = await activity_log_controller.count_for_project(project_uuid)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)
