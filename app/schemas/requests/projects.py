from typing import Optional

from pydantic import BaseModel, constr


class ProjectCreate(BaseModel):
    name: constr(min_length=1, max_length=255)
    description: Optional[constr(max_length=1000)] = None
