from __future__ import annotations

from decimal import Decimal
from datetime import date
from typing import Iterable

from .exceptions import InvoiceValidationError, ValidationError
from .models import Invoice, InvoiceStatus

SUPPORTED_CURRENCIES = {"EUR", "USD", "GBP", "CHF"}
TOLERANCE = Decimal("0.01")


def validate_required_fields(invoice: Invoice) -> list[ValidationError]:
    """Validate mandatory invoice attributes."""
    errors: list[ValidationError] = []
    for field_name, value in [
        ("company_code", invoice.company_code),
        ("vendor_id", invoice.vendor_id),
        ("vendor_name", invoice.vendor_name),
        ("invoice_number", invoice.invoice_number),
    ]:
        if not value or not str(value).strip():
            errors.append(
                ValidationError(field_name, "REQUIRED_FIELD", f"{field_name} is required.")
            )
    if not invoice.invoice_date:
        errors.append(ValidationError("invoice_date", "REQUIRED_FIELD", "Invoice date is required."))
    return errors


def validate_currency(invoice: Invoice) -> list[ValidationError]:
    """Validate allowed currency codes."""
    if invoice.currency_code.upper() not in SUPPORTED_CURRENCIES:
        return [
            ValidationError(
                "currency_code",
                "INVALID_CURRENCY",
                "Currency must be one of EUR, USD, GBP, CHF.",
            )
        ]
    return []


def validate_amounts(invoice: Invoice) -> list[ValidationError]:
    """Validate basic financial amount rules."""
    errors: list[ValidationError] = []
    if invoice.gross_amount <= Decimal("0"):
        errors.append(
            ValidationError(
                "gross_amount",
                "INVALID_AMOUNT",
                "Gross amount must be greater than zero.",
            )
        )
    if invoice.tax_amount < Decimal("0"):
        errors.append(
            ValidationError("tax_amount", "INVALID_AMOUNT", "Tax amount cannot be negative.")
        )
    if invoice.net_amount < Decimal("0"):
        errors.append(
            ValidationError("net_amount", "INVALID_AMOUNT", "Net amount cannot be negative.")
        )
    return errors


def validate_amount_reconciliation(invoice: Invoice) -> list[ValidationError]:
    """Ensure gross, net, and tax reconcile."""
    if abs((invoice.net_amount + invoice.tax_amount) - invoice.gross_amount) > TOLERANCE:
        return [
            ValidationError(
                "gross_amount",
                "RECONCILIATION_ERROR",
                "Net plus tax must equal gross amount within a tolerance of 0.01.",
            )
        ]
    return []


def validate_duplicate_invoice(invoice: Invoice, existing_invoices: Iterable[Invoice]) -> list[ValidationError]:
    """Ensure vendor and invoice number are unique."""
    for existing in existing_invoices:
        if existing.vendor_id == invoice.vendor_id and existing.invoice_number == invoice.invoice_number:
            return [
                ValidationError(
                    "vendor_id",
                    "DUPLICATE_INVOICE",
                    "Vendor ID plus invoice number must be unique.",
                )
            ]
    return []


def validate_invoice(invoice: Invoice, existing_invoices: Iterable[Invoice]) -> list[ValidationError]:
    """Run all invoice validation rules."""
    errors = []
    errors.extend(validate_required_fields(invoice))
    errors.extend(validate_currency(invoice))
    errors.extend(validate_amounts(invoice))
    errors.extend(validate_amount_reconciliation(invoice))
    errors.extend(validate_duplicate_invoice(invoice, existing_invoices))
    return errors


def ensure_valid_invoice(invoice: Invoice, existing_invoices: Iterable[Invoice]) -> None:
    """Raise a documented exception if the invoice is invalid."""
    errors = validate_invoice(invoice, existing_invoices)
    if errors:
        raise InvoiceValidationError(errors)
