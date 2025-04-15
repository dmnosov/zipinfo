from uuid import UUID

from pydantic import BaseModel

from application.entities.report import Status
from infrastructure.adapters.sq.types import SonarqubeModel


class Report(BaseModel):
    id: UUID
    status: Status
    data: SonarqubeModel | None = None
