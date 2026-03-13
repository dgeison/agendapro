from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.professor import Professor


class ProfessorRepository(ABC):
    @abstractmethod
    def save(self, professor: Professor) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, professor_id: UUID) -> Optional[Professor]:
        raise NotImplementedError
