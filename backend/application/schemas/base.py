from pydantic import BaseModel


class Message(BaseModel):
    error: str
