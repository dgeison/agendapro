from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator


class CreateSessionRequest(BaseModel):
    student_id: UUID
    slot_start: datetime
    slot_end: datetime

    @model_validator(mode="after")
    def slot_end_must_be_after_slot_start(self) -> "CreateSessionRequest":
        if self.slot_end <= self.slot_start:
            raise ValueError("slot_end must be after slot_start")
        return self


class SessionResponse(BaseModel):
    id: UUID
    professor_id: UUID
    student_id: UUID
    slot_start: datetime
    slot_end: datetime
    status: str
    lock_expires_at: datetime
