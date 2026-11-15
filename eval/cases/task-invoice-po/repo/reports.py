"""CSV export of all invoices."""
import csv
import io

from models import validate_invoice

COLUMNS = ("id", "customer", "amount_cents", "currency", "po_number", "source")


def export_csv(store):
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(COLUMNS)
    for invoice in store.all():
        validate_invoice(invoice)
        writer.writerow(["" if invoice.get(c) is None else invoice[c] for c in COLUMNS])
    return out.getvalue()
