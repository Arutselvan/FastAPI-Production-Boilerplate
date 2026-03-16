from typing import Callable

from fastapi import APIRouter, Depends, Request

from app.controllers import AttachmentController, CommentController, ProjectController
from app.models.comment import CommentPermission
from app.schemas.requests.comments import CommentCreate
from app.schemas.responses.attachments import AttachmentResponse
from app.schemas.responses.comments import CommentResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

comment_router = APIRouter()


@comment_router.get("/", response_model=list[CommentResponse])
async def get_comments(
    request: Request,
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
    assert_access: Callable = Depends(Permissions(CommentPermission.READ)),
) -> list[CommentResponse]:
    comments = await comment_controller.get_by_author_id(request.user.id)

    assert_access(comments)
    return comments


@comment_router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(
    request: Request,
    comment_create: CommentCreate,
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
    project_controller: ProjectController = Depends(Factory().get_project_controller),
) -> CommentResponse:
    project = await project_controller.get_by_uuid(comment_create.project_uuid)
    comment = await comment_controller.add(
        body=comment_create.body,
        author_id=request.user.id,
        project_id=project.id,
    )
    return comment


@comment_router.get("/{comment_uuid}", response_model=CommentResponse)
async def get_comment(
    comment_uuid: str,
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
    assert_access: Callable = Depends(Permissions(CommentPermission.READ)),
) -> CommentResponse:
    comment = await comment_controller.get_by_uuid(comment_uuid)

    assert_access(comment)
    return comment


@comment_router.get("/{comment_uuid}/attachments", response_model=list[AttachmentResponse])
async def get_comment_attachments(
    comment_uuid: str,
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
    attachment_controller: AttachmentController = Depends(Factory().get_attachment_controller),
    assert_access: Callable = Depends(Permissions(CommentPermission.READ)),
) -> list[AttachmentResponse]:
    comment = await comment_controller.get_by_uuid(comment_uuid)

    assert_access(comment)
    attachments = await attachment_controller.get_by_comment_id(comment.id)
    return attachments


@comment_router.delete("/{comment_uuid}", status_code=204)
async def delete_comment(
    comment_uuid: str,
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
    assert_access: Callable = Depends(Permissions(CommentPermission.DELETE)),
) -> None:
    comment = await comment_controller.get_by_uuid(comment_uuid)

    assert_access(comment)
    await comment_controller.delete(comment)
