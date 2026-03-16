from fastapi import APIRouter, Depends

from app.controllers import TagController
from app.schemas.requests.tags import TagCreate
from app.schemas.responses.tags import TagResponse
from core.factory import Factory

tag_router = APIRouter()


@tag_router.get("/", response_model=list[TagResponse])
async def get_tags(
    tag_controller: TagController = Depends(Factory().get_tag_controller),
) -> list[TagResponse]:
    return await tag_controller.get_all()


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
