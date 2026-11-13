import unittest
from app import label


class Public(unittest.TestCase):
    def test_label(self):
        self.assertEqual(label("x"), "cache:x")
