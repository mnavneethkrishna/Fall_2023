import sqlite3
from sqlite3 import Error
from flask import Response
from validate import validate_username, validate_password

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import configparser

config = configparser.ConfigParser()
config.read('db_config.ini')

def login(data):
    try:
        username = data.get('username')
        if not username or not validate_username(username):
            return False, Response("Invalid Credentials! Username format is incorrect.", status=400, mimetype='application/json')
    except Exception as e:
        logger.error(f"Error while processing username: {e}")
        return False, Response("Invalid Credentials! Username missing.", status=400, mimetype='application/json')

    logger.info(f"LOGIN: LOGIN VALIDATE ATTEMPT SUCCESS, USERNAME={username}")

    try:
        password = data.get('password')
        if not password or not validate_password(password):
            return False, Response("Invalid Credentials! Password format is incorrect.", status=400, mimetype='application/json')
    except Exception as e:
        logger.error(f"Error while processing password: {e}")
        return False, Response("Invalid Credentials! Password missing.", status=400, mimetype='application/json')

    if not check_user(username, password):
        return False, Response("Invalid Credentials! Username or password is incorrect.", status=400, mimetype='application/json')
    else:
        return True, ""

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(config['loginDB']['db_name'])
    except Error as e:
        logger.error(e)
    return conn

def check_user(username, password):
    logger.info(f"LOGIN: LOGIN ATTEMPT, USERNAME={username}")
    sql = ''' SELECT username, password FROM USERS1021;'''
    conn = create_connection()

    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        output = cur.fetchall()

    for user in output:
        if username == user[0] and password == user[1]:
            logger.info(f"LOGIN: LOGIN SUCCESS, USERNAME={username}")
            return True

    logger.info(f"LOGIN: LOGIN FAILED, USERNAME={username}")
    return False
