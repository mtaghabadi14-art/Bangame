import os
import psycopg2

from utils.titles import get_title
from rubika import send_message


# ==========================================
# اتصال به PostgreSQL (Supabase)
# ==========================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


def connect():

    return psycopg2.connect(
        DATABASE_URL
    )


# ==========================================
# XP مورد نیاز برای Level بعدی
# ==========================================

def get_next_level_xp(level):

    levels = {
        1: 100,
        2: 250,
        3: 500,
        4: 800,
        5: 1200,
        6: 1700,
        7: 2500,
        8: 3500,
        9: 5000,
    }

    return levels.get(
        level,
        level * 700
    )


# ==========================================
# ساخت جدول‌ها
# ==========================================

def create_tables():

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            user_id TEXT PRIMARY KEY,

            nickname TEXT,

            title TEXT DEFAULT '🥉 تازه‌کار',

            coins INTEGER DEFAULT 1000,

            level INTEGER DEFAULT 1,

            xp INTEGER DEFAULT 0,

            typing_games INTEGER DEFAULT 0,

            typing_best_time REAL DEFAULT 0,

            typing_best_wpm REAL DEFAULT 0

        )
        """
    )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================
# اضافه کردن ستون‌های جدید
# ==========================================

def add_typing_columns():

    conn = connect()

    cur = conn.cursor()

    columns = [

        (
            "typing_games",
            "INTEGER DEFAULT 0"
        ),

        (
            "typing_best_time",
            "REAL DEFAULT 0"
        ),

        (
            "typing_best_wpm",
            "REAL DEFAULT 0"
        ),

        (
            "nickname",
            "TEXT"
        ),

        (
            "title",
            "TEXT DEFAULT '🥉 تازه‌کار'"
        ),

    ]

    for name, dtype in columns:

        try:

            cur.execute(
                f"""
                ALTER TABLE users
                ADD COLUMN {name} {dtype}
                """
            )

        except Exception:

            conn.rollback()

    conn.commit()

    cur.close()

    conn.close()


# ==========================================
# ساخت کاربر
# ==========================================

def add_user(user_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users(user_id)
        VALUES(%s)

        ON CONFLICT (user_id)
        DO NOTHING
        """,
        (
            user_id,
        )
    )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================
# گرفتن اطلاعات کاربر
# ==========================================

def get_user(user_id):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            user_id,
            nickname,
            title,
            coins,
            level,
            xp,
            typing_games,
            typing_best_time,
            typing_best_wpm
        FROM users
        WHERE user_id=%s
        """,
        (
            user_id,
        )
    )

    user = cur.fetchone()

    cur.close()

    conn.close()

    return user


# ==========================================
# ذخیره لقب
# ==========================================

def set_nickname(user_id, nickname):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users

        SET nickname=%s

        WHERE user_id=%s
        """,
        (
            nickname,
            user_id
        )
    )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================
# گرفتن لقب
# ==========================================

def get_nickname(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT nickname
        FROM users
        WHERE user_id = %s
        """,
        (user_id,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return result[0]

    return None


# ==========================================
# سکه
# ==========================================

def add_coins(user_id, amount):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users

        SET coins = coins + %s

        WHERE user_id=%s
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================
# XP
# ==========================================

def add_xp(user_id, amount):

    conn = connect()
    cur = conn.cursor()

    # ==========================================
    # گرفتن اطلاعات فعلی
    # ==========================================

    cur.execute(
        """
        SELECT
            level,
            xp,
            title
        FROM users
        WHERE user_id=%s
        """,
        (
            user_id,
        )
    )

    data = cur.fetchone()

    if not data:

        cur.close()
        conn.close()

        return

    old_level, current_xp, old_title = data

    current_xp += amount

    level = old_level

    # ==========================================
    # بررسی Level Up
    # ==========================================

    level_ups = 0

    while True:

        needed_xp = get_next_level_xp(level)

        if current_xp < needed_xp:
            break

        current_xp -= needed_xp
        level += 1
        level_ups += 1

    # ==========================================
    # رتبه جدید
    # ==========================================

    new_title = get_title(level)

    # ==========================================
    # ذخیره اطلاعات
    # ==========================================

    cur.execute(
        """
        UPDATE users

        SET
            xp=%s,
            level=%s,
            title=%s

        WHERE user_id=%s
        """,
        (
            current_xp,
            level,
            new_title,
            user_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    # ==========================================
    # پیام ارتقای Level
    # ==========================================

    if level > old_level:

        send_message(
            user_id,
            f"🎉 Level Up!\n\n"
            f"تبریک! به Level {level} رسیدی! ⭐\n"
            f"✨ XP: {current_xp}/{get_next_level_xp(level)}"
        )

    # ==========================================
    # پیام تغییر رتبه
    # ==========================================

    if new_title != old_title:

        send_message(
            user_id,
            f"🏆 رتبه جدید!\n\n"
            f"تبریک! رتبه‌ات ارتقا پیدا کرد! 🔥\n\n"
            f"{new_title}\n"
            f"⭐ Level {level}"
        )

# ==========================================
# تغییر Level و رتبه
# ==========================================

def set_level(user_id, level):

    conn = connect()

    cur = conn.cursor()

    title = get_title(level)

    cur.execute(
        """
        UPDATE users

        SET
            level=%s,
            title=%s

        WHERE user_id=%s
        """,
        (
            level,
            title,
            user_id
        )
    )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================
# تغییر رتبه
# ==========================================

def set_title(user_id, title):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users

        SET title=%s

        WHERE user_id=%s
        """,
        (
            title,
            user_id
        )
    )

    conn.commit()

    cur.close()

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

        SET xp=%s

        WHERE user_id=%s
        """,
        (
            xp,
            user_id
        )
    )

    conn.commit()

    cur.close()

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

    cur.execute(
        """
        UPDATE users

        SET typing_games = typing_games + 1

        WHERE user_id=%s
        """,
        (
            user_id,
        )
    )

    cur.execute(
        """
        SELECT
            typing_best_time,
            typing_best_wpm

        FROM users

        WHERE user_id=%s
        """,
        (
            user_id,
        )
    )

    data = cur.fetchone()

    new_time_record = False

    new_wpm_record = False

    if data:

        best_time, best_wpm = data

        if best_time == 0 or time_taken < best_time:

            cur.execute(
                """
                UPDATE users

                SET typing_best_time=%s

                WHERE user_id=%s
                """,
                (
                    time_taken,
                    user_id
                )
            )

            new_time_record = True

        if wpm > best_wpm:

            cur.execute(
                """
                UPDATE users

                SET typing_best_wpm=%s

                WHERE user_id=%s
                """,
                (
                    wpm,
                    user_id
                )
            )

            new_wpm_record = True

    conn.commit()

    cur.close()

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

        WHERE user_id=%s
        """,
        (
            user_id,
        )
    )

    data = cur.fetchone()

    cur.close()

    conn.close()

    return data


# ==========================================
# لیدربورد سرعت تایپ
# ==========================================

def get_typing_leaderboard(limit=10):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            user_id,

            typing_best_wpm,

            typing_best_time

        FROM users

        WHERE typing_games > 0

        ORDER BY typing_best_wpm DESC

        LIMIT %s
        """,
        (
            limit,
        )
    )

    data = cur.fetchall()

    cur.close()

    conn.close()

    return data