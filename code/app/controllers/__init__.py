from boto3 import Session
from os import environ as env

s3 = Session(profile_name=env.get('AWS_PROFILE', 'default'), region_name=env.get('AWS_REGION', 'ap-northeast-1')).client('s3')


def show_envs():
    e=env.__dict__.get('_data')
    return {"environment": e}


def get_buckets():
    return {"buckets": s3.list_buckets()['Buckets']}

