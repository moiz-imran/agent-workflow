"""Event payloads."""


def created(note, version):
    return {"type": "created", "note": note["id"], "version": version}


def updated(note, version):
    return {"type": "updated", "note": note["id"], "version": version}


def moved(note, version, previous):
    return {"type": "moved", "note": note["id"], "version": version,
            "previous_folder": previous, "current_folder": note["folder"]}
