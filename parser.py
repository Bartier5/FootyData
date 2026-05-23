from bs4 import BeautifulSoup
from config import PLAYER_COLUMNS
from utils import logger, log_call

def parse_league(raw: dict):
    league = raw["league"]
    html = raw["html"]
    players = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class":"items"})
        
        if not table:
            logger.warning(f"No stats table found for {league}")
            return []
        tbody = table.find("tbody")
        rows = tbody.find_all("tr")
        for row in rows:
            if row.get("class") and "thead" in row.get("class"):
                continue
            cols = row.find_all("td")
            if len (cols) < 6:
                continue
            try:
                player = {
                    "name":           cols[1].text.strip(),
                     "team":           cols[5].text.strip(),
                    "league":         league,
                    "goals":          int(cols[7].text.strip() or 0),
                     "assists":        int(cols[8].text.strip() or 0),
                     "matches_played": int(cols[3].text.strip() or 0),
                }
                players.append(player)
            except(ValueError, IndexError) as e:
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