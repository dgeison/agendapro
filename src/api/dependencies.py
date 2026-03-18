from typing import Annotated

from fastapi import Depends
from supabase import Client

from src.application.use_cases.create_appointment import CreateAppointmentUseCase
from src.application.use_cases.create_professor import CreateProfessorUseCase
from src.application.use_cases.create_session import CreateSessionUseCase
from src.application.use_cases.get_professor import GetProfessorUseCase
from src.infrastructure.database import get_supabase_client
from src.infrastructure.repositories.supabase_appointment_repository import (
    SupabaseAppointmentRepository,
)
from src.infrastructure.repositories.supabase_professor_repository import (
    SupabaseProfessorRepository,
)
from src.infrastructure.repositories.supabase_session_repository import (
    SupabaseSessionRepository,
)


def get_client() -> Client:
    return get_supabase_client()


def get_session_repository(
    client: Annotated[Client, Depends(get_client)],
) -> SupabaseSessionRepository:
    return SupabaseSessionRepository(client)


def get_professor_repository(
    client: Annotated[Client, Depends(get_client)],
) -> SupabaseProfessorRepository:
    return SupabaseProfessorRepository(client)


def get_create_session_use_case(
    session_repository: Annotated[SupabaseSessionRepository, Depends(get_session_repository)],
) -> CreateSessionUseCase:
    return CreateSessionUseCase(session_repository=session_repository)


def get_create_professor_use_case(
    professor_repository: Annotated[SupabaseProfessorRepository, Depends(get_professor_repository)],
) -> CreateProfessorUseCase:
    return CreateProfessorUseCase(professor_repository=professor_repository)


def get_get_professor_use_case(
    professor_repository: Annotated[SupabaseProfessorRepository, Depends(get_professor_repository)],
) -> GetProfessorUseCase:
    return GetProfessorUseCase(professor_repository=professor_repository)


def get_appointment_repository(
    client: Annotated[Client, Depends(get_client)],
) -> SupabaseAppointmentRepository:
    return SupabaseAppointmentRepository(client)


def get_create_appointment_use_case(
    appointment_repository: Annotated[SupabaseAppointmentRepository, Depends(get_appointment_repository)],
) -> CreateAppointmentUseCase:
    return CreateAppointmentUseCase(appointment_repository=appointment_repository)
