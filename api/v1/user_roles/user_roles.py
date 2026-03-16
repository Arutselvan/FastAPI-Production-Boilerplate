from fastapi import APIRouter, Depends, Query, Request

from app.controllers.team import TeamController
from app.controllers.user import UserController
from app.controllers.user_role import UserRoleController
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.requests.user_roles import UserRoleCreate
from app.schemas.responses.user_roles import UserRoleResponse
from core.factory import Factory

user_role_router = APIRouter()


@user_role_router.post(
    "/teams/{team_uuid}/roles",
    response_model=UserRoleResponse,
    status_code=201,
)
async def assign_role(
    request: Request,
    team_uuid: str,
    role_create: UserRoleCreate,
    user_role_controller: UserRoleController = Depends(Factory().get_user_role_controller),
    team_controller: TeamController = Depends(Factory().get_team_controller),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserRoleResponse:
    team = await team_controller.get_by_uuid(team_uuid)
    user = await user_controller.get_by_uuid(role_create.user_uuid)
    user_role = await user_role_controller.assign_role(
        user_id=user.id,
        team_id=team.id,
        role=role_create.role,
    )
    return user_role


@user_role_router.get(
    "/teams/{team_uuid}/roles",
    response_model=PaginatedResponse[UserRoleResponse],
)
async def get_roles(
    team_uuid: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_role_controller: UserRoleController = Depends(Factory().get_user_role_controller),
    team_controller: TeamController = Depends(Factory().get_team_controller),
) -> PaginatedResponse[UserRoleResponse]:
    team = await team_controller.get_by_uuid(team_uuid)
    items = await user_role_controller.get_by_team_id_paginated(
        team.id, limit=limit, offset=offset
    )
    total = await user_role_controller.count_by_team_id(team.id)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)
