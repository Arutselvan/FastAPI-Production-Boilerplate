from datetime import date
from typing import Optional

from pydantic import BaseModel, constr


class MilestoneCreate(BaseModel):
    title: constr(min_length=1, max_length=255)
    due_date: Optional[date] = None
    project_uuid: str
