"""
Testes unitários — CreateProfessorUseCase
Critérios de aceite do Plano 006:
  1. Professor inexistente → cria e salva com o professor_id correto (UUID do JWT)
  2. Professor já existente → lança ProfessorAlreadyExistsError
"""
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.domain.errors import ProfessorAlreadyExistsError


def _valid_input(professor_id):
    from src.application.use_cases.create_professor import CreateProfessorInput
    return CreateProfessorInput(
        professor_id=professor_id,
        name="Ana Lima",
        specialty="Química",
        hourly_rate=Decimal("120.00"),
        room_link="https://meet.google.com/ana-lima",
        cancellation_tolerance_minutes=30,
    )


class TestCreateProfessorUseCase:
    def test_creates_and_saves_professor_with_jwt_id(self):
        """Critério 1: professor inexistente → cria e salva com professor_id correto."""
        from src.application.use_cases.create_professor import CreateProfessorUseCase

        professor_id = uuid4()
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = None

        use_case = CreateProfessorUseCase(professor_repository=mock_repo)
        result = use_case.execute(_valid_input(professor_id))

        assert result.id == professor_id
        assert result.name == "Ana Lima"
        mock_repo.find_by_id.assert_called_once_with(professor_id)
        mock_repo.save.assert_called_once()
        saved = mock_repo.save.call_args[0][0]
        assert saved.id == professor_id

    def test_raises_already_exists_when_professor_found(self):
        """Critério 2: professor já existente → ProfessorAlreadyExistsError."""
        from src.application.use_cases.create_professor import CreateProfessorUseCase
        from src.domain.entities.professor import Professor

        professor_id = uuid4()
        existing = Professor(
            id=professor_id,
            name="Ana Lima",
            specialty="Química",
            hourly_rate=Decimal("120.00"),
            room_link="https://meet.google.com/ana-lima",
            cancellation_tolerance_minutes=30,
        )
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = existing

        use_case = CreateProfessorUseCase(professor_repository=mock_repo)

        with pytest.raises(ProfessorAlreadyExistsError):
            use_case.execute(_valid_input(professor_id))

        mock_repo.save.assert_not_called()
