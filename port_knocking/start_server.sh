#!/bin/bash

echo "=== Starting Port Knocking Server ==="

# Start SSH service
sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
echo "[1/4] Starting SSH service..."
service ssh start

# Set up initial firewall rules
echo "[2/4] Blocking protected port 2222..."
iptables -A INPUT -p tcp --dport 2222 -j DROP

# Show available interfaces
echo "Available network interfaces:"
ip addr show

# Start knockd - try eth0 first, fallback to auto-detect
echo "[3/4] Starting knockd daemon..."
if ip link show eth0 &>/dev/null; then
    knockd -v -c /app/knockd.conf -i eth0 &
else
    # Auto-detect first non-loopback interface
    IFACE=$(ip -o link show | awk -F': ' '$2 !~ /^lo$/ {print $2; exit}')
    echo "eth0 not found, using $IFACE"
    knockd -d -c /app/knockd.conf -i $IFACE
fi

echo "[4/4] Server ready!"

# Keep container running
tail -f /dev/null