from typing import Callable

from fastapi import APIRouter, Depends, Request

from app.controllers import TeamController
from app.models.team import TeamPermission
from app.schemas.requests.teams import TeamCreate
from app.schemas.responses.teams import TeamResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

team_router = APIRouter()


@team_router.get("/", response_model=list[TeamResponse])
async def get_teams(
    request: Request,
    team_controller: TeamController = Depends(Factory().get_team_controller),
    assert_access: Callable = Depends(Permissions(TeamPermission.READ)),
) -> list[TeamResponse]:
    teams = await team_controller.get_by_owner_id(request.user.id)

    assert_access(teams)
    return teams


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


@team_router.delete("/{team_uuid}", status_code=204)
async def delete_team(
    team_uuid: str,
    team_controller: TeamController = Depends(Factory().get_team_controller),
    assert_access: Callable = Depends(Permissions(TeamPermission.DELETE)),
) -> None:
    team = await team_controller.get_by_uuid(team_uuid)

    assert_access(team)
    await team_controller.delete(team)
