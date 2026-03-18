from abc import ABC, abstractmethod
from datetime import datetime


class AppointmentRepository(ABC):
    @abstractmethod
    def save(self, appointment: dict) -> dict:
        """Persiste um agendamento. Lança SlotAlreadyLockedError em caso de conflito de unique constraint."""
        raise NotImplementedError

    @abstractmethod
    def find_by_time_range(
        self, start_time: datetime, end_time: datetime, professor_id: str
    ) -> list:
        """Retorna agendamentos do professor cujo slot se sobreponha ao intervalo dado."""
        raise NotImplementedError
