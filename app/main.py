from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import embed_file, search, embed_bucket
from app.utils.logger import logger
from fastapi import HTTPException


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting Embedding Service...")
    try:
        yield
    finally:
        logger.info("Shutting down Embedding Service...")


app = FastAPI(
    title="Embedding Service",
    lifespan=lifespan,
)

app.include_router(embed_file.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(embed_bucket.router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
