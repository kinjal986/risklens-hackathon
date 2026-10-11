
import pandas as pd
import plotly.express as px
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from data_cleaning import clean_news_dataframe
from news_sources import fetch_all_news

st.set_page_config(
    page_title="RiskLens | Financial Event Risk",
    page_icon="📊",
    layout="wide",
)

st.title("RiskLens")
st.caption(
    "Evidence-backed financial event analysis and portfolio stress testing"
)

analyzer = SentimentIntensityAnalyzer()

SAMPLE_NEWS = [
    {
        "title": "Major steel producer faces prolonged supply disruption",
        "text": "Geopolitical tensions disrupt raw material shipments, "
                "raising costs and delaying production.",
        "source": "Demo dataset A",
        "published_at": "2026-10-11T08:00:00Z",
    },
    {
        "title": "Central bank signals a possible interest rate increase",
        "text": "Borrowing costs may rise as policymakers respond to inflation.",
        "source": "Demo dataset B",
        "published_at": "2026-10-11T08:30:00Z",
    },
    {
        "title": "Technology company reports stronger quarterly earnings",
        "text": "Revenue growth and improved margins lift investor expectations.",
        "source": "Demo dataset A",
        "published_at": "2026-10-11T09:00:00Z",
    },
    {
        "title": "Large borrower faces credit downgrade concerns",
        "text": "Analysts warn that weakening cash flow may increase default risk.",
        "source": "Demo dataset B",
        "published_at": "2026-10-11T09:30:00Z",
    },
]



def classify_event(text):
    text = str(text).lower()

    # Check specific financial events before broader contextual keywords.
    rules = {
        "Credit Event": [
            "credit downgrade", "downgrade", "default",
            "borrower", "debt", "cash flow", "credit risk",
            "bankruptcy", "loan impairment"
        ],
        "Supply Chain": [
            "supply chain", "supply disruption", "shipment",
            "raw material", "shortage", "production disruption"
        ],
        "Energy / Commodity": [
            "fuel prices", "oil prices", "crude oil",
            "energy supply", "oil supply", "gas prices",
            "energy prices", "oil production"
        ],
        "Corporate Earnings": [
            "earnings", "revenue", "profit", "quarterly",
            "margins", "profit warning"
        ],
        "M&A": [
            "acquisition", "merger", "takeover"
        ],
        "Macroeconomic": [
            "inflation", "interest rate", "central bank",
            "gdp", "recession", "monetary policy"
        ],
        "Geopolitical": [
            "geopolitical", "war", "sanction",
            "conflict", "border"
        ],
    }

    for label, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return label

    return "Other"



def impact_score(text, event_type):
    """Transparent heuristic; not a trained or calibrated risk model."""
    text = text.lower()
    score = 3

    high_impact_terms = [
        "default", "bankruptcy", "war", "sanction",
        "systemic", "prolonged", "collapse", "crisis"
    ]
    medium_impact_terms = [
        "disruption", "downgrade", "inflation",
        "interest rate", "shortage", "recession"
    ]

    score += sum(2 for term in high_impact_terms if term in text)
    score += sum(1 for term in medium_impact_terms if term in text)

    if event_type in ["Geopolitical", "Credit Event"]:
        score += 1

    return max(1, min(10, score))


def analyse_news(df):
    results = []

    for _, row in df.iterrows():
        text = row["analysis_text"]
        sentiment = analyzer.polarity_scores(text)["compound"]
        event = classify_event(text)
        impact = impact_score(text, event)

        results.append({
            "title": row["title"],
            "source": row["source"] or "Unknown",
            "published_at": row["published_at"],
            "sentiment": sentiment,
            "event_type": event,
            "impact": impact,
            "analysis_text": text,
            "url": row.get("url", ""),
            "ingestion_source": row.get("ingestion_source", ""),
        })

    return pd.DataFrame(results)


st.sidebar.header("RiskLens Controls")
st.sidebar.write("Choose your news data source.")

news_mode = st.sidebar.radio(
    "News source",
    [
        "Sample demo data",
        "Fetch live news",
        "Upload CSV",
    ],
)
uploaded_file = None

if news_mode == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader(
        "Upload a CSV news dataset",
        type=["csv"],
    )

if news_mode == "Upload CSV" and uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    news_df, cleaning_report = clean_news_dataframe(raw_df)
    data_origin = "Uploaded CSV"


elif news_mode == "Fetch live news":
    with st.spinner("Fetching articles from GDELT and RSS feeds..."):
        raw_df = fetch_all_news()

    if raw_df.empty:
        st.warning(
            "No live articles were retrieved. This may be due to "
            "network access or feed availability. Using sample data instead."
        )
        raw_df = pd.DataFrame(SAMPLE_NEWS)
        data_origin = (
            "Illustrative demo fallback "
            "(live fetch returned no articles)"
        )
    else:
        data_origin = "Live GDELT and RSS feeds"

    news_df, cleaning_report = clean_news_dataframe(raw_df)


if news_mode == "Sample demo data" or (
    news_mode == "Upload CSV" and uploaded_file is None
):
    raw_df = pd.DataFrame(SAMPLE_NEWS)
    news_df, cleaning_report = clean_news_dataframe(raw_df)

    if news_mode == "Sample demo data":
        data_origin = "Built-in illustrative demo data"

results = analyse_news(news_df)


st.info(
    f"Data source: {data_origin}. "
    "Sample headlines are illustrative, not live news."
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Articles retained", len(results))
c2.metric(
    "Negative sentiment",
    int((results["sentiment"] < -0.05).sum()) if len(results) else 0,
)
c3.metric(
    "High-impact events (7+)",
    int((results["impact"] >= 7).sum()) if len(results) else 0,
)
c4.metric(
    "Average impact",
    f"{results['impact'].mean():.1f}/10" if len(results) else "N/A",
)

st.subheader("1. News risk signals")

if not results.empty:
    display_df = results[
        ["title", "source", "event_type", "sentiment", "impact", "url", "ingestion_source" ]    ].copy()
    display_df["sentiment"] = display_df["sentiment"].round(3)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    selected_index = st.selectbox(
        "Inspect an event",
        options=list(results.index),
        format_func=lambda i: results.loc[i, "title"],
    )
    selected = results.loc[selected_index]

    with st.expander("Evidence and scoring explanation", expanded=True):
        st.write("**Article text:**", selected["analysis_text"])
        st.write("**Source label:**", selected["source"])
        if selected.get("url"):
            st.markdown(f"[Open original article]({selected['url']})")
        if selected.get("ingestion_source"):
            st.write("**Ingestion method:**", selected["ingestion_source"])
        st.write("**Event class:**", selected["event_type"])
        st.write(
            f"**VADER sentiment:** {selected['sentiment']:.3f} "
            "(lexicon-based baseline)"
        )
        st.write(
            f"**Impact score:** {selected['impact']}/10 "
            "(transparent keyword heuristic, not a calibrated prediction)"
        )

    st.subheader("2. Sentiment and event impact")
    chart_df = results.copy()
    chart_df["impact_label"] = chart_df["impact"].astype(str) + "/10"
    fig = px.scatter(
        chart_df,
        x="sentiment",
        y="impact",
        color="event_type",
        hover_name="title",
        size="impact",
        range_x=[-1, 1],
        range_y=[0, 10],
        title="News sentiment versus heuristic impact",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3. Synthetic banking portfolio stress test")
    st.markdown("#### Event-driven scenario selection")

    scenario_shocks = {
        "Geopolitical": [8.0, 2.0, 10.0, 5.0],
        "Macroeconomic": [6.0, 5.0, 8.0, 5.0],
        "Credit Event": [12.0, 1.0, 9.0, 7.0],
        "Corporate Earnings": [3.0, 1.0, 5.0, 2.0],
        "Supply Chain": [9.0, 2.0, 7.0, 10.0],
        "M&A": [4.0, 1.0, 6.0, 3.0],
        "Other": [5.0, 2.0, 5.0, 3.0],
    }

    
    event_options = list(scenario_shocks.keys())

    # Find the highest-impact article.
    high_impact_results = results[results["impact"] > 7]
        
    st.write(
        f"**High-impact articles detected:** "
        f"{len(high_impact_results)}"
    )

    if not high_impact_results.empty:
        st.dataframe(
            high_impact_results[
                ["title", "event_type", "impact", "sentiment"]
            ].sort_values(
                "impact", ascending=False
            ),
            use_container_width=True,
            hide_index=True,
        )


    if not high_impact_results.empty:
        trigger_row = high_impact_results.loc[
            high_impact_results["impact"].idxmax()
        ]

        detected_event = trigger_row["event_type"]
        auto_event = (
            detected_event
            if detected_event in scenario_shocks
            else "Other"
        )

        st.warning(
            f"Automatic stress-test trigger: "
            f"'{trigger_row['title']}' | "
            f"Impact: {trigger_row['impact']}/10 | "
            f"Event: {auto_event}"
        )
        st.write(
            "The highest-impact article above 7 determines "
            "the automatically selected stress scenario."
        )
    else:
        auto_event = "Other"
        st.info(
            "No article has an impact score above 7. "
            "The automatic high-impact trigger has not fired. "
            "The portfolio below uses the 'Other' scenario "
            "for illustrative comparison."
        )


# Manual scenario selection is optional.

    
    manual_override = st.checkbox(
        "Manually override the automatic scenario for comparison",
        value=False,
    )

    if manual_override:
        selected_scenario = st.selectbox(
            "Choose a comparison scenario",
            event_options,
            index=event_options.index(auto_event),
            key="manual_scenario_override",
        )
    else:
        selected_scenario = auto_event

    st.write(f"**Scenario applied:** {selected_scenario}")

    st.caption(
        "Illustrative assumptions for demonstration only; "
        "these shocks are not calibrated market predictions."
    )
    st.caption(
        "Portfolio losses are simulated from user-adjustable assumptions, "
        "not measured market responses or forecasts."
    )

    
    portfolio = pd.DataFrame([
        {
            "asset": "Corporate loans",
            "exposure_cr": 30.0,
            "shock_pct": scenario_shocks[selected_scenario][0],
        },
        {
            "asset": "Government bonds",
            "exposure_cr": 20.0,
            "shock_pct": scenario_shocks[selected_scenario][1],
        },
        {
            "asset": "Banking equities",
            "exposure_cr": 15.0,
            "shock_pct": scenario_shocks[selected_scenario][2],
        },
        {
            "asset": "Infrastructure loans",
            "exposure_cr": 20.0,
            "shock_pct": scenario_shocks[selected_scenario][3],
        },
        {
            "asset": "Derivatives exposure (synthetic)",
            "exposure_cr": 15.0,
            "shock_pct": scenario_shocks[selected_scenario][4],
        },
    ])

    st.write("Adjust scenario shocks to test different assumptions.")

    edited_portfolio = st.data_editor(
        portfolio,
        use_container_width=True,
        hide_index=True,
        disabled=["asset", "exposure_cr"],
        column_config={
            "shock_pct": st.column_config.NumberColumn(
                "Scenario shock (%)",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
            )
        },
        key="portfolio_editor",
    )

    before_value = float(edited_portfolio["exposure_cr"].sum())

    edited_portfolio["loss_cr"] = (
        edited_portfolio["exposure_cr"]
        * edited_portfolio["shock_pct"] / 100
    )

    edited_portfolio["after_value_cr"] = (
        edited_portfolio["exposure_cr"]
        - edited_portfolio["loss_cr"]
    )

    total_loss = float(edited_portfolio["loss_cr"].sum())
    after_value = before_value - total_loss

    p1, p2, p3 = st.columns(3)
    p1.metric("Starting portfolio", f"₹{before_value:.2f} crore")
    p2.metric("Scenario loss", f"₹{total_loss:.2f} crore")
    p3.metric("After stress", f"₹{after_value:.2f} crore")

    loss_fig = px.bar(
        edited_portfolio,
        x="asset",
        y="loss_cr",
        title="Scenario loss attribution by asset",
        labels={
            "asset": "Portfolio asset",
            "loss_cr": "Loss (₹ crore)",
        },
    )
    st.plotly_chart(loss_fig, use_container_width=True)

    st.dataframe(
        edited_portfolio,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download risk signals and evidence as CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="risklens_risk_signals.csv",
        mime="text/csv",
    )

with st.expander("Dataset cleaning report"):
    for key, value in cleaning_report.items():
        st.write(f"**{key.replace('_', ' ').title()}:** {value}")

st.divider()

st.caption(
    "RiskLens prototype | Research and educational demonstration; "
    "not investment advice or a production credit-risk model."
)






