import unittest

from api import book_response
from repository import Repository
from service import BookError, import_book, update_book


class Public(unittest.TestCase):
    def test_import_and_respond(self):
        repo = Repository()
        import_book(repo, {"isbn": "978-0-1", "title": " Dune ", "author": "Herbert"})
        self.assertEqual(book_response(repo, "97801")["title"], "Dune")

    def test_update_title(self):
        repo = Repository()
        import_book(repo, {"isbn": "1", "title": "A", "author": "B"})
        self.assertEqual(update_book(repo, "1", {"title": " C "})["title"], "C")

    def test_bad_isbn(self):
        with self.assertRaises(BookError):
            import_book(Repository(), {"isbn": "x1", "title": "A", "author": "B"})

    def test_unknown(self):
        self.assertIsNone(book_response(Repository(), "9"))
