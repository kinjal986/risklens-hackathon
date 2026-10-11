# RiskLens — News-Driven Risk Intelligence & Event-Triggered Portfolio Stress Testing

S&P Global & CRISIL Campus Hackathon 2026

- Candidate: Kinjal Gupta
- College: VIT Bhopal
- College email: kinjal.23mip10052@vitbhopal.ac.in
- Demo video: [To be added after recording](https://youtu.be/-1J-GBqnc8E)
- Presentation: [`docs/presentation.pdf`](docs/presentation.pdf)
- Architecture diagram: [`docs/architecture.png`](docs/architecture.png)

1. Project Overview

Financial risk signals can emerge from geopolitical developments, economic announcements, corporate news and other public information. Reviewing fragmented news sources and exploring their possible implications for portfolio exposures can be time-consuming.

RiskLens is a research prototype that combines public news ingestion, sentiment analysis, event categorisation and an interactive risk dashboard. It also provides a scenario-based portfolio stress test using a synthetic portfolio and user-selectable illustrative asset shocks.

The objective is to make the process from a news headline to risk indicators and hypothetical portfolio scenarios easier to inspect.

2. Architecture and Technology Stack

News intelligence pipeline

Public news sources (GDELT DOC API and RSS feeds) → data cleaning and deduplication → VADER sentiment analysis, keyword-based event categorisation and heuristic impact scoring → Streamlit and Plotly dashboard.

Market-data reference

Yahoo Finance through `yfinance` → NIFTY 50 historical closing prices and daily returns.

This is a separate market-data reference component. NIFTY 50 returns do not calibrate the portfolio scenario shocks in the current implementation.

Portfolio stress test

Synthetic ₹100 crore portfolio + selected scenario + illustrative asset shocks → simulated portfolio impact and loss attribution by asset.

Technology

- Python
- Streamlit
- Pandas
- Plotly
- VADER Sentiment
- `feedparser`
- Requests
- `yfinance`

See the [standalone architecture diagram](docs/architecture.png).

3. Datasets and Data Sources

Public data

- News: Public news metadata collected from GDELT and RSS feeds. Source URLs and available article metadata are retained where provided.
- Market reference: NIFTY 50 historical market data retrieved through Yahoo Finance using `yfinance`.
- Historical snapshot: `data/nifty50_historical.csv`, if present in the repository, contains a saved market-data snapshot.

Synthetic data

- `data/synthetic_portfolio.csv` contains illustrative portfolio exposure assumptions, if present in the repository.
- The portfolio represents ₹100 crore distributed across five asset categories.
- Scenario shocks and heuristic impact scores are assumptions for demonstration, not measured market responses.

No confidential client portfolio data is intended to be used.

4. Quickstart and Installation

Prerequisites

- Python 3.11 or a compatible Python version
- Internet connection for live news and market-data retrieval

Clone the repository

bash
git clone https://github.com/kinjal986/risklens-hackathon.git
cd risklens-hackathon


Create a virtual environment

Windows PowerShell:

powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1


Install dependencies

bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt


 Run the application

bash
python -m streamlit run app.py


Open the local URL printed in the terminal, normally `http://localhost:8501`.

Live data retrieval depends on external services being available and reachable.

5. Features and Demonstration

RiskLens demonstrates:

1. Collection of public news from GDELT and RSS sources.
2. Cleaning and deduplication of news records.
3. Article sentiment analysis using VADER.
4. Keyword-based event categorisation and heuristic impact scoring.
5. Interactive news and risk visualisations using Streamlit and Plotly.
6. NIFTY 50 historical price and daily-return charts.
7. Scenario-based stress testing of a synthetic portfolio.
8. Visualisation of simulated losses by asset category.

Demo video: To be added after the recording is uploaded.

 6. Results and Potential Impact

RiskLens brings news analysis, a market-data reference and hypothetical portfolio stress testing into one inspectable workflow.

It allows users to explore news indicators and see how different illustrative shocks affect different asset categories. The prototype demonstrates a possible approach to organising risk-related information; it does not establish that a particular headline predicts a specific market movement or portfolio loss.

7. Limitations and Future Work

Current limitations

- Event categories are assigned using keyword-based rules.
- Sentiment is calculated using VADER.
- Impact scores are heuristic indicators, not validated risk predictions.
- Portfolio shocks are illustrative assumptions, not calibrated loss forecasts.
- No validated causal relationship between news events and market movements has been established.
- Live data availability depends on external news and market-data services.

Future work

- Validate event classification against manually labelled news.
- Evaluate indicators against documented historical market events.
- Calibrate scenario shocks using a transparent, documented methodology.
- Add automated tests and systematic error handling.
- Improve portfolio modelling with validated exposure and risk data.

8. Deliverables

- [Presentation PDF](docs/presentation.pdf)
- [Architecture diagram](docs/architecture.png)
- Demo video: add the public-accessible YouTube Unlisted URL after recording.

 Disclaimer

RiskLens is an educational and research prototype. Sentiment scores, event categories and impact indicators are heuristic. Portfolio losses are simulated under illustrative assumptions and are not forecasts, measured losses, investment advice or production-grade financial risk estimates.
