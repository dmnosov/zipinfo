from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import BaseEntity


class Upload(BaseEntity):
    __tablename__ = "uploads"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    filename: Mapped[str]
    user_id: Mapped[UUID]
