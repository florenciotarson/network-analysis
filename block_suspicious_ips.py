"""
This script blocks suspicious IPs using the firewall.
It reads the 'suspicious_ips.csv' file and blocks each listed IP.
"""

import os
import pandas as pd

SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "blocked_ips.log"

# Check if the suspicious IP file exists
if not os.path.exists(SUSPICIOUS_IPS_FILE):
    print(f"Error: {SUSPICIOUS_IPS_FILE} not found! Please check the file path.")
    exit()

# Load the list of suspicious IPs
suspicious_ips_df = pd.read_csv(SUSPICIOUS_IPS_FILE)

# Convert IPs to a list
suspicious_ip_list = suspicious_ips_df["ip_address"].tolist()

def is_ip_blocked(ip_address):
    """ Check if an IP is already blocked (Linux only) """
    result = os.popen(f"iptables -L INPUT -v -n | grep {ip_address}").read()
    return bool(result)

def block_ip(ip_address):
    """
    Function to block an IP using the system firewall.
    Prevents duplicate blocks.
    """
    if is_ip_blocked(ip_address):
        print(f"Skipping {ip_address} (already blocked).")
        return

    print(f"Blocking IP: {ip_address}")
    os.system(f"iptables -A INPUT -s {ip_address} -j DROP")  # Linux firewall rule

    # Log the blocked IP (Fixed Indentation)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{ip_address} blocked\n")  # Correctly indented


# Block each suspicious IP
for suspicious_ip in suspicious_ip_list:
    block_ip(suspicious_ip)

print("All suspicious IPs have been blocked.")
