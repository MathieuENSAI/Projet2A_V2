from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError

from .init_app import jwt_service

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False, partial_access_allowed=False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.partial_access_allowed = partial_access_allowed

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)
        
        if self.partial_access_allowed:
            try:
                jwt_service.validate_user_jwt(credentials.credentials)
            except Exception :
                return {"restricted_access": True}
        else :
            if not credentials:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")

            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            try:
                jwt_service.validate_user_jwt(credentials.credentials)
            except ExpiredSignatureError as e:
                raise HTTPException(status_code=403, detail="Expired token") from e
            except DecodeError as e:
                raise HTTPException(status_code=403, detail="Error decoding token") from e
            except Exception as e:
                raise HTTPException(status_code=403, detail="Unknown error") from e

        return credentials
