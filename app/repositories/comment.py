from datetime import datetime

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Comment
from core.repository import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    """Comment repository provides all the database operations for the Comment model."""

    def _query(
        self,
        join_: set[str] | None = None,
        order_: dict | None = None,
    ) -> Select:
        query = super()._query(join_, order_)
        query = query.where(Comment.deleted_at.is_(None))
        return query

    async def get_by_project_id(
        self, project_id: int, join_: set[str] | None = None
    ) -> list[Comment]:
        """Get all comments by project id."""
        query = self._query(join_)
        query = self._get_by(query, "project_id", project_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def get_by_author_id(
        self, author_id: int, join_: set[str] | None = None
    ) -> list[Comment]:
        """Get all comments by author id."""
        query = self._query(join_)
        query = self._get_by(query, "author_id", author_id)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._all(query)

    async def soft_delete(self, id: int) -> None:
        """Soft delete a comment by setting deleted_at."""
        comments = await self.get_by(field="id", value=id, unique=True)
        if comments:
            comments.deleted_at = datetime.utcnow()

    def _join_author(self, query: Select) -> Select:
        """Join the author relationship."""
        return query.options(joinedload(Comment.author))

    def _join_project(self, query: Select) -> Select:
        """Join the project relationship."""
        return query.options(joinedload(Comment.project))
