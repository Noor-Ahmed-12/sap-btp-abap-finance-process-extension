from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .exceptions import RepositoryError
from .models import Invoice, InvoiceStatus

DEFAULT_REPOSITORY_PATH = Path("local-data/invoices.json")


def get_default_repository_path() -> Path:
    return DEFAULT_REPOSITORY_PATH


def set_default_repository_path(path: str | Path) -> None:
    global DEFAULT_REPOSITORY_PATH
    DEFAULT_REPOSITORY_PATH = Path(path)


class LocalInvoiceRepository:
    """JSON-backed repository for local invoice persistence."""

    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = Path(storage_path or DEFAULT_REPOSITORY_PATH)
        set_default_repository_path(self.storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.touch(exist_ok=True)
        if self.storage_path.stat().st_size == 0:
            self.storage_path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict[str, Any]]:
        return json.loads(self.storage_path.read_text(encoding="utf-8"))

    def _save(self, items: list[dict[str, Any]]) -> None:
        self.storage_path.write_text(json.dumps(items, indent=2), encoding="utf-8")

    def _decode(self, data: dict[str, Any]) -> Invoice:
        return Invoice(
            invoice_uuid=data["invoice_uuid"],
            company_code=data["company_code"],
            vendor_id=data["vendor_id"],
            vendor_name=data["vendor_name"],
            invoice_number=data["invoice_number"],
            invoice_date=__import__("datetime").date.fromisoformat(data["invoice_date"]),
            currency_code=data["currency_code"],
            gross_amount=__import__("decimal").Decimal(data["gross_amount"]),
            tax_amount=__import__("decimal").Decimal(data["tax_amount"]),
            net_amount=__import__("decimal").Decimal(data["net_amount"]),
            cost_center=data.get("cost_center", ""),
            description=data.get("description", ""),
            processing_status=InvoiceStatus(data.get("processing_status", InvoiceStatus.NEW.value)),
            rejection_reason=data.get("rejection_reason"),
            error_message=data.get("error_message"),
            created_by=data.get("created_by", "system"),
            created_at=__import__("datetime").datetime.fromisoformat(data["created_at"]),
            last_changed_by=data.get("last_changed_by", "system"),
            last_changed_at=__import__("datetime").datetime.fromisoformat(data["last_changed_at"]),
        )

    def add(self, invoice: Invoice) -> Invoice:
        if self.get(invoice.invoice_uuid) is not None:
            raise RepositoryError("Invoice UUID already exists.")
        records = self._load()
        records.append(invoice.to_dict())
        self._save(records)
        return invoice

    def get(self, invoice_uuid: str) -> Invoice | None:
        for record in self._load():
            if record["invoice_uuid"] == invoice_uuid:
                return self._decode(record)
        return None

    def list_all(self) -> list[Invoice]:
        return [self._decode(record) for record in self._load()]

    def update(self, invoice: Invoice) -> Invoice:
        existing = self.get(invoice.invoice_uuid)
        if existing is None:
            raise RepositoryError("Invoice not found.")
        if existing.processing_status == InvoiceStatus.POSTED:
            raise RepositoryError("Posted invoices cannot be modified.")
        records = self._load()
        for index, record in enumerate(records):
            if record["invoice_uuid"] == invoice.invoice_uuid:
                records[index] = invoice.to_dict()
                self._save(records)
                return invoice
        raise RepositoryError("Invoice not found.")

    def delete(self, invoice_uuid: str) -> None:
        records = self._load()
        updated = [record for record in records if record["invoice_uuid"] != invoice_uuid]
        if len(updated) == len(records):
            raise RepositoryError("Invoice not found.")
        self._save(updated)

    def find_by_vendor_and_invoice_number(self, vendor_id: str, invoice_number: str) -> Invoice | None:
        for record in self._load():
            if record["vendor_id"] == vendor_id and record["invoice_number"] == invoice_number:
                return self._decode(record)
        return None
