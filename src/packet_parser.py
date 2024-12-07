def extract_packet_info(packet):
    """Extract basic information from a packet."""
    if packet.haslayer("IP"):
        return {
            "source": packet["IP"].src,
            "destination": packet["IP"].dst,
            "protocol": packet["IP"].proto,
        }
    return None
