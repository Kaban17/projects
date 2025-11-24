from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    """
    User model for botfarm.
    Represents a test user credentials for E2E testing.
    """

    __tablename__ = "users"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    login: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(String)
    project_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
    )
    env: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )
    domain: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )
    locktime: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
