import time
import pytest
from src.colors import Colors

from src.mqtt.Mqtt_Broker import MQTTBroker
from src.mqtt.Mqtt_Client import MQTTClient


#@pytest.mark.focus
def test_pubsub():
    # Given broker is started
    broker = MQTTBroker(host="127.0.0.1", port=1883)
    broker.start(background=True)
    broker.wait_until_running()

    # And clients are started
    lamp1 = MQTTClient("Lamp 1 on field 1", Colors.blue, Colors.magenta)
    lamp1.connect(broker_host="127.0.0.1", broker_port=1883)

    lamp2 = MQTTClient("Lamp 2 on field 2", Colors.blue, Colors.magenta)
    lamp2.connect(broker_host="127.0.0.1", broker_port=1883)
    
    lamp3 = MQTTClient("Lamp 3 on field 1", Colors.blue, Colors.magenta)
    lamp3.connect(broker_host="127.0.0.1", broker_port=1883)
    
    laptop_at_central = MQTTClient("UI at Central", Colors.blue, Colors.magenta)
    laptop_at_central.connect(broker_host="127.0.0.1", broker_port=1883)
    
    laptop_at_barn = MQTTClient("UI at Barn", Colors.blue, Colors.magenta)
    laptop_at_barn.connect(broker_host="127.0.0.1", broker_port=1883)

    # And clients are subscribed
    lamp1.subscribe("field 1")
    lamp2.subscribe("field 2")
    lamp3.subscribe("field 1")
    laptop_at_central.subscribe("central")
    laptop_at_barn.subscribe("barn")

    # When
    laptop_at_central.publish("field 2", f"on 2")
    time.sleep(0.1)
    laptop_at_central.publish("field 1", f"on 1")
    time.sleep(0.1)
    laptop_at_barn.publish("field 1", f"off 1")
    time.sleep(0.1)
    

    # Then
    assert getNumberOfMessagesRecieved(lamp1, "on 1") == 1
    assert getNumberOfMessagesRecieved(lamp1, "on 2") == 0
    assert getNumberOfMessagesRecieved(lamp1, "off 1") == 1

    assert getNumberOfMessagesRecieved(lamp2, "on 1") == 0
    assert getNumberOfMessagesRecieved(lamp2, "on 2") == 1
    assert getNumberOfMessagesRecieved(lamp2, "off 1") == 0
    
    assert getNumberOfMessagesRecieved(lamp3, "on 1") == 1
    assert getNumberOfMessagesRecieved(lamp3, "on 2") == 0
    assert getNumberOfMessagesRecieved(lamp3, "off 1") == 1

def getNumberOfMessagesRecieved(device, expected_message):
    found_messages = 0
    for message in device.receivedMessages:
        if(message == expected_message):
           found_messages += 1
    return found_messages
    