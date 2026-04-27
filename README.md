# Snowflake (SNOW) investment dossier

[Live demo](https://astew24.github.io/one-company-investment-dossier--SNOW-Snowflake-)

Single-name equity deep dive on Snowflake: investment memo, tear sheet,
catalyst / risk tracker, financial model workbook, and a Streamlit app
that renders the whole thing as a structured web page with live price
from `yfinance`.

## Thesis, in one sentence

Snowflake can be mispriced when short-term consumption noise dominates
the narrative and masks the durability of retention, cash generation,
and product-surface expansion.

## What's in here

| File | Description |
|---|---|
| [`streamlit_app.py`](streamlit_app.py) | Dossier app that stitches the briefs together |
| [`brief/Investment_Memo.md`](brief/Investment_Memo.md) | Full memo |
| [`brief/Tear_Sheet.md`](brief/Tear_Sheet.md) | One-pager: thesis, scenarios, what could break |
| [`brief/Catalyst_Tracker.md`](brief/Catalyst_Tracker.md) | Event calendar and monitoring triggers |
| [`brief/Interview_Talk_Track.md`](brief/Interview_Talk_Track.md) | 2-minute talking points |
| [`model/Model.xlsx`](model/Model.xlsx) | Workbook |
| [`model/scenario_assumptions.csv`](model/scenario_assumptions.csv) | Bear / base / bull driver set |
| [`model/monitoring_triggers.csv`](model/monitoring_triggers.csv) | KPI thresholds and responses |
| [`data/sources_log.csv`](data/sources_log.csv) | Primary-source citations |

## Running the Streamlit app

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

No API keys. Live price pulled from `yfinance`; everything else reads
from the files in this repo.

## How the research was built

1. Primary research: SEC filings, investor materials, earnings updates.
2. Competitive context: BigQuery, Redshift, Synapse, Databricks.
3. Model framework: scenario assumptions on growth, margin, and
   valuation sensitivity.
4. Risk framing: concentration, pricing pressure, consumption
   volatility, AI monetization uncertainty.

*Independent equity research. Not investment advice.*
