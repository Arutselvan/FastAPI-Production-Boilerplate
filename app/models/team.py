from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, ForeignKey, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin
from core.security.access_control import (
    Allow,
    Authenticated,
    RolePrincipal,
    UserPrincipal,
)


class TeamPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Team(Base, TimestampMixin):
    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    name = Column(Unicode(255), nullable=False, unique=True)
    description = Column(Unicode(1000), nullable=True)

    owner_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("User", back_populates="teams", uselist=False, lazy="raise")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [TeamPermission.CREATE]
        self_permissions = [
            TeamPermission.READ,
            TeamPermission.EDIT,
            TeamPermission.DELETE,
        ]
        all_permissions = list(TeamPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.owner_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
