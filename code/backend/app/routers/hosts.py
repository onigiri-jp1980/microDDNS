import json
from app.models import Hosts, ApiKeys
from app.models.host import HostModel, HostResponseModel
from fastapi import APIRouter, Depends,Response,HTTPException
from typing import List,Dict
from app.middleswares.auth import ApiKeyAuthMiddleware
from app.controllers.hosts import create, get_all

router = APIRouter(prefix="/host")

@router.get("s", dependencies=[Depends(ApiKeyAuthMiddleware)],
  response_model=None,
  tags=["host"],description="ホスト一覧を取得")
def get_hosts(api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->List[Hosts]:
    return get_all(api_key.secret)


@router.post("", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホストを作成",response_model=HostResponseModel)
def create_host(host: HostModel, api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->HostResponseModel:
    return create(host, api_key)


@router.put("", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホストを更新",response_model=HostResponseModel)
def update_host(host: HostModel, api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->HostResponseModel:
    return HostResponseModel(
      message="message from update_host()",
      fqdn=host.fqdn,
      ip_address=host.ip_address)


@router.delete("", dependencies=[Depends(ApiKeyAuthMiddleware)],
  tags=["host"],description="ホストを削除",response_model=HostResponseModel)
def delete_host(api_key: ApiKeys = Depends(ApiKeyAuthMiddleware))->HostResponseModel:
    return HostResponseModel(
      message="message from delete_host()",
      fqdn="",
      ip_address="")