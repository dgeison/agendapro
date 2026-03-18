import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.domain.errors import SlotAlreadyLockedError
from src.domain.ports.appointment_repository import AppointmentRepository
from src.application.use_cases.create_appointment import CreateAppointmentUseCase


# ---------------------------------------------------------------------------
# Fake Repository (in-memory) — sem IO, sem Supabase
# ---------------------------------------------------------------------------

class FakeAppointmentRepository(AppointmentRepository):
    def __init__(self):
        self._store: list[dict] = []

    def save(self, appointment: dict) -> dict:
        saved = {**appointment, "id": str(uuid4())}
        self._store.append(saved)
        return saved

    def find_by_time_range(
        self, start_time: datetime, end_time: datetime, professor_id: str
    ) -> list:
        results = []
        for appt in self._store:
            if appt["professor_id"] != professor_id:
                continue
            appt_start = datetime.fromisoformat(appt["start_time"])
            appt_end = datetime.fromisoformat(appt["end_time"])
            # Overlap: existing.start < query.end AND existing.end > query.start
            if appt_start < end_time and appt_end > start_time:
                results.append(appt)
        return results


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def repo():
    return FakeAppointmentRepository()


@pytest.fixture
def use_case(repo):
    return CreateAppointmentUseCase(appointment_repository=repo)


@pytest.fixture
def aluno_id():
    return str(uuid4())


@pytest.fixture
def professor_id():
    return str(uuid4())


@pytest.fixture
def future_slot():
    start = datetime.now(tz=timezone.utc) + timedelta(days=7)
    end = start + timedelta(hours=1)
    return start, end


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

class TestCreateAppointmentUseCase:
    def test_create_appointment_success(
        self, use_case, aluno_id, professor_id, future_slot
    ):
        """Critério 1: Cria o agendamento com sucesso no cenário ideal (sem conflito)."""
        start, end = future_slot

        result = use_case.execute(
            aluno_id=aluno_id,
            professor_id=professor_id,
            start_time=start,
            end_time=end,
        )

        assert result is not None
        assert isinstance(result, dict)
        assert result["professor_id"] == professor_id
        assert result["aluno_id"] == aluno_id
        assert "id" in result

    def test_create_appointment_overlap_raises_slot_already_locked_error(
        self, use_case, aluno_id, professor_id, future_slot
    ):
        """Critério 2: Lança SlotAlreadyLockedError se o slot estiver ocupado."""
        start, end = future_slot

        # Cria o primeiro agendamento
        use_case.execute(
            aluno_id=aluno_id,
            professor_id=professor_id,
            start_time=start,
            end_time=end,
        )

        # Tenta criar outro que sobrepõe (30 min dentro do slot existente)
        overlap_start = start + timedelta(minutes=30)
        overlap_end = overlap_start + timedelta(hours=1)

        with pytest.raises(SlotAlreadyLockedError):
            use_case.execute(
                aluno_id=aluno_id,
                professor_id=professor_id,
                start_time=overlap_start,
                end_time=overlap_end,
            )

    def test_invalid_time_range_raises_value_error(
        self, use_case, aluno_id, professor_id
    ):
        """Critério 3: Lança ValueError se start_time >= end_time."""
        now = datetime.now(tz=timezone.utc)
        invalid_start = now + timedelta(hours=2)
        invalid_end = now + timedelta(hours=1)  # end antes de start

        with pytest.raises(ValueError, match="start_time must be before end_time"):
            use_case.execute(
                aluno_id=aluno_id,
                professor_id=professor_id,
                start_time=invalid_start,
                end_time=invalid_end,
            )
