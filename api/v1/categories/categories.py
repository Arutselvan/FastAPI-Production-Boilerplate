from fastapi import APIRouter, Depends

from app.controllers import CategoryController
from app.schemas.requests.categories import CategoryCreate
from app.schemas.responses.categories import CategoryResponse
from core.factory import Factory

category_router = APIRouter()


@category_router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    category_controller: CategoryController = Depends(Factory().get_category_controller),
) -> list[CategoryResponse]:
    return await category_controller.get_all()


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
