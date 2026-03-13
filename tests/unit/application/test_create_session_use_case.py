import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from src.domain.entities.professor import Professor
from src.domain.entities.session import Session, SessionStatus
from src.domain.entities.student import Student
from src.domain.errors import SlotAlreadyBookedError
from src.application.use_cases.create_session import CreateSessionUseCase, CreateSessionInput


@pytest.fixture
def professor():
    return Professor(
        name="João Silva",
        specialty="Matemática",
        hourly_rate=Decimal("150.00"),
        room_link="https://meet.google.com/abc",
        cancellation_tolerance_minutes=30,
    )


@pytest.fixture
def student():
    return Student(name="Maria Oliveira", whatsapp="+5511999998888")


@pytest.fixture
def future_slot_start():
    return datetime.now(tz=timezone.utc) + timedelta(days=1)


@pytest.fixture
def mock_session_repository():
    repo = MagicMock()
    repo.find_conflicting_session.return_value = None
    return repo


@pytest.fixture
def use_case(mock_session_repository):
    return CreateSessionUseCase(session_repository=mock_session_repository)


class TestCreateSessionUseCase:
    def test_raises_error_when_slot_is_already_booked(
        self, use_case, mock_session_repository, professor, student, future_slot_start
    ):
        """Critério de aceite 1: Não é possível agendar em horário já ocupado."""
        slot_end = future_slot_start + timedelta(hours=1)
        existing_session = MagicMock(spec=Session)
        mock_session_repository.find_conflicting_session.return_value = existing_session

        input_data = CreateSessionInput(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        with pytest.raises(SlotAlreadyBookedError):
            use_case.execute(input_data)

    def test_created_session_has_pendent_payment_status_and_lock(
        self, use_case, mock_session_repository, professor, student, future_slot_start
    ):
        """Critério de aceite 2: Session criada inicia em PENDENT_PAYMENT com lock de 10 min."""
        slot_end = future_slot_start + timedelta(hours=1)
        mock_session_repository.find_conflicting_session.return_value = None

        before = datetime.now(tz=timezone.utc)

        input_data = CreateSessionInput(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        session = use_case.execute(input_data)

        after = datetime.now(tz=timezone.utc)

        assert session.status == SessionStatus.PENDENT_PAYMENT
        assert session.lock_expires_at is not None
        assert session.lock_expires_at >= before + timedelta(minutes=10)
        assert session.lock_expires_at <= after + timedelta(minutes=10)

    def test_created_session_is_saved_to_repository(
        self, use_case, mock_session_repository, professor, student, future_slot_start
    ):
        slot_end = future_slot_start + timedelta(hours=1)

        input_data = CreateSessionInput(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        session = use_case.execute(input_data)

        mock_session_repository.save.assert_called_once_with(session)

    def test_find_conflicting_session_is_called_with_correct_args(
        self, use_case, mock_session_repository, professor, student, future_slot_start
    ):
        slot_end = future_slot_start + timedelta(hours=1)

        input_data = CreateSessionInput(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        use_case.execute(input_data)

        mock_session_repository.find_conflicting_session.assert_called_once_with(
            professor_id=professor.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )
