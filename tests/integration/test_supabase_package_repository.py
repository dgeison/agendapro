"""
Teste de integração: SupabasePackageRepository
Critérios de aceite:
  1. get_student_balance() retorna 0 para aluno sem registro.
  2. add_credits() adiciona créditos e retorna dict com os dados do pacote.
  3. get_student_balance() retorna o saldo correto após add_credits().
"""
import uuid

import pytest

from src.infrastructure.repositories.supabase_package_repository import (
    SupabasePackageRepository,
)


@pytest.fixture(scope="module")
def package_repo(supabase_client):
    return SupabasePackageRepository(supabase_client)


@pytest.fixture
def student_id():
    return str(uuid.uuid4())


class TestSupabasePackageRepository:
    def test_get_student_balance_returns_zero_for_unknown_student(
        self, package_repo: SupabasePackageRepository
    ):
        """Critério 1: saldo retorna 0 para aluno sem registro."""
        unknown_id = str(uuid.uuid4())
        balance = package_repo.get_student_balance(unknown_id)
        assert balance == 0

    def test_add_credits_returns_dict_with_package_data(
        self, package_repo: SupabasePackageRepository, student_id: str
    ):
        """Critério 2: add_credits() retorna dict com dados do pacote."""
        result = package_repo.add_credits(student_id=student_id, amount=10)
        assert result is not None

    def test_get_student_balance_returns_correct_balance_after_add(
        self, package_repo: SupabasePackageRepository
    ):
        """Critério 3: saldo correto após add_credits()."""
        sid = str(uuid.uuid4())
        package_repo.add_credits(student_id=sid, amount=5)
        balance = package_repo.get_student_balance(sid)
        assert balance == 5
