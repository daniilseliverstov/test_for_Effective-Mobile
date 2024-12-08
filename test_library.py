import unittest
import json
import os
from io import StringIO
from unittest.mock import patch
from backend.Book import Book
from backend.Library import Library
from backend.JsonBookStorage import JsonBookStorage


class TestLibrary(unittest.TestCase):
    def setUp(self) -> None:
        """Создает временный файл для тестирования и инициализирует библиотеку."""
        self.test_file: str = 'test_library.json'
        self.storage = JsonBookStorage(file_path=self.test_file)  # Создаем экземпляр JsonBookStorage
        self.library: Library = Library(storage=self.storage)  # Передаем хранилище в библиотеку

    def tearDown(self) -> None:
        """Удаляет временный файл после завершения тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self) -> None:
        """Тестирует добавление книги в библиотеку."""
        self.library.add_book("1984", "George Orwell", 1949)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "1984")

    def test_remove_book(self) -> None:
        """Тестирует удаление книги из библиотеки."""
        self.library.add_book("1984", "George Orwell", 1949)
        book_id: str = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self) -> None:
        """Тестирует попытку удаления несуществующей книги."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library.remove_book("nonexistent_id")
            self.assertIn("не найдена", fake_out.getvalue())

    def test_search_books(self) -> None:
        """Тестирует поиск книги по заголовку."""
        self.library.add_book("1984", "George Orwell", 1949)
        results: list = self.library.search_books('title', '1984')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

    def test_search_nonexistent_book(self) -> None:
        """Тестирует поиск по несуществующему заголовку."""
        results: list = self.library.search_books('title', 'nonexistent_title')
        self.assertEqual(len(results), 0)

    def test_display_books(self) -> None:
        """Тестирует отображение всех книг в библиотеке."""
        self.library.add_book("1984", "George Orwell", 1949)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library.display_books()
            self.assertIn("1984", fake_out.getvalue())

    def test_update_status(self) -> None:
        """Тестирует обновление статуса книги."""
        self.library.add_book("1984", "George Orwell", 1949)
        book_id: str = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_update_status_of_nonexistent_book(self) -> None:
        """Тестирует попытку обновления статуса несуществующей книги."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library.update_status("nonexistent_id", "выдана")
            self.assertIn("не найдена", fake_out.getvalue())

    def test_load_books_from_file(self) -> None:
        """Тестирует загрузку книг из файла."""
        self.library.add_book("1984", "George Orwell", 1949)
        self.library = Library(storage=self.storage)  # Перезагружаем библиотеку с тем же хранилищем
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "1984")


if __name__ == '__main__':
    unittest.main()
