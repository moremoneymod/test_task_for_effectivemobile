import datetime
import sys

from .book_manager import BookManager


class ConsoleManager:
    """
    Класс для работы с консолью.
    Реализует вывод консольного интерфейса для пользователя
    """

    def __init__(self, file_link) -> None:
        """
        Метод-конструктор для класса ConsoleManager.
        Создает экземпляр класса BookManager для работы с файлом книг
        :param file_link: путь к файлу
        """
        self.book_manager = BookManager(file_link)

    def main_menu(self) -> None:
        """
        Метод главного меню менеджера консоли.
        Главное меню представляет собой приветствие и список доступных действий.
        Метод содержит проверку на валидный идентификатор операции.
        Ничего не возвращает
        """
        actions = {1: "Отобразить все книги", 2: "Добавить новую книгу", 3: "Поиск книги", 4: "Изменить статус книги",
                   5: "Удалить книгу", 6: "Выйти из программы"}
        print("---" * 10)
        print("Добро пожаловать в библиотеку книг!\n")
        print(f"Выберите действие: ")
        for action_number, action in actions.items():
            print(f"\t{action_number}. {action}")
        print("---" * 10)
        action_id = input("\nНомер действия: ")
        if not self._is_valid_operation_id(operation_id=action_id, operations_cnt=6):
            print("\nОшибка!\nТакого действия нет\n")
            self.main_menu()
        else:
            action_id = int(action_id)
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
            case 6:
                sys.exit()

    def _show_all_books(self) -> None:
        """
        Метод, отвечающий за вывод всех книг в консоль.
        Использует метод класса BookManager для получения всех книг из файла.
        Ничего не возвращает
        """
        books = self.book_manager.read_books()
        books = self.book_manager.create_books_str_view(books)
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
        """
        Метод, отвечающий за удаление книги.
        Реализованы проверки на корректность идентификатора книги.
        Использует метод класса BookManager для удаления книги из файла.
        Ничего не возвращает
        """
        print("\nУдаление книги. Для отмены введите 0")
        book_id = input("\nВведите идентификатор книги: ")
        if not self._is_valid_book_id(book_id=book_id):
            print("Введен некорректный идентификатор книги")
            while not self._is_valid_book_id(book_id=book_id):
                book_id = input("\nВведите идентификатор книги: ")
                if not self._is_valid_book_id(book_id=book_id):
                    print("Введен некорректный идентификатор книги")
        book_id = int(book_id)
        if book_id == 0:
            self.main_menu()
        check_book = self.book_manager.check_book_exists(book_id)
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
        """
        Метод, отвечающий за добавление новой книги.
        В методе присутствуют проверки на валидность введенных данных о книге.
        Использует метод класса BookManager.
        Ничего не возвращает
        """
        print("Добавление новой книги в библиотеку. Введите 0 для отмены")
        title = input("Укажите название книги: ")
        if len(title) == 0:
            print("У книги должно быть название")
            while len(title) == 0:
                title = input("Укажите название книги: ")
                if len(title) == 0:
                    print("У книги должно быть название")
        elif title == '0':
            self.main_menu()

        author = input("Укажите автора книги: ")
        if len(author) == 0:
            print("У книги должен быть автор")
            while len(author) == 0:
                author = input("Укажите автора книги: ")
                if len(author) == 0:
                    print("У книги должен быть автор")
        elif author == '0':
            self.main_menu()

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

    def _change_book_status(self) -> None:
        """
        Метод, отвечающий за изменение статуса книги.
        В методе реализованы проверки валидность введенных данных.
        Метод реализует выбор нового статуса путем выбора одного из двух предложенных пользователю статусов.
        Использует методы класса BookManager.
        Ничего не возвращает
        """
        print("Изменение статуса книги. Введите 0 для отмены операции")
        book_id = input("\nВведите идентификатор книги: ")
        if not self._is_valid_book_id(book_id=book_id):
            print("Введен некорректный идентификатор книги")
            while not self._is_valid_book_id(book_id=book_id):
                book_id = input("\nВведите идентификатор книги: ")
                if not self._is_valid_book_id(book_id=book_id):
                    print("Введен некорректный идентификатор книги")
        book_id = int(book_id)
        if book_id == 0:
            self.main_menu()
        check_book = self.book_manager.check_book_exists(book_id)
        if check_book["status_code"] == 404:
            print("Ошибка:\nКниги с таким идентификатором не существует")
        elif check_book["status_code"] == 500:
            print("Ошибка:\nВозникли проблемы при чтении файла")
        else:
            new_statuses = ["в наличии", "выдана"]
            print("\nВыберите новый статус книги:\n\t1 - в наличии\n\t2 - выдана\n\t0 - отмена операции")
            new_status_id = input("\nНовый статус: ")
            print(new_status_id)
            if not self._is_valid_operation_id(operation_id=new_status_id, operations_cnt=2):
                print("\nНет такого статуса")
                while not self._is_valid_operation_id(operation_id=new_status_id, operations_cnt=2):
                    new_status_id = input("Новый статус: ")
                    if not self._is_valid_operation_id(operation_id=new_status_id, operations_cnt=2):
                        print("\nНет такого статуса")
            new_status_id = int(new_status_id)
            if new_status_id == 0:
                self.main_menu()

            try_change = self.book_manager.change_book_status(book_id=book_id,
                                                              new_status=new_statuses[new_status_id - 1])
            if try_change["status_code"] != 200:
                print("\nОшибка:\nВозникли проблемы с изменением статуса книги")
            else:
                print("\nСтатус книги успешно изменен")
        self.main_menu()

    @staticmethod
    def _is_valid_book_id(book_id: str) -> bool:
        """
        Метод для проверки валидности идентификатора книги.
        Если полученный идентификатор не является числом или меньше 0, то функция возвращает ложь,
        в других случаях - истину
        0 - идентификатор книги для отмены операции
        :param book_id: идентификатор книги, который подлежит проверки на валидность
        :return: булевый тип, означающий результат проверки на валидность
        """
        try:
            int(book_id)
            if int(book_id) >= 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def _search_book(self) -> None:
        """
        Метод, отвечающий за поиск книги.
        Предлагает пользователю три поиска на выбор - по названию, по автору и по году издания
        путем предложения выбрать один тип поиска из предложенных.
        Введенный пользователем идентификатор типа поиска проверяется на валидность.
        При успешной проверке используются методы класса BookManager для поиска книги в файле
        и строкового представления книги.
        Ничего не возвращает.
        """
        print("\nПоиск книги. Введите 0 для отмены")
        print("Выберите тип поиска:\n\t1 - по названию\n\t2 - по автору\n\t3 - по году издания")
        search_type = input("Тип поиска: ")
        if not self._is_valid_operation_id(operation_id=search_type, operations_cnt=3):
            print("Нет такого типа поиска")
            while not self._is_valid_operation_id(operation_id=search_type, operations_cnt=3):
                search_type = input("Тип поиска: ")
                if not self._is_valid_operation_id(operation_id=search_type, operations_cnt=3):
                    print("Нет такого типа поиска")
        search_type = int(search_type)
        if search_type == 0:
            self.main_menu()

        if search_type == 1:
            title = input("Введите заголовок книги: ")
            if len(title) == 0:
                print("У книги должно быть название")
                while len(title) == 0:
                    title = input("Укажите название книги: ")
                    if len(title) == 0:
                        print("У книги должно быть название")
            try_search = self.book_manager.search_book_by_title(title=title)
            print()
            print("Результат поиска:")
            print()
            if try_search["status_code"] == 404:
                print("Ошибка:\nКнига с таким заголовком не найдена")
            elif try_search["status_code"] == 500:
                print("Ошибка:\nВозникли проблемы при чтении файла")
            else:
                books = self.book_manager.create_books_str_view(try_search)
                for book in list(books.values())[1:]:
                    print(book + "\n")

        elif search_type == 2:
            author = input("Введите автора книги: ")
            if len(author) == 0:
                print("У книги должен быть автор")
                while len(author) == 0:
                    author = input("Укажите автора книги: ")
                    if len(author) == 0:
                        print("У книги должен быть автор")
            try_search = self.book_manager.search_book_by_author(author=author)
            print()
            print("Результат поиска:")
            print()
            if try_search["status_code"] == 404:
                print("Ошибка:\nКнига с таким автором не найдена")
            elif try_search["status_code"] == 500:
                print("Ошибка:\nВозникли проблемы при чтении файла")
            else:
                books = self.book_manager.create_books_str_view(try_search)
                for book in list(books.values())[1:]:
                    print(book + "\n")

        elif search_type == 3:
            year = input("Введите год издания книги: ")
            if len(year) == 0:
                print("У книги должен быть год издания")
                while len(year) == 0:
                    year = input("Укажите год издания книги: ")
                    if len(year) == 0:
                        print("У книги должен быть год издания")
            year = int(year)
            try_search = self.book_manager.search_book_by_year(year=year)
            print()
            print("Результат поиска:")
            print()
            if try_search["status_code"] == 404:
                print("Ошибка:\nКнига с таким годом издания не найдена")
            elif try_search["status_code"] == 500:
                print("Ошибка:\nВозникли проблемы при чтении файла")
            else:
                books = self.book_manager.create_books_str_view(try_search)
                for book in list(books.values())[1:]:
                    print(book + "\n")

        self.main_menu()

    @staticmethod
    def _is_valid_operation_id(operation_id: str, operations_cnt: int) -> bool:
        """
        Метод для проверки выбранного идентификатора операции. Метод получает на вход идентификатор и проверяет,
        является ли он числом и лежит ли в заданном диапазоне. Диапазон - от 0 до числа операций включительно.
        0 - идентификатор для отмены операции.
        Если проверка успешна, метод возвращает истину, иначе - ложь
        :param operation_id: идентификатор операции, подлежащий проверке
        :param operations_cnt: количество доступных операций
        :return: булевый тип, отражающий результат проверки
        """
        try:
            int(operation_id)
            if int(operation_id) in [i for i in range(0, operations_cnt + 1)]:
                return True
            else:
                return False
        except ValueError:
            return False
