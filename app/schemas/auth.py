from pydantic import BaseModel
from app.schemas.user import UserResponse
from app.schemas.token import AuthTokens

class AuthResponse(BaseModel):
    user: UserResponse
    tokens: AuthTokens