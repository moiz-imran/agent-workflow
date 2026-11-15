"""Content fingerprints. Stored with each record; a change here re-labels every record."""
import hashlib
import json


def fingerprint(record):
    content = [record["sku"], record["title"], record["price_cents"]]
    if record.get("regions"):  # only when present, so records without regions keep their stored print
        content.append(record["regions"])
    return hashlib.sha256(json.dumps(content).encode()).hexdigest()
