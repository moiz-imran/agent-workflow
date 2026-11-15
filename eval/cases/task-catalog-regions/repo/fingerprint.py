"""Content fingerprints. Stored with each record; a change here re-labels every record."""
import hashlib
import json


def fingerprint(record):
    content = [record["sku"], record["title"], record["price_cents"]]
    return hashlib.sha256(json.dumps(content).encode()).hexdigest()
