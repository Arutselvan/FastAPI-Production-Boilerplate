from pydantic import BaseModel, constr


class TagCreate(BaseModel):
    name: constr(min_length=1, max_length=255)
    color: constr(min_length=1, max_length=7) | None = None
