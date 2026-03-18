from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from uuid import UUID, uuid4


class SessionStatus(str, Enum):
    PENDENT_PAYMENT = "PENDENT_PAYMENT"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


@dataclass
class Session:
    professor_id: UUID
    student_id: UUID
    slot_start: datetime
    slot_end: datetime
    id: UUID = field(default_factory=uuid4)
    status: SessionStatus = field(default=SessionStatus.PENDENT_PAYMENT, init=False)
    lock_expires_at: datetime = field(init=False)

    def __post_init__(self):
        if self.slot_end <= self.slot_start:
            raise ValueError("slot_end must be after slot_start")
        self.lock_expires_at = datetime.now(tz=timezone.utc) + timedelta(minutes=10)

    def confirm(self):
        if self.status != SessionStatus.PENDENT_PAYMENT:
            raise ValueError(f"Cannot confirm session with status {self.status}")
        self.status = SessionStatus.CONFIRMED

    def cancel(self):
        self.status = SessionStatus.CANCELLED

    def expire(self) -> None:
        """Expira o lock. Só pode ser chamado se lock_expires_at < now() e status == PENDENT_PAYMENT."""
        if self.status != SessionStatus.PENDENT_PAYMENT:
            raise ValueError("Only PENDENT_PAYMENT sessions can be expired.")
        if self.lock_expires_at is None or self.lock_expires_at > datetime.now(tz=timezone.utc):
            raise ValueError("Lock has not expired yet.")
        self.status = SessionStatus.EXPIRED
