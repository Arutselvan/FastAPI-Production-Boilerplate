from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, ForeignKey, Table, Unicode
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

project_tags = Table(
    "project_tags",
    Base.metadata,
    Column("project_id", BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", BigInteger, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class ProjectPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(1000), nullable=True)

    owner_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    team_id = Column(
        BigInteger, ForeignKey("teams.id", ondelete="SET NULL"), nullable=True
    )
    owner = relationship("User", back_populates="projects", uselist=False, lazy="raise")
    team = relationship("Team", backref="projects", uselist=False, lazy="raise")
    comments = relationship(
        "Comment", back_populates="project", lazy="raise", passive_deletes=True
    )
    tags = relationship("Tag", secondary=project_tags, lazy="raise")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [ProjectPermission.CREATE]
        self_permissions = [
            ProjectPermission.READ,
            ProjectPermission.EDIT,
            ProjectPermission.DELETE,
        ]
        all_permissions = list(ProjectPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.owner_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
