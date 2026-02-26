from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    accessToken: str
    idToken: str
    refreshToken: str
    expiresIn: int
