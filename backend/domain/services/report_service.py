from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound

from application.entities.report import Report, Status
from domain.models.report import Report as DomainReport
from infrastructure.adapters.sq.types import SonarqubeModel
from infrastructure.database import async_session_maker


class ReportService:
    @staticmethod
    async def create(id: UUID) -> UUID:
        async with async_session_maker() as session:
            stmt = insert(Report).values(id=id, status=Status.PENDING).returning(Report.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    @staticmethod
    async def update_upload(id: UUID, upload_id: UUID) -> None:
        async with async_session_maker() as session:
            stmt = (
                update(Report)
                .where(Report.id == id)
                .values(
                    upload_id=upload_id,
                    status=Status.IN_PROGRESS,
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_status(id: UUID, new_status: Status) -> None:
        async with async_session_maker() as session:
            stmt = (
                update(Report)
                .where(Report.id == id)
                .values(
                    status=new_status,
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_data(id: UUID, model: SonarqubeModel) -> None:
        async with async_session_maker() as session:
            stmt = (
                update(Report)
                .where(Report.id == id)
                .values(
                    status=Status.SUCCESS,
                    data=model.model_dump_json(),
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def find(id: UUID) -> DomainReport | None:
        async with async_session_maker() as session:
            try:
                res = await session.execute(select(Report).filter_by(id=id))
                report = res.scalar_one()
                return DomainReport(
                    id=report.id,
                    status=report.status,
                    data=SonarqubeModel.model_validate_json(report.data) if report.data is not None else None,
                )
            except NoResultFound:
                return None
