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

pinTrigerL = 22
pinEchoL = 23
pinTrigerR = 24
pinEchoR  = 26

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pinMotorFL1,GPIO.OUT)
GPIO.setup(pinMotorFL2,GPIO.OUT)
GPIO.setup(pinMotorFR1,GPIO.OUT)
GPIO.setup(pinMotorFR2,GPIO.OUT)
GPIO.setup(pinMotorBL1,GPIO.OUT)
GPIO.setup(pinMotorBL2,GPIO.OUT)
GPIO.setup(pinMotorBR1,GPIO.OUT)
GPIO.setup(pinMotorBR2,GPIO.OUT)


# trig (cable amarillo en el prototipo)
GPIO.setup(pinTrigerL, GPIO.OUT)
# echo (cable verde en el prototipo)
GPIO.setup(pinEchoL, GPIO.IN)
# trig (cable amarillo en el prototipo)
GPIO.setup(pinTrigerR, GPIO.OUT)
# echo (cable verde en el prototipo)
GPIO.setup(pinEchoR, GPIO.IN)

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



def run_motor(self, params, packet):
 
 print("oayload %s" % packet.payload)
 
 data = json.loads(packet.payload.decode()) 

 ruta = data['light']
      
 if ruta =='front':
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
    if ruta =='front-right':
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
         
      if ruta =='front-left':
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
         if ruta =='back':
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
          if ruta =='stop':
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

myAWSIoTMQTTClient.subscribe("LED", 1, run_motor)
# Publish to the same topic in a loop forever
loopCount = 0
while True:
        startL = 0
        endL = 0
        startR = 0
        endR = 0
        # Configura el sensor
        GPIO.output(pinTrigerL, False)
        GPIO.output(pinTrigerR, False)
        time.sleep(2) # 2 segundos para hacer el programa usable
        # Empezamos a medir
        GPIO.output(pinTrigerL, True)
        time.sleep(10*10**-6) #10 microsegundos
        GPIO.output(pinTrigerL, False)
        # Flanco de 0 a 1 = inicio
        while GPIO.input(pinEchoL) == GPIO.LOW:
            startL = time.time()
        while GPIO.input(pinEchoL) == GPIO.HIGH:
            endL = time.time()
      
        GPIO.output(pinTrigerR, True)
        time.sleep(10*10**-6) #10 microsegundos
        GPIO.output(pinTrigerR, False)
       
        while GPIO.input(pinEchoR) == GPIO.LOW:
            startR = time.time()
        while GPIO.input(pinEchoR) == GPIO.HIGH:
            endR = time.time()
            
            
       

        # el tiempo que devuelve time() estÃ¡ en segundos
        distanciaL = (endL-startL) * 343 / 2
        distanciaR = (endR-startR) * 343 / 2
      
        if distanciaL < 0.1 and distanciaR < 0.1:
           comando ="stop"
        else :
          if distanciaL < 0.3 and distanciaR < 0.3:
             comando ="back"
          else :
             if distanciaL > 1 and distanciaR > 1:
                comando ="front"
             else :
                 if distanciaL < distanciaR:
                    comando ="front-right"
                 else :
                     if distanciaL > distanciaR:
                        comando ="front-left"
                
        print ("Distancia al objeto =", str(distanciaL))
                        
        print ("Distancia al objeto =", str(distanciaR))
        message = {}
        message['light'] = comando
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        print('Published topic %s: %s\n' % (topic, messageJson))
        time.sleep(1)
        
myAWSIoTMQTTClient.disconnect()
