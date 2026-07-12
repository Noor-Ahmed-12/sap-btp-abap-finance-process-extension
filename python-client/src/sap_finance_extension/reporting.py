from __future__ import annotations

from collections import Counter
from decimal import Decimal
from typing import Iterable

from .models import Invoice, InvoiceStatus


def build_summary(invoices: Iterable[Invoice]) -> dict[str, object]:
    """Create a serializable summary dictionary from invoices."""
    invoices = list(invoices)
    counts = Counter(invoice.processing_status.value for invoice in invoices)
    gross_by_currency: dict[str, Decimal] = {}
    approved_by_currency: dict[str, Decimal] = {}
    posted_by_currency: dict[str, Decimal] = {}
    for invoice in invoices:
        currency = invoice.currency_code
        gross_by_currency[currency] = gross_by_currency.get(currency, Decimal("0")) + invoice.gross_amount
        if invoice.processing_status == InvoiceStatus.APPROVED:
            approved_by_currency[currency] = approved_by_currency.get(currency, Decimal("0")) + invoice.gross_amount
        if invoice.processing_status == InvoiceStatus.POSTED:
            posted_by_currency[currency] = posted_by_currency.get(currency, Decimal("0")) + invoice.gross_amount

    return {
        "total_invoice_count": len(invoices),
        "count_by_status": {key: counts.get(key, 0) for key in InvoiceStatus._value2member_map_},
        "gross_amount_by_currency": {key: str(value) for key, value in sorted(gross_by_currency.items())},
        "approved_gross_amount_by_currency": {key: str(value) for key, value in sorted(approved_by_currency.items())},
        "posted_gross_amount_by_currency": {key: str(value) for key, value in sorted(posted_by_currency.items())},
        "rejected_invoice_count": sum(1 for invoice in invoices if invoice.processing_status == InvoiceStatus.REJECTED),
        "validation_error_count": sum(1 for invoice in invoices if invoice.error_message),
        "vendor_count": len({invoice.vendor_id for invoice in invoices}),
        "average_gross_amount_by_currency": {
            key: str(value / Decimal(max(1, sum(1 for invoice in invoices if invoice.currency_code == key))))
            for key, value in sorted(gross_by_currency.items())
        },
    }
