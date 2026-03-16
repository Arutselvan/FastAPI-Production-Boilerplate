from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class AttachmentResponse(BaseModel):
    id: int = Field(..., description="Attachment ID")
    uuid: UUID4 = Field(
        ..., description="Attachment UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    filename: str = Field(..., description="Filename")
    file_url: str = Field(..., description="File URL")
    file_size: int | None = Field(None, description="File size in bytes")
    comment_id: int = Field(..., description="Comment ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
