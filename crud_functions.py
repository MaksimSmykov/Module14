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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    ); 
    ''')
    connection.commit()

def add_user(username, email, age):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, 1000))
    connection.commit()

def is_included(user_name):
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (user_name,))
    if check_user.fetchone() is not None:
        connection.commit()
        return True
    connection.commit()
    return False

def get_all_products():
    connection.commit()
    return cursor.execute('SELECT * FROM Products')

# initiate_db()
# for i in range(4):
#     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                    (f'Продукт {i + 1}', f'Описание {i + 1}', f'{(i + 1) * 100}'))
# connection.commit()
