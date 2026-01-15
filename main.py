from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import videos
from db.models import Base
from db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    await engine.dispose()


app = FastAPI(
    lifespan=lifespan
)


app.include_router(videos.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
