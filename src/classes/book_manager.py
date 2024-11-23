import json
from src.classes.book import Book


class BookManager:
    def __init__(self, file_link: str) -> None:
        """Метод-конструктор класса BookManager. Принимает на вход путь к файлу books.json.
        Ничего не возвращает"""
        self.file_link = file_link

    @staticmethod
    def read_books() -> dict:
        """Метод, отвечающий за чтение книг из books.json.
        Считанные данные записывает в словарь со статус-кодом.
        Если файл пустой или произошла ошибка во время чтения, возвращает словарь только со статус-кодом.
        Ничего не принимает на вход.
        Возвращает словарь с книгами из файла"""
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
        """Метод, отвечающий за создание уникального id для каждой книги.
        Новый id генерируется на основе id последней книги.
        Возвращает id"""
        data = self.read_books()
        if data["status_code"] == 404 or data["status_code"] == 500:
            return 1
        else:
            print(len(data.keys()))
            return len(data.keys())

    @staticmethod
    def _write_books(books: dict) -> dict:
        """Метод, отвечающий за запись словаря книг в books.json.
        В случае ошибки возвращает статус-код, отличный от 200.
        Принимает на вход словарь книг.
        Возвращает словарь со статус-кодом"""
        try:
            with open("./books.json", 'w', encoding="utf-8") as f:
                f.write(json.dumps(books, ensure_ascii=False))
            return {"status_code": 200}
        except Exception as e:
            return {"status_code": 500}

    def add_book(self, title: str, author: str, year: int, status: str) -> dict:
        """Метод для добавления книги. Отвечает за создание экземпляра класса Book и запись объекта books.json.
        Сама функция никаких действий не выполняет, является просто связующим звеном между другими функциями.
        Принимает на вход данные для создания объекта. Возвращает словарь со статус-кодом"""
        new_book = self._create_book(title, author, year, status)
        try_add = self._add_book_to_json(new_book)
        print(try_add)
        return try_add

    def _create_book(self, title: str, author: str, year: int, status: str) -> Book:
        """Метод для создания экземпляра класса Book, принимает на вход данные для создания объекта,
        возвращает экземпляр класса для дальнейших действий с ним"""
        new_book_id = self._create_book_id()
        new_book = Book(new_book_id, title, author, year, status)
        return new_book

    def _add_book_to_json(self, book: Book) -> dict:
        """Метод, отвечающий за запись книги в books.json.
        Сначала считывает все книги из файла в словарь, используя метод для чтения.
        Затем формирует словарь из объекта Book и добавляет этот словарь к словарю со всеми книгами.
        В случае, если файл пустой, создает словарь, содержащий только одну книгу.
        Затем, используя метод для записи в books.json, записывает новый словарь в файл.
        Возвращает словарь со статус-кодом"""
        books = self.read_books()
        if books["status_code"] == 404:
            books = {
                book.book_id: {"title": book.title, "author": book.author, "year": book.year, "status": book.status}}
        else:
            books[book.book_id] = {"title": book.title, "author": book.author, "year": book.year, "status": book.status}
        try_write = self._write_books(books)
        return try_write

    def _search_book(self, search_filter: str, search_filter_data: str | int) -> dict:
        """Общая метод поиска по фильтру: принимает название ключа словаря и значение для поиска.
        Возвращает словарь со статус-кодом 200 и найденной книгой, если книга не найдена - только со статус-кодом 404,
        в случае ошибки чтения файла books.json - словарь со статус-кодом 500"""
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
        """Метод для поиска книги по заголовку, использует метод общего поиска по фильтру.
        Возвращает словарь, полученный от общего метода поиска"""
        search_data = self._search_book("title", title)
        print(search_data)
        return search_data

    def search_book_by_author(self, author: str) -> dict:
        """Метод для поиска книги по автору, использует метод общего поиска по фильтру.
        Возвращает словарь, полученный от общего метода поиска"""
        search_data = self._search_book("author", author)
        print(search_data)
        return search_data

    def search_book_by_year(self, year: int) -> dict:
        """Метод для поиска книги по году, использует метод общего поиска по фильтру.
        Возвращает словарь, полученный от общего метода поиска"""
        search_data = self._search_book("year", year)
        print(search_data)
        return search_data

    def _search_book_by_id(self, book_id) -> dict:
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
        """Метод для удаления книги из books.json. Принимает на вход id книги.
        Возвращает словарь со статус-кодом операции удаления"""
        books = self.read_books()
        if books["status_code"] != 200:
            return {"status_code": books["status_code"]}
        if str(book_id) in books:
            del books[str(book_id)]
            try_write = self._write_books(books)
            return try_write
        else:
            return {"status_code": 404}

    def change_book_status(self, book_id: int, new_status: str):
        pass
