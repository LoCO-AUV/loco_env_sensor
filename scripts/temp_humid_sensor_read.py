#!/usr/bin/env python

# This code is a part of the LoCO AUV project.
# Copyright (C) The Regents of the University of Minnesota

# Maintainer: Junaed Sattar <junaed@umn.edu> and the Interactive Robotics and Vision Laboratory

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import rospy
import Adafruit_DHT
from sensor_msgs.msg import Temperature, RelativeHumidity

DHT_PIN = 21
DHT_SENSOR = Adafruit_DHT.DHT11 #if using DHT11 sensor
#DHT_SENSOR = Adafruit_DHT.DHT22 #if using DHT22 sensor

""" Creates TempHumid message """
def readSensor(sensor, datapin):
    humid, temp = Adafruit_DHT.read(sensor, datapin)
    tempMsg = Temperature()
    humidMsg = RelativeHumidity()
    time = rospy.Time.now()
    if temp is not None: 
        tempMsg.header.stamp = time
        tempMsg.temperature = temp
        tempMsg.variance = 0
    if humid is not None:
        humidMsg.header.stamp = time
        humidMsg.relative_humidity = humid
        humidMsg.variance = 0
    return (tempMsg,humidMsg)

def temp_humid_sensor():
    """ Takes in the temperature and humidity of the environment and publishes them on
        two respective topics every two seconds. If the temperature and humidity data
        are invalid, publish a warning. """
    rospy.init_node('temp_humid_sensor', anonymous=True)
    tempPub = rospy.Publisher('/loco/env_sensor/left/temperature', Temperature, queue_size = 50)
    humidPub = rospy.Publisher('/loco/env_sensor/left/humidity', RelativeHumidity, queue_size = 50)
    rate = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        msgs = readSensor(DHT_SENSOR, DHT_PIN)
        tempMsg = msgs[0]
        humidMsg = msgs[1]
        if tempMsg.header.stamp.secs is not 0:
            tempPub.publish(tempMsg)
            rospy.loginfo('Temperature of left tube: %d C' % tempMsg.temperature)
        if humidMsg.header.stamp.secs is not 0:
            humidPub.publish(humidMsg)
            rospy.loginfo('Relative humidity of left tube: %d%%' % humidMsg.relative_humidity)
        else: #Warn if reading the sensor fails
            rospy.logwarn('Failed to read Temperature/Humidity sensor') 
        rate.sleep()

if __name__ == '__main__':
    try:
        temp_humid_sensor()
    except rospy.ROSInterruptException:
        pass
