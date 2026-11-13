def copy_document(doc, folder):
    return {**doc, "folder": folder, "followers": list(doc["followers"])}


def move_document(doc, folder):
    doc["folder"] = folder
    doc["followers"] = []
    return []


def save_document(doc, body):
    changed = doc["body"] != body
    doc["body"] = body
    return list(doc["followers"]) if changed else []
