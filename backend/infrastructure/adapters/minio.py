from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiobotocore.session import get_session
from types_aiobotocore_s3 import S3Client


class MinioAdapter:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        ssl: bool = False,
        port: int | None = None,
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = (
            f"{'https://' if ssl else 'http://'}{endpoint_url}:{port}" if port is not None else endpoint_url
        )
        self.use_ssl = ssl
        self.session = get_session()

    @asynccontextmanager
    async def client(self) -> AsyncGenerator[S3Client, None]:
        async with self.session.create_client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
        ) as client:
            yield client
