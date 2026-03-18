import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.entities.session import Session, SessionStatus
from src.domain.entities.professor import Professor
from src.domain.entities.student import Student


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


class TestSession:
    def test_create_session_with_valid_data(self, professor, student, future_slot_start):
        slot_end = future_slot_start + timedelta(hours=1)

        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        assert isinstance(session.id, UUID)
        assert session.professor_id == professor.id
        assert session.student_id == student.id
        assert session.slot_start == future_slot_start
        assert session.slot_end == slot_end

    def test_session_initial_status_is_pendent_payment(self, professor, student, future_slot_start):
        slot_end = future_slot_start + timedelta(hours=1)

        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        assert session.status == SessionStatus.PENDENT_PAYMENT

    def test_session_lock_expires_in_10_minutes(self, professor, student, future_slot_start):
        before_creation = datetime.now(tz=timezone.utc)
        slot_end = future_slot_start + timedelta(hours=1)

        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        after_creation = datetime.now(tz=timezone.utc)

        expected_lock_min = before_creation + timedelta(minutes=10)
        expected_lock_max = after_creation + timedelta(minutes=10)

        assert session.lock_expires_at is not None
        assert expected_lock_min <= session.lock_expires_at <= expected_lock_max

    def test_session_slot_end_must_be_after_slot_start(self, professor, student, future_slot_start):
        slot_end = future_slot_start - timedelta(minutes=1)

        with pytest.raises(ValueError, match="slot_end"):
            Session(
                professor_id=professor.id,
                student_id=student.id,
                slot_start=future_slot_start,
                slot_end=slot_end,
            )

    def test_session_can_be_confirmed(self, professor, student, future_slot_start):
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        session.confirm()

        assert session.status == SessionStatus.CONFIRMED

    def test_session_can_be_cancelled(self, professor, student, future_slot_start):
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )

        session.cancel()

        assert session.status == SessionStatus.CANCELLED

    def test_confirmed_session_cannot_be_confirmed_again(self, professor, student, future_slot_start):
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )
        session.confirm()

        with pytest.raises(ValueError, match="status"):
            session.confirm()

    def test_cancelled_session_cannot_be_confirmed(self, professor, student, future_slot_start):
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )
        session.cancel()

        with pytest.raises(ValueError, match="status"):
            session.confirm()

    def test_expire_pendent_payment_session_with_expired_lock(self, professor, student, future_slot_start):
        """Critério 1 Plano 005: expire() em PENDENT_PAYMENT com lock vencido → EXPIRED."""
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )
        # Forçar lock vencido
        session.lock_expires_at = datetime.now(tz=timezone.utc) - timedelta(minutes=1)

        session.expire()

        assert session.status == SessionStatus.EXPIRED

    def test_expire_already_expired_session_raises_value_error(self, professor, student, future_slot_start):
        """Critério 2 Plano 005: expire() em sessão já EXPIRED → ValueError."""
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )
        session.lock_expires_at = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
        session.expire()

        with pytest.raises(ValueError):
            session.expire()

    def test_expire_session_with_valid_lock_raises_value_error(self, professor, student, future_slot_start):
        """Critério 3 Plano 005: expire() com lock ainda válido → ValueError."""
        slot_end = future_slot_start + timedelta(hours=1)
        session = Session(
            professor_id=professor.id,
            student_id=student.id,
            slot_start=future_slot_start,
            slot_end=slot_end,
        )
        # lock_expires_at é now + 10min por padrão — ainda não venceu

        with pytest.raises(ValueError):
            session.expire()
