import pandas as pd
from config import PLAYER_COLUMNS
from utils import logger, log_call

@log_call
def clean_data(players: list):
    if not players:
        logger.warning("No player data to clean")
        return pd.DataFrame()
    df = pd.DataFrame(players, columns=PLAYER_COLUMNS)
    before = len(df)
    df = df.drop_duplicates(subset=["name", "team", "league"])
    after = len(df)
    logger.info(f"✓ Dropped {before - after} duplicates")
    df = df.dropna(subset=["name", "team"])
    df["goals"]          = pd.to_numeric(df["goals"],          errors="coerce").fillna(0).astype(int)
    df["assists"]        = pd.to_numeric(df["assists"],        errors="coerce").fillna(0).astype(int)
    df["matches_played"] = pd.to_numeric(df["matches_played"], errors="coerce").fillna(0).astype(int)
    df["name"]   = df["name"].str.strip()
    df["team"]   = df["team"].str.strip()
    df["league"] = df["league"].str.strip()

    logger.info(f"✓ Clean complete | {len(df)} players ready")
    return df
@log_call
def top_scorers(df: pd.DataFrame, min_goals: int = 10):
    filtered = df[df["goals"] >= min_goals]
    sorted_df = filtered.sort_values("goals", ascending=False)
    logger.info(f"✓ Top scorers with {min_goals}+ goals: {len(sorted_df)}")
    return sorted_df

@log_call
def goals_by_team(df: pd.DataFrame):
    result = df.groupby("team")["goals"].sum().sort_values(ascending=False)
    logger.info(f"✓ Goals by team calculated | {len(result)} teams")
    return result

@log_call
def league_averages(df: pd.DataFrame):
    result = df.groupby("league").agg(
        avg_goals    = ("goals",          "mean"),
        avg_assists  = ("assists",        "mean"),
        total_players= ("name",           "count")
    ).round(2)
    logger.info(f"✓ League averages calculated")
    return result

@log_call
def export_csv(df: pd.DataFrame, path: str = "data/players.csv"):
    df.to_csv(path, index=False)
    logger.info(f"✓ Exported to {path}")