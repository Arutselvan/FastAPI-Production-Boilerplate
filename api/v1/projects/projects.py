from typing import Callable

from fastapi import APIRouter, Depends, Request

from app.controllers import CommentController, ProjectController
from app.models.project import ProjectPermission
from app.schemas.requests.projects import ProjectCreate
from app.schemas.responses.comments import CommentResponse
from app.schemas.responses.projects import ProjectResponse
from app.schemas.responses.tags import TagResponse
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


@project_router.get("/{project_uuid}/comments", response_model=list[CommentResponse])
async def get_project_comments(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> list[CommentResponse]:
    project = await project_controller.get_by_uuid(project_uuid)

    assert_access(project)
    comments = await comment_controller.get_by_project_id(project.id)
    return comments


@project_router.post("/{project_uuid}/tags/{tag_uuid}", status_code=201)
async def assign_tag_to_project(
    project_uuid: str,
    tag_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.EDIT)),
) -> None:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    await project_controller.assign_tag(project_uuid, tag_uuid)


@project_router.delete("/{project_uuid}/tags/{tag_uuid}", status_code=204)
async def remove_tag_from_project(
    project_uuid: str,
    tag_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.EDIT)),
) -> None:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    await project_controller.remove_tag(project_uuid, tag_uuid)


@project_router.get("/{project_uuid}/tags", response_model=list[TagResponse])
async def get_project_tags(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> list[TagResponse]:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    return await project_controller.get_tags(project_uuid)
