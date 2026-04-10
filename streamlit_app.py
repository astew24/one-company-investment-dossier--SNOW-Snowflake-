from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import yfinance as yf


ROOT = Path(__file__).resolve().parent
TICKER = "SNOW"
REPO_URL = "https://github.com/astew24/one-company-investment-dossier--SNOW-Snowflake-"
LIVE_DEMO_URL = "https://astew24.github.io/one-company-investment-dossier--SNOW-Snowflake-"

# The repo does not currently store explicit scenario price targets.
# If you add them later, the app will prefer these values over the live fallback.
MANUAL_SCENARIO_PRICE_TARGETS: dict[str, float | None] = {
    "Bear": None,
    "Base": None,
    "Bull": None,
}


st.set_page_config(
    page_title="Snowflake (SNOW) Dossier",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
          .stApp {
            background:
              radial-gradient(circle at top left, rgba(17, 75, 95, 0.08), transparent 28rem),
              linear-gradient(180deg, #f8f3ea 0%, #f3ecdf 100%);
          }
          .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
          }
          div[data-testid="stMetric"] {
            background: rgba(255, 252, 247, 0.85);
            border: 1px solid rgba(30, 36, 48, 0.10);
            border-radius: 18px;
            padding: 0.85rem 1rem;
          }
          .section-card {
            background: rgba(255, 252, 247, 0.78);
            border: 1px solid rgba(30, 36, 48, 0.10);
            border-radius: 20px;
            padding: 1.15rem 1.2rem;
          }
          .section-card h3 {
            margin-top: 0;
            margin-bottom: 0.55rem;
          }
          .section-card p {
            margin-bottom: 0.7rem;
          }
          .section-card ul {
            margin: 0;
            padding-left: 1.2rem;
          }
          .section-kicker {
            display: inline-block;
            margin-bottom: 0.55rem;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #114b5f;
            font-weight: 700;
          }
          .thesis-card {
            background: rgba(255, 252, 247, 0.92);
            border: 1px solid rgba(30, 36, 48, 0.10);
            border-radius: 24px;
            padding: 1.4rem 1.5rem;
            margin-bottom: 1rem;
          }
          .thesis-card h1 {
            margin: 0;
            font-size: 3rem;
            line-height: 0.95;
          }
          .thesis-card p {
            font-size: 1.05rem;
            line-height: 1.65;
            margin: 0.8rem 0 0 0;
          }
          .note-card {
            background: rgba(17, 75, 95, 0.06);
            border: 1px solid rgba(17, 75, 95, 0.12);
            border-radius: 18px;
            padding: 0.9rem 1rem;
          }
          .note-card p {
            margin: 0;
            line-height: 1.55;
          }
          [data-testid="stSidebar"] .stMarkdown a {
            text-decoration: none;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def read_markdown(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


@st.cache_data
def read_sources() -> pd.DataFrame:
    return pd.read_csv(ROOT / "data/sources_log.csv")


@st.cache_data
def read_scenarios() -> pd.DataFrame:
    return pd.read_csv(ROOT / "model/scenario_assumptions.csv")


@st.cache_data
def read_kpi_history() -> pd.DataFrame:
    df = pd.read_excel(
        ROOT / "model/Model.xlsx",
        sheet_name="KPI_History",
        engine="openpyxl",
    )
    df.columns = [str(column).strip() for column in df.columns]
    return df.dropna(how="all").reset_index(drop=True)


@st.cache_data(ttl=900, show_spinner=False)
def fetch_market_snapshot(ticker: str) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "current_price": None,
        "price_as_of": None,
        "target_low": None,
        "target_mean": None,
        "target_high": None,
    }

    instrument = yf.Ticker(ticker)

    try:
        history = instrument.history(period="5d", interval="1d", auto_adjust=False)
        history = history.dropna(subset=["Close"])
        if not history.empty:
            latest = history.iloc[-1]
            snapshot["current_price"] = float(latest["Close"])
            snapshot["price_as_of"] = history.index[-1]
    except Exception:
        pass

    try:
        info = instrument.get_info()
    except Exception:
        try:
            info = instrument.info
        except Exception:
            info = {}

    if isinstance(info, dict):
        for output_key, source_key in (
            ("target_low", "targetLowPrice"),
            ("target_mean", "targetMeanPrice"),
            ("target_high", "targetHighPrice"),
        ):
            value = info.get(source_key)
            if value is not None:
                snapshot[output_key] = float(value)

    return snapshot


def split_markdown_sections(markdown_text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_heading: str | None = None
    buffer: list[str] = []

    for raw_line in markdown_text.splitlines():
        if raw_line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(buffer).strip()
            current_heading = raw_line[3:].strip()
            buffer = []
        else:
            buffer.append(raw_line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(buffer).strip()

    return sections


def get_section(markdown_text: str, heading_fragment: str) -> str:
    target = heading_fragment.lower()
    for heading, body in split_markdown_sections(markdown_text).items():
        if target in heading.lower():
            return body.strip()
    return ""


def clean_markdown(text: str) -> str:
    cleaned = text.replace("**", "").replace("`", "")
    cleaned = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -")


def extract_bullet_blocks(markdown_text: str) -> list[str]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("- "):
            if current:
                blocks.append(current)
            current = [line[2:].strip()]
        elif current and (line.startswith("  ") or line.startswith("    ")):
            current.append(line.strip())
        elif current and line.strip():
            current.append(line.strip())
        elif current and not line.strip():
            current.append("")

    if current:
        blocks.append(current)

    return [clean_markdown(" ".join(part for part in block if part)) for block in blocks]


def parse_named_bullets(markdown_text: str) -> dict[str, str]:
    items: dict[str, str] = {}
    for block in extract_bullet_blocks(markdown_text):
        if ":" not in block:
            continue
        label, value = block.split(":", 1)
        items[clean_markdown(label)] = clean_markdown(value)
    return items


def extract_first_table(markdown_text: str) -> pd.DataFrame:
    table_lines = [line.strip() for line in markdown_text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return pd.DataFrame()

    headers = [clean_markdown(cell) for cell in table_lines[0].strip("|").split("|")]
    rows: list[list[str]] = []

    for line in table_lines[2:]:
        values = [clean_markdown(cell) for cell in line.strip("|").split("|")]
        if len(values) == len(headers):
            rows.append(values)

    return pd.DataFrame(rows, columns=headers)


def build_risk_matrix(markdown_text: str) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for block in extract_bullet_blocks(markdown_text):
        risk, _, watch = block.partition("Watch:")
        rows.append(
            {
                "Risk": clean_markdown(risk),
                "What To Watch": clean_markdown(watch),
            }
        )
    return pd.DataFrame(rows)


def format_currency(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "Not available"
    return f"${value:,.2f}"


def format_percent_delta(target_value: float | None, current_price: float | None) -> str | None:
    if not target_value or not current_price:
        return None
    return f"{((target_value / current_price) - 1):+.1%} vs current"


def build_source_link(path: str) -> str:
    return f"{REPO_URL}/blob/main/{path}"


def resolve_scenario_prices(market_snapshot: dict[str, Any]) -> tuple[dict[str, float], str]:
    if all(value is not None for value in MANUAL_SCENARIO_PRICE_TARGETS.values()):
        return {
            scenario: float(value)
            for scenario, value in MANUAL_SCENARIO_PRICE_TARGETS.items()
            if value is not None
        }, "manual"

    fallback = {
        "Bear": market_snapshot.get("target_low"),
        "Base": market_snapshot.get("target_mean"),
        "Bull": market_snapshot.get("target_high"),
    }

    if all(value is not None for value in fallback.values()):
        return {scenario: float(value) for scenario, value in fallback.items() if value is not None}, "yfinance"

    return {}, "missing"


def make_html_list(items: list[str]) -> str:
    rendered_items = "".join(f"<li>{item}</li>" for item in items)
    return f"<ul>{rendered_items}</ul>"


def render_sidebar() -> None:
    st.sidebar.title("Browse")
    st.sidebar.markdown(
        """
        - Header
        - Section 1 - Long/Short Debate
        - Section 2 - Valuation
        - Section 3 - KPI History
        - Section 4 - Catalyst Map & Risk Matrix
        - Section 5 - Sources
        """
    )
    st.sidebar.divider()
    st.sidebar.markdown("### Repo Artifacts")
    st.sidebar.markdown(f"- [Investment Memo]({build_source_link('brief/Investment_Memo.md')})")
    st.sidebar.markdown(f"- [Tear Sheet]({build_source_link('brief/Tear_Sheet.md')})")
    st.sidebar.markdown(f"- [Catalyst Tracker]({build_source_link('brief/Catalyst_Tracker.md')})")
    st.sidebar.markdown(f"- [Model Notes]({build_source_link('model/README.md')})")
    st.sidebar.markdown(f"- [Sources Log]({build_source_link('data/sources_log.csv')})")
    st.sidebar.divider()
    st.sidebar.markdown(f"Live demo: [GitHub Pages]({LIVE_DEMO_URL})")
    st.sidebar.markdown(f"Repository: [GitHub]({REPO_URL})")


def render_header(
    thesis_text: str,
    market_snapshot: dict[str, Any],
    scenario_prices: dict[str, float],
    scenario_price_source: str,
) -> None:
    current_price = market_snapshot.get("current_price")
    base_target = scenario_prices.get("Base")

    if scenario_price_source == "manual":
        target_label = "Price target"
        target_help = "Base-case price target supplied in the dossier app."
    elif scenario_price_source == "yfinance":
        target_label = "Reference target"
        target_help = (
            "The repo does not store an explicit price target, so this falls back to "
            "yfinance mean analyst target data."
        )
    else:
        target_label = "Price target"
        target_help = "No explicit price target exists in the repo today."

    st.markdown(
        """
        <div class="thesis-card">
          <div class="section-kicker">Single-Name Investment Dossier</div>
          <h1>Snowflake (SNOW)</h1>
          <p>Read-only research presentation built from the repo's markdown, CSV, and workbook files.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="note-card">
          <p>{thesis_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Ticker", TICKER)
    metric_columns[1].metric("Current price", format_currency(current_price))
    metric_columns[2].metric(
        target_label,
        format_currency(base_target) if base_target is not None else "Not stated",
        delta=format_percent_delta(base_target, current_price),
    )
    metric_columns[3].metric("Horizon", "3-5 years")

    as_of = market_snapshot.get("price_as_of")
    as_of_text = as_of.strftime("%Y-%m-%d") if hasattr(as_of, "strftime") else "Unavailable"
    st.caption(f"Live price source: yfinance. Last market data point used: {as_of_text}.")
    st.caption(target_help)


def render_long_short_debate(tear_sheet_text: str) -> None:
    long_case = extract_bullet_blocks(get_section(tear_sheet_text, "Why The Thesis Works If It Works"))
    short_case = extract_bullet_blocks(get_section(tear_sheet_text, "What Could Break It"))
    scenario_framing = parse_named_bullets(get_section(tear_sheet_text, "Quick Scenario Framing"))

    st.header("Section 1 - Long/Short Debate")
    left, right = st.columns(2)

    with left:
        st.markdown(
            f"""
            <div class="section-card">
              <div class="section-kicker">Long Case</div>
              <h3>{scenario_framing.get('Bull', 'Bull case')}</h3>
              {make_html_list(long_case)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="section-card">
              <div class="section-kicker">Short Case</div>
              <h3>{scenario_framing.get('Bear', 'Bear case')}</h3>
              {make_html_list(short_case)}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_valuation(
    scenario_df: pd.DataFrame,
    current_price: float | None,
    scenario_prices: dict[str, float],
    scenario_price_source: str,
) -> None:
    st.header("Section 2 - Valuation")

    table_df = scenario_df.rename(
        columns={
            "scenario": "Scenario",
            "revenue_cagr_3yr": "3Y Revenue CAGR",
            "nrr_assumption": "NRR Assumption",
            "gross_margin_target": "Gross Margin Target",
            "cfo_margin_target": "CFO Margin Target",
            "capex_pct_revenue": "Capex % Revenue",
            "wacc": "WACC",
            "terminal_growth": "Terminal Growth",
        }
    ).copy()

    if scenario_prices:
        table_df["Scenario Price"] = table_df["Scenario"].map(scenario_prices).map(format_currency)
        if current_price:
            table_df["Vs Current"] = table_df["Scenario"].map(
                lambda scenario: format_percent_delta(scenario_prices.get(scenario), current_price) or "-"
            )

    st.dataframe(table_df, hide_index=True, use_container_width=True)

    if not scenario_prices or current_price is None:
        st.info(
            "The repo does not currently include per-scenario price outputs. "
            "Add values to MANUAL_SCENARIO_PRICE_TARGETS in streamlit_app.py to enable the comparison chart."
        )
        return

    colors = {"Bear": "#9a3d2f", "Base": "#2e7d6b", "Bull": "#1d6f42"}
    ordered = ["Bear", "Base", "Bull"]
    fig = go.Figure()
    fig.add_bar(
        x=ordered,
        y=[scenario_prices[scenario] for scenario in ordered],
        marker_color=[colors[scenario] for scenario in ordered],
        text=[format_currency(scenario_prices[scenario]) for scenario in ordered],
        textposition="outside",
        hovertemplate="%{x}: %{y:$,.2f}<extra></extra>",
    )
    fig.add_hline(
        y=current_price,
        line_dash="dash",
        line_color="#114b5f",
        annotation_text=f"Current price {format_currency(current_price)}",
        annotation_position="top left",
    )
    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.65)",
        yaxis_title="Price",
        xaxis_title="Scenario",
    )
    st.plotly_chart(fig, use_container_width=True)

    if scenario_price_source == "yfinance":
        st.caption(
            "The repo does not contain authored scenario price targets. "
            "This chart uses yfinance low / mean / high analyst targets as a reference overlay, "
            "while the scenario table itself is pulled from model/scenario_assumptions.csv."
        )


def render_kpi_history(kpi_df: pd.DataFrame) -> None:
    st.header("Section 3 - KPI History")

    chart_df = kpi_df[["quarter", "revenue", "fcf", "nrr_%"]].copy()
    chart_df["is_estimate"] = chart_df["quarter"].astype(str).str.contains("E", regex=False)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=chart_df["quarter"],
            y=chart_df["revenue"],
            name="Revenue ($m)",
            mode="lines+markers",
            line=dict(color="#114b5f", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=chart_df["quarter"],
            y=chart_df["fcf"],
            name="FCF ($m)",
            mode="lines+markers",
            line=dict(color="#ab7a16", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=chart_df["quarter"],
            y=chart_df["nrr_%"],
            name="NRR (%)",
            mode="lines+markers",
            line=dict(color="#7a3342", width=3),
        ),
        secondary_y=True,
    )

    estimate_rows = chart_df.index[chart_df["is_estimate"]].tolist()
    if estimate_rows:
        first_estimate = chart_df.iloc[estimate_rows[0]]["quarter"]
        last_estimate = chart_df.iloc[estimate_rows[-1]]["quarter"]
        fig.add_vrect(
            x0=first_estimate,
            x1=last_estimate,
            fillcolor="rgba(17, 75, 95, 0.06)",
            line_width=0,
            annotation_text="Estimated quarters",
            annotation_position="top left",
        )

    fig.update_layout(
        height=470,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.65)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_yaxes(title_text="Revenue / FCF ($m)", secondary_y=False)
    fig.update_yaxes(title_text="NRR (%)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: model/Model.xlsx, sheet KPI_History.")


def render_catalysts_and_risks(catalyst_text: str, memo_text: str) -> None:
    st.header("Section 4 - Catalyst Map & Risk Matrix")

    catalyst_df = extract_first_table(get_section(catalyst_text, "Event Calendar"))
    risk_df = build_risk_matrix(get_section(memo_text, "Risk Matrix"))

    left, right = st.columns((1.55, 1.0))
    with left:
        st.subheader("Catalyst map")
        st.dataframe(catalyst_df, hide_index=True, use_container_width=True)

    with right:
        st.subheader("Risk matrix")
        st.dataframe(risk_df, hide_index=True, use_container_width=True)


def render_sources(sources_df: pd.DataFrame) -> None:
    st.header("Section 5 - Sources")

    display_df = sources_df.rename(
        columns={
            "date_found": "Date Found",
            "source_title": "Source",
            "doc_type": "Document Type",
            "metric_captured": "Metric / Topic",
            "time_period": "Time Period",
            "exact_ref": "Exact Reference",
            "url": "URL",
            "your_note": "Note",
        }
    )[
        [
            "Date Found",
            "Source",
            "Document Type",
            "Metric / Topic",
            "Time Period",
            "Exact Reference",
            "URL",
            "Note",
        ]
    ]

    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "URL": st.column_config.LinkColumn("Source URL"),
        },
    )
    st.caption(f"{len(display_df)} primary sources logged in data/sources_log.csv.")


def main() -> None:
    inject_styles()
    render_sidebar()

    investment_memo = read_markdown("brief/Investment_Memo.md")
    tear_sheet = read_markdown("brief/Tear_Sheet.md")
    catalyst_tracker = read_markdown("brief/Catalyst_Tracker.md")

    thesis_text = clean_markdown(get_section(investment_memo, "Core Thesis"))
    market_snapshot = fetch_market_snapshot(TICKER)
    scenario_df = read_scenarios()
    scenario_prices, scenario_price_source = resolve_scenario_prices(market_snapshot)
    kpi_history = read_kpi_history()
    sources_df = read_sources()

    render_header(thesis_text, market_snapshot, scenario_prices, scenario_price_source)
    st.divider()
    render_long_short_debate(tear_sheet)
    st.divider()
    render_valuation(scenario_df, market_snapshot.get("current_price"), scenario_prices, scenario_price_source)
    st.divider()
    render_kpi_history(kpi_history)
    st.divider()
    render_catalysts_and_risks(catalyst_tracker, investment_memo)
    st.divider()
    render_sources(sources_df)


if __name__ == "__main__":
    main()
