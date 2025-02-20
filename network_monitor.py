"""
This script listens to network traffic in real-time and prints detected packets.
Think of it as a "security camera" that watches all the computers talking to each other.
"""

from scapy.all import sniff
from scapy.layers.inet import IP  # Corrected import

def monitor_packet(packet):
    """
    Function to analyze network packets.
    If a packet has an IP layer, it prints source and destination information.
    """
    if packet.haslayer(IP):
        print(f"Packet detected: {packet[IP].src} -> {packet[IP].dst} | Size: {len(packet)} bytes")

# Start monitoring network packets
print("Starting real-time network monitoring...")
sniff(prn=monitor_packet, store=False)  # Sniffs packets and calls monitor_packet function
