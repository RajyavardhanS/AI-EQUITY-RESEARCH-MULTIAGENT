import sys
sys.path.append(".")
import os
from datetime import datetime
from scrapers.yahoo_scraper import get_stock_data
from scrapers.edgar_scraper import get_recent_filings, get_filing_text, clean_filing_text
from scrapers.news_scraper import get_company_news
from agents.risk_agent import analyze_risks
from agents.valuation_agent import analyze_valuation
from agents.news_agent import analyze_news_sentiment
from analytics.financial_analyzer import build_analytics_summary

os.makedirs("data", exist_ok=True)


def generate_report(ticker, company_name, peers=None):
    print(f"\n{'='*50}")
    print(f"Generating report for {ticker}")
    print(f"{'='*50}\n")

    print("[1/6] Fetching stock data...")
    stock_data = get_stock_data(ticker)

    print("[2/6] Running analytics...")
    if peers is None:
        peers = []
    analytics = build_analytics_summary(ticker, stock_data, peers)

    print("[3/6] Fetching 10-K filing...")
    filings = get_recent_filings(ticker, filing_type="10-K", count=1)
    filing_text = ""
    if filings:
        raw_text = get_filing_text(
            ticker,
            filings[0]["accession_number"],
            filings[0]["primary_document"]
        )
        filing_text = clean_filing_text(raw_text)

    print("[4/6] Fetching news...")
    articles = get_company_news(company_name, ticker, count=8)

    print("[5/6] Running AI agents...")
    risk_summary = analyze_risks(filing_text, ticker) if filing_text else "No filing data available."
    valuation_summary = analyze_valuation(analytics, ticker)
    news_summary = analyze_news_sentiment(articles, ticker)

    print("[6/6] Assembling report...")

    # Peer comparison section
    peer_section = ""
    if analytics.get("peer_comparison") is not None:
        pc = analytics["peer_comparison"]
        peer_df = pc["df"].copy()
        peer_df["Revenue"] = peer_df["Revenue"].apply(
            lambda x: f"${x/1e9:.1f}B" if x >= 1e9 else f"${x/1e6:.1f}M"
        )
        peer_df["Market Cap"] = peer_df["Market Cap"].apply(
            lambda x: f"${x/1e12:.2f}T" if x >= 1e12 else f"${x/1e9:.1f}B"
        )
        peer_df["Profit Margin"] = peer_df["Profit Margin"].apply(
            lambda x: f"{x*100:.1f}%"
        )
        peer_df["P/E Ratio"] = peer_df["P/E Ratio"].apply(
            lambda x: f"{x:.1f}x"
        )

        peer_section = f"""
## Peer Comparison

| | {" | ".join(peer_df.columns)} |
|---|{"---|" * len(peer_df.columns)}
"""
        for idx, row in peer_df.iterrows():
            peer_section += f"| **{idx}** | {' | '.join(str(v) for v in row.values)} |\n"

        peer_section += f"""
- **P/E vs peer average:** {pc['pe_vs_peers']:+.2f} points
- **Profit margin vs peer average:** {pc['margin_vs_peers']*100:+.2f}%
"""

    # Historical financials section
    hist_section = ""
    if analytics.get("historical_df") is not None:
        df = analytics["historical_df"].copy()
        df["Revenue"] = df["Revenue"].apply(lambda x: f"${x/1e9:.1f}B")
        df["Net Income"] = df["Net Income"].apply(lambda x: f"${x/1e9:.1f}B")
        df["Revenue Growth QoQ"] = df["Revenue Growth QoQ"].apply(
            lambda x: f"{x:+.1f}%" if str(x) != "nan" else "—"
        )
        df["Net Income Growth QoQ"] = df["Net Income Growth QoQ"].apply(
            lambda x: f"{x:+.1f}%" if str(x) != "nan" else "—"
        )

        hist_section = "## Quarterly Financial Trend (Last 4 Quarters)\n\n"
        hist_section += f"| {' | '.join(df.columns)} |\n"
        hist_section += f"|{'---|' * len(df.columns)}\n"
        for _, row in df.iterrows():
            hist_section += f"| {' | '.join(str(v) for v in row.values)} |\n"

    report = f"""# AI Based Equity Research Multi-Agent: {analytics['company_name']} ({ticker})
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## Company Snapshot

| Metric | Value |
|---|---|
| Current Price | {analytics['current_price']} |
| Market Cap | {analytics['market_cap']} |
| P/E Ratio | {analytics['pe_ratio']} |
| EPS | {analytics['eps']} |
| Revenue (TTM) | {analytics['revenue']} |
| Profit Margin | {analytics['profit_margin']} |
| Debt to Equity | {analytics['debt_to_equity']} |
| 52-Week Range | {analytics['52_week_low']} – {analytics['52_week_high']} |
| Price Position | {analytics['price_position']} |

{hist_section}

{peer_section}

## Valuation Analysis

{valuation_summary}

## Risk Factors

{risk_summary}

## News & Market Sentiment

{news_summary}

---
*AI Based Equity Research Multi-Agent — AI-generated report. Not financial advice.*
"""

    filename = f"data/{ticker}_report.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved to {filename}")
    return report


if __name__ == "__main__":
    ticker = input("Enter ticker: ")
    company_name = input("Enter company name: ")
    peers_input = input("Enter peer tickers comma-separated (e.g. MSFT,GOOGL) or press Enter to skip: ")
    peers = [p.strip() for p in peers_input.split(",")] if peers_input.strip() else []
    report = generate_report(ticker, company_name, peers)
    print("\n" + "="*50)
    print(report)