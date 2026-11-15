import unittest

from fingerprint import fingerprint
from ingest import ingest
from listing import parse_listing
from store import Store

LAMP = "SKU: L-1\nTitle: Desk lamp\nPrice: 19.90\n"
OLD_PRINT = "a587d41f6f0ddeb186228c84bb8246b668f3b3b3a7214e83fe8c1570c310ddca"


class Regions(unittest.TestCase):
    def test_parsed_normalised(self):
        self.assertEqual(parse_listing(LAMP + "Regions: eu, US ,us\n")["regions"], ["EU", "US"])

    def test_missing_or_empty_is_none(self):
        self.assertEqual(parse_listing(LAMP)["regions"], [])
        self.assertEqual(parse_listing(LAMP + "Regions:\n")["regions"], [])

    def test_region_only_change_is_stored(self):
        store = Store()
        ingest(store, [LAMP + "Regions: EU\n"])
        self.assertEqual(ingest(store, [LAMP + "Regions: EU, US\n"]), {"created": 0, "updated": 1, "unchanged": 0})
        self.assertEqual(store.get("L-1")["regions"], ["EU", "US"])

    def test_regions_removed_is_stored(self):
        store = Store()
        ingest(store, [LAMP + "Regions: EU\n"])
        self.assertEqual(ingest(store, [LAMP])["updated"], 1)
        self.assertEqual(store.get("L-1")["regions"], [])


class Compatibility(unittest.TestCase):
    def test_no_regions_keeps_old_fingerprint(self):
        self.assertEqual(fingerprint(parse_listing(LAMP)), OLD_PRINT)

    def test_existing_records_not_relabelled(self):
        # A record stored before the release: no regions key, old fingerprint.
        store = Store([{"sku": "L-1", "title": "Desk lamp", "price_cents": 1990, "fingerprint": OLD_PRINT}])
        self.assertEqual(ingest(store, [LAMP]), {"created": 0, "updated": 0, "unchanged": 1})
        self.assertEqual(store.writes, 0)

    def test_ordinary_listing_still_ingests(self):
        store = Store()
        self.assertEqual(ingest(store, [LAMP, "SKU: B-2\nTitle: Bulb\nPrice: 3\n"])["created"], 2)
        self.assertEqual(store.get("B-2")["price_cents"], 300)
