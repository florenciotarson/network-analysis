"""
This script analyzes network traffic logs and detects "suspicious" IPs.
If an IP makes too many requests, it gets flagged as suspicious.
"""
import os
import pandas as pd

# Define file paths
DATA_FILE = "network_data.csv"
SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "suspicious_activity.log"

# Check if the network data file exists
if not os.path.exists(DATA_FILE):
    print(f"Error: {DATA_FILE} not found! Please check the file path.")
    exit()

# Load the dataset
df = pd.read_csv(DATA_FILE)

# Define a threshold for suspicious behavior (More than 1000 requests)
REQUEST_THRESHOLD = 1000

# Find IPs that exceed the limit
suspicious_traffic = df[df["request_count"] > REQUEST_THRESHOLD]

# Display and log suspicious IPs
with open(LOG_FILE, "a", encoding="utf-8") as log:  #  Fixed encoding issue
    log.write("\nSuspicious IPs detected:\n")
    for index, row in suspicious_traffic.iterrows():
        log_entry = f"{row['ip_address']} - {row['request_count']} requests\n"
        print(log_entry.strip())  # Print to console
        log.write(log_entry)

# Save the suspicious IPs to a file for later use
suspicious_traffic[["ip_address"]].to_csv(SUSPICIOUS_IPS_FILE, index=False)

print(f"Suspicious IPs saved to {SUSPICIOUS_IPS_FILE}")
