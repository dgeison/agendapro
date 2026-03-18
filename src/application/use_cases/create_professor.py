import logging
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.entities.professor import Professor
from src.domain.errors import ProfessorAlreadyExistsError
from src.domain.ports.professor_repository import ProfessorRepository

logger = logging.getLogger(__name__)


@dataclass
class CreateProfessorInput:
    professor_id: UUID
    name: str
    specialty: str
    hourly_rate: Decimal
    room_link: str
    cancellation_tolerance_minutes: int


class CreateProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self._professor_repository = professor_repository

    def execute(self, input_data: CreateProfessorInput) -> Professor:
        existing = self._professor_repository.find_by_id(input_data.professor_id)
        if existing is not None:
            logger.warning(
                "professor_already_exists",
                extra={"professor_id": str(input_data.professor_id)},
            )
            raise ProfessorAlreadyExistsError(professor_id=input_data.professor_id)

        professor = Professor(
            id=input_data.professor_id,
            name=input_data.name,
            specialty=input_data.specialty,
            hourly_rate=input_data.hourly_rate,
            room_link=input_data.room_link,
            cancellation_tolerance_minutes=input_data.cancellation_tolerance_minutes,
        )

        self._professor_repository.save(professor)

        logger.info(
            "professor_created",
            extra={"professor_id": str(professor.id)},
        )

        return professor
