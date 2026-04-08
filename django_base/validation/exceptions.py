class APIValidationError(Exception):
    """Raised when request or payload validation fails; maps to a JSON error response."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
