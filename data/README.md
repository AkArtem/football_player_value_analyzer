# Data
Source: https://www.kaggle.com/datasets/davidcariboo/player-scores

Files used in project:
- appearances.csv
- player_valuations.csv
- players.csv
- games.csv
- competitions.csv
- clubs.csv
- transfers.csv

Not committed due to file size.

# Data changes

- Dataset auto-updates weekly from Transfermarkt (source: dcaribou/transfermarkt-datasets). Data taken 2026-07-11
- Removed 15 rows from `transfers.csv` (data with transfer_date after 2026-07-01)
- Target variable: each player's latest available market value, using valuations updated within the last 365 days — not a season-end or future-season prediction

# Data quality note

Player valuation freshness varies significantly (median: 2.7 years since last update). 
Analysis is focused on players with a valuation update within the last 12 months, to ensure current-value estimates reflect active market pricing.

Excluded 390 (6.5% of fresh players) players with a valuation but no appearance data in the dataset.

# Leakage fix

Performance stats from appearances.csv included appearances recorded after each player's valuation date, so future performance was influencing a value that was already set in the past.

- 3406 of 5613 fresh players affected, median leakage 150 days, max 378 days
Examples of impact (total goals: before -> after fix):
- Harry Kane: 414 -> 382
- Erling Haaland: 259 -> 237
- Ousmane Dembélé: 121 -> 102

No players lost entirely to the leakage fix (0 players with total_minutes == 0 after filtering).

# Low-minutes noise filter

Players with under 300 total career minutes were excluded, per-90 stats (goals/assists per 90 minutes) become unreliable at very low sample sizes.
Removed rather than zeroed out, to avoid falsely teaching the model that low-minute players have zero output.

Final dataset after all cleaning steps: **4,816 players**.

# Modeling notes

Final model uses recency-weighted stats (last 1-2 seasons instead of full career) and a league/country tier feature, in addition to age, age², total minutes
and position. See main README for model comparison table and results.