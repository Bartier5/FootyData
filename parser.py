from bs4 import BeautifulSoup
from config import PLAYER_COLUMNS
from utils import logger, log_call

def parse_league(raw: dict):
    league = raw["league"]
    html   = raw["html"]
    players = []

    try:
        soup  = BeautifulSoup(html, "html.parser")
        table = soup.find_all("table")[1]

        if not table:
            logger.warning(f"No stats table found for {league}")
            return []

        rows = table.find_all("tr")

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) < 9:
                continue

            try:
                # grab team from the image alt tag inside the row
                team_link = cols[7].find("a")
                team = team_link["title"] if team_link else "Unknown"

                player = {
                    "name":           cols[3].text.strip(),
                    "team":           team,
                    "league":         league,
                    "goals":          int(cols[8].text.strip() or 0),
                    "assists":        0,
                    "matches_played": int(cols[9].text.strip() or 0),
                }
                players.append(player)
            except (ValueError, IndexError) as e:
                logger.warning(f"Skipping malformed row in {league}: {e}")
                continue

    except Exception as e:
        logger.error(f"Parse failed for {league}: {e}")

    logger.info(f"✓ Parsed {len(players)} players from {league}")
    return players
@log_call
def parse_all(raw_results: list):
    all_players = []
    for raw in raw_results:
        players = parse_league(raw)
        all_players.extend(players)
    logger.info(f"✓ Total players parsed: {len(all_players)}")
    return all_players