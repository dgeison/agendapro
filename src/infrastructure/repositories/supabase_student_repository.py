import logging
from typing import Optional
from uuid import UUID

from supabase import Client

from src.domain.entities.student import Student
from src.domain.ports.student_repository import StudentRepository

logger = logging.getLogger(__name__)

TABLE = "students"


class SupabaseStudentRepository(StudentRepository):
    def __init__(self, client: Client):
        self._client = client

    def save(self, student: Student) -> None:
        data = {
            "id": str(student.id),
            "name": student.name,
            "whatsapp": student.whatsapp,
            "email": student.email,
        }

        response = self._client.table(TABLE).upsert(data).execute()

        logger.info(
            "student_saved",
            extra={"student_id": str(student.id), "rows": len(response.data)},
        )

    def find_by_id(self, student_id: UUID) -> Optional[Student]:
        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("id", str(student_id))
            .maybe_single()
            .execute()
        )

        if response is None or response.data is None:
            return None

        return self._to_entity(response.data)

    def find_by_whatsapp(self, whatsapp: str) -> Optional[Student]:
        response = (
            self._client.table(TABLE)
            .select("*")
            .eq("whatsapp", whatsapp)
            .maybe_single()
            .execute()
        )

        if response is None or response.data is None:
            return None

        return self._to_entity(response.data)

    @staticmethod
    def _to_entity(row: dict) -> Student:
        return Student(
            id=UUID(row["id"]),
            name=row["name"],
            whatsapp=row["whatsapp"],
            email=row.get("email"),
        )
