from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Student:
    name: str
    whatsapp: str
    email: Optional[str] = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.whatsapp:
            raise ValueError("whatsapp must not be empty")
