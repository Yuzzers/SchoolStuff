# What is this repository for?
This is for teaching different protocols on Zealand Business Academy (zealand.dk)

Prototypes are for:

* UDP
* TCP
* MQTT
* HTTP

# Installation (Before running test)

* `pip install pytest`
* pip install amqtt
* pip install asyncio
* pip install paho-mqtt
* pip install pytest-timeout

## Run in terminal:
* pytest -v -s 

## Run in VSCodium:
* **[shift]+[ctrl]+b** and select **"pytest run all"**
* Use **@pytest.mark.focus** on and select **"pytest focus"** to only run the test case in focus

# Narrative
The students have to create their own narrative, so it can be more relevant for them. 

### Company examples
| Company&nbsp;Logo | Company why & how |
| --- | --- |
| ![company 1 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_1.png) | **Why:** Our goal is to help farmers optimize their crop yields and promote more sustainable farming practices by using data-driven insights . **How:** We are developing IoT-based sensors that measure soil moisture, fertilizer levels, and temperature. These sensors transmit real-time data to a cloud-based platform where farmers can access analytics and recommendations.|
| ![company 2 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_2.png) | **Why:** : The purpose of our company is to ensure the safe and efficient transport of sensitive goods such as medicine and perishable food. **How:**We are developing IoT devices that monitor temperature, humidity, and location of goods during transportation. These devices send real-time data to a cloud platform where alerts and insights are generated to support proactive decision-making. |
| ![company 3 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_3.png) | **Why:** : Our purpose is to improve the quality of home care by giving healthcare professionals access to real-time patient data. **How:**We are developing IoT devices that can monitor patients’ pulse, blood pressure, and activity levels. The devices securely transmit data to a cloud platform, where caregivers and medical staff can access it through a dashboard. |

## Incidents
Each teaching material will come from an incident.

Please write your incidents solutions like this (in your own repo and README.file)

### 3 Examples: Test of UDP protocol (for each company)
![company 1 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_1.png)

We collect data from 1000 soil sensors that send data every 10 seconds.
Each sensor measures soil moisture, fertilizer levels, and temperature, and transmits data continuously to our cloud platform.

#### Why UDP?

We chose UDP (User Datagram Protocol) because:
* Sensor readings are frequent and lightweight – a few bytes per packet.
* Occasional packet loss is acceptable (soil values do not change drastically second-to-second).
* Low latency and reduced network overhead compared to TCP.
* It scales efficiently with 1000 distributed sensors sending periodic updates.

#### How UDP is Used
Each sensor sends a small UDP packet with:
```
{
  "sensor_id": "farm-001",
  "timestamp": "2025-09-23T14:52:05Z",
  "soil_moisture": 32.5,
  "fertilizer_level": 14.2,
  "temperature": 21.8
}
```
Packets are transmitted to a UDP server endpoint

---
![company 2 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_2.png)

We collect data from 100 sensors that send data every 1 second.
Each sensor monitors temperature, humidity, and location inside transport containers.

#### We use UDP because:
* Transport monitoring requires near real-time alerts with minimal delay.
* Each message is small and frequent (sent once per second).
* If a packet is lost, a new one arrives one second later – making retries unnecessary.
* Lower bandwidth and CPU usage on constrained IoT devices.

#### How UDP is used
Each IoT tracker sends a UDP datagram to our monitoring service.

Payload contains:
```
{
  "device_id": "truck-42",
  "timestamp": "2025-09-23T14:55:12Z",
  "temperature": 4.3,
  "humidity": 72.1,
  "gps_location": {
    "lat": 52.520008,
    "lon": 13.404954
  }
}
```
UDP ensures lightweight, fast updates, while reliability is handled at the application level (e.g., redundant devices in a container, validation rules).

---
![company 3 logo](https://bitbucket.org/BartlomiejRohardWarszawski/client_server_protocols/raw/main/images/company_3.png)

We collect data from 10 wearable medical sensors that send data every 100 milliseconds.
Each device monitors pulse, blood pressure, and activity levels.

#### We use UDP because:
* Ultra-low latency is required for real-time health monitoring.
* Sensors transmit high-frequency updates (10 per second per device).
* Small packet loss is tolerable, since new data arrives almost instantly.
* TCP handshakes and retransmissions would introduce unacceptable delays.

#### How UDP is used
Each IoT tracker sends a UDP datagram to our monitoring service.

Payload contains:
```
{
  "patient_id": "patient-007",
  "timestamp": "2025-09-23T14:56:30Z",
  "pulse": 78,
  "blood_pressure": {
    "systolic": 118,
    "diastolic": 76
  },
  "activity_level": "moderate"
}
```
UDP ensures lightweight, fast updates, while reliability is handled at the application level (e.g., redundant devices in a container, validation rules). 