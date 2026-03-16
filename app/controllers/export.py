import csv
import io

from app.repositories import CommentRepository, MilestoneRepository, ProjectRepository, TagRepository
from app.repositories.team import TeamRepository


class ExportController:
    """Controller for generating CSV export summaries."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        milestone_repository: MilestoneRepository,
        comment_repository: CommentRepository,
        tag_repository: TagRepository,
        team_repository: TeamRepository,
    ):
        self.project_repository = project_repository
        self.milestone_repository = milestone_repository
        self.comment_repository = comment_repository
        self.tag_repository = tag_repository
        self.team_repository = team_repository

    async def export_team_summary(self, team_id: int) -> str:
        """Generate CSV summary of a team's projects.

        Columns: team_name, project_name, project_status, milestone_count, comment_count
        """
        team = await self.team_repository.get_by_id(team_id)
        projects = await self.project_repository.get_by_team_id(team_id)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["team_name", "project_name", "project_status", "milestone_count", "comment_count"])

        for project in projects:
            milestones = await self.milestone_repository.get_by_project_id(project.id)
            comments = await self.comment_repository.get_by_project_id(project.id)
            writer.writerow([
                team.name,
                project.name,
                project.status,
                len(milestones),
                len(comments),
            ])

        return output.getvalue()

    async def export_projects_summary(self, owner_id: int) -> str:
        """Generate CSV summary of a user's projects.

        Columns: project_name, status, tag_names, created_at
        """
        projects = await self.project_repository.get_by_owner_id_paginated(
            owner_id, limit=10000, offset=0,
        )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["project_name", "status", "tag_names", "created_at"])

        for project in projects:
            tags = await self.project_repository.get_tags(project.id)
            tag_names = ";".join(tag.name for tag in tags)
            writer.writerow([
                project.name,
                project.status,
                tag_names,
                project.created_at.isoformat() if project.created_at else "",
            ])

        return output.getvalue()
