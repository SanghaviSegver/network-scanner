# 🔍 Python Network Scanner

A command-line network scanning tool built in Python that discovers live hosts, resolves hostnames, and identifies open ports across a subnet — similar to basic Nmap functionality.

---

## 📌 Features

- ✅ Ping sweep to detect live hosts in any subnet
- ✅ Hostname resolution via reverse DNS lookup
- ✅ Port scanning for 13 common services (SSH, HTTP, FTP, MySQL, RDP, etc.)
- ✅ Multi-threaded scanning for fast results (50 threads)
- ✅ Real-time progress bar in terminal
- ✅ JSON report export with timestamp
- ✅ Works on Windows, Linux, and macOS

---

## 🛠️ Technologies Used

- Python 3.x
- `socket` — TCP port scanning and hostname resolution
- `subprocess` — Cross-platform ping execution
- `ipaddress` — Subnet parsing and IP iteration
- `concurrent.futures` — Multi-threaded scanning
- `json` — Report generation

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/SanghaviSegver/network-scanner.git
cd network-scanner
```

### 2. Run the scanner
```bash
python network_scanner.py
```

### 3. Enter the subnet when prompted
```
Enter subnet to scan (e.g. 192.168.1.0/24): 192.168.1.0/24
```

---

## 📊 Sample Output

```
=======================================================
  Network Scanner - Scanning: 192.168.1.0/24
  Started: 2025-06-01 10:30:00
=======================================================

[*] Scanning 254 hosts...

  [+] HOST UP   192.168.1.1        router.local
      Ports   : 80/HTTP, 443/HTTPS

  [+] HOST UP   192.168.1.5        desktop-pc
      Ports   : 22/SSH, 3389/RDP

=======================================================
  Scan Complete!
  Total Hosts UP : 2
  Finished: 2025-06-01 10:30:45
=======================================================
```

---

## 📁 Report Export (JSON)

```json
{
    "scan_time": "20250601_103045",
    "subnet": "192.168.1.0/24",
    "total_hosts_up": 2,
    "hosts": [
        {
            "ip": "192.168.1.1",
            "status": "UP",
            "hostname": "router.local",
            "open_ports": [
                {"port": 80, "service": "HTTP"},
                {"port": 443, "service": "HTTPS"}
            ]
        }
    ]
}
```

---

## 📡 Ports Scanned

| Port | Service |
|------|---------|
| 21   | FTP     |
| 22   | SSH     |
| 23   | Telnet  |
| 25   | SMTP    |
| 53   | DNS     |
| 80   | HTTP    |
| 110  | POP3    |
| 143  | IMAP    |
| 443  | HTTPS   |
| 3306 | MySQL   |
| 3389 | RDP     |
| 8080 | HTTP-Alt|
| 8443 | HTTPS-Alt|

---

## 🔧 Networking Concepts Used

- **TCP/IP** — Understanding of IP addressing and TCP handshake for port scanning
- **Subnetting** — CIDR notation parsing to iterate over valid host IPs
- **DNS** — Reverse lookup to resolve IP → hostname
- **Socket Programming** — Low-level TCP connection attempts to detect open ports
- **ICMP** — Ping (ICMP Echo Request) to check host availability

---

## 📌 Use Cases

- Network inventory and asset discovery
- Home lab network monitoring
- Learning TCP/IP and socket programming
- Pre-audit reconnaissance (on networks you own)

---

## ⚠️ Disclaimer

This tool is intended for educational purposes and use on networks you own or have explicit permission to scan. Unauthorized scanning is illegal.

---

## 👤 Author

**Sanghavi S**  
B.E. Computer Science Engineering  
Interested in Network Engineering | Python | Linux | MERN Stack
[LinkedIn](https://www.linkedin.com/in/sanghavi-s-721416215/) | [GitHub](https://github.com/SanghaviSegver)
