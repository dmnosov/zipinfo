from pydantic import BaseModel

from application.entities.report import Status
from infrastructure.adapters.sq.types import SonarqubeModel


class GetResultByIdResponse(BaseModel):
    status: Status

    class Result(BaseModel):
        sonarqube: SonarqubeModel

    results: Result | None = None
