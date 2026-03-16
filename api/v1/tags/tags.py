from fastapi import APIRouter, Depends, Query

from app.controllers import AttachmentController, TagController
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.requests.tags import TagCreate
from app.schemas.responses.attachments import AttachmentResponse
from app.schemas.responses.tags import TagResponse
from core.factory import Factory

tag_router = APIRouter()


@tag_router.get("/", response_model=PaginatedResponse[TagResponse])
async def get_tags(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    tag_controller: TagController = Depends(Factory().get_tag_controller),
) -> PaginatedResponse[TagResponse]:
    if search is not None:
        items = await tag_controller.search_by_name(search, limit=limit, offset=offset)
        total = await tag_controller.count_search_by_name(search)
    else:
        items = await tag_controller.get_paginated(limit=limit, offset=offset)
        total = await tag_controller.count()
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


@tag_router.post("/", response_model=TagResponse, status_code=201)
async def create_tag(
    tag_create: TagCreate,
    tag_controller: TagController = Depends(Factory().get_tag_controller),
) -> TagResponse:
    return await tag_controller.add(
        name=tag_create.name,
        color=tag_create.color,
    )


@tag_router.get("/{tag_uuid}", response_model=TagResponse)
async def get_tag(
    tag_uuid: str,
    tag_controller: TagController = Depends(Factory().get_tag_controller),
) -> TagResponse:
    return await tag_controller.get_by_uuid(tag_uuid)


@tag_router.delete("/{tag_uuid}", status_code=204)
async def delete_tag(
    tag_uuid: str,
    tag_controller: TagController = Depends(Factory().get_tag_controller),
) -> None:
    tag = await tag_controller.get_by_uuid(tag_uuid)
    await tag_controller.delete(tag)


@tag_router.get("/{tag_uuid}/attachments", response_model=list[AttachmentResponse])
async def get_tag_attachments(
    tag_uuid: str,
    attachment_controller: AttachmentController = Depends(Factory().get_attachment_controller),
) -> list[AttachmentResponse]:
    return await attachment_controller.get_by_tag_uuid(tag_uuid)
