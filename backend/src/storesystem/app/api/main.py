from fastapi import FastAPI
from storesystem.app.api.routes.items import items_router

app = FastAPI()
app.include_router(items_router)


@app.get("/")
def root():
    return {"message": "This is Root. Hello from FastAPI!"}
