![AI in Decision Science — Mattia Ferrini, Entropy42, ETH, September 19, 2026](pres_screen_opener.png)

# Portfolio Optimizer

Demo code accompanying the "AI in Decision Science" talk at ETH: a simple
Markowitz mean-variance portfolio optimization example.

## Contents

- [portfolio_optimization.ipynb](portfolio_optimization.ipynb) — loads historical
  adjusted close prices, solves a minimum-variance allocation with Pyomo/HiGHS
  for a target return, and plots the resulting allocation by stock and by sector.
- [download_stock_prices.py](download_stock_prices.py) — downloads historical
  price data into `stock_data/`.
- [fetch_metadata.py](fetch_metadata.py) — fetches ticker metadata (e.g. sector)
  into `stock_data/metadata.csv`.
- [app/](app/) — small FastAPI example.
- [various_utils/](various_utils/) — misc supporting scripts.

## Setup

```bash
poetry install
```

`stock_data/` is not checked in; regenerate it with:

```bash
python download_stock_prices.py
python fetch_metadata.py
```

Then open [portfolio_optimization.ipynb](portfolio_optimization.ipynb) and run
the cells.
