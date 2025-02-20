"""
This script analyzes network traffic logs and detects "suspicious" IPs.
If an IP makes too many requests, it gets flagged as suspicious.
"""

import pandas as pd

# Load the dataset (Replace 'network_data.csv' with your actual file path)
df = pd.read_csv("network_data.csv")

# Define a threshold for suspicious behavior (More than 1000 requests)
REQUEST_THRESHOLD = 1000  # Fixed naming convention for constants

# Find IPs that exceed the limit
suspicious_traffic = df[df["request_count"] > REQUEST_THRESHOLD]

# Display suspicious IPs
print("Suspicious IPs detected:")
print(suspicious_traffic[["ip_address", "request_count"]])

# Save the suspicious IPs to a file for later use
suspicious_traffic[["ip_address"]].to_csv("suspicious_ips.csv", index=False)
