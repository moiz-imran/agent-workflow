# Notes

A note has an `id`, a `body`, a `folder` (string, or `None` for notes created before folders
existed) and a list of versions. `Notebook.save(note_id, body=..., folder=...)` writes a note.
Every call returns the events it emitted, also appended to `Notebook.events`.

- A new note gets version 1 and emits `{"type": "created", "note": id, "version": 1}`.
- A body change creates the next version and emits
  `{"type": "updated", "note": id, "version": n}`.
- Saving identical content creates nothing and emits nothing.
- Versions are immutable snapshots of `body` and `folder`.

## Folder moves

Until now a folder change only refreshed the live note: no version, no event. That is
replaced:

- A save that changes the folder of a note from one folder to a different folder creates the
  next version and emits `{"type": "moved", "note": id, "version": n,
  "previous_folder": old, "current_folder": new}`.
- When the body and the folder both change in one save, it is one version with two events:
  `updated` then `moved`, both carrying that version number.
- A note whose folder is `None` getting its first folder is not a move: the live note is
  refreshed silently, with no version and no event, as before. This keeps the folder
  backfill for old notes from producing a flood of moves.

The public test `test_move_refreshes_without_version` pins the old behaviour. Update it to
the new rule; don't keep the old behaviour to make it pass.
