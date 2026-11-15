"""In-memory invoice store."""
import copy
import itertools


class Store:
    def __init__(self):
        self._invoices = {}
        self._ids = itertools.count(1)

    def next_id(self):
        return f"INV-{next(self._ids):05d}"

    def put(self, invoice):
        self._invoices[invoice["id"]] = copy.deepcopy(invoice)

    def all(self):
        return [copy.deepcopy(self._invoices[k]) for k in sorted(self._invoices)]
