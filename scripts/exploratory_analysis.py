"""
exploratory_analysis.py

This script performs an exploratory data analysis (EDA) on network traffic data.
It loads the data, checks for missing values or duplicates, converts timestamps,
and generates basic statistics and plots to help identify potential security risks.

Usage:
------
1. Install required dependencies:
   pip install pandas seaborn matplotlib

2. Ensure your dataset is inside a `data/` folder or update `config.py`.

3. Run:
   python -m scripts.exploratory_analysis
"""

import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🔹 Safe import of DATA_PATH from config.py
try:
    from scripts.config import DATA_PATH
except ImportError:
    logging.warning(
        "Could not import DATA_PATH from config. "
        "Using default path '../data/network_data.csv'."
    )
    DATA_PATH = "../data/network_data.csv"  # Default fallback

def main():
    """
    Main function to load, inspect, and visualize network traffic data.
    """

    # 1. Load the dataset with error handling
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Data file '{DATA_PATH}' not found. Please check the path.")
        return
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty. Please provide a valid dataset.")
        return
    except pd.errors.ParserError:
        print("Error: CSV parsing issue detected. Check the file format.")
        return
    except OSError:
        print("Error: Issue accessing the file. Check file permissions.")
        return

    # Basic check: ensure we have rows to analyze
    if df.empty:
        print("Warning: No data found in the CSV file. Skipping analysis.")
        return

    # 2. Display the first few rows to understand the structure
    print("\n=== First Few Rows of the Data ===")
    print(df.head(), "\n")

    # 3. Get basic information about the dataset
    print("\n=== DataFrame Info ===")
    print(df.info(), "\n")

    # 4. Check for missing values in each column
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("\n=== Missing Values in Each Column ===")
        print(missing_values[missing_values > 0], "\n")
    else:
        print("\nNo missing values detected.\n")

    # 5. Check for duplicate rows
    duplicates = df.duplicated().sum()
    print(f"\n=== Number of Duplicate Rows: {duplicates} ===\n")

    # 6. Convert timestamps if available
    if 'EdgeStartTimestamp' in df.columns:
        df['EdgeStartTimestamp'] = pd.to_datetime(
            df['EdgeStartTimestamp'], errors='coerce'
        )
        invalid_timestamps = df['EdgeStartTimestamp'].isna().sum()
        if invalid_timestamps > 0:
            print(f"\nWarning: {invalid_timestamps} rows have invalid timestamps.\n")

    # 7. Generate basic statistics for numerical columns
    print("\n=== Basic Statistical Summary (Numerical Columns) ===")
    print(df.describe())

    # 8. Visual Explorations
    # ----------------------

    # A) Distribution of ClientRequestBytes
    if 'ClientRequestBytes' in df.columns and df['ClientRequestBytes'].notna().any():
        plt.figure(figsize=(8, 5))
        sns.histplot(df['ClientRequestBytes'].dropna(), bins=50, kde=True)
        plt.title("Distribution of Client Request Bytes")
        plt.xlabel("Client Request Bytes")
        plt.ylabel("Count")
        plt.show()
    else:
        print("\n⚠ Skipping 'ClientRequestBytes' plot due to missing or invalid data.\n")

    # B) Top 10 Client Countries
    if 'ClientCountry' in df.columns and df['ClientCountry'].notna().any():
        top_countries = df['ClientCountry'].value_counts().head(10)
        plt.figure(figsize=(8, 5))
        sns.barplot(x=top_countries.index, y=top_countries.values)
        plt.title("Top 10 Client Countries")
        plt.xticks(rotation=45)
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()
    else:
        print("\n⚠ Skipping 'ClientCountry' plot due to missing or invalid data.\n")

    # C) Requests Over Time (Hourly)
    if 'EdgeStartTimestamp' in df.columns and df['EdgeStartTimestamp'].notna().any():
        df = df.sort_values('EdgeStartTimestamp')
        df.set_index('EdgeStartTimestamp', inplace=True)
        hourly_counts = df.resample('H').size()

        if not hourly_counts.empty:
            plt.figure(figsize=(10, 5))
            hourly_counts.plot()
            plt.title("Requests per Hour")
            plt.xlabel("Time (Hourly)")
            plt.ylabel("Number of Requests")
            plt.show()
        else:
            print("\n⚠ Not enough timestamp data for time series analysis.\n")

        # Reset index for further non-time-based analysis
        df.reset_index(inplace=True)
    else:
        print("\n⚠ Skipping time series analysis due to missing timestamps.\n")

    # Conclusion
    print("\nAnalysis Complete")
    print("Review the printed outputs and generated plots for insights.")
    print("Consider how anomalies or unusual patterns might pose security risks.\n")

if __name__ == "__main__":
    main()
