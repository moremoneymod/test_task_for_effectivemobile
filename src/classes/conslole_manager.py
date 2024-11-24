import datetime

from src.classes.book_manager import BookManager


class ConsoleManager:
    """
    Класс для работы с консолью
    """

    def __init__(self, file_link) -> None:
        self.book_manager = BookManager(file_link)

    def main_menu(self) -> None:
        actions = {1: "Отобразить все книги", 2: "Добавить новую книгу", 3: "Поиск книги", 4: "Изменить статус книги",
                   5: "Удалить книгу"}
        print("---" * 10)
        print("Добро пожаловать в библиотеку книг!\n")
        print(f"Выберите действие: ")
        for action_number, action in actions.items():
            print(f"\t{action_number}. {action}")
        print("---" * 10)
        action_id = int(input("\nНомер действия: "))
        if action_id > 5 or action_id < 1:
            print("\nОшибка!\nТакого действия нет\n")
            self.main_menu()
        match action_id:
            case 1:
                self._show_all_books()
            case 2:
                self._add_book()
            case 3:
                self._search_book()
            case 4:
                self._change_book_status()
            case 5:
                self._delete_book()

    def _show_all_books(self) -> None:
        books = self.book_manager._create_book_str_view()
        print()
        if books["status_code"] == 404:
            print("Ошибка:\nВ библиотеке пока нет книг")
        elif books["status_code"] == 500:
            print("Ошибка:\nВозникли проблемы при чтении файла")
        else:
            print("Книги, принадлежащие библиотеке:")
            print("---" * 10)
            for book in list(books.values())[1:]:
                print(book + "\n")

        self.main_menu()

    def _delete_book(self) -> None:
        print("\nУдаление книги")
        book_id = input("\nВведите идентификатор книги: ")
        if not self._is_valid_book_id(book_id=book_id):
            print("Введен некорректный идентификатор книги")
            while not self._is_valid_book_id(book_id=book_id):
                book_id = input("\nВведите идентификатор книги: ")
                if not self._is_valid_book_id(book_id=book_id):
                    print("Введен некорректный идентификатор книги")
        book_id = int(book_id)
        check_book = self.book_manager._check_book_exists(book_id)
        print()
        if check_book["status_code"] == 404:
            print("Ошибка:\nТакой книги не существует")
        elif check_book["status_code"] == 500:
            print("Ошибка:\nВозникли проблемы при чтении файла")
        else:
            try_delete = self.book_manager.delete_book(book_id)
            if try_delete["status_code"] != 200:
                print("Ошибка:\nВозникли проблемы при удалении книги")
            else:
                print("Книга успешно удалена")
        self.main_menu()

    def _add_book(self) -> None:
        print("Добавление новой книги в библиотеку")
        title = input("Укажите название книги: ")
        if len(title) == 0:
            print("У книги должно быть название")
            while len(title) == 0:
                title = input("Укажите название книги: ")
                if len(title) == 0:
                    print("У книги должно быть название")

        author = input("Укажите автора книги: ")
        if len(author) == 0:
            print("У книги должен быть автор")
            while len(author) == 0:
                author = input("Укажите автора книги: ")
                if len(author) == 0:
                    print("У книги должен быть автор")

        year = int(input("Укажите год издания книги: "))
        year_now = datetime.datetime.now().year
        if year < 0 or year > year_now:
            print(f"Год издания должен быть в диапазоне от 0 до {year_now}")
            while year < 0 or year > year_now:
                year = int(input("Укажите год издания книги: "))
                if year < 0 or year > year_now:
                    print(f"Год издания должен быть в диапазоне от 0 до {year_now}")

        try_add = self.book_manager.add_book(title, author, year)
        print()
        if try_add["status_code"] != 200:
            print("Ошибка:\nВозникли проблемы с добавлением книги в файл")
        else:
            print("Книга успешно добавлена!")

        self.main_menu()

    def _change_book_status(self):
        print("Изменение статуса книги")
        book_id = input("\nВведите идентификатор книги: ")
        if not self._is_valid_book_id(book_id=book_id):
            print("Введен некорректный идентификатор книги")
            while not self._is_valid_book_id(book_id=book_id):
                book_id = input("\nВведите идентификатор книги: ")
                if not self._is_valid_book_id(book_id=book_id):
                    print("Введен некорректный идентификатор книги")
        book_id = int(book_id)
        check_book = self.book_manager._check_book_exists(book_id)
        if check_book["status_code"] == 404:
            print("Ошибка:\nКниги с таким идентификатором не существует")
        elif check_book["status_code"] == 500:
            print("Ошибка:\nВозникли проблемы при чтении файла")
        else:
            new_statuses = ["в наличии", "выдана"]
            print("\nВыберите новый статус книги:\n\t1 - в наличии\n\t2 - выдана")
            new_status_id = input("\nНовый статус: ")
            print(new_status_id)
            if not self._is_valid_operation_id(operation_id=new_status_id, operations_cnt=2):
                print("\nНет такого статуса")
                while not self._is_valid_operation_id(operation_id=new_status_id, operations_cnt=2):
                    new_status_id = input("Новый статус: ")
                    if not self._is_valid_operation_id(operation_id=new_status_id, operations_cnt=2):
                        print("\nНет такого статуса")
            new_status_id = int(new_status_id)

            try_change = self.book_manager.change_book_status(book_id=book_id,
                                                              new_status=new_statuses[new_status_id - 1])
            if try_change["status_code"] != 200:
                print("\nОшибка:\nВозникли проблемы с изменением статуса книги")
            else:
                print("\nСтатус книги успешно изменен")
        self.main_menu()

    @staticmethod
    def _is_valid_book_id(book_id: str) -> bool:
        try:
            int(book_id)
            if int(book_id) >= 1:
                return True
            else:
                return False
        except ValueError:
            return False

    def _search_book(self) -> None:
        print("\nПоиск книги")
        print("Выберите тип поиска:\n\t1 - по названию\n\t2 - по автору\n\t3 - по году издания")
        search_type = input("Выберите тип поиска: ")
        if not self._is_valid_operation_id(operation_id=search_type, operations_cnt=3):
            print("Нет такого типа поиска")
            while not self._is_valid_operation_id(operation_id=search_type, operations_cnt=3):
                search_type = input("Выберите тип поиска: ")
                if not self._is_valid_operation_id(operation_id=search_type, operations_cnt=3):
                    print("Нет такого типа поиска")
        search_type = int(search_type)

        if search_type == 1:
            title = input("Введите заголовок книги: ")
            if len(title) == 0:
                print("У книги должно быть название")
                while len(title) == 0:
                    title = input("Укажите название книги: ")
                    if len(title) == 0:
                        print("У книги должно быть название")
            try_search = self.book_manager.search_book_by_title(title=title)
            if try_search["status_code"] == 404:
                print("Ошибка:\nКнига с таким заголовком не найдена")
            elif try_search["status_code"] == 500:
                print("Ошибка:\nВозникли проблемы при чтении файла")
            else:
                print("!!!", try_search)
        self.main_menu()

    @staticmethod
    def _is_valid_operation_id(operation_id: str, operations_cnt: int) -> bool:
        try:
            int(operation_id)
            if int(operation_id) in [i for i in range(1, operations_cnt + 1)]:
                return True
            else:
                return False
        except ValueError:
            return False
