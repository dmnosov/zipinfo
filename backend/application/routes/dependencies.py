from uuid import UUID

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from infrastructure.adapters import sso_adapter


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request):  # type:ignore
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403)
            try:
                jwk_client = jwt.PyJWKClient(f"{sso_adapter.server}/auth/certs")
                payload = jwt.decode(
                    credentials.credentials,
                    jwk_client.get_signing_key_from_jwt(credentials.credentials),
                    algorithms="RS256",
                    options={"verify_exp": False},
                )
                return UUID(payload["sub"])
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=403)
        else:
            raise HTTPException(status_code=403)
