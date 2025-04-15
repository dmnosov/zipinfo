from uuid import UUID, uuid4

from sqlalchemy import insert

from application.entities import Upload
from infrastructure.database import async_session_maker


class UploadService:
    @staticmethod
    async def create(filename: str, user_id: UUID) -> UUID:
        async with async_session_maker() as session:
            stmt = (
                insert(Upload)
                .values(
                    id=uuid4(),
                    filename=filename,
                    user_id=user_id,
                )
                .returning(Upload.id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
