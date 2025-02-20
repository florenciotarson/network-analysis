"""
exploratory_analysis.py

This script performs an exploratory data analysis (EDA) on network traffic data. 
It loads the data, checks for missing values or duplicates, converts timestamps, 
and generates basic statistics and plots to help identify potential security risks.

Usage:
------
1. Make sure you have `pandas`, `seaborn`, and `matplotlib` installed:
   pip install pandas seaborn matplotlib

2. Place this script in your 'scripts' folder (or adjust the path to your CSV
   accordingly). If your CSV is in a folder named 'data' at the same level, then
   the path from config.py will be used.

3. From your project's root directory, run:
   python -m scripts.exploratory_analysis

Notes:
------
- Identifying suspicious IPs or countries with unusual request volumes can
  highlight potential malicious scanning or attacks.
- Large or abnormal request sizes could indicate data exfiltration attempts.
- Unusual spikes in traffic over time might point to DDoS attacks or other anomalies.

After running this script:
- Review the console output for DataFrame info, missing values, duplicates, 
  and basic stats.
- Inspect the generated plots (histogram, bar chart, time series) for any red flags.
- Use these findings to inform a security policy in a separate script or notebook.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Use a relative import to pull in DATA_PATH from config.py
# (Requires __init__.py in the same folder so Python treats 'scripts' as a package)
from .config import DATA_PATH

def main():
    """
    Main function to load, inspect, and visualize network traffic data.

    Steps:
    ------
    1. Load Data:
       - Reads the network traffic CSV (using the path defined in config.py).
    2. Basic Inspection:
       - Prints a sample of rows (head), info about data types, missing values, 
         and duplicates.
    3. Timestamp Conversion:
       - Converts 'EdgeStartTimestamp' to a datetime object if present.
    4. Statistical Summary:
       - Generates basic stats for numerical columns.
    5. Visual Explorations:
       - Distribution of 'ClientRequestBytes' to spot potential outliers or 
         abnormal usage.
       - Bar plot of top 10 'ClientCountry' entries to identify geographic patterns.
       - Time series analysis (requests per hour) if timestamps are valid.
    """

    # 1. Load the network traffic data using the constant from config.py
    df = pd.read_csv(DATA_PATH)

    # 2. Display the first few rows to understand the structure
    print("=== First Few Rows of the Data ===")
    print(df.head())

    # Get basic information about the dataset
    print("\n=== DataFrame Info ===")
    print(df.info())

    # Check for missing values in each column
    print("\n=== Missing Values in Each Column ===")
    print(df.isnull().sum())

    # Check for duplicate rows (often important in network logs)
    duplicates = df.duplicated().sum()
    print(f"\n=== Number of Duplicate Rows: {duplicates} ===")

    # 3. Convert timestamps to datetime (if you have a timestamp column)
    if 'EdgeStartTimestamp' in df.columns:
        df['EdgeStartTimestamp'] = pd.to_datetime(
            df['EdgeStartTimestamp'],
            errors='coerce'
        )
        invalid_timestamps = df['EdgeStartTimestamp'].isna().sum()
        print(f"\n=== Rows with Invalid Timestamps: {invalid_timestamps} ===")

    # 4. Generate basic statistics for numerical columns
    print("\n=== Basic Statistical Summary (Numerical Columns) ===")
    print(df.describe())

    # 5. Visual Explorations
    # ----------------------

    # A) Distribution of ClientRequestBytes
    if 'ClientRequestBytes' in df.columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df['ClientRequestBytes'], bins=50, kde=True)
        plt.title("Distribution of Client Request Bytes")
        plt.xlabel("ClientRequestBytes")
        plt.ylabel("Count")
        plt.show()

    # B) Top 10 Client Countries
    if 'ClientCountry' in df.columns:
        top_countries = (
            df['ClientCountry']
            .value_counts()
            .head(10)
        )
        plt.figure(figsize=(8, 5))
        sns.barplot(x=top_countries.index, y=top_countries.values)
        plt.title("Top 10 Client Countries")
        plt.xticks(rotation=45)
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    # C) Requests Over Time (Hourly)
    if 'EdgeStartTimestamp' in df.columns and df['EdgeStartTimestamp'].notna().any():
        df.sort_values('EdgeStartTimestamp', inplace=True)
        df.set_index('EdgeStartTimestamp', inplace=True)
        hourly_counts = df.resample('H').size()

        plt.figure(figsize=(10, 5))
        hourly_counts.plot()
        plt.title("Requests per Hour")
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Number of Requests")
        plt.show()

        # Reset index if you need to do further non-time-based analysis
        df.reset_index(inplace=True)

    # Conclusion
    print("\n=== Analysis Complete ===")
    print("Review the printed outputs and generated plots for insights.")
    print("Consider how anomalies or unusual patterns might pose security risks.")
    print("Next, you can develop a security policy to address these findings.\n")

if __name__ == "__main__":
    main()
