import unittest
from app import reserve


class Contract(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(reserve(5, 2), (3, True))

    def test_exact(self):
        self.assertEqual(reserve(5, 5), (0, True))

    def test_oversized(self):
        self.assertEqual(reserve(5, 6), (5, False))
        self.assertEqual(reserve(0, 1), (0, False))

    def test_invalid(self):
        for amount in (0, -1, -100):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                reserve(5, amount)
