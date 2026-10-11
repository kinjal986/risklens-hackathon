import requests
import feedparser
import pandas as pd
from datetime import datetime, timezone
from urllib.parse import quote


def fetch_gdelt_news(query="financial markets OR economy OR credit risk", limit=15):
    """Fetch recent news articles from the GDELT DOC API."""
    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": limit,
        "sort": "DateDesc",
    }

    rows = []

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        for article in data.get("articles", []):
            rows.append({
                "title": article.get("title", ""),
                "text": article.get("title", ""),
                "source": article.get("domain", "GDELT"),
                "published_at": article.get("seendate", ""),
                "url": article.get("url", ""),
                "ingestion_source": "GDELT",
            })

    except Exception as exc:
        print(f"GDELT fetch failed: {exc}")

    return rows


def fetch_rss_news(limit=15):
    """Fetch articles from public RSS news feeds."""
    feeds = [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.theguardian.com/business/rss",
    ]

    rows = []

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:limit]:
                published = (
                    entry.get("published", "")
                    or entry.get("updated", "")
                )

                rows.append({
                    "title": entry.get("title", ""),
                    "text": entry.get("summary", "")
                    or entry.get("description", "")
                    or entry.get("title", ""),
                    "source": feed.feed.get("title", feed_url),
                    "published_at": published,
                    "url": entry.get("link", ""),
                    "ingestion_source": "RSS",
                })

        except Exception as exc:
            print(f"RSS fetch failed for {feed_url}: {exc}")

    return rows


def fetch_all_news():
    """Combine available news from both ingestion methods."""
    articles = fetch_gdelt_news() + fetch_rss_news()

    if not articles:
        return pd.DataFrame(
            columns=[
                "title", "text", "source", "published_at",
                "url", "ingestion_source",
            ]
        )

    df = pd.DataFrame(articles)

    # Remove blank headlines and exact duplicate URLs.
    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df = df[df["title"] != ""]
    df = df.drop_duplicates(subset=["url"], keep="first")

    return df.reset_index(drop=True)
