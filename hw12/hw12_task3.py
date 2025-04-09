import sqlite3

def find_books_by_author(author_name: str, db_path: str) -> list:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = """
    SELECT books.title
    FROM books
    JOIN book_authors ON books.id = book_authors.book_id
    JOIN authors ON book_authors.author_id = authors.id
    WHERE authors.name = ?
    """
    cur.execute(query, (author_name,))
    books = cur.fetchall()
    conn.close()
    return [book[0] for book in books]

def find_books_by_publisher_and_year(publisher_name: str, year: int, db_path: str) -> list:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = """
    SELECT title
    FROM books
    WHERE publisher = ? AND year = ?
    """
    cur.execute(query, (publisher_name, year))
    books = cur.fetchall()
    conn.close()
    return [book[0] for book in books]

def average_price_by_author(author_name: str, db_path: str) -> float:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = """
    SELECT AVG(sells.price)
    FROM sells
    JOIN books ON sells.book_id = books.id
    JOIN book_authors ON books.id = book_authors.book_id
    JOIN authors ON book_authors.author_id = authors.id
    WHERE authors.name = ?
    """
    cur.execute(query, (author_name,))
    result = cur.fetchone()[0]
    conn.close()
    return result if result is not None else 0.0

if __name__ == "__main__":
    db_path = "bookstore.db"
    print("Books by Harper Lee:", find_books_by_author("Harper Lee", db_path))
    print("Books by Secker & Warburg in 1949:", find_books_by_publisher_and_year("Secker & Warburg", 1949, db_path))
    print("Average price for J.R.R. Tolkien:", average_price_by_author("J.R.R. Tolkien", db_path))
