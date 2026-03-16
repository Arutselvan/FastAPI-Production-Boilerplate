from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ApprovalResponse(BaseModel):
    id: int = Field(..., description="Approval ID")
    uuid: UUID4 = Field(
        ..., description="Approval UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    milestone_id: int = Field(..., description="Milestone ID")
    approved_by: int = Field(..., description="Approver user ID")
    decision: str = Field(..., description="Approval decision", example="approved")
    notes: Optional[str] = Field(None, description="Approval notes")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
