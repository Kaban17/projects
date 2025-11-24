from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.crud.user import acquire_lock, create_user, get_users, release_lock
from app.schemas.user import DomainEnum, EnvEnum, UserCreate


@pytest.mark.asyncio
class TestCRUD:
    @pytest.fixture
    def user_create(self):
        return UserCreate(
            login="test@example.com",
            password="testpass123",
            project_id=uuid4(),
            env=EnvEnum.PROD,
            domain=DomainEnum.CANARY,
        )

    @pytest.fixture
    def mock_session(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_result.scalar_one_or_none.return_value = None
        mock_result.rowcount = 0
        session.execute.return_value = mock_result
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        return session

    async def test_create_user(self, mock_session, user_create):
        with patch("app.crud.user.get_password_hash", return_value="hashed"):
            mock_session.refresh.side_effect = lambda obj: (
                setattr(obj, "id", uuid4()),
                setattr(obj, "created_at", datetime.now()),
                None,
            )
            result = await create_user(mock_session, user_create)
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            assert result.login == user_create.login
            assert result.id is not None
            assert result.created_at is not None

    async def test_get_users(self, mock_session):
        result = await get_users(mock_session)
        mock_session.execute.assert_called_once()
        assert result == []

    async def test_acquire_lock_success(self, mock_session):
        mock_result1 = MagicMock()
        mock_result1.scalar_one_or_none.return_value = None
        mock_result2 = MagicMock()
        mock_result2.rowcount = 1
        mock_session.execute.side_effect = [mock_result1, mock_result2]
        success = await acquire_lock(mock_session, uuid4())
        assert success

    async def test_acquire_lock_already(self, mock_session):
        mock_session.execute.return_value.scalar_one_or_none.return_value = object()
        success = await acquire_lock(mock_session, uuid4())
        assert not success

    async def test_release_lock(self, mock_session):
        mock_session.execute.return_value.rowcount = 1
        success = await release_lock(mock_session, uuid4())
        assert success
