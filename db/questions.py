import sqlite3

from db.database import get_db
from db.queries import INSERT_QUESTION, GET_ALL_QUESTIONS, GET_QUESTION_BY_ID, DELETE_QUESTION_BY_ID


def add_question(question_text: str, correct_answer: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(INSERT_QUESTION, (question_text, correct_answer))
        conn.commit()
        new_id = cursor.lastrowid
        return new_id
    except sqlite3.IntegrityError:
        return None  # такой вопрос уже есть
    finally:
        conn.close()

def get_all_questions():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute(GET_ALL_QUESTIONS).fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_question(question_id: int):
    conn = get_db()
    row = conn.execute(GET_QUESTION_BY_ID, (question_id, )).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_question(question_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(DELETE_QUESTION_BY_ID, (question_id,))
    conn.commit()
    deleted = cursor.rowcount > 0

    conn.close()
    return deleted

