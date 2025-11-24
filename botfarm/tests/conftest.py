import asyncio
import os
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import get_session
from app.models.user import Base
from main import app


@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db_session(
    test_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        yield session
        # Clean up database between tests by deleting all rows
        from app.models.user import User

        await session.execute(User.__table__.delete())
        await session.commit()


@pytest_asyncio.fixture
async def test_client(
    test_db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_db_session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
    app.dependency_overrides.clear()
