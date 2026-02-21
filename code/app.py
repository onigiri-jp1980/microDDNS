from fastapi import FastAPI
from mangum import Mangum
from os import environ

app = FastAPI()

@app.get("/")
def hello_world():
    env=environ.__dict__.get('_data')
    return {"environment": env}

handler = Mangum(app)
