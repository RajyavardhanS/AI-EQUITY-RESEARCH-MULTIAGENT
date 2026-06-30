import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_risks(filing_text, ticker):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # The real section heading has this exact pattern: "Item 1A." followed
    # by whitespace then "Risk Factors" with no page number after it.
    # We search for "Risk Factors\nThe following" which is unique to the
    # actual section content (not TOC, not cross-references).
    marker = "Risk Factors\nThe following"
    start_idx = filing_text.find(marker)

    if start_idx == -1:
        # fallback to less specific marker
        start_idx = filing_text.find("Item 1A.    Risk Factors")

    if start_idx == -1:
        start_idx = 0

    max_chars = 20000
    relevant_text = filing_text[start_idx:start_idx + max_chars]

    prompt = f"""You are a financial risk analyst. Below is an excerpt from {ticker}'s 10-K filing, starting from the Risk Factors section.

Identify and summarize the TOP 5 risk factors mentioned in this filing excerpt.
For each risk, give:
1. A short title
2. A 2-3 sentence explanation in plain English

If the excerpt does not contain risk factor content, say so explicitly instead of guessing.

Filing excerpt:
{relevant_text}

Respond in this format:
1. [Risk Title]: [Explanation]
2. [Risk Title]: [Explanation]
...
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    with open("data/sample_10k.txt", "r", encoding="utf-8") as f:
        filing_text = f.read()

    ticker = input("Enter ticker for context: ")
    print("\nAnalyzing risks...\n")
    result = analyze_risks(filing_text, ticker)
    print(result)