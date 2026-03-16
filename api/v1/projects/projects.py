from datetime import date
from typing import Callable

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import Response

from app.controllers import CommentController, ExportController, MilestoneController, ProjectController, TaskController
from app.models.project import ProjectPermission
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.requests.projects import ProjectCreate, ProjectStatusUpdate
from app.schemas.responses.comments import CommentResponse
from app.schemas.responses.milestones import MilestoneResponse
from app.schemas.responses.projects import ProjectResponse
from app.schemas.responses.tags import TagResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

project_router = APIRouter()


@project_router.get("/", response_model=PaginatedResponse[ProjectResponse])
async def get_projects(
    request: Request,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    created_after: date | None = Query(None),
    created_before: date | None = Query(None),
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> PaginatedResponse[ProjectResponse]:
    if search is not None:
        items = await project_controller.search_by_name_and_owner_id(
            search, request.user.id, limit=limit, offset=offset,
            created_after=created_after, created_before=created_before,
        )
        total = await project_controller.count_search_by_name_and_owner_id(
            search, request.user.id,
            created_after=created_after, created_before=created_before,
        )
    elif created_after is not None or created_before is not None:
        items = await project_controller.get_by_owner_id_paginated_filtered(
            request.user.id, limit=limit, offset=offset,
            created_after=created_after, created_before=created_before,
        )
        total = await project_controller.count_by_owner_id_filtered(
            request.user.id,
            created_after=created_after, created_before=created_before,
        )
    else:
        items = await project_controller.get_by_owner_id_paginated(
            request.user.id, limit=limit, offset=offset
        )
        total = await project_controller.count_by_owner_id(request.user.id)

    assert_access(items)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


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


@project_router.get("/export.csv")
async def export_projects_csv(
    request: Request,
    export_controller: ExportController = Depends(Factory().get_export_controller),
) -> Response:
    csv_content = await export_controller.export_projects_summary(request.user.id)
    return Response(content=csv_content, media_type="text/csv")


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


@project_router.patch("/{project_uuid}/status", response_model=ProjectResponse)
async def update_project_status(
    project_uuid: str,
    body: ProjectStatusUpdate,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.EDIT)),
) -> ProjectResponse:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    return await project_controller.transition_status(project_uuid, body.status, actor_id=request.user.id)


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


@project_router.get("/{project_uuid}/milestones", response_model=list[MilestoneResponse])
async def get_project_milestones(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    milestone_controller: MilestoneController = Depends(Factory().get_milestone_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> list[MilestoneResponse]:
    project = await project_controller.get_by_uuid(project_uuid)

    assert_access(project)
    milestones = await milestone_controller.get_by_project_id(project.id)
    return milestones


@project_router.post("/{project_uuid}/tags/{tag_uuid}", status_code=201)
async def assign_tag_to_project(
    request: Request,
    project_uuid: str,
    tag_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.EDIT)),
) -> None:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    await project_controller.assign_tag(project_uuid, tag_uuid, actor_id=request.user.id)


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


@project_router.post("/{project_uuid}/recalculate-priority", status_code=200)
async def recalculate_priority(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    task_controller: TaskController = Depends(Factory().get_task_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.EDIT)),
) -> None:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    await task_controller.recalculate_priority(project_uuid)


@project_router.get("/{project_uuid}/tags", response_model=list[TagResponse])
async def get_project_tags(
    project_uuid: str,
    project_controller: ProjectController = Depends(Factory().get_project_controller),
    assert_access: Callable = Depends(Permissions(ProjectPermission.READ)),
) -> list[TagResponse]:
    project = await project_controller.get_by_uuid(project_uuid)
    assert_access(project)
    return await project_controller.get_tags(project_uuid)
