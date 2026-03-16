from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ActivityLogResponse(BaseModel):
    id: int = Field(..., description="Activity log ID")
    uuid: UUID4 = Field(
        ..., description="Activity log UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    project_id: int = Field(..., description="Project ID")
    actor_id: int = Field(..., description="Actor user ID")
    action: str = Field(..., description="Action performed", example="status_changed")
    details: Optional[str] = Field(None, description="Additional details")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
