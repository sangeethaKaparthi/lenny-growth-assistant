from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings 

from app.api.chat import router as chat_router 
from app.api.sessions import router as sessions_router

from app.database import (
    close_database,
    engine,
    init_database,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("lenny-growth-assistant")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Lenny Growth Assistant")

    try:
        await init_database()
        logger.info("PostgreSQL + pgvector initialized successfully")
    except Exception:
        logger.exception("Database initialization failed")

    yield

    logger.info("Shutting down application")
    await close_database()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="The Lenny Growth Assistant",
    lifespan=lifespan,
)


origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router)
app.include_router(sessions_router)

@app.get("/")
async def root():
    return {
        "message": "Lenny Growth Assistant API",
        "status": "running",
    }


@app.get("/api/health")
async def health():
    database_status = "healthy"

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "unhealthy"

    return {
        "status": (
            "ok"
            if database_status == "healthy"
            else "degraded"
        ),
        "database": database_status,
        "ollama": settings.ollama_base_url,
        "llm_provider": settings.default_llm_provider,
    }