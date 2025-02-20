"""
risk_analysis.py

This module provides the perform_risk_analysis function, which checks a dataframe
for various security risks (e.g., high request counts, large request sizes,
and after-hours requests).
"""

import logging
import pandas as pd

# Importing threshold from config correctly
try:
    from scripts.config import SUSPICIOUS_IP_THRESHOLD
except ImportError:
    logging.warning(
        "Could not import SUSPICIOUS_IP_THRESHOLD from config. "
        "Using default value: 100"
    )
    SUSPICIOUS_IP_THRESHOLD = 100  # Default fallback


def perform_risk_analysis(df: pd.DataFrame) -> dict:
    """
    Perform risk analysis on the provided dataframe.
    Returns a dictionary with HTML-formatted risk findings.
    """
    results = {}

    # 🔹 Risk 1: High Request Count by IP
    if "ClientIP" in df.columns:
        ip_counts = df["ClientIP"].value_counts()
        suspicious_ips = ip_counts[ip_counts > SUSPICIOUS_IP_THRESHOLD]

        results["suspicious_ips"] = (
            suspicious_ips.to_frame(name="Request Count").to_html(
                classes="table table-bordered"
            )
        )
    else:
        results[
            "suspicious_ips"
        ] = "<p>'ClientIP' column not found. IP-based risk analysis skipped.</p>"

    # 🔹 Risk 2: Unusually Large Request Sizes
    if "ClientRequestBytes" in df.columns:
        high_threshold = df["ClientRequestBytes"].quantile(0.95)
        large_requests = df[df["ClientRequestBytes"] > high_threshold]

        results["large_requests"] = (
            f"<p>Threshold for large requests: {high_threshold:.2f}. "
            f"Number of large requests: {len(large_requests)}</p>"
        )
    else:
        results[
            "large_requests"
        ] = "<p>'ClientRequestBytes' column not found. Size-based risk analysis skipped.</p>"

    # 🔹 Risk 3: After-Hours Requests
    if "EdgeStartTimestamp" in df.columns:
        df["EdgeStartTimestamp"] = pd.to_datetime(
            df["EdgeStartTimestamp"], errors="coerce"
        )
        # Drop rows where timestamps are NaT (invalid date conversion)
        df = df.dropna(subset=["EdgeStartTimestamp"])
        df["Hour"] = df["EdgeStartTimestamp"].dt.hour
        after_hours = df[(df["Hour"] < 8) | (df["Hour"] > 18)]

        results["after_hours"] = (
            f"<p>Number of after-hours requests: {len(after_hours)}</p>"
        )
    else:
        results[
            "after_hours"
        ] = "<p>'EdgeStartTimestamp' column not found. Time-based risk analysis skipped.</p>"

    logging.info("Risk analysis completed successfully.")
    return results
