from decimal import Decimal

from sap_finance_extension.local_repository import LocalInvoiceRepository
from sap_finance_extension.models import Invoice, InvoiceStatus


def make_invoice(invoice_uuid: str) -> Invoice:
    return Invoice(
        invoice_uuid=invoice_uuid,
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


def test_add_invoice(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    invoice = make_invoice("inv-1")
    repository.add(invoice)
    assert repository.get("inv-1") is not None


def test_retrieve_invoice(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    invoice = make_invoice("inv-1")
    repository.add(invoice)
    retrieved = repository.get("inv-1")
    assert retrieved is not None and retrieved.vendor_id == "VEN-1"


def test_update_invoice(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    invoice = make_invoice("inv-1")
    repository.add(invoice)
    invoice.processing_status = InvoiceStatus.VALIDATED
    repository.update(invoice)
    updated = repository.get("inv-1")
    assert updated is not None and updated.processing_status == InvoiceStatus.VALIDATED


def test_reject_duplicate_uuid(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    repository.add(make_invoice("inv-1"))
    try:
        repository.add(make_invoice("inv-1"))
    except Exception as exc:
        assert "already exists" in str(exc).lower()


def test_find_by_vendor_and_invoice_number(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    repository.add(make_invoice("inv-1"))
    found = repository.find_by_vendor_and_invoice_number("VEN-1", "INV-1")
    assert found is not None


def test_delete_invoice(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    repository.add(make_invoice("inv-1"))
    repository.delete("inv-1")
    assert repository.get("inv-1") is None


def test_persistence_survives_reinitialization(tmp_path) -> None:
    repository = LocalInvoiceRepository(tmp_path / "invoices.json")
    repository.add(make_invoice("inv-1"))
    reloaded = LocalInvoiceRepository(tmp_path / "invoices.json")
    assert reloaded.get("inv-1") is not None
