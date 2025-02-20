
## Available Translations
- 🇬🇧 English (Current)
- 🇧🇷 [Portuguese](network_security_scripts_pt-br.md)

# Network Security Scripts Documentation

## Overview
This documentation provides an explanation of three key scripts used in a network security system.  
Each script has a specific role: monitoring network traffic, detecting suspicious IPs, and blocking malicious IPs.

---

## 1. Network Monitoring Script (`network_monitor.py`)

### Purpose
- This script monitors network traffic in real-time.
- It logs detected packets, recording their source, destination, and size.
- It acts as a security camera watching all the network activity.

### How It Works
- Uses Scapy to sniff packets from the network.
- If a packet contains an IP layer, it logs its details.
- Stores all packet logs in a file: `packet_log.txt`.

### Code Explanation
```python
from datetime import datetime
from scapy.all import sniff
from scapy.layers.inet import IP

LOG_FILE = "packet_log.txt"

def monitor_packet(packet):
    """
    Analyzes network packets and logs detected IP traffic.
    """
    if packet.haslayer(IP):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        packet_size = len(packet)

        log_entry = (
            f"[{timestamp}] Packet detected: {src_ip} -> {dst_ip} "
            f"| Size: {packet_size} bytes\n"
        )

        print(log_entry.strip())  # Print to console

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_entry)

print("Starting real-time network monitoring...")
sniff(prn=monitor_packet, store=False, filter="ip")  # Captures only IP packets
```

### Output Example
```
[2024-02-20 10:30:45] Packet detected: 192.168.1.10 -> 8.8.8.8 | Size: 64 bytes
[2024-02-20 10:30:47] Packet detected: 192.168.1.20 -> 192.168.1.1 | Size: 128 bytes
```

---

## 2. Suspicious IP Detection Script (`detect_suspicious_ips.py`)

### Purpose
- This script analyzes network logs to find suspicious IPs.
- If an IP makes too many requests, it gets flagged.
- Stores suspicious IPs in a file: `suspicious_ips.csv`.

### How It Works
- Loads network traffic data from `network_data.csv`.
- Defines a request threshold (e.g., more than 1000 requests is suspicious).
- Filters out IPs exceeding the threshold and logs them.

### Code Explanation
```python
import os
import pandas as pd

DATA_FILE = "network_data.csv"
SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "suspicious_activity.log"

if not os.path.exists(DATA_FILE):
    print(f"Error: {DATA_FILE} not found! Please check the file path.")
    exit()

df = pd.read_csv(DATA_FILE)

REQUEST_THRESHOLD = 1000

suspicious_traffic = df[df["request_count"] > REQUEST_THRESHOLD]

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write("\nSuspicious IPs detected:\n")
    for index, row in suspicious_traffic.iterrows():
        log_entry = f"{row['ip_address']} - {row['request_count']} requests\n"
        print(log_entry.strip())  
        log.write(log_entry)

suspicious_traffic[["ip_address"]].to_csv(SUSPICIOUS_IPS_FILE, index=False)

print(f"Suspicious IPs saved to {SUSPICIOUS_IPS_FILE}")
```

### Output Example
```
Suspicious IPs detected:
203.0.113.15 - 1500 requests
192.168.1.100 - 1800 requests
Suspicious IPs saved to suspicious_ips.csv
```

---

## 3. IP Blocking Script (`block_suspicious_ips.py`)

### Purpose
- This script blocks IPs that were flagged as suspicious.
- Uses iptables (Linux firewall) to prevent further access.
- Stores blocked IPs in `blocked_ips.log`.

### How It Works
- Loads suspicious IPs from `suspicious_ips.csv`.
- Checks if an IP is already blocked to prevent duplicates.
- Adds a firewall rule (`iptables -A INPUT -s <IP> -j DROP`).
- Logs blocked IPs in `blocked_ips.log`.

### Code Explanation
```python
import os
import pandas as pd

SUSPICIOUS_IPS_FILE = "suspicious_ips.csv"
LOG_FILE = "blocked_ips.log"

if not os.path.exists(SUSPICIOUS_IPS_FILE):
    print(f"Error: {SUSPICIOUS_IPS_FILE} not found! Please check the file path.")
    exit()

suspicious_ips_df = pd.read_csv(SUSPICIOUS_IPS_FILE)
suspicious_ip_list = suspicious_ips_df["ip_address"].tolist()

def is_ip_blocked(ip_address):
    result = os.popen(f"iptables -L INPUT -v -n | grep {ip_address}").read()
    return bool(result)

def block_ip(ip_address):
    if is_ip_blocked(ip_address):
        print(f"Skipping {ip_address} (already blocked).")
        return

    print(f"Blocking IP: {ip_address}")
    os.system(f"iptables -A INPUT -s {ip_address} -j DROP")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{ip_address} blocked\n")

for suspicious_ip in suspicious_ip_list:
    block_ip(suspicious_ip)

print("All suspicious IPs have been blocked.")
```

### Output Example
```
Blocking IP: 203.0.113.15
Blocking IP: 192.168.1.100
All suspicious IPs have been blocked.
```

---

## How to Run the Scripts

### Step 1: Monitor Network Traffic
```bash
python network_monitor.py
```

### Step 2: Detect Suspicious IPs
```bash
python detect_suspicious_ips.py
```

### Step 3: Block Suspicious IPs
```bash
sudo python block_suspicious_ips.py
```

---

## Script Summary

| Script | Function | Output File |
|--------|----------|-------------|
| `network_monitor.py` | Monitors network traffic in real-time | `packet_log.txt` |
| `detect_suspicious_ips.py` | Detects suspicious IPs (high request volume) | `suspicious_ips.csv` |
| `block_suspicious_ips.py` | Blocks malicious IPs via firewall | `blocked_ips.log` |

---

## Conclusion

- These three scripts work together to monitor, detect, and block malicious activities on the network.
- Real-time monitoring helps track activities, while log analysis identifies threats.
- Firewall rules ensure that suspicious IPs are denied network access.

---