from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class TagResponse(BaseModel):
    id: int = Field(..., description="Tag ID")
    uuid: UUID4 = Field(
        ..., description="Tag UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    name: str = Field(..., description="Tag name", example="Urgent")
    color: str | None = Field(
        None, description="Tag color", example="#FF5733"
    )
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
