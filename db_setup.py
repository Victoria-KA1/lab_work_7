import sqlite3

def create_database(db_name="library.db"):
    """Создаёт БД, таблицы, индексы и вставляет данные."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            price REAL,
            FOREIGN KEY (author_id) REFERENCES authors (id)
        )
    ''')

    # Задание 2: Вставка данных
    cursor.execute("DELETE FROM books") # очистка для повторного запуска
    cursor.execute("DELETE FROM authors")
    
    cursor.execute("INSERT INTO authors (name) VALUES ('Лев Толстой')")
    cursor.execute("INSERT INTO authors (name) VALUES ('Фёдор Достоевский')")
    cursor.execute("INSERT INTO authors (name) VALUES ('Антон Чехов')")
    
    cursor.execute("INSERT INTO books (title, author_id, price) VALUES ('Война и мир', 1, 1500.0)")
    cursor.execute("INSERT INTO books (title, author_id, price) VALUES ('Анна Каренина', 1, 1200.0)")
    cursor.execute("INSERT INTO books (title, author_id, price) VALUES ('Преступление и наказание', 2, 900.0)")
    cursor.execute("INSERT INTO books (title, author_id, price) VALUES ('Идиот', 2, 1000.0)")
    cursor.execute("INSERT INTO books (title, author_id, price) VALUES ('Вишнёвый сад', 3, 500.0)")

    # Задание 4: Индексация и поиск
    # Создаём индекс по полю author_id, чтобы JOIN и поиск работали быстрее
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id)")
    
    conn.commit()

    # Задание 8: Выполнить JOIN (вывод всех книг с именами авторов)
    print("--- Задание 8: Результат JOIN (Книги и Авторы) ---")
    cursor.execute('''
        SELECT books.title, authors.name, books.price
        FROM books
        JOIN authors ON books.author_id = authors.id
    ''')
    
    for row in cursor.fetchall():
        print(f"Книга: {row[0]} | Автор: {row[1]} | Цена: {row[2]}")

    conn.close()
    print("\nБаза данных успешно создана и заполнена!")

if __name__ == "__main__":
    create_database()