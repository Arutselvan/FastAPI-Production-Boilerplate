from pydantic import BaseModel, constr


class CategoryCreate(BaseModel):
    name: constr(min_length=1, max_length=255)
    description: constr(min_length=1, max_length=1000) | None = None
