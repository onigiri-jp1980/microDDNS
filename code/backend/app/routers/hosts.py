import json
from app.models import Hosts, ApiKeys
from app.models.host import HostModel, HostResponseModel
from fastapi import APIRouter, Depends,Response
from app.middleswares.auth import ApiKeyAuthMiddleware

router = APIRouter(prefix="/host")

@router.get("/list", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホスト一覧を取得")
def get_hosts(api_key: ApiKeys = Depends(ApiKeyAuthMiddleware)):
    print("get_hosts(): spawned")
    content = {"message":"get_hosts(): completed"}
    return Response(content=json.dumps(content), status_code=200)


@router.post("/", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホストを作成",response_model=HostResponseModel)
def create_host(host: HostModel, api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->HostResponseModel:
    return {"message": "Hello, World!"}


@router.put("/", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホストを更新",response_model=HostResponseModel)
def update_host(host: HostModel, api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->HostResponseModel:
    return {"message": "Hello, World!"}


@router.delete("/delete", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホストを削除",response_model=HostResponseModel)
def delete_host(api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->HostResponseModel:
    return {"message": "Hello, World!"}