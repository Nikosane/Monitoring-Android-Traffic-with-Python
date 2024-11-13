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
```

## 2. Capturing Traffic with **Tcpdump** on Android

Now we’ll capture network traffic directly from the Android device using **tcpdump**. This method doesn’t require root access and allows us to capture packets over Wi-Fi or mobile data.

### Setup
1. Install **tcpdump** on the Android device using a package manager (e.g., **Termux**).
2. Enable **USB Debugging** and connect your Android device to your computer via **ADB**.
3. Ensure that **tcpdump** is available on your device.

### Code
```bash
# Capture traffic on Wi-Fi interface (typically wlan0) and save it to a file
adb shell "tcpdump -i wlan0 -w /sdcard/traffic.pcap"
```


### Explanation
- **`-i wlan0`**: This option specifies the network interface to capture packets from. Replace `'wlan0'` with the correct network interface if your Android device uses a different one (e.g., `rmnet0` for mobile data).
- **`-w /sdcard/traffic.pcap`**: The `-w` option saves the captured packets into a file. Here, the packets will be saved as `traffic.pcap` in the Android device’s `/sdcard/` directory.

After running this command, tcpdump will start capturing packets and saving them to the file `traffic.pcap`.

---

### Transferring the Captured Traffic
Once you have the `.pcap` file on your Android device, you can transfer it to your computer for analysis. Use the following **ADB** command:

```bash
adb pull /sdcard/traffic.pcap

```

### Analyzing Captured Traffic

After transferring the `.pcap` file, you can analyze the captured traffic using **Wireshark** or **Pyshark**.

#### Analyzing with **Wireshark**:
1. Open **Wireshark** on your computer.
2. Load the `.pcap` file by clicking on **File > Open** and selecting the file.
3. Use **filters** in Wireshark to inspect specific types of traffic. For example:
   - **`ip.addr == 192.168.1.1`**: Filter packets related to a specific IP address.
   - **`tcp.port == 80`**: Filter packets related to HTTP traffic on port 80.

Wireshark provides a rich set of tools to help you visualize and analyze network traffic, such as inspecting protocol details, packet streams, and more.
