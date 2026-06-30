import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_news_sentiment(articles, ticker):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if not articles:
        return "No recent news articles found to analyze."

    # Format articles into a readable block for the LLM
    articles_text = ""
    for i, a in enumerate(articles, 1):
        articles_text += f"{i}. {a['title']}\n   {a.get('description', '')}\n   Source: {a['source']}, {a['published_at']}\n\n"

    prompt = f"""You are a financial news analyst. Below are recent news headlines about {ticker}.

Based on these headlines, provide:
1. Overall sentiment: Bullish, Bearish, or Neutral
2. A 3-4 sentence summary of what the current news narrative is about this stock
3. Any notable events or themes mentioned (e.g. product launches, earnings, legal issues, analyst opinions)

Recent news:
{articles_text}

Respond in this format:
Sentiment: [Bullish/Bearish/Neutral]
Summary: [your summary]
Key Themes: [list of themes]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    import sys
    sys.path.append("..")
    from scrapers.news_scraper import get_company_news

    company = input("Enter company name: ")
    ticker = input("Enter ticker: ")

    print("\nFetching news...")
    articles = get_company_news(company, ticker, count=8)

    print(f"Found {len(articles)} articles. Analyzing sentiment...\n")
    result = analyze_news_sentiment(articles, ticker)
    print(result)