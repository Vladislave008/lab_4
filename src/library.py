from src.book_collection import BookCollection, Book, LibraryException
from dataclasses import dataclass
from datetime import datetime
from src.constants import COLORS
from typing import Optional

@dataclass
class BorrowerInfo:
    user_id: int
    borrowed_books: dict  # book: count
    total_borrowed: int = 0
    total_returned: int = 0
    first_borrow_date: Optional[datetime] = None
    last_activity_date: Optional[datetime] = None

class Library:
    def __init__(self, library_name: str = "Unnamed Library"):
        self.name: str = library_name
        self.collection: BookCollection = BookCollection(library_name)
        self.borrowed_books: dict = {}  # book: {user_id: count}
        self.borrowers: dict = {}       # user_id: BorrowerInfo
        self.statistics: dict = {
            'total_borrowed': 0,
            'total_returned': 0,
            'unique_borrowers': 0,
            'active_borrowers': 0
        }

    def borrow_books(self, book: Book, user_id: int, count: int = 1) -> str:
        """Выдача нескольких экземпляров книги читателю"""
        if count <= 0:
            raise LibraryException("Count must be positive")
        if book not in self.collection:
            return f"{COLORS.RED}Book '{book.title}' not available{COLORS.RESET}"
        current_count = self.collection.get_count(book)
        if current_count < count:
            return f"{COLORS.RED}Not enough copies of '{book.title}'. Available: {current_count}, requested: {count}{COLORS.RESET}"

        if book not in self.borrowed_books:
            self.borrowed_books[book] = {}
        current_borrowed = self.borrowed_books[book].get(user_id, 0)
        self.borrowed_books[book][user_id] = current_borrowed + count

        if user_id not in self.borrowers:
            self.statistics['active_borrowers']+=1
            self.borrowers[user_id] = BorrowerInfo(
                user_id=user_id,
                borrowed_books={},
                first_borrow_date=datetime.now()
            )
            self.statistics['unique_borrowers'] += 1
        borrower = self.borrowers[user_id]
        borrower.borrowed_books[book] = borrower.borrowed_books.get(book, 0) + count
        borrower.total_borrowed += count
        borrower.last_activity_date = datetime.now()

        self.collection.delete_book(book, count)
        self.statistics['total_borrowed'] += count
        return f"{COLORS.GREEN}Borrowed {count} copy/copies of '{book.title}' for user {user_id}{COLORS.RESET}"

    def return_books(self, book: Book, user_id: int, count: int = 1) -> str:
        """Возврат нескольких экземпляров книги"""
        if count <= 0:
            raise LibraryException("Count must be positive")
        if book not in self.borrowed_books or user_id not in self.borrowed_books[book]:
            return f"{COLORS.RED}User {user_id} has no copies of '{book.title}' borrowed{COLORS.RESET}"

        current_borrowed = self.borrowed_books[book][user_id]
        if current_borrowed < count:
            return f"{COLORS.RED}User {user_id} has only {current_borrowed} copies of '{book.title}' borrowed, but trying to return {count}{COLORS.RESET}"

        self.borrowed_books[book][user_id] -= count
        if self.borrowed_books[book][user_id] == 0:
            del self.borrowed_books[book][user_id]
        if not self.borrowed_books[book]:
            del self.borrowed_books[book]

        if user_id in self.borrowers:
            borrower = self.borrowers[user_id]
            borrower.borrowed_books[book] -= count
            borrower.total_returned += count
            borrower.last_activity_date = datetime.now()

            if borrower.borrowed_books[book] == 0:
                del borrower.borrowed_books[book]
            if len(borrower.borrowed_books) == 0:
                del self.borrowers[user_id]
                self.statistics['active_borrowers']-=1

        self.collection.add_book(book, count)
        self.statistics['total_returned'] += count

        return f"{COLORS.GREEN}Returned {count} copy/copies of '{book.title}' from user {user_id}{COLORS.RESET}"

    def get_user_borrowed_books(self, user_id: int) -> dict:
        """Получить все книги, выданные пользователю"""
        if user_id in self.borrowers:
            return self.borrowers[user_id].borrowed_books.copy()
        return {}

    def get_borrower_info(self, user_id: int):
        """Полная информация о читателе"""
        return self.borrowers.get(user_id)

    def get_active_borrowers(self) -> list:
        """Активные читатели (у которых есть книги на руках)"""
        return [
            user_id
            for user_id, borrower in self.borrowers.items()
            if borrower.borrowed_books
        ]

    def get_book_borrow_info(self, book: Book) -> dict:
        """Получить информацию о выдаче конкретной книги"""
        if book not in self.borrowed_books:
            return {
                'available': self.collection.get_count(book),
                'borrowed': 0,
                'total_copies': self.collection.get_count(book),
                'users': {}
            }

        total_borrowed = sum(self.borrowed_books[book].values())
        return {
            'available': self.collection.get_count(book),
            'borrowed': total_borrowed,
            'total_copies': self.collection.get_count(book) + total_borrowed,
            'users': self.borrowed_books[book].copy()
        }

    def get_popular_books(self, limit=5)  -> list:
        """Самые популярные книги (по количеству экземпляров)"""
        books_with_counts = self.collection.get_all_books_with_counts()
        return sorted(books_with_counts, key=lambda x: x[1], reverse=True)[:limit]

    def generate_report(self) -> dict:
        """Генерация отчета"""
        return {
            'library_name': self.name,
            'unique_books': len(self.collection),
            'total_copies': self.collection.total_count(),
            'authors_count': self.collection.index_dict.author_count(),
            'genres_count': self.collection.index_dict.genre_count(),
            'statistics': self.statistics.copy()
        }

    def __repr__(self):
        return (f"Library '{self.name}' ({len(self.collection)} books, "
                f"{self.collection.total_count()} copies available, {self.statistics['total_borrowed']} total borrowed, "
                f"{self.statistics['active_borrowers']} active borrowers)")

    def get_available_books(self) -> list:
        """Получить все доступные книги"""
        return [book for book, count in self.collection.items if count > 0]

    def is_book_available(self, book: Book, count: int = 1) -> bool:
        """Доступна ли книга в нужном количестве"""
        return (book in self.collection and
                self.collection.get_count(book) >= count)

    def get_most_borrowed_books(self, limit=5) -> list:
        """Самые популярные книги по количеству выдач"""
        book_borrow_counts = []
        for book, users in self.borrowed_books.items():
            total_borrowed = sum(users.values())
            book_borrow_counts.append((book, total_borrowed))
        return sorted(book_borrow_counts, key=lambda x: x[1], reverse=True)[:limit]

    def get_top_borrowers(self, limit=5) -> list:
        """Самые активные читатели на текущий момент"""
        borrowers_with_counts = [
            (user_id, sum(borrower.borrowed_books.values()))
            for user_id, borrower in self.borrowers.items()
        ]
        return sorted(borrowers_with_counts, key=lambda x: x[1], reverse=True)[:limit]

    def get_borrower_history(self, user_id: int) -> None | dict:
        """История выдачи/возврата для читателя"""
        if user_id not in self.borrowers:
            return None

        borrower = self.borrowers[user_id]
        return {
            'user_id': user_id,
            'currently_borrowed': borrower.borrowed_books.copy(),
            'total_borrowed': borrower.total_borrowed,
            'total_returned': borrower.total_returned,
            'first_borrow_date': borrower.first_borrow_date,
            'last_activity_date': borrower.last_activity_date
        }
