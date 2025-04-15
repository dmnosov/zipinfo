from io import BytesIO

from infrastructure.database import s3


class ArchiveService:
    @staticmethod
    async def save_archive(file: bytes, filename: str) -> None:
        async with s3.client() as client:
            buffer = BytesIO(file)
            await client.put_object(
                Bucket="files",
                Key=filename,
                Body=buffer,
                ContentType="application/zip",
            )

    @staticmethod
    async def find_archive() -> bytes:
        return bytes()
