import unittest

from notebook import Notebook


def fresh():
    book = Notebook()
    book.save("n1", body="hi", folder="inbox")
    return book


class Moves(unittest.TestCase):
    def test_move_is_versioned(self):
        book = fresh()
        self.assertEqual(book.save("n1", folder="archive"),
                         [{"type": "moved", "note": "n1", "version": 2,
                           "previous_folder": "inbox", "current_folder": "archive"}])
        note = book.get("n1")
        self.assertEqual(note["versions"][-1], {"version": 2, "body": "hi", "folder": "archive"})
        self.assertEqual(note["versions"][0]["folder"], "inbox")

    def test_body_and_folder_one_version(self):
        book = fresh()
        emitted = book.save("n1", body="bye", folder="archive")
        self.assertEqual([e["type"] for e in emitted], ["updated", "moved"])
        self.assertEqual({e["version"] for e in emitted}, {2})
        self.assertEqual(len(book.get("n1")["versions"]), 2)

    def test_events_log(self):
        book = fresh()
        book.save("n1", folder="archive")
        self.assertEqual([e["type"] for e in book.events], ["created", "moved"])


class Unchanged(unittest.TestCase):
    def test_first_folder_is_silent(self):
        book = Notebook([{"id": "old", "body": "x", "folder": None,
                          "versions": [{"version": 1, "body": "x", "folder": None}]}])
        self.assertEqual(book.save("old", folder="inbox"), [])
        self.assertEqual(len(book.get("old")["versions"]), 1)
        self.assertEqual(book.get("old")["folder"], "inbox")

    def test_same_folder_is_nothing(self):
        book = fresh()
        self.assertEqual(book.save("n1", folder="inbox"), [])
        self.assertEqual(len(book.get("n1")["versions"]), 1)

    def test_body_change_unchanged(self):
        book = fresh()
        self.assertEqual(book.save("n1", body="hello"), [{"type": "updated", "note": "n1", "version": 2}])
