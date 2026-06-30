import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_valuation(stock_data, ticker):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a financial valuation analyst. Below are the current financial metrics for {ticker} ({stock_data.get('company_name', 'N/A')}).

Metrics:
- Current Price: ${stock_data.get('current_price', 'N/A')}
- Market Cap: ${stock_data.get('market_cap', 'N/A')}
- P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
- EPS: ${stock_data.get('eps', 'N/A')}
- Revenue: ${stock_data.get('revenue', 'N/A')}
- Profit Margin: {stock_data.get('profit_margin', 'N/A')}
- Debt to Equity: {stock_data.get('debt_to_equity', 'N/A')}
- 52-Week High: ${stock_data.get('52_week_high', 'N/A')}
- 52-Week Low: ${stock_data.get('52_week_low', 'N/A')}
- Sector: {stock_data.get('sector', 'N/A')}

Based on these metrics, provide a valuation thesis covering:
1. Is the stock currently overvalued, undervalued, or fairly valued? State your view clearly.
2. What does the P/E ratio suggest about market expectations for this company?
3. How healthy does the balance sheet look (profit margin, debt-to-equity)?
4. Where does the current price sit relative to its 52-week range, and what might that suggest?

Keep your response to 4-5 short paragraphs, written like an equity analyst's valuation note.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from scrapers.yahoo_scraper import get_stock_data

    ticker = input("Enter ticker: ")
    print("\nFetching stock data...")
    stock_data = get_stock_data(ticker)

    print("Analyzing valuation...\n")
    result = analyze_valuation(stock_data, ticker)
    print(result)