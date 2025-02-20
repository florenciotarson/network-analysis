"""
This script listens to network traffic in real-time and prints detected packets.
Think of it as a "security camera" that watches all the computers talking to each other.
"""

# Corrected import order: Standard libraries first
from datetime import datetime
from scapy.all import sniff
from scapy.layers.inet import IP

# Define log file
LOG_FILE = "packet_log.txt"

def monitor_packet(packet):
    """
    Function to analyze network packets.
    If a packet has an IP layer, it prints and logs source and destination information.
    """
    if packet.haslayer(IP):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        packet_size = len(packet)

        # Log entry with improved formatting
        log_entry = (
            f"[{timestamp}] Packet detected: {src_ip} -> {dst_ip} "
            f"| Size: {packet_size} bytes\n"
        )

        print(log_entry.strip())  # Print to console

        # Write packet details to log file with UTF-8 encoding
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_entry)

# Start monitoring network packets
print("Starting real-time network monitoring...")
sniff(prn=monitor_packet, store=False, filter="ip")  # Capture only IP packets
