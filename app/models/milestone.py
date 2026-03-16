from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Unicode
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


class MilestonePermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Milestone(Base, TimestampMixin):
    __tablename__ = "milestones"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    title = Column(Unicode(255), nullable=False)
    due_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)

    project_id = Column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    project = relationship("Project", back_populates="milestones", uselist=False, lazy="raise")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [MilestonePermission.CREATE]
        self_permissions = [
            MilestonePermission.READ,
            MilestonePermission.EDIT,
            MilestonePermission.DELETE,
        ]
        all_permissions = list(MilestonePermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
