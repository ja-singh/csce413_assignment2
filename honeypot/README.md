## Honeypot Starter Template

This directory is a starter template for the honeypot portion of the assignment.

### What you need to implement
- Choose a protocol (SSH, HTTP, or multi-protocol).
- Simulate a convincing service banner and responses.
- Log connection metadata, authentication attempts, and attacker actions.
- Store logs under `logs/` and include an `analysis.md` summary.
- Update `honeypot.py` and `logger.py` (and add modules as needed) to implement the honeypot.

### Getting started
1. Implement your honeypot logic in `honeypot.py`.
2. Wire logging in `logger.py` and record results in `logs/`.
3. Summarize your findings in `analysis.md`.
4. Run from the repo root with `docker-compose up honeypot`.

# Honeypot Implementation

This directory contains the demonstration of a low-interaction Honeypot that was created using Python's `socket` library. This honeypot aims to simulate a real SSH service where it allows attackers to attempt connection and records the details of the intrusion in the honeypot logs.

## Overview
#### File Structure
- `honeypot.py`: The core Python script managing the socket listener and threading logic.
- `.\logs\honeypot.log`: The destination for all captured security events and intruder data.
- `Dockerfile`: Used to containerize the honeypot for deployment within the Docker network.

#### Implementation Details 
1. SSH Service Simulation: The script poses as a real SSH server by presenting a realistic banner (`SSH-2.0-OpenSSH_8.8p1 Ubuntu-5ubuntu0.15`). This aims to deceive scanners into identifying the container as a vulnerable target.
2. Concurrency & Threading: The threading library was incorporated into the implementation to handle each incoming connection in a separate thread. This ensures the honeypot remains active and accurately logs data even if multiple attackers connect simultaneously.
3. Logging Mechanism: Every interaction is captured in a dedicated log file. The system records the source IP, port, high-resolution timestamps (start, end, and duration), and the raw data or login credentials attempted by the intruder.

## Usage
```bash
sudo docker build -t honeypot
```
```bash
nc 
ssh 
```
