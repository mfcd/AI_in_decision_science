"""
Fetch company metadata (sector, industry, market cap, etc.) for the same
50 tickers used in download_stock_prices.py.

Usage:
    pip install yfinance pandas
    python fetch_metadata.py
"""

from pathlib import Path

import pandas as pd
import yfinance as yf

from download_stock_prices import TICKERS

OUTPUT_DIR = Path("stock_data")

FIELDS = [
    "shortName",
    "sector",
    "industry",
    "country",
    "exchange",
    "currency",
    "marketCap",
    "fullTimeEmployees",
    "trailingPE",
    "forwardPE",
    "dividendYield",
    "beta",
    "fiftyTwoWeekHigh",
    "fiftyTwoWeekLow",
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Fetching metadata for {len(TICKERS)} tickers...")

    rows = []
    failed = []

    for ticker in TICKERS:
        try:
            info = yf.Ticker(ticker).info
        except Exception:
            failed.append(ticker)
            continue

        if not info or info.get("sector") is None:
            failed.append(ticker)

        row = {"ticker": ticker}
        row.update({field: info.get(field) for field in FIELDS})
        rows.append(row)

    if failed:
        print(f"Warning: incomplete/missing metadata for {len(failed)} ticker(s): {', '.join(failed)}")

    df = pd.DataFrame(rows).set_index("ticker")
    df.to_csv(OUTPUT_DIR / "metadata.csv")

    print(f"Saved metadata for {len(df)} tickers to {OUTPUT_DIR / 'metadata.csv'}")


if __name__ == "__main__":
    main()
