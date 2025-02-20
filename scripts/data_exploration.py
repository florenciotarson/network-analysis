"""
data_exploration.py

Minimal script for loading and inspecting network traffic data.
"""

import logging
import pandas as pd

try:
    from scripts.config import DATA_PATH
except ImportError:
    logging.warning(
        "Could not import DATA_PATH from config. Using default path '../data/network_data.csv'."
    )
    DATA_PATH = "../data/network_data.csv"  # Default fallback

def main():
    """
    Main function to load and inspect the network traffic data.
    """

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
    except pd.errors.DtypeWarning:
        print("Error: Potential datatype issue. Consider reviewing column formats.")
        return
    except OSError:
        print("Error: Issue accessing the file. Check permissions.")
        return

    if df.empty:
        print("No data found. Please verify the CSV file.")
        return

    print("=== First Few Rows of the Data ===")
    print(df.head(), "\n")

    print("=== DataFrame Info ===")
    print(df.info(), "\n")

    print("=== Missing Values in Each Column ===")
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0], "\n")

    print("=== Basic Statistical Summary ===")
    print(df.describe())

if __name__ == "__main__":
    main()
