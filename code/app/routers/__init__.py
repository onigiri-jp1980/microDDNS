from fastapi import APIRouter, Request
from app.controllers import get_buckets, show_envs

api_router = APIRouter(prefix="/api")

@api_router.get("/envs")
def root():
    return show_envs()

@api_router.get("/buckets")
def get_buckets():
    return get_buckets()

@api_router.get("/dump")
def dump(request: Request):
    return {"aws.event": request.scope.get('aws.event'), 
     "aws.context": request.scope.get('aws.context')}