import os
import sys
import pandas as pd

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.features import main_league_tier, filter_before_valuation, recent_window, per90

def test_no_matches_after_valuation():
    apps = pd.DataFrame({
        "player_id": [1, 1, 2, 2],
        "date": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-01-15", "2025-02-15"])
    })
    
    valuations = pd.DataFrame({
        "player_id": [1, 2],
        "current_date": pd.to_datetime(["2025-01-15", "2025-02-15"])
    })
    
    result = filter_before_valuation(apps, valuations)
    
    assert len(result) == 3
    assert (result["date"] <= result["current_date"]).all()

def test_recent_window_drops_all_matches():
    apps = pd.DataFrame({
        "player_id": [1, 1, 2, 2],
        "date": pd.to_datetime(["2024-10-01", "2025-09-01", "2024-11-01", "2025-08-01"]),
        "current_date": pd.to_datetime(["2025-12-01", "2025-12-01", "2025-12-01", "2025-12-01"]),
    })
    result = recent_window(apps, days=365)
    assert len(result) == 2
    
def test_league_tier_mapping():
    apps_recent = pd.DataFrame({
        "player_id": [1, 1, 2, 3],
        "competition_id": ["PO1", "CL", "A1", "GB1"],
        "minutes_played": [100, 500, 800, 1200]
    })
    
    competitions = pd.DataFrame({
        "competition_id": ["PO1", "CL", "A1", "GB1"],
        "type": ["domestic_league", "international_cup", "domestic_league", "domestic_league"]
    })
    
    result = main_league_tier(apps_recent, competitions).set_index("player_id")["league_tier"]
    
    assert result[1] == 2 
    assert result[2] == 1
    assert result[3] == 3
    
def test_per90_zero_minutes():
    df = pd.DataFrame({
        "player_id": [3, 2, 1],
        "minutes_played": [150, 0, 0]
    })
    result = per90(df["minutes_played"], df["minutes_played"])
    assert result[0] == 90
    assert result[1] == 0
    assert result[2] == 0
    
def test_dashboard_data():
    df = pd.read_csv(os.path.join(ROOT, "app", "dashboard_data.csv"))
    features = ["age", "age_squared", "total_minutes", "recent_goals_per_90", "recent_assists_per_90", "recent_minutes", "league_tier", "league_tier_missing"]
    
    assert len(df) == 4816
    assert df["player_id"].nunique() == 4816
    assert df[features].isna().sum().sum() == 0