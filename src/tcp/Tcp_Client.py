import socket
import time
from src.colors import Colors

class TCPClient:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(f"Connected to server {self.host}:{self.port}")

    def send_message(self, message: str):
        if not self.sock:
            raise ConnectionError("Client is not connected to a server.")
        print(f"{Colors.yellow}Sent:     {message}{Colors.reset}")
        self.sock.sendall((message + "\n").encode())

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        print("Connection closed.")


if __name__ == "__main__":
    client = TCPClient()
    client.connect()

    # Send 10 messages with timestamps
    for n in range(10):
        timestamp_us = int(time.time() * 1_000_000)  # microseconds
        msg = f"hello world {timestamp_us}"
        client.send_message(msg)
        time.sleep(.3)

    client.close()
