from pydantic import BaseModel, Field

class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    AccessToken: str
    IdToken: str
    RefreshToken: str
    ExpiresIn: int
    TokenType: str

class AuthErrorResponse(BaseModel):
    detail: str