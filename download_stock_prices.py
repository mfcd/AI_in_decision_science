"""
Download 3 years of aligned daily time series data for 50 large-cap stocks.

Note: Google Finance has no public API for scripted historical downloads
(the old Google Finance API was retired; GOOGLEFINANCE() only works inside
Google Sheets). This script uses Yahoo Finance via the `yfinance` library
instead, which provides equivalent daily OHLCV data.

Usage:
    pip install yfinance pandas
    python download_stock_data.py
"""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "AVGO", "TSLA", "BRK-B", "JPM",
    "LLY", "V", "XOM", "UNH", "MA", "COST", "HD", "PG", "JNJ", "NFLX",
    "ABBV", "BAC", "CRM", "ORCL", "WMT", "KO", "CVX", "MRK", "AMD", "PEP",
    "ADBE", "TMO", "LIN", "ACN", "MCD", "CSCO", "ABT", "WFC", "IBM", "GE",
    "DHR", "TXN", "PM", "INTU", "CAT", "VZ", "NOW", "AMGN", "ISRG", "QCOM",
]

YEARS_BACK = 3
OUTPUT_DIR = Path("stock_data")


def main() -> None:
    end_date = date.today()
    start_date = end_date - timedelta(days=365 * YEARS_BACK)

    OUTPUT_DIR.mkdir(exist_ok=True)
    per_ticker_dir = OUTPUT_DIR / "per_ticker"
    per_ticker_dir.mkdir(exist_ok=True)

    print(f"Downloading {len(TICKERS)} tickers from {start_date} to {end_date}...")

    data = yf.download(
        TICKERS,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        auto_adjust=False,
        group_by="ticker",
        threads=True,
    )

    adj_close = {}
    failed = []

    for ticker in TICKERS:
        try:
            df = data[ticker].dropna(how="all")
        except KeyError:
            failed.append(ticker)
            continue

        if df.empty:
            failed.append(ticker)
            continue

        df.index.name = "Date"
        df.to_csv(per_ticker_dir / f"{ticker}.csv")
        adj_close[ticker] = df["Adj Close"]

    if failed:
        print(f"Warning: no data returned for {len(failed)} ticker(s): {', '.join(failed)}")

    # Align all tickers on dates every one of them has data for (inner join),
    # so the combined series is a clean, gap-free matrix.
    aligned = pd.DataFrame(adj_close).dropna(how="any")
    aligned.index.name = "Date"
    aligned.to_csv(OUTPUT_DIR / "aligned_adj_close.csv")

    print(f"Saved {len(adj_close)} per-ticker CSVs to {per_ticker_dir}/")
    print(f"Saved aligned adjusted-close matrix ({aligned.shape[0]} dates x "
          f"{aligned.shape[1]} tickers) to {OUTPUT_DIR / 'aligned_adj_close.csv'}")


if __name__ == "__main__":
    main()
