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
        emitted = []
        if body is not UNSET and body != note["body"]:
            note["body"] = body
            number = latest(note)["version"] + 1
            note["versions"].append(snapshot(note, number))
            emitted.append(events.updated(note, number))
        if folder is not UNSET and folder != note["folder"]:
            note["folder"] = folder  # live refresh only: folders are not versioned
        return self._emit(emitted)

    def _emit(self, emitted):
        self.events.extend(emitted)
        return emitted
