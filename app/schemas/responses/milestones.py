from datetime import date, datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class MilestoneResponse(BaseModel):
    id: int = Field(..., description="Milestone ID")
    uuid: UUID4 = Field(
        ..., description="Milestone UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    title: str = Field(..., description="Milestone title", example="v1.0 Release")
    due_date: Optional[date] = Field(None, description="Due date")
    project_id: int = Field(..., description="Project ID")
    is_completed: bool = Field(..., description="Milestone completed status")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
