import unittest

from api import create_invoice
from models import InvoiceError
from reconcile import nightly_reconcile
from reports import export_csv
from store import Store


class Public(unittest.TestCase):
    def test_create_and_export(self):
        store = Store()
        inv = create_invoice(store, {"customer": "Acme", "amount_cents": 500, "currency": "EUR", "po_number": "PO-1"})
        self.assertEqual(inv["id"], "INV-00001")
        self.assertIn("INV-00001,Acme,500,EUR,PO-1,api", export_csv(store))

    def test_bad_currency(self):
        with self.assertRaises(InvoiceError):
            create_invoice(Store(), {"customer": "Acme", "amount_cents": 5, "currency": "GBP", "po_number": "PO-1"})

    def test_reconcile(self):
        store = Store()
        nightly_reconcile(store, [{"payer": "Beta", "amount_cents": 900, "currency": "USD"}])
        self.assertEqual(store.all()[0]["source"], "reconcile")
