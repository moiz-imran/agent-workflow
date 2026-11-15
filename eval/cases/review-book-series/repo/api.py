"""Public response shapes."""


def book_response(repo, isbn):
    book = repo.load(str(isbn).replace("-", ""))
    if book is None:
        return None
    return {"isbn": book["isbn"], "title": book["title"], "author": book["author"],
            "links": {"self": f"/books/{book['isbn']}"}}
