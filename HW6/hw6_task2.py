#Task 2
class LibraryMember:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name= name
        self.borrowed_books =[] #able to store values

    def add_book(self, book_title):
        self. borrowed_books.append(book_title)
    def remove_book(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
    def count_books(self):
        return len(self.borrowed_books)
    def __str__(self): #how it is going to be read
        return f"Library member(member_id = {self.member_id}, name = {self.name}, total_borrowed = {self.count_books()})"
    def __repr__(self):
        return self.__str__()
alice= LibraryMember("001", "Alice")

alice.add_book("The Great Gatsby")

print(alice)
