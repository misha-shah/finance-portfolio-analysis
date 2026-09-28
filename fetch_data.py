"""
fetch_data.py

Step 1: just fetch and look at real stock price data. Nothing fancy yet --
the goal here is to see what yfinance actually gives you back.
"""

import yfinance as yf

# 5 diversified stocks
TICKERS = ["AAPL", "MSFT", "JNJ", "JPM", "XOM"]
BENCHMARK = "^GSPC"  # this is the actual ticker symbol for the S&P 500 index

# 3 years of daily price history for everything
all_symbols = TICKERS + [BENCHMARK]
data = yf.download(all_symbols, period="3y")

# just the close prices, cuts out other data; printed out data
close_prices = data["Close"]

print("Shape of the data (rows, columns):", close_prices.shape)
print()
print("First 5 rows:")
print(close_prices.head())
print()
print("Last 5 rows:")
print(close_prices.tail())

import pandas as pd

#pct_change() calculates percent change

returns = close_prices.pct_change().dropna()

print("Daily returns (first 5 rows):")
print(returns.head())
print()

portfolio_returns = returns[TICKERS].mean(axis=1)

#when things get sold the portfolio will return to an equal distribution of each stock
portfolio_growth =  (1+portfolio_returns).cumprod()
benchmark_growth = (1+returns[BENCHMARK]).cumprod()

#what would one dollar invested in our simulated portfolio be versus the s&p500 index over the last 5 days?
print('growth of $1 invested -- portfolio vs. s&p500 (last 5 days):')
comparison = pd.DataFrame({'Portfolio':portfolio_growth,'s&p500':benchmark_growth})
print(comparison.tail())

import numpy as np

def annualized_return(daily_returns):
    #makes the daily return yearly
    #252 trading days in a year

    total_growth=(1+daily_returns).prod()
    n_years = len(daily_returns)/252
    return total_growth ** (1/n_years)-1
    #this is the formula for annualized return, which is the geometric mean of the returns over a year
    #n_years is the number of years in the data, which is the number of daily returns divided by 252

def annualized_volatility(daily_returns):
    #determines how much the stocks bounce around (higher means more uncertainty)
    #standard deviation (stats stuff)
    return daily_returns.std() * np.sqrt(252)

def sharpe_ratio(daily_returns, risk_free_rate=0.04):
    #sharpe ratio is the reutrn you get for the amount of risk you take
    #higher is better because it means you got more return for the same amount of risk
    #subtract a risk-free rate (like savings accounts) since returns are above that, those are the actual rewards for taking a risk
    ann_ret = annualized_return(daily_returns)
    ann_vol = annualized_volatility(daily_returns)
    return (ann_ret - risk_free_rate) / ann_vol

def max_drawdown(daily_returns):
    #the worst it could've gone, the largest drop from peak to trough
    growth = (1+daily_returns).cumprod()
    running_max = growth.cummax()
    drawdown = (growth - running_max) / running_max
    return drawdown.min()

print("Performance summary:")
print(f"{'Metric':<25}{'Portfolio':<15}{'S&P 500'}")
print(f"{'Annualized return':<25}{annualized_return(portfolio_returns):<15.2%}{annualized_return(returns[BENCHMARK]):.2%}")
print(f"{'Annualized volatility':<25}{annualized_volatility(portfolio_returns):<15.2%}{annualized_volatility(returns[BENCHMARK]):.2%}")
print(f"{'Sharpe ratio':<25}{sharpe_ratio(portfolio_returns):<15.2f}{sharpe_ratio(returns[BENCHMARK]):.2f}")
print(f"{'Max drawdown':<25}{max_drawdown(portfolio_returns):<15.2%}{max_drawdown(returns[BENCHMARK]):.2%}")

import matplotlib.pyplot as plt
import os

#chart it

os.makedirs("output", exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(portfolio_growth.index, portfolio_growth, label="Equal-Weight Portfolio", linewidth=2)
ax.plot(benchmark_growth.index, benchmark_growth, label="S&P 500", linewidth=2, linestyle="--")

ax.set_title("Growth of $1: Portfolio vs. S&P 500 (3 Years)")
ax.set_xlabel("Date")
ax.set_ylabel("Value of $1 invested")
ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("output/portfolio_vs_sp500.png", dpi=150)
print("\nChart saved to output/portfolio_vs_sp500.png")