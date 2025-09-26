<<<<<<< HEAD
from typing import Optional

=======
>>>>>>> b84106d (wagner alteracao fastapi-render)
from fastapi import FastAPI

app = FastAPI()

<<<<<<< HEAD

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
=======
@app.get('/')
def index():
    return {"message": "Funciona"}
>>>>>>> b84106d (wagner alteracao fastapi-render)
