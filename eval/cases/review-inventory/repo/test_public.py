import unittest
from app import reserve


class Public(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(reserve(5, 2), (3, True))
