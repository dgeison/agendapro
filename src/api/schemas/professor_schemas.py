from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CreateProfessorRequest(BaseModel):
    name: str
    specialty: str
    hourly_rate: Decimal
    room_link: str
    cancellation_tolerance_minutes: int


class ProfessorResponse(BaseModel):
    id: UUID
    name: str
    specialty: str
    hourly_rate: Decimal
    room_link: str
    cancellation_tolerance_minutes: int
