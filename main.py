import os
import sys
from config import DATA_DIR,LOG_DIR,DB_PATH
from utils import logger
from scraper import scrape_all
from parser import parse_all
from cleaner import clean_data, top_scorers, goals_by_team, league_averages,export_csv
from database import create_table, bulk_insert, get_all_players, get_players_by_goals

def bootstrap():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    create_table()
    logger.info("✓ FOOTYDATA initialized")
def run_pipeline():
    logger.info("═══ Starting full pipeline ═══")
    raw_results = scrape_all()
    if not raw_results:
        logger.error("✗ No data scraped. Exiting pipeline.")
        return
    players = parse_all(raw_results)
    if not players:
        logger.error("✗ No players parsed. Exiting pipeline.")
        return
    df = clean_data(players)
    if df.empty:
        logger.error("✗ DataFrame empty after cleaning. Exiting.")
        return
    bulk_insert(df.to_dict(orient="records"))
    export_csv(df)
    logger.info("═══ Pipeline complete ═══")
def show_menu():
      print("""
╔══════════════════════════════╗
║       FOOTYDATA CLI          ║
╠══════════════════════════════╣
║  1. Run full scrape pipeline ║
║  2. View all players         ║
║  3. Top scorers              ║
║  4. Goals by team            ║
║  5. League averages          ║
║  6. Export CSV               ║
║  7. Exit                     ║
╚══════════════════════════════╝
    """)

def handle_choice(choice : str):
    if choice == "1":
        run_pipeline()
    elif choice == "2":
        rows = get_all_players()
        if not rows:
            print("No players in database yet. Run the pipeline first.")
            return
        print(f"\n{'ID':<5} {'Name':<25} {'Team':<20} {'League':<15} {'G':<5} {'A':<5} {'MP':<5}")
        print("─" * 80)
        for row in rows:
            print(f"{row['id']:<5} {row['name']:<25} {row['team']:<20} {row['league']:<15} {row['goals']:<5} {row['assists']:<5} {row['matches_played']:<5}")
    elif choice == "3":
        try:
            min_g = int(input("Minimum goals (default 10): ") or 10)
        except ValueError:
            min_g = 10
        rows = get_players_by_goals(min_g)
        if not rows:
            print(f"No players with {min_g}+ goals found.")
            return
        print(f"\n{'Name':<25} {'Team':<20} {'Goals':<6}")
        print("─" * 55)
        for row in rows:
            print(f"{row['name']:<25} {row['team']:<20} {row['goals']:<6}")
    elif choice == "4":
        rows = get_all_players()
        if not rows:
            print("No data yet.")
            return
        import pandas as pd
        df = pd.DataFrame([dict(r) for r in rows])
        result = goals_by_team(df)
        print("\n── Goals by Team ──")
        print(result.to_string())
    elif choice == "5":
        rows = get_all_players()
        if not rows:
            print("No data yet.")
            return
        import pandas as pd
        df = pd.DataFrame([dict(r) for r in rows])
        result = league_averages(df)
        print("\n── League Averages ──")
        print(result.to_string())

    elif choice == "6":
        rows = get_all_players()
        if not rows:
            print("No data yet.")
            return
        import pandas as pd
        df = pd.DataFrame([dict(r) for r in rows])
        export_csv(df)
        print("✓ Exported to data/players.csv")

    elif choice == "7":
        logger.info("FOOTYDATA exiting.")
        print("Goodbye.")
        sys.exit(0)

    else:
        print("Invalid choice. Pick 1–7.")
if __name__ == "__main__":
    bootstrap()
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
        handle_choice(choice)