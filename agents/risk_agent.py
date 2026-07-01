import os
from groq import Groq
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def find_relevant_chunks(filing_text, query="risk factors material adverse", top_n=5):
    """
    Split the filing into chunks and return the ones most likely
    to contain risk factor content — without any company-specific
    string matching. Works for any 10-K regardless of formatting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,    # each chunk ~2000 chars
        chunk_overlap=200,  # 200 char overlap so context isn't lost at boundaries
        separators=["\n\n", "\n", ".", " "]  # try to split at natural boundaries first
    )
    chunks = splitter.split_text(filing_text)

    # Score each chunk by counting how many risk-related keywords it contains
    # Simple but effective — risk sections have dense keyword concentration
    keywords = [
        "risk", "adverse", "material", "uncertainty", "may not",
        "could", "subject to", "exposure", "competition", "regulatory",
        "litigation", "supply chain", "cybersecurity", "inflation",
        "geopolitical", "failure", "disruption", "volatility"
    ]

    scored = []
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = sum(chunk_lower.count(kw) for kw in keywords)
        scored.append((score, i, chunk))

    # Sort by score descending, take top N chunks
    scored.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [chunk for _, _, chunk in scored[:top_n]]

    return top_chunks


def analyze_risks(filing_text, ticker):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if not filing_text:
        return "No filing data available."

    print(f"    Splitting filing into chunks and finding relevant sections...")
    relevant_chunks = find_relevant_chunks(filing_text)
    context = "\n\n---\n\n".join(relevant_chunks)

    # Safety check — stay within Groq token limits
    max_chars = 20000
    if len(context) > max_chars:
        context = context[:max_chars]

    prompt = f"""You are a financial risk analyst. Below are the most risk-relevant excerpts from {ticker}'s 10-K annual filing, automatically selected from the full document.

Based on these excerpts, identify and summarize the TOP 5 risk factors.
For each risk:
1. Give it a short title
2. Explain it in 2-3 sentences in plain English

If the excerpts do not contain sufficient risk factor content, say so explicitly — do not guess or fabricate risks.

Filing excerpts:
{context}

Format:
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