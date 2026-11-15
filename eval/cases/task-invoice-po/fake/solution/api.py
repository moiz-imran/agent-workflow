"""Customer-facing invoice creation."""
import re

from models import InvoiceError, validate_invoice

ALLOWED = ("customer", "amount_cents", "currency", "po_number")
PO = re.compile(r"PO-\d+")


def create_invoice(store, payload):
    unknown = set(payload) - set(ALLOWED)
    if unknown:
        raise InvoiceError(f"unknown fields: {sorted(unknown)}")
    po = payload.get("po_number")
    if not isinstance(po, str) or not PO.fullmatch(po):  # API only: reconciled invoices have no PO
        raise InvoiceError("po_number must look like PO-123")
    invoice = {**{k: payload.get(k) for k in ALLOWED}, "source": "api"}
    validate_invoice(invoice)
    invoice["id"] = store.next_id()
    store.put(invoice)
    return invoice
