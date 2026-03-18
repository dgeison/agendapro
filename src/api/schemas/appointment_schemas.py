from datetime import datetime

from pydantic import BaseModel, model_validator


class AppointmentCreateRequest(BaseModel):
    aluno_id: str
    professor_id: str
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def end_time_must_be_after_start_time(self) -> "AppointmentCreateRequest":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class AppointmentResponse(BaseModel):
    id: str
    professor_id: str
    aluno_id: str
    start_time: str
    end_time: str
