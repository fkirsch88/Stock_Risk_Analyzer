# Stock Risk Analyzer

A Python tool that downloads historical stock data and calculates key risk metrics used in quantitative finance.

## What it does
- Calculates Daily Volatility, Annual Volatility, Annual Return, Sharpe Ratio, and Value at Risk (95%)
- Generates 3 charts per stock: price history, returns distribution, and rolling volatility
- Runs on any list of stocks automatically

## Stocks Analyzed (2023)
| Stock | Annual Return | Annual Volatility | Sharpe Ratio | VaR (95%) |
|-------|--------------|-------------------|--------------|-----------|
| AAPL  | 46.24%       | 19.95%            | 2.07         | -1.72%    |
| TSLA  | 98.10%       | 52.65%            | 1.77         | -5.01%    |
| GOOGL | 50.14%       | 30.40%            | 1.48         | -2.51%    |
| MSFT  | 49.69%       | 25.12%            | 1.78         | -2.29%    |

## Analysis
**AAPL** — Best risk-adjusted performance of the group with a Sharpe ratio of 2.07. Lowest volatility at 19.95% and rolling volatility trended downward through the year, indicating increasing market stability. VaR of -1.72% reflects limited downside risk.

**TSLA** — Highest raw return at 98.1% but nearly 3x Apple's volatility at 52.65%. A VaR of -5.01% means on a bad day Tesla could lose 3x more than Apple. High risk, high reward.

**GOOGL** — Lowest Sharpe ratio of the group at 1.48, meaning it delivered the least return per unit of risk. Mid-year volatility spikes are visible in the rolling chart.

**MSFT** — Closely mirrored Apple in return (49.69%) but with slightly higher volatility (25.12%), giving it a Sharpe of 1.78. Still a strong risk-adjusted performer.

**Summary** — For a risk-conscious investor in 2023, Apple offered the best balance of return and stability. Tesla was a high risk high reward bet. Google was the weakest on a risk-adjusted basis despite solid returns.

## Skills Used
- Python, pandas, numpy, matplotlib
- Time series analysis
- Risk metrics: Volatility, Sharpe Ratio, Value at Risk
- Data visualization

## Libraries Required
pip install yfinance pandas numpy matplotlib
