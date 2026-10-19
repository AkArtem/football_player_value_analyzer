import pandas as pd
import numpy as np
TIER_BY_COMPETITION = {
    'GB1': 3, 'ES1': 3, 'IT1': 3, 'L1': 3, 'FR1': 3,
    'PO1': 2, 'NL1': 2, 'BE1': 2, 'TR1': 2
}

def main_league_tier(apps_recent, competitions):
    apps_recent = apps_recent.merge(competitions[["competition_id", "type"]], on="competition_id", how="left")
    apps = apps_recent[apps_recent["type"] == "domestic_league"]
    
    minutes = apps.groupby(["player_id", "competition_id"])["minutes_played"].sum().reset_index()
    
    idx = minutes.groupby("player_id")["minutes_played"].idxmax()
    main = minutes.loc[idx] 
    
    main = main.rename(columns={"competition_id": "main_league"})
    main["league_tier"] = main["main_league"].map(lambda c: TIER_BY_COMPETITION.get(c, 1))

    return main[["player_id", "main_league", "league_tier"]]
    
    
def filter_before_valuation(apps, valuations):
    apps = apps.merge(valuations[["player_id", "current_date"]], on="player_id")
    apps = apps[apps["date"] <= apps["current_date"]]
    return apps

def recent_window(apps, days=365):
    apps = apps[((apps["current_date"] - apps["date"]).dt.days <= days) & ((apps["current_date"] - apps["date"]).dt.days >= 0)]
    return apps
    
def per90(stat, minutes):
    return np.where(minutes > 0, stat * 90 / minutes, 0)
