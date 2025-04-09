-- Insert sample data into the books table
INSERT INTO books (id, title, publisher, year) VALUES
(1, 'The Great Gatsby', 'Scribner', 1925),
(2, 'To Kill a Mockingbird', 'J.B. Lippincott & Co.', 1960),
(3, '1984', 'Secker & Warburg', 1949),
(4, 'Pride and Prejudice', 'T. Egerton', 1813),
(5, 'The Catcher in the Rye', 'Little, Brown and Company', 1951),
(6, 'American Gods', 'William Morrow', 2001),
(7, 'Coraline', 'HarperCollins', 2002),
(8, 'The Ocean at the End of the Lane', 'William Morrow', 2013),
(9, 'Good Omens', 'Gollancz', 1990),
(10, 'Neverwhere', 'BBC Books', 1996),
(11, 'The Hobbit', 'George Allen & Unwin', 1937),
(12, 'The Lord of the Rings', 'George Allen & Unwin', 1954),
(13, 'Fahrenheit 451', 'Ballantine Books', 1953),
(14, 'Brave New World', 'Chatto & Windus', 1932),
(15, 'The Hitchhiker''s Guide to the Galaxy', 'Pan Books', 1979);

-- Insert sample data into the authors table
INSERT INTO authors (id, name) VALUES
(1, 'F. Scott Fitzgerald'),
(2, 'Harper Lee'),
(3, 'George Orwell'),
(4, 'Jane Austen'),
(5, 'J.D. Salinger'),
(6, 'Neil Gaiman'),
(7, 'J.R.R. Tolkien'),
(8, 'Ray Bradbury'),
(9, 'Aldous Huxley'),
(10, 'Douglas Adams');

-- Insert sample data into the book_authors table
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1),  -- The Great Gatsby by F. Scott Fitzgerald
(2, 2),  -- To Kill a Mockingbird by Harper Lee
(3, 3),  -- 1984 by George Orwell
(4, 4),  -- Pride and Prejudice by Jane Austen
(5, 5),  -- The Catcher in the Rye by J.D. Salinger
(6, 6),  -- American Gods by Neil Gaiman
(7, 6),  -- Coraline by Neil Gaiman
(8, 6),  -- The Ocean at the End of the Lane by Neil Gaiman
(9, 6),  -- Good Omens by Neil Gaiman
(10, 6), -- Neverwhere by Neil Gaiman
(11, 7), -- The Hobbit by J.R.R. Tolkien
(12, 7), -- The Lord of the Rings by J.R.R. Tolkien
(13, 8), -- Fahrenheit 451 by Ray Bradbury
(14, 9), -- Brave New World by Aldous Huxley
(15, 10); -- The Hitchhiker's Guide to the Galaxy by Douglas Adams

-- Insert sample data into the bookstores table
INSERT INTO bookstores (id, name, address) VALUES
(1, 'City Bookstore', '123 Main St, Anytown, USA'),
(2, 'Readers Haven', '456 Elm St, Anytown, USA'),
(3, 'The Book Nook', '789 Oak St, Anytown, USA');

-- Insert sample data into the sells table
INSERT INTO sells (bookstore_id, book_id, price) VALUES
(1, 1, 10.99),  -- City Bookstore sells The Great Gatsby for $10.99
(1, 2, 12.99),  -- City Bookstore sells To Kill a Mockingbird for $12.99
(2, 3, 15.99),  -- Readers Haven sells 1984 for $15.99
(2, 4, 9.99),   -- Readers Haven sells Pride and Prejudice for $9.99
(3, 5, 14.99),  -- The Book Nook sells The Catcher in the Rye for $14.99
(3, 1, 11.99);  -- The Book Nook sells The Great Gatsby for $11.99
