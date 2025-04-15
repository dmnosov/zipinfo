from httpx import AsyncClient

from infrastructure.settings import settings


class SSOAdapter:
    def __init__(self, server: str, client_id: str):
        self._server = server
        self.client_id = client_id

    @property
    def server(self) -> str:
        return self._server

    @server.setter
    def server(self, value: str) -> None:
        self._server = value

    async def token(self, username: str, password: str) -> dict | None:
        async with AsyncClient() as client:
            r = await client.post(
                f"{self.server}/auth/token",
                json={
                    "client_id": self.client_id,
                    "username": username,
                    "password": password,
                },
            )
            r.raise_for_status()
            return r.json()

    async def create_user(self, username: str, password: str) -> dict | None:
        async with AsyncClient() as client:
            r = await client.post(
                f"{self.server}/user/create",
                json={
                    "username": username,
                    "password": password,
                },
            )
            return r.json()


sso_adapter = SSOAdapter(settings.sso.server, settings.sso.client_id)
