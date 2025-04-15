from uuid import UUID

from pydantic import BaseModel, Field


class UploadZipResponse(BaseModel):
    task_id: UUID = Field(description="ID задачи для отслеживания результатов")
