from core.database.transactional import Propagation, Transactional
from app.repositories import TagRepository, CategoryRepository


class ImportController:
    """Controller for bulk-importing Tags and Categories from JSON payloads."""

    def __init__(
        self,
        tag_repository: TagRepository,
        category_repository: CategoryRepository,
    ):
        self.tag_repository = tag_repository
        self.category_repository = category_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def import_tags(self, data: list[dict]) -> dict:
        """Bulk create tags, skipping duplicates.

        Args:
            data: List of dicts with "name" and optional "color" keys.

        Returns:
            {"created": N, "skipped": N, "errors": [...]}
        """
        created = 0
        skipped = 0
        errors: list[str] = []

        for index, item in enumerate(data):
            name = item.get("name")
            if not name or not isinstance(name, str) or not name.strip():
                errors.append(f"Item {index}: missing or invalid 'name' field")
                continue

            name = name.strip()
            color = item.get("color")
            if color is not None and not isinstance(color, str):
                errors.append(f"Item {index}: invalid 'color' field")
                continue

            existing = await self.tag_repository.get_by_name(name)
            if existing:
                skipped += 1
                continue

            await self.tag_repository.create({"name": name, "color": color})
            created += 1

        return {"created": created, "skipped": skipped, "errors": errors}

    @Transactional(propagation=Propagation.REQUIRED)
    async def import_categories(self, data: list[dict]) -> dict:
        """Bulk create categories, skipping duplicates.

        Args:
            data: List of dicts with "name" and optional "description" keys.

        Returns:
            {"created": N, "skipped": N, "errors": [...]}
        """
        created = 0
        skipped = 0
        errors: list[str] = []

        for index, item in enumerate(data):
            name = item.get("name")
            if not name or not isinstance(name, str) or not name.strip():
                errors.append(f"Item {index}: missing or invalid 'name' field")
                continue

            name = name.strip()
            description = item.get("description")
            if description is not None and not isinstance(description, str):
                errors.append(f"Item {index}: invalid 'description' field")
                continue

            existing = await self.category_repository.get_by_name(name)
            if existing:
                skipped += 1
                continue

            await self.category_repository.create({"name": name, "description": description})
            created += 1

        return {"created": created, "skipped": skipped, "errors": errors}
