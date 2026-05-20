import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

DB_PATH  = os.path.join(DATA_DIR, "football.db")
LOG_PATH = os.path.join(LOG_DIR, "scraper.log")
LOG_LEVEL = "DEBUG"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

URLS = {
    "premier_league": "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
    "la_liga":        "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
}

PLAYER_COLUMNS = [
    "name",
    "team",
    "league",
    "goals",
    "assists",
    "matches_played"
]

REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
DELAY_BETWEEN = 2

