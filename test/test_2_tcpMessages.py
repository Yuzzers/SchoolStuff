import socket, time, sys, os, json, time, re, pytest, random
from datetime import datetime, timezone

from src.tcp.Tcp_Server import TCPServer
from src.tcp.Tcp_Client import TCPClient

pytestmark = pytest.mark.focus

@pytest.mark.timeout(20)
def test_server_client_message_exchange():
    host, port = "127.0.0.1", 12345
    sending_interval = .1
    simulated_lag = 2.5/100 # 10/100 is up to 10% lag, while 0/100 is up to 0% lag  
    expected_receive_interval = .1
    number_of_messages = 10

    server = TCPServer(host=host, port=port)
    server.start(expected_receive_interval=expected_receive_interval, background=True)

    # Allow server startup
    time.sleep(0.5)

    client = TCPClient(host=host, port=port)
    client.connect()

    state = "off"
    for n in range(number_of_messages):
        if state == "on":
            state = "off"
        else:
            state = "on"

        message = json.dumps({
            "actuator_id": "lamp-001",
            "command": state,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        client.send_message(message)
        time.sleep(sending_interval*(1+simulated_lag*random.random()))
        print("--")

    client.close()
    server.close()

    # Then it is verified that the server recieved all the messages
    assert(len(server.receivedMessages)==number_of_messages)
