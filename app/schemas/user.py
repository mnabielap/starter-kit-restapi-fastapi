from pydantic import BaseModel, EmailStr, Field

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None
    role: str = "user"
    is_active: bool = True
    is_email_verified: bool = False

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Password must be at least 8 characters")

    # In strict FastAPI/Pydantic, we usually validate password complexity here if needed,
    # but min_length is often enough for the schema.

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    password: str | None = None
    role: str | None = None
    is_email_verified: bool | None = None

# Properties to return to client (Response)
class UserResponse(UserBase):
    id: int
    
    # Config to allow Pydantic to read data from SQLAlchemy models
    model_config = {
        "from_attributes": True
    }