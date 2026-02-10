#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

import socket
import sys
# hint to use concurrent futures foe efficent scanning
from concurrent.futures import ThreadPoolExecutor
# to help organize output files:
import os

# in the deliverables we need: port number, service name/tyoe, banner, + flag if any
    # instead of just returning true, return as much info as possible about the port
def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool, int, string : True if port open, Port Number, Banner
    """
    try:
        # create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set timeout
        sock.settimeout(timeout)
        # try to connect to target:port
        connection = sock.connect_ex((target, port))

        # close the socket
        # return True if connection successful
        # successful if conn = 0
        if connection == 0:
            # store additional port info
            banner = "N/A"
            try:
                # try interacting with the port 
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                # if nothing received, try a generic request (for HTTP/Redis/API)
                if not banner:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                
                # nothing on redis
                if not banner and port == 6379:
                    sock.send(b"PING\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except:
                pass
            sock.close()
            return {"status": True, "portNumber": port, "banner": banner}
        
        # else return flase
        sock.close()
        return {"status": False, "portNumber": port, "banner": "N/A"}

        # pass  # Remove this and implement

    except (socket.timeout, ConnectionRefusedError, OSError):
        return {"status": False, "portNumber": port, "banner": "N/A"}

# instead of using the seperate function, im using scan_Range's logic to create and execute the thread tasks for concurrency
def scan_range(target, start_port, end_port):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")

    # TODO: Implement the scanning logic
    # Hint: Loop through port range and call scan_port()
    # Hint: Consider using threading for better performance

    for port in range(start_port, end_port + 1):
        # TODO: Scan this port
        scanResult = scan_port(target, port)
        # TODO: If open, add to open_ports list
        # TODO: Print progress (optional)
        if scanResult["status"]:
            open_ports.append(scanResult)
        # pass  # Remove this and implement

    return open_ports


def getServiceName(port, banner):
    commonPorts = {3306: "MySQL", 5000: "Flask Web App", 6379: "Redis", 22: "SSH", 2222: "Hidden SSH Server", 8888: "Secret API Service"}
    if port in commonPorts:
        return commonPorts[port]
    if "ssh" in banner.lower():
        return "SSH Server"
    if "http" in banner.lower() or "html" in banner.lower():
        return "HTTP Web Server"
    return "Unknown Service"

def main():
    """Main function"""

    # Example usage (you should improve this):
    if len(sys.argv) < 2:
        print("Usage: python3 port_scanner_template.py <target>")
        print("Example: python3 port_scanner_template.py 172.20.0.10")
        sys.exit(1)

    target = sys.argv[1]
    start_port = 1
    end_port = 60000  # Scan first 1024 ports by default ---- change to 10000 for 1.2
    threads = 100

    print(f"[*] Starting port scan on {target}")

    # open_ports = scan_range(target, start_port, end_port) --- change to threading
    open_ports = []
    with ThreadPoolExecutor(threads) as threadExecutor:
        # create tasks
        tasks = [threadExecutor.submit(scan_port, target, portRange) for portRange in range(start_port, end_port + 1)]
        # do tasks
        for task in tasks:
            scanResult = task.result()
            if scanResult["status"]:
                open_ports.append(scanResult)

    print(f"\n[+] Scan complete!")
    print(f"[+] Found {len(open_ports)} open ports:")
    for port in open_ports:
        print(f"    Port {port['portNumber']}: open")
    
    # output formatting -- table for easier reading
    outputDir = "port_scanner/scanResults"
    filename = os.path.join(outputDir, f"portScanner_target{target}_portRange_{start_port}_{end_port}.txt")
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    with open(filename, "w") as file:
        file.write(f"Scan Results for Target: {target}\nPort Range: [{start_port}, {end_port}]\n")
        file.write(f"Total OPEN Ports: {len(open_ports)}\n")
        file.write(f"{'PORT':<10} {'SERVICE':<20} {'BANNER':<100}\n")
        if len(open_ports) > 0:
            for port in open_ports:
                portNumber = port["portNumber"]
                portBanner = port["banner"]
                portService = getServiceName(portNumber, portBanner)
                file.write(f"{portNumber:<10} {portService:<20} {portBanner:<100}\n")


if __name__ == "__main__":
    main()
