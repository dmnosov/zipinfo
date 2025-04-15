from enum import StrEnum
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.entities.upload import Upload
from infrastructure.database import BaseEntity


class Status(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Report(BaseEntity):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    upload_id: Mapped[UUID | None] = mapped_column(ForeignKey("uploads.id"))

    status: Mapped[Status]
    data: Mapped[str | None]

    upload: Mapped["Upload | None"] = relationship(
        foreign_keys=[upload_id],
        lazy="joined",
    )
