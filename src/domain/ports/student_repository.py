from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.student import Student


class StudentRepository(ABC):
    @abstractmethod
    def save(self, student: Student) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, student_id: UUID) -> Optional[Student]:
        raise NotImplementedError

    @abstractmethod
    def find_by_whatsapp(self, whatsapp: str) -> Optional[Student]:
        raise NotImplementedError
