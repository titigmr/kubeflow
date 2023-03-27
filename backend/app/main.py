import os
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_version():
    return {"version": os.environ.get('TAG', 'v0.0.0')}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
