from typing import Union
from contextlib import asynccontextmanager
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI

from src.apis import apis
from src.prisma import prisma


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. APPLICATION START | Connect to prisma client
    await prisma.connect()
    print("Prisma.Connected?")

    # 2. Give way to application so it can run
    yield

    # 3. APPLICATION STOP: disconnect from prisma
    await prisma.disconnect()
    print("Prisma.Disconnected?")


app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(apis, prefix="/apis")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
