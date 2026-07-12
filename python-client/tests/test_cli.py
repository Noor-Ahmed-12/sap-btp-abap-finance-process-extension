import json
from pathlib import Path

import pytest

from sap_finance_extension.cli import build_parser, main
from sap_finance_extension.models import Invoice, InvoiceStatus


@pytest.fixture
def repository_path(tmp_path: Path) -> Path:
    return tmp_path / "invoices.json"


def test_build_parser_accepts_show_subcommand() -> None:
    parser = build_parser()
    args = parser.parse_args(["show", "inv-123"])
    assert args.command == "show"
    assert args.invoice_uuid == "inv-123"


def test_cli_init_creates_store(tmp_path: Path) -> None:
    storage = tmp_path / "invoices.json"
    exit_code = main(["init"])
    assert exit_code == 0


def test_cli_show_returns_invoice(tmp_path: Path) -> None:
    repository_path = tmp_path / "invoices.json"
    invoice = Invoice(
        invoice_uuid="inv-1",
        company_code="1000",
        vendor_id="VEN-1",
        vendor_name="Example Vendor",
        invoice_number="INV-1",
        invoice_date=__import__("datetime").date(2026, 7, 1),
        currency_code="EUR",
        gross_amount=__import__("decimal").Decimal("100.00"),
        tax_amount=__import__("decimal").Decimal("10.00"),
        net_amount=__import__("decimal").Decimal("90.00"),
        processing_status=InvoiceStatus.NEW,
    )
    from sap_finance_extension.local_repository import LocalInvoiceRepository

    repository = LocalInvoiceRepository(repository_path)
    repository.add(invoice)
    exit_code = main(["show", "inv-1"])
    assert exit_code == 0
