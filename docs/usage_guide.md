# Usage Guide: Monitoring Android Traffic with Python

## Prerequisites
- Python 3.x installed on your computer.
- Android device with `tcpdump` installed.
- `adb` (Android Debug Bridge) setup.

## Steps
1. Enable USB debugging on your Android device.
2. Install `tcpdump`:
   ```bash
   adb shell su -c "apt install tcpdump"
   ```
3. Start capturing traffic:
```bash
adb shell tcpdump -i any -w /sdcard/capture.pcap
```
4. Pull the file to your computer:
```bash
adb pull /sdcard/capture.pcap ./data/sample_packets.pcap
```
5. Analyze traffic:
```bash
python src/traffic_monitor.py --file ./data/sample_packets.pcap
```
## Example Output
```bash
TCP Packet: 192.168.1.2 -> 172.217.16.142
UDP Packet: 192.168.1.2 -> 8.8.8.8
```