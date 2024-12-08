from backend.Library import Library
from backend.JsonBookStorage import JsonBookStorage


def main() -> None:
    """Основная функция для взаимодействия с пользователем."""
    storage = JsonBookStorage()
    library = Library(storage)
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
