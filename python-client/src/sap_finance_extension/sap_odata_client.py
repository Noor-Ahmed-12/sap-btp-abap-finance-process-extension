from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

from .exceptions import SAPClientError

load_dotenv()


class SAPODataClient:
    """Prepared client for future SAP OData integration."""

    def __init__(self, base_url: str | None = None, username: str | None = None, password: str | None = None, verify_ssl: bool | None = None) -> None:
        self.base_url = base_url or os.getenv("SAP_ODATA_URL", "")
        self.username = username or os.getenv("SAP_USERNAME", "")
        self.password = password or os.getenv("SAP_PASSWORD", "")
        self.verify_ssl = verify_ssl if verify_ssl is not None else os.getenv("SAP_VERIFY_SSL", "true").lower() != "false"

    def list_invoices(self) -> list[dict[str, Any]]:
        return self._request("GET", "")

    def get_invoice(self, invoice_uuid: str) -> dict[str, Any]:
        return self._request("GET", invoice_uuid)

    def create_invoice(self, invoice: Any) -> dict[str, Any]:
        return self._request("POST", "", payload=invoice.to_dict() if hasattr(invoice, "to_dict") else invoice)

    def update_invoice(self, invoice: Any) -> dict[str, Any]:
        return self._request("PUT", invoice.invoice_uuid, payload=invoice.to_dict() if hasattr(invoice, "to_dict") else invoice)

    def execute_action(self, invoice_uuid: str, action_name: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = parameters or {}
        return self._request("POST", f"{invoice_uuid}/{action_name}", payload=payload)

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        if not self.base_url:
            raise SAPClientError("SAP_ODATA_URL is not configured.")
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            response = requests.request(method, url, json=payload, timeout=10, verify=self.verify_ssl, auth=(self.username, self.password))
        except requests.RequestException as exc:
            raise SAPClientError(f"Request failed: {exc}") from exc
        if not response.ok:
            raise SAPClientError(f"SAP request failed with status {response.status_code}.")
        try:
            return response.json()
        except ValueError as exc:
            raise SAPClientError("Received invalid JSON response from SAP service.") from exc
