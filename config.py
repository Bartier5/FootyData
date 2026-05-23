import os
import random
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(DATA_DIR, "logs")

DB_PATH  = os.path.join(DATA_DIR, "football.db")
LOG_PATH = os.path.join(LOG_DIR, "scraper.log")
LOG_LEVEL = "DEBUG"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]


URLS = {
    "premier_league": "https://www.transfermarkt.us/premier-league/scorers/wettbewerb/GB1",
    "la_liga": "https://www.transfermarkt.us/laliga/scorers/wettbewerb/ES1",
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
DELAY_BETWEEN = 5

def get_headers():
  return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com",
        "Upgrade-Insecure-Requests": "1",
    }