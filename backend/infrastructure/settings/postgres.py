from pydantic import BaseModel


class Postgres(BaseModel):
    host: str
    port: int
    db_name: str
    username: str
    password: str
