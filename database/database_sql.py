import sqlite3

connection = sqlite3.connect("bangame.db", check_same_thread=False)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    coins INTEGER,
    xp INTEGER,
    level INTEGER,
    wins INTEGER,
    losses INTEGER,
    last_reward TEXT
)
""")

connection.commit()


def add_player(player):
    cursor.execute("""
    INSERT OR REPLACE INTO players
    (
        user_id,
        name,
        coins,
        xp,
        level,
        wins,
        losses,
        last_reward
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        player.user_id,
        player.name,
        player.coins,
        player.xp,
        player.level,
        player.wins,
        player.losses,
        player.last_reward
    ))

    connection.commit()


def get_player(user_id):

    cursor.execute("""
    SELECT
        user_id,
        name,
        coins,
        xp,
        level,
        wins,
        losses,
        last_reward
    FROM players
    WHERE user_id = ?
    """, (user_id,))

    return cursor.fetchone()


def get_all_players():

    cursor.execute("""
    SELECT *
    FROM players
    ORDER BY coins DESC
    """)

    return cursor.fetchall()


def delete_player(user_id):

    cursor.execute("""
    DELETE FROM players
    WHERE user_id = ?
    """, (user_id,))

    connection.commit()