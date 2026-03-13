import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_create_session_use_case
from src.api.schemas.session_schemas import CreateSessionRequest, SessionResponse
from src.application.use_cases.create_session import CreateSessionInput, CreateSessionUseCase
from src.domain.errors import SlotAlreadyBookedError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar agendamento",
    description="Cria uma nova sessão para o professor e aluno no slot informado.",
)
def create_session(
    body: CreateSessionRequest,
    use_case: Annotated[CreateSessionUseCase, Depends(get_create_session_use_case)],
) -> SessionResponse:
    try:
        session = use_case.execute(
            CreateSessionInput(
                professor_id=body.professor_id,
                student_id=body.student_id,
                slot_start=body.slot_start,
                slot_end=body.slot_end,
            )
        )
    except SlotAlreadyBookedError as exc:
        logger.warning("slot_conflict_at_api", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return SessionResponse(
        id=session.id,
        professor_id=session.professor_id,
        student_id=session.student_id,
        slot_start=session.slot_start,
        slot_end=session.slot_end,
        status=session.status.value,
        lock_expires_at=session.lock_expires_at,
    )
