from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.entities.session import Session


class SessionRepository(ABC):
    @abstractmethod
    def save(self, session: Session) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session_id: UUID) -> Optional[Session]:
        raise NotImplementedError

    @abstractmethod
    def find_conflicting_session(
        self,
        professor_id: UUID,
        slot_start: datetime,
        slot_end: datetime,
    ) -> Optional[Session]:
        """Retorna uma Session ativa que conflite com o slot dado para o professor."""
        raise NotImplementedError

    @abstractmethod
    def find_expired_pending(self) -> list[Session]:
        """Retorna sessões com status PENDENT_PAYMENT e lock_expires_at < now()."""
        raise NotImplementedError

    @abstractmethod
    def update_status(self, session: Session) -> None:
        """Persiste a mudança de status de uma sessão."""
        raise NotImplementedError
