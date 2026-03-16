from app.models import Project, Tag
from app.repositories import MilestoneRepository, ProjectRepository, TagRepository, TeamRepository
from app.repositories.activity_log import ActivityLogRepository
from core.controller import BaseController
from core.database.transactional import Propagation, Transactional
from app.models.project import ProjectStatus
from core.exceptions import BadRequestException, NotFoundException


class ProjectController(BaseController[Project]):
    """Project controller."""

    keyword_tag_map: dict[str, str] = {
        "urgent": "urgent",
        "bug": "bug",
        "feature": "feature-request",
    }

    def __init__(
        self,
        project_repository: ProjectRepository,
        milestone_repository: MilestoneRepository | None = None,
        team_repository: TeamRepository | None = None,
        tag_repository: TagRepository | None = None,
        activity_log_repository: ActivityLogRepository | None = None,
    ):
        super().__init__(model=Project, repository=project_repository)
        self.project_repository = project_repository
        self.milestone_repository = milestone_repository
        self.team_repository = team_repository
        self.tag_repository = tag_repository
        self.activity_log_repository = activity_log_repository

    async def get_by_team_id(self, team_id: int) -> list[Project]:
        """
        Returns a list of projects based on team_id.

        :param team_id: The team id.
        :return: A list of projects.
        """

        return await self.project_repository.get_by_team_id(team_id)

    async def get_by_owner_id(self, owner_id: int) -> list[Project]:
        """
        Returns a list of projects based on owner_id.

        :param owner_id: The owner id.
        :return: A list of projects.
        """

        return await self.project_repository.get_by_owner_id(owner_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, name: str, description: str, owner_id: int) -> Project:
        """
        Adds a project.

        :param name: The project name.
        :param description: The project description.
        :param owner_id: The owner id.
        :return: The project.
        """

        project = await self.project_repository.create(
            {
                "name": name,
                "description": description,
                "owner_id": owner_id,
            }
        )
        await self.auto_tag(project.id)
        return project

    async def auto_tag(self, project_id: int) -> None:
        """Automatically assign tags to a project based on keyword matches in name/description."""
        project = await self.project_repository.get_by_id(project_id)
        text = f"{project.name} {project.description or ''}".lower()

        for keyword, tag_name in self.keyword_tag_map.items():
            if keyword in text:
                tag = await self.tag_repository.get_by_name(tag_name)
                if not tag:
                    tag = await self.tag_repository.create({"name": tag_name})
                await self.project_repository.assign_tag(project_id, tag.id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def assign_tag(self, project_uuid: str, tag_uuid: str, actor_id: int | None = None) -> None:
        """Assign a tag to a project."""
        project = await self.get_by_uuid(project_uuid)
        tag = await self.project_repository.get_tag_by_uuid(tag_uuid)
        if not tag:
            raise NotFoundException(f"Tag with uuid: {tag_uuid} does not exist")
        await self.project_repository.assign_tag(project.id, tag.id)
        if actor_id and self.activity_log_repository:
            await self.activity_log_repository.create_log(
                project_id=project.id,
                actor_id=actor_id,
                action="tag_assigned",
                details=f"Tag {tag_uuid} assigned",
            )

    @Transactional(propagation=Propagation.REQUIRED)
    async def remove_tag(self, project_uuid: str, tag_uuid: str) -> None:
        """Remove a tag from a project."""
        project = await self.get_by_uuid(project_uuid)
        tag = await self.project_repository.get_tag_by_uuid(tag_uuid)
        if not tag:
            raise NotFoundException(f"Tag with uuid: {tag_uuid} does not exist")
        await self.project_repository.remove_tag(project.id, tag.id)

    async def get_tags(self, project_uuid: str) -> list[Tag]:
        """Get all tags for a project."""
        project = await self.get_by_uuid(project_uuid)
        return await self.project_repository.get_tags(project.id)

    _ALLOWED_TRANSITIONS = {
        ProjectStatus.DRAFT: {ProjectStatus.ACTIVE},
        ProjectStatus.ACTIVE: {ProjectStatus.ARCHIVED},
        ProjectStatus.ARCHIVED: set(),
    }

    @Transactional(propagation=Propagation.REQUIRED)
    async def transition_status(self, project_uuid: str, new_status: str, actor_id: int | None = None) -> Project:
        """Transition a project's status with validation."""
        project = await self.get_by_uuid(project_uuid)
        current = ProjectStatus(project.status)
        try:
            target = ProjectStatus(new_status)
        except ValueError:
            raise BadRequestException(f"Invalid status: {new_status}")

        if target not in self._ALLOWED_TRANSITIONS.get(current, set()):
            raise BadRequestException(
                f"Transition from {current.value} to {target.value} is not allowed"
            )

        updated = await self.project_repository.update_status(project.id, target.value)
        if actor_id and self.activity_log_repository:
            await self.activity_log_repository.create_log(
                project_id=project.id,
                actor_id=actor_id,
                action="status_changed",
                details=f"{current.value} -> {target.value}",
            )
        return updated

    @Transactional(propagation=Propagation.REQUIRED)
    async def bulk_archive_team_projects(self, team_uuid: str, actor_id: int | None = None) -> dict:
        """Bulk-archive all projects for a team and complete their milestones."""
        team = await self.team_repository.get_by("uuid", team_uuid, unique=True)
        projects = await self.project_repository.get_by_team_id(team.id)
        project_ids = [p.id for p in projects]

        archived_count = await self.project_repository.bulk_archive_by_team_id(team.id)
        completed_count = await self.milestone_repository.bulk_complete_by_project_ids(
            project_ids
        )

        if actor_id and self.activity_log_repository:
            for project in projects:
                await self.activity_log_repository.create_log(
                    project_id=project.id,
                    actor_id=actor_id,
                    action="archived",
                    details=f"Bulk archived via team {team_uuid}",
                )

        return {
            "archived_projects": archived_count,
            "completed_milestones": completed_count,
        }
