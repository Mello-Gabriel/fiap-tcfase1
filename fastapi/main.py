from fastapi import FastAPI

app = FastAPI()

@app.get("/")

@app.get('/')
def index():
    return {"message": "Funciona"}

