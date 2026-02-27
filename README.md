# One-Company Investment Dossier — Snowflake (SNOW)

**[Live Demo →](https://astew24.github.io/one-company-investment-dossier--SNOW-Snowflake-)**

Single-name equity deep dive on Snowflake. Covers the investment thesis, financial model, scenario analysis, catalyst tracking, and risk framework. Also includes a Streamlit app that renders the dossier as a structured web page with live price data.

## Investment Thesis

Snowflake can be mispriced when short-term consumption noise dominates the narrative and masks the durability of retention, cash generation, and product-surface expansion.

## What's In Here

| Artifact | Format | |
|---|---|---|
| Streamlit Dossier App | PY | [`streamlit_app.py`](streamlit_app.py) |
| Investment Memo | MD | [`brief/Investment_Memo.md`](brief/Investment_Memo.md) |
| Tear Sheet | MD | [`brief/Tear_Sheet.md`](brief/Tear_Sheet.md) |
| Catalyst & Risk Tracker | MD | [`brief/Catalyst_Tracker.md`](brief/Catalyst_Tracker.md) |
| Interview Talk Track | MD | [`brief/Interview_Talk_Track.md`](brief/Interview_Talk_Track.md) |
| Financial Model Workbook | XLSX | [`model/Model.xlsx`](model/Model.xlsx) |
| Scenario Inputs | CSV | [`model/scenario_assumptions.csv`](model/scenario_assumptions.csv) |
| Monitoring Triggers | CSV | [`model/monitoring_triggers.csv`](model/monitoring_triggers.csv) |
| Sources Log | CSV | [`data/sources_log.csv`](data/sources_log.csv) |

## Streamlit App

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Renders the dossier as a structured web page with thesis header, live SNOW price from `yfinance`, scenario table, KPI history chart, catalyst map, and risk matrix. Fully read-only — no API keys required.

## Methodology

1. **Primary research** — SEC filings, investor materials, earnings updates
2. **Competitive analysis** — BigQuery, Redshift, Synapse, Databricks
3. **Model framework** — scenario assumptions for growth, margin, and valuation sensitivity
4. **Risk testing** — concentration, pricing pressure, consumption volatility, AI monetization uncertainty

## Repository Structure

```
.
├── brief/          # Memo, tear sheet, tracker, and interview notes
├── data/           # Source log
├── docs/           # GitHub Pages site
├── model/          # Workbook + scenario assumptions + notes
├── streamlit_app.py
└── requirements.txt
```

*Independent equity research. Not investment advice.*
