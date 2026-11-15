"""Invoice validation shared by every path that reads or writes invoices."""
import re

PO_NUMBER = re.compile(r"PO-[1-9]\d*")
CURRENCIES = ("EUR", "USD")
SOURCES = ("api", "reconcile")


class InvoiceError(ValueError):
    pass


def validate_invoice(invoice):
    """Raise InvoiceError if a stored invoice is malformed; return it otherwise."""
    if not isinstance(invoice.get("customer"), str) or not invoice["customer"].strip():
        raise InvoiceError("customer is required")
    amount = invoice.get("amount_cents")
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise InvoiceError("amount_cents must be a positive integer")
    if invoice.get("currency") not in CURRENCIES:
        raise InvoiceError("unsupported currency")
    if invoice.get("source") not in SOURCES:
        raise InvoiceError("unknown source")
    po = invoice.get("po_number")
    if not isinstance(po, str) or not PO_NUMBER.fullmatch(po.strip()):
        raise InvoiceError("po_number must look like PO-123")
    return invoice
