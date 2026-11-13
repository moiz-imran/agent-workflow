import unittest
from app import copy_document, move_document, save_document


class Contract(unittest.TestCase):
    def setUp(self):
        self.doc = {"body": "hello world", "folder": "a", "followers": ["reader"]}

    def test_copy(self):
        copied = copy_document(self.doc, "b")
        self.assertEqual(copied["followers"], [])
        copied["followers"].append("other")
        self.assertEqual(self.doc, {"body": "hello world", "folder": "a", "followers": ["reader"]})

    def test_move(self):
        self.assertEqual(move_document(self.doc, "b"), [])
        self.assertEqual(self.doc["followers"], ["reader"])
        self.assertEqual(self.doc["folder"], "b")

    def test_format(self):
        self.assertEqual(save_document(self.doc, " hello\nworld  "), [])
        self.assertEqual(self.doc["body"], " hello\nworld  ")

    def test_content(self):
        self.assertEqual(save_document(self.doc, "new words"), ["reader"])
