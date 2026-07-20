import sqlite3


DB_NAME = "bangame.db"


def connect():
    return sqlite3.connect(DB_NAME)



def create_tables():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        coins INTEGER DEFAULT 1000,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()



def add_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )

    conn.commit()
    conn.close()



def get_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user