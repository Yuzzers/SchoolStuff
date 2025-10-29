
__Disclaimer:__ This is for teaching advanced network class on Zealand Business Academy (zealand.dk)

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
#### Why MQTT?

We chose MQTT (Message Queuing Telemetry Transport) because:
* It uses a publish/subscribe model, enabling scalable and flexible communication between many devices without direct links.

* Topic-based filtering allows targeted control — e.g., sending a single command to all lamps on field 1.

* Quality of Service (QoS) levels ensure reliable message delivery, even on unstable networks.

* Persistent sessions and last will messages improve robustness and fault tolerance in distributed systems.

#### How MQTT is Used
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
# Test of Physical connections
#### Incident
When setting up and operating a system consisting of x sensors, y actuators, and 1 controller, the following challenges may be experienced (choose yourself):
* Data loss due to unstable communication (too great a distance)
* Data loss due to overload (excessive data volume)
* Data loss due to interference from other networks, high-voltage equipment, or powerful motors.
A good idea would be to look into the setup of the network and design a good one.

### My solution
#### Why these connections?

We choose:
* __Field 1__ has a 433hz radio controller for our sensors. It is easy and cheap to setup and has a large radius. The sensors don't send much data and the data is not vurnable, so we use UDP. The field 1 controller is connected by  RJ45 cables, because it needs to travel a long distance to the office. 

* __The barn, field 2 and field 3__ is covered by wifi 2,4Ghz. It has a larger coverage than 5Ghz, which is more important here. We use MQTT. We collect lot of data here, which The wifi routers are connected with a RJ45 cables to the office.

* __The office__ uses 5Ghz wifi, because we need to transfer a lot of data and we also need the security of wifi, since we also use it for business data. Most runs on HTTP, but also on MQTT. The office is also connected to the internet with a fiber cable.

__drawing__

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/7_1.png)

---

# Test of HTTP protocol (RestAPI)
#### Incident
The company wants to enable devices and systems to communicate and exchange data easily with external applications, dashboards, or cloud services.

It must also be easy to integrate with web and mobile applications using common web standards and tools. 

HTTP REST API communication can handle these needs effectively, as it:
* Uses standard web ports (80/443) and is firewall-friendly.
* Is simple to test, debug, and integrate with existing web services.



### My solution
#### Why RestApi?
It makes it easy to collect all data.
It also makes it easy to share over the web.
It also makes it easy to integrate it in different web applications.
We can also add user authentication to manage, who can read and write data (later on). First we need a user system.

#### How the RestApi is used
We have used FastApi in Python to implement it, because it automatically creates interactive documentation.

__The overview:__

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/8_1.png)

__Creating a person:__

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/8_2.png)

__Reading a person:__

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/8_3.png)


We have also added unit-tests:

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/8_4.png)

1st and 2nd test gives HTTP Status code 200 (ok)
3rd test gives HTTP status code 404 (not found)
4th test gives HTTP status code 400 (bad requestm because we need person_id)

---

# Test of data technologies
#### Incident
The company experiences that sensor and measurement data from IoT devices are only stored temporarily in the server’s memory.

When the system restarts or crashes, all data are lost, meaning the system must maintain 100% uptime to avoid data loss.

However, even highly critical systems typically achieve only 99.999% uptime.

A good idea would be to implement one of these:
* A flat file for fast buffering/logging during failures.
* A SQL database for structured and persistent storage of measurement data.
* A NoSQL storage for fast collection of unstructured IoT data and real-time analysis.


### My solution
#### Why
We have selected to implement a flat_file_db that contains json data.

It is very easy to implement and maintain.

Of course we don't get all the features a known DB could give us.

Currently we don't need much and is okay for small scale projects.

It is also easy to backup and move to other installations.



#### How
Data from our flat_file:
```
{
  "1337": {
    "person_id": "1337",
    "name": "Jens",
    "age": 22
  },
  "2337": {
    "person_id": "2337",
    "name": "Peter",
    "age": 95
  }
}
```

We have implemented the following tests:

![screenshot](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/9_1.png)

* 1st test verifies if the application can start without the flat_file_db.json (it gives a warning, which is good)
* 2nd test verifies if the application can start with a flat_file.db json and read a person.
* 3rd test verifies if the application can update a person
* 4th test verifies if the application can start without the flat_file and create a person and read it.
* 5th test verifies if the application keeps the data after a restart.

---