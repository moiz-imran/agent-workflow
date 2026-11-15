import unittest

from notebook import Notebook


class Public(unittest.TestCase):
    def test_create(self):
        book = Notebook()
        self.assertEqual(book.save("n1", body="hi", folder="inbox"), [{"type": "created", "note": "n1", "version": 1}])

    def test_body_change(self):
        book = Notebook()
        book.save("n1", body="hi", folder="inbox")
        self.assertEqual(book.save("n1", body="hello"), [{"type": "updated", "note": "n1", "version": 2}])
        self.assertEqual(book.save("n1", body="hello"), [])

    def test_move_is_versioned(self):
        book = Notebook()
        book.save("n1", body="hi", folder="inbox")
        self.assertEqual([e["type"] for e in book.save("n1", folder="archive")], ["moved"])
        self.assertEqual(len(book.get("n1")["versions"]), 2)
        self.assertEqual(book.get("n1")["folder"], "archive")
