from fastapi import APIRouter
from app.services.auth import CognitoService
from app.models.auth import AuthRequest, AuthResponse
auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login")
def sign_in(request: AuthRequest)->AuthResponse:
    return CognitoService(email=request.email).sign_in(request.email, request.password)