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


class CommentPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    body = Column(Unicode(2000), nullable=False)

    author_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User", back_populates="comments", uselist=False, lazy="raise")

    project_id = Column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    project = relationship("Project", back_populates="comments", uselist=False, lazy="raise")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [CommentPermission.CREATE]
        self_permissions = [
            CommentPermission.READ,
            CommentPermission.EDIT,
            CommentPermission.DELETE,
        ]
        all_permissions = list(CommentPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.author_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
