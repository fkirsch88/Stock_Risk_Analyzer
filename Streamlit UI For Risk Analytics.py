import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    close_prices = data["Close"][ticker]
    return close_prices

def calculate_metrics(close_prices, ticker):
    daily_returns = close_prices.pct_change()
    daily_volatility = daily_returns.std()
    annual_volatility = daily_volatility * np.sqrt(252)
    avg_daily_return = daily_returns.mean()
    annual_return = avg_daily_return * 252
    risk_free_rate = 0.05
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    VaR_95 = daily_returns.quantile(0.05)
    cumulative_returns = (1 + daily_returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()

    st.subheader(f"Risk Metrics for {ticker}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Daily Volatility", f"{round(daily_volatility * 100, 2)}%")
    col1.metric("Annual Volatility", f"{round(annual_volatility * 100, 2)}%")
    col2.metric("Annual Return", f"{round(annual_return * 100, 2)}%")
    col2.metric("Sharpe Ratio", round(sharpe_ratio, 2))
    col3.metric("Value at Risk (95%)", f"{round(VaR_95 * 100, 2)}%")
    col3.metric("Max Drawdown", f"{round(max_drawdown * 100, 2)}%")

    return daily_returns, VaR_95, max_drawdown, annual_return, annual_volatility, sharpe_ratio

def plot_charts(close_prices, daily_returns, VaR_95, ticker):
    # Chart 1: Price over time
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(close_prices.index, close_prices.values)
    ax1.set_title(f"{ticker} Stock Price")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price (USD)")
    ax1.grid(True)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close()

    # Chart 2: Returns distribution
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.hist(daily_returns.dropna() * 100, bins=50, edgecolor='black')
    ax2.axvline(VaR_95 * 100, color='red', linestyle='dashed', linewidth=2, label=f'VaR 95%: {round(VaR_95 * 100, 2)}%')
    ax2.set_title(f"{ticker} Daily Returns Distribution")
    ax2.set_xlabel("Daily Return (%)")
    ax2.set_ylabel("Frequency")
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

def plot_rolling_volatility(daily_returns, ticker):
    rolling_vol = daily_returns.rolling(window=30).std() * np.sqrt(252) * 100
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(rolling_vol.index, rolling_vol.values)
    ax.set_title(f"{ticker} Rolling 30-Day Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualized Volatility (%)")
    plt.xticks(rotation=45)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def plot_cumulative_returns(daily_returns, ticker):
    cumulative_returns = (1 + daily_returns).cumprod()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(cumulative_returns.index, cumulative_returns.values)
    ax.set_title(f"{ticker} Cumulative Returns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth of $1 Invested")
    plt.xticks(rotation=45)
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def analyze_stock(ticker, start, end):
    close_prices = get_stock_data(ticker, start, end)
    daily_returns, VaR_95, max_drawdown, annual_return, annual_volatility, sharpe_ratio = calculate_metrics(close_prices, ticker)
    plot_charts(close_prices, daily_returns, VaR_95, ticker)
    plot_rolling_volatility(daily_returns, ticker)
    plot_cumulative_returns(daily_returns, ticker)

# Streamlit UI
st.title("Stock Risk Analyzer")
st.write("Enter a stock ticker and date range to analyze risk metrics.")

ticker = st.text_input("Enter a Stock Ticker:")
start = st.date_input("Start Date")
end = st.date_input("End Date")
button = st.button("Analyze")

if button:
    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    analyze_stock(ticker, start_str, end_str)