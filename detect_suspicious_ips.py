"""
This script analyzes network traffic logs and detects "suspicious" IPs.
If an IP makes too many requests, it gets flagged as suspicious.
"""
import os
import pandas as pd

# Define file paths
DATA_FILE = "data/network_data.csv"
SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "suspicious_activity.log"

# Check if the network data file exists
if not os.path.exists(DATA_FILE):
    print(f"Error: {DATA_FILE} not found! Please check the file path.")
    exit()

# Load dataset
df = pd.read_csv(DATA_FILE)

# Print column names to check structure
print("CSV Columns:", df.columns.tolist())

# Count the number of requests per IP
df_counted = df.groupby("ClientIP").size().reset_index(name="request_count")

# Define a threshold for suspicious behavior (More than 1000 requests)
REQUEST_THRESHOLD = 1000

# Find IPs that exceed the threshold
suspicious_traffic = df_counted[df_counted["request_count"] > REQUEST_THRESHOLD]

# Display and log suspicious IPs
with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write("\nSuspicious IPs detected:\n")
    for index, row in suspicious_traffic.iterrows():
        log_entry = f"{row['ClientIP']} - {row['request_count']} requests\n"
        print(log_entry.strip())  # Print to console
        log.write(log_entry)

# Save the suspicious IPs to a file for later use
suspicious_traffic[["ClientIP"]].to_csv(SUSPICIOUS_IPS_FILE, index=False)

print(f"Suspicious IPs saved to {SUSPICIOUS_IPS_FILE}")
