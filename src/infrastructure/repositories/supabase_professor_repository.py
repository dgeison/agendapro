import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from supabase import Client

from src.domain.entities.professor import Professor
from src.domain.ports.professor_repository import ProfessorRepository

logger = logging.getLogger(__name__)

TABLE = "professors"


class SupabaseProfessorRepository(ProfessorRepository):
    def __init__(self, client: Client):
        self._client = client

    def save(self, professor: Professor) -> None:
        data = {
            "id": str(professor.id),
            "name": professor.name,
            "specialty": professor.specialty,
            "hourly_rate": float(professor.hourly_rate),
            "room_link": professor.room_link,
            "cancellation_tolerance_minutes": professor.cancellation_tolerance_minutes,
        }

        response = self._client.table(TABLE).upsert(data).execute()

        logger.info(
            "professor_saved",
            extra={"professor_id": str(professor.id), "rows": len(response.data)},
        )

    def find_by_id(self, professor_id: UUID) -> Optional[Professor]:
        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("id", str(professor_id))
            .maybe_single()
            .execute()
        )

        if response is None or response.data is None:
            return None

        return self._to_entity(response.data)

    @staticmethod
    def _to_entity(row: dict) -> Professor:
        return Professor(
            id=UUID(row["id"]),
            name=row["name"],
            specialty=row["specialty"],
            hourly_rate=Decimal(str(row["hourly_rate"])),
            room_link=row["room_link"],
            cancellation_tolerance_minutes=row["cancellation_tolerance_minutes"],
        )
