
import logging
import time
import argparse
import json
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)


pinTrigerL = 22
pinEchoL = 23
pinTrigerR = 24
pinEchoR  = 26


# trig (cable amarillo en el prototipo)
GPIO.setup(pinTrigerL, GPIO.OUT)
# echo (cable verde en el prototipo)
GPIO.setup(pinEchoL, GPIO.IN)
# trig (cable amarillo en el prototipo)
GPIO.setup(pinTrigerR, GPIO.OUT)
# echo (cable verde en el prototipo)
GPIO.setup(pinEchoR, GPIO.IN)

try:
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
        
        if distanciaL < 0.3:
           comando ="back"
        else :
            if distanciaL > 1:
                comando ="front"
        print(str(endR)," ",str(startR))
        print(str(endL)," ",str(startL))        
        print ("Distancia al left =", str(distanciaL))
        print ("Distancia al rigth =", str(distanciaR))
  
        
        
        
except KeyboardInterrupt:
    print("\nFin del programa")
    GPIO.output(pinTrigerL, False)
    GPIO.cleanup()