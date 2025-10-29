import time
import threading
import paho.mqtt.client as mqtt
from src.colors import Colors


class MQTTClient:
    def __init__(self, name="client", colorPublish=Colors.green, colorRecieved=Colors.bright_green):
        self.name = name
        self.colorPublish = colorPublish
        self.colorRecieved = colorRecieved 
        
        self.client = mqtt.Client(client_id=None, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        
        self.connected = False
        self.receivedMessages = []


        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        #self.connect(self)

    def connect(self, broker_host="127.0.0.1", broker_port=1883):
        self.client.connect(broker_host, broker_port, keepalive=60)
        self._thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        self._thread.start()
        self.wait_until_connected()
    
    def wait_until_connected(self, timeout=5):
        print(f"\n* '{self.name}' is waiting to connect")
        start = time.time()
        while not self.connected:
            if time.time() - start > timeout:
                raise TimeoutError("{MQTT client failed to connect in time")
            time.sleep(0.1)
        print(f"* '{self.name}' is connected")

    def _on_connect(self, client, userdata, flags, reasonCode, properties):
        if reasonCode == 0:
            self.connected = True
        else:
            print(f"{Colors.red}* {self.name}: MQTT connection failed with code {rc}{Colors.reset}")

    def _on_disconnect(self, client, userdata, reasonCode, properties):
        self._connected = False
        print(f"{Colors.orange}* {self.name}: MQTT disconnected (rc={rc}){Colors.reset}")

    def _on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"{self.colorRecieved}* {self.name}: Received: {msg.topic} -> {message}{Colors.reset}")
        self.receivedMessages.append(message)

    def publish(self, topic, message):
        if not self.connected:
            raise ConnectionError("Client is not connected to a broker.")
        print(f"{self.colorPublish}* {self.name}: Published: {topic} -> {message}{Colors.reset}")
        self.client.publish(topic, message)

    def subscribe(self, topic):
        if not self.connected:
            raise ConnectionError("Client is not connected to a broker.")
        print(f"* {self.name}: Subscribed to topic: {topic}")
        self.client.subscribe(topic)



if __name__ == "__main__":
    # Example usage
    client = MQTTClient("MQTT_client", Colors.green, Colors.bright_green, broker_host="127.0.0.1", broker_port=1883)
    client.connect(background=True)
    client.wait_until_connected()

    client.subscribe("test/topic")

    for n in range(5):
        timestamp_us = int(time.time() * 1_000_000)
        msg = f"hello world {timestamp_us}"
        client.publish("test/topic", msg)
        time.sleep(1)

    time.sleep(2)  # give some time to receive messages
    client.close()
