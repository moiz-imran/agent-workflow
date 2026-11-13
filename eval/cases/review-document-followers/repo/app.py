def copy_document(doc, folder):
    return {**doc, "folder": folder, "followers": []}


def move_document(doc, folder):
    doc["folder"] = folder
    return []


def save_document(doc, body):
    changed = doc["body"].split() != body.split()
    doc["body"] = body
    return list(doc["followers"]) if changed else []
