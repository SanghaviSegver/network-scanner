"""
Network Scanner Tool
Author: [Your Name]
Description: Scans a subnet to discover live hosts, open ports, and device info.
             Useful for network monitoring and administration tasks.
"""

import socket
import subprocess
import platform
import ipaddress
import concurrent.futures
import datetime
import json
import os

# ─── CONFIGURATION ────────────────────────────────────────────────
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080, 8443]
PORT_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}
TIMEOUT = 1  # seconds


# ─── PING HOST ─────────────────────────────────────────────────────
def ping_host(ip):
    """Ping a host to check if it is alive."""
    system = platform.system().lower()
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "500", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, timeout=2)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


# ─── GET HOSTNAME ──────────────────────────────────────────────────
def get_hostname(ip):
    """Resolve IP address to hostname."""
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except socket.herror:
        return "Unknown"


# ─── SCAN PORTS ───────────────────────────────────────────────────
def scan_ports(ip):
    """Scan common ports on a host and return open ones."""
    open_ports = []
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            result = sock.connect_ex((str(ip), port))
            if result == 0:
                open_ports.append({
                    "port": port,
                    "service": PORT_NAMES.get(port, "Unknown")
                })
            sock.close()
        except socket.error:
            pass
    return open_ports


# ─── SCAN SINGLE HOST ─────────────────────────────────────────────
def scan_host(ip):
    """Ping, resolve, and port-scan a single IP address."""
    if ping_host(ip):
        hostname = get_hostname(ip)
        open_ports = scan_ports(ip)
        return {
            "ip": str(ip),
            "status": "UP",
            "hostname": hostname,
            "open_ports": open_ports
        }
    return None


# ─── SCAN SUBNET ──────────────────────────────────────────────────
def scan_subnet(subnet):
    """Scan all hosts in a subnet using multithreading for speed."""
    print(f"\n{'='*55}")
    print(f"  Network Scanner - Scanning: {subnet}")
    print(f"  Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}\n")

    network = ipaddress.IPv4Network(subnet, strict=False)
    hosts = list(network.hosts())
    results = []

    print(f"[*] Scanning {len(hosts)} hosts...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_host, ip): ip for ip in hosts}
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            if result:
                results.append(result)
                ip = result["ip"]
                hostname = result["hostname"]
                ports = result["open_ports"]
                port_str = ", ".join(
                    [f"{p['port']}/{p['service']}" for p in ports]
                ) if ports else "No open ports found"
                print(f"  [+] HOST UP   {ip:<18} {hostname}")
                print(f"      Ports   : {port_str}\n")

            # Progress indicator
            progress = int((i + 1) / len(hosts) * 20)
            bar = "█" * progress + "░" * (20 - progress)
            print(f"\r  Progress: [{bar}] {i+1}/{len(hosts)}", end="", flush=True)

    print(f"\n\n{'='*55}")
    print(f"  Scan Complete!")
    print(f"  Total Hosts UP : {len(results)}")
    print(f"  Finished: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}\n")

    return results


# ─── SAVE REPORT ──────────────────────────────────────────────────
def save_report(results, subnet):
    """Save scan results to a JSON report file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_report_{timestamp}.json"
    report = {
        "scan_time": timestamp,
        "subnet": subnet,
        "total_hosts_up": len(results),
        "hosts": results
    }
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
    print(f"[✓] Report saved: {filename}\n")
    return filename


# ─── MAIN ─────────────────────────────────────────────────────────
def main():
    print("\n╔══════════════════════════════════════════╗")
    print("║        Python Network Scanner v1.0       ║")
    print("║     Built for Network Engineering        ║")
    print("╚══════════════════════════════════════════╝")

    print("\nExamples:")
    print("  192.168.1.0/24   → scans 192.168.1.1 to 192.168.1.254")
    print("  10.0.0.0/28      → scans 10.0.0.1 to 10.0.0.14")

    subnet = input("\nEnter subnet to scan (e.g. 192.168.1.0/24): ").strip()

    try:
        ipaddress.IPv4Network(subnet, strict=False)
    except ValueError:
        print("[!] Invalid subnet format. Please try again.")
        return

    results = scan_subnet(subnet)

    if results:
        save = input("Save report to JSON? (y/n): ").strip().lower()
        if save == "y":
            save_report(results, subnet)
    else:
        print("[!] No live hosts found.\n")


if __name__ == "__main__":
    main()
