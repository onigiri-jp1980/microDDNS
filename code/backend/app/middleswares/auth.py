from fastapi import Request, HTTPException, Depends
from app.services.auth import CognitoService
from app.services.request import RequestService
from app.models import ApiKeys

def JwtAuthMiddleware(request: Request = Depends(RequestService)):
    """Authorization: Bearer トークンを検証し、Cognito のユーザー情報を返す依存関係。"""
    headers = request.aws_event.get("headers") or {}
    auth = headers.get("authorization") or headers.get("Authorization") or ""
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    access_token = auth[7:].strip()
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    cognito = CognitoService()
    return cognito.get_user(access_token)

def ApiKeyAuthMiddleware(request: Request = Depends(RequestService)):
    """x-api-key を検証し、一致した ApiKeys を返す依存関係。ルーターで Depends(ApiKeyAuthMiddleware) として利用する。"""
    headers = request.aws_event.get("headers") or {}
    api_key_header = headers.get("x-api-key")
    if not api_key_header:
        raise HTTPException(status_code=401, detail="Unauthorized")
    verified = next(ApiKeys().get_by_secret(api_key_header), None)
    if verified is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return verified