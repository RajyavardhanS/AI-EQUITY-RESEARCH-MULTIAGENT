import streamlit as st
from report_gen.markdown_report import generate_report

st.set_page_config(page_title="AI Based Equity Research Multi-Agent", page_icon="📊", layout="wide")

st.title("📊 AI Based Equity Research Multi-Agent")
st.markdown("AI-powered equity research reports in seconds.")

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Stock Ticker", placeholder="e.g. AAPL")
with col2:
    company_name = st.text_input("Company Name", placeholder="e.g. Apple Inc")
with col3:
    peers_input = st.text_input("Peer Tickers (optional)", placeholder="e.g. MSFT,GOOGL")

if st.button("Generate Report", type="primary"):
    if not ticker or not company_name:
        st.error("Please enter both ticker and company name.")
    else:
        peers = [p.strip() for p in peers_input.split(",")] if peers_input.strip() else []
        with st.spinner("Running AI Based Equity Research Multi-Agent... fetching data + running 3 AI agents (30-60 seconds)"):
            try:
                report = generate_report(ticker.upper(), company_name, peers)
                st.session_state.report = report
                st.session_state.ticker = ticker.upper()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "report" in st.session_state:
    st.divider()
    st.markdown(st.session_state.report)
    st.download_button(
        label="⬇️ Download Report",
        data=st.session_state.report,
        file_name=f"{st.session_state.ticker}_report.md",
        mime="text/markdown"
    )