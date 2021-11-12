from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"钱舟是": "蔡徐坤"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
