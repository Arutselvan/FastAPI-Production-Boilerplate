from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class ProjectResponse(BaseModel):
    id: int = Field(..., description="Project ID")
    uuid: UUID4 = Field(
        ..., description="Project UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    name: str = Field(..., description="Project name", example="My Project")
    description: str | None = Field(
        None, description="Project description", example="A sample project"
    )
    owner_id: int = Field(..., description="Owner ID")
    status: str = Field(..., description="Project status")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
