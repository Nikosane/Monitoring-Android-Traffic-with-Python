import unittest
from src.packet_parser import extract_packet_info
from scapy.layers.inet import IP

class TestPacketParser(unittest.TestCase):
    def test_extract_packet_info(self):
        packet = IP(src="192.168.1.1", dst="8.8.8.8", proto=6)
        info = extract_packet_info(packet)
        self.assertEqual(info["source"], "192.168.1.1")
        self.assertEqual(info["destination"], "8.8.8.8")
        self.assertEqual(info["protocol"], 6)

if __name__ == "__main__":
    unittest.main()
