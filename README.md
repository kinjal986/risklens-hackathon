# RiskLens — S&P Global & CRISIL Campus Hackathon

**Project:** News-Driven Risk Intelligence and Event-Triggered Portfolio Stress Testing  
**Candidate Name:** Kinjal Gupta  
**College / Campus:** VIT Bhopal  
**College Email ID:** kinjal.23mip10052@vitbhopal.ac.in 
**Demo Video Link:** To be added  
**Presentation:** `docs/presentation.pdf`

## 1. Project Overview / Problem Statement & Approach

Financial risks can emerge from breaking news, economic developments, geopolitical events, and corporate announcements. Manually reviewing unstructured news and assessing its potential portfolio impact can be slow and inconsistent.

RiskLens is a prototype that collects news from public news feeds and GDELT, cleans and deduplicates articles, analyzes sentiment, classifies potential risk events, and assigns a heuristic impact score from 1 to 10. It presents the results in an interactive dashboard with links to the source articles.

The downstream portfolio module applies simplified, event-specific percentage shocks to a portfolio and visualizes estimated losses and post-stress value. The prototype is intended for research and demonstration, not as a production risk model or investment recommendation.

## 2. Architecture & Tech Stack

**Data flow:** Public news sources → ingestion → cleaning and deduplication → sentiment and event analysis → risk dashboard → event-triggered portfolio stress test.

**Technology:** Python, Streamlit, pandas, Plotly, feedparser, requests, VADER Sentiment and scikit-learn (listed dependency; describe its actual use only if applicable).

See `docs/architecture.png` for the architecture diagram.

## 3. Dataset Used

News data is retrieved from public RSS feeds and GDELT. The application also supports sample news records for demonstration. The portfolio exposures and scenario shocks must be documented according to the actual dataset included with the final submission.

All sample or synthetic data must be identified clearly. No confidential client data is used.

## 4. Quickstart & Installation

**Runtime:** Python 3.11 or another compatible Python version; tested on Windows.

```bash
git clone https://github.com/kinjal986/risklens-hackathon.git
cd risklens-hackathon
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and run the application:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## 5. Key Results & Domain Impact

RiskLens demonstrates news ingestion, article-level sentiment and event classification, heuristic impact scoring, traceable source links, and a simplified portfolio stress test with before-and-after values and asset-level loss attribution.

The dashboard is designed to help users connect unstructured news signals to a structured, explainable risk-review workflow.

## 6. Limitations & Next Steps

- Event classification is keyword-based and impact scoring is heuristic.
- Portfolio shocks are illustrative assumptions, not calibrated loss forecasts.
- Portfolio data and assumptions must be validated against the dataset included in the final submission.
- Future work includes validated transaction-level exposure aggregation, improved event classification, and calibrated stress scenarios.

## Disclaimer

RiskLens is an educational prototype. Its outputs are not investment advice or production-grade financial risk estimates.
