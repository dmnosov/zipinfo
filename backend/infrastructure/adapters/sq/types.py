from pydantic import BaseModel


class IssueStats(BaseModel):
    total: int
    critical: int
    major: int
    minor: int


class SonarqubeModel(BaseModel):
    overall_coverage: float
    bugs: IssueStats
    code_smells: IssueStats
    vulnerabilities: IssueStats
