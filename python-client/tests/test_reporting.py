from decimal import Decimal

from sap_finance_extension.models import Invoice, InvoiceStatus
from sap_finance_extension.reporting import build_summary


def make_invoice(
    invoice_uuid: str,
    status: InvoiceStatus,
    currency_code: str,
    gross_amount: Decimal,
) -> Invoice:
    return Invoice(
        invoice_uuid=invoice_uuid,
        company_code="1000",
        vendor_id="VEN-1",
        vendor_name="Example Vendor",
        invoice_number=invoice_uuid,
        invoice_date=__import__("datetime").date(2026, 7, 1),
        currency_code=currency_code,
        gross_amount=gross_amount,
        tax_amount=Decimal("10.00"),
        net_amount=Decimal("90.00"),
        processing_status=status,
    )


def test_counts_by_status_are_correct() -> None:
    invoices = [
        make_invoice("1", InvoiceStatus.NEW, "EUR", Decimal("100")),
        make_invoice("2", InvoiceStatus.VALIDATED, "EUR", Decimal("200")),
        make_invoice("3", InvoiceStatus.REJECTED, "USD", Decimal("300")),
    ]
    summary = build_summary(invoices)
    assert summary["count_by_status"]["NEW"] == 1
    assert summary["count_by_status"]["REJECTED"] == 1


def test_currency_totals_remain_separate() -> None:
    invoices = [
        make_invoice("1", InvoiceStatus.NEW, "EUR", Decimal("100")),
        make_invoice("2", InvoiceStatus.NEW, "USD", Decimal("200")),
    ]
    summary = build_summary(invoices)
    assert summary["gross_amount_by_currency"]["EUR"] == "100"
    assert summary["gross_amount_by_currency"]["USD"] == "200"


def test_approved_totals_are_correct() -> None:
    invoices = [
        make_invoice("1", InvoiceStatus.APPROVED, "EUR", Decimal("100")),
        make_invoice("2", InvoiceStatus.APPROVED, "EUR", Decimal("200")),
        make_invoice("3", InvoiceStatus.NEW, "EUR", Decimal("50")),
    ]
    summary = build_summary(invoices)
    assert summary["approved_gross_amount_by_currency"]["EUR"] == "300"


def test_posted_totals_are_correct() -> None:
    invoices = [
        make_invoice("1", InvoiceStatus.POSTED, "EUR", Decimal("100")),
        make_invoice("2", InvoiceStatus.POSTED, "USD", Decimal("200")),
    ]
    summary = build_summary(invoices)
    assert summary["posted_gross_amount_by_currency"]["EUR"] == "100"
    assert summary["posted_gross_amount_by_currency"]["USD"] == "200"


def test_average_values_are_correct() -> None:
    invoices = [
        make_invoice("1", InvoiceStatus.NEW, "EUR", Decimal("100")),
        make_invoice("2", InvoiceStatus.NEW, "EUR", Decimal("200")),
    ]
    summary = build_summary(invoices)
    assert summary["average_gross_amount_by_currency"]["EUR"] == "150"
