import sqlite3

def get_books_by_author(author_name, db_name="library.db"):
    """Задание 6: Использование параметров запроса."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # ВАЖНО: используем ? вместо f-строк для безопасности
    query = '''
        SELECT books.title, books.price
        FROM books
        JOIN authors ON books.author_id = authors.id
        WHERE authors.name = ?
    '''
    
    cursor.execute(query, (author_name,))
    results = cursor.fetchall()
    
    conn.close()
    return results

if __name__ == "__main__":
    print("--- Задание 6: Поиск книг по автору с параметром ---")
    
    # Поиск книг Льва Толстого
    author = "Лев Толстой"
    books = get_books_by_author(author)
    
    print(f"Книги автора {author}:")
    for book in books:
        print(f"  - {book[0]} ({book[1]} руб.)")