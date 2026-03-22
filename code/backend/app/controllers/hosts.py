from fastapi import Depends, HTTPException
from app.models.host import HostModel, HostResponseModel
from app.models import Hosts,ApiKeys
from app.services.cloudflare import DNSManagementService

def get_all(api_key: str):
    h=Hosts()
    return [host for host in h.get_all() if host['apiKey']==api_key]

def create(host: HostModel, api_key: ApiKeys = Depends(ApiKeys)):
    h=Hosts()
    h.fqdn=host.fqdn
    h.apiKey=api_key.secret
    h.ipAddress=host.ip_address
    try:
        result = h.save()
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))
    return host

def update(Hosts: Hosts = Depends(Hosts)):
    return Hosts.update(host.fqdn, host.ip_address)

def delete(Hosts: Hosts = Depends(Hosts)):
    return Hosts.delete(host.fqdn)