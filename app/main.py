from fastapi import FastAPI 
from app.api.routers import user

app = FastAPI()

app.include_router(user.router)

@app.get('/')
def check():
    return {'Status': 'OK'}

