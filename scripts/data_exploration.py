"""
basic_exploration.py

A minimal script for loading and inspecting network traffic data. This script:
1. Reads a CSV file (adjust the path if needed).
2. Prints a sample of the data (head).
3. Shows DataFrame info (column types, non-null counts).
4. Checks for missing values in each column.
5. Generates basic statistics for numerical columns.

Usage:
------
1. Make sure you have `pandas` installed:
   pip install pandas
2. Place this script in a folder (e.g., `scripts`) and ensure your CSV is in
   a directory such that '../data/network_data.csv' points to the file.
   Alternatively, update the `pd.read_csv()` path to match your setup.
3. Run:
   python -m scripts.basic_exploration

Notes:
------
- This script is intentionally lightweight, focusing on initial data checks.
- For a more in-depth exploratory analysis (including visualizations), refer to
  a more comprehensive script or notebook.
"""

import pandas as pd

# Use a relative import to pull in DATA_PATH from config.py
from .config import DATA_PATH

def main():
    """
    Main function to load and inspect the network traffic data.
    
    Steps:
    ------
    1. Load the CSV file into a DataFrame.
    2. Print the first few rows to understand the structure.
    3. Print DataFrame info (types, memory usage).
    4. Print missing values for each column.
    5. Generate basic statistics for numerical columns.
    """

    # 1. Load the network traffic data using DATA_PATH from config.py
    df = pd.read_csv(DATA_PATH)

    # 2. Display the first few rows to understand the structure
    print("=== First Few Rows of the Data ===")
    print(df.head())

    # 3. Get basic information about the dataset
    print("\n=== DataFrame Info ===")
    print(df.info())

    # 4. Check for missing values in each column
    print("\n=== Missing Values in Each Column ===")
    print(df.isnull().sum())

    # 5. Generate basic statistics for numerical columns
    print("\n=== Basic Statistical Summary ===")
    print(df.describe())

if __name__ == "__main__":
    main()
