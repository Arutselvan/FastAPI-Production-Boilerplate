from typing import Callable

from fastapi import APIRouter, Depends, Request

from app.controllers import AttachmentController, CommentController
from app.models.attachment import AttachmentPermission
from app.schemas.requests.attachments import AttachmentCreate
from app.schemas.responses.attachments import AttachmentResponse
from core.factory import Factory
from core.fastapi.dependencies.permissions import Permissions

attachment_router = APIRouter()


@attachment_router.post("/", response_model=AttachmentResponse, status_code=201)
async def create_attachment(
    request: Request,
    attachment_create: AttachmentCreate,
    attachment_controller: AttachmentController = Depends(Factory().get_attachment_controller),
    comment_controller: CommentController = Depends(Factory().get_comment_controller),
) -> AttachmentResponse:
    comment = await comment_controller.get_by_uuid(attachment_create.comment_uuid)
    attachment = await attachment_controller.add(
        filename=attachment_create.filename,
        file_url=attachment_create.file_url,
        file_size=attachment_create.file_size,
        comment_id=comment.id,
        uploaded_by=request.user.id,
    )
    return attachment


@attachment_router.delete("/{attachment_uuid}", status_code=204)
async def delete_attachment(
    attachment_uuid: str,
    attachment_controller: AttachmentController = Depends(Factory().get_attachment_controller),
    assert_access: Callable = Depends(Permissions(AttachmentPermission.DELETE)),
) -> None:
    attachment = await attachment_controller.get_by_uuid(attachment_uuid)

    assert_access(attachment)
    await attachment_controller.delete(attachment)
