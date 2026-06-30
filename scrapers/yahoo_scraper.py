import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    data = {
        "ticker": ticker,
        "company_name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "current_price": info.get("currentPrice", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "eps": info.get("trailingEps", "N/A"),
        "revenue": info.get("totalRevenue", "N/A"),
        "profit_margin": info.get("profitMargins", "N/A"),
        "debt_to_equity": info.get("debtToEquity", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
    }
    return data

if __name__ == "__main__":
    ticker = input("Enter stock ticker (e.g. AAPL): ")
    data = get_stock_data(ticker)
    for key, value in data.items():
        print(f"{key}: {value}")