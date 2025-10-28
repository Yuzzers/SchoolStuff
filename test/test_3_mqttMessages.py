import time
import pytest
from src.colors import Colors

from src.mqtt.Mqtt_Broker import MQTTBroker
from src.mqtt.Mqtt_Client import MQTTClient


@pytest.fixture(scope="module")
def broker():
    b = MQTTBroker(host="127.0.0.1", port=1883)
    b.start(background=True)
    # give the broker time to spin up
    time.sleep(1)
    yield b
    #b.close()


@pytest.fixture
def client_factory():
    clients = []

    def _make_client(client_id):
        colorPublish = Colors.blue
        colorRecieved = Colors.blue
        if(client_id=="C1"):
            colorPublish = Colors.blue
            colorRecieved = Colors.blue
        if(client_id=="C2"):
            colorPublish = Colors.cyan
            colorRecieved = Colors.cyan
        if(client_id=="C3"):
            colorPublish = Colors.magenta
            colorRecieved = Colors.magenta

     
        c = MQTTClient(client_id, colorPublish, colorRecieved, broker_host="127.0.0.1", broker_port=1883, client_id=client_id)
        c.connect(background=True)
        clients.append(c)
        return c

    yield _make_client

    # cleanup
    for c in clients:
        c.close()

@pytest.mark.focus
def test_pubsub(broker, client_factory):
    # Given
    lamp1 = client_factory("Lamp 1 on field 1")
    lamp2 = client_factory("Lamp 2 on field 2")
    lamp3 = client_factory("Lamp 3 on field 1")
    lamp4 = client_factory("Lamp 3 on field 2")
    laptop_at_central = client_factory("Central")
    laptop_at_barn = client_factory("Barn")

    lamp1.subscribe("field 1")
    lamp2.subscribe("field 2")
    lamp3.subscribe("field 1")
    laptop_at_central.subscribe("central")
    laptop_at_barn.subscribe("barn")

    time.sleep(1)  # allow subscriptions to register

    # When
    numberOfRepeats = 1
    for i in range(numberOfRepeats):
        laptop_at_central.publish("field 2", f"on 2")
        laptop_at_central.publish("field 1", f"on 1")
        laptop_at_barn.publish("field 1", f"off 1")
        time.sleep(0.1)  # give broker time to route

    # give time for async callbacks to fire
    time.sleep(2)

    # Then
    lamp1_messages = [m for _, m in lamp1.receivedMessages if m.startswith("on 1")]
    assert len(lamp1_messages) == numberOfRepeats

    lamp1_messages = [m for _, m in lamp1.receivedMessages if m.startswith("on 2")]
    assert len(lamp1_messages) == 0

    lamp1_messages = [m for _, m in lamp1.receivedMessages if m.startswith("off 1")]
    assert len(lamp1_messages) == numberOfRepeats


    lamp2_messages = [m for _, m in lamp2.receivedMessages if m.startswith("on 1")]
    assert len(lamp2_messages) == 0

    lamp2_messages = [m for _, m in lamp2.receivedMessages if m.startswith("on 2")]
    assert len(lamp2_messages) == numberOfRepeats

    lamp2_messages = [m for _, m in lamp2.receivedMessages if m.startswith("off 1")]
    assert len(lamp2_messages) == 0
    

    lamp3_messages = [m for _, m in lamp3.receivedMessages if m.startswith("on 1")]
    assert len(lamp3_messages) == numberOfRepeats

    lamp3_messages = [m for _, m in lamp3.receivedMessages if m.startswith("on 2")]
    assert len(lamp3_messages) == 0

    lamp3_messages = [m for _, m in lamp3.receivedMessages if m.startswith("off 1")]
    assert len(lamp3_messages) == numberOfRepeats
