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


def clean(data):
    return {"isbn": _isbn(data.get("isbn", "")), "title": _text(data, "title"), "author": _text(data, "author")}


def import_book(repo, data):
    book = clean(data)
    repo.save(book)
    return book


def update_book(repo, isbn, changes):
    changes = dict(changes)
    for key in ("title", "author"):
        if key in changes:
            changes[key] = _text(changes, key)
    return repo.update_fields(_isbn(isbn), changes)
