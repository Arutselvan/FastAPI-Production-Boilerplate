from fastapi import APIRouter, Depends

from pydantic import BaseModel

from app.controllers.import_controller import ImportController
from core.factory import Factory

import_router = APIRouter()


class ImportRequest(BaseModel):
    items: list[dict]


class ImportResponse(BaseModel):
    created: int
    skipped: int
    errors: list[str]


@import_router.post("/tags", response_model=ImportResponse, status_code=200)
async def import_tags(
    request: ImportRequest,
    import_controller: ImportController = Depends(Factory().get_import_controller),
) -> ImportResponse:
    result = await import_controller.import_tags(request.items)
    return ImportResponse(**result)


@import_router.post("/categories", response_model=ImportResponse, status_code=200)
async def import_categories(
    request: ImportRequest,
    import_controller: ImportController = Depends(Factory().get_import_controller),
) -> ImportResponse:
    result = await import_controller.import_categories(request.items)
    return ImportResponse(**result)
