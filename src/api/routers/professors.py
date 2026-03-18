import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.auth import get_current_professor_id
from src.api.dependencies import get_create_professor_use_case, get_get_professor_use_case
from src.api.schemas.professor_schemas import CreateProfessorRequest, ProfessorResponse
from src.application.use_cases.create_professor import CreateProfessorInput, CreateProfessorUseCase
from src.application.use_cases.get_professor import GetProfessorUseCase
from src.domain.errors import ProfessorAlreadyExistsError, ProfessorNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/professors", tags=["professors"])


@router.post(
    "/me",
    response_model=ProfessorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar perfil do professor",
    description="Cria o perfil de negócio do professor autenticado.",
)
def create_professor(
    body: CreateProfessorRequest,
    professor_id: Annotated[UUID, Depends(get_current_professor_id)],
    use_case: Annotated[CreateProfessorUseCase, Depends(get_create_professor_use_case)],
) -> ProfessorResponse:
    try:
        professor = use_case.execute(
            CreateProfessorInput(
                professor_id=professor_id,
                name=body.name,
                specialty=body.specialty,
                hourly_rate=body.hourly_rate,
                room_link=body.room_link,
                cancellation_tolerance_minutes=body.cancellation_tolerance_minutes,
            )
        )
    except ProfessorAlreadyExistsError as exc:
        logger.warning("professor_already_exists_at_api", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return ProfessorResponse(
        id=professor.id,
        name=professor.name,
        specialty=professor.specialty,
        hourly_rate=professor.hourly_rate,
        room_link=professor.room_link,
        cancellation_tolerance_minutes=professor.cancellation_tolerance_minutes,
    )


@router.get(
    "/me",
    response_model=ProfessorResponse,
    status_code=status.HTTP_200_OK,
    summary="Ler perfil do professor",
    description="Retorna o perfil de negócio do professor autenticado.",
)
def get_professor(
    professor_id: Annotated[UUID, Depends(get_current_professor_id)],
    use_case: Annotated[GetProfessorUseCase, Depends(get_get_professor_use_case)],
) -> ProfessorResponse:
    try:
        professor = use_case.execute(professor_id)
    except ProfessorNotFoundError as exc:
        logger.warning("professor_not_found_at_api", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return ProfessorResponse(
        id=professor.id,
        name=professor.name,
        specialty=professor.specialty,
        hourly_rate=professor.hourly_rate,
        room_link=professor.room_link,
        cancellation_tolerance_minutes=professor.cancellation_tolerance_minutes,
    )
