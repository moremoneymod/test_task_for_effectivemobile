from classes.book_manager import BookManager

book_manager = BookManager("test")
book_manager.read_books()
book_manager.add_book("test1", "test2", 2001, "в наличии")
book_manager.search_book_by_title("test10")
book_manager.change_book_status(1, "тест")