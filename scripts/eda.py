"""
eda.py

This module provides the perform_eda function, which executes exploratory data
analysis on a given DataFrame, generating statistics and saving plot images.
"""

import os
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Use a relative import to pull in PLOTS_DIR from config.py
from .config import PLOTS_DIR  # Import the plots directory constant

# Set a consistent theme for visuals
sns.set_theme(style="whitegrid")

def perform_eda(df):
    """
    Perform exploratory data analysis on the provided dataframe.
    Returns a dictionary with summary statistics and paths to generated figures.
    """
    results = {}

    # Data Summary as an HTML table
    results['summary'] = df.describe().to_html(classes='table table-striped')

    # Missing values summary as HTML
    missing_html = (
        df.isnull()
          .sum()
          .to_frame(name="Missing Values")
          .to_html(classes="table table-bordered")
    )
    # Store the missing values table in the results dictionary
    results['missing'] = missing_html

    # Duplicate rows count as HTML snippet
    duplicates_count = df.duplicated().sum()
    results['duplicates'] = f"<p>Duplicate rows: {duplicates_count}</p>"

    # Convert timestamp if available
    if 'EdgeStartTimestamp' in df.columns:
        df['EdgeStartTimestamp'] = pd.to_datetime(
            df['EdgeStartTimestamp'],
            errors='coerce'
        )

    # Create directory for saving plots if it doesn't exist (using constant)
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    # Plot 1: Distribution of Client Request Bytes
    if 'ClientRequestBytes' in df.columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df['ClientRequestBytes'], bins=50, kde=True, color="skyblue")
        plt.title("Distribution of Client Request Bytes")
        plt.xlabel("Client Request Bytes")
        plt.ylabel("Count")
        plot1_path = os.path.join(PLOTS_DIR, "client_request_bytes.png")
        plt.savefig(plot1_path, bbox_inches="tight")
        plt.close()
        results['plot1'] = plot1_path
    else:
        results['plot1'] = "Not available"

    # Plot 2: Top 10 Client Countries
    if 'ClientCountry' in df.columns:
        top_countries = df['ClientCountry'].value_counts().head(10)
        plt.figure(figsize=(8, 5))
        sns.barplot(x=top_countries.index, y=top_countries.values, palette="viridis")
        plt.title("Top 10 Client Countries")
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot2_path = os.path.join(PLOTS_DIR, "top_client_countries.png")
        plt.savefig(plot2_path, bbox_inches="tight")
        plt.close()
        results['plot2'] = plot2_path
    else:
        results['plot2'] = "Not available"

    # Plot 3: Requests Over Time (Hourly)
    if 'EdgeStartTimestamp' in df.columns and df['EdgeStartTimestamp'].notna().any():
        df.sort_values('EdgeStartTimestamp', inplace=True)
        df.set_index('EdgeStartTimestamp', inplace=True)
        hourly_counts = df.resample('H').size()
        plt.figure(figsize=(10, 5))
        hourly_counts.plot(color="teal")
        plt.title("Requests per Hour")
        plt.xlabel("Time (Hourly)")
        plt.ylabel("Number of Requests")
        plot3_path = os.path.join(PLOTS_DIR, "requests_per_hour.png")
        plt.savefig(plot3_path, bbox_inches="tight")
        plt.close()
        df.reset_index(inplace=True)
        results['plot3'] = plot3_path
    else:
        results['plot3'] = "Not available"

    logging.info("EDA completed successfully.")
    return results
