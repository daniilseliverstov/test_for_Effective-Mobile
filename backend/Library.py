import json
from typing import List, Protocol
from backend.Book import Book


class IBookStorage(Protocol):
    def load_books(self) -> List[Book]:
        pass

    def save_books(self, books: List[Book]) -> None:
        pass


class Library:
    def __init__(self, storage: IBookStorage) -> None:
        """Инициализирует объект библиотеки.

        Args:
            storage (IBookStorage): Хранилище для книг.
        """
        self.storage: IBookStorage = storage
        self.books: List[Book] = self.storage.load_books()

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку."""
        book = Book(title, author, year)
        self.books.append(book)
        self.storage.save_books(self.books)
        print(f'Книга "{title}" добавлена с ID {book.id}.')

    def remove_book(self, book_id: str) -> None:
        """Удаляет книгу из библиотеки по её ID."""
        book = next((b for b in self.books if b.id == book_id), None)
        if book:
            self.books.remove(book)
            self.storage.save_books(self.books)
            print(f'Книга "{book.title}" c ID {book_id} удалена')
        else:
            print(f'Книга с ID {book_id} не найдена.')

    def search_books(self, field: str, value: str) -> List[Book]:
        """Ищет книги по заданному полю и значению."""
        if field not in {"title", "author", "year"}:
            print("Некорректное поле для поиска. Используйте 'title', 'author' или 'year'.")
            return []

        if field == "year":
            value = str(value)
        results = [book for book in self.books if str(getattr(book, field, '')).lower() == value.lower()]
        if results:
            for book in results:
                print(book.to_dict())
        else:
            print('Ничего не найдено.')
        return results

    def display_books(self) -> None:
        """Отображает все книги в библиотеке."""
        if self.books:
            for book in self.books:
                print(book.to_dict())
        else:
            print('Библиотека пуста')

    def update_status(self, book_id: str, new_status: str) -> None:
        """Обновляет статус книги."""
        book = next((b for b in self.books if b.id == book_id), None)
        if book:
            book.status = new_status
            self.storage.save_books(self.books)
            print(f'Статус книги "{book.title}" с ID {book_id} обновлен на "{new_status}".')
        else:
            print(f'Книга с ID {book_id} не найдена.')
