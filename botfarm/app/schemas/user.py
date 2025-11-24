from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EnvEnum(str, Enum):
    """Environment types."""

    PROD = "prod"
    PREPROD = "preprod"
    STAGE = "stage"


class DomainEnum(str, Enum):
    """User domain types."""

    CANARY = "canary"
    REGULAR = "regular"


class UserBase(BaseModel):
    """Common user attributes."""

    project_id: UUID = Field(..., description="Project UUID")
    env: EnvEnum = Field(..., description="Environment")
    domain: DomainEnum = Field(..., description="User domain type")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    login: EmailStr = Field(..., description="User email/login")
    password: str = Field(..., min_length=8, description="User password")


class UserRead(UserBase):
    """Schema for reading a user."""

    id: UUID
    login: str
    created_at: datetime
    locktime: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserLock(BaseModel):
    """Schema for lock operations."""

    user_id: UUID = Field(..., description="User ID to lock/unlock")
