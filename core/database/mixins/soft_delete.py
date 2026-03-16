# pylint: skip-file

from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


class SoftDeleteMixin:
    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True, default=None)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
