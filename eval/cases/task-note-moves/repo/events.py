"""Event payloads."""


def created(note, version):
    return {"type": "created", "note": note["id"], "version": version}


def updated(note, version):
    return {"type": "updated", "note": note["id"], "version": version}
