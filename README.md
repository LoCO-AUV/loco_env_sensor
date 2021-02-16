# loco_env_sensor
Includes ROS nodes to handle various sensors inside LoCO tube enclosure. Currently implements only a `temp_humid_sensor` node for monitoring temperature and relative humidity.

#### Requirements
The `temp_humid_sensor` node is run on a Raspberry Pi 4 running:
- ROS Melodic
- Python 2.7, with `Adafruit_DHT` library installed

Node may also work with ROS Noetic and/or Python 3, but is untested.

#### Hardware
A DHT11 or DHT22 temperature-humidity sensor is required. Info on these sensors can be found on the AdaFruit website [here](https://cdn-learn.adafruit.com/downloads/pdf/dht.pdf). For ease of use, it is recommended to use a DHT sensor pre-installed onto a PCB board such as the [KY-015](https://arduinomodules.info/ky-015-temperature-humidity-sensor-module/).

Pinouts for the bare-bones DHT sensor is as follows, from left to right with the front facing up:
* VCC/Power
* Data
* Unused
* Ground

Both DHT11 and DHT22 have identical pinouts.

Pinouts for the KY-015, from left to right:
* Data
* VCC/Power
* Ground

#### Usage
- Connect the power, data, and ground pins to the RPi using jumper cables (a 10k pullup resistor needs to be added between power and data if not using a PCB board).
- Specify the GPIO pin used for reading data in line 6 of `temp_humid_sensor_read.py`.
- Comment/uncomment `DHT_SENSOR` lines 7-8 as necessary depending on which DHT sensor is used.
- During use, `temp_humid_sensor` node reads sensor every 2 seconds, publishes the temperature/humidity measurements onto corresponding topics `/loco/env_sensor/left/temperature` and `/loco/env_sensor/left/humidity`.
