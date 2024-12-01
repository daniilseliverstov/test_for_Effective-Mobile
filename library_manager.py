import json
import uuid


class Book:
    def __init__(self, title, author, year, status='в наличии'):
        self.id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        book = Book(data["title"], data["author"], data["year"], data["status"])
        book.id = data["id"]
        return book


class Library:
    def __init__(self, file_path: str = "library.json"):
        self.file_path = file_path
        self.books = self._load_books()

    def _load_books(self) -> list[Book]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Файл повреждён.")
            return []

    def _save_books(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: str):
        book = Book(title, author, year)
        self.books.append(book)
        self._save_books()
        print(f'Книга "{title}" добавлена с ID {book.id}.')

    def remove_book(self, book_id: str):
        book = next((b for b in self.books if b.id == book_id), None)
        if book:
            self.books.remove(book)
            self._save_books()
            print(f'Книга "{book.title}" c ID {book_id} удалена')
        else:
            print(f'Книга с ID {book_id} не найдена.')

    def search_books(self, field: str, value: str):
        if field == "year":
            value = str(value)
        results = [book for book in self.books if str(getattr(book, field, '')).lower() == value.lower()]
        if results:
            for book in results:
                print(book.to_dict())
        else:
            print('Ничего не найдено.')
        return results

    def display_books(self):
        if self.books:
            for book in self.books:
                print(book.to_dict())
        else:
            print(f'Библиотека пуста')

    def update_status(self, book_id: str, new_status: str):
        book = next((b for b in self.books if b.id == book_id), None)
        if book:
            book.status = new_status
            self._save_books()
            print(f'Статус книги "{book.title}" с ID {book_id} обновлен на "{new_status}".')
        else:
            print(f'Книга с ID {book_id} не найдена.')


def main():
    """Основная функция для взаимодействия с пользователем."""
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = input("Введите ID книги: ")
            library.remove_book(book_id)
        elif choice == "3":
            field = input("Введите поле для поиска (title, author, year): ")
            value = input("Введите значение для поиска: ")
            library.search_books(field, value)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = input("Введите ID книги: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, new_status)
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()

