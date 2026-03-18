"""
Testes unitários — POST /appointments
Critérios de aceite do Plano 009:
  1. Dados válidos + slot livre    → 201 Created com contrato JSON correto
  2. Slot ocupado (SlotAlreadyLockedError) → 409 Conflict
  3. Payload inválido (end_time antes de start_time) → 422 Unprocessable Entity
"""
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.api.dependencies import get_create_appointment_use_case
from src.api.main import app
from src.domain.errors import SlotAlreadyLockedError


def _future_slot(days_ahead: int = 7):
    start = datetime.now(tz=timezone.utc) + timedelta(days=days_ahead)
    end = start + timedelta(hours=1)
    return start, end


@pytest.fixture
def mock_use_case():
    return MagicMock()


@pytest.fixture
def test_client(mock_use_case):
    app.dependency_overrides[get_create_appointment_use_case] = lambda: mock_use_case
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestPostAppointments:
    def test_post_appointments_success(
        self, test_client: TestClient, mock_use_case: MagicMock
    ):
        """Critério 1: slot livre → 201 Created com contrato JSON."""
        professor_id = str(uuid4())
        aluno_id = str(uuid4())
        start, end = _future_slot()

        mock_use_case.execute.return_value = {
            "id": str(uuid4()),
            "professor_id": professor_id,
            "aluno_id": aluno_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }

        payload = {
            "professor_id": professor_id,
            "aluno_id": aluno_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }

        response = test_client.post("/appointments", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert body["professor_id"] == professor_id
        assert body["aluno_id"] == aluno_id

    def test_post_appointments_overlap_conflict(
        self, test_client: TestClient, mock_use_case: MagicMock
    ):
        """Critério 2: SlotAlreadyLockedError → 409 Conflict."""
        professor_id = str(uuid4())
        start, end = _future_slot(days_ahead=14)

        mock_use_case.execute.side_effect = SlotAlreadyLockedError(
            professor_id=professor_id,
            start_time=start,
            end_time=end,
        )

        payload = {
            "professor_id": professor_id,
            "aluno_id": str(uuid4()),
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }

        response = test_client.post("/appointments", json=payload)

        assert response.status_code == 409
        body = response.json()
        assert "detail" in body
        assert len(body["detail"]) > 0

    def test_post_appointments_invalid_schema(self, test_client: TestClient):
        """Critério 3: end_time antes de start_time → 422 Unprocessable Entity."""
        start = datetime.now(tz=timezone.utc) + timedelta(days=7)
        end = start - timedelta(hours=1)  # inválido

        payload = {
            "professor_id": str(uuid4()),
            "aluno_id": str(uuid4()),
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        }

        response = test_client.post("/appointments", json=payload)

        assert response.status_code == 422
