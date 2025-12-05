from datetime import datetime
from pydantic import BaseModel

class TokenData(BaseModel):
    token: str
    expires: datetime

class AuthTokens(BaseModel):
    access: TokenData
    refresh: TokenData

class TokenPayload(BaseModel):
    sub: str | None = None
    type: str | None = None