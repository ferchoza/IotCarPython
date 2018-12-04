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
pinMotorBR1 = 19
pinMotorBR2 = 21



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
#host = "a1io5eo0eh1c6a-ats.iot.us-east-1.amazonaws.com"
#certPath = "/home/pi/demo/cert/"
certPath = "/home/pi/demo/demo-cert/"
clientId = "sajith-pi-demo-publisher"
topic = "LED"


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
#myAWSIoTMQTTClient.configureCredentials("{}root-CA.crt".format(certPath), "{}040198d3e3-private.pem.key".format(certPath), "{}040198d3e3-certificate.pem.crt".format(certPath))
myAWSIoTMQTTClient.configureCredentials("{}aws-root-cert.pem".format(certPath), "{}private-key.pem.key".format(certPath), "{}iot-cert.pem.crt".format(certPath))

def go():
     print('ir hacia Delante')
     GPIO.output(pinMotorFL1,GPIO.HIGH)
     GPIO.output(pinMotorFL2,GPIO.LOW)
     GPIO.output(pinMotorFR1,GPIO.HIGH)
     GPIO.output(pinMotorFR2,GPIO.LOW)
     
     GPIO.output(pinMotorBL1,GPIO.HIGH)
     GPIO.output(pinMotorBL2,GPIO.LOW)
     GPIO.output(pinMotorBR1,GPIO.HIGH)
     GPIO.output(pinMotorBR2,GPIO.LOW)     

def go_back():
    print('ir hacia Atras')
    GPIO.output(pinMotorFL2,GPIO.HIGH)
    GPIO.output(pinMotorFL1,GPIO.LOW)
    GPIO.output(pinMotorFR2,GPIO.HIGH)
    GPIO.output(pinMotorFR1,GPIO.LOW)
     
    GPIO.output(pinMotorBL2,GPIO.HIGH)
    GPIO.output(pinMotorBL1,GPIO.LOW)
    GPIO.output(pinMotorBR2,GPIO.HIGH)
    GPIO.output(pinMotorBR1,GPIO.LOW)

def go_left():
    print('ir hacia izquierda')
          
    GPIO.output(pinMotorFL2,GPIO.HIGH)
    GPIO.output(pinMotorFL1,GPIO.LOW)
    GPIO.output(pinMotorFR1,GPIO.HIGH)
    GPIO.output(pinMotorFR2,GPIO.LOW)
     
    GPIO.output(pinMotorBL2,GPIO.HIGH)
    GPIO.output(pinMotorBL1,GPIO.LOW)
    GPIO.output(pinMotorBR1,GPIO.HIGH)
    GPIO.output(pinMotorBR2,GPIO.LOW)
    
def  go_right():
     print('ir hacia Derecha')
     GPIO.output(pinMotorFL1,GPIO.HIGH)
     GPIO.output(pinMotorFL2,GPIO.LOW)
     GPIO.output(pinMotorFR2,GPIO.HIGH)
     GPIO.output(pinMotorFR1,GPIO.LOW)
     GPIO.output(pinMotorBL1,GPIO.HIGH)
     GPIO.output(pinMotorBL2,GPIO.LOW)
     GPIO.output(pinMotorBR2,GPIO.HIGH)
     GPIO.output(pinMotorBR1,GPIO.LOW)

def        stop():     
           print('ir hacia Atras')
           GPIO.output(pinMotorFL2,GPIO.LOW)
           GPIO.output(pinMotorFL1,GPIO.LOW)
           GPIO.output(pinMotorFR2,GPIO.LOW)
           GPIO.output(pinMotorFR1,GPIO.LOW)
     
           GPIO.output(pinMotorBL2,GPIO.LOW)
           GPIO.output(pinMotorBL1,GPIO.LOW)
           GPIO.output(pinMotorBR2,GPIO.LOW)
           GPIO.output(pinMotorBR1,GPIO.LOW)
           
def go_abismo():
    stop()
    go_back()
    time.sleep(1)
    go_left()
    time.sleep(1)
    
def run_motor(self, params, packet):
 
 print("oayload %s" % packet.payload)
 
 data = json.loads(packet.payload.decode()) 

 ruta = data['light']
      
 if ruta =='front':
    go()
     
 else :
    if ruta =='front-right':
       go_right()
    else :
         
      if ruta =='front-left':
         go_left() 
          
      else :
         if ruta =='back':
          go_back()
          
         else :
          if ruta =='stop':
             stop()
          else :
              if ruta =='abismo':
                 go_abismo()
 
 
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.subscribe("LED", 1, run_motor)

while True:
        time.sleep(1)

       
myAWSIoTMQTTClient.disconnect()
