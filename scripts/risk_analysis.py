"""
risk_analysis.py

This module provides the perform_risk_analysis function, which checks a dataframe
for various security risks (e.g., high request counts, large request sizes,
and after-hours requests).
"""

import logging
import os
import pandas as pd


# Import configuration values safely
try:
    from scripts.config import DATA_PATH, SUSPICIOUS_IP_THRESHOLD
except ImportError:
    logging.warning(
        "Could not import config values from scripts.config. "
        "Using default values."
    )
    DATA_PATH = "data/network_data.csv"
    SUSPICIOUS_IP_THRESHOLD = 100  # Default fallback


def perform_risk_analysis(data: pd.DataFrame) -> dict:
    """
    Perform risk analysis on the provided dataframe.
    Returns a dictionary with formatted risk findings.
    """
    risk_results = {}

    # Ensure we are not modifying the original dataframe
    df_copy = data.copy()

    # Risk 1: High Request Count by IP
    if "ClientIP" in df_copy.columns:
        ip_counts = df_copy["ClientIP"].value_counts()
        suspicious_ips = ip_counts[ip_counts > SUSPICIOUS_IP_THRESHOLD]

        if not suspicious_ips.empty:
            risk_results["suspicious_ips"] = (
                suspicious_ips.to_frame(name="Request Count")
            )
        else:
            risk_results["suspicious_ips"] = "No suspicious IPs detected."
    else:
        risk_results["suspicious_ips"] = (
            "Column 'ClientIP' not found. Skipping IP analysis."
        )

    # Risk 2: Unusually Large Request Sizes
    if "ClientRequestBytes" in df_copy.columns:
        try:
            high_threshold = df_copy["ClientRequestBytes"].quantile(0.95)
            large_requests = df_copy[df_copy["ClientRequestBytes"] > high_threshold]

            risk_results["large_requests"] = (
                f"Threshold: {high_threshold:.2f}. "
                f"Large requests: {len(large_requests)}"
            )
        except ValueError:
            risk_results["large_requests"] = (
                "Error processing 'ClientRequestBytes'. Check data integrity."
            )
    else:
        risk_results["large_requests"] = (
            "Column 'ClientRequestBytes' not found. Skipping size analysis."
        )

    # Risk 3: After-Hours Requests
    if "EdgeStartTimestamp" in df_copy.columns:
        try:
            df_copy["EdgeStartTimestamp"] = pd.to_datetime(
                df_copy["EdgeStartTimestamp"], errors="coerce"
            )
            df_copy = df_copy.dropna(subset=["EdgeStartTimestamp"])  # Drop invalid timestamps
            df_copy["Hour"] = df_copy["EdgeStartTimestamp"].dt.hour
            after_hours = df_copy[(df_copy["Hour"] < 8) | (df_copy["Hour"] > 18)]

            risk_results["after_hours"] = (
                f"After-hours requests: {len(after_hours)}"
            )
        except ValueError:
            risk_results["after_hours"] = (
                "Error processing timestamps. Check data format."
            )
    else:
        risk_results["after_hours"] = (
            "Column 'EdgeStartTimestamp' not found. Skipping time analysis."
        )

    logging.info("Risk analysis completed successfully.")
    return risk_results


if __name__ == "__main__":
    # Ensure the dataset exists
    if not os.path.exists(DATA_PATH):
        logging.error(
            "Error: Data file not found at %s. "
            "Check the file path.", DATA_PATH
        )
    else:
        try:
            network_data = pd.read_csv(DATA_PATH)

            if network_data.empty:
                logging.warning(
                    "Dataset is empty. Ensure the CSV file contains data."
                )
            else:
                analysis_results = perform_risk_analysis(network_data)

                print("\n" + "=" * 50)
                print(" RISK ANALYSIS SUMMARY")
                print("=" * 50)

                # Display suspicious IPs
                if isinstance(analysis_results["suspicious_ips"], pd.DataFrame):
                    print("\nSuspicious IPs (Above Threshold)")
                    print("-" * 50)
                    print(analysis_results["suspicious_ips"].to_string(index=False))
                else:
                    print("\nSuspicious IPs:", analysis_results["suspicious_ips"])

                # Display large request sizes
                print("\nLarge Requests")
                print("-" * 50)
                print(analysis_results["large_requests"])

                # Display after-hours activity
                print("\nAfter-Hours Requests")
                print("-" * 50)
                print(analysis_results["after_hours"])

                print("\nAnalysis complete. Review findings and investigate flagged issues.\n")

        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            logging.error(
                "Error reading the data file: %s", str(e)
            )
        except pd.errors.ParserError:
            logging.error(
                "Error parsing the CSV file. Ensure it is formatted correctly."
            )
