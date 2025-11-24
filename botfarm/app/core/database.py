from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.user import Base

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
)


async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session.
    """
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
