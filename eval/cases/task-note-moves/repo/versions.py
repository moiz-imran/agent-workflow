"""Immutable version snapshots."""


def snapshot(note, number):
    return {"version": number, "body": note["body"], "folder": note["folder"]}


def latest(note):
    return note["versions"][-1] if note["versions"] else None
