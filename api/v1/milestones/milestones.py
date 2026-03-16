from typing import Callable

from fastapi import APIRouter, Depends, Query, Request

from app.controllers import MilestoneController, ProjectController
from app.models.milestone import MilestonePermission
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.requests.milestones import MilestoneCreate
from app.schemas.responses.milestones import MilestoneResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

milestone_router = APIRouter()


@milestone_router.get("/", response_model=PaginatedResponse[MilestoneResponse])
async def get_milestones(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
) -> PaginatedResponse[MilestoneResponse]:
    items = await milestone_controller.get_paginated(limit=limit, offset=offset)
    total = await milestone_controller.count()
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


@milestone_router.post("/", response_model=MilestoneResponse, status_code=201)
async def create_milestone(
    request: Request,
    milestone_create: MilestoneCreate,
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
    project_controller: ProjectController = Depends(Factory().get_project_controller),
) -> MilestoneResponse:
    project = await project_controller.get_by_uuid(milestone_create.project_uuid)
    milestone = await milestone_controller.add(
        title=milestone_create.title,
        due_date=milestone_create.due_date,
        project_id=project.id,
    )
    return milestone


@milestone_router.get("/{milestone_uuid}", response_model=MilestoneResponse)
async def get_milestone(
    milestone_uuid: str,
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
    assert_access: Callable = Depends(Permissions(MilestonePermission.READ)),
) -> MilestoneResponse:
    milestone = await milestone_controller.get_by_uuid(milestone_uuid)

    assert_access(milestone)
    return milestone


@milestone_router.patch("/{milestone_uuid}/complete", response_model=MilestoneResponse)
async def complete_milestone(
    milestone_uuid: str,
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
    assert_access: Callable = Depends(Permissions(MilestonePermission.EDIT)),
) -> MilestoneResponse:
    milestone = await milestone_controller.get_by_uuid(milestone_uuid)

    assert_access(milestone)
    completed = await milestone_controller.complete(milestone.id)
    return completed
