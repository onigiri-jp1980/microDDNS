from os import listdir,path
from fastapi import APIRouter, Request,Depends
from app.controllers import show_envs
from app.services.request import RequestService
from app.middleswares.auth import JwtAuthMiddleware, ApiKeyAuthMiddleware
from importlib import import_module as import_module_func


api_router = APIRouter(prefix="/api")

# ルーターを動的にインポート
for module in listdir(path.dirname(__file__)):
    if module.endswith('.py') and module != '__init__.py':
        module_name = module[:-3]
        router = import_module_func(f'app.routers.{module_name}').router
        api_router.include_router(router)

# チェック用:環境変数を取得
@api_router.get("/envs", dependencies=[Depends(ApiKeyAuthMiddleware)])
def root():
    return show_envs()

# チェック用:AWS EventとContextを返す
@api_router.get("/dump", dependencies=[Depends(JwtAuthMiddleware)])
def dump(request: Request = Depends(RequestService)):
    return {"aws.event": request.aws_event, 
     "aws.context": request.aws_context}