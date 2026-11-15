"""Note storage, versioning and events."""
import copy

import events
from versions import latest, snapshot

UNSET = object()


class Notebook:
    def __init__(self, notes=None):
        self._notes = {n["id"]: copy.deepcopy(n) for n in notes or []}
        self.events = []

    def get(self, note_id):
        return copy.deepcopy(self._notes[note_id])

    def save(self, note_id, body=UNSET, folder=UNSET):
        note = self._notes.get(note_id)
        if note is None:
            note = {"id": note_id, "body": "" if body is UNSET else body,
                    "folder": None if folder is UNSET else folder, "versions": []}
            note["versions"].append(snapshot(note, 1))
            self._notes[note_id] = note
            return self._emit([events.created(note, 1)])
        body_changed = body is not UNSET and body != note["body"]
        previous = note["folder"]
        folder_changed = folder is not UNSET and folder != previous
        moved = folder_changed and previous is not None  # a first folder is a silent backfill
        if body_changed:
            note["body"] = body
        if folder_changed:
            note["folder"] = folder
        if not (body_changed or moved):
            return []
        number = latest(note)["version"] + 1
        note["versions"].append(snapshot(note, number))
        emitted = [events.updated(note, number)] if body_changed else []
        if moved:
            emitted.append(events.moved(note, number, previous))
        return self._emit(emitted)

    def _emit(self, emitted):
        self.events.extend(emitted)
        return emitted
