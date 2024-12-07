from scapy.all import rdpcap, IP, TCP, UDP

def analyze_packets(pcap_file):
    packets = rdpcap(pcap_file)
    print(f"Analyzing {len(packets)} packets...\n")

    for packet in packets:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
            print(f"{protocol} Packet: {src_ip} -> {dst_ip}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze Android traffic from a .pcap file.")
    parser.add_argument("--file", required=True, help="Path to the .pcap file.")
    args = parser.parse_args()

    analyze_packets(args.file)