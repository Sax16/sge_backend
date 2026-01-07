from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.database import engine
from app.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app = FastAPI(lifespan=lifespan)


app.include_router(api_router)
