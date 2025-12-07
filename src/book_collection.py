from dataclasses import dataclass
from typing import Optional

from src.constants import COLORS

class LibraryException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

@dataclass(frozen=True)
class Book():
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    isbn: Optional[str] = None

    def is_identical(self, other: 'Book') -> bool:
        """Сравнение двух книг на идентичность"""
        return (self.title == other.title and
                self.author == other.author and
                self.year == other.year and
                self.genre == other.genre and
                self.isbn == other.isbn)

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.is_identical(other)

    def __repr__(self):
        return f"The book '{self.title}', written by {self.author} in {self.year}"

    def __hash__(self):
        return hash((self.title, self.author, self.year, self.genre, self.isbn))

class IndexDict():
    def __init__(self):
        self.group_by_isbn: dict[str, Book] = {}
        self.group_by_title: dict[str, list[Book]] = {}
        self.group_by_author: dict[str, list[Book]] = {}
        self.group_by_genre: dict[str, list[Book]] = {}
        self.group_by_year: dict[int, list[Book]] = {}


    def __iter__(self):
        for isbn, book in self.group_by_isbn.items():
            yield book

    def add_book(self, book: Book) -> None:
        """Добавление книги"""
        title = book.title
        author = book.author
        year = book.year
        genre = book.genre
        isbn = book.isbn

        if isbn is not None and author is not None and year is not None and genre is not None and title is not None:
            self.group_by_isbn[isbn] = book

            if author not in self.group_by_author.keys():
                self.group_by_author[author] = []
            self.group_by_author[author].append(book)

            if year not in self.group_by_year.keys():
                self.group_by_year[year] = []
            self.group_by_year[year].append(book)

            if genre not in self.group_by_genre.keys():
                self.group_by_genre[genre] = []
            self.group_by_genre[genre].append(book)

            if title not in self.group_by_title.keys():
                self.group_by_title[title] = []
            self.group_by_title[title].append(book)


    def delete_book(self, book: Book) -> None:
        """Удаление книги"""
        title = book.title
        author = book.author
        year = book.year
        genre = book.genre
        isbn = book.isbn

        if isbn in self.group_by_isbn:
            self.group_by_isbn.pop(isbn)

        if author in self.group_by_author and book in self.group_by_author[author]:
            self.group_by_author[author].remove(book)
            if not self.group_by_author[author]:
                del self.group_by_author[author]

        if year in self.group_by_year and book in self.group_by_year[year]:
            self.group_by_year[year].remove(book)
            if not self.group_by_year[year]:
                del self.group_by_year[year]

        if genre in self.group_by_genre and book in self.group_by_genre[genre]:
            self.group_by_genre[genre].remove(book)
            if not self.group_by_genre[genre]:
                del self.group_by_genre[genre]

        if title in self.group_by_title and book in self.group_by_title[title]:
            self.group_by_title[title].remove(book)
            if not self.group_by_title[title]:
                del self.group_by_title[title]

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.group_by_isbn.get(isbn)

    def get_by_author(self, author: str) -> list[Book]:
        return self.group_by_author.get(author, [])

    def get_by_title(self, title: str) -> list[Book]:
        return self.group_by_title.get(title, [])

    def get_by_genre(self, genre: str) -> list[Book]:
        return self.group_by_genre.get(genre, [])

    def get_by_year(self, year: int) -> list[Book]:
        return self.group_by_year.get(year, [])

    def book_count(self) -> int:
        return len(self.group_by_isbn)

    def author_count(self) -> int:
        return len(self.group_by_author)

    def year_count(self) -> int:
        return len(self.group_by_year)

    def genre_count(self) -> int:
        return len(self.group_by_genre)

    def __len__(self) -> int:
        return len(self.group_by_isbn)


class BookCollection():
    def __init__(self, collection_name=None):
        self.index_dict = IndexDict()
        self.items: list[tuple] = [] # (book, count)
        self.collection_name = collection_name

    def __add__(self, other):
        new_collection = BookCollection()
        for book, count in self.items + other.items:
            new_collection.add_book(book, count)
        return new_collection

    def __setitem__(self, index: int, book: Book):
        if not isinstance(book, Book):
            raise LibraryException("Can only assign Book objects")
        old_book, old_count = self.items[index]
        self.index_dict.delete_book(old_book)
        self.items[index] = (book, old_count) # с сохранением количества
        self.index_dict.add_book(book)

    def validate_book(self, book: Book) -> None:
        """Валидация полученных полей"""
        title = book.title
        author = book.author
        year = book.year
        genre = book.genre
        isbn = book.isbn
        if not isinstance(title, str):
            raise LibraryException(f"Title must be a string, found {type(title)}: {title}")
        if not isinstance(author, str):
            raise LibraryException(f"Author must be a string, found {type(author)}: {author}")
        if not isinstance(genre, str):
            raise LibraryException(f"Genre must be a string, found {type(genre)}: {genre}")
        if not isinstance(isbn, str):
            raise LibraryException(f"Isbn must be a string, found {type(isbn)}: {isbn}")
        if not isinstance(year, int):
            raise LibraryException(f"Year must be an integer, found {type(year)}: {year}")

    def add_book(self, book: Book, count=1) -> str:
        """Добавление книги"""
        if count <= 0:
            raise LibraryException("Count must be positive")
        self.validate_book(book)
        for i, (existing_book, existing_count) in enumerate(self.items):
            if existing_book.isbn == book.isbn:
                if existing_book.is_identical(book):
                    self.items[i] = (existing_book, existing_count + count)
                    return f"{COLORS.GREEN}Book '{book.title}' is already in collection '{self.collection_name}', added items: {count}, summary items: {existing_count+count}{COLORS.RESET}"
                else:
                    raise LibraryException(
                        f"ISBN conflict: {book.isbn}\n"
                        f"Existing: {existing_book}\n"
                        f"New: {book}"
                    )
        self.items.append((book, count))
        self.index_dict.add_book(book)
        return f"{COLORS.GREEN}Book '{book.title}' added to collection '{self.collection_name}', number of items: {count}{COLORS.RESET}"

    def delete_book(self, book: Book, count=1)-> str:
        """Удаление книги"""
        if count <= 0:
            raise LibraryException("Count must be positive")
        for i, (existing_book, existing_count) in enumerate(self.items):
            if existing_book.isbn == book.isbn:
                if count < existing_count:
                    self.items[i] = (existing_book, existing_count - count)
                    return f"{COLORS.GREEN}Book '{book.title}' deleted from collection '{self.collection_name}', number of items deleted: {count}, number of items left: {existing_count-count}{COLORS.RESET}"
                elif count == existing_count:
                    self.items.pop(i)
                    self.index_dict.delete_book(book)
                    return f"{COLORS.GREEN}Book '{book.title}' deleted from collection '{self.collection_name}', deleted all available items: {count}{COLORS.RESET}"
                else:
                    self.items.pop(i)
                    self.index_dict.delete_book(book)
                    return f"{COLORS.YELLOW}Warning: Trying to delete book '{book.title}' from collection '{self.collection_name}' in count {count}\n\t Available items count: {existing_count}\n\t Deleting all...{COLORS.RESET}"

        #return f"{COLORS.RED}Cannot delete book '{book.title}': not found in collection '{self.collection_name}'{COLORS.RESET}"
        raise LibraryException(f"Cannot delete book '{book.title}': not found in collection '{self.collection_name}')")

    def get_all_books_with_counts(self)-> list[tuple]:
        """Получить полное содержание коллекции"""
        return self.items.copy()

    def get_count(self, book: Book)-> int:
        """Поулчить количество экземпляров книги"""
        for existing_book, count in self.items:
            if existing_book.isbn == book.isbn:
                return count
        return 0

    def total_count(self) -> int:
        """Поулчить общее число экземпляров"""
        return sum(count for book, count in self.items)

    def __contains__(self, book: Book):
        if book in [t[0] for t in self.items]:
            return True
        return False

    def __getitem__(self, key):
        if isinstance(key, int):
            if len(self.items) == 0:
                raise IndexError(f"Colection {self.collection_name} is empty")
            return self.items[key][0]
        elif isinstance(key, slice):
            return [i[0] for i in self.items[key]]
        elif isinstance(key, str):
            for book, count in self.items:
                if book.title == key:
                    return book
            raise KeyError(f"Book with title '{key}' not found")
        else:
            raise TypeError("Invalid key type")

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for book, count in self.items:
            yield book

    def __repr__(self):
        if self.collection_name is not None:
            res = f"Library '{self.collection_name}' Info:\n"
        else:
            res = "Library Info:\n"
        for book, count in self.items:
            res += f"\tTitle: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available: {count} items\n"
        return res.strip()
