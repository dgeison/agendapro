import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.entities.session import Session
from src.domain.errors import SlotAlreadyBookedError
from src.domain.ports.session_repository import SessionRepository

logger = logging.getLogger(__name__)


@dataclass
class CreateSessionInput:
    professor_id: UUID
    student_id: UUID
    slot_start: datetime
    slot_end: datetime


class CreateSessionUseCase:
    def __init__(self, session_repository: SessionRepository):
        self._session_repository = session_repository

    def execute(self, input_data: CreateSessionInput) -> Session:
        conflicting = self._session_repository.find_conflicting_session(
            professor_id=input_data.professor_id,
            slot_start=input_data.slot_start,
            slot_end=input_data.slot_end,
        )

        if conflicting is not None:
            logger.warning(
                "slot_already_booked",
                extra={
                    "professor_id": str(input_data.professor_id),
                    "slot_start": input_data.slot_start.isoformat(),
                    "slot_end": input_data.slot_end.isoformat(),
                },
            )
            raise SlotAlreadyBookedError(
                professor_id=input_data.professor_id,
                slot_start=input_data.slot_start,
                slot_end=input_data.slot_end,
            )

        session = Session(
            professor_id=input_data.professor_id,
            student_id=input_data.student_id,
            slot_start=input_data.slot_start,
            slot_end=input_data.slot_end,
        )

        self._session_repository.save(session)

        logger.info(
            "session_created",
            extra={
                "session_id": str(session.id),
                "professor_id": str(session.professor_id),
                "student_id": str(session.student_id),
                "slot_start": session.slot_start.isoformat(),
                "lock_expires_at": session.lock_expires_at.isoformat(),
            },
        )

        return session
