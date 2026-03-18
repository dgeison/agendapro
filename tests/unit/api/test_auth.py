"""
Testes unitários — src/api/auth.py
Critérios de aceite do Plano 004:
  1. Token JWT válido + role 'authenticated' → retorna UUID correto do campo 'sub'
  2. Token JWT expirado → lança HTTPException(401)
  3. Token JWT com assinatura inválida → lança HTTPException(401)
  4. Token JWT com role != 'authenticated' (ex: 'anon') → lança HTTPException(403)
  5. Header Authorization ausente → FastAPI retorna 403 via HTTPBearer
"""
import time
from uuid import UUID, uuid4

import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

TEST_SECRET = "test-jwt-secret-for-unit-tests"
ALGORITHM = "HS256"


def _make_token(sub: str, role: str, exp_offset: int = 3600) -> str:
    """Gera um JWT de teste com os campos necessários."""
    payload = {
        "sub": sub,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + exp_offset,
    }
    return jwt.encode(payload, TEST_SECRET, algorithm=ALGORITHM)


def _credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


class TestGetCurrentProfessorId:
    def test_valid_token_returns_uuid(self, monkeypatch):
        """Critério 1: token válido + role 'authenticated' → UUID do sub."""
        import src.api.auth as auth_module
        monkeypatch.setattr(auth_module, "_get_jwt_secret", lambda: TEST_SECRET)

        professor_id = uuid4()
        token = _make_token(str(professor_id), "authenticated")
        credentials = _credentials(token)

        result = auth_module.get_current_professor_id(credentials)

        assert isinstance(result, UUID)
        assert result == professor_id

    def test_expired_token_raises_401(self, monkeypatch):
        """Critério 2: token expirado → HTTPException(401)."""
        import src.api.auth as auth_module
        monkeypatch.setattr(auth_module, "_get_jwt_secret", lambda: TEST_SECRET)

        token = _make_token(str(uuid4()), "authenticated", exp_offset=-10)
        credentials = _credentials(token)

        with pytest.raises(HTTPException) as exc_info:
            auth_module.get_current_professor_id(credentials)

        assert exc_info.value.status_code == 401

    def test_invalid_signature_raises_401(self, monkeypatch):
        """Critério 3: assinatura inválida → HTTPException(401)."""
        import src.api.auth as auth_module
        monkeypatch.setattr(auth_module, "_get_jwt_secret", lambda: TEST_SECRET)

        token = _make_token(str(uuid4()), "authenticated")
        tampered = token[:-5] + "XXXXX"
        credentials = _credentials(tampered)

        with pytest.raises(HTTPException) as exc_info:
            auth_module.get_current_professor_id(credentials)

        assert exc_info.value.status_code == 401

    def test_anon_role_raises_403(self, monkeypatch):
        """Critério 4: role != 'authenticated' → HTTPException(403)."""
        import src.api.auth as auth_module
        monkeypatch.setattr(auth_module, "_get_jwt_secret", lambda: TEST_SECRET)

        token = _make_token(str(uuid4()), "anon")
        credentials = _credentials(token)

        with pytest.raises(HTTPException) as exc_info:
            auth_module.get_current_professor_id(credentials)

        assert exc_info.value.status_code == 403
