from pydantic import BaseModel, constr


class CommentCreate(BaseModel):
    body: constr(min_length=1, max_length=2000)
    project_uuid: str
