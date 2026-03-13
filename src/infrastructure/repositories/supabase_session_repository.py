import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from supabase import Client

from src.domain.entities.session import Session, SessionStatus
from src.domain.ports.session_repository import SessionRepository

logger = logging.getLogger(__name__)

TABLE = "sessions"


class SupabaseSessionRepository(SessionRepository):
    def __init__(self, client: Client):
        self._client = client

    def save(self, session: Session) -> None:
        data = {
            "id": str(session.id),
            "professor_id": str(session.professor_id),
            "student_id": str(session.student_id),
            "slot_start": session.slot_start.isoformat(),
            "slot_end": session.slot_end.isoformat(),
            "status": session.status.value,
            "lock_expires_at": session.lock_expires_at.isoformat(),
        }

        response = self._client.table(TABLE).upsert(data).execute()

        logger.info(
            "session_saved",
            extra={
                "session_id": str(session.id),
                "status": session.status.value,
                "rows": len(response.data),
            },
        )

    def find_by_id(self, session_id: UUID) -> Optional[Session]:
        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("id", str(session_id))
            .maybe_single()
            .execute()
        )

        if response is None or response.data is None:
            return None

        return self._to_entity(response.data)

    def find_conflicting_session(
        self,
        professor_id: UUID,
        slot_start: datetime,
        slot_end: datetime,
    ) -> Optional[Session]:
        """
        Retorna uma Session ativa (não CANCELLED) cujo slot se sobreponha
        ao intervalo [slot_start, slot_end) para o professor dado.
        Overlapping condition: existing.slot_start < slot_end AND existing.slot_end > slot_start
        """
        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("professor_id", str(professor_id))
            .neq("status", SessionStatus.CANCELLED.value)
            .lt("slot_start", slot_end.isoformat())
            .gt("slot_end", slot_start.isoformat())
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        logger.warning(
            "conflicting_session_found",
            extra={
                "professor_id": str(professor_id),
                "slot_start": slot_start.isoformat(),
                "slot_end": slot_end.isoformat(),
                "conflicting_id": response.data[0]["id"],
            },
        )

        return self._to_entity(response.data[0])

    @staticmethod
    def _to_entity(row: dict) -> Session:
        session = Session.__new__(Session)
        session.id = UUID(row["id"])
        session.professor_id = UUID(row["professor_id"])
        session.student_id = UUID(row["student_id"])
        session.slot_start = datetime.fromisoformat(row["slot_start"]).replace(
            tzinfo=timezone.utc
        )
        session.slot_end = datetime.fromisoformat(row["slot_end"]).replace(
            tzinfo=timezone.utc
        )
        session.status = SessionStatus(row["status"])
        session.lock_expires_at = datetime.fromisoformat(row["lock_expires_at"]).replace(
            tzinfo=timezone.utc
        )
        return session
