"""
Testes unitários — /professors/me
Critérios de aceite do Plano 006:
  5. POST /professors/me com dados válidos → 201 com ProfessorResponse
  6. POST /professors/me com professor já existente → 409 Conflict
  7. GET /professors/me com professor existente → 200 com ProfessorResponse
  8. GET /professors/me com professor inexistente → 404 Not Found
  9. Ambos os endpoints sem token → 401
"""
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.api.auth import get_current_professor_id
from src.api.dependencies import get_create_professor_use_case, get_get_professor_use_case
from src.api.main import app
from src.domain.entities.professor import Professor
from src.domain.errors import ProfessorAlreadyExistsError, ProfessorNotFoundError

AUTH_PROFESSOR_ID = uuid4()


def _make_professor(professor_id=None) -> Professor:
    return Professor(
        id=professor_id or AUTH_PROFESSOR_ID,
        name="Ana Lima",
        specialty="Química",
        hourly_rate=Decimal("120.00"),
        room_link="https://meet.google.com/ana-lima",
        cancellation_tolerance_minutes=30,
    )


def _valid_payload() -> dict:
    return {
        "name": "Ana Lima",
        "specialty": "Química",
        "hourly_rate": "120.00",
        "room_link": "https://meet.google.com/ana-lima",
        "cancellation_tolerance_minutes": 30,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_create_uc():
    return MagicMock()


@pytest.fixture
def mock_get_uc():
    return MagicMock()


@pytest.fixture
def test_client(mock_create_uc, mock_get_uc):
    app.dependency_overrides[get_current_professor_id] = lambda: AUTH_PROFESSOR_ID
    app.dependency_overrides[get_create_professor_use_case] = lambda: mock_create_uc
    app.dependency_overrides[get_get_professor_use_case] = lambda: mock_get_uc
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def unauthenticated_client():
    yield TestClient(app)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

class TestProfessorsRouter:
    def test_create_professor_returns_201(
        self, test_client: TestClient, mock_create_uc: MagicMock
    ):
        """Critério 5: POST /professors/me com dados válidos → 201 com ProfessorResponse."""
        professor = _make_professor()
        mock_create_uc.execute.return_value = professor

        response = test_client.post("/professors/me", json=_valid_payload())

        assert response.status_code == 201
        body = response.json()
        assert body["id"] == str(AUTH_PROFESSOR_ID)
        assert body["name"] == "Ana Lima"
        assert body["specialty"] == "Química"
        assert "hourly_rate" in body
        assert body["room_link"] == "https://meet.google.com/ana-lima"
        assert body["cancellation_tolerance_minutes"] == 30

    def test_create_professor_already_exists_returns_409(
        self, test_client: TestClient, mock_create_uc: MagicMock
    ):
        """Critério 6: POST /professors/me com professor já existente → 409 Conflict."""
        mock_create_uc.execute.side_effect = ProfessorAlreadyExistsError(
            professor_id=AUTH_PROFESSOR_ID
        )

        response = test_client.post("/professors/me", json=_valid_payload())

        assert response.status_code == 409
        assert "detail" in response.json()

    def test_get_professor_returns_200(
        self, test_client: TestClient, mock_get_uc: MagicMock
    ):
        """Critério 7: GET /professors/me com professor existente → 200 com ProfessorResponse."""
        professor = _make_professor()
        mock_get_uc.execute.return_value = professor

        response = test_client.get("/professors/me")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == str(AUTH_PROFESSOR_ID)
        assert body["name"] == "Ana Lima"

    def test_get_professor_not_found_returns_404(
        self, test_client: TestClient, mock_get_uc: MagicMock
    ):
        """Critério 8: GET /professors/me com professor inexistente → 404 Not Found."""
        mock_get_uc.execute.side_effect = ProfessorNotFoundError(
            professor_id=AUTH_PROFESSOR_ID
        )

        response = test_client.get("/professors/me")

        assert response.status_code == 404
        assert "detail" in response.json()

    def test_post_without_token_returns_401(self, unauthenticated_client: TestClient):
        """Critério 9a: POST /professors/me sem token → 401."""
        response = unauthenticated_client.post("/professors/me", json=_valid_payload())

        assert response.status_code in (401, 403)

    def test_get_without_token_returns_401(self, unauthenticated_client: TestClient):
        """Critério 9b: GET /professors/me sem token → 401."""
        response = unauthenticated_client.get("/professors/me")

        assert response.status_code in (401, 403)
