# Monitoring Android Traffic with Python

In this guide, we’ll walk through several methods to monitor network traffic from an Android device using Python. This is useful for debugging app behavior, analyzing network requests, or studying traffic patterns. We’ll use tools like Pyshark, tcpdump, and mitmproxy to capture and analyze network data.

## Requirements
- **Wireshark and Tshark** (for Pyshark method)
- **tcpdump** (for Android packet capture)
- **mitmproxy** (for HTTP/HTTPS traffic monitoring)
- **ADB** (Android Debug Bridge)

---

## 1. Capturing Traffic with Pyshark

Pyshark is a wrapper for Tshark, allowing us to capture and analyze packets directly in Python.

### Setup
1. Enable **Developer Mode** on your Android device.
2. Enable **USB Debugging** and connect the Android device to your computer.
3. Configure the Android device to connect through the computer’s network interface (Wi-Fi or USB tethering).

### Code
```python
import pyshark

def capture_android_traffic(interface='wlan0', capture_filter="ip"):
    print(f"Starting packet capture on interface: {interface}")
    capture = pyshark.LiveCapture(interface=interface, display_filter=capture_filter)
    
    for packet in capture.sniff_continuously():
        print(f"Packet: {packet}")
        # Access packet details: packet.ip.src, packet.ip.dst, etc.

if __name__ == "__main__":
    capture_android_traffic()
