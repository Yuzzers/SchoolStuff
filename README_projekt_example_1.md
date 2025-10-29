
__Disclaimer:__ This is for teaching advanced network class on Zealand Business Academy (zealand.dk)

# Table of Contents
<!-- TOC -->
- [Table of Contents](#table-of-contents)
- [Roleplay as an CTO](#roleplay-as-an-cto)
    - [Incident](#incident)
    - [My solution:](#my-solution)
      - [Why:](#why)
      - [How:](#how)
- [Intro to Automated testing](#intro-to-automated-testing)
    - [Incident](#incident-1)
    - [My solution](#my-solution-1)
- [Test of UDP protocol](#test-of-udp-protocol)
      - [Incident](#incident-2)
    - [My solution](#my-solution-2)
      - [Why UDP?](#why-udp)
      - [How UDP is Used](#how-udp-is-used)
      - [screenshot of test result:](#screenshot-of-test-result)
- [Test of TCP protocol](#test-of-tcp-protocol)
      - [Incident](#incident-3)
    - [My solution](#my-solution-3)
      - [Why TCP?](#why-tcp)
      - [How TCP is Used](#how-tcp-is-used)
      - [screenshot of test result:](#screenshot-of-test-result-1)
- [Test of MQTT protocol](#test-of-mqtt-protocol)
      - [Incident](#incident-4)
    - [My solution](#my-solution-4)
      - [Why TCP?](#why-tcp-1)
      - [How TCP is Used](#how-tcp-is-used-1)
      - [screenshot of test result:](#screenshot-of-test-result-2)
- [Test of MQTT protocol](#test-of-mqtt-protocol-1)
      - [Incident](#incident-5)
    - [My solution](#my-solution-5)
      - [Why TCP?](#why-tcp-2)
      - [How TCP is Used](#how-tcp-is-used-2)
      - [screenshot of test result:](#screenshot-of-test-result-3)

<!-- /TOC -->

---
# Roleplay as an CTO
### Incident
The student needs to learn how to be a CTO of a startup company. 

Along the way, they face real-world incidents reflecting the theoretical challenges they must solve through 4 phases:
`Garage → MVP → Pilot Project → Scalability`

The student must first design the company. It can be what ever they want, as long it is about network and IoT.

### My solution:
![company 1 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_1.png)

#### Why:
Our goal is to help farmers optimize their crop yields and promote more sustainable farming practices by using data-driven insights . 

#### How:
We are developing IoT-based sensors that measure soil moisture, fertilizer levels, and temperature. These sensors transmit real-time data to a cloud-based platform where farmers can access analytics and recommendations.

[To table of contents](#table-of-contents)

---

# Intro to Automated testing
### Incident
The company struggles to remember how different systems are supposed to work.

They want to implement live documentation based on automated test cases, ensuring:
* codes works as specified
* documentation:
  *  stays up to date, 
  *  serves as a reference for past implementations

The student must setup an automated testing in Python, to build prototypes, show that they work, and how they are supposed to be used.

### My solution
__My testfile__

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/3_1.png)

__My test cases (1 pass, 1 fail, 1 skips, 1 crashes)__
![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/3_2.png)

__The test result__
![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/3_3.png)

[To table of contents](#table-of-contents)

---
# Test of UDP protocol
#### Incident
The company must collect data from one or more sensor setups:
* 10 sensors sending data every 100 ms
* 100 sensors sending data every 1 second
* 1000 sensors sending data every 10 seconds

Each sensor measures and transmits values such as temperature, humidity, acceleration, or speed. 

A UDP setup would be good.

### My solution
#### Why UDP?

We chose UDP (User Datagram Protocol) because:
* Sensor readings are frequent and lightweight, a few bytes per packet.
* Occasional packet loss is acceptable (soil values do not change drastically second-to-second).
* Low latency and reduced network overhead compared to TCP, MQTT, and HTTP.
* It scales efficiently with 1000 distributed sensors sending periodic updates.

#### How UDP is Used
Each sensor sends a small UDP packet with:
```
{
  "sensor_id": "farm-001",
  "temperature": 21.8
  "timestamp": "2025-09-23T14:52:05Z",
}
```

#### screenshot of test result:
Location: `test/test_1_udpMessages.py`
![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/4_1.png)


[To table of contents](#table-of-contents)

---
# Test of TCP protocol
#### Incident
The company needs to control various actuators and devices over a network. 

Actuators perform actions based on received data (e.g., lamps, motors, speakers, displays), while devices include controllers such as Arduino, Raspberry Pi, or computers. 

Command order and delivery reliability are critical, for example, a lamp must correctly respond to a sequence like `on, off, on, off` without errors or and in correct order.

A TCP setup would be good.

### My solution
#### Why TCP?

We chose TCP (Transmission Control Protocol) because:
* Reliable delivery ensures all control commands reach the target devices without loss.
* Ordered transmission guarantees commands are executed in the correct sequence (e.g., on → off → on).
* Error detection and retransmission make it suitable for critical actuator control where missed or corrupted data could cause faults.
* Low latency and reduced network overhead compared to MQTT, and HTTP.

#### How TCP is Used
Each sensor sends a small TCP packet with:
```
{
  "actuator_id": "lamp-001",
  "command": "on",
  "timestamp": "2025-09-23T14:52:05Z",
}
```

#### screenshot of test result:
Location: `test/test_2_tcpMessages.py`
![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/5_1.png)

[To table of contents](#table-of-contents)

---

---
# Test of MQTT protocol
#### Incident
The company wants to build a decentralized and scalable IoT network. 

Sensors, actuators, and devices must be configured to publish and subscribe to relevant topics so they can exchange data efficiently without having to setup direct connections between each. 

For example that all lamps on field 1 and not field 2 can be turned off with a single command.

A MQTT setup would be good.

### My solution
#### Why TCP?

We chose MQTT (Message Queuing Telemetry Transport) because:
* It uses a publish/subscribe model, enabling scalable and flexible communication between many devices without direct links.

* Topic-based filtering allows targeted control — e.g., sending a single command to all lamps on field 1.

* Quality of Service (QoS) levels ensure reliable message delivery, even on unstable networks.

* Persistent sessions and last will messages improve robustness and fault tolerance in distributed systems.

#### How TCP is Used
Each sensor sends a small MQTT message with:
```
* UI at Central: Published: field 2 -> on 2
* Lamp 2 on field 2: Received: field 2 -> on 2
```
```
* UI at Central: Published: field 1 -> on 1
* Lamp 1 on field 1: Received: field 1 -> on 1
* Lamp 3 on field 1: Received: field 1 -> on 1
```
```
* UI at Barn: Published: field 1 -> off 1
* Lamp 3 on field 1: Received: field 1 -> off 1
* Lamp 1 on field 1: Received: field 1 -> off 1
}
```

#### screenshot of test result:
Location: `test/test_2_tcpMessages.py`
![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/6_1.png)

[To table of contents](#table-of-contents)

---
# Test of MQTT protocol
#### Incident
The company wants to build a decentralized and scalable IoT network. 

Sensors, actuators, and devices must be configured to publish and subscribe to relevant topics so they can exchange data efficiently without having to setup direct connections between each. 

For example that all lamps on field 1 and not field 2 can be turned off with a single command.

A MQTT setup would be good.

### My solution
#### Why TCP?

We chose MQTT (Message Queuing Telemetry Transport) because:
* It uses a publish/subscribe model, enabling scalable and flexible communication between many devices without direct links.

* Topic-based filtering allows targeted control — e.g., sending a single command to all lamps on field 1.

* Quality of Service (QoS) levels ensure reliable message delivery, even on unstable networks.

* Persistent sessions and last will messages improve robustness and fault tolerance in distributed systems.

#### How TCP is Used
Each sensor sends a small MQTT message with:
```
* UI at Central: Published: field 2 -> on 2
* Lamp 2 on field 2: Received: field 2 -> on 2
```
```
* UI at Central: Published: field 1 -> on 1
* Lamp 1 on field 1: Received: field 1 -> on 1
* Lamp 3 on field 1: Received: field 1 -> on 1
```
```
* UI at Barn: Published: field 1 -> off 1
* Lamp 3 on field 1: Received: field 1 -> off 1
* Lamp 1 on field 1: Received: field 1 -> off 1
}
```

#### screenshot of test result:
Location: `test/test_2_tcpMessages.py`
![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/6_1.png)

[To table of contents](#table-of-contents)

---
