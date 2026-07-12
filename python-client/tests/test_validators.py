from decimal import Decimal

from sap_finance_extension.exceptions import InvoiceValidationError
from sap_finance_extension.models import Invoice, InvoiceStatus
from sap_finance_extension.validators import validate_invoice


def make_invoice(**overrides):
    invoice = Invoice(
        invoice_uuid="inv-1",
        company_code="1000",
        vendor_id="VEN-1",
        vendor_name="Example Vendor",
        invoice_number="INV-1",
        invoice_date=__import__("datetime").date(2026, 7, 1),
        currency_code="EUR",
        gross_amount=Decimal("100.00"),
        tax_amount=Decimal("10.00"),
        net_amount=Decimal("90.00"),
        processing_status=InvoiceStatus.NEW,
    )
    for key, value in overrides.items():
        setattr(invoice, key, value)
    return invoice


def test_valid_invoice_passes():
    invoice = make_invoice()
    assert validate_invoice(invoice, []) == []


def test_missing_vendor_id_fails():
    invoice = make_invoice(vendor_id="")
    errors = validate_invoice(invoice, [])
    assert any(error.field == "vendor_id" for error in errors)


def test_missing_invoice_number_fails():
    invoice = make_invoice(invoice_number="")
    errors = validate_invoice(invoice, [])
    assert any(error.field == "invoice_number" for error in errors)


def test_gross_amount_zero_fails():
    invoice = make_invoice(gross_amount=Decimal("0"))
    errors = validate_invoice(invoice, [])
    assert any(error.code == "INVALID_AMOUNT" for error in errors)


def test_negative_tax_fails():
    invoice = make_invoice(tax_amount=Decimal("-1"))
    errors = validate_invoice(invoice, [])
    assert any(error.field == "tax_amount" for error in errors)


def test_unsupported_currency_fails():
    invoice = make_invoice(currency_code="XYZ")
    errors = validate_invoice(invoice, [])
    assert any(error.field == "currency_code" for error in errors)


def test_amount_reconciliation_failure_fails():
    invoice = make_invoice(net_amount=Decimal("80.00"))
    errors = validate_invoice(invoice, [])
    assert any(error.code == "RECONCILIATION_ERROR" for error in errors)


def test_duplicate_vendor_invoice_number_fails():
    invoice = make_invoice()
    duplicate = make_invoice(invoice_uuid="inv-2")
    errors = validate_invoice(invoice, [duplicate])
    assert any(error.code == "DUPLICATE_INVOICE" for error in errors)


def test_self_duplicate_is_ignored():
    invoice = make_invoice()
    errors = validate_invoice(invoice, [invoice])
    assert errors == []
