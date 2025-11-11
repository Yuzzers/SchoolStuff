import socket, time, sys, os, json, time
from datetime import datetime, timezone
from src.colors import Colors

class UDPClient:
    
    def __init__(self, server_ip: str = "127.0.0.1", server_port: int = 9999):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendMessage(self, repeat: int = 10, delay_ms: int = 1000):
        for i in range(repeat): 
            message = json.dumps({
                "sensor_id": "farm-001",
                "temperature": 21.8,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })    
            print(f"{Colors.yellow}Sent:     {message}{Colors.reset}")      
            self.client_socket.sendto(message.encode("utf-8"), (self.server_ip, self.server_port))

            time.sleep(delay_ms / 1000.0)


# Kan køres som main
if __name__ == "__main__":
    client = UDPClient()  # Default 127.0.0.1:9999
    client.sendMessage("hej server")
