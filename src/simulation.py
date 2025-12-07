from src.library import Library
from src.book_database import BOOKS, AUTHORS, YEARS, GENRES
import random
import numpy as np #type: ignore
from src.constants import COLORS
from copy import deepcopy

class Simulator():
    def __init__(self):
        self.library = Library("Simulation Library")

    def add_book(self):
        try:
            print(self.library.collection.add_book(random.choice(BOOKS), count=random.randint(1,5)))
        except Exception as e:
            print(f"{COLORS.RED}Error found in add_book: {e}{COLORS.RESET}")

    def delete_book(self):
        books_available = [t[0] for t in self.library.collection.items]
        if not books_available:
            print(f"{COLORS.RED}Cannot perferm delete_book: no available books found{COLORS.RESET}")
            return
        try:
            index_before = deepcopy(self.library.collection.index_dict)
            print(self.library.collection.delete_book(random.choice(books_available), count=random.randint(1,5)))
            index_after = self.library.collection.index_dict
            print(f"\t{COLORS.GRAY}Index_dict length before delete: {len(index_before.group_by_isbn.values())}{COLORS.RESET}\n\t{COLORS.GRAY}Index_dict length after delete: {len(index_after.group_by_isbn.values())}{COLORS.RESET}")
        except Exception as e:
            print(f"{COLORS.RED}Error found in delete_book: {e}{COLORS.RESET}")

    def borrow_book(self):
        user_id = random.choice(self.users)
        count = random.randint(1,3)
        books_available = [t[0] for t in self.library.collection.items]
        if not books_available:
            print(f"{COLORS.RED}Cannot perferm borrow_book: no available books found{COLORS.RESET}")
            return
        try:
            print(self.library.borrow_books(random.choice(books_available), user_id, count))
        except Exception as e:
            print(f"{COLORS.RED}Error found in borrow_book: {e}{COLORS.RESET}")

    def borrow_book_non_existent(self):
        user_id = random.choice(self.users)
        count = random.randint(1,3)
        books_available = [t[0] for t in self.library.collection.items]
        try:
            print(self.library.borrow_books(random.choice([book for book in BOOKS if book not in books_available]), user_id, count))
        except Exception as e:
            print(f"{COLORS.RED}Error found in borrow_book_non_existent: {e}{COLORS.RESET}")

    def return_book(self):
        active_borrowers = self.library.get_active_borrowers()
        if not active_borrowers:
            print(f"{COLORS.RED}Cannot perferm return: no active borrowers found{COLORS.RESET}")
            return
        user_id = random.choice(self.library.get_active_borrowers())
        count = random.randint(1,3)
        try:
            b=list(self.library.borrowers[user_id].borrowed_books.keys())
            print(self.library.return_books(b[random.randint(0, len(b)-1)], user_id, count))
        except Exception as e:
            print(f"{COLORS.RED}Error found in return_book: {e}{COLORS.RESET}")

    def find_book_by_key(self):
        index_dict = self.library.collection.index_dict
        key_types = ["genre", "author", "year"]
        key = random.choice(key_types)
        try:
            match(key):
                case "genre":
                    genre = random.choice(GENRES)
                    res = index_dict.get_by_genre(genre)
                    print(f"{COLORS.CYAN}Found for genre key '{genre}': {res}{COLORS.RESET}")
                case "author":
                    author = random.choice(AUTHORS)
                    res = index_dict.get_by_author(author)
                    print(f"{COLORS.CYAN}Found for author key '{author}': {res}{COLORS.RESET}")
                case "year":
                    year = random.choice(YEARS)
                    res = index_dict.get_by_year(year)
                    print(f"{COLORS.CYAN}Found for year key '{year}': {res}{COLORS.RESET}")
        except Exception as e:
             print(f"{COLORS.RED}Error found in find_book_by_key: {e}{COLORS.RESET}")

    def run_simulation(self, steps: int = 20, seed: int | None = None) -> None:
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.users = np.random.choice(10000, size=50, replace=False)
        self.users = self.users.tolist()
        pre_add_n = random.randint(30,60)
        print(f"\n{COLORS.PINK}----------------- Pre-adding {pre_add_n} books to show functionality ----------------{COLORS.RESET}\n")
        for i in range(pre_add_n):
            self.add_book()
        print(f"\n{COLORS.PINK}---------------------- Making random actions (steps: {steps}) -----------------------{COLORS.RESET}\n")
        functions = [self.add_book, self.borrow_book, self.borrow_book_non_existent, self.delete_book, self.find_book_by_key, self.return_book]
        for i in range(steps):
            function = random.choice(functions)
            function()
        print(f"\n{COLORS.PINK}------------------------- Showing final library statistics --------------------------{COLORS.RESET}\n")
        print(f"Total borrowed: {self.library.statistics['total_borrowed']}\nTotal returned: {self.library.statistics['total_returned']}\nUnique borrowers: {self.library.statistics['unique_borrowers']}\nActive borrowers: {self.library.statistics['active_borrowers']}")
        print(f"Most popular books (live, for borrow): {[book[0].title for book in self.library.get_most_borrowed_books(3)]}")
        print(f"Top borrowers (live): {[borrower[0] for borrower in self.library.get_top_borrowers(3)]}")
        print(f"\n{COLORS.PINK}-------------------------------------------------------------------------------------{COLORS.RESET}\n")
