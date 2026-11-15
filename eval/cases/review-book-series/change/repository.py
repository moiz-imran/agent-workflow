"""Row storage. Rows are tuples in COLUMNS order, as the storage engine requires."""
COLUMNS = ("isbn", "title", "author", "series", "tags")
DEFAULTS = {"series": None, "tags": ()}  # rows from earlier releases are shorter


def _to_row(book):
    return tuple(tuple(book.get("tags") or ()) if c == "tags" else book.get(c) for c in COLUMNS)


def _from_row(row):
    book = {**DEFAULTS, **dict(zip(COLUMNS, row))}
    book["tags"] = list(book["tags"])
    return book


class Repository:
    def __init__(self, rows=None):
        self._rows = {row[0]: tuple(row) for row in rows or []}

    def save(self, book):
        self._rows[book["isbn"]] = _to_row(book)

    def load(self, isbn):
        row = self._rows.get(isbn)
        return _from_row(row) if row else None

    def update_fields(self, isbn, changes):
        """Apply known columns from changes; unknown keys are ignored."""
        book = self.load(isbn)
        if book is None:
            raise KeyError(isbn)
        book.update({k: v for k, v in changes.items() if k in COLUMNS})
        self.save(book)
        return book
