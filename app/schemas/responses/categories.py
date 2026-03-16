from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class CategoryResponse(BaseModel):
    id: int = Field(..., description="Category ID")
    uuid: UUID4 = Field(
        ..., description="Category UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    name: str = Field(..., description="Category name", example="Technology")
    description: str | None = Field(
        None, description="Category description", example="Technology related items"
    )
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
