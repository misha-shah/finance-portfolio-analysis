# Equal-Weight Portfolio vs. S&P 500 — Backtest Analysis

A Python backtest comparing a simple equal-weighted 5-stock portfolio against
the S&P 500 over the past 3 years, using real historical market data.

## What it does

1. Pulls 3 years of daily closing prices for 5 stocks spanning different
   sectors (AAPL – tech, MSFT – tech, JNJ – healthcare, JPM – financials,
   XOM – energy) plus the S&P 500 index, via the `yfinance` library
2. Converts prices into daily returns, then builds an **equal-weighted
   portfolio** (each stock counted equally, rebalanced daily — a
   simplifying assumption; see note below)
3. Computes "growth of $1 invested" for both the portfolio and the S&P 500
   so they're directly comparable in dollar terms
4. Calculates standard performance metrics: **annualized return**,
   **annualized volatility**, **Sharpe ratio**, and **maximum drawdown**
5. Plots both growth curves on one chart

## Results (as of this run)

| Metric                  | Portfolio | S&P 500 |
|--------------------------|-----------|---------|
| Annualized return         | 26.28%    | 22.04%  |
| Annualized volatility     | 13.17%    | 15.01%  |
| Sharpe ratio               | 1.69      | 1.20    |
| Max drawdown               | -16.01%   | -18.90% |

The portfolio outperformed the benchmark on every metric here — higher
return, *lower* risk (volatility and drawdown), and a better risk-adjusted
return (Sharpe ratio). Worth noting from the chart: the S&P 500 was
actually ahead for roughly the first two years; the portfolio only pulled
decisively ahead in the final stretch. These numbers will change whenever
the script is re-run, since it's always pulling the latest 3 years of data.

## Project structure

```
finance-portfolio-analysis/
├── fetch_data.py          # main script — run this
├── output/
│   └── portfolio_vs_sp500.png
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone <your-repo-url>
cd finance-portfolio-analysis
pip install -r requirements.txt
```

## Run it

```bash
python3 fetch_data.py
```

Requires an internet connection (it pulls live data from Yahoo Finance via
`yfinance` every time it runs).

## ⚠️ Important caveats — this is a backtest, not a prediction

- This is a **backtest**: it shows how this specific portfolio *would have*
  performed historically. It says nothing about future performance.
- **Equal-weight, daily-rebalanced is a simplifying assumption.** Real
  portfolios don't typically rebalance back to equal weights every single
  day (that would rack up significant transaction costs); this model
  ignores trading costs and taxes entirely.
- **5 stocks is a small, concentrated sample** chosen for sector spread,
  not through any optimization or screening process — this isn't a claim
  that this specific combination is "the best" portfolio.
- The risk-free rate used in the Sharpe ratio calculation (4%) is a fixed
  assumption, not pulled from live Treasury data.

## Definitions (for anyone reading this who wants the plain-English version)

- **Annualized return**: the average yearly growth rate, compounded —
  answers "if this rate held steady every year, what would the yearly
  return be?"
- **Annualized volatility**: how much returns bounce around day to day,
  scaled to a yearly measure. Higher = more unpredictable, not necessarily
  worse.
- **Sharpe ratio**: return earned per unit of risk taken. Higher is
  generally better — it means more reward for the same bumpiness.
- **Max drawdown**: the worst peak-to-trough loss an investor would have
  experienced at any point — a "how bad could it have gotten" number that
  average returns alone don't capture.

## Possible extensions

- Add more stocks, or test different weighting schemes (market-cap
  weighted instead of equal weighted)
- Add a rolling/rebalanced-monthly version instead of daily rebalancing,
  to compare how much the assumption actually matters
- Backtest across a market downturn specifically (e.g. 2022) instead of
  a mostly-upward period, to see how the portfolio holds up in a bad year
