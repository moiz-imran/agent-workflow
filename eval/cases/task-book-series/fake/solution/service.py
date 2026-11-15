"""Cleaning and business rules for books."""
from repository import Repository  # noqa: F401  (type of repo arguments)


class BookError(ValueError):
    pass


def _isbn(value):
    digits = str(value).replace("-", "")
    if not digits.isdigit():
        raise BookError(f"bad isbn: {value!r}")
    return digits


def _text(data, key):
    value = str(data.get(key) or "").strip()
    if not value:
        raise BookError(f"{key} is required")
    return value


def _series(value):
    return str(value).strip() or None if value is not None else None


def _tags(values):
    seen = []
    for tag in values or []:
        tag = str(tag).strip().lower()
        if tag and tag not in seen:
            seen.append(tag)
    return seen


def clean(data):
    return {"isbn": _isbn(data.get("isbn", "")), "title": _text(data, "title"), "author": _text(data, "author"),
            "series": _series(data.get("series")), "tags": _tags(data.get("tags"))}


def import_book(repo, data):
    book = clean(data)
    repo.save(book)
    return book


def update_book(repo, isbn, changes):
    changes = dict(changes)
    for key in ("title", "author"):
        if key in changes:
            changes[key] = _text(changes, key)
    if "series" in changes:
        changes["series"] = _series(changes["series"])
    if "tags" in changes:
        changes["tags"] = _tags(changes["tags"])
    return repo.update_fields(_isbn(isbn), changes)
