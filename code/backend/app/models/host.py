from pydantic import BaseModel

class HostModel(BaseModel):
    fqdn: str
    ip_address: str

class HostResponseModel(HostModel):
    message: str