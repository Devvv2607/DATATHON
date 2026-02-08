"""Custom exceptions and error handling for the simulator."""

from typing import Optional, List
from .types import ErrorResponse, ValidationFailure


class SimulatorException(Exception):
    """Base exception for simulator errors."""

    pass


class ValidationException(SimulatorException):
    """Raised when scenario validation fails."""

    def __init__(
        self,
        message: str,
        failures: Optional[List[ValidationFailure]] = None,
    ):
        """
        Initialize validation exception.
        
        Args:
            message: Error message
            failures: List of validation failures
        """
        super().__init__(message)
        self.failures = failures or []

    def to_error_response(self) -> ErrorResponse:
        """Convert to structured error response."""
        return ErrorResponse(
            error_code="VALIDATION_ERROR",
            error_message=str(self),
            validation_failures=self.failures,
        )


class ExternalSystemException(SimulatorException):
    """Raised when external system query fails."""

    pass


class DataQualityException(SimulatorException):
    """Raised when data quality issues are detected."""

    pass
