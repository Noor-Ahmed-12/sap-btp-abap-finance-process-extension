from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum


class InvoiceStatus(str, Enum):
    """Supported invoice workflow statuses."""

    NEW = "NEW"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    POSTED = "POSTED"


@dataclass(slots=True)
class Invoice:
    """Represents a finance invoice in the local demonstration workflow."""

    invoice_uuid: str
    company_code: str
    vendor_id: str
    vendor_name: str
    invoice_number: str
    invoice_date: date
    currency_code: str
    gross_amount: Decimal
    tax_amount: Decimal
    net_amount: Decimal
    cost_center: str = ""
    description: str = ""
    processing_status: InvoiceStatus = InvoiceStatus.NEW
    rejection_reason: str | None = None
    error_message: str | None = None
    created_by: str = "system"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_changed_by: str = "system"
    last_changed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the invoice."""
        return {
            "invoice_uuid": self.invoice_uuid,
            "company_code": self.company_code,
            "vendor_id": self.vendor_id,
            "vendor_name": self.vendor_name,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date.isoformat(),
            "currency_code": self.currency_code,
            "gross_amount": str(self.gross_amount),
            "tax_amount": str(self.tax_amount),
            "net_amount": str(self.net_amount),
            "cost_center": self.cost_center,
            "description": self.description,
            "processing_status": self.processing_status.value,
            "rejection_reason": self.rejection_reason,
            "error_message": self.error_message,
            "created_by": self.created_by,
            "created_at": self._format_datetime(self.created_at),
            "last_changed_by": self.last_changed_by,
            "last_changed_at": self._format_datetime(self.last_changed_at),
        }

    @staticmethod
    def _format_datetime(value: datetime) -> str:
        return (
            value.astimezone(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
