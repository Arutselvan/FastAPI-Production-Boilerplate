from fastapi import APIRouter, Depends, Query

from app.controllers import CategoryController
from app.schemas.extras.pagination import PaginatedResponse
from app.schemas.requests.categories import CategoryCreate
from app.schemas.responses.categories import CategoryResponse
from core.factory import Factory

category_router = APIRouter()


@category_router.get("/", response_model=PaginatedResponse[CategoryResponse])
async def get_categories(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    category_controller: CategoryController = Depends(Factory().get_category_controller),
) -> PaginatedResponse[CategoryResponse]:
    if search is not None:
        items = await category_controller.search_by_name(search, limit=limit, offset=offset)
        total = await category_controller.count_search_by_name(search)
    else:
        items = await category_controller.get_paginated(limit=limit, offset=offset)
        total = await category_controller.count()
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


@category_router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_create: CategoryCreate,
    category_controller: CategoryController = Depends(Factory().get_category_controller),
) -> CategoryResponse:
    return await category_controller.add(
        name=category_create.name,
        description=category_create.description,
    )


@category_router.get("/{category_uuid}", response_model=CategoryResponse)
async def get_category(
    category_uuid: str,
    category_controller: CategoryController = Depends(Factory().get_category_controller),
) -> CategoryResponse:
    return await category_controller.get_by_uuid(category_uuid)
