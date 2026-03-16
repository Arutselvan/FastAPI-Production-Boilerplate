from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.security.access_control import (
    Allow,
    Authenticated,
    RolePrincipal,
    UserPrincipal,
)


class UserRoleEnum(Enum):
    MEMBER = "member"
    TEAM_LEAD = "team_lead"
    VIEWER = "viewer"


class UserRolePermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    role = Column(
        SAEnum("member", "team_lead", "viewer", name="user_role_enum"),
        nullable=False,
    )
    assigned_at = Column(DateTime, default=func.now(), nullable=False)

    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    team_id = Column(
        BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", backref="user_roles", uselist=False, lazy="raise")
    team = relationship("Team", backref="user_roles", uselist=False, lazy="raise")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [UserRolePermission.CREATE]
        self_permissions = [
            UserRolePermission.READ,
            UserRolePermission.EDIT,
            UserRolePermission.DELETE,
        ]
        all_permissions = list(UserRolePermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.user_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
