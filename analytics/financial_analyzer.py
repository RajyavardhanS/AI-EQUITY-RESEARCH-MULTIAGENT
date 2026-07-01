import pandas as pd
import numpy as np
import yfinance as yf


def format_large_number(n):
    """Convert raw numbers to readable format: 4138015391744 → $4.14T"""
    if n == "N/A" or n is None:
        return "N/A"
    try:
        n = float(n)
        if n >= 1e12:
            return f"${n/1e12:.2f}T"
        elif n >= 1e9:
            return f"${n/1e9:.2f}B"
        elif n >= 1e6:
            return f"${n/1e6:.2f}M"
        else:
            return f"${n:,.2f}"
    except:
        return "N/A"


def format_percent(n):
    """Convert 0.27152 → 27.15%"""
    if n == "N/A" or n is None:
        return "N/A"
    try:
        return f"{float(n) * 100:.2f}%"
    except:
        return "N/A"


def get_price_position(current, low, high):
    """Where does current price sit in the 52-week range? Returns 0-100%"""
    try:
        position = (float(current) - float(low)) / (float(high) - float(low)) * 100
        return f"{position:.1f}% above 52-week low"
    except:
        return "N/A"


def get_historical_financials(ticker):
    """
    Pull quarterly revenue + earnings history using yfinance.
    Returns a clean pandas DataFrame with growth rates calculated.
    This is where pandas earns its place — comparing rows across time.
    """
    stock = yf.Ticker(ticker)

    try:
        # Quarterly income statement
        income = stock.quarterly_income_stmt

        if income is None or income.empty:
            return None, None

        # Extract revenue and net income rows
        revenue_row = "Total Revenue"
        net_income_row = "Net Income"

        if revenue_row not in income.index or net_income_row not in income.index:
            return None, None

        # Get last 4 quarters
        revenue = income.loc[revenue_row].iloc[:4][::-1]      # oldest first
        net_income = income.loc[net_income_row].iloc[:4][::-1]

        # Build DataFrame
        df = pd.DataFrame({
            "Quarter": [str(d)[:7] for d in revenue.index],   # "2025-03" format
            "Revenue": revenue.values,
            "Net Income": net_income.values,
        })

        # Calculate quarter-over-quarter growth rates using numpy
        df["Revenue Growth QoQ"] = np.append(
            [np.nan],
            np.diff(df["Revenue"].values) / np.abs(df["Revenue"].values[:-1]) * 100
        )
        df["Net Income Growth QoQ"] = np.append(
            [np.nan],
            np.diff(df["Net Income"].values) / np.abs(df["Net Income"].values[:-1]) * 100
        )

        return df, income

    except Exception as e:
        print(f"Could not fetch historical financials: {e}")
        return None, None


def get_peer_comparison(ticker, peers):
    """
    Pull key metrics for ticker + peers and return a comparison DataFrame.
    This is where pandas is essential — aligning metrics across multiple companies.
    """
    all_data = []

    tickers_to_check = [ticker] + peers

    for t in tickers_to_check:
        try:
            stock = yf.Ticker(t)
            info = stock.info
            all_data.append({
                "Ticker": t,
                "Company": info.get("shortName", t),
                "P/E Ratio": info.get("trailingPE", np.nan),
                "Profit Margin": info.get("profitMargins", np.nan),
                "Revenue": info.get("totalRevenue", np.nan),
                "Market Cap": info.get("marketCap", np.nan),
                "Debt/Equity": info.get("debtToEquity", np.nan),
            })
        except Exception as e:
            print(f"Could not fetch data for {t}: {e}")

    if not all_data:
        return None

    df = pd.DataFrame(all_data)
    df.set_index("Ticker", inplace=True)

    # Calculate how target ticker compares to peer average
    peer_df = df.drop(ticker, errors="ignore")
    peer_avg_pe = peer_df["P/E Ratio"].mean()
    peer_avg_margin = peer_df["Profit Margin"].mean()

    comparison = {
        "df": df,
        "peer_avg_pe": peer_avg_pe,
        "peer_avg_margin": peer_avg_margin,
        "pe_vs_peers": df.loc[ticker, "P/E Ratio"] - peer_avg_pe if ticker in df.index else np.nan,
        "margin_vs_peers": df.loc[ticker, "Profit Margin"] - peer_avg_margin if ticker in df.index else np.nan,
    }

    return comparison


def build_analytics_summary(ticker, stock_data, peers=None):
    """
    Master function called by the report generator.
    Returns a clean, formatted analytics block ready to be fed to agents.
    """
    print(f"  Running analytics for {ticker}...")

    # Format raw numbers properly
    formatted = {
        "ticker": ticker,
        "company_name": stock_data.get("company_name", "N/A"),
        "current_price": f"${stock_data.get('current_price', 'N/A')}",
        "market_cap": format_large_number(stock_data.get("market_cap")),
        "pe_ratio": f"{float(stock_data.get('pe_ratio', 0)):.1f}x",
        "eps": f"${stock_data.get('eps', 'N/A')}",
        "revenue": format_large_number(stock_data.get("revenue")),
        "profit_margin": format_percent(stock_data.get("profit_margin")),
        "debt_to_equity": stock_data.get("debt_to_equity", "N/A"),
        "52_week_high": f"${stock_data.get('52_week_high', 'N/A')}",
        "52_week_low": f"${stock_data.get('52_week_low', 'N/A')}",
        "price_position": get_price_position(
            stock_data.get("current_price"),
            stock_data.get("52_week_low"),
            stock_data.get("52_week_high")
        ),
    }

    # Historical financials
    hist_df, _ = get_historical_financials(ticker)
    formatted["historical_df"] = hist_df

    # Peer comparison
    if peers:
        peer_comparison = get_peer_comparison(ticker, peers)
        formatted["peer_comparison"] = peer_comparison
    else:
        formatted["peer_comparison"] = None

    return formatted


if __name__ == "__main__":
    ticker = input("Enter ticker: ")
    peers_input = input("Enter peer tickers comma-separated (e.g. MSFT,GOOGL) or press Enter to skip: ")
    peers = [p.strip() for p in peers_input.split(",")] if peers_input.strip() else []

    from scrapers.yahoo_scraper import get_stock_data
    stock_data = get_stock_data(ticker)

    summary = build_analytics_summary(ticker, stock_data, peers)

    print("\n--- Formatted Metrics ---")
    for k, v in summary.items():
        if k not in ["historical_df", "peer_comparison"]:
            print(f"{k}: {v}")

    if summary["historical_df"] is not None:
        print("\n--- Quarterly Financials ---")
        print(summary["historical_df"].to_string(index=False))

    if summary["peer_comparison"] is not None:
        print("\n--- Peer Comparison ---")
        print(summary["peer_comparison"]["df"].to_string())
        print(f"\nP/E vs peer avg: {summary['peer_comparison']['pe_vs_peers']:+.2f}")
        print(f"Margin vs peer avg: {summary['peer_comparison']['margin_vs_peers']*100:+.2f}%")