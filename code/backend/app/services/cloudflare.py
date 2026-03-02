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
        self.zones = [{'id': zone.id, **zone.to_dict()}
                      for zone in self.get_zones()]

    def get_zones(self):
        return self.client.zones.list().result

    def get_zone(self, zone_id):
        return self.client.zones.get(zone_id)

    def get_records(self, zone_id):
        _zones = self.client.dns.records.list(zone_id=zone_id).result
        return [{'id': record.id, **record.to_dict()}
                for record in _zones]

    def get_record(self, zone_id, record_id):
        return self.client.dns.records.get(zone_id=zone_id, record_id=record_id)

    def create_record(self, zone_id, record):
        return self.client.dns.records.create(zone_id=zone_id, record=record)

    def update_record(self, zone_id, record_id, record):
        return self.client.dns.records.update(zone_id=zone_id, record_id=record_id, record=record)
