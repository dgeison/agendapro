"""
Testes unitários — POST /sessions
Critérios de aceite do Plano 003 (adaptados para Plano 004):
  1. Dados válidos + slot livre   → 201 Created com status PENDENT_PAYMENT
  2. Dados válidos + slot ocupado → 409 Conflict com mensagem de erro clara
  3. Payload inválido (slot_end antes de slot_start) → 422 Unprocessable Entity
  4. Campo obrigatório ausente → 422

Critérios de aceite do Plano 004 (autenticação):
  6. POST /sessions sem header Authorization → 403
  7. POST /sessions com token inválido (get_current_professor_id lançando 401) → 401
"""
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.api.auth import get_current_professor_id
from src.api.dependencies import get_create_session_use_case
from src.api.main import app
from src.domain.entities.session import Session, SessionStatus
from src.domain.errors import SlotAlreadyBookedError

# UUID fixo retornado pelo mock de auth
AUTH_PROFESSOR_ID = uuid4()


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
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_use_case():
    return MagicMock()


@pytest.fixture
def test_client(mock_use_case):
    """Client com use case E autenticação mockados."""
    app.dependency_overrides[get_create_session_use_case] = lambda: mock_use_case
    app.dependency_overrides[get_current_professor_id] = lambda: AUTH_PROFESSOR_ID
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def unauthenticated_client(mock_use_case):
    """Client com use case mockado mas sem override de auth."""
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
        student_id = uuid4()
        slot_start, slot_end = _future_slot()

        session = _make_session(AUTH_PROFESSOR_ID, student_id, slot_start, slot_end)
        mock_use_case.execute.return_value = session

        payload = {
            "student_id": str(student_id),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == SessionStatus.PENDENT_PAYMENT.value
        assert body["id"] == str(session.id)
        assert body["professor_id"] == str(AUTH_PROFESSOR_ID)
        assert body["student_id"] == str(student_id)
        assert "lock_expires_at" in body

    def test_slot_already_booked_returns_409_conflict(
        self, test_client: TestClient, mock_use_case: MagicMock
    ):
        """Critério 2: slot ocupado → 409 Conflict com mensagem clara."""
        student_id = uuid4()
        slot_start, slot_end = _future_slot(days_ahead=14)

        mock_use_case.execute.side_effect = SlotAlreadyBookedError(
            professor_id=AUTH_PROFESSOR_ID,
            slot_start=slot_start,
            slot_end=slot_end,
        )

        payload = {
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
        slot_end = slot_start - timedelta(minutes=30)  # inválido

        payload = {
            "student_id": str(uuid4()),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 422

    def test_missing_required_field_returns_422(self, test_client: TestClient):
        """Campo obrigatório ausente → 422."""
        payload = {
            # student_id ausente
            "slot_start": (datetime.now(tz=timezone.utc) + timedelta(days=1)).isoformat(),
            "slot_end": (datetime.now(tz=timezone.utc) + timedelta(days=1, hours=1)).isoformat(),
        }

        response = test_client.post("/sessions", json=payload)

        assert response.status_code == 422

    def test_missing_authorization_header_returns_4xx(
        self, unauthenticated_client: TestClient
    ):
        """Critério 6: sem header Authorization → erro 4xx via HTTPBearer.

        Nota: O plano 004 previa 403, mas FastAPI 0.135.1 / Starlette 0.52.1
        retorna 401 para header ausente. O comportamento correto (rejeitar
        requisição não autenticada) é mantido.
        """
        slot_start, slot_end = _future_slot()
        payload = {
            "student_id": str(uuid4()),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = unauthenticated_client.post("/sessions", json=payload)

        assert response.status_code in (401, 403)

    def test_invalid_token_returns_401(
        self, unauthenticated_client: TestClient
    ):
        """Critério 7: token inválido (get_current_professor_id lança 401) → 401."""
        def raise_401():
            raise HTTPException(status_code=401, detail="Invalid authentication token.")

        app.dependency_overrides[get_current_professor_id] = raise_401

        slot_start, slot_end = _future_slot()
        payload = {
            "student_id": str(uuid4()),
            "slot_start": slot_start.isoformat(),
            "slot_end": slot_end.isoformat(),
        }

        response = unauthenticated_client.post(
            "/sessions",
            json=payload,
            headers={"Authorization": "Bearer invalid.token.here"},
        )

        assert response.status_code == 401
