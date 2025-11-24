from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import lifespan
from app.routers import users

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Botfarm service for E2E test users",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
