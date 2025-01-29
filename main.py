from fastapi import FastAPI
from apis.apis import router
from models.models import Base
from base import engine

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(router)

@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Custom-Header"] = "CustomValue"
    return response