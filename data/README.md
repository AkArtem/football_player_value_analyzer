# Data
Source: https://www.kaggle.com/datasets/davidcariboo/player-scores

Not committed due to file size. Download the dataset and unzip all CSV files into this `data/` folder:

```bash
pip install kaggle
kaggle datasets download -d davidcariboo/player-scores -p data --unzip
```

Or download the ZIP manually from the Kaggle page and unzip it here.

| Notebook | Raw files it reads |
|---|---|
| 01_data_overview | all raw tables (overview only) |
| 02_data_check | player_valuations.csv, players.csv |
| 03_features | appearances.csv, players.csv (+ player_values_fresh.csv from 02) |
| 04_check | appearances.csv, games.csv, players.csv (+ outputs of 03) |
| 05_sql | appearances.csv, players.csv, player_valuations.csv, competitions.csv (+ outputs of 03/04) |
| 06_eda | players_fresh_final.csv (output of 04) |
| 07_modeling | appearances.csv, games.csv, competitions.csv (+ players_fresh_final.csv) |
| 08_sensitivity | appearances.csv, competitions.csv, player_valuations.csv, players.csv |

Run the notebooks in order (01 → 08); later notebooks use CSVs written by earlier ones. The app and the tests only need `app/dashboard_data.csv` and `app/metrics.json`, which are committed.

# Data snapshot

- Downloaded from Kaggle on 2026-07-11. The upstream project (dcaribou/transfermarkt-datasets) has paused updates, so this is the final available snapshot.
- Latest match in the data: 2026-07-06. Latest market valuation: 2026-02-27.
- Target variable: each player's latest available market value, using valuations updated within the last 365 days, not a season-end or future-season prediction.

# Data quality note

Player valuation freshness varies significantly (median: 2.7 years since last update). 
Analysis is focused on players with a valuation update within the last 12 months, to ensure current-value estimates reflect active market pricing.

Excluded 390 (6.5% of fresh players) players with a valuation but no appearance data in the dataset.

# Leakage fix

Performance stats from appearances.csv included appearances recorded after each player's valuation date, so future performance was influencing a value that was already set in the past.

- 3406 of 5613 fresh players affected, median leakage 150 days, max 378 days

28 players had all of their appearances after their valuation date and were dropped (5,613 → 5,585).

# Low-minutes noise filter

Players with under 300 total career minutes were excluded, per-90 stats (goals/assists per 90 minutes) become unreliable at very low sample sizes.
Removed rather than zeroed out, to avoid falsely teaching the model that low-minute players have zero output.

Final dataset after all cleaning steps: **4,816 players**.

# Modeling notes

Final model features: age, age^2, total career minutes and position, plus recent form (minutes, goals and assists per 90 in the 365 days before each player's valuation) and league tier (tier of the player's main domestic league, mapped by competition_id in src/features.py). See the main README for the model comparison table and results.
