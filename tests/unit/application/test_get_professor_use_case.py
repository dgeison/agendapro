"""
Testes unitários — GetProfessorUseCase
Critérios de aceite do Plano 006:
  3. Professor existente → retorna Professor correto
  4. Professor inexistente → lança ProfessorNotFoundError
"""
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.domain.errors import ProfessorNotFoundError


class TestGetProfessorUseCase:
    def test_returns_professor_when_found(self):
        """Critério 3: professor existente → retorna Professor correto."""
        from src.application.use_cases.get_professor import GetProfessorUseCase
        from src.domain.entities.professor import Professor

        professor_id = uuid4()
        existing = Professor(
            id=professor_id,
            name="Carlos Souza",
            specialty="Física",
            hourly_rate=Decimal("200.00"),
            room_link="https://meet.google.com/carlos",
            cancellation_tolerance_minutes=15,
        )
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = existing

        use_case = GetProfessorUseCase(professor_repository=mock_repo)
        result = use_case.execute(professor_id)

        assert result == existing
        assert result.id == professor_id
        mock_repo.find_by_id.assert_called_once_with(professor_id)

    def test_raises_not_found_when_professor_missing(self):
        """Critério 4: professor inexistente → ProfessorNotFoundError."""
        from src.application.use_cases.get_professor import GetProfessorUseCase

        professor_id = uuid4()
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = None

        use_case = GetProfessorUseCase(professor_repository=mock_repo)

        with pytest.raises(ProfessorNotFoundError):
            use_case.execute(professor_id)
