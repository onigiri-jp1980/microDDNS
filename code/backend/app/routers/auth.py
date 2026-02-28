from fastapi import APIRouter, Depends
from app.models.auth import AuthRequest, AuthResponse, AuthErrorResponse
from app.controllers.auth import sign_in, verify_token

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login",
  response_model=AuthResponse,
  status_code=200,
  description="ログイン",
  responses={
    401: {
      "description": "Authentication failed",
      "model": AuthErrorResponse,
    },
    404: {
      "description": "User not Found",
      "model": AuthErrorResponse,
    },
  },
  tags=["auth"])
def login(result: AuthResponse = Depends(sign_in)) -> AuthResponse:
    return result

@auth_router.get("/verify",
  response_model=AuthResponse,
  status_code=200,
  description="トークン検証",
  responses={
    401: {
      "description": "Authentication failed",
      "model": AuthErrorResponse,
    },
  },
  tags=["auth"])
