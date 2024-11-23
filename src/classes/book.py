class Book:
    """Класс, отвечающий за представление книги"""
    book_id: int
    title: str
    author: str
    year: int
    status: str

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str) -> None:
        """Метод-конструктор, принимает на вход данные книги"""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status
