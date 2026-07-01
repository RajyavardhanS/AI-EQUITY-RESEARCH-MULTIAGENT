![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![LLM](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-orange)
![Frontend](https://img.shields.io/badge/frontend-Streamlit-red)
![Finance](https://img.shields.io/badge/domain-Equity%20Research-green)
![Architecture](https://img.shields.io/badge/architecture-Multi--Agent-purple)
![Data](https://img.shields.io/badge/data-Live%20Financial%20Feeds-yellow)

---

# 📊 AI Based Equity Research Multi-Agent

## 🌍 Overview

**AI-EQUITY-RESEARCH-MULTIAGENT** is an autonomous institutional-style equity research pipeline designed to replicate how real-world analysts evaluate public companies.

The system combines:
* **Live market intelligence** from Yahoo Finance
* **SEC filing analysis** via direct EDGAR API integration
* **Real-time financial news** from NewsAPI
* **LLM-powered reasoning agents** running on Groq (Llama 3.3 70B)

to generate structured, analyst-grade equity research reports in under 60 seconds.

Unlike a traditional chatbot, this system is built as a **modular pipeline**, where every stage is independently testable, observable, and replaceable. Each agent knows nothing about the others — if one data source fails, only that section degrades, the rest of the report still runs.

---

## ⚡ Key Features

| Feature | Description |
| --- | --- |
| 📈 Live Market Data | Pulls stock price, P/E, EPS, margins, debt ratios, market cap — no API key required |
| 📑 SEC Filing Parser | Retrieves and cleans latest 10-K filings directly from SEC EDGAR |
| ⚠️ Risk Intelligence Agent | Extracts top 5 company-specific risk factors from actual filing text |
| 📰 News Sentiment Agent | Pulls latest headlines and classifies Bullish / Bearish / Neutral |
| 💰 Valuation Agent | Generates analyst-style valuation thesis with peer comparison and directional call |
| 📊 Analytics Layer | Formats raw numbers, calculates QoQ growth rates, runs peer benchmarking |
| 🧠 Multi-Agent Architecture | Independent LLM agents for each research dimension — stateless and composable |
| 🖥️ Streamlit Dashboard | Interactive frontend: enter ticker, generate report, download in one click |
| 📄 Markdown Report Generator | Structured downloadable reports with tables, trend data, and AI analysis |

---

## 🏗️ System Architecture

```
User Input (Ticker + Company Name + Optional Peers)
        |
        ├── Yahoo Finance Scraper   →  Live market metrics
        ├── SEC EDGAR Scraper       →  10-K filing text (cleaned)
        └── NewsAPI Scraper         →  Recent headlines
                  |
        Analytics Layer
        • Number formatting ($4.25T, 27.15%, 35.1x)
        • QoQ revenue + earnings growth (pandas + numpy)
        • Peer comparison table
                  |
        ┌─────────────────┬─────────────────┬─────────────────┐
        │ Valuation Agent │ Risk Agent      │ News Agent      │
        │ reasons over    │ reads 10-K text │ reads headlines │
        │ financials      │ for risks       │ for sentiment   │
        └─────────────────┴─────────────────┴─────────────────┘
                  |
        Report Generator (Orchestrator)
                  |
        Streamlit UI → rendered report + download
```

---

## 🗂️ Project Structure

```
equity-research-agent/
│
├── scrapers/
│   ├── yahoo_scraper.py        # Live market data via yfinance
│   ├── edgar_scraper.py        # SEC EDGAR 10-K fetcher + HTML cleaner
│   └── news_scraper.py         # NewsAPI with relevance filtering
│
├── analytics/
│   └── financial_analyzer.py   # Number formatting, QoQ growth, peer comparison
│
├── agents/
│   ├── risk_agent.py           # LLM reads 10-K → top 5 risk factors
│   ├── valuation_agent.py      # LLM reasons over financials → valuation thesis
│   └── news_agent.py           # LLM reads headlines → sentiment + themes
│
├── report_gen/
│   └── markdown_report.py      # Orchestrator: calls all scrapers + agents
│
├── data/                       # Generated reports (gitignored)
├── app.py                      # Streamlit web UI
├── .env                        # API keys (gitignored)
├── .gitignore
└── requirements.txt
```

---

## 📄 Sample Report Sections

| Section | What It Contains |
| --- | --- |
| Company Snapshot | 9 formatted live metrics — price, cap, P/E, margins, 52-week range, price position |
| Quarterly Trend | Last 4 quarters of revenue + net income with QoQ growth rates |
| Peer Comparison | Side-by-side table vs competitors with delta vs peer average |
| Valuation Analysis | 5-paragraph thesis with directional call and price target reasoning |
| Risk Factors | 5 risks from the actual 10-K filing — not generic, not fabricated |
| News Sentiment | Bullish/Bearish/Neutral + narrative summary + key themes |

---

## ⚙️ Tech Stack

| Component | Tool | Why |
| --- | --- | --- |
| Market data | `yfinance` | Free, no API key, direct Yahoo Finance access |
| Filing data | SEC EDGAR API | Free, official, all public 10-K/10-Q filings |
| News | NewsAPI | Structured search with relevance filtering |
| HTML parsing | BeautifulSoup4 | Strips SEC filing HTML to clean readable text |
| Analytics | pandas + numpy | QoQ growth rates, peer comparison, number formatting |
| LLM | Groq (Llama 3.3 70B) | Fast inference, generous free tier, high context window |
| Frontend | Streamlit | Python → web UI with no HTML/CSS required |
| Secrets | python-dotenv | API keys out of source code |

---

## 🚀 Getting Started

### 1. Clone and set up environment
```bash
git clone https://github.com/yourusername/equity-research-agent.git
cd equity-research-agent
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Get free API keys
- **Groq** (LLM): [console.groq.com](https://console.groq.com) → API Keys → Create
- **NewsAPI**: [newsapi.org](https://newsapi.org) → Get API Key
- SEC EDGAR and Yahoo Finance require **no API key**

### 3. Create `.env` file in project root
```
GROQ_API_KEY=your_groq_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### 4. Run
```bash
streamlit run app.py
```

Open `http://localhost:8501`, enter a ticker (e.g. `AAPL`), company name (e.g. `Apple Inc`), optional peer tickers (e.g. `MSFT,GOOGL`), and click **Generate Report**.

---

## 📦 Requirements

```
streamlit
groq
python-dotenv
yfinance
requests
pandas
numpy
beautifulsoup4
langchain-text-splitters
```

Install all:
```bash
pip install streamlit groq python-dotenv yfinance requests pandas numpy beautifulsoup4 langchain-text-splitters
```

---

## ⚠️ Known Limitations

- Groq free tier token limits require truncating large filings; finding the correct section is therefore critical
- NewsAPI free tier: up to 100 requests/day
- Report generation is sequential (~60 seconds); parallel agent execution is a planned improvement
- 
---
## 🗺️ Roadmap

- [ ] Generalized 10-K section extraction (structural Item 1A/1B detection across all companies)
- [ ] PDF export with formatted layout
- [ ] Earnings call transcript analysis
- [ ] Sector average benchmarking
- [ ] Caching layer for repeat ticker requests
- [ ] Async agent execution (parallel instead of sequential)

---

## 📌 Disclaimer

This tool is for educational and research purposes only. Reports are AI-generated and do not constitute financial advice. Always conduct your own research before making investment decisions.
