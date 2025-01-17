#!/usr/bin/env python3

import os
import subprocess
import platform
from multiprocessing.pool import ThreadPool

def ping_ip(ip):
    """Pingează un IP și verifică dacă este activ."""
    param = "-c" if platform.system().lower() != "windows" else "-n"
    try:
        subprocess.run(['ping', param, '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return ip
    except subprocess.CalledProcessError:
        return None

def scan_network(network_prefix):
    """Scanează toate IP-urile dintr-un subnet."""
    ips = [f"{network_prefix}.{i}" for i in range(1, 255)]
    with ThreadPool(50) as pool:
        active_ips = pool.map(ping_ip, ips)
    return [ip for ip in active_ips if ip]

if __name__ == "__main__":
    # Setează direct prefixul rețelei tale
    subnet = "10.11.14.0"
    print(f"Prefixul rețelei utilizat: {subnet}")

    # Scanează rețeaua și afișează IP-urile active
    active_ips = scan_network(subnet)
    print("IP-uri active în rețea:", active_ips)
