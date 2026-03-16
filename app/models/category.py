from uuid import uuid4

from sqlalchemy import BigInteger, Column, Unicode
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base
from core.database.mixins import TimestampMixin


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    name = Column(Unicode(255), nullable=False, unique=True)
    description = Column(Unicode(1000), nullable=True)

    __mapper_args__ = {"eager_defaults": True}
