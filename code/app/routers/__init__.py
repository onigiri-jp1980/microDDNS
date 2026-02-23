from fastapi import APIRouter, Request,Depends
from app.controllers import get_buckets, show_envs
from app.services.request import RequestService
from app.routers.auth import auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)

@api_router.get("/envs")
def root():
    return show_envs()

@api_router.get("/buckets")
def get_buckets():
    return get_buckets()

@api_router.get("/dump")
def dump(request: Request = Depends(RequestService)):
    return {"aws.event": request.aws_event, 
     "aws.context": request.aws_context}