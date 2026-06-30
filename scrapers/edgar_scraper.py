import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Raj singhrajyavardhan15@gmail.com"}

def get_cik(ticker):
    """Look up a company's CIK number (EDGAR's internal ID) from its ticker"""
    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=HEADERS)
    companies = response.json()

    for entry in companies.values():
        if entry["ticker"].upper() == ticker.upper():
            return str(entry["cik_str"]).zfill(10)  # CIK needs to be 10 digits, zero-padded
    return None


def get_recent_filings(ticker, filing_type="10-K", count=1):
    cik = get_cik(ticker)
    if not cik:
        print(f"Could not find CIK for {ticker}")
        return []

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    recent = data["filings"]["recent"]
    filings = []

    for i in range(len(recent["form"])):
        if recent["form"][i] == filing_type:
            filings.append({
                "form": recent["form"][i],
                "filing_date": recent["filingDate"][i],
                "accession_number": recent["accessionNumber"][i],
                "primary_document": recent["primaryDocument"][i]
            })
            if len(filings) >= count:
                break

    return filings


def get_filing_text(ticker, accession_number, primary_document):
    cik = get_cik(ticker)
    accession_no_dashes = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dashes}/{primary_document}"

    response = requests.get(url, headers=HEADERS)
    return response.text  # raw HTML of the filing


def clean_filing_text(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove script and style tags entirely
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Clean up excessive blank lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    clean_text = "\n".join(lines)

    return clean_text


if __name__ == "__main__":
    ticker = input("Enter stock ticker: ")
    filings = get_recent_filings(ticker, filing_type="10-K", count=1)
    for f in filings:
        print(f)

    if filings:
        print("\nFetching filing text...")
        raw_text = get_filing_text(ticker, filings[0]["accession_number"], filings[0]["primary_document"])
        print(f"Raw length: {len(raw_text)} characters")

        print("\nCleaning HTML...")
        clean_text = clean_filing_text(raw_text)
        print(f"Clean length: {len(clean_text)} characters")

        with open("data/sample_10k.txt", "w", encoding="utf-8") as f:
            f.write(clean_text)
        print("\nSaved cleaned filing to data/sample_10k.txt")