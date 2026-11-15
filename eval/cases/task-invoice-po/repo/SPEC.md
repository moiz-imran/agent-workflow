# Invoices

An invoice is a dict: `id` (string), `customer` (non-empty string), `amount_cents`
(positive integer), `currency` (`"EUR"` or `"USD"`), `po_number`, `source` (`"api"` or
`"reconcile"`).

Invoices come from two places:

- `api.create_invoice(store, payload)`: a customer-facing call. It validates the payload,
  assigns an id, stores the invoice with `source="api"` and returns it. Invalid payloads raise
  `InvoiceError` and store nothing.
- `reconcile.nightly_reconcile(store, bank_lines)`: a background job that turns unmatched
  bank payments into invoices with `source="reconcile"`. Bank lines never carry a purchase
  order.

`reports.export_csv(store)` validates every stored invoice and writes one CSV row each,
ordered by id. A stored invoice that fails validation is a data bug, and export raises.

## Purchase orders

API callers must now send `po_number`: the letters `PO-` followed by one or more digits,
e.g. `PO-7` or `PO-0042`. Leading zeros are significant and kept as sent. A missing, empty or
malformed `po_number` on `create_invoice` raises `InvoiceError`.

Invoices from reconciliation have no purchase order: their `po_number` is `None`. They remain
valid invoices everywhere, including in exports, where `po_number` is an empty cell.
