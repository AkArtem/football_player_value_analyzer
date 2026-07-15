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
- Removed 15 rows from `transfers.csv`(data with transfer_date after 2026-07-01)
- Target variable: player market value matched to the end of the last completed season

# Data quality note
Player valuation freshness varies significantly (median: 2.7 years since last update)
Analysis is focused on players with a valuation update within the last 12 months, to ensure current-value estimates reflect active market pricing