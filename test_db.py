import unittest
import sqlite3
import os
from db_operations import get_books_by_author

class TestDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Используем временный файл для тестовой БД
        cls.db_name = "test_library.db"
        cls.conn = sqlite3.connect(cls.db_name)
        cls.cursor = cls.conn.cursor()
        
        # Создаём таблицы и вставляем данные
        cls.cursor.execute("CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name TEXT)")
        cls.cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER, price REAL)")
        
        # Очищаем на случай, если файл остался от прошлых запусков
        cls.cursor.execute("DELETE FROM books")
        cls.cursor.execute("DELETE FROM authors")
        
        cls.cursor.execute("INSERT INTO authors (id, name) VALUES (1, 'Тестовый Автор')")
        cls.cursor.execute("INSERT INTO books (id, title, author_id, price) VALUES (1, 'Тестовая Книга', 1, 100.0)")
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        # Закрываем соединение и удаляем временный файл БД
        cls.conn.close()
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)

    def test_insert_data(self):
        """Тест: проверка, что данные вставились."""
        self.cursor.execute("SELECT COUNT(*) FROM books")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_join_query(self):
        """Тест: проверка JOIN-запроса."""
        query = '''
            SELECT books.title, authors.name 
            FROM books JOIN authors ON books.author_id = authors.id
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        self.assertEqual(result, ('Тестовая Книга', 'Тестовый Автор'))

    def test_parameterized_query(self):
        """Тест: проверка параметризованного поиска (защита от инъекций)."""
        # Передаем имя файла тестовой БД, чтобы функция подключилась к ней
        result = get_books_by_author("' OR '1'='1", db_name=self.db_name)
        self.assertEqual(len(result), 0) # Инъекция не сработает, вернется пустой список

if __name__ == '__main__':
    unittest.main()