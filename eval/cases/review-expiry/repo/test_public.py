import unittest
from app import expired


class Public(unittest.TestCase):
    def test_later(self):
        self.assertTrue(expired(11, 10))
