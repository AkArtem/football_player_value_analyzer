# Football Player Value Analyzer

Identifying over/undervalued football players by comparing their actual market value to what a model predicts based on their performance stats.

**[Live Demo](https://football-value-analyzer.streamlit.app/)**

# Overview

I take performance stats (goals, assists, minutes played, age, position) and try to predict a player's market value from that. Then I look at the difference between the actual value and the predicted value (residual), a big negative residual means the player is probably undervalued relative to their stats, a big positive one means overvalued.

This project demonstrates data cleaning, SQL, exploratory analysis, and modeling on a real-world, imperfect football dataset. This is a current value analysis, not a forecast of future seasons. The target is each player's latest available market value, updated within the last 365 days.

# Key Results
- **4,816 players** analyzed after data cleaning
- **Random Forest (tuned):** R²=0.657, RMSE=0.987 — vs R²≈0 for baseline
- Found and fixed temporal data leakage affecting 61% of players
- Live interactive dashboard deployed on Streamlit Cloud

# Skills Demonstrated
- Data cleaning & quality auditing (staleness, leakage, low-sample noise)
- SQL (JOINs, window functions: RANK/DENSE_RANK/LAG)
- Feature engineering, EDA, ML modeling with cross-validation
- Deployment (Streamlit Cloud)

# Data

Source: [davidcariboo/player-scores](https://www.kaggle.com/datasets/davidcariboo/player-scores) on Kaggle, scraped from Transfermarkt, auto-updated weekly.
Raw CSVs aren't committed here because of file size, see [data/README.md](data/README.md) for which files you need and how to set them up.

### Data problems found and fixed

This dataset required significant cleaning before it could be used reliably.
Full details in [data/README.md](data/README.md), summarized here:

- **Valuation staleness:** median time since last valuation update across all players is ~2.7 years; 81% of records are older than 12 months. Analysis is restricted to players with a valuation update within the last 365 days.
- **Missing appearance data:** 390 players (6.5%) had a valuation but no match appearance records — excluded from the feature set.
- **Temporal data leakage:** the initial feature aggregation included match appearances recorded after each player's valuation date, meaning future performance was leaking into features meant to explain a past value. Affected 3,406 of 5,613 players (61%), with a median leakage window of 150 days (max 378 days). Fixed by filtering each player's appearance stats to only include matches on or before their individual valuation date.
- Final analysis dataset after cleaning: **4,816 players**.

## Tech Stack

- Python: pandas, numpy, scipy, scikit-learn, matplotlib, seaborn, joblib, Streamlit
- SQL: sqlite3 (in-memory), queries in `sql/`
- Git/GitHub

## Repository Structure

```
notebooks/ — data cleaning, leakage fix, SQL queries, EDA, modeling
sql/       — SQL queries (JOINs, RANK/DENSE_RANK, LAG)
data/      — data docs (raw files not committed, see data/README.md)
app/       — Streamlit dashboard
```

## Notebooks (in order)

1. `01_data_overview.ipynb` — loading and checking all the raw tables
2. `02_data_check.ipynb` — valuation freshness, current/peak value per player
3. `03_features.ipynb` — first version of feature engineering (turned out to have the leakage bug)
4. `04_check.ipynb` — found and fixed the temporal leakage, produced the final clean feature table
5. `05_sql.ipynb` — SQL queries: top scorers, per-90 stats, ranking by position, value change over time
6. `06_eda.ipynb` — exploratory analysis on the clean data
7. `07_modeling.ipynb` — baselines, linear/lasso/ridge, random forest with CV and tuning, residual analysis
8. `08_sensitivity.ipynb` — sensitivity check on the valuation-freshness cutoff (90/180/365/540 days)

## SQL

All queries in `sql/`, run through sqlite3 from Python. Covers JOINs, aggregation, RANK()/DENSE_RANK() (ranking players within their position), and LAG() (tracking how a player's value changed over time).

## Modeling results

Model selection happened in two stages: a broad comparison of baselines and linear models on a single train/test split (base features), followed by 5-fold cross-validated, out-of-fold evaluation of the final candidate feature set (recency-weighted stats + league/country tier) to pick and honestly score the deployed model.

**Stage 1 - baseline exploration (single train/test split, base features)**

| Model | RMSE (log scale) | R² |
|---|---|---|
| Mean baseline | 1.686 | -0.0004 |
| Median baseline | 1.689 | -0.0041 |
| Age-only | 1.600 | 0.0988 |
| Minutes-only | 1.640 | 0.0541 |
| Linear Regression | 1.206 | 0.4885 |
| Lasso | 1.217 | 0.4787 |
| Ridge | 1.206 | 0.4887 |

**Stage 2 - final validation (5-fold cross-validated, out-of-fold predictions, recency + league-tier features)**

| Model | RMSE (log scale) | R² |
|---|---|---|
| Mean baseline | 1.655 | -0.021 |
| Minutes-only | 1.618 | 0.024 |
| Linear Regression | 1.108 | 0.543 |
| **Tuned Random Forest** | **1.040** | **0.597** |

Tuned Random Forest with recency-weighted stats + league tier is the best model, and it's what's deployed in the live app: `predicted_log_value`/`residual` in `dashboard_data.csv` are exactly these out-of-fold predictions, so the numbers above reflect what you'll actually see when you use the dashboard. Feature importance still shows playing time as dominant, but recency and market-tier signals improve overall fit and reduce top-end underprediction versus the base model.

## Residual analysis

Residual = actual log(value) - predicted log(value). Negative means the model thinks the player should be worth more than the market says (undervalued). Positive means overvalued.

Two patterns showed up in the biggest residuals:

1. Young players (18-25) with almost no playing time get overvalued by the model - the market pays for potential/hype, which isn't in the data at all.
2. Older players (25-33) with a lot of career minutes get undervalued by the model - total_minutes is the model's strongest feature, so it assumes lots of minutes means high value, but the real market already discounted them for age.

Goalkeepers had the widest residual spread of any position, makes sense since goals/assists per 90 barely mean anything for a keeper.

## Known Limitations

- Transfermarkt valuations are editorial estimates, not actual transaction prices.
- The dataset does not capture contract length, injury history, or transfer demand, all of which affect real market value but aren't available as features.
- Market value prediction is a well-studied problem; this project's differentiator is execution depth and data quality rigor (systematic leakage detection and correction, staleness-aware filtering), not methodological novelty.

## How to run locally

```bash
git clone https://github.com/AkArtem/football_player_value_analyzer.git
cd football_player_value_analyzer
pip install -r requirements.txt
```

Download the dataset from Kaggle (see `data/README.md`), put the CSVs in
`data/`, then run the notebooks in order (01 → 08).

Streamlit app:
```bash
streamlit run app/streamlit_app.py
```

## License

MIT