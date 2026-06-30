import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_company_news(company_name, ticker=None, count=5):
    api_key = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"

    # Make the query more specific to avoid generic keyword matches
    # (e.g. "Apple" alone matches fruit, movies, unrelated mentions)
    query = f'"{company_name}"'
    if ticker:
        query += f' OR "{ticker} stock"'

    params = {
        "q": query,
        "sortBy": "relevancy",  # changed from publishedAt -- relevancy filters noise better
        "language": "en",
        "pageSize": count,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print(f"Error: {data.get('message', 'Unknown error')}")
        return []

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url")
        })

    return articles


if __name__ == "__main__":
    company = input("Enter company name (e.g. Apple Inc): ")
    ticker = input("Enter ticker (e.g. AAPL): ")
    articles = get_company_news(company, ticker)

    print(f"\nFound {len(articles)} articles:\n")
    for a in articles:
        print(f"- {a['title']} ({a['source']}, {a['published_at']})")
