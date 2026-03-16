from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class CommentResponse(BaseModel):
    id: int = Field(..., description="Comment ID")
    uuid: UUID4 = Field(
        ..., description="Comment UUID", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
    )
    body: str = Field(..., description="Comment body", example="This is a comment")
    author_id: int = Field(..., description="Author ID")
    project_id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        orm_mode = True
