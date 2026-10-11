
import re
import hashlib
import pandas as pd


REQUIRED_COLUMNS = ["title", "text", "source", "published_at"]


def normalize_text(value):
    """Normalize whitespace and remove basic HTML tags."""
    if pd.isna(value):
        return ""

    value = str(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean_news_dataframe(df):
    """Validate, normalize, deduplicate and report news records."""
    original_count = len(df)

    # Support common alternative column names.
    aliases = {
        "headline": "title",
        "description": "text",
        "content": "text",
        "published": "published_at",
        "date": "published_at",
        "url_source": "source",
    }

    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    # Preserve evidence and ingestion provenance when available.
    for col in ["url", "ingestion_source"]:
        if col not in df.columns:
            df[col] = ""


    df["title"] = df["title"].map(normalize_text)
    df["text"] = df["text"].map(normalize_text)
    df["source"] = df["source"].map(normalize_text)

    # If article text is missing, the headline can still be analysed.
    df["analysis_text"] = (
        df["title"] + ". " + df["text"]
    ).str.strip(" .")

    df["published_at"] = pd.to_datetime(
        df["published_at"], errors="coerce", utc=True
    )

    missing_text = int(df["analysis_text"].eq("").sum())
    df = df[df["analysis_text"].ne("")].copy()

    # Remove exact duplicate analysis text.
    df["dedup_key"] = df["analysis_text"].str.lower().str.strip()
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["dedup_key"]).copy()
    duplicates_removed = before_dedup - len(df)

    df = df.drop(columns=["dedup_key"])

    report = {
        "input_rows": original_count,
        "empty_records_removed": missing_text,
        "duplicates_removed": duplicates_removed,
        "retained_rows": len(df),
        "invalid_dates": int(df["published_at"].isna().sum()),
    }

    return df.reset_index(drop=True), report
