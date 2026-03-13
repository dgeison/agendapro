from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Professor:
    name: str
    specialty: str
    hourly_rate: Decimal
    room_link: str
    cancellation_tolerance_minutes: int
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if self.hourly_rate <= Decimal("0"):
            raise ValueError("hourly_rate must be positive")
        if self.cancellation_tolerance_minutes < 0:
            raise ValueError("cancellation_tolerance_minutes must be non-negative")
