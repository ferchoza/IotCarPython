from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import RPi.GPIO as GPIO


pinMotorFL1 = 11
pinMotorFL2 = 12
pinMotorFR1 = 13
pinMotorFR2 = 15

pinMotorBL1 = 16
pinMotorBL2 = 18
pinMotorBR1 = 29
pinMotorBR2 = 31

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pinMotorFL1,GPIO.OUT)
GPIO.setup(pinMotorFL2,GPIO.OUT)
GPIO.setup(pinMotorFR1,GPIO.OUT)
GPIO.setup(pinMotorFR2,GPIO.OUT)
GPIO.setup(pinMotorBL1,GPIO.OUT)
GPIO.setup(pinMotorBL2,GPIO.OUT)
GPIO.setup(pinMotorBR1,GPIO.OUT)
GPIO.setup(pinMotorBR2,GPIO.OUT)

host = "a27b8oybks6hla-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/pi/demo/demo-cert/"
clientId = "sajith-pi-demo-publisher"
topic = "c"


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}aws-root-cert.pem".format(certPath), "{}private-key.pem.key".format(certPath), "{}iot-cert.pem.crt".format(certPath))



def run_motor(self, params, packet):
 
 print("oayload %s" % packet.payload)
 
 data = json.loads(packet.payload.decode()) 

 ruta = data['ruta']
      
 if ruta =='F':
     print('ir hacia Delante')
     GPIO.output(pinMotorFL1,GPIO.HIGH)
     GPIO.output(pinMotorFL2,GPIO.LOW)
     GPIO.output(pinMotorFR1,GPIO.HIGH)
     GPIO.output(pinMotorFR2,GPIO.LOW)
     
     GPIO.output(pinMotorBL1,GPIO.HIGH)
     GPIO.output(pinMotorBL2,GPIO.LOW)
     GPIO.output(pinMotorBR1,GPIO.HIGH)
     GPIO.output(pinMotorBR2,GPIO.LOW)
     
 else :
    if ruta =='R':
     print('ir hacia Derecha')
     GPIO.output(pinMotorFL1,GPIO.HIGH)
     GPIO.output(pinMotorFL2,GPIO.LOW)
     GPIO.output(pinMotorFR2,GPIO.HIGH)
     GPIO.output(pinMotorFR1,GPIO.LOW)
     
     GPIO.output(pinMotorBL1,GPIO.HIGH)
     GPIO.output(pinMotorBL2,GPIO.LOW)
     GPIO.output(pinMotorBR2,GPIO.HIGH)
     GPIO.output(pinMotorBR1,GPIO.LOW)
    else :
         
      if ruta =='L':
          print('ir hacia izquierda')
          
          GPIO.output(pinMotorFL2,GPIO.HIGH)
          GPIO.output(pinMotorFL1,GPIO.LOW)
          GPIO.output(pinMotorFR1,GPIO.HIGH)
          GPIO.output(pinMotorFR2,GPIO.LOW)
     
          GPIO.output(pinMotorBL2,GPIO.HIGH)
          GPIO.output(pinMotorBL1,GPIO.LOW)
          GPIO.output(pinMotorBR1,GPIO.HIGH)
          GPIO.output(pinMotorBR2,GPIO.LOW)
          
      else :
         if ruta =='B':
          print('ir hacia Atras')
          GPIO.output(pinMotorFL2,GPIO.HIGH)
          GPIO.output(pinMotorFL1,GPIO.LOW)
          GPIO.output(pinMotorFR2,GPIO.HIGH)
          GPIO.output(pinMotorFR1,GPIO.LOW)
     
          GPIO.output(pinMotorBL2,GPIO.HIGH)
          GPIO.output(pinMotorBL1,GPIO.LOW)
          GPIO.output(pinMotorBR2,GPIO.HIGH)
          GPIO.output(pinMotorBR1,GPIO.LOW)
          
         else :
          if ruta =='S':
           print('ir hacia Atras')
           GPIO.output(pinMotorFL2,GPIO.LOW)
           GPIO.output(pinMotorFL1,GPIO.LOW)
           GPIO.output(pinMotorFR2,GPIO.LOW)
           GPIO.output(pinMotorFR1,GPIO.LOW)
     
          GPIO.output(pinMotorBL2,GPIO.LOW)
          GPIO.output(pinMotorBL1,GPIO.LOW)
          GPIO.output(pinMotorBR2,GPIO.LOW)
          GPIO.output(pinMotorBR1,GPIO.LOW)
 
 
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.subscribe("miTema", 1, run_motor)
# Publish to the same topic in a loop forever
loopCount = 0
while True:
    message = {}
    message['message'] = "demo-topic-sample-message"
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(10)
myAWSIoTMQTTClient.disconnect()