from decimal import Decimal

import pytest
from sap_finance_extension.exceptions import InvalidStatusTransitionError
from sap_finance_extension.lifecycle import InvoiceLifecycleService
from sap_finance_extension.models import Invoice, InvoiceStatus


@pytest.fixture
def service() -> InvoiceLifecycleService:
    return InvoiceLifecycleService()


def make_invoice(status: InvoiceStatus = InvoiceStatus.NEW) -> Invoice:
    return Invoice(
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
        processing_status=status,
    )


def test_new_invoice_can_be_validated(service: InvoiceLifecycleService) -> None:
    invoice = service.validate(make_invoice())
    assert invoice.processing_status == InvoiceStatus.VALIDATED


def test_new_invoice_cannot_be_approved(service: InvoiceLifecycleService) -> None:
    with pytest.raises(InvalidStatusTransitionError):
        service.approve(make_invoice())


def test_validated_invoice_can_be_approved(service: InvoiceLifecycleService) -> None:
    invoice = service.validate(make_invoice())
    approved = service.approve(invoice)
    assert approved.processing_status == InvoiceStatus.APPROVED


def test_validated_invoice_can_be_rejected(service: InvoiceLifecycleService) -> None:
    invoice = service.validate(make_invoice())
    rejected = service.reject(invoice, "Reason")
    assert rejected.processing_status == InvoiceStatus.REJECTED


def test_rejection_requires_a_reason(service: InvoiceLifecycleService) -> None:
    with pytest.raises(ValueError):
        service.reject(make_invoice(), "")


def test_rejected_invoice_can_be_reopened(service: InvoiceLifecycleService) -> None:
    invoice = service.reject(make_invoice(), "Reason")
    reopened = service.reopen(invoice)
    assert reopened.processing_status == InvoiceStatus.NEW


def test_approved_invoice_can_be_posted(service: InvoiceLifecycleService) -> None:
    invoice = service.validate(make_invoice())
    invoice = service.approve(invoice)
    posted = service.post(invoice)
    assert posted.processing_status == InvoiceStatus.POSTED


def test_rejected_invoice_cannot_be_posted(service: InvoiceLifecycleService) -> None:
    invoice = service.reject(make_invoice(), "Reason")
    with pytest.raises(InvalidStatusTransitionError):
        service.post(invoice)


def test_posted_invoice_cannot_be_modified(service: InvoiceLifecycleService) -> None:
    invoice = service.validate(make_invoice())
    invoice = service.approve(invoice)
    invoice = service.post(invoice)
    assert invoice.processing_status == InvoiceStatus.POSTED
