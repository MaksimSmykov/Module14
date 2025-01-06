import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    ); 
    ''')
    connection.commit()

def get_all_products():
    return cursor.execute('SELECT * FROM Products')

# initiate_db()
# for i in range(4):
#     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                    (f'Продукт {i + 1}', f'Описание {i + 1}', f'{(i + 1) * 100}'))
# connection.commit()