class ProcessingError(Exception):
    """Base exception for validation errors."""
    pass


class InvalidRecordError(ProcessingError):
    """Raised when a specific data payload breaks schema invariants."""
    def __init__(self, record_id: str, reason: str):
        self.record_id = record_id
        self.reason = reason
        super().__init__(f"Record '{record_id}' failed validation: {reason}")