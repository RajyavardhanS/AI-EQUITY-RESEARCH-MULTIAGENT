# 📊 AI-EQUITY-RESEARCH-MULTIAGENT — Autonomous Multi-Agent Equity Research Engine

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![LLM](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-orange)
![Frontend](https://img.shields.io/badge/frontend-Streamlit-red)
![Finance](https://img.shields.io/badge/domain-Equity%20Research-green)
![Architecture](https://img.shields.io/badge/architecture-Multi--Agent-purple)
![Data](https://img.shields.io/badge/data-Live%20Financial%20Feeds-yellow)

---

## 🌍 Overview

**AI-EQUITY-RESEARCH-MULTIAGENT** is an autonomous institutional-style equity research pipeline designed to replicate how real-world analysts evaluate public companies.

The system combines:

* **Live market intelligence**
* **SEC filing analysis**
* **Real-time financial news**
* **LLM-powered reasoning agents**

to generate structured, analyst-grade equity research reports.

Unlike a traditional chatbot, this system is built as a **modular pipeline**, where every stage is independently testable, observable, and replaceable.

---

## ⚡ Key Features

| Feature                      | Description                                                   |
| ---------------------------- | ------------------------------------------------------------- |
| 📈 Live Market Data          | Pulls stock price, P/E, EPS, margins, debt ratios, market cap |
| 📑 SEC Filing Parser         | Retrieves latest 10-K filings directly from SEC EDGAR         |
| ⚠️ Risk Intelligence Agent   | Extracts and analyzes company-specific risk factors           |
| 📰 News Sentiment Agent      | Pulls latest news and performs sentiment analysis             |
| 💰 Valuation Agent           | Generates analyst-style valuation thesis                      |
| 🧠 Multi-Agent Architecture  | Independent LLM agents for each research dimension            |
| 📊 Streamlit Dashboard       | Interactive frontend for report generation                    |
| 📄 Markdown Report Generator | Generates structured downloadable reports                     |

---

## 🧠 Multi-Agent Architecture

Traditional stock research tools rely on one model for everything.

This system separates responsibilities:

### 1. Valuation Agent

Reasons over structured financial metrics.

Analyzes:

* Revenue quality
* Profitability
* Valuation multiples
* Debt strength

---

### 2. Risk Agent

Reads actual SEC filing text.

Finds:

* Operational risks
* Legal risks
* Competitive threats
* Macro vulnerabilities

---

### 3. News Agent

Processes live news.

Outputs:

* Sentiment classification
* Key catalysts
* Recent developments

---

## 🏗 System Architecture

```text id="sys001"
User Input (Ticker)
        ↓
+------------------------+
| Data Collection Layer  |
|------------------------|
| Yahoo Finance          |
| SEC EDGAR              |
| NewsAPI                |
+------------------------+
        ↓
+------------------------+
| AI Agent Layer         |
|------------------------|
| Valuation Agent        |
| Risk Agent             |
| News Agent             |
+------------------------+
        ↓
+------------------------+
| Report Orchestrator    |
+------------------------+
        ↓
+------------------------+
| Streamlit UI           |
+------------------------+
```

---

## 📂 Project Structure

```text id="proj001"
AI-EQUITY-RESEARCH-MULTIAGENT/
│
├── agents/
│   ├── valuation_agent.py
│   ├── risk_agent.py
│   ├── news_agent.py
│
├── scrapers/
│   ├── yahoo_scraper.py
│   ├── sec_scraper.py
│   ├── news_scraper.py
│
├── report_gen/
│   ├── generate_report.py
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🔌 Data Flow

```text id="flow001"
User Input (Ticker)
        ↓
Fetch Live Financial Data
        ↓
Fetch SEC Filing
        ↓
Fetch News Data
        ↓
Valuation Agent Analysis
        ↓
Risk Agent Analysis
        ↓
News Agent Analysis
        ↓
Report Generator
        ↓
Streamlit Dashboard Output
```

---

## 🛠 Tech Stack

| Layer       | Technology           |
| ----------- | -------------------- |
| Backend     | Python 3.11          |
| Market Data | yfinance             |
| Filings     | SEC EDGAR API        |
| News        | NewsAPI              |
| Parsing     | BeautifulSoup4       |
| LLM         | Groq (Llama 3.3 70B) |
| Frontend    | Streamlit            |
| Environment | python-dotenv        |

---

## 🚀 Setup & Running

### Prerequisites

* Python 3.11+
* Groq API Key
* NewsAPI Key

---

### 1. Clone Repository

```bash id="clone001"
git clone https://github.com/RajyavardhanS/AI-EQUITY-RESEARCH-MULTIAGENT.git
cd AI-EQUITY-RESEARCH-MULTIAGENT
```

---

### 2. Install Dependencies

```bash id="install001"
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create `.env`

```env id="env001"
GROQ_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

---

### 4. Run Application

```bash id="run001"
streamlit run app.py
```

Open:

```text id="url001"
http://localhost:8501
```

---

## 📊 Example Report Pipeline

Input:

```python id="input001"
ticker = "AAPL"
```

System fetches:

```text id="data001"
• Live stock metrics
• Latest 10-K filing
• Recent market news
```

Agents produce:

```text id="agents001"
• Valuation Thesis
• Risk Breakdown
• Sentiment Summary
```

Final Output:

```text id="output001"
Complete Equity Research Report
```

---

## 🚧 Engineering Challenges Solved

### Challenge 1 — SEC Filing Section Extraction

SEC filings contain repeated "Risk Factors" references.

Solved by:

* locating true structural Item 1A sections
* filtering false TOC matches

---

### Challenge 2 — LLM Provider Migration

Gemini free-tier quota failures.

Solution:

* migrated to Groq
* zero architecture rewrite required

---

### Challenge 3 — Token Rate Limits

Large 10-K filings exceeded token limits.

Solution:

* optimized chunk sizes
* selective section extraction

---

### Challenge 4 — Hallucination Prevention

LLM generated fake risks on irrelevant excerpts.

Solution:

* explicit failure prompting
* enforced “I don’t know” behavior

---

### Challenge 5 — News Relevance Filtering

Generic company names returned noisy results.

Solution:

* exact-phrase search
* relevance sorting

---

## ⚙️ Future Improvements

| Improvement               | Description                        |
| ------------------------- | ---------------------------------- |
| 📄 PDF Export             | Generate downloadable PDF reports  |
| 📊 Peer Benchmarking      | Compare against sector competitors |
| 🎙 Earnings Call Analysis | Parse transcripts                  |
| ⚡ Caching                 | Reduce repeated API calls          |
| 📦 Portfolio Analysis     | Multi-stock analysis               |
| 🧠 Better Risk Parsing    | Generalize across all SEC formats  |

---

## 🎯 Why This Project Matters

This project demonstrates:

* Multi-agent orchestration
* Financial AI systems
* LLM reliability engineering
* API integrations
* Prompt engineering
* Failure detection
* Production debugging
* Modular architecture

This is designed as a **real-world institutional equity research simulator**, not just a stock analysis app.

---



---
