import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_stock_data(ticker, start, end):
    # Download historical price data from Yahoo Finance
    data = yf.download(ticker, start=start, end=end)
    close_prices = data["Close"][ticker]
    return close_prices

def calculate_metrics(close_prices, ticker):
    # Pct_change calculates daily return as (today - yesterday) / yesterday
    daily_returns = close_prices.pct_change()
    
    # Standard deviation of returns measures how much prices deviate from average
    daily_volatility = daily_returns.std()
    # Annualize by multiplying by sqrt(252) - there are 252 trading days in a year
    annual_volatility = daily_volatility * np.sqrt(252)
    
    avg_daily_return = daily_returns.mean()
    # Scale daily return to annual by multiplying by 252 trading days
    annual_return = avg_daily_return * 252
    
    # Risk free rate represents return on a US Treasury bond (safe baseline)
    risk_free_rate = 0.05
    # Sharpe ratio measures return earned per unit of risk taken
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    
    # VaR: worst expected daily loss 95% of the time (bottom 5% of returns)
    VaR_95 = daily_returns.quantile(0.05)
    
    print(f"\n--- Risk Metrics for {ticker} ---")
    print(f"Daily Volatility:    {round(daily_volatility * 100, 2)}%")
    print(f"Annual Volatility:   {round(annual_volatility * 100, 2)}%")
    print(f"Annual Return:       {round(annual_return * 100, 2)}%")
    print(f"Sharpe Ratio:        {round(sharpe_ratio, 2)}")
    print(f"Value at Risk (95%): {round(VaR_95 * 100, 2)}%")
    
    return daily_returns, VaR_95

def plot_charts(close_prices, daily_returns, VaR_95, ticker):
    # Chart 1: Price over time
    plt.figure(figsize=(12, 5))
    plt.plot(close_prices.index, close_prices.values)
    plt.title(f"{ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{ticker}_price_chart.png", dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()

    # Chart 2: Distribution of daily returns with VaR marked
    plt.figure(figsize=(12, 5))
    plt.hist(daily_returns.dropna() * 100, bins=50, edgecolor='black')
    plt.axvline(VaR_95 * 100, color='red', linestyle='dashed', linewidth=2, label=f'VaR 95%: {round(VaR_95 * 100, 2)}%')
    plt.title(f"{ticker} Daily Returns Distribution")
    plt.xlabel("Daily Return (%)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{ticker}_returns_distribution.png", dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()

def plot_rolling_volatility(daily_returns, ticker):
    # Rolling 30-day window shows how risk changed over time vs a single average
    rolling_vol = daily_returns.rolling(window=30).std() * np.sqrt(252) * 100
    
    # Chart 3: Rolling volatility over time
    plt.figure(figsize=(12, 5))
    plt.plot(rolling_vol.index, rolling_vol.values)
    plt.title(f"{ticker} Rolling 30-Day Volatility - 2023")
    plt.xlabel("Date")
    plt.ylabel("Annualized Volatility (%)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{ticker}_rolling_volatility.png", dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()

def analyze_stock(ticker, start, end):
    # Master function that runs the full pipeline for a given stock
    close_prices = get_stock_data(ticker, start, end)
    daily_returns, VaR_95 = calculate_metrics(close_prices, ticker)
    plot_charts(close_prices, daily_returns, VaR_95, ticker)
    plot_rolling_volatility(daily_returns, ticker)

# Analyze these stocks for the full year 2023
tickers = ["AAPL", "TSLA", "GOOGL", "MSFT"]

for ticker in tickers:
    analyze_stock(ticker, "2023-01-01", "2024-01-01")