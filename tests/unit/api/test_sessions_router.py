"""
Testes unitários — POST /sessions
Critérios de aceite do Plano 003:
  1. Dados válidos + slot livre   → 201 Created  com status PENDENT_PAYMENT
  2. Dados válidos + slot ocupado → 409 Conflict com mensagem de erro clara
  3. Payload inválido (slot_end antes de slot_start) → 422 Unprocessable Entity
"""
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.api.dependencies import get_create_session_use_case
from src.api.main import app
from src.domain.entities.session import Session, SessionStatus
from src.domain.errors import SlotAlreadyBookedError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _future_slot(days_ahead: int = 7):
    start = datetime.now(tz=timezone.utc) + timedelta(days=days_ahead)
    end = start + timedelta(hours=1)
    return start, end


def _make_session(professor_id, student_id, slot_start, slot_end) -> Session:
    """Cria uma Session real via domínio para usar como retorno do mock."""
    return Session(
        professor_id=professor_id,
        student_id=student_id,
        slot_start=slot_start,
        slot_end=slot_end,
    )


# ---------------------------------------------------------------------------
# Fixture: client com use case mockado
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_use_case():
    return MagicMock()


@pytest.fixture
def test_client(mock_use_case):
    app.dependency_overrides[get_create_session_use_case] = lambda: mock_use_case
    yield TestClient(app)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

class TestPostSessions:
    def test_valid_request_returns_201_with_pendent_payment_status(
        self, test_client: TestClient, mock_use_case: MagicMock
    ):
        """Critério 1: slot livre → 201 Created com PENDENT_PAYMENT."""
        professor_id = uuid4()
        student_id = uuid4()
        slot_start, slot_end = _future_slot()

        session = _make_session(professor_id, student_id, slot_start, slot_end)
        mock_use_case.execute.return_value = session

        payload = {
            "professor_id": str(professor_id),
            "student_id": str(student_id),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == SessionStatus.PENDENT_PAYMENT.value
        assert body["id"] == str(session.id)
        assert body["professor_id"] == str(professor_id)
        assert body["student_id"] == str(student_id)
        assert "lock_expires_at" in body

    def test_slot_already_booked_returns_409_conflict(
        self, test_client: TestClient, mock_use_case: MagicMock
    ):
        """Critério 2: slot ocupado → 409 Conflict com mensagem clara."""
        professor_id = uuid4()
        student_id = uuid4()
        slot_start, slot_end = _future_slot(days_ahead=14)

        mock_use_case.execute.side_effect = SlotAlreadyBookedError(
            professor_id=professor_id,
            slot_start=slot_start,
            slot_end=slot_end,
        )

        payload = {
            "professor_id": str(professor_id),
            "student_id": str(student_id),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 409
        body = response.json()
        assert "detail" in body
        assert len(body["detail"]) > 0

    def test_invalid_payload_slot_end_before_start_returns_422(
        self, test_client: TestClient
    ):
        """Critério 3: slot_end antes de slot_start → 422 Unprocessable Entity."""
        slot_start = datetime.now(tz=timezone.utc) + timedelta(days=7)
        slot_end = slot_start - timedelta(minutes=30)   # inválido

        payload = {
            "professor_id": str(uuid4()),
            "student_id": str(uuid4()),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 422

    def test_missing_required_field_returns_422(self, test_client: TestClient):
        """Campo obrigatório ausente → 422."""
        payload = {
            "professor_id": str(uuid4()),
            # student_id ausente
            "slot_start": (datetime.now(tz=timezone.utc) + timedelta(days=1)).isoformat(),
            "slot_end": (datetime.now(tz=timezone.utc) + timedelta(days=1, hours=1)).isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 422
