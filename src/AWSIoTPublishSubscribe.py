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

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

myMQTTClient.subscribe("test/raspberrypi", 0, customCallback)

#temperature = str(34.60)
#humidity = str(60.71)

myMQTTClient.publish("test/raspberrypi", "{\"temperature\":"+str(34.60)+",\"humidity\":"+str(60.71)+"}", 0)
