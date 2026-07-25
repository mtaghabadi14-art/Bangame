import sqlite3

DB_NAME = "bangame.db"


# ==========================================
# اتصال دیتابیس
# ==========================================

def connect():

    return sqlite3.connect(DB_NAME)


# ==========================================
# ساخت جدول‌ها
# ==========================================

def create_tables():

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (

        user_id TEXT PRIMARY KEY,

        coins INTEGER DEFAULT 1000,

        level INTEGER DEFAULT 1,

        xp INTEGER DEFAULT 0,

        typing_games INTEGER DEFAULT 0,

        typing_best_time REAL DEFAULT 0,

        typing_best_wpm REAL DEFAULT 0

    )
    """)

    conn.commit()

    conn.close()


# ==========================================
# اضافه کردن ستون‌های جدید
# ==========================================

def add_typing_columns():

    conn = connect()

    cur = conn.cursor()

    columns = [

        ("typing_games", "INTEGER DEFAULT 0"),

        ("typing_best_time", "REAL DEFAULT 0"),

        ("typing_best_wpm", "REAL DEFAULT 0")

    ]

    for name, dtype in columns:

        try:

            cur.execute(
                f"""
                ALTER TABLE users
                ADD COLUMN {name} {dtype}
                """
            )

        except sqlite3.OperationalError:

            pass

    conn.commit()

    conn.close()


# ==========================================
# ساخت کاربر
# ==========================================

def add_user(user_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users(user_id)
        VALUES(?)
        """,
        (user_id,)
    )

    conn.commit()

    conn.close()


# ==========================================
# گرفتن اطلاعات کاربر
# ==========================================

def get_user(user_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user
# ==========================================
# سکه
# ==========================================

def add_coins(user_id, amount):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET coins = coins + ?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()

    conn.close()


# ==========================================
# XP
# ==========================================

def add_xp(user_id, amount):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET xp = xp + ?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()

    conn.close()


# ==========================================
# تغییر Level
# ==========================================

def set_level(user_id, level):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET level = ?
        WHERE user_id=?
        """,
        (
            level,
            user_id
        )
    )

    conn.commit()

    conn.close()


# ==========================================
# تغییر XP
# ==========================================

def set_xp(user_id, xp):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET xp = ?
        WHERE user_id=?
        """,
        (
            xp,
            user_id
        )
    )

    conn.commit()

    conn.close()
    # ==========================================
# آمار سرعت تایپ
# ==========================================

def update_typing_stats(
    user_id,
    time_taken,
    wpm
):

    conn = connect()

    cur = conn.cursor()

    # افزایش تعداد بازی‌ها

    cur.execute(
        """
        UPDATE users
        SET typing_games = typing_games + 1
        WHERE user_id=?
        """,
        (user_id,)
    )

    # گرفتن رکورد قبلی

    cur.execute(
        """
        SELECT
            typing_best_time,
            typing_best_wpm
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    data = cur.fetchone()

    new_time_record = False
    new_wpm_record = False

    if data:

        best_time, best_wpm = data

        # رکورد زمان

        if best_time == 0 or time_taken < best_time:

            cur.execute(
                """
                UPDATE users
                SET typing_best_time=?
                WHERE user_id=?
                """,
                (
                    time_taken,
                    user_id
                )
            )

            new_time_record = True

        # رکورد سرعت

        if wpm > best_wpm:

            cur.execute(
                """
                UPDATE users
                SET typing_best_wpm=?
                WHERE user_id=?
                """,
                (
                    wpm,
                    user_id
                )
            )

            new_wpm_record = True

    conn.commit()

    conn.close()

    return {
        "new_time_record": new_time_record,
        "new_wpm_record": new_wpm_record
    }


# ==========================================
# گرفتن آمار سرعت تایپ
# ==========================================

def get_typing_stats(user_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            typing_games,
            typing_best_time,
            typing_best_wpm
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    data = cur.fetchone()

    conn.close()

    return data