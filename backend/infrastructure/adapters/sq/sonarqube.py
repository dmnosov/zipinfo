from httpx import AsyncClient

from infrastructure.adapters.sq.types import SonarqubeModel
from infrastructure.settings import settings


class SonarqubeAdapter:
    @staticmethod
    async def scan() -> SonarqubeModel:
        async with AsyncClient() as client:
            resp = await client.get(f"{settings.sq.server}/scan")
            return SonarqubeModel.model_validate(resp.json())
