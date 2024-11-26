import unittest
from .classes.book_manager import BookManager


class Test(unittest.TestCase):
    def setUp(self):
        self.book_manager = BookManager("src/books.json")

    # тесты на успешное добавление книги
    def test_add_book(self):
        self.assertEqual(self.book_manager.add_book("Название", "Автор", 1900)["status_code"], 200)

    # тесты на добавление книги с недостающими данными
    def test_add_book_invalid_data(self):
        self.assertEqual(self.book_manager.add_book("", "Автор", 1900)["status_code"], 500)
        self.assertEqual(self.book_manager.add_book("Название", "", 1900)["status_code"], 500)
        self.assertEqual(self.book_manager.add_book("Название", "Автор", -100)["status_code"], 500)
        self.assertEqual(self.book_manager.add_book("", "", -100)["status_code"], 500)

    # тесты на успешный поиск книг
    def test_find_books(self):
        self.book_manager.add_book("Название", "Автор", 1900)
        results1 = self.book_manager.search_book_by_title("Название")
        results2 = self.book_manager.search_book_by_author("Автор")
        results3 = self.book_manager.search_book_by_year(1900)
        self.assertEqual(results1["status_code"], 200)
        self.assertEqual(results2["status_code"], 200)
        self.assertEqual(results3["status_code"], 200)

    # тесты на не успешный поиск книг
    def test_find_books_no_matches(self):
        results1 = self.book_manager.search_book_by_title("1231441441")
        results2 = self.book_manager.search_book_by_author("fdsbsbbsdb")
        results3 = self.book_manager.search_book_by_year(90)
        self.assertEqual(results1["status_code"], 404)
        self.assertEqual(results2["status_code"], 404)
        self.assertEqual(results3["status_code"], 404)

    def test_list_books(self):
        self.book_manager.add_book("Название", "Автор", 1900)
        result = self.book_manager.read_books()
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
