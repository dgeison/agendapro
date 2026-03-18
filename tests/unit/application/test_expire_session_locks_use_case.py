"""
Testes unitários — ExpireSessionLocksUseCase
Critérios de aceite do Plano 005:
  4. Use case com 2 sessões expiradas → chama expire() em ambas, chama update_status 2x, retorna 2
  5. Use case sem sessões expiradas → retorna 0, não chama update_status
"""
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, call, patch
from uuid import uuid4

import pytest

from src.domain.entities.session import Session, SessionStatus


def _make_expired_session() -> Session:
    """Cria uma Session com lock já vencido usando __new__ para evitar a validação de slot."""
    session = Session.__new__(Session)
    session.id = uuid4()
    session.professor_id = uuid4()
    session.student_id = uuid4()
    session.slot_start = datetime.now(tz=timezone.utc) + timedelta(days=1)
    session.slot_end = session.slot_start + timedelta(hours=1)
    session.status = SessionStatus.PENDENT_PAYMENT
    session.lock_expires_at = datetime.now(tz=timezone.utc) - timedelta(minutes=5)
    return session


class TestExpireSessionLocksUseCase:
    def test_expires_all_pending_sessions_and_returns_count(self):
        """Critério 4: 2 sessões expiradas → expire() em ambas, update_status 2x, retorna 2."""
        from src.application.use_cases.expire_session_locks import ExpireSessionLocksUseCase

        mock_repo = MagicMock()
        session_a = _make_expired_session()
        session_b = _make_expired_session()
        mock_repo.find_expired_pending.return_value = [session_a, session_b]

        use_case = ExpireSessionLocksUseCase(session_repository=mock_repo)
        result = use_case.execute()

        assert result == 2
        assert session_a.status == SessionStatus.EXPIRED
        assert session_b.status == SessionStatus.EXPIRED
        assert mock_repo.update_status.call_count == 2
        mock_repo.update_status.assert_any_call(session_a)
        mock_repo.update_status.assert_any_call(session_b)

    def test_returns_zero_when_no_expired_sessions(self):
        """Critério 5: sem sessões expiradas → retorna 0, update_status não chamado."""
        from src.application.use_cases.expire_session_locks import ExpireSessionLocksUseCase

        mock_repo = MagicMock()
        mock_repo.find_expired_pending.return_value = []

        use_case = ExpireSessionLocksUseCase(session_repository=mock_repo)
        result = use_case.execute()

        assert result == 0
        mock_repo.update_status.assert_not_called()
