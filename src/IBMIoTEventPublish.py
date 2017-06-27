import sys
#import getopt
#import signal
#import time
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

client.connect()
myQosLevel=0
myData={'temperature' : 34.60, 'humidity' : 60.71}
# myData={"temperature" : 34.60, "humidity" : 60.71}
# single or double quote produce same paylod with single quote
client.publishEvent("raspberry-pi-sensors", "json", myData, myQosLevel)
# print(myData)
client.disconnect()
