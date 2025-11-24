from typing import Any, List, Optional, cast
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserRead


async def create_user(session: AsyncSession, user_create: UserCreate) -> UserRead:
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        login=user_create.login,
        password=hashed_password,
        project_id=user_create.project_id,
        env=user_create.env,
        domain=user_create.domain,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return UserRead.model_validate(db_user)


async def get_users(session: AsyncSession) -> List[UserRead]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [UserRead.model_validate(user) for user in users]


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> Optional[UserRead]:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        return UserRead.model_validate(user)
    return None


async def acquire_lock(session: AsyncSession, user_id: UUID) -> bool:
    result = await session.execute(
        select(User).where(User.id == user_id, User.locktime.is_not(None))
    )
    if result.scalar_one_or_none():
        return False
    result = await session.execute(
        update(User)
        .where(User.id == user_id, User.locktime.is_(None))
        .values(locktime=func.now())
        .execution_options(synchronize_session="fetch")
    )
    if cast(Any, result).rowcount == 0:
        return False
    await session.commit()
    return True


async def release_lock(session: AsyncSession, user_id: UUID) -> bool:
    result = await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(locktime=None)
        .execution_options(synchronize_session="fetch")
    )
    if cast(Any, result).rowcount == 0:
        return False
    await session.commit()
    return True
