import sqlite3

from config import DATABASE
from db.queries import (
    CREATE_QUESTIONS_TABLE,
    CREATE_RESULTS_TABLE,
    CREATE_USERS_TABLE
)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # строки возвращает как словари
    return conn

def init_db():
    conn = get_db()
    conn.execute(CREATE_USERS_TABLE)
    conn.execute(CREATE_QUESTIONS_TABLE)
    conn.execute(CREATE_RESULTS_TABLE)
    conn.commit()
    conn.close()