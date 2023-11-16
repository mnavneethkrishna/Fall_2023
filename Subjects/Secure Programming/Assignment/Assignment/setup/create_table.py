import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        print(f'Successful connection to the database: {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PHONEBOOK (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                PhoneNumber TEXT UNIQUE NOT NULL
            );
        ''')
        print('Table created successfully')
    except Error as e:
        print(e)

def main():
    connection = create_connection()
    if connection is not None:
        create_table(connection)
        connection.close()
    else:
        print('Unable to create connection.')

if __name__ == '__main__':
    main()