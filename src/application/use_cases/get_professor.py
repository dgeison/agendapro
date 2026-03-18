import logging
from uuid import UUID

from src.domain.entities.professor import Professor
from src.domain.errors import ProfessorNotFoundError
from src.domain.ports.professor_repository import ProfessorRepository

logger = logging.getLogger(__name__)


class GetProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self._professor_repository = professor_repository

    def execute(self, professor_id: UUID) -> Professor:
        professor = self._professor_repository.find_by_id(professor_id)
        if professor is None:
            logger.warning(
                "professor_not_found",
                extra={"professor_id": str(professor_id)},
            )
            raise ProfessorNotFoundError(professor_id=professor_id)

        return professor
