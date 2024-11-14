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
---


### Analyzing Captured Traffic

After transferring the `.pcap` file, you can analyze the captured traffic using **Wireshark** or **Pyshark**.

#### Analyzing with **Wireshark**:
1. Open **Wireshark** on your computer.
2. Load the `.pcap` file by clicking on **File > Open** and selecting the file.
3. Use **filters** in Wireshark to inspect specific types of traffic. For example:
   - **`ip.addr == 192.168.1.1`**: Filter packets related to a specific IP address.
   - **`tcp.port == 80`**: Filter packets related to HTTP traffic on port 80.

Wireshark provides a rich set of tools to help you visualize and analyze network traffic, such as inspecting protocol details, packet streams, and more.



## 3. Capturing HTTP/HTTPS Traffic with mitmproxy

mitmproxy is an interactive, SSL-capable proxy that can capture and inspect HTTP/HTTPS traffic from your Android device. It’s especially useful for monitoring web traffic and can decrypt HTTPS traffic when configured correctly.
Setup
Install mitmproxy on your computer:

```bash
pip install mitmproxy
```

## Start mitmproxy to listen for incoming traffic:
```shell
mitmproxy --mode transparent
```
This command starts mitmproxy in transparent mode, allowing it to intercept and display all incoming traffic.



**Configure your Android device to use your computer as a proxy:**
- Go to Settings > Wi-Fi on your Android device.
- Long-press on the connected Wi-Fi network and select Modify Network.
- Under Advanced options, set Proxy to Manual and enter your computer’s IP address and mitmproxy’s default port 8080.

**To intercept HTTPS traffic, install the mitmproxy certificate on your Android device:**
- On your Android browser, go to http://mitm.it and download the certificate.
- Follow the prompts to install the certificate, enabling mitmproxy to decrypt HTTPS traffic.



## Code Example for Running mitmproxy as a Python Script

To automate traffic logging, you can use the mitmdump tool from mitmproxy and log requests with a Python script:

```python 
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Log request details
    print(f"Request URL: {flow.request.pretty_url}")
    print(f"Request Headers: {flow.request.headers}")
    print(f"Request Method: {flow.request.method}")
    
    # Optionally, filter for specific URLs or keywords
    if "example.com" in flow.request.pretty_url:
        print(f"Captured traffic to example.com: {flow.request}")
```

---

**Run this script with mitmdump:**
```bash
mitmdump -s path_to_your_script.py
```


Explanation
- **`mitmproxy --mode transparent`**: Starts mitmproxy in transparent mode, allowing it to intercept all traffic.
- **`mitmdump -s path_to_your_script.py`**: Runs mitmdump with your custom Python script to log and filter requests.

---

## 4. Monitoring Network Requests with adb logcat

For basic network debugging, adb logcat can capture logs directly from the Android device, including network-related events. This is helpful for identifying network request errors, connection issues, and general app debugging.
Setup

Connect your Android device to your computer with USB Debugging enabled.

Open a terminal or command prompt on your computer and run the following command to start capturing logs:
```
adb logcat
```
This command outputs all log messages from the device. You may see a lot of information, so filtering by network tags is often helpful.


    

**Filtering for Network Logs**

To focus only on network-related logs, you can use grep (on Unix-based systems) to filter relevant log tags. Here are some examples:

- Filter for HTTP logs from WebView-based apps:
    ```
    adb logcat | grep -i "chromium"
    ```

- Filter by specific keywords such as HTTP, HTTPS, or network:
    ```
    adb logcat | grep -i "network"
    ```

- Filter by application-specific tags by using the app’s specific package name. First, find the package name of your target app:
    ```
    adb shell pm list packages | grep "your_app_name"
    ```
    
- Then filter logs from that package:
    ```
    adb logcat | grep "your.package.name"


**Explanation**

**`adb logcat`**: Starts capturing logs from the Android device.
**`grep -i "keyword"`**: Filters logs by keyword, case-insensitive, to find specific network-related messages.
**`adb shell pm list packages`**: Lists all packages on the device; useful for finding an app’s package name to filter logs for that specific app.
