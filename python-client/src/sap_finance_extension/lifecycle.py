from __future__ import annotations

from datetime import datetime

from .exceptions import InvalidStatusTransitionError
from .models import Invoice, InvoiceStatus


class InvoiceLifecycleService:
    """Manage invoice workflow transitions and metadata updates."""

    def validate(self, invoice: Invoice) -> Invoice:
        if invoice.processing_status != InvoiceStatus.NEW:
            raise InvalidStatusTransitionError("Only a NEW invoice can be validated.")
        invoice.processing_status = InvoiceStatus.VALIDATED
        invoice.last_changed_at = datetime.utcnow()
        return invoice

    def approve(self, invoice: Invoice) -> Invoice:
        if invoice.processing_status != InvoiceStatus.VALIDATED:
            raise InvalidStatusTransitionError("Only a VALIDATED invoice can be approved.")
        invoice.processing_status = InvoiceStatus.APPROVED
        invoice.last_changed_at = datetime.utcnow()
        return invoice

    def reject(self, invoice: Invoice, reason: str) -> Invoice:
        if invoice.processing_status not in {InvoiceStatus.NEW, InvoiceStatus.VALIDATED}:
            raise InvalidStatusTransitionError("Only NEW or VALIDATED invoices can be rejected.")
        if not reason or not reason.strip():
            raise ValueError("A rejection reason is required.")
        invoice.processing_status = InvoiceStatus.REJECTED
        invoice.rejection_reason = reason
        invoice.last_changed_at = datetime.utcnow()
        return invoice

    def reopen(self, invoice: Invoice) -> Invoice:
        if invoice.processing_status != InvoiceStatus.REJECTED:
            raise InvalidStatusTransitionError("Only a REJECTED invoice can be reopened.")
        invoice.processing_status = InvoiceStatus.NEW
        invoice.rejection_reason = None
        invoice.last_changed_at = datetime.utcnow()
        return invoice

    def post(self, invoice: Invoice) -> Invoice:
        if invoice.processing_status != InvoiceStatus.APPROVED:
            raise InvalidStatusTransitionError("Only an APPROVED invoice can be posted.")
        invoice.processing_status = InvoiceStatus.POSTED
        invoice.last_changed_at = datetime.utcnow()
        return invoice
