import pytest
from dotenv import load_dotenv

from src.infrastructure.database import get_supabase_client
from src.infrastructure.repositories.supabase_professor_repository import (
    SupabaseProfessorRepository,
)
from src.infrastructure.repositories.supabase_session_repository import (
    SupabaseSessionRepository,
)
from src.infrastructure.repositories.supabase_student_repository import (
    SupabaseStudentRepository,
)

load_dotenv()


@pytest.fixture(scope="session")
def supabase_client():
    return get_supabase_client()


@pytest.fixture(scope="session")
def professor_repo(supabase_client):
    return SupabaseProfessorRepository(supabase_client)


@pytest.fixture(scope="session")
def student_repo(supabase_client):
    return SupabaseStudentRepository(supabase_client)


@pytest.fixture(scope="session")
def session_repo(supabase_client):
    return SupabaseSessionRepository(supabase_client)
