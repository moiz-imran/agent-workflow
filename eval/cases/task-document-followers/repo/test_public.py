import unittest
from app import copy_document


class Public(unittest.TestCase):
    def test_copy_folder(self):
        self.assertEqual(copy_document({"body": "a", "folder": "x", "followers": []}, "y")["folder"], "y")
