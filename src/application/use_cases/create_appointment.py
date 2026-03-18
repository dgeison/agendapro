import logging
from datetime import datetime

from src.domain.errors import SlotAlreadyLockedError
from src.domain.ports.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)


class CreateAppointmentUseCase:
    def __init__(self, appointment_repository: AppointmentRepository):
        self._appointment_repository = appointment_repository

    def execute(
        self,
        aluno_id: str,
        professor_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> dict:
        if start_time >= end_time:
            raise ValueError("start_time must be before end_time")

        conflicts = self._appointment_repository.find_by_time_range(
            start_time=start_time,
            end_time=end_time,
            professor_id=professor_id,
        )

        if conflicts:
            logger.warning(
                "slot_already_locked",
                extra={
                    "professor_id": professor_id,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                },
            )
            raise SlotAlreadyLockedError(
                professor_id=professor_id,
                start_time=start_time,
                end_time=end_time,
            )

        appointment = {
            "professor_id": professor_id,
            "aluno_id": aluno_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }

        saved = self._appointment_repository.save(appointment)

        logger.info(
            "appointment_created",
            extra={
                "appointment_id": saved.get("id"),
                "professor_id": professor_id,
                "aluno_id": aluno_id,
                "start_time": start_time.isoformat(),
            },
        )

        return saved
