# FOOTYDATA 🏆

An async football stats scraper, cleaner, and analyzer CLI built in Python.
Scrapes top scorer data from Transfermarkt across multiple leagues,
stores it in SQLite, and lets you query and analyze it from the terminal.

## Stack
- **aiohttp** — async concurrent HTTP scraping
- **BeautifulSoup4** — HTML parsing and data extraction
- **Pandas** — data cleaning, filtering, and analysis
- **SQLite** — local persistent storage with deduplication
- **asyncio** — concurrent league fetching
- **logging** — file + terminal logging with timing decorators

## Project Structure
FOOTYDATA/
├── config.py        # URLs, constants, headers, settings
├── utils.py         # Logger, decorators, generator
├── scraper.py       # Async aiohttp scraper with retry logic
├── parser.py        # BeautifulSoup HTML parser
├── cleaner.py       # Pandas cleaning and analysis
├── database.py      # SQLite CRUD with parameterized queries
├── main.py          # CLI entry point
└── data/
├── football.db  # SQLite database
├── players.csv  # Exported CSV
└── logs/
└── scraper.log

## Setup
```bash
git clone https://github.com/Bartier5/footydata.git
cd footydata
pip install -r requirements.txt
python main.py
```

## Features
- Concurrent async scraping of multiple leagues simultaneously
- Rotating user-agent headers for anti-bot evasion
- Automatic retry logic with configurable delays
- Pandas deduplication and type validation pipeline
- SQLite storage with UNIQUE constraint deduplication
- CLI menu with 6 options:
  - Run full scrape pipeline
  - View all players
  - Filter by top scorers
  - Goals by team
  - League averages
  - Export to CSV

## Supported Leagues
| League | Source |
|---|---|
| Premier League | Transfermarkt |
| La Liga | Transfermarkt |

## Adding a New League
Open `config.py` and add to the URLS dict:
```python
URLS = {
    "premier_league": "https://www.transfermarkt.com/...",
    "la_liga":        "https://www.transfermarkt.com/...",
    "bundesliga":     "https://www.transfermarkt.com/...",  # add here
}
```

## Key Concepts Demonstrated
- Async/await with aiohttp and asyncio.gather()
- Decorator pattern for logging and timing
- Generator-based row processing
- Parameterized SQLite queries
- Pandas groupby, boolean indexing, aggregation
- Anti-bot evasion with header rotation
- Production-grade error handling and logging

## Author
Anjikwi Peter — [github.com/Bartier5](https://github.com/Bartier5)