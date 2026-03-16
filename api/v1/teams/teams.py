from typing import Callable

from fastapi import APIRouter, Depends, Query, Request

from app.controllers import MilestoneController, ProjectController, TeamController
from app.models.milestone import MilestonePermission
from app.models.project import ProjectPermission
from app.models.team import TeamPermission
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.requests.teams import TeamCreate
from app.schemas.responses.milestones import MilestoneResponse
from app.schemas.responses.projects import ProjectResponse
from app.schemas.responses.teams import TeamResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

team_router = APIRouter()


@team_router.get("/", response_model=PaginatedResponse[TeamResponse])
async def get_teams(
    request: Request,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    team_controller: TeamController = Depends(Factory().get_team_controller),
    assert_access: Callable = Depends(Permissions(TeamPermission.READ)),
) -> PaginatedResponse[TeamResponse]:
    items = await team_controller.get_by_owner_id_paginated(
        request.user.id, limit=limit, offset=offset
    )
    total = await team_controller.count_by_owner_id(request.user.id)

    assert_access(items)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


@team_router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(
    request: Request,
    team_create: TeamCreate,
    team_controller: TeamController = Depends(Factory().get_team_controller),
) -> TeamResponse:
    team = await team_controller.add(
        name=team_create.name,
        description=team_create.description,
        owner_id=request.user.id,
    )
    return team


@team_router.get("/{team_uuid}", response_model=TeamResponse)
async def get_team(
    team_uuid: str,
    team_controller: TeamController = Depends(Factory().get_team_controller),
    assert_access: Callable = Depends(Permissions(TeamPermission.READ)),
) -> TeamResponse:
    team = await team_controller.get_by_uuid(team_uuid)

    assert_access(team)
    return team


@team_router.get("/{team_uuid}/projects", response_model=list[ProjectResponse])
async def get_team_projects(
    team_uuid: str,
    team_controller: TeamController = Depends(Factory().get_team_controller),
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> list[ProjectResponse]:
    team = await team_controller.get_by_uuid(team_uuid)
    projects = await project_controller.get_by_team_id(team.id)

    assert_access(projects)
    return projects


@team_router.get("/{team_uuid}/milestones", response_model=list[MilestoneResponse])
async def get_team_milestones(
    team_uuid: str,
    team_controller: TeamController = Depends(Factory().get_team_controller),
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
    assert_access: Callable = Depends(Permissions(MilestonePermission.READ)),
) -> list[MilestoneResponse]:
    team = await team_controller.get_by_uuid(team_uuid)
    milestones = await milestone_controller.get_by_team_id(team.id)

    assert_access(milestones)
    return milestones


@team_router.post("/{team_uuid}/archive-projects")
async def archive_team_projects(
    request: Request,
    team_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
) -> dict:
    return await project_controller.bulk_archive_team_projects(team_uuid, actor_id=request.user.id)


@team_router.delete("/{team_uuid}", status_code=204)
async def delete_team(
    team_uuid: str,
    team_controller: TeamController = Depends(Factory().get_team_controller),
    assert_access: Callable = Depends(Permissions(TeamPermission.DELETE)),
) -> None:
    team = await team_controller.get_by_uuid(team_uuid)

    assert_access(team)
    await team_controller.delete(team)
