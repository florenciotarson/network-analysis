"""
risk_analysis_2.py

This script highlights potential security risks in network traffic by checking for:
1. IP addresses with unusually high request counts (potential brute force or scanning).
2. Sessions with very large request sizes (potential data exfiltration).
3. Possible anomalies in the time distribution of requests (if a timestamp is present).

Usage:
------
1. Ensure you have `pandas` installed:
   pip install pandas

2. Adjust the CSV path if necessary. By default, it looks for:
   '../data/network_data.csv' (defined in config.py)

3. Run:
   python -m scripts.risk_analysis_2

Notes:
------
- This script is intentionally more focused on detecting suspicious activity 
  than on general exploratory analysis.
- Use its findings to inform your security policy or to investigate specific 
  IP addresses further.
"""

import pandas as pd

# Minimal change: relative import from .config
from .config import DATA_PATH


def main():
    """
    Main function to load data and check for potential security risks.

    Steps:
    ------
    1. Load the CSV into a DataFrame.
    2. Identify top IPs by request count.
    3. Check for unusually large request sizes.
    4. (Optional) Inspect time distribution if a timestamp column is present.
    """

    # 1. Load the network traffic data (from config.py instead of a hard-coded path)
    df = pd.read_csv(DATA_PATH)

    # Basic check: ensure we have rows to analyze
    if df.empty:
        print("No data found. Please verify the CSV file.")
        return

    # 2. Identify top IPs by request count
    if 'ClientIP' in df.columns:
        ip_counts = df['ClientIP'].value_counts().head(10)
        print("=== Top 10 IPs by Request Count ===")
        print(ip_counts)
        print()

        suspicious_ips = ip_counts[ip_counts > 100]
        if not suspicious_ips.empty:
            print("Suspicious IPs (more than 100 requests):")
            print(suspicious_ips)
            print()
    else:
        print("Warning: 'ClientIP' column not found; skipping IP-based checks.\n")

    # 3. Check for unusually large request sizes
    if 'ClientRequestBytes' in df.columns:
        high_threshold = df['ClientRequestBytes'].quantile(0.95)
        large_requests = df[df['ClientRequestBytes'] > high_threshold]
        print("=== Potentially Large Requests (above 95th percentile) ===")
        print(f"Threshold: {high_threshold}")
        print(f"Number of large requests: {len(large_requests)}\n")
    else:
        print("Warning: 'ClientRequestBytes' column not found; skipping size checks.\n")

    # 4. Inspect time distribution if a timestamp column is present
    if 'EdgeStartTimestamp' in df.columns:
        df['EdgeStartTimestamp'] = pd.to_datetime(
            df['EdgeStartTimestamp'],
            errors='coerce'
        )
        valid_times = df['EdgeStartTimestamp'].dropna()
        if not valid_times.empty:
            df['Hour'] = df['EdgeStartTimestamp'].dt.hour
            after_hours = df[(df['Hour'] < 8) | (df['Hour'] > 18)]
            print("=== After-Hours Requests ===")
            print(f"Total requests outside 8 AM-6 PM: {len(after_hours)}\n")
        else:
            print("No valid timestamps found. Skipping time-based checks.\n")
    else:
        print("Warning: 'EdgeStartTimestamp' column not found; "
              "skipping time-based checks.\n")

    print("=== Risk Analysis Complete ===")
    print("Consider investigating any flagged IPs, large requests, or after-hours spikes.")
    print("Use these findings to refine your security policy and incident response.\n")


if __name__ == "__main__":
    main()
