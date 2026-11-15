"""Customer-facing invoice creation."""
from models import InvoiceError, validate_invoice

ALLOWED = ("customer", "amount_cents", "currency", "po_number")


def create_invoice(store, payload):
    unknown = set(payload) - set(ALLOWED)
    if unknown:
        raise InvoiceError(f"unknown fields: {sorted(unknown)}")
    invoice = {**{k: payload.get(k) for k in ALLOWED}, "source": "api"}
    validate_invoice(invoice)
    invoice["id"] = store.next_id()
    store.put(invoice)
    return invoice
