from pydantic import BaseModel


class ObjectStorage(BaseModel):
    host: str
    port: int | None = None

    access_key_id: str
    secret_access_key: str

    files_bucketname: str | None = None  # bucket for storage uploaded files
