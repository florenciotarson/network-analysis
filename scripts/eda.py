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

# 🔹 Try importing PLOTS_DIR from config.py safely
try:
    from scripts.config import PLOTS_DIR
except ImportError:
    logging.warning("Could not import PLOTS_DIR from config. Using default 'plots'.")
    PLOTS_DIR = "plots"  # Default fallback

# Set a consistent theme for visuals
sns.set_theme(style="whitegrid")

def perform_eda(df: pd.DataFrame) -> dict:
    """
    Perform exploratory data analysis on the provided dataframe.
    Returns a dictionary with summary statistics and paths to generated figures.
    """
    results = {}

    if df.empty:
        logging.warning("The DataFrame is empty. No EDA performed.")
        return {"error": "The dataset is empty. No analysis performed."}

    # Data Summary as an HTML table
    results['summary'] = df.describe().to_html(classes='table table-striped')

    # Missing values summary as HTML
    missing_values = df.isnull().sum()
    results['missing'] = (
        missing_values
        .to_frame(name="Missing Values")
        .to_html(classes="table table-bordered")
    )

    # Duplicate rows count
    duplicates_count = df.duplicated().sum()
    results['duplicates'] = f"<p>Duplicate rows: {duplicates_count}</p>"

    # Convert timestamp if available
    if 'EdgeStartTimestamp' in df.columns:
        df['EdgeStartTimestamp'] = pd.to_datetime(df['EdgeStartTimestamp'], errors='coerce')

    # Create directory for saving plots if it doesn't exist
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Plot 1: Distribution of Client Request Bytes
    if 'ClientRequestBytes' in df.columns and df['ClientRequestBytes'].notna().any():
        plt.figure(figsize=(8, 5))
        sns.histplot(df['ClientRequestBytes'].dropna(), bins=50, kde=True, color="skyblue")
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
    if 'ClientCountry' in df.columns and df['ClientCountry'].notna().any():
        top_countries = df['ClientCountry'].value_counts().head(10)
        plt.figure(figsize=(8, 5))
        # Assign x variable to hue and disable dodging and legend to avoid the FutureWarning.
        sns.barplot(
            x=top_countries.index,
            y=top_countries.values,
            hue=top_countries.index,
            palette="viridis",
            dodge=False,
            legend=False
        )
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

        hourly_counts = df.resample('h').size()
        if not hourly_counts.empty:
            plt.figure(figsize=(10, 5))
            hourly_counts.plot(color="teal")
            plt.title("Requests per Hour")
            plt.xlabel("Time (Hourly)")
            plt.ylabel("Number of Requests")
            plot3_path = os.path.join(PLOTS_DIR, "requests_per_hour.png")
            plt.savefig(plot3_path, bbox_inches="tight")
            plt.close()
            results['plot3'] = plot3_path
        else:
            results['plot3'] = "No data available for hourly requests."

        df.reset_index(inplace=True)
    else:
        results['plot3'] = "Not available"

    logging.info("EDA completed successfully.")
    return results
