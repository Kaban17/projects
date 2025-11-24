from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.user import acquire_lock, create_user, get_users, release_lock
from app.schemas.user import UserCreate, UserRead

router = APIRouter(tags=["users"])


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new bot user",
)
async def create_bot_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    """
    Create a new user in the botfarm.

    Verifies login uniqueness and hashes the password before storing.
    """
    try:
        return await create_user(session, user_in)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already exists",
        )


@router.get(
    "/",
    response_model=List[UserRead],
    summary="Get all bot users",
)
async def list_bot_users(
    session: AsyncSession = Depends(get_session),
) -> List[UserRead]:
    """
    Retrieve a list of all existing users in the botfarm.
    """
    return await get_users(session)


@router.post(
    "/{user_id}/acquire",
    status_code=status.HTTP_200_OK,
    summary="Acquire lock on a user",
)
async def acquire_bot_user_lock(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Lock a user for E2E testing by setting locktime.

    Returns 409 if user is already locked or does not exist.
    """
    success = await acquire_lock(session, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already locked or does not exist",
        )
    return {
        "message": "User locked successfully",
        "user_id": str(user_id),
    }


@router.post(
    "/{user_id}/release",
    status_code=status.HTTP_200_OK,
    summary="Release lock on a user",
)
async def release_bot_user_lock(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Release the lock on a user by clearing locktime.

    Returns 404 if user does not exist.
    """
    success = await release_lock(session, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return {
        "message": "User unlocked successfully",
        "user_id": str(user_id),
    }
