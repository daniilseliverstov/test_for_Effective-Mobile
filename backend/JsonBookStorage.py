import json
from typing import List
from backend.Book import Book
from backend.Library import IBookStorage


class JsonBookStorage(IBookStorage):
    def __init__(self, file_path: str = "library.json") -> None:
        self.file_path = file_path

    def load_books(self) -> List[Book]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Файл повреждён.")
            return []

    def save_books(self, books: List[Book]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)