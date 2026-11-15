"""Parse catalog listing text into a record dict."""
from decimal import Decimal, InvalidOperation

REQUIRED = ("sku", "title", "price")


class ListingError(ValueError):
    pass


def _fields(text):
    fields = {}
    for raw in text.splitlines():
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        fields[key.strip().lower()] = value.strip()
    return fields


def _cents(value):
    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise ListingError(f"bad price: {value!r}") from None
    if amount.as_tuple().exponent < -2 or amount < 0:
        raise ListingError(f"bad price: {value!r}")
    return int(amount * 100)


def parse_listing(text):
    fields = _fields(text)
    for key in REQUIRED:
        if not fields.get(key):
            raise ListingError(f"missing {key}")
    return {
        "sku": fields["sku"],
        "title": fields["title"],
        "price_cents": _cents(fields["price"]),
        "regions": _regions(fields.get("regions", "")),
    }


def _regions(value):
    return sorted({code.strip().upper() for code in value.split(",") if code.strip()})
