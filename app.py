import sys
sys.path.append(".")

import streamlit as st
from report_gen.markdown_report import generate_report

st.set_page_config(page_title="Equity Research Agent", page_icon="📊", layout="wide")

st.title("📊 AI Equity Research Agent")
st.markdown("Generate an AI-powered equity research report for any public company.")

col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Stock Ticker", placeholder="e.g. AAPL")
with col2:
    company_name = st.text_input("Company Name", placeholder="e.g. Apple Inc")

if st.button("Generate Report", type="primary"):
    if not ticker or not company_name:
        st.error("Please enter both ticker and company name.")
    else:
        with st.spinner("Generating report... this takes 30-60 seconds (fetching data + running 3 AI agents)"):
            try:
                report = generate_report(ticker.upper(), company_name)
                st.session_state.report = report
                st.session_state.ticker = ticker.upper()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "report" in st.session_state:
    st.divider()
    st.markdown(st.session_state.report)

    st.download_button(
        label="Download Report (Markdown)",
        data=st.session_state.report,
        file_name=f"{st.session_state.ticker}_report.md",
        mime="text/markdown"
    )