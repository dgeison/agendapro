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
