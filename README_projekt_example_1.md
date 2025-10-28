
__Disclaimer:__ This is for teaching advanced network class on Zealand Business Academy (zealand.dk)

<!-- TOC -->
# Table of Contents
- [Roleplay as an CTO](#roleplay-as-an-cto)
    - [Incident](#incident)
    - [Logo:](#logo)
    - [Why:](#why)
    - [How:](#how)
- [Intro to GIT](#intro-to-git)
      - [Why UDP?](#why-udp)
      - [How UDP is Used](#how-udp-is-used)
      - [We use UDP because:](#we-use-udp-because)
      - [How UDP is used](#how-udp-is-used-1)
      - [We use UDP because:](#we-use-udp-because-1)
      - [How UDP is used](#how-udp-is-used-2)

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
# Intro to GIT
### Incident
Project data, documentation, or source code has been lost or corrupted. 

Causes may include:
* a developer’s computer crash, 
* last-minute code changes breaking functionality, 
* or confusion between multiple unsynchronized versions. 

The student must be able to restore the project and implement proper backup and version control practices.

### My solution
####
This readme_project_example and repo is the solution to this assignment.

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
