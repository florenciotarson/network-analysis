"""
report_generator.py

This module provides functionality to generate an HTML report that consolidates
exploratory data analysis (EDA) results and risk analysis findings into a single
HTML document.
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any

def generate_html_report(
    eda_results: Dict[str, Any],
    risk_results: Dict[str, Any],
    output_file: str = "security_report.html"
) -> None:
    """
    Generate an HTML report including EDA results and risk analysis.

    Args:
        eda_results (Dict[str, Any]): 
            A dictionary containing EDA results, including:
              - 'summary': HTML table of DataFrame.describe()
              - 'missing': HTML table showing missing values
              - 'duplicates': A simple HTML string with the count of duplicates
              - 'plot1', 'plot2', 'plot3': Paths to saved plot images (if any).
        risk_results (Dict[str, Any]):
            A dictionary containing identified security risks, such as:
              - 'suspicious_ips': HTML table of IPs exceeding a request threshold
              - 'large_requests': HTML snippet describing large request findings
              - 'after_hours': HTML snippet for requests made after normal
                business hours.
        output_file (str, optional):
            The name (and path) of the output HTML file. Defaults to 
            "security_report.html".

    Raises:
        OSError: If an error occurs while writing the HTML file.

    Returns:
        None
    """

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # HTML Content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Security Analysis Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f9f9f9;
            }}
            h1, h2 {{
                color: #2C3E50;
            }}
            h2 {{
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }}
            .section {{
                margin-bottom: 40px;
                background-color: #fff;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .plot {{
                max-width: 100%;
                height: auto;
                margin-bottom: 20px;
                border: 1px solid #ddd;
            }}
            .timestamp {{
                font-size: 14px;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <h1>Security Analysis Report</h1>
        <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="section">
            <h2>1. Data Summary</h2>
            {eda_results.get('summary', '<p>No summary available.</p>')}
        </div>
        
        <div class="section">
            <h2>2. Missing Values</h2>
            {eda_results.get('missing', '<p>No missing values info available.</p>')}
        </div>
        
        <div class="section">
            <h2>3. Duplicate Rows</h2>
            {eda_results.get('duplicates', '<p>No duplicate information available.</p>')}
        </div>
        
        <div class="section">
            <h2>4. Visual Explorations</h2>
            
            <h3>Distribution of Client Request Bytes</h3>
            {f"<img src='{eda_results['plot1']}' class='plot'>" if eda_results.get('plot1') and os.path.exists(eda_results['plot1']) else "<p>Plot not available.</p>"}
            
            <h3>Top 10 Client Countries</h3>
            {f"<img src='{eda_results['plot2']}' class='plot'>" if eda_results.get('plot2') and os.path.exists(eda_results['plot2']) else "<p>Plot not available.</p>"}
            
            <h3>Requests per Hour</h3>
            {f"<img src='{eda_results['plot3']}' class='plot'>" if eda_results.get('plot3') and os.path.exists(eda_results['plot3']) else "<p>Plot not available.</p>"}
        </div>
        
        <div class="section">
            <h2>5. Risk Analysis</h2>
            
            <h3>Suspicious IPs</h3>
            {risk_results.get('suspicious_ips', '<p>No IP risk analysis available.</p>')}
            
            <h3>Large Request Sizes</h3>
            {risk_results.get('large_requests', '<p>No size risk analysis available.</p>')}
            
            <h3>After-Hours Requests</h3>
            {risk_results.get('after_hours', '<p>No time-based risk analysis available.</p>')}
        </div>
    </body>
    </html>
    """

    # Save the HTML report
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info(" HTML report generated successfully at '%s'.", output_file)
    except OSError as e:
        logging.error(" Error generating HTML report: %s", e)
        raise
