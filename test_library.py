import unittest
import json
import os
from io import StringIO
from unittest.mock import patch
from library_manager import Book, Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл для тестирования
        self.test_file = 'test_library.json'
        self.library = Library(file_path=self.test_file)

    def tearDown(self):
        # Удаляем временный файл после тестов
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        self.library.add_book("1984", "George Orwell", 1949)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "1984")

    def test_remove_book(self):
        self.library.add_book("1984", "George Orwell", 1949)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        self.library.add_book("1984", "George Orwell", 1949)
        results = self.library.search_books('title', '1984')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

    def test_display_books(self):
        self.library.add_book("1984", "George Orwell", 1949)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.library.display_books()
            self.assertIn("1984", fake_out.getvalue())

    def test_update_status(self):
        self.library.add_book("1984", "George Orwell", 1949)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")


if __name__ == '__main__':
    unittest.main()
