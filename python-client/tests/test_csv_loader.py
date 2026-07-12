from pathlib import Path

from sap_finance_extension.csv_loader import CSVLoader
from sap_finance_extension.models import InvoiceStatus


def test_valid_file_imports() -> None:
    loader = CSVLoader(Path("sample-data/valid_invoices.csv"))
    result = loader.load()
    assert len(result.successful) == 5
    assert result.failed == []


def test_invalid_rows_are_reported() -> None:
    loader = CSVLoader(Path("sample-data/invalid_invoices.csv"))
    result = loader.load()
    assert len(result.successful) == 0
    assert len(result.failed) == 8


def test_missing_headers_are_reported() -> None:
    bad_file = Path("python-client/tests/fixtures/bad_headers.csv")
    bad_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.write_text("not,valid\n", encoding="utf-8")
    try:
        loader = CSVLoader(bad_file)
        loader.load()
    except ValueError as exc:
        assert "headers" in str(exc).lower()
    finally:
        bad_file.unlink(missing_ok=True)


def test_decimal_parsing_works() -> None:
    loader = CSVLoader(Path("sample-data/valid_invoices.csv"))
    invoice = loader.load().successful[0]
    assert invoice.gross_amount == 1250.00


def test_date_parsing_works() -> None:
    loader = CSVLoader(Path("sample-data/valid_invoices.csv"))
    invoice = loader.load().successful[0]
    assert invoice.invoice_date.year == 2026


def test_business_validation_is_applied_during_csv_import() -> None:
    loader = CSVLoader(Path("sample-data/invalid_invoices.csv"))
    result = loader.load()
    assert any("vendor_id" in item["error"].lower() for item in result.failed)
    assert any("gross" in item["error"].lower() or "currency" in item["error"].lower() for item in result.failed)


def test_invalid_status_is_reported() -> None:
    bad_file = Path("python-client/tests/fixtures/bad_status.csv")
    bad_file.parent.mkdir(parents=True, exist_ok=True)
    bad_file.write_text(
        "invoice_uuid,company_code,vendor_id,vendor_name,invoice_number,invoice_date,currency_code,gross_amount,tax_amount,net_amount,cost_center,description,processing_status,rejection_reason,error_message,created_by,created_at,last_changed_by,last_changed_at\n" +
        "inv-1,1000,VEN-1,Example Vendor,INV-1,2026-07-01,EUR,100.00,10.00,90.00,CC-100,Description,INVALID,,,,system,2026-07-01T09:00:00Z,system,2026-07-01T09:00:00Z\n",
        encoding="utf-8",
    )
    try:
        loader = CSVLoader(bad_file)
        result = loader.load()
        assert len(result.successful) == 0
        assert len(result.failed) == 1
    finally:
        bad_file.unlink(missing_ok=True)
