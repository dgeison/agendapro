import pytest
from decimal import Decimal
from uuid import UUID

from src.domain.entities.professor import Professor


class TestProfessor:
    def test_create_professor_with_valid_data(self):
        professor = Professor(
            name="João Silva",
            specialty="Matemática",
            hourly_rate=Decimal("150.00"),
            room_link="https://meet.google.com/abc-defg-hij",
            cancellation_tolerance_minutes=30,
        )

        assert isinstance(professor.id, UUID)
        assert professor.name == "João Silva"
        assert professor.specialty == "Matemática"
        assert professor.hourly_rate == Decimal("150.00")
        assert professor.room_link == "https://meet.google.com/abc-defg-hij"
        assert professor.cancellation_tolerance_minutes == 30

    def test_professor_id_is_unique(self):
        p1 = Professor(
            name="Professor A",
            specialty="Física",
            hourly_rate=Decimal("100.00"),
            room_link="https://example.com/room1",
            cancellation_tolerance_minutes=15,
        )
        p2 = Professor(
            name="Professor B",
            specialty="Química",
            hourly_rate=Decimal("120.00"),
            room_link="https://example.com/room2",
            cancellation_tolerance_minutes=20,
        )

        assert p1.id != p2.id

    def test_professor_hourly_rate_must_be_positive(self):
        with pytest.raises(ValueError, match="hourly_rate"):
            Professor(
                name="Professor Inválido",
                specialty="Biologia",
                hourly_rate=Decimal("-50.00"),
                room_link="https://example.com/room",
                cancellation_tolerance_minutes=15,
            )

    def test_professor_cancellation_tolerance_must_be_non_negative(self):
        with pytest.raises(ValueError, match="cancellation_tolerance_minutes"):
            Professor(
                name="Professor Inválido",
                specialty="Biologia",
                hourly_rate=Decimal("100.00"),
                room_link="https://example.com/room",
                cancellation_tolerance_minutes=-1,
            )
