import logging

from src.domain.ports.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class ExpireSessionLocksUseCase:
    def __init__(self, session_repository: SessionRepository):
        self._session_repository = session_repository

    def execute(self) -> int:
        """Expira todos os locks vencidos. Retorna a quantidade de sessões expiradas."""
        expired_sessions = self._session_repository.find_expired_pending()

        for session in expired_sessions:
            session.expire()
            self._session_repository.update_status(session)

        count = len(expired_sessions)
        if count > 0:
            logger.info("session_locks_expired", extra={"count": count})

        return count
