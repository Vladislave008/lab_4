from unittest.mock import patch
from datetime import datetime
from src.library import Library, Book

class TestLibrary:
    def test_library_initialization(self):
        lib = Library("Test Library")
        assert lib.name == "Test Library"
        assert len(lib.collection) == 0
        assert lib.statistics['total_borrowed'] == 0

    def test_borrow_books_success(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 3)
        result = lib.borrow_books(book, 123, 2)

        assert "Borrowed" in result
        assert lib.collection.get_count(book) == 1
        assert lib.statistics['total_borrowed'] == 2
        assert lib.statistics['active_borrowers'] == 1

    def test_borrow_books_not_available(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")
        assert "not available" in lib.borrow_books(book, 123, 1)

    def test_borrow_books_not_enough_copies(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 1)

        assert "Not enough copies" in lib.borrow_books(book, 123, 2)

    def test_return_books_success(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 3)
        lib.borrow_books(book, 123, 2)

        result = lib.return_books(book, 123, 1)

        assert "Returned" in result
        assert lib.collection.get_count(book) == 2
        assert lib.statistics['total_returned'] == 1
        assert 123 in lib.borrowers

    def test_return_books_not_borrowed(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 1)

        assert "has no copies" in lib.return_books(book, 123, 1)

    def test_get_user_borrowed_books(self):
        lib = Library()
        book1 = Book("Title1", "Author", 2020, "Fiction", "1")
        book2 = Book("Title2", "Author", 2021, "Fiction", "2")

        lib.collection.add_book(book1, 2)
        lib.collection.add_book(book2, 2)

        lib.borrow_books(book1, 123, 1)
        lib.borrow_books(book2, 123, 2)

        borrowed = lib.get_user_borrowed_books(123)
        assert book1 in borrowed
        assert book2 in borrowed
        assert borrowed[book1] == 1
        assert borrowed[book2] == 2

    def test_get_active_borrowers(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 5)

        lib.borrow_books(book, 123, 1)
        lib.borrow_books(book, 456, 2)

        active = lib.get_active_borrowers()
        assert 123 in active
        assert 456 in active
        assert len(active) == 2

    def test_get_book_borrow_info(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 5)
        lib.borrow_books(book, 123, 2)
        lib.borrow_books(book, 456, 1)

        info = lib.get_book_borrow_info(book)

        assert info['available'] == 2
        assert info['borrowed'] == 3
        assert info['total_copies'] == 5
        assert info['users'][123] == 2
        assert info['users'][456] == 1

    def test_is_book_available(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        assert not lib.is_book_available(book)

        lib.collection.add_book(book, 3)
        assert lib.is_book_available(book)
        assert lib.is_book_available(book, 2)
        assert not lib.is_book_available(book, 4)

    def test_get_most_borrowed_books(self):
        lib = Library()
        book1 = Book("Title1", "Author", 2020, "Fiction", "1")
        book2 = Book("Title2", "Author", 2021, "Fiction", "2")

        lib.collection.add_book(book1, 10)
        lib.collection.add_book(book2, 10)

        lib.borrow_books(book1, 123, 5)
        lib.borrow_books(book1, 456, 3)
        lib.borrow_books(book2, 789, 2)

        top_books = lib.get_most_borrowed_books(2)
        assert len(top_books) == 2
        assert top_books[0][0] == book1
        assert top_books[0][1] == 8
        assert top_books[1][0] == book2
        assert top_books[1][1] == 2

    def test_get_top_borrowers(self):
        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 10)

        lib.borrow_books(book, 123, 5)
        lib.borrow_books(book, 456, 3)
        lib.borrow_books(book, 789, 1)

        top_borrowers = lib.get_top_borrowers(2)
        assert len(top_borrowers) == 2
        assert top_borrowers[0][0] == 123
        assert top_borrowers[0][1] == 5
        assert top_borrowers[1][0] == 456
        assert top_borrowers[1][1] == 3

    def test_generate_report(self):
        lib = Library("Test Lib")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 5)
        lib.borrow_books(book, 123, 2)

        report = lib.generate_report()

        assert report['library_name'] == "Test Lib"
        assert report['unique_books'] == 1
        assert report['total_copies'] == 3
        assert report['statistics']['total_borrowed'] == 2

    @patch('src.library.datetime')
    def test_borrower_history(self, mock_datetime):
        fixed_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time

        lib = Library()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 3)
        lib.borrow_books(book, 123, 2)

        history = lib.get_borrower_history(123)

        assert history['user_id'] == 123
        assert history['total_borrowed'] == 2
        assert history['total_returned'] == 0
        assert history['first_borrow_date'] == fixed_time
        assert history['last_activity_date'] == fixed_time
        assert book in history['currently_borrowed']

    def test_repr(self):
        lib = Library("My Library")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        lib.collection.add_book(book, 3)
        lib.borrow_books(book, 123, 1)

        repr_str = repr(lib)
        assert "My Library" in repr_str
        assert "1 books" in repr_str
        assert "2 copies available" in repr_str
