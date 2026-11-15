"""Nightly job: unmatched bank payments become invoices."""
from models import validate_invoice


def nightly_reconcile(store, bank_lines):
    """bank_lines: dicts with payer, amount_cents, currency. Returns the created invoices."""
    created = []
    for line in bank_lines:
        invoice = validate_invoice({
            "customer": line["payer"], "amount_cents": line["amount_cents"],
            "currency": line["currency"], "po_number": None, "source": "reconcile",
        })
        invoice["id"] = store.next_id()
        store.put(invoice)
        created.append(invoice)
    return created
