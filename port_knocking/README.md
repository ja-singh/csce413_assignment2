# Port Knocking Implementation

This directory contains the demonstration of Port Knocking using the existing `knockd` daemon implementation on the open port (2222) of the SSH Server.

## Overview
#### File Structure
- `demo.sh`: An automated script to demonstrate the transition from a closed to an open port.
- `Dockerfile`: Used to containerize the port knocking demonstration for deployment within the Docker network.
- `knock_client.py`: A Python script modified from the starter template to send TCP SYN packets to the target sequence.
- `knockd.conf`: Configuration file defining the knock sequence and iptables rules.
- - `knock_server.py`: A Python script from the initial starter template that has not been modified for this implementation. 
- `start_server.sh`: Script to initialize the firewall (setting port 2222 to DROP) and start the knockd daemon.

#### Implementation Details 
1. Initial Firewall Configuration: Using `start_server.sh`, the system is set to `DROP` all incoming packets to port 2222 (as the network reconaissance showed this as an open port). 
2. Knock Sequence: The `knockd.conf` file is configured with a secret sequence (1234, 5678, 9012) and specifies what firewalls the system should run when a correct sequence is recieved. Specifically, upon a sucessful knock, `knockd` executes an `iptables` `append` rule to allow the requester's IP. After a specified timeout, it executes a `delete` rule to close the port again.
3. Client Starter Code Modification: The knock_client.py was updated to use TCP connections, as knockd is configured to listen for TCP SYN packets.

## Usage
```bash
sudo docker build -t port-knock-server .
sudo docker run -d   --name knock-server   --privileged   --network csce413_assignment2_vulnerable_network   --ip 172.20.0.40   port-knock-server
./demo.sh 172.20.0.40