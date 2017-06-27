"""
Note: Remember to start pigpio deamon using the command 'sudo pigpiod'
before running this code as this is needed to gain root access to GPIO pins.
This has to be done every time we restart the PI
"""

import pigpio
import DHT22
from time import sleep

#import getopt
#import signal
#import time
import sys
#import json
import ibmiotf.application
import ibmiotf.device

# https://github.com/ibm-watson-iot/iot-python
# Note: During installation use - sudo pip install ibmiotf
# https://console.bluemix.net/docs/services/IoT/devices/libraries/python.html#python
# https://github.com/ibm-watson-iot/iot-python/blob/master/samples/customMessageFormat/customCodecSample.py
# https://github.com/ibm-watson-iot/iot-python/blob/master/samples/simpleApp/simpleApp.py
# https://console.bluemix.net/docs/services/IoT/applications/libraries/python.html#python

try:
    options = {
        "org": "<Organization-ID>",
        "type": "<Device-Type>",
        "id": "<Device-ID>",
        "auth-method": "token",
        "auth-token": "<Authentication-Token>",
        "clean-session": "true"
    }
	client = ibmiotf.device.Client(options)
	# print(options.get("org"))
except ibmiotf.ConnectionException  as e:
	print(str(e))
	sys.exit()

# connect to IBM IoT platform
client.connect()


# Intite GPIO for pigpio
pi = pigpio.pi()
# Setup the sensor
dht22 = DHT22.sensor(pi, 27) # use the actual GPIO pin name
dht22.trigger()

# We have sleep time above 2 seconds bcoz interval for DHT22 sensor to generate data is 2 secs
sleepTime = 3

def readDHT22():
    # Get a reading
    dht22.trigger()
    # save the data
    humidity = '%.2f' % (dht22.humidity())
    temperature = '%.2f' % (dht22.temperature())
    return (humidity, temperature)

sleep(sleepTime)


numberOfIterations = 30;
myQosLevel=0
# myData={'temperature' : 34.60, 'humidity' : 60.71}
# myData={"temperature" : 34.60, "humidity" : 60.71}
# single or double quote produce same paylod with single quote

#while True:
    #humidity, temperature = readDHT22()
    #print("Humidity:: " + humidity + "%")
    #print("Temperature:: " + temperature + "*C")
    # print(humidity + "," + temperature)
    #client.publishEvent("raspberry-pi-sensors", "json", "{\"temperature\":"+temperature+",\"humidity\":"+humidity+"}", myQosLevel)
    #sleep(sleepTime)

while numberOfIterations > 0:
    humidity, temperature = readDHT22()
    print("Humidity:: " + humidity + "%")
    print("Temperature:: " + temperature + "*C")
    # print(humidity + "," + temperature)
    client.publishEvent("raspberry-pi-sensors", "json", "{\"temperature\":"+temperature+",\"humidity\":"+humidity+"}", myQosLevel)
    #sleep(sleepTime)
    # adding more sleep time between readings
    sleep(6)
    numberOfIterations = numberOfIterations-1

sleep(sleepTime)
# print(myData)
client.disconnect()
