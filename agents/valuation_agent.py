import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_valuation(analytics_summary, ticker):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Build peer comparison text if available
    peer_text = ""
    if analytics_summary.get("peer_comparison") is not None:
        pc = analytics_summary["peer_comparison"]
        peer_text = f"""
Peer Comparison:
{pc['df'].to_string()}

vs Peer Averages:
- P/E ratio is {pc['pe_vs_peers']:+.2f} points vs peer average
- Profit margin is {pc['margin_vs_peers']*100:+.2f}% vs peer average
"""

    # Build historical financials text if available
    hist_text = ""
    if analytics_summary.get("historical_df") is not None:
        hist_text = f"""
Quarterly Revenue & Earnings Trend (last 4 quarters):
{analytics_summary['historical_df'].to_string(index=False)}
"""

    prompt = f"""You are a financial valuation analyst. Below are the financial metrics for {ticker} ({analytics_summary.get('company_name', 'N/A')}), including peer comparison and historical trend data.

Current Metrics:
- Current Price: {analytics_summary['current_price']}
- Market Cap: {analytics_summary['market_cap']}
- P/E Ratio: {analytics_summary['pe_ratio']}
- EPS: {analytics_summary['eps']}
- Revenue: {analytics_summary['revenue']}
- Profit Margin: {analytics_summary['profit_margin']}
- Debt to Equity: {analytics_summary['debt_to_equity']}
- 52-Week Range: {analytics_summary['52_week_low']} - {analytics_summary['52_week_high']}
- Price Position: {analytics_summary['price_position']}
{peer_text}
{hist_text}

Based on ALL of the above data, provide a valuation thesis covering:
1. Is the stock overvalued, undervalued, or fairly valued? State clearly.
2. What does the P/E premium/discount vs peers suggest?
3. How do margins and debt compare to competitors?
4. What does the quarterly revenue trend reveal?
5. Where does the price sit in its 52-week range and what does that suggest?

Write like a senior equity analyst — 5 short paragraphs, specific numbers, clear directional call.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content