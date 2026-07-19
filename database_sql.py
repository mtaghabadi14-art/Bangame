import sqlite3

connection = sqlite3.connect("bangame.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
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
    (name, coins, xp, level, wins, losses, last_reward)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        player.name,
        player.coins,
        player.xp,
        player.level,
        player.wins,
        player.losses,
        player.last_reward
    ))

    connection.commit()


def get_player(name):
    cursor.execute("""
    SELECT name, coins, xp, level, wins, losses, last_reward
    FROM players
    WHERE name = ?
    """, (name,))

    return cursor.fetchone()