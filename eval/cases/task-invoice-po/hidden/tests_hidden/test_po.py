import unittest

from api import create_invoice
from models import InvoiceError
from reconcile import nightly_reconcile
from reports import export_csv
from store import Store


def payload(**kw):
    return {"customer": "Acme", "amount_cents": 500, "currency": "EUR", "po_number": "PO-1", **kw}


class PurchaseOrders(unittest.TestCase):
    def test_missing_po_rejected(self):
        store = Store()
        for bad in ({"po_number": None}, {"po_number": ""}, {"po_number": "PO-"}, {"po_number": "po-12"},
                    {"po_number": "PO-12a"}, {"po_number": 12}):
            with self.subTest(bad=bad), self.assertRaises(InvoiceError):
                create_invoice(store, payload(**bad))
        omitted = payload()
        del omitted["po_number"]
        with self.assertRaises(InvoiceError):
            create_invoice(store, omitted)
        self.assertEqual(store.all(), [])

    def test_valid_po_kept_as_sent(self):
        store = Store()
        self.assertEqual(create_invoice(store, payload(po_number="PO-0042"))["po_number"], "PO-0042")
        self.assertEqual(create_invoice(store, payload(po_number="PO-7"))["po_number"], "PO-7")


class Reconciled(unittest.TestCase):
    def test_reconcile_still_works(self):
        store = Store()
        created = nightly_reconcile(store, [{"payer": "Beta", "amount_cents": 900, "currency": "USD"}])
        self.assertIsNone(created[0]["po_number"])

    def test_export_mixes_sources(self):
        store = Store()
        create_invoice(store, payload(po_number="PO-0042"))
        nightly_reconcile(store, [{"payer": "Beta", "amount_cents": 900, "currency": "USD"}])
        rows = export_csv(store).splitlines()
        self.assertEqual(rows[1], "INV-00001,Acme,500,EUR,PO-0042,api")
        self.assertEqual(rows[2], "INV-00002,Beta,900,USD,,reconcile")
