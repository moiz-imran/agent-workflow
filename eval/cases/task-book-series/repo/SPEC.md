# Book catalogue

`service.import_book(repo, data)` cleans incoming book data and saves it.
`service.update_book(repo, isbn, changes)` applies a partial update to a stored book.
`api.book_response(repo, isbn)` returns the public JSON shape for one book, or `None` when
the ISBN is unknown.

Fields: `isbn` (string, digits only after removing hyphens), `title` (trimmed, non-empty),
`author` (trimmed, non-empty). The repository stores rows as tuples in column order; rows
written by earlier releases stay in the store and must keep loading.

## Series and tags

- `series`: optional string, trimmed; an empty string means no series. Absent → `None`.
- `tags`: optional list of strings; each trimmed and lower-cased, empties dropped,
  duplicates removed, order of first appearance kept. Absent → `[]`.

Both are accepted by `import_book` and `update_book`, stored, and returned by
`book_response` as `"series"` and `"tags"`. Books stored before this release have no series
and no tags. An update that does not mention a field leaves it unchanged.
