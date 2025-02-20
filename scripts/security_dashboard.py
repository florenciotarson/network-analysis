"""
Security Dashboard for Network Traffic Analysis

This script creates a Streamlit-based dashboard to analyze:
- Suspicious network traffic
- Large data requests
- After-hours activities

Run with:
    streamlit run security_dashboard.py
"""

# ---- IMPORTS AND STREAMLIT PAGE CONFIG (Must be the first Streamlit command) ----
import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Security Risk Dashboard", layout="wide")

# ---- PATH CONFIGURATION ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "network_data.csv")
SUSPICIOUS_THRESHOLD = 100  # Customize threshold

# ---- ERROR HANDLING: Check if File Exists ----
if not os.path.exists(DATA_PATH):
    st.error(f"Error: Data file not found at `{DATA_PATH}`. Please upload `network_data.csv`.")
    st.stop()  # Stop execution if file is missing

@st.cache_data
def load_data():
    """ Load dataset from CSV file """
    return pd.read_csv(DATA_PATH)

# Load data once
df = load_data()

# ---- HEADER ----
st.title("Security Risk Analysis Dashboard")
st.markdown(
    """
    **This dashboard provides insights into:**
    - Suspicious network traffic
    - Large data requests
    - After-hours activities
    """
)

# ---- DATA OVERVIEW ----
st.subheader("Data Summary")
st.write(df.describe())

# ---- SUSPICIOUS IPs ----
st.subheader("Suspicious IPs")
ip_counts = df["ClientIP"].value_counts()
suspicious_ips = ip_counts[ip_counts > SUSPICIOUS_THRESHOLD]

if suspicious_ips.empty:
    st.success("No suspicious IPs detected.")
else:
    st.warning(
        f"Found `{len(suspicious_ips)}` suspicious IPs exceeding `{SUSPICIOUS_THRESHOLD}` requests."
    )
    st.dataframe(
        suspicious_ips.to_frame()
        .reset_index()
        .rename(columns={"index": "ClientIP", "ClientIP": "Request Count"})
    )

# ---- LARGE REQUESTS ----
st.subheader("Large Request Sizes")
if "ClientRequestBytes" in df.columns:
    large_requests_threshold = df["ClientRequestBytes"].quantile(0.95)
    large_requests = df[df["ClientRequestBytes"] > large_requests_threshold]

    fig = px.histogram(
        df,
        x="ClientRequestBytes",
        nbins=50,
        title="Distribution of Client Request Bytes",
        log_x=True
    )
    st.plotly_chart(fig)

    st.markdown(
        f"""
        - **Threshold for large requests:** `{large_requests_threshold:.2f}`
        - **Total large requests:** `{len(large_requests)}`"""
    )

# ---- AFTER-HOURS REQUESTS ----
st.subheader("After-Hours Requests")
if "EdgeStartTimestamp" in df.columns:
    df["EdgeStartTimestamp"] = pd.to_datetime(df["EdgeStartTimestamp"], errors="coerce")
    df["Hour"] = df["EdgeStartTimestamp"].dt.hour
    after_hours = df[(df["Hour"] < 8) | (df["Hour"] > 18)]

    fig = px.line(
        df,
        x="EdgeStartTimestamp",
        y=df.index,
        title="Requests Over Time (After-Hours Highlighted)"
    )
    st.plotly_chart(fig)

    st.markdown(f"**Total after-hours requests:** `{len(after_hours)}`")

# ---- TOP CLIENT COUNTRIES ----
st.subheader("Top 10 Client Countries")
if "ClientCountry" in df.columns:
    top_countries = df["ClientCountry"].value_counts().head(10)

    fig = px.bar(
        top_countries,
        x=top_countries.index,
        y=top_countries.values,
        title="Top 10 Client Countries"
    )
    st.plotly_chart(fig)

# ---- EXPORT REPORT ----
st.subheader("Export Report")
if st.button("Generate Security Report"):
    df.to_csv("security_report.csv", index=False)
    st.success("Security report generated successfully!")
