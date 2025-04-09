DROP TABLE IF EXISTS sells;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS bookstores;

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE book_authors (
    book_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (author_id) REFERENCES authors(id),
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE bookstores (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE sells (
    bookstore_id INTEGER,
    book_id INTEGER,
    price REAL NOT NULL,
    FOREIGN KEY (bookstore_id) REFERENCES bookstores(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    PRIMARY KEY (bookstore_id, book_id)
);