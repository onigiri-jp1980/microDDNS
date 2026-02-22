from os import environ as env
from cloudflare import Cloudflare

def get_client():
    # API Token 使用時、CLOUDFLARE_EMAIL があると SDK が X-Auth-Email のみ送り
    # X-Auth-Key が無いため 403 になる。api_token を優先させるため一時退避。
    email_backup = env.pop('CLOUDFLARE_EMAIL', None)
    try:
        return Cloudflare(api_token=env.get('CLOUDFLARE_API_TOKEN'))
    finally:
        if email_backup is not None:
            env['CLOUDFLARE_EMAIL'] = email_backup
      

class DNSManagementService:
    def __init__(self):
        self.client = get_client()

    def get_zones(self):
        return self.client.zones.list()

    def get_zone(self, zone_id):
        return self.client.zones.get(zone_id)

    def get_records(self, zone_id):
        return self.client.zones.get(zone_id).dns_records.get()