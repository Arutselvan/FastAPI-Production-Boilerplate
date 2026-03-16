from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class TeamResponse(BaseModel):
    id: int = Field(..., description="Team ID")
    uuid: UUID4 = Field(
        ..., description="Team UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    name: str = Field(..., description="Team name", example="My Team")
    description: str | None = Field(
        None, description="Team description", example="A sample team"
    )
    owner_id: int = Field(..., description="Owner ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
