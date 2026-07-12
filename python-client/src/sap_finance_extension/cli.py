from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .csv_loader import CSVLoader
from .exceptions import (
    InvalidStatusTransitionError,
    InvoiceValidationError,
    RepositoryError,
)
from .lifecycle import InvoiceLifecycleService
from .local_repository import (
    LocalInvoiceRepository,
    get_default_repository_path,
)
from .reporting import build_summary
from .validators import ensure_valid_invoice


class CLIError(Exception):
    """Raised for CLI command failures."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SAP finance invoice workflow demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local data store")

    import_parser = subparsers.add_parser("import-csv", help="Import invoices from a CSV file")
    import_parser.add_argument("file_path")

    subparsers.add_parser("list", help="List all invoices")
    show_parser = subparsers.add_parser("show", help="Show one invoice")
    show_parser.add_argument("invoice_uuid")

    validate_parser = subparsers.add_parser("validate", help="Validate an invoice")
    validate_parser.add_argument("invoice_uuid")

    approve_parser = subparsers.add_parser("approve", help="Approve an invoice")
    approve_parser.add_argument("invoice_uuid")

    reject_parser = subparsers.add_parser("reject", help="Reject an invoice")
    reject_parser.add_argument("invoice_uuid")
    reject_parser.add_argument("reason")

    reopen_parser = subparsers.add_parser("reopen", help="Reopen a rejected invoice")
    reopen_parser.add_argument("invoice_uuid")

    post_parser = subparsers.add_parser("post", help="Post an approved invoice")
    post_parser.add_argument("invoice_uuid")

    subparsers.add_parser("summary", help="Show finance summary")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage_path = Path(
        __import__("os").environ.get(
            "SAP_FINANCE_REPOSITORY",
            str(get_default_repository_path()),
        )
    )
    repository = LocalInvoiceRepository(storage_path)
    lifecycle = InvoiceLifecycleService()

    try:
        if args.command == "init":
            repository.storage_path.parent.mkdir(parents=True, exist_ok=True)
            repository.storage_path.write_text("[]", encoding="utf-8")
            print("Initialized local invoice store.")
            return 0

        if args.command == "import-csv":
            loader = CSVLoader(args.file_path)
            result = loader.load()
            for invoice in result.successful:
                ensure_valid_invoice(invoice, repository.list_all())
                repository.add(invoice)
            print(f"Imported {len(result.successful)} invoices.")
            if result.failed:
                print("Failed rows:")
                for item in result.failed:
                    print(f"- row {item['row']}: {item['error']}")
            return 0 if not result.failed else 1

        if args.command == "list":
            invoices = repository.list_all()
            for invoice in invoices:
                print(
                    f"{invoice.invoice_uuid} | "
                    f"{invoice.processing_status.value} | "
                    f"{invoice.vendor_id}"
                )
            return 0

        if args.command == "show":
            invoice = repository.get(args.invoice_uuid)
            assert invoice is not None, "Invoice not found."
            print(json.dumps(invoice.to_dict(), indent=2))
            return 0

        if args.command == "validate":
            invoice = repository.get(args.invoice_uuid)
            assert invoice is not None, "Invoice not found."
            ensure_valid_invoice(invoice, repository.list_all())
            lifecycle.validate(invoice)
            repository.update(invoice)
            print(f"Validated invoice {invoice.invoice_uuid}")
            return 0

        if args.command == "approve":
            invoice = repository.get(args.invoice_uuid)
            assert invoice is not None, "Invoice not found."
            lifecycle.approve(invoice)
            repository.update(invoice)
            print(f"Approved invoice {invoice.invoice_uuid}")
            return 0

        if args.command == "reject":
            invoice = repository.get(args.invoice_uuid)
            assert invoice is not None, "Invoice not found."
            lifecycle.reject(invoice, args.reason)
            repository.update(invoice)
            print(f"Rejected invoice {invoice.invoice_uuid}")
            return 0

        if args.command == "reopen":
            invoice = repository.get(args.invoice_uuid)
            assert invoice is not None, "Invoice not found."
            lifecycle.reopen(invoice)
            repository.update(invoice)
            print(f"Reopened invoice {invoice.invoice_uuid}")
            return 0

        if args.command == "post":
            invoice = repository.get(args.invoice_uuid)
            assert invoice is not None, "Invoice not found."
            lifecycle.post(invoice)
            repository.update(invoice)
            print(f"Posted invoice {invoice.invoice_uuid}")
            return 0

        if args.command == "summary":
            summary = build_summary(repository.list_all())
            print(json.dumps(summary, indent=2))
            return 0
    except (
        CLIError,
        InvoiceValidationError,
        InvalidStatusTransitionError,
        RepositoryError,
        ValueError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    parser.error("Unsupported command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
