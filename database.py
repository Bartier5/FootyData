import sqlite3
import os
from config import DB_PATH, PLAYER_COLUMNS, DATA_DIR
from utils import logger

os.makedirs(DATA_DIR, exist_ok=True)
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        team TEXT,
        league TEXT,
        goals INTEGER DEFAULT 0,
        assists INTEGER DEFAULT 0,
        matches_played INTEGER DEFAULT 0,
        UNIQUE(name, team, league)
    )
                   """)
    conn.commit()
    conn.close()
    logger.info("✓ Players table ready")
def insert_player(player: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT OR IGNORE INTO players
            (name, team, league, goals, assists, matches_played)
            VALUES
                (?, ?, ?, ?, ?, ?)
                       """,( player["name"],
            player["team"],
            player["league"],
            player["goals"],
            player["assists"],
            player["matches_played"]))
        conn.commit()
    except Exception as e:
        logger.error(f"Insert failed for {player.get('name')}: {e}")
    finally:
        conn.close()
def bulk_insert(data: list):
    from utils import row_generator
    inserted = 0
    for row in row_generator(data):
        insert_player(row)
        inserted += 1
    logger.info(f"✓ Bulk insert complete | {inserted} rows processed")
def get_all_players():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    rows = cursor.fetchall()
    conn.close()
    return rows
def get_players_by_goals(min_goals: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM players WHERE goals >= ?",
        (min_goals,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
def update_player_goals(name: str, team: str, new_goals: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE players
        SET goals = ?
        WHERE name = ? AND team = ?
    """, (new_goals, name, team))
    conn.commit()
    conn.close()
    logger.info(f"✓ Updated goals for {name} → {new_goals}")