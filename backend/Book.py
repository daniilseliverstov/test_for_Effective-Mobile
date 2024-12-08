import uuid
from typing import Dict


class Book:
    def __init__(self, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        """Инициализирует объект книги.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
            status (str): Статус книги (по умолчанию 'в наличии').
        """
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, str]:
        """Преобразует объект книги в словарь.

        Returns:
            Dict[str, str]: Словарь с данными книги.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, str]) -> "Book":
        """Создает объект книги из словаря.

        Args:
            data (Dict[str, str]): Словарь с данными книги.

        Returns:
            Book: Объект книги.
        """
        book = Book(data["title"], data["author"], data["year"], data["status"])
        book.id = data["id"]
        return book

