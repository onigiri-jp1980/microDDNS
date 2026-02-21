from fastapi import FastAPI
from mangum import Mangum
from boto3 import Session
from os import environ

app = FastAPI()
s3 = Session(profile_name=environ.get('AWS_PROFILE', 'default'), region_name=environ.get('AWS_REGION', 'ap-northeast-1')).client('s3')


@app.get("/")
def hello_world():
    env=environ.__dict__.get('_data')
    return {"environment": env}


@app.get("/buckets")
def get_buckets():
    return {"buckets": s3.list_buckets()['Buckets']}



handler = Mangum(app)
