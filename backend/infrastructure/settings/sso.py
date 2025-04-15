from pydantic import BaseModel


class SSO(BaseModel):
    server: str
    client_id: str
