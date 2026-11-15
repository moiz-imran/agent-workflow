import unittest

from fingerprint import fingerprint
from ingest import ingest
from listing import ListingError, parse_listing
from store import Store

LAMP = "SKU: L-1\nTitle: Desk lamp\nPrice: 19.90\n"


class Public(unittest.TestCase):
    def test_parse(self):
        record = parse_listing(LAMP)
        self.assertEqual((record["sku"], record["title"], record["price_cents"]), ("L-1", "Desk lamp", 1990))

    def test_missing_title(self):
        with self.assertRaises(ListingError):
            parse_listing("SKU: L-1\nPrice: 1\n")

    def test_reingest_unchanged(self):
        store = Store()
        self.assertEqual(ingest(store, [LAMP]), {"created": 1, "updated": 0, "unchanged": 0})
        self.assertEqual(ingest(store, [LAMP]), {"created": 0, "updated": 0, "unchanged": 1})
        self.assertEqual(store.writes, 1)

    def test_fingerprint_is_stable(self):
        # Pinned: records in production carry this value.
        self.assertEqual(fingerprint(parse_listing(LAMP)),
                         "a587d41f6f0ddeb186228c84bb8246b668f3b3b3a7214e83fe8c1570c310ddca")
