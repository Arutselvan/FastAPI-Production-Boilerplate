from typing import Optional

from pydantic import BaseModel, constr


class AttachmentCreate(BaseModel):
    filename: constr(min_length=1, max_length=255)
    file_url: constr(min_length=1, max_length=1000)
    file_size: Optional[int] = None
    comment_uuid: str
