from typing import Callable

from fastapi import APIRouter, Depends, Request

from app.controllers import ProjectController
from app.models.project import ProjectPermission
from app.schemas.requests.projects import ProjectCreate
from app.schemas.responses.projects import ProjectResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

project_router = APIRouter()


@project_router.get("/", response_model=list[ProjectResponse])
async def get_projects(
    request: Request,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> list[ProjectResponse]:
    projects = await project_controller.get_by_owner_id(request.user.id)

    assert_access(projects)
    return projects


@project_router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    request: Request,
    project_create: ProjectCreate,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
) -> ProjectResponse:
    project = await project_controller.add(
        name=project_create.name,
        description=project_create.description,
        owner_id=request.user.id,
    )
    return project


@project_router.get("/{project_uuid}", response_model=ProjectResponse)
async def get_project(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> ProjectResponse:
    project = await project_controller.get_by_uuid(project_uuid)

    assert_access(project)
    return project


@project_router.delete("/{project_uuid}", status_code=204)
async def delete_project(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.DELETE)),
) -> None:
    project = await project_controller.get_by_uuid(project_uuid)

    assert_access(project)
    await project_controller.delete(project)
