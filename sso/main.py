import uvicorn
from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import ConnectionPool
from redis import Redis as RedisClient


class Keycloak(BaseModel):
    server_url: str
    realm_name: str

    username: str
    password: str


class Redis(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    keycloak: Keycloak
    redis: Redis


settings = Settings()  # type: ignore


class KeycloakAdapter:
    def __init__(
        self,
        redis: RedisClient,
        server_url: str,
        realm_name: str,
        username: str,
        password: str,
    ):
        self.redis = redis

        self.server_url = server_url
        self.realm_name = realm_name
        self.username = username
        self.password = password

        self._client_id = None

    @property
    def client_id(self) -> str | None:
        return self.client_id

    @client_id.setter
    def client_id(self, value: str | None) -> None:
        self.client_id = value

    async def create_user(self, username: str, password: str, email: str) -> dict:
        token = await self.get_admin_token()
        url = f"{self.server_url}admin/realms/{self.realm_name}/users"

        user_data = {
            "username": username,
            "email": email,
            "emailVerified": True,
            "enabled": True,
            "credentials": [
                {
                    "type": "password",
                    "value": password,
                    "temporary": False,
                },
            ],
            "requiredActions": [],
            "firstName": "Default",
            "lastName": "Default",
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        async with AsyncClient() as client:
            response = await client.post(url, json=user_data, headers=headers)
            if response.status_code == 409:
                return {"status": "conflict", "message": "User already exist"}
            response.raise_for_status()
            return {"status": "created", "username": username}

    async def get_admin_token(self) -> str:
        kc_token = self.redis.get("kc_token")
        if kc_token is not None:
            return str(kc_token)

        async with AsyncClient() as client:
            response = await client.post(
                f"{self.server_url}realms/master/protocol/openid-connect/token",
                data={
                    "grant_type": "password",
                    "client_id": "admin-cli",
                    "username": self.username,
                    "password": self.password,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            token = response.json()
            self.redis.set("kc_token", token["access_token"], ex=60)  # admin token expire after 5 min
            return token["access_token"]

    async def get_token(
        self,
        username: str,
        password: str,
        client_id: str,
    ) -> dict:
        url = f"{self.server_url}realms/{self.realm_name}/protocol/openid-connect/token"

        data = {
            "grant_type": "password",
            "client_id": client_id,
            "username": username,
            "password": password,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_certs(self) -> dict:
        url = f"{self.server_url}realms/{self.realm_name}/protocol/openid-connect/certs"

        async with AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


redis = RedisClient(
    connection_pool=ConnectionPool(
        host=settings.redis.host,
        port=settings.redis.port,
        username=settings.redis.username,
        password=settings.redis.password,
        db=settings.redis.db,
        decode_responses=True,
    )
)

kc = KeycloakAdapter(
    redis=redis,
    server_url=settings.keycloak.server_url,
    realm_name=settings.keycloak.realm_name,
    username=settings.keycloak.username,
    password=settings.keycloak.password,
)


app = FastAPI(title="SSO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GetTokenRequest(BaseModel):
    username: str
    password: str
    client_id: str


class CreateUserRequest(BaseModel):
    username: str
    password: str


@app.post("/user/create")
async def create_user(request: CreateUserRequest):
    response = await kc.create_user(
        request.username,
        request.password,
        "default@zipinfo.com",
    )
    if response["status"] == "created":
        return Response(status_code=201)
    elif response["status"] == "conflict":
        return JSONResponse(content=response, status_code=409)


@app.post("/auth/token")
async def get_token(request: GetTokenRequest):
    response = await kc.get_token(
        request.username,
        request.password,
        request.client_id,
    )
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=200,
    )


# public certs for jwt decode
@app.get("/auth/certs")
async def get_certs():
    response = await kc.get_certs()
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
