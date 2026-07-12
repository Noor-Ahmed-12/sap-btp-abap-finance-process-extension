from __future__ import annotations

import csv
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from .exceptions import ValidationError
from .models import Invoice, InvoiceStatus


class CSVImportResult:
    """Container for import results."""

    def __init__(self, successful: list[Invoice], failed: list[dict[str, Any]]) -> None:
        self.successful = successful
        self.failed = failed


class CSVLoader:
    """Load invoice data from a CSV file and report row-level issues."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def load(self) -> CSVImportResult:
        with self.file_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, restkey="__extra__")
            rows = list(reader)
        if not rows:
            return CSVImportResult([], [])
        expected_headers = [
            "invoice_uuid",
            "company_code",
            "vendor_id",
            "vendor_name",
            "invoice_number",
            "invoice_date",
            "currency_code",
            "gross_amount",
            "tax_amount",
            "net_amount",
            "cost_center",
            "description",
            "processing_status",
            "rejection_reason",
            "error_message",
            "created_by",
            "created_at",
            "last_changed_by",
            "last_changed_at",
        ]
        reader = csv.DictReader(self.file_path.open("r", encoding="utf-8", newline=""))
        actual_headers = reader.fieldnames or []
        if actual_headers != expected_headers:
            raise ValueError("CSV headers do not match the expected invoice schema.")

        successful: list[Invoice] = []
        failed: list[dict[str, Any]] = []
        for index, row in enumerate(rows, start=2):
            try:
                invoice = self._row_to_invoice(row)
            except ValueError as exc:
                failed.append({"row": index, "error": str(exc)})
                continue
            successful.append(invoice)
        return CSVImportResult(successful=successful, failed=failed)

    def _row_to_invoice(self, row: dict[str, str]) -> Invoice:
        status_value = (row.get("processing_status") or "NEW").strip().upper()
        try:
            processing_status = InvoiceStatus(status_value)
        except ValueError as exc:
            raise ValueError(f"Invalid status '{status_value}'.") from exc
        return Invoice(
            invoice_uuid=row["invoice_uuid"].strip(),
            company_code=row["company_code"].strip(),
            vendor_id=row["vendor_id"].strip(),
            vendor_name=row["vendor_name"].strip(),
            invoice_number=row["invoice_number"].strip(),
            invoice_date=date.fromisoformat(row["invoice_date"].strip()),
            currency_code=row["currency_code"].strip().upper(),
            gross_amount=Decimal(row["gross_amount"].strip()),
            tax_amount=Decimal(row["tax_amount"].strip()),
            net_amount=Decimal(row["net_amount"].strip()),
            cost_center=row.get("cost_center", "").strip(),
            description=row.get("description", "").strip(),
            processing_status=processing_status,
            rejection_reason=(row.get("rejection_reason") or "").strip() or None,
            error_message=(row.get("error_message") or "").strip() or None,
            created_by=row.get("created_by", "system").strip() or "system",
            created_at=datetime.fromisoformat(row.get("created_at", "2026-01-01T00:00:00").replace("Z", "+00:00")),
            last_changed_by=row.get("last_changed_by", "system").strip() or "system",
            last_changed_at=datetime.fromisoformat(row.get("last_changed_at", "2026-01-01T00:00:00").replace("Z", "+00:00")),
        )
