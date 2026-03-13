"""
Teste de integração: SupabaseProfessorRepository
Critério de aceite: save() persiste um Professor e find_by_id() o recupera corretamente.
"""
import pytest
from decimal import Decimal

from src.domain.entities.professor import Professor
from src.infrastructure.repositories.supabase_professor_repository import (
    SupabaseProfessorRepository,
)


class TestSupabaseProfessorRepository:
    def test_save_and_find_by_id(self, professor_repo: SupabaseProfessorRepository):
        professor = Professor(
            name="Integração Professor",
            specialty="Matemática",
            hourly_rate=Decimal("200.00"),
            room_link="https://meet.google.com/test-room",
            cancellation_tolerance_minutes=30,
        )

        professor_repo.save(professor)

        recovered = professor_repo.find_by_id(professor.id)

        assert recovered is not None
        assert recovered.id == professor.id
        assert recovered.name == professor.name
        assert recovered.specialty == professor.specialty
        assert recovered.hourly_rate == professor.hourly_rate
        assert recovered.room_link == professor.room_link
        assert recovered.cancellation_tolerance_minutes == professor.cancellation_tolerance_minutes

    def test_find_by_id_returns_none_for_unknown_id(
        self, professor_repo: SupabaseProfessorRepository
    ):
        from uuid import uuid4

        result = professor_repo.find_by_id(uuid4())

        assert result is None
