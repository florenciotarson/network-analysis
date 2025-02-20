"""
This script blocks suspicious IPs using the firewall.
It reads the 'suspicious_ips.csv' file and blocks each listed IP.
"""

import os
import pandas as pd

# Load the list of suspicious IPs detected earlier
suspicious_ips_df = pd.read_csv("suspicious_ips.csv")

# Convert IPs to a list
suspicious_ip_list = suspicious_ips_df["ip_address"].tolist()

def block_ip(ip_address):
    """
    Function to block an IP using the system firewall.
    This works on Linux using 'iptables'. For Windows, you need to adjust the command.
    """
    print(f"Blocking IP: {ip_address}")
    os.system(f"iptables -A INPUT -s {ip_address} -j DROP")  # Linux firewall rule

# Block each suspicious IP
for suspicious_ip in suspicious_ip_list:
    block_ip(suspicious_ip)

print("All suspicious IPs have been blocked.")
