# Stock Risk Analyzer

A Python tool that downloads historical stock data and calculates key risk metrics used in quantitative finance. Built as a first project to learn financial data analysis and risk modeling using real market data.

## Background
Risk analytics is at the core of every investment decision. Before allocating capital to any asset, portfolio managers and risk analysts need to understand not just how much a stock returned, but how much risk was taken to generate that return. This project replicates the kind of analysis done daily at hedge funds, asset managers, and investment banks.

## What it does
- Downloads real historical stock data from Yahoo Finance using yfinance
- Calculates 5 professional risk metrics: Daily Volatility, Annual Volatility, Sharpe Ratio, Value at Risk (95%), and Max Drawdown
- Generates 4 charts per stock: price history, returns distribution with VaR marked, rolling 30-day volatility, and cumulative returns
- Prints a comparison summary table of all stocks side by side
- Runs on any list of stocks automatically — just add a ticker to the list

## How it works
The tool is built around 4 functions that form a clean pipeline:
- `get_stock_data()` — pulls historical closing prices for any ticker and date range
- `calculate_metrics()` — computes all risk metrics from the price data
- `plot_charts()` — generates price and returns distribution charts
- `plot_rolling_volatility()` — generates a rolling volatility chart showing how risk evolved over time
- `plot_cumulative_returns()` — shows how $1 invested would grow over the period
- `print_summary_table()` — prints a clean comparison table of all stocks
- `analyze_stock()` — master function that runs the full pipeline with one call

## Stocks Analyzed (2023)
| Stock | Annual Return | Annual Volatility | Sharpe Ratio | VaR (95%) | Max Drawdown |
|-------|--------------|-------------------|--------------|-----------|--------------|
| AAPL  | 46.24%       | 19.95%            | 2.07         | -1.72%    | -14.93%      |
| TSLA  | 98.10%       | 52.65%            | 1.77         | -5.01%    | -32.72%      |
| GOOGL | 50.14%       | 30.40%            | 1.48         | -2.51%    | -17.27%      |
| MSFT  | 49.69%       | 25.12%            | 1.78         | -2.29%    | -12.99%      |

## Analysis
**AAPL** — Best risk-adjusted performance of the group with a Sharpe ratio of 2.07. Lowest volatility at 19.95% and rolling volatility trended downward through the year, indicating increasing market stability. VaR of -1.72% and max drawdown of -14.93% reflect limited downside risk.

**TSLA** — Highest raw return at 98.1% but nearly 3x Apple's volatility at 52.65%. Max drawdown of -32.72% means at its worst point Tesla had lost nearly a third of its peak value. A VaR of -5.01% means on a bad d
