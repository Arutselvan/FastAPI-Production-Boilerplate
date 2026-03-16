from pydantic import BaseModel, constr


class UserRoleCreate(BaseModel):
    user_uuid: str
    team_uuid: str
    role: constr(regex="^(member|team_lead|viewer)$")
