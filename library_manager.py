import json
import os


class Book:
    def __init__(self, id, title, author, years, status='в наличии'):
        self.id = id
        self.title = title
        self.author = author
        self.years = years
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'years': self.years,
            'status': self.status,
        }


class Library:
    def __init__(self, filename='library.json'):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """Загружает книги из файла."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                try:
                    books_data = json.load(file)
                    self.books = [Book(**book) for book in books_data]
                except json.JSONDecodeError:
                    print("Ошибка чтения файла. Проверьте формат JSON.")
                    self.books = []  # Установить пустой список, если произошла ошибка

    def save_books(self):
        """Сохраняет книги в файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        """Добавляет новую книгу в библиотеку."""
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f'Книга "{title}" добавлена с ID {book_id}.')

    def remove_book(self, book_id):
        """Удаляет книгу по ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f'Книга с ID {book_id} удалена.')
                return
        print(f'Книга с ID {book_id} не найдена.')

    def search_books(self, query):
        """Ищет книги по title, author или year."""
        results = [book for book in self.books if
                   query in book.title or query in book.author or query in str(book.year)]
        if results:
            for book in results:
                print(
                    f'ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}')
        else:
            print('Книги не найдены.')

    def display_books(self):
        """Отображает все книги в библиотеке."""
        if not self.books:
            print('Библиотека пуста.')
            return
        for book in self.books:
            print(
                f'ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}')

    def update_status(self, book_id, new_status):
        """Изменяет статус книги по ID."""
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_books()
                    print(f'Статус книги с ID {book_id} изменён на "{new_status}".')
                else:
                    print('Некорректный статус. Доступные статусы: "в наличии", "выдана".')
                return
        print(f'Книга с ID {book_id} не найдена.')


def main():
    """Основная функция для взаимодействия с пользователем."""
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)
        elif choice == '3':
            query = input("Введите запрос для поиска (title, author или year): ")
            library.search_books(query)
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.update_status(book_id, new_status)
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")


if __name__ == '__main__':
    main()

