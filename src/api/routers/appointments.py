import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_create_appointment_use_case
from src.api.schemas.appointment_schemas import AppointmentCreateRequest, AppointmentResponse
from src.application.use_cases.create_appointment import CreateAppointmentUseCase
from src.domain.errors import SlotAlreadyLockedError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar agendamento",
    description="Cria um novo agendamento e inicia o lock do slot para o professor.",
)
def create_appointment(
    body: AppointmentCreateRequest,
    use_case: Annotated[CreateAppointmentUseCase, Depends(get_create_appointment_use_case)],
) -> AppointmentResponse:
    try:
        result = use_case.execute(
            aluno_id=body.aluno_id,
            professor_id=body.professor_id,
            start_time=body.start_time,
            end_time=body.end_time,
        )
    except SlotAlreadyLockedError as exc:
        logger.warning("slot_locked_at_api", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return AppointmentResponse(
        id=result["id"],
        professor_id=result["professor_id"],
        aluno_id=result["aluno_id"],
        start_time=result["start_time"],
        end_time=result["end_time"],
    )
