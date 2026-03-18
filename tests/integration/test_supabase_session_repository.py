"""
Teste de integração: SupabaseSessionRepository
Critérios de aceite:
  1. save() persiste Session com status PENDENT_PAYMENT e lock_expires_at preenchido.
  2. find_conflicting_session() retorna a sessão correta ao buscar por professor e slot.
"""
import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from src.domain.entities.professor import Professor
from src.domain.entities.session import Session, SessionStatus
from src.domain.entities.student import Student
from src.infrastructure.repositories.supabase_professor_repository import (
    SupabaseProfessorRepository,
)
from src.infrastructure.repositories.supabase_session_repository import (
    SupabaseSessionRepository,
)
from src.infrastructure.repositories.supabase_student_repository import (
    SupabaseStudentRepository,
)


@pytest.fixture(scope="module")
def persisted_professor(professor_repo: SupabaseProfessorRepository):
    professor = Professor(
        name="Professor Sessão",
        specialty="Física",
        hourly_rate=Decimal("180.00"),
        room_link="https://meet.google.com/sessao-room",
        cancellation_tolerance_minutes=15,
    )
    professor_repo.save(professor)
    return professor


@pytest.fixture(scope="module")
def persisted_student(student_repo: SupabaseStudentRepository):
    import uuid
    unique_wpp = f"+551199999{uuid.uuid4().hex[:4]}"
    student = Student(
        name="Aluno Sessão",
        whatsapp=unique_wpp,
    )
    student_repo.save(student)
    return student


@pytest.fixture
def future_slot():
    start = datetime.now(tz=timezone.utc) + timedelta(days=7)
    end = start + timedelta(hours=1)
    return start, end


class TestSupabaseSessionRepository:
    def test_save_creates_session_with_pendent_payment_status_and_lock(
        self,
        session_repo: SupabaseSessionRepository,
        persisted_professor: Professor,
        persisted_student: Student,
        future_slot,
    ):
        """Critério de aceite 1."""
        slot_start, slot_end = future_slot

        session = Session(
            professor_id=persisted_professor.id,
            student_id=persisted_student.id,
            slot_start=slot_start,
            slot_end=slot_end,
        )

        session_repo.save(session)

        recovered = session_repo.find_by_id(session.id)

        assert recovered is not None
        assert recovered.id == session.id
        assert recovered.status == SessionStatus.PENDENT_PAYMENT
        assert recovered.lock_expires_at is not None

    def test_find_conflicting_session_returns_booked_slot(
        self,
        session_repo: SupabaseSessionRepository,
        persisted_professor: Professor,
        persisted_student: Student,
    ):
        """Critério de aceite 2: find_conflicting_session retorna sessão que ocupa o slot."""
        slot_start = datetime.now(tz=timezone.utc) + timedelta(days=14)
        slot_end = slot_start + timedelta(hours=1)

        session = Session(
            professor_id=persisted_professor.id,
            student_id=persisted_student.id,
            slot_start=slot_start,
            slot_end=slot_end,
        )
        session_repo.save(session)

        # Busca com slot que se sobrepõe (30 min dentro do slot existente)
        overlapping_start = slot_start + timedelta(minutes=30)
        overlapping_end = overlapping_start + timedelta(hours=1)

        conflict = session_repo.find_conflicting_session(
            professor_id=persisted_professor.id,
            slot_start=overlapping_start,
            slot_end=overlapping_end,
        )

        assert conflict is not None
        assert conflict.professor_id == persisted_professor.id

    def test_find_conflicting_session_returns_none_for_free_slot(
        self,
        session_repo: SupabaseSessionRepository,
        persisted_professor: Professor,
    ):
        # Slot bem distante no futuro — não deve colidir com nenhum existente
        slot_start = datetime.now(tz=timezone.utc) + timedelta(days=365)
        slot_end = slot_start + timedelta(hours=1)

        conflict = session_repo.find_conflicting_session(
            professor_id=persisted_professor.id,
            slot_start=slot_start,
            slot_end=slot_end,
        )

        assert conflict is None

    def test_find_expired_pending_returns_only_expired_locks(
        self,
        session_repo: SupabaseSessionRepository,
        persisted_professor: Professor,
        persisted_student: Student,
    ):
        """Critério 7 Plano 005: find_expired_pending() retorna apenas sessões com lock vencido e PENDENT_PAYMENT."""
        # Criar sessão com lock artificialmente vencido via update direto
        slot_start = datetime.now(tz=timezone.utc) + timedelta(days=60)
        slot_end = slot_start + timedelta(hours=1)
        session = Session(
            professor_id=persisted_professor.id,
            student_id=persisted_student.id,
            slot_start=slot_start,
            slot_end=slot_end,
        )
        session_repo.save(session)

        # Vencer o lock manualmente via update_status indireto — forçar lock_expires_at no passado
        past_lock = (datetime.now(tz=timezone.utc) - timedelta(minutes=5)).isoformat()
        session_repo._client.table("sessions").update({"lock_expires_at": past_lock}).eq(
            "id", str(session.id)
        ).execute()

        expired = session_repo.find_expired_pending()

        found_ids = {s.id for s in expired}
        assert session.id in found_ids

    def test_update_status_persists_status_change(
        self,
        session_repo: SupabaseSessionRepository,
        persisted_professor: Professor,
        persisted_student: Student,
    ):
        """Critério 8 Plano 005: update_status() persiste mudança de status no banco."""
        from src.domain.entities.session import SessionStatus

        slot_start = datetime.now(tz=timezone.utc) + timedelta(days=90)
        slot_end = slot_start + timedelta(hours=1)
        session = Session(
            professor_id=persisted_professor.id,
            student_id=persisted_student.id,
            slot_start=slot_start,
            slot_end=slot_end,
        )
        session_repo.save(session)

        # Mudar status para EXPIRED manualmente no objeto e persistir
        session.status = SessionStatus.EXPIRED
        session_repo.update_status(session)

        recovered = session_repo.find_by_id(session.id)

        assert recovered is not None
        assert recovered.status == SessionStatus.EXPIRED
