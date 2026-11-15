# Catalog ingest

A listing is plain text, one `Key: value` per line. Keys are case-insensitive.

- `SKU` (required): non-empty string, stored as given after trimming.
- `Title` (required): non-empty string, trimmed.
- `Price` (required): decimal with at most two places, e.g. `12.5` or `12.50`; stored as
  integer cents.

Unknown keys are ignored. A listing missing a required key raises `ListingError`.

`ingest(store, texts)` parses each text and upserts it by SKU. It returns counts
`{"created": n, "updated": n, "unchanged": n}`. A listing is `unchanged` when its stored
fingerprint matches; nothing is written for it. Fingerprints are persisted with each record
and must stay stable across releases: a listing whose content has not changed must keep the
fingerprint it was stored with.

## Regions

A listing may contain a `Regions` line: comma-separated region codes, e.g.
`Regions: eu, US ,us`. Codes are trimmed, upper-cased, de-duplicated and stored sorted
(`["EU", "US"]`). A missing line or an empty value means no regions (`[]`).

- Re-ingesting a listing whose only change is its regions updates the stored record and
  counts as `updated`.
- A listing with no regions keeps exactly the fingerprint it had before this feature, so
  records already in the store are not reported as updated just because the release added
  regions.
