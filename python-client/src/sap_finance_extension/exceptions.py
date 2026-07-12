from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ValidationError:
    """Structured validation error for invoice checks."""

    field: str
    code: str
    message: str


class InvoiceValidationError(Exception):
    """Raised when invoice validation fails."""

    def __init__(self, errors: list[ValidationError]):
        self.errors = errors
        message = "; ".join(f"{error.field}:{error.code}:{error.message}" for error in errors)
        super().__init__(message)


class InvalidStatusTransitionError(Exception):
    """Raised when an invalid workflow transition is attempted."""


class RepositoryError(Exception):
    """Raised when the repository cannot complete a requested operation."""


class SAPClientError(Exception):
    """Raised when the SAP client request fails."""
