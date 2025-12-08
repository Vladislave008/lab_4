from abc import ABC, abstractmethod
from typing import Optional, Any
from src.constants import COLORS
from dataclasses import dataclass

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

class Index(ABC):
    """Базовый класс для всех типов индексов"""

    @abstractmethod
    def add(self, book: Book) -> None:
        """Добавить книгу в индекс"""
        pass

    @abstractmethod
    def remove(self, book: Book) -> None:
        """Удалить книгу из индекса"""
        pass

    @abstractmethod
    def search(self, key: Any) -> list[Book]:
        """Найти книги по ключу"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистить индекс"""
        pass

    @abstractmethod
    def count(self) -> int:
        """Количество уникальных ключей в индексе"""
        pass

    @abstractmethod
    def get_all(self) -> list[Book]:
        """Получить все книги из индекса"""
        pass


class AuthorIndex(Index):
    """Индекс по авторам"""

    def __init__(self):
        self.index: dict[str, list[Book]] = {}

    def add(self, book: Book) -> None:
        if book.author is not None:
            if book.author not in self.index:
                self.index[book.author] = []
            if book not in self.index[book.author]:
                self.index[book.author].append(book)

    def remove(self, book: Book) -> None:
        if book.author is not None and book.author in self.index:
            if book in self.index[book.author]:
                self.index[book.author].remove(book)
                if not self.index[book.author]:
                    del self.index[book.author]

    def search(self, author: str) -> list[Book]:
        return self.index.get(author, [])

    def clear(self) -> None:
        self.index.clear()

    def count(self) -> int:
        return len(self.index)

    def get_all(self) -> list[Book]:
        all_books = []
        for books_list in self.index.values():
            all_books.extend(books_list)
        return all_books

    def __repr__(self):
        return f"AuthorIndex({self.count()} authors)"

class YearIndex(Index):
    """Индекс по годам издания"""

    def __init__(self):
        self.index: dict[int, list[Book]] = {}

    def add(self, book: Book) -> None:
        if book.year is not None:
            if book.year not in self.index:
                self.index[book.year] = []
            if book not in self.index[book.year]:
                self.index[book.year].append(book)

    def remove(self, book: Book) -> None:
        if book.year is not None and book.year in self.index:
            if book in self.index[book.year]:
                self.index[book.year].remove(book)
                if not self.index[book.year]:
                    del self.index[book.year]

    def search(self, year: int) -> list[Book]:
        return self.index.get(year, [])

    def clear(self) -> None:
        self.index.clear()

    def count(self) -> int:
        return len(self.index)

    def get_all(self) -> list[Book]:
        all_books = []
        for books_list in self.index.values():
            all_books.extend(books_list)
        return all_books

    def __repr__(self):
        return f"YearIndex({self.count()} years)"

class GenreIndex(Index):
    """Индекс по жанрам"""

    def __init__(self):
        self.index: dict[str, list[Book]] = {}

    def add(self, book: Book) -> None:
        if book.genre is not None:
            if book.genre not in self.index:
                self.index[book.genre] = []
            if book not in self.index[book.genre]:
                self.index[book.genre].append(book)

    def remove(self, book: Book) -> None:
        if book.genre is not None and book.genre in self.index:
            if book in self.index[book.genre]:
                self.index[book.genre].remove(book)
                if not self.index[book.genre]:
                    del self.index[book.genre]

    def search(self, genre: str) -> list[Book]:
        return self.index.get(genre, [])

    def clear(self) -> None:
        self.index.clear()

    def count(self) -> int:
        return len(self.index)

    def get_all(self) -> list[Book]:
        all_books = []
        for books_list in self.index.values():
            all_books.extend(books_list)
        return all_books

    def __repr__(self):
        return f"GenreIndex({self.count()} genres)"

class TitleIndex(Index):
    """Индекс по названиям"""

    def __init__(self):
        self.index: dict[str, list[Book]] = {}

    def add(self, book: Book) -> None:
        if book.title is not None:
            if book.title not in self.index:
                self.index[book.title] = []
            if book not in self.index[book.title]:
                self.index[book.title].append(book)

    def remove(self, book: Book) -> None:
        if book.title is not None and book.title in self.index:
            if book in self.index[book.title]:
                self.index[book.title].remove(book)
                if not self.index[book.title]:
                    del self.index[book.title]

    def search(self, title: str) -> list[Book]:
        return self.index.get(title, [])

    def clear(self) -> None:
        self.index.clear()

    def count(self) -> int:
        return len(self.index)

    def get_all(self) -> list[Book]:
        all_books = []
        for books_list in self.index.values():
            all_books.extend(books_list)
        return all_books

    def __repr__(self):
        return f"TitleIndex({self.count()} titles)"

class IndexDict():
    def __init__(self):
        self.group_by_isbn: dict[str, Book] = {}
        self.group_by_title = TitleIndex()
        self.group_by_author = AuthorIndex()
        self.group_by_genre = GenreIndex()
        self.group_by_year = YearIndex()

    def __iter__(self):
        for isbn, book in self.group_by_isbn.items():
            yield book

    def add_book(self, book: Book) -> None:
        """Добавление книги во все индексы"""
        if (book.isbn is not None and book.author is not None and
            book.year is not None and book.genre is not None and
            book.title is not None):

            self.group_by_isbn[book.isbn] = book
            self.group_by_author.add(book)
            self.group_by_year.add(book)
            self.group_by_genre.add(book)
            self.group_by_title.add(book)

    def delete_book(self, book: Book) -> None:
        """Удаление книги из всех индексов"""
        if book.isbn in self.group_by_isbn:
            self.group_by_isbn.pop(book.isbn)

        self.group_by_author.remove(book)
        self.group_by_year.remove(book)
        self.group_by_genre.remove(book)
        self.group_by_title.remove(book)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.group_by_isbn.get(isbn)

    def get_by_author(self, author: str) -> list[Book]:
        return self.group_by_author.search(author)

    def get_by_title(self, title: str) -> list[Book]:
        return self.group_by_title.search(title)

    def get_by_genre(self, genre: str) -> list[Book]:
        return self.group_by_genre.search(genre)

    def get_by_year(self, year: int) -> list[Book]:
        return self.group_by_year.search(year)

    def book_count(self) -> int:
        return len(self.group_by_isbn)

    def author_count(self) -> int:
        return self.group_by_author.count()

    def year_count(self) -> int:
        return self.group_by_year.count()

    def genre_count(self) -> int:
        return self.group_by_genre.count()

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

        return f"{COLORS.RED}Cannot delete book '{book.title}': not found in collection '{self.collection_name}'{COLORS.RESET}"
        #raise LibraryException(f"Cannot delete book '{book.title}': not found in collection '{self.collection_name}')")

    def update_book(self, old_book: Book, new_book: Book) -> str:
        """Обновление данных книги с синхронизацией индексов"""
        if old_book.isbn != new_book.isbn:
            raise LibraryException("Cannot change ISBN. Use delete/add instead")
        self.validate_book(new_book)
        for i, (existing_book, count) in enumerate(self.items):
            if existing_book.isbn == old_book.isbn:
                self.items[i] = (new_book, count)
                self.index_dict.delete_book(old_book)
                self.index_dict.add_book(new_book)
                return f"{COLORS.GREEN}Updated book with ISBN '{old_book.isbn}' in collection '{self.collection_name}'{COLORS.RESET}"
        raise LibraryException(f"Can't update book '{old_book.title}': not found in collection")

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
                raise IndexError(f"Collection {self.collection_name} is empty")
            return self.items[key][0]
        elif isinstance(key, slice):
            return [i[0] for i in self.items[key]]
        elif isinstance(key, str):
            for book, count in self.items:
                if book.isbn == key:
                    return book
            raise KeyError(f"Book with ISBN '{key}' not found")
        else:
            raise TypeError("Invalid key type")

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for book, count in self.items:
            yield book

    def __repr__(self):
        if self.collection_name is not None:
            res = f"Collection '{self.collection_name}' Info:\n"
        else:
            res = "Collection Info:\n"
        for book, count in self.items:
            res += f"\tTitle: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available: {count} items\n"
        return res.strip()
