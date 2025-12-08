import pytest # type: ignore
from src.book_collection import Book, BookCollection, IndexDict, LibraryException

class TestBook:
    def test_book_creation(self):
        book = Book("Title", "Author", 2020, "Fiction", "12345")
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.year == 2020
        assert book.genre == "Fiction"
        assert book.isbn == "12345"

    def test_book_equality(self):
        book1 = Book("Title", "Author", 2020, "Fiction", "12345")
        book2 = Book("Title", "Author", 2020, "Fiction", "12345")
        book3 = Book("Different", "Author", 2020, "Fiction", "12345")

        assert book1 == book2
        assert book1 != book3

    def test_book_hash(self):
        book1 = Book("Title", "Author", 2020, "Fiction", "12345")
        book2 = Book("Title", "Author", 2020, "Fiction", "12345")
        assert hash(book1) == hash(book2)

class TestIndexDict:
    def test_add_and_get_book(self):
        index = IndexDict()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        index.add_book(book)

        assert index.get_by_isbn("12345") == book
        assert index.get_by_author("Author") == [book]
        assert index.get_by_year(2020) == [book]
        assert index.get_by_genre("Fiction") == [book]
        assert index.get_by_title("Title") == [book]

    def test_delete_book(self):
        index = IndexDict()
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        index.add_book(book)
        assert len(index) == 1

        index.delete_book(book)
        assert len(index) == 0
        assert index.get_by_isbn("12345") is None

    def test_iteration(self):
        index = IndexDict()
        books = [
            Book("Title1", "Author1", 2020, "Fiction", "1"),
            Book("Title2", "Author2", 2021, "Non-Fiction", "2")
        ]

        for book in books:
            index.add_book(book)

        assert list(index) == books

    def test_multiple_books_same_author(self):
        index = IndexDict()
        book1 = Book("Title1", "Author", 2020, "Fiction", "1")
        book2 = Book("Title2", "Author", 2021, "Fiction", "2")

        index.add_book(book1)
        index.add_book(book2)

        assert len(index.get_by_author("Author")) == 2

class TestBookCollection:
    def test_add_book(self):
        collection = BookCollection("Test")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        result = collection.add_book(book, 3)
        assert "added to collection" in result
        assert len(collection) == 1
        assert collection.total_count() == 3

    def test_add_duplicate_book_increases_count(self):
        collection = BookCollection("Test")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        collection.add_book(book, 2)
        result = collection.add_book(book, 3)

        assert "already in collection" in result
        assert collection.total_count() == 5
        assert collection.get_count(book) == 5

    def test_isbn_conflict_raises_exception(self):
        collection = BookCollection("Test")
        book1 = Book("Title1", "Author1", 2020, "Fiction", "12345")
        book2 = Book("Title2", "Author2", 2021, "Non-Fiction", "12345")

        collection.add_book(book1, 1)

        with pytest.raises(LibraryException, match="ISBN conflict"):
            collection.add_book(book2, 1)

    def test_delete_book(self):
        collection = BookCollection("Test")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        collection.add_book(book, 5)
        result = collection.delete_book(book, 2)

        assert "deleted from collection" in result
        assert collection.total_count() == 3

    def test_delete_all_copies(self):
        collection = BookCollection("Test")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        collection.add_book(book, 3)
        result = collection.delete_book(book, 3)

        assert "deleted all available items" in result
        assert len(collection) == 0

    def test_delete_nonexistent_book(self):
        collection = BookCollection("Test")
        book = Book("Title", "Author", 2020, "Fiction", "12345")
        assert "not found in collection" in collection.delete_book(book, 1)

    def test_update_book_success(self):
        collection = BookCollection("Test")
        old_book = Book("Old Title", "Old Author", 2020, "Fiction", "12345")
        new_book = Book("New Title", "New Author", 2021, "Non-Fiction", "12345")
        collection.add_book(old_book, 3)
        result = collection.update_book(old_book, new_book)
        assert "Updated book" in result
        assert len(collection) == 1
        assert collection.total_count() == 3
        assert collection["12345"] == new_book
        assert old_book not in collection
        assert new_book in collection

    def test_update_book_isbn_conflict(self):
        collection = BookCollection("Test")
        old_book = Book("Title", "Author", 2020, "Fiction", "12345")
        new_book = Book("New Title", "New Author", 2021, "Non-Fiction", "67890")
        collection.add_book(old_book, 1)
        with pytest.raises(LibraryException, match="Cannot change ISBN"):
            collection.update_book(old_book, new_book)
        assert collection["12345"] == old_book

    def test_update_book_not_found(self):
        collection = BookCollection("Test")
        old_book = Book("Title", "Author", 2020, "Fiction", "12345")
        new_book = Book("New Title", "New Author", 2021, "Non-Fiction", "12345")
        with pytest.raises(LibraryException, match="not found in collection"):
            collection.update_book(old_book, new_book)

    def test_update_book_syncs_indexes(self):
        collection = BookCollection("Test")
        old_book = Book("Old Title", "Old Author", 2020, "Old Genre", "12345")
        new_book = Book("New Title", "New Author", 2021, "New Genre", "12345")
        collection.add_book(old_book, 1)
        assert len(collection.index_dict.get_by_author("Old Author")) == 1
        assert len(collection.index_dict.get_by_genre("Old Genre")) == 1
        assert len(collection.index_dict.get_by_year(2020)) == 1
        assert len(collection.index_dict.get_by_title("Old Title")) == 1
        collection.update_book(old_book, new_book)
        assert len(collection.index_dict.get_by_author("New Author")) == 1
        assert len(collection.index_dict.get_by_genre("New Genre")) == 1
        assert len(collection.index_dict.get_by_year(2021)) == 1
        assert len(collection.index_dict.get_by_title("New Title")) == 1
        assert len(collection.index_dict.get_by_author("Old Author")) == 0
        assert len(collection.index_dict.get_by_genre("Old Genre")) == 0

    def test_update_book_with_multiple_copies(self):
        collection = BookCollection("Test")
        old_book = Book("Title", "Author", 2020, "Fiction", "12345")
        new_book = Book("Updated Title", "Updated Author", 2021, "Non-Fiction", "12345")
        collection.add_book(old_book, 5)
        result = collection.update_book(old_book, new_book)
        assert "Updated book" in result
        assert collection.get_count(new_book) == 5
        assert collection.total_count() == 5

    def test_getitem_by_index(self):
        collection = BookCollection("Test")
        book1 = Book("Title1", "Author1", 2020, "Fiction", "1")
        book2 = Book("Title2", "Author2", 2021, "Non-Fiction", "2")

        collection.add_book(book1, 1)
        collection.add_book(book2, 1)

        assert collection[0] == book1
        assert collection[1] == book2

    def test_getitem_by_slice(self):
        collection = BookCollection("Test")
        books = [
            Book(f"Title{i}", f"Author{i}", 2000+i, "Fiction", str(i))
            for i in range(5)
        ]

        for book in books:
            collection.add_book(book, 1)

        slice_result = collection[1:3]
        assert len(slice_result) == 2
        assert slice_result[0] == books[1]
        assert slice_result[1] == books[2]

    def test_getitem_by_isbn(self):
        collection = BookCollection("Test")
        book = Book("Specific Title", "Author", 2020, "Fiction", "12345")

        collection.add_book(book, 1)
        assert collection["12345"] == book

        with pytest.raises(KeyError, match="not found"):
            collection["Nonexistent isbn"]

    def test_contains(self):
        collection = BookCollection("Test")
        book = Book("Title", "Author", 2020, "Fiction", "12345")

        assert book not in collection
        collection.add_book(book, 1)
        assert book in collection

    def test_iteration(self):
        collection = BookCollection("Test")
        books = [
            Book(f"Title{i}", f"Author{i}", 2000+i, "Fiction", str(i))
            for i in range(3)
        ]

        for book in books:
            collection.add_book(book, 1)

        assert list(collection) == books

    def test_len(self):
        collection = BookCollection("Test")
        assert len(collection) == 0

        collection.add_book(Book("Title1", "Author1", 2020, "Fiction", "1"), 1)
        assert len(collection) == 1

        collection.add_book(Book("Title2", "Author2", 2021, "Fiction", "2"), 1)
        assert len(collection) == 2

    def test_add_collections(self):
        coll1 = BookCollection("Coll1")
        coll2 = BookCollection("Coll2")

        book1 = Book("Title1", "Author1", 2020, "Fiction", "1")
        book2 = Book("Title2", "Author2", 2021, "Fiction", "2")

        coll1.add_book(book1, 2)
        coll2.add_book(book2, 3)

        combined = coll1 + coll2
        assert len(combined) == 2
        assert combined.total_count() == 5

    def test_setitem(self):
        collection = BookCollection("Test")
        book1 = Book("Old", "Author", 2020, "Fiction", "12345")
        book2 = Book("New", "Author", 2021, "Non-Fiction", "67890")

        collection.add_book(book1, 2)
        collection[0] = book2

        assert collection[0] == book2
        assert collection.total_count() == 2

        with pytest.raises(LibraryException, match="Can only assign Book objects"):
            collection[0] = "not a book"

    def test_validation(self):
        collection = BookCollection("Test")

        with pytest.raises(LibraryException, match="must be a string"):
            collection.add_book(Book(title=123, author="Author", year=2020, genre="Fiction", isbn="123"), 1)

        with pytest.raises(LibraryException, match="must be an integer"):
            collection.add_book(Book(title="Title", author="Author", year="2020", genre="Fiction", isbn="123"), 1)

        with pytest.raises(LibraryException, match="must be positive"):
            collection.add_book(Book("Title", "Author", 2020, "Fiction", "123"), 0)
