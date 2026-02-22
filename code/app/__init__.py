from fastapi import FastAPI
from mangum import Mangum
from boto3 import Session
from os import environ
from app.routers import api_router

app = FastAPI()
app.include_router(api_router)