from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class UserRoleResponse(BaseModel):
    id: int = Field(..., description="UserRole ID")
    uuid: UUID4 = Field(
        ..., description="UserRole UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    user_id: int = Field(..., description="User ID")
    team_id: int = Field(..., description="Team ID")
    role: str = Field(..., description="Role", example="member")
    assigned_at: datetime = Field(..., description="Assignment timestamp")

    class Config:
        orm_mode = True
