import unittest

from api import book_response
from repository import Repository
from service import import_book, update_book

BOOK = {"isbn": "1", "title": "Dune", "author": "Herbert"}


class SeriesAndTags(unittest.TestCase):
    def test_round_trip(self):
        repo = Repository()
        import_book(repo, {**BOOK, "series": " Dune Chronicles ", "tags": [" SciFi", "classic", "scifi", ""]})
        body = book_response(repo, "1")
        self.assertEqual(body["series"], "Dune Chronicles")
        self.assertEqual(body["tags"], ["scifi", "classic"])

    def test_defaults(self):
        repo = Repository()
        import_book(repo, {**BOOK, "series": "  "})
        body = book_response(repo, "1")
        self.assertIsNone(body["series"])
        self.assertEqual(body["tags"], [])

    def test_update_tags_only(self):
        repo = Repository()
        import_book(repo, {**BOOK, "series": "Dune"})
        update_book(repo, "1", {"tags": ["Epic"]})
        body = book_response(repo, "1")
        self.assertEqual((body["series"], body["tags"]), ("Dune", ["epic"]))

    def test_update_clears_series(self):
        repo = Repository()
        import_book(repo, {**BOOK, "series": "Dune"})
        update_book(repo, "1", {"series": ""})
        self.assertIsNone(book_response(repo, "1")["series"])

    def test_old_rows_still_load(self):
        repo = Repository([("1", "Dune", "Herbert")])  # written by the previous release
        body = book_response(repo, "1")
        self.assertEqual((body["title"], body["series"], body["tags"]), ("Dune", None, []))
        update_book(repo, "1", {"title": "Dune Messiah"})
        self.assertEqual(book_response(repo, "1")["tags"], [])

    def test_tag_lists_not_shared(self):
        repo = Repository([("1", "Dune", "Herbert"), ("2", "Emma", "Austen")])
        book_response(repo, "1")["tags"].append("x")
        self.assertEqual(book_response(repo, "2")["tags"], [])
        self.assertEqual(book_response(repo, "1")["tags"], [])


class Existing(unittest.TestCase):
    def test_plain_book(self):
        repo = Repository()
        import_book(repo, BOOK)
        self.assertEqual(book_response(repo, "1")["links"], {"self": "/books/1"})
