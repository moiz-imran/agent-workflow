"""In-memory record store keyed by SKU."""
import copy

from fingerprint import fingerprint


class Store:
    def __init__(self, rows=None):
        self._rows = {r["sku"]: copy.deepcopy(r) for r in rows or []}
        self.writes = 0

    def get(self, sku):
        row = self._rows.get(sku)
        return copy.deepcopy(row) if row else None

    def upsert(self, record):
        """Return "created", "updated" or "unchanged"."""
        new_print = fingerprint(record)
        old = self._rows.get(record["sku"])
        if old and old["fingerprint"] == new_print:
            return "unchanged"
        self._rows[record["sku"]] = {**copy.deepcopy(record), "fingerprint": new_print}
        self.writes += 1
        return "updated" if old else "created"
