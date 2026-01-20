from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1.router import router as api_router
from app.core.database import engine
from app.middleware.cors import setup_cors
from app.middleware.error_handler import validation_exception_handler
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API SGE",
    version="0.1.0",
    summary="API para el sistema de gestión escolar en Instituciones Educativas",
    lifespan=lifespan,
    exception_handlers={RequestValidationError: validation_exception_handler}
)

setup_cors(app)

app.include_router(api_router)
