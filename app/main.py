from fastapi import FastAPI 


app = FastAPI()

@app.get('/')
def check():
    return {'Status': 'OK'}