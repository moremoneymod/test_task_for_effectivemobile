import json
from src.classes.book import Book


class BookManager:
    """Класс, отвечающий за менеджер для работы с книгами
    Содержит методы для чтения книг из файла, запись книг в файл, поиск по разным фильтрам и тд"""

    def __init__(self, file_link: str) -> None:
        """
        Метод-конструктор класса

        :param file_link: путь к файлу books.json
        """
        self.file_link = file_link

    @staticmethod
    def read_books() -> dict:
        """
        Метод, отвечающий за считывание всех книг из файла
        Если файл пустой - возвращает словарь со статус-кодом 404
        Если возникли проблемы при чтении файлы - возвращает словарь со статус-кодом 500
        В случае успешного чтения и наличия книг - возвращает словарь со статус-кодом 200

        :return: словарь со всеми книгами и статус-кодом
        """
        with open("./books.json", encoding="utf-8") as f:
            try:
                data = {"status_code": 200}
                data.update(json.load(f))
            except json.decoder.JSONDecodeError:
                data = {"status_code": 404}
            except Exception as e:
                data = {"status_code": 500}
        print(data)
        return data

    def _create_book_id(self) -> int:
        """
        Метод для создания уникального идентификатора
        Идентификатор создается на основе количества книг в файле books.json

        :return: созданный уникальный идентификатор
        """
        data = self.read_books()
        if data["status_code"] == 404 or data["status_code"] == 500:
            return 1
        else:
            print(len(data.keys()))
            return len(data.keys())

    @staticmethod
    def _write_books(books: dict) -> dict:
        """
        Метод, отвечающий за запись всех книг в файл books.json
        Получает на вход словарь и, преобразовав его в json, записывает в файл
        Если возникли проблемы при записи в файл - возвращает словарь со статус-кодом 500
        В случае успешной записи - возвращает словарь со статус-кодом 200

        :param books: словарь с книгами
        :return: словарь со статус-кодом операции
        """
        try:
            with open("./books.json", 'w', encoding="utf-8") as f:
                f.write(json.dumps(books, ensure_ascii=False))
            return {"status_code": 200}
        except Exception as e:
            return {"status_code": 500}

    def add_book(self, title: str, author: str, year: int, status: str) -> dict:
        """
        Метод, отвечающий за добавление новой книги
        Является промежуточным звеном между двумя другими методами: методом для создания новой книги и
        методом записи книги в файл books.json

        :param title: название книги
        :param author: автор книги
        :param year: год издания книги
        :param status: статус книги
        :return: словарь со статус-кодом операции
        """
        new_book = self._create_book(title, author, year, status)
        try_add = self._add_book_to_json(new_book)
        print(try_add)
        return try_add

    def _create_book(self, title: str, author: str, year: int, status: str) -> Book:
        """
        Метод для создания новой книги - объекта класса Book.
        Получает уникальный идентификатор через метод для генерации и, используя переданные параметры,
        создает экземпляр класса

        :param title: название книги
        :param author: автор книги
        :param year: год издания книги
        :param status: статус книги
        :return: словарь с новой книгой и статус-кодом операции
        """
        new_book_id = self._create_book_id()
        new_book = Book(new_book_id, title, author, year, status)
        return new_book

    def _add_book_to_json(self, book: Book) -> dict:
        """
        Метод, отвечающий за запись книги в файл books.json. Считывает все книги из файла в словарь,
        затем добавляет к ним новую книгу и записывает новый словарь в файл. Если файл пустой,
        создается пустой словарь и в него записывается новая книга. Затем точно так же словарь записывается в файл

        :param book: объекта класса Book, представляющий собой книгу для записи
        :return: словарь со статус-кодом операции
        """
        books = self.read_books()
        if books["status_code"] == 404:
            books = {
                book.book_id: {"title": book.title, "author": book.author, "year": book.year, "status": book.status}}
        else:
            books[book.book_id] = {"title": book.title, "author": book.author, "year": book.year, "status": book.status}
        try_write = self._write_books(books)
        return try_write

    def _search_book(self, search_filter: str, search_filter_data: str | int) -> dict:
        """
        Метод для поиска книги по переданному фильтру.
        Является общим методом поиска, который используют остальные методы поиска.
        Считывает все книги из файла, затем через цикл ищет нужную книгу по переданным фильтру и значению фильтра
        Если книга не найдена - возвращает словарь со статус-кодом 404
        Если возникли проблемы при чтении файла - возвращает словарь со статус-кодом 500

        :param search_filter: название фильтра для поиска книги
        :param search_filter_data: значение фильтра
        :return: словарь с найденной книгой и статус-кодом операции
        """
        books = self.read_books()
        if books["status_code"] == 500:
            return books
        book_data = {"status_code": 404}
        for data_tuple in list(books.items())[1:]:
            if data_tuple[1][f"{search_filter}"] == search_filter_data:
                book_data.update({data_tuple[0]: data_tuple[1]})
                book_data["status_code"] = 200
                break

        print(book_data)
        return book_data

    def search_book_by_title(self, title: str) -> dict:
        """
        Метод для поиска книги по заголовку.
        Использует общий метод поиска по фильтру
        В случае успешного поиска - возвращает словарь с найденной книгой и статус-кодом 200
        Если книга не найдена - возвращает словарь со статус-кодом 404
        Если возникли проблемы с чтением файла - возвращает словарь со статус-кодом 500

        :param title: заголовок книги
        :return: словарь с найденной книгой и статус-кодом
        """
        search_data = self._search_book("title", title)
        print(search_data)
        return search_data

    def search_book_by_author(self, author: str) -> dict:
        """
        Метод для поиска книги по автору.
        Использует общий метод поиска по фильтру
        В случае успешного поиска - возвращает словарь с найденной книгой и статус-кодом 200
        Если книга не найдена - возвращает словарь со статус-кодом 404
        Если возникли проблемы с чтением файла - возвращает словарь со статус-кодом 500

        :param author: автор книги
        :return: словарь с найденной книгой и статус-кодом
        """
        search_data = self._search_book("author", author)
        print(search_data)
        return search_data

    def search_book_by_year(self, year: int) -> dict:
        """
        Метод для поиска книги по году издания.
        Использует общий метод поиска по фильтру
        В случае успешного поиска - возвращает словарь с найденной книгой и статус-кодом 200
        Если книга не найдена - возвращает словарь со статус-кодом 404
        Если возникли проблемы с чтением файла - возвращает словарь со статус-кодом 500

        :param year: год издания книги
        :return: словарь с найденной книгой и статус-кодом
        """
        search_data = self._search_book("year", year)
        print(search_data)
        return search_data

    def _search_book_by_id(self, book_id) -> dict:
        """
        Метод для поиска книги по уникальному идентификатору.
        Считывает все книги при помощи метода для чтения книг из файла и затем ищет книгу по переданному идентификатору
        В случае успешного поиска - возвращает словарь с найденной книгой и статус-кодом 200
        Если книга не найдена - возвращает словарь со статус-кодом 404
        Если возникли проблемы с чтением файла - возвращает словарь со статус-кодом 500

        :param book_id: уникальный идентификатор книги
        :return: словарь с найденной книгой и статус-кодом
        """
        books = self.read_books()
        book_data = {"status_code": 404}
        if books["status_code"] == 200:
            if str(book_id) in books:
                book_data.update(books[str(book_id)])
                book_data["status_code"] = 200
        else:
            book_data["status_code"] = 500
        return book_data

    def delete_book(self, book_id: int) -> dict:
        """
        Метод для удаления книги по переданному уникальному идентификатору.
        Считывает все книги из файла в словарь, используя метод для чтения книг,
        удаляет книгу из словаря и затем записывает словарь в файл, используя метод для записи всех книг
        Если книга успешно удалена - возвращает словарь со статус-кодом 200
        Если книга не найдена - возвращает словарь со статус-кодом 404
        Если возникли проблемы при чтении или записи в файл - возвращает словарь со статус-кодом 500

        :param book_id: уникальный идентификатор книги
        :return: словарь со статус-кодом операции
        """
        books = self.read_books()
        if books["status_code"] != 200:
            return {"status_code": books["status_code"]}
        if str(book_id) in books:
            del books[str(book_id)]
            try_write = self._write_books(books)
            return try_write
        else:
            return {"status_code": 404}

    def _update_book(self, book_id: int, new_book: dict) -> dict:
        """
        Метод для обновления книги в файле books.json. Принимает на вход идентификатор и обновленную книгу.
        Считывает все книги из файла в словарь, используя метод для чтения, затем обновляет словарь
        и записывает его в файл, используя метод для записи

        :param book_id: уникальный идентификатор книги для обновления
        :param new_book: словарь, представляющий собой книгу с обновленными данными
        :return: возвращает словарь со статус-кодом операции
        """
        books = self.read_books()
        try_update = {"status_code": 200}
        if books["status_code"] != 200:
            try_update["status_code"] = books["status_code"]
        else:
            books[str(book_id)] = new_book
            try_write = self._write_books(books)
            if try_write != 200:
                try_update["status_code"] = try_write["status_code"]

        return try_update

    def change_book_status(self, book_id: int, new_status: str) -> dict:
        book = self._search_book_by_id(book_id)
        change_try = {"status_code": 200}
        if book["status_code"] != 200:
            change_try["status_code"] = book["status_code"]
        else:
            book["status"] = new_status
            change_try = self._update_book(book_id, book)
        return change_try
