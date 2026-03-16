from typing import Optional

from pydantic import BaseModel, constr


class ApprovalCreate(BaseModel):
    milestone_uuid: str
    decision: constr(regex="^(approved|rejected)$")
    notes: Optional[constr(max_length=1000)] = None
