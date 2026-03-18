class ProfessorAlreadyExistsError(Exception):
    """Raised when trying to create a professor profile that already exists."""

    def __init__(self, professor_id):
        super().__init__(f"Professor with id {professor_id} already exists.")
        self.professor_id = professor_id


class ProfessorNotFoundError(Exception):
    """Raised when a professor profile is not found."""

    def __init__(self, professor_id):
        super().__init__(f"Professor with id {professor_id} not found.")
        self.professor_id = professor_id


class SlotAlreadyBookedError(Exception):
    """Raised when a session slot is already occupied by another active session."""

    def __init__(self, professor_id, slot_start, slot_end):
        super().__init__(
            f"Slot from {slot_start.isoformat()} to {slot_end.isoformat()} "
            f"is already booked for professor {professor_id}"
        )
        self.professor_id = professor_id
        self.slot_start = slot_start
        self.slot_end = slot_end


class GatewayConnectionError(Exception):
    """Raised when a payment gateway call fails due to network or API error."""

    def __init__(self, gateway: str, detail: str):
        super().__init__(f"Gateway '{gateway}' error: {detail}")
        self.gateway = gateway
        self.detail = detail


class SlotAlreadyLockedError(Exception):
    """Raised when trying to lock an appointment slot that already has an active lock."""

    def __init__(self, professor_id, start_time, end_time):
        start_str = start_time.isoformat() if hasattr(start_time, "isoformat") else start_time
        end_str = end_time.isoformat() if hasattr(end_time, "isoformat") else end_time
        super().__init__(
            f"Slot from {start_str} to {end_str} "
            f"is already locked for professor {professor_id}"
        )
        self.professor_id = professor_id
        self.start_time = start_time
        self.end_time = end_time
