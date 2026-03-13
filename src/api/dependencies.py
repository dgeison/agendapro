from typing import Annotated

from fastapi import Depends
from supabase import Client

from src.application.use_cases.create_session import CreateSessionUseCase
from src.infrastructure.database import get_supabase_client
from src.infrastructure.repositories.supabase_session_repository import (
    SupabaseSessionRepository,
)


def get_client() -> Client:
    return get_supabase_client()


def get_session_repository(
    client: Annotated[Client, Depends(get_client)],
) -> SupabaseSessionRepository:
    return SupabaseSessionRepository(client)


def get_create_session_use_case(
    session_repository: Annotated[SupabaseSessionRepository, Depends(get_session_repository)],
) -> CreateSessionUseCase:
    return CreateSessionUseCase(session_repository=session_repository)
