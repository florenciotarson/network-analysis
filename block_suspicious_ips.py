"""
This script blocks suspicious IPs using Windows Firewall.
It reads the 'suspicious_ips.csv' file and blocks each listed IP.
"""

import os
import subprocess
import pandas as pd

SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "blocked_ips.log"

# Check if the suspicious IP file exists
if not os.path.exists(SUSPICIOUS_IPS_FILE):
    print(f"Error: {SUSPICIOUS_IPS_FILE} not found! Please check the file path.")
    exit()

# Load the list of suspicious IPs
suspicious_ips_df = pd.read_csv(SUSPICIOUS_IPS_FILE)

# Print available columns for debugging
print("Available columns:", suspicious_ips_df.columns.tolist())

# Ensure column names have no spaces or hidden characters
suspicious_ips_df.columns = suspicious_ips_df.columns.str.strip()

# Define possible column names for IP addresses
POSSIBLE_COLUMNS = ["ip_address", "IP", "ClientIP", "SourceIP", "RemoteIP"]

# Identify the correct column name for IP addresses
# pylint: disable=invalid-name
correct_column_name = None

for col in suspicious_ips_df.columns:
    if col in POSSIBLE_COLUMNS:
        correct_column_name = col
        break

if not correct_column_name:
    print("Error: No valid IP address column found in CSV.")
    exit()

# Convert IPs to a list
suspicious_ip_list = suspicious_ips_df[correct_column_name].tolist()

def is_ip_blocked(ip_address):
    """Check if an IP is already blocked in Windows Firewall."""
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", f'name=Block_{ip_address}'],
            capture_output=True, text=True, check=True
        ).stdout
        return "No rules match" not in result
    except subprocess.CalledProcessError:
        return False

def block_ip(ip_address):
    """
    Function to block an IP using Windows Firewall.
    Prevents duplicate blocks.
    """
    if is_ip_blocked(ip_address):
        print(f"Skipping {ip_address} (already blocked).")
        return

    print(f"Blocking IP: {ip_address}")

    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f'name=Block_{ip_address}', "dir=in", "action=block",
            f"remoteip={ip_address}"
        ], shell=True, check=True)

        # Log the blocked IP
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{ip_address} blocked\n")

    except subprocess.CalledProcessError as e:
        print(f"Error blocking {ip_address}: {e}")

# Block each suspicious IP
for suspicious_ip in suspicious_ip_list:
    block_ip(suspicious_ip)

print("All suspicious IPs have been blocked.")
