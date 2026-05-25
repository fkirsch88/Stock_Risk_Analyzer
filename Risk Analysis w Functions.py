import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_stock_data(ticker, start, end):
    # Download historical price data from Yahoo Finance
    data = yf.download(ticker, start=start, end=end)
    close_prices = data["Close"][ticker]
    return close_prices

def calculate_metrics(close_prices, ticker):
    # pct_change calculates daily return as (today - yesterday) / yesterday
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
    
    # Max drawdown: worst peak to trough loss over the entire period
    cumulative_returns = (1 + daily_returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    print(f"\n--- Risk Metrics for {ticker} ---")
    print(f"Daily Volatility:    {round(daily_volatility * 100, 2)}%")
    print(f"Annual Volatility:   {round(annual_volatility * 100, 2)}%")
    print(f"Annual Return:       {round(annual_return * 100, 2)}%")
    print(f"Sharpe Ratio:        {round(sharpe_ratio, 2)}")
    print(f"Value at Risk (95%): {round(VaR_95 * 100, 2)}%")
    print(f"Max Drawdown:        {round(max_drawdown * 100, 2)}%")
    
    return daily_returns, VaR_95, max_drawdown, annual_return, annual_volatility, sharpe_ratio

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

def plot_cumulative_returns(daily_returns, ticker):
    # Cumulative returns show how $1 invested would grow over time
    cumulative_returns = (1 + daily_returns).cumprod()
    
    # Chart 4: Cumulative returns over time
    plt.figure(figsize=(12, 5))
    plt.plot(cumulative_returns.index, cumulative_returns.values)
    plt.title(f"{ticker} Cumulative Returns - 2023")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1 Invested")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{ticker}_cumulative_returns.png", dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()

def print_summary_table(results):
    # Print a comparison table of all stocks side by side
    print("\n" + "="*75)
    print(f"{'SUMMARY TABLE':^75}")
    print("="*75)
    print(f"{'Ticker':<8} {'Ann. Return':>12} {'Ann. Volatility':>16} {'Sharpe':>8} {'VaR 95%':>10} {'Max DD':>10}")
    print("-"*75)
    for r in results:
        print(f"{r['ticker']:<8} {r['annual_return']:>12} {r['annual_volatility']:>16} {r['sharpe']:>8} {r['var']:>10} {r['max_drawdown']:>10}")
    print("="*75)

def analyze_stock(ticker, start, end):
    # Master function that runs the full pipeline for a given stock
    close_prices = get_stock_data(ticker, start, end)
    daily_returns, VaR_95, max_drawdown, annual_return, annual_volatility, sharpe_ratio = calculate_metrics(close_prices, ticker)
    plot_charts(close_prices, daily_returns, VaR_95, ticker)
    plot_rolling_volatility(daily_returns, ticker)
    plot_cumulative_returns(daily_returns, ticker)
    
    # Store results as a dictionary for the summary table
    return {
        "ticker": ticker,
        "annual_return": f"{round(annual_return * 100, 2)}%",
        "annual_volatility": f"{round(annual_volatility * 100, 2)}%",
        "sharpe": round(sharpe_ratio, 2),
        "var": f"{round(VaR_95 * 100, 2)}%",
        "max_drawdown": f"{round(max_drawdown * 100, 2)}%"
    }

# Analyze these stocks for the full year 2023
tickers = ["AAPL", "TSLA", "GOOGL", "MSFT"]
results = []

for ticker in tickers:
    result = analyze_stock(ticker, "2023-01-01", "2024-01-01")
    results.append(result)

# Print summary table after all stocks are analyzed
print_summary_table(results)
