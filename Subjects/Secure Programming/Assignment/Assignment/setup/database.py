import sqlite3
from sqlite3 import Error
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import configparser

config = configparser.ConfigParser()
config.read('db_config.ini')

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(config['phonebookDB']['db_name'])
    except Error as e:
        logger.error(e)
    return conn

def select():
    logger.info("DB: User: xxx Query: SELECT Name, PhoneNumber from PHONEBOOK;")
    sql = ''' SELECT Name, PhoneNumber from PHONEBOOK;'''
    conn = create_connection()
    records = []

    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        output = cur.fetchall()

        for row in output:
            records.append({"name": row[0], "phone": row[1]})

    return records

def insert(username, name, phone):
    logger.info(f"DB: User: {username} Query: INSERT INTO PHONEBOOK(Name,PhoneNumber) VALUES({name},{phone}) ")
    sql = ''' INSERT INTO PHONEBOOK(Name,PhoneNumber)
              VALUES(?,?) '''
    conn = create_connection()

    with conn:
        task = (name, phone)
        cur = conn.cursor()

        try:
            cur.execute(sql, task)
        except Error as e:
            if "UNIQUE constraint failed" in str(e):
                return "PhoneNumber already Exists", 400

    return "Success", 200

def delete_name(username, name):
    logger.info(f"DB: User: {username} Query: DELETE FROM PHONEBOOK WHERE Name={name}")
    sql = '''DELETE FROM PHONEBOOK WHERE Name=?'''
    conn = create_connection()

    with conn:
        task = (name,)
        cur = conn.cursor()
        cur.execute("SELECT * FROM PHONEBOOK WHERE Name=?", task)
        row = cur.fetchone()

        if row is None:
            return "Name doesn't exist in PhoneBook", 404

        cur.execute(sql, task)

    return "Success", 200

def delete_number(username, phone):
    logger.info(f"DB: User: {username} Query: DELETE FROM PHONEBOOK WHERE PhoneNumber={phone}")
    sql = '''DELETE FROM PHONEBOOK WHERE PhoneNumber=?'''
    conn = create_connection()

    with conn:
        task = (phone,)
        cur = conn.cursor()
        cur.execute("SELECT * FROM PHONEBOOK WHERE PhoneNumber=?", task)
        row = cur.fetchone()

        if row is None:
            return "Phone Number doesn't exist in PhoneBook", 404

        cur.execute(sql, task)

    return "Success", 200
