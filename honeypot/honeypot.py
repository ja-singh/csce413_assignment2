#!/usr/bin/env python3
"""Starter template for the honeypot assignment."""

import logging
import os
import socket
import logging
import datetime
import threading

LOG_PATH = "/app/logs/honeypot.log"
HOST = '0.0.0.0'
PORT = 22
# using ip .20's banner as inspo: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.13, just change numbers 
    # sockets send text as bytes 
SSH_BANNER = b"SSH-2.0-OpenSSH_8.8p1 Ubuntu-5ubuntu0.15\r\n"


def setup_logging():
    os.makedirs("/app/logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
    )


# allow hacker to attempt to connect / login
def make_fake_connection(client_socket, addr):
    # get the attackers ip and port and store the time for the logs
    source_ip = addr[0]
    source_port = addr[1]
    start_time = datetime.datetime.now()
    
    logging.info(f"Intruder Detected (IP:PORT) @ {source_ip}:{source_port}")
    
    try:
        # greet the attacker -- send the fake banner 
        client_socket.sendall(SSH_BANNER)
        
        # accept attacker data 
        data = client_socket.recv(1024)
        logging.info(f"   Data Recieved from {source_ip}: {data.strip()}")

        # allow the attacker to attemot to log in
        # store user and pass for logs
        for attempt in range(3):
            client_socket.sendall(b"user: ")
            user = client_socket.recv(1024).decode(errors='ignore').strip()
            client_socket.sendall(b"password: ")
            password = client_socket.recv(1024).decode(errors='ignore').strip()
            logging.info(f"   Login Attempt from {source_ip} --- User: <{user}> | Pass: <{password}>")
            
            # let them know they arent allowed access (but dont reveal honeypot)
            if attempt < 2:
                client_socket.sendall(b"\r\nAccess Denied. Please try again.\r\n")
            else:
                client_socket.sendall(b"\r\nToo many failed attempts.\r\n")
        
    except Exception as e:
        logging.error(f"Error handling {source_ip}: {e}")
    finally:
        # finish logging 
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logging.info(f"   Timeline: START {start_time} --- END {end_time} | Total Duration: {duration} sec")
        client_socket.close()


def run_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    logging.info(f"Honeypot active on port {PORT}...")

    while True:
        client, addr = server.accept()
        # Handle each attacker in a separate thread so the honeypot stays up
        client_handler = threading.Thread(target=make_fake_connection, args=(client, addr))
        client_handler.start()


if __name__ == "__main__":
    setup_logging()
    run_honeypot()
