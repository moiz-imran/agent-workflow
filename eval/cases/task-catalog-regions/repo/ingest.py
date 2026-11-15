"""Batch ingest of listing texts."""
from listing import parse_listing


def ingest(store, texts):
    counts = {"created": 0, "updated": 0, "unchanged": 0}
    for text in texts:
        counts[store.upsert(parse_listing(text))] += 1
    return counts
