# Model Notes

## Files
- `Model.xlsx` — KPI history sheet with illustrative historical + projection rows
- `scenario_assumptions.csv` — base/bull/bear inputs used for valuation and sensitivity framing
- `monitoring_triggers.csv` — KPI thresholds used for post-earnings conviction updates

## KPI Definitions
- `revenue`: product + related services revenue
- `yoy_growth_%`: year-over-year growth on reported revenue
- `gross_margin_%`: gross profit / revenue
- `s&m_%rev`, `r&d_%rev`, `g&a_%rev`: operating expense ratios
- `arr`: annualized recurring run-rate proxy used for trend tracking
- `nrr_%`: net revenue retention
- `churn_%`: gross customer churn proxy
- `arpu`: average revenue per customer proxy
- `cfo`, `capex`, `fcf`: cash from operations, capital expenditures, and free cash flow

## How To Use
1. Update KPI history after each quarterly earnings release.
2. Reconcile management guidance changes into scenario assumptions.
3. Re-score monitoring triggers and adjust scenario probabilities.
4. Re-run valuation sensitivity when NRR, margin, or discount-rate assumptions shift.

## QC Checklist Before Publishing An Update
- Confirm source line items tie back to filings or earnings materials.
- Check that KPI trend direction matches management commentary.
- Reconcile any large quarter-over-quarter change with a documented reason.
- Keep bull/base/bear internally consistent (no mixed-case assumptions).

## Recruiting Note
This model package is structured to demonstrate analyst workflow discipline: assumption transparency, scenario testing, and periodic update cadence.

## Data Scope Note
Workbook values are illustrative for portfolio demonstration and should be replaced with filing-sourced actuals during live investment work.
