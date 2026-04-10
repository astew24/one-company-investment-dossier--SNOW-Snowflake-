# One-Company Investment Dossier — Snowflake (SNOW)

**Asset Class:** Public Equity — Growth SaaS / Cloud Infrastructure  
**Project Focus:** Single-name equity underwriting process  
**Recruiting Use:** Finance / Equity Research / Investment Analyst applications  
**Role Fit:** Equity Research, Long-Only AM, Public-Markets Analyst tracks  
**Live Demo:** [astew24.github.io/one-company-investment-dossier--SNOW-Snowflake-](https://astew24.github.io/one-company-investment-dossier--SNOW-Snowflake-)  
**Repository:** [github.com/astew24/one-company-investment-dossier--SNOW-Snowflake-](https://github.com/astew24/one-company-investment-dossier--SNOW-Snowflake-)

## Investment Thesis
Snowflake can be mispriced when short-term consumption noise dominates the narrative and masks the durability of retention, cash generation, and product-surface expansion.

## Deliverables

| Artifact | Format | Status |
|---|---|---|
| Streamlit Dossier App | PY | [`streamlit_app.py`](streamlit_app.py) |
| Investment Memo | MD | [`brief/Investment_Memo.md`](brief/Investment_Memo.md) |
| Tear Sheet | MD | [`brief/Tear_Sheet.md`](brief/Tear_Sheet.md) |
| Catalyst & Risk Tracker | MD | [`brief/Catalyst_Tracker.md`](brief/Catalyst_Tracker.md) |
| Interview Talk Track | MD | [`brief/Interview_Talk_Track.md`](brief/Interview_Talk_Track.md) |
| Financial Model Workbook | XLSX | [`model/Model.xlsx`](model/Model.xlsx) |
| Scenario Inputs | CSV | [`model/scenario_assumptions.csv`](model/scenario_assumptions.csv) |
| Monitoring Triggers | CSV | [`model/monitoring_triggers.csv`](model/monitoring_triggers.csv) |
| Model Notes | MD | [`model/README.md`](model/README.md) |
| Sources Log | CSV | [`data/sources_log.csv`](data/sources_log.csv) |
| Python Dependencies | TXT | [`requirements.txt`](requirements.txt) |

## Streamlit App

The repo now includes a read-only Streamlit presentation in [`streamlit_app.py`](streamlit_app.py). It renders the dossier as a structured web page with:

- thesis header and live SNOW price from `yfinance`
- long / short debate view from the markdown briefs
- scenario table from [`model/scenario_assumptions.csv`](model/scenario_assumptions.csv)
- KPI history chart from [`model/Model.xlsx`](model/Model.xlsx)
- catalyst map, risk matrix, and full source log tables

### Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Notes

- The app is fully read-only.
- No API keys are required.
- `yfinance` is used for the live market price.
- The repo does not currently store explicit scenario price targets, so the app falls back to `yfinance` analyst low / mean / high targets for the valuation comparison chart until authored targets are added.

## What Makes This Project Useful In Recruiting
- Uses explicit decision rules rather than thesis-only language.
- Separates catalyst tracking from valuation assumptions to avoid narrative drift.
- Includes a repeatable post-earnings workflow (update KPIs, re-score risks, re-check scenario ranges).
- Documents what would invalidate the thesis, not only what supports it.

## Analyst Skills Demonstrated
- Driver-based modeling: scenario framing with explicit sensitivity ranges
- Public-market diligence: SEC-driven workflow and recurring earnings updates
- KPI-based underwriting: NRR, growth quality, operating leverage, cash conversion
- Competitive work: Snowflake vs. hyperscaler and data-platform alternatives
- Investment communication: memo, tear sheet, and event tracker built for decision use
- Process evidence: 12-quarter KPI sheet + source log for repeatable updates

## Methodology
1. **Primary research** — SEC filings, investor materials, earnings updates
2. **Competitive analysis** — BigQuery, Redshift, Synapse, Databricks pricing and positioning
3. **Model framework** — scenario assumptions for growth, margin, and valuation sensitivity
4. **Risk testing** — concentration, pricing pressure, consumption volatility, AI monetization uncertainty

## Repository Structure

```
.
├── brief/          # Memo, tear sheet, tracker, and interview notes
├── data/           # Source log for evidence tracking
├── docs/           # GitHub Pages site
├── model/          # Workbook + scenario assumptions + notes
├── streamlit_app.py
├── requirements.txt
└── README.md
```

*Independent equity research project. Not investment advice.*
