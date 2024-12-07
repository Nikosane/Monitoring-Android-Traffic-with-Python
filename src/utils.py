import os
from scapy.all import PcapReader, wrpcap


def check_file_exists(filepath):
    """
    Check if a file exists.
    :param filepath: Path to the file.
    :return: True if the file exists, False otherwise.
    """
    if os.path.exists(filepath):
        return True
    print(f"Error: File not found - {filepath}")
    return False


def read_pcap_file(filepath):
    """
    Read packets from a .pcap file.
    :param filepath: Path to the .pcap file.
    :return: List of packets.
    """
    if not check_file_exists(filepath):
        return []

    try:
        packets = list(PcapReader(filepath))
        print(f"Successfully read {len(packets)} packets from {filepath}.")
        return packets
    except Exception as e:
        print(f"Error reading pcap file: {e}")
        return []


def save_filtered_packets(packets, output_file):
    """
    Save filtered packets to a new .pcap file.
    :param packets: List of filtered packets.
    :param output_file: Path to save the filtered packets.
    """
    try:
        wrpcap(output_file, packets)
        print(f"Filtered packets saved to {output_file}")
    except Exception as e:
        print(f"Error saving filtered packets: {e}")


def filter_packets_by_ip(packets, ip_address, direction="src"):
    """
    Filter packets based on source or destination IP address.
    :param packets: List of packets.
    :param ip_address: IP address to filter by.
    :param direction: 'src' for source IP, 'dst' for destination IP.
    :return: List of filtered packets.
    """
    if direction not in ["src", "dst"]:
        print("Error: Direction must be 'src' or 'dst'.")
        return []

    filtered_packets = []
    for packet in packets:
        if packet.haslayer("IP"):
            if direction == "src" and packet["IP"].src == ip_address:
                filtered_packets.append(packet)
            elif direction == "dst" and packet["IP"].dst == ip_address:
                filtered_packets.append(packet)

    print(f"Found {len(filtered_packets)} packets matching {direction} IP: {ip_address}.")
    return filtered_packets


def pretty_print_packet(packet):
    """
    Print packet details in a readable format.
    :param packet: A single packet.
    """
    if packet.haslayer("IP"):
        src = packet["IP"].src
        dst = packet["IP"].dst
        protocol = "TCP" if packet.haslayer("TCP") else "UDP" if packet.haslayer("UDP") else "Other"
        print(f"Packet: {src} -> {dst}, Protocol: {protocol}")
    else:
        print("Non-IP packet detected.")
