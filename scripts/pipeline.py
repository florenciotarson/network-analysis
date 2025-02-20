"""
pipeline.py

This module orchestrates the data pipeline by:
1. Setting up logging.
2. Loading network traffic data from a CSV file.
3. Performing exploratory data analysis (EDA).
4. Performing risk analysis.
5. Generating an HTML report summarizing the findings.
"""

import logging
import pandas as pd

# Use relative imports (note the leading dot):
from .config import DATA_PATH
from .eda import perform_eda
from .risk_analysis import perform_risk_analysis
from .report_generator import generate_html_report

def load_data(file_path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load the network traffic data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded network traffic data.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully from %s", file_path)
        return df
    except FileNotFoundError as e:
        logging.error("File not found: %s", e)
        raise
    except Exception as e:
        logging.error("Error loading data: %s", e)
        raise

def main() -> None:
    """
    Main function to run the pipeline.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    logging.info("Starting the modular data pipeline.")

    # 1. Load the dataset
    df = load_data()

    # 2. Perform EDA
    eda_results = perform_eda(df)

    # 3. Perform risk analysis
    risk_results = perform_risk_analysis(df)

    # 4. Generate an HTML report
    report_file = "security_report.html"
    generate_html_report(eda_results, risk_results, report_file)
    logging.info("Report generated: %s", report_file)

if __name__ == "__main__":
    main()
