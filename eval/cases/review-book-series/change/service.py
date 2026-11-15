"""Cleaning and business rules for books."""
from repository import Repository  # noqa: F401  (type of repo arguments)


class BookError(ValueError):
    pass


def _isbn(value):
    digits = str(value).replace("-", "")
    if not digits.isdigit():
        raise BookError(f"bad isbn: {value!r}")
    return digits


def _required_text(data, key):
    value = str(data.get(key) or "").strip()
    if not value:
        raise BookError(f"{key} is required")
    return value


def _series(value):
    """Trimmed series name; blank or missing means no series."""
    if value is None:
        return None
    return str(value).strip() or None


def _tags(values):
    """Trimmed, lower-cased, de-duplicated tags in order of first appearance."""
    return list(dict.fromkeys(t for t in (str(v).strip().lower() for v in values or []) if t))


def clean(data):
    return {
        "isbn": _isbn(data.get("isbn", "")),
        "title": _required_text(data, "title"),
        "author": _required_text(data, "author"),
        "series": _series(data.get("series")),
        "tags": _tags(data.get("tags")),
    }


def import_book(repo, data):
    book = clean(data)
    repo.save(book)
    return book


def update_book(repo, isbn, changes):
    changes = dict(changes)
    for key in ("title", "author"):
        if key in changes:
            changes[key] = _required_text(changes, key)
    if "series" in changes:
        changes["series"] = _series(changes["series"])
    return repo.update_fields(_isbn(isbn), changes)
