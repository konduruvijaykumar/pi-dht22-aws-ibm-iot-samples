"""
Note: Remember to start pigpio deamon using the command 'sudo pigpiod'
before running this code as this is needed to gain root access to GPIO pins.
This has to be done every time we restart the PI
"""

import pigpio
import DHT22
from time import sleep

# Import SDK packages
# https://github.com/aws/aws-iot-device-sdk-python/
# Note: During installation use - sudo pip install AWSIoTPythonSDK
# https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSub.py
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("Python_AWS_SDK_RaspberryPI")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("Python_AWS_SDK_RaspberryPI", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint("< Client endpoint Ex. <prefix>.iot.us-east-1.amazonaws.com >", 8883)
# For Websocket
# myMQTTClient.configureEndpoint("< Client endpoint Ex <prefix>.iot.us-east-1.amazonaws.com >", 443)
myMQTTClient.configureCredentials("< Root Certificate File Path >", "< Client private key file Path >", "< Client certificate file Path >")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("< Root Certificate File Path >")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()
#myMQTTClient.publish("test/raspberrypi", "myPayload", 0)
#myMQTTClient.subscribe("test/raspberrypi", 1, customCallback)
#myMQTTClient.unsubscribe("test/raspberrypi")
#myMQTTClient.disconnect()


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

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

myMQTTClient.subscribe("test/raspberrypi", 0, customCallback)

sleep(sleepTime)

while True:
    humidity, temperature = readDHT22()
    print("Humidity:: " + humidity + "%")
    print("Temperature:: " + temperature + "*C")
    # print(humidity + "," + temperature)
    myMQTTClient.publish("test/raspberrypi", "{\"temperature\":"+temperature+",\"humidity\":"+humidity+"}", 0)
    #sleep(sleepTime)
    # adding more sleep time between readings
    sleep(6)
