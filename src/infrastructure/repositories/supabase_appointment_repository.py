import logging
from datetime import datetime

from supabase import Client

from src.domain.errors import SlotAlreadyLockedError
from src.domain.ports.appointment_repository import AppointmentRepository

logger = logging.getLogger(__name__)

TABLE = "appointments"
UNIQUE_VIOLATION_CODE = "23505"


class SupabaseAppointmentRepository(AppointmentRepository):
    def __init__(self, client: Client):
        self._client = client

    def save(self, appointment: dict) -> dict:
        try:
            response = self._client.table(TABLE).insert(appointment).execute()
        except Exception as exc:
            if UNIQUE_VIOLATION_CODE in str(exc):
                logger.warning(
                    "slot_already_locked",
                    extra={
                        "professor_id": appointment.get("professor_id"),
                        "start_time": appointment.get("start_time"),
                        "end_time": appointment.get("end_time"),
                    },
                )
                raise SlotAlreadyLockedError(
                    professor_id=appointment.get("professor_id"),
                    start_time=appointment.get("start_time"),
                    end_time=appointment.get("end_time"),
                ) from exc
            raise

        saved = response.data[0]
        logger.info(
            "appointment_saved",
            extra={
                "appointment_id": saved.get("id"),
                "professor_id": saved.get("professor_id"),
            },
        )
        return saved

    def find_by_time_range(
        self, start_time: datetime, end_time: datetime, professor_id: str
    ) -> list:
        """
        Retorna agendamentos cujo slot se sobreponha ao intervalo [start_time, end_time).
        Overlapping condition: existing.start_time < end_time AND existing.end_time > start_time
        """
        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("professor_id", professor_id)
            .lt("start_time", end_time.isoformat())
            .gt("end_time", start_time.isoformat())
            .execute()
        )

        results = response.data or []
        logger.info(
            "appointments_queried_by_time_range",
            extra={
                "professor_id": professor_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "count": len(results),
            },
        )
        return results
