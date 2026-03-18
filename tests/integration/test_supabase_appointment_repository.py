"""
Teste de integração: SupabaseAppointmentRepository
Critérios de aceite:
  1. save() persiste um agendamento e retorna o dict com os dados salvos.
  2. save() com horário em conflito (unique constraint) lança SlotAlreadyLockedError.
  3. find_by_time_range() retorna agendamentos que se sobrepõem ao intervalo dado.
"""
import uuid
from datetime import datetime, timedelta, timezone

import pytest

from src.domain.errors import SlotAlreadyLockedError
from src.infrastructure.repositories.supabase_appointment_repository import (
    SupabaseAppointmentRepository,
)


@pytest.fixture(scope="module")
def appointment_repo(supabase_client):
    return SupabaseAppointmentRepository(supabase_client)


@pytest.fixture
def professor_id():
    return str(uuid.uuid4())


@pytest.fixture
def future_slot():
    start = datetime.now(tz=timezone.utc) + timedelta(days=30)
    end = start + timedelta(hours=1)
    return start, end


class TestSupabaseAppointmentRepository:
    def test_save_persists_appointment_and_returns_dict(
        self, appointment_repo: SupabaseAppointmentRepository, professor_id: str, future_slot
    ):
        """Critério 1: save() persiste e retorna dict com dados do agendamento."""
        start, end = future_slot

        appointment = {
            "professor_id": professor_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }

        result = appointment_repo.save(appointment)

        assert result is not None
        assert isinstance(result, dict)
        assert result["professor_id"] == professor_id
        assert "id" in result

    def test_save_raises_slot_already_locked_error_on_duplicate(
        self, appointment_repo: SupabaseAppointmentRepository, professor_id: str
    ):
        """Critério 2: save() lança SlotAlreadyLockedError em caso de unique constraint violation."""
        start = datetime.now(tz=timezone.utc) + timedelta(days=45)
        end = start + timedelta(hours=1)

        appointment = {
            "professor_id": professor_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }

        appointment_repo.save(appointment)

        with pytest.raises(SlotAlreadyLockedError):
            appointment_repo.save(appointment)

    def test_find_by_time_range_returns_overlapping_appointments(
        self, appointment_repo: SupabaseAppointmentRepository
    ):
        """Critério 3: find_by_time_range() retorna agendamentos que se sobrepõem ao intervalo."""
        prof_id = str(uuid.uuid4())
        start = datetime.now(tz=timezone.utc) + timedelta(days=60)
        end = start + timedelta(hours=1)

        appointment_repo.save({
            "professor_id": prof_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        })

        # Busca com intervalo que se sobrepõe (30 min dentro do slot existente)
        query_start = start + timedelta(minutes=30)
        query_end = query_start + timedelta(hours=1)

        results = appointment_repo.find_by_time_range(
            start_time=query_start,
            end_time=query_end,
            professor_id=prof_id,
        )

        assert len(results) >= 1
        assert any(r["professor_id"] == prof_id for r in results)

    def test_find_by_time_range_returns_empty_for_free_slot(
        self, appointment_repo: SupabaseAppointmentRepository
    ):
        """find_by_time_range() retorna lista vazia para slot sem agendamentos."""
        prof_id = str(uuid.uuid4())
        far_future = datetime.now(tz=timezone.utc) + timedelta(days=365)
        far_end = far_future + timedelta(hours=1)

        results = appointment_repo.find_by_time_range(
            start_time=far_future,
            end_time=far_end,
            professor_id=prof_id,
        )

        assert results == []
