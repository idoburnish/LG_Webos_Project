import serial
import numpy as np
import os
import socket
import sys
import json
import socketio

import RPi.GPIO as GPIO
import time

from twilio.rest import Client

#arduino = serial.Serial('/dev/ttyACM0',9600)
json_data = 0;
realfinger = 0;

Sockio = socketio.Client()
Sockio.connect('http://3.35.107.196:5000')
print('Connected!!  My sid : ', Sockio.sid)


@Sockio.on('finger_send')
def get_num(data):

    print("finger num : ", data['fingerNum'])
    print("status : " ,data['status'])
    realfinger = int(data['fingerNum'])
    realstatus = int(data['status'])

    if realfinger == 1:
        if realstatus == 0:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(18,GPIO.OUT)
            GPIO.output(18,True)
        else :
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(18,GPIO.OUT)
            GPIO.cleanup(18)

    elif realfinger == 2 :
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        pwm=GPIO.PWM(16, 50)

        #c = int(input())

        if realstatus==0 :
            #window open
            pwm.start(3) 
            time.sleep(1)
            pwm.ChangeDutyCycle(7.5) 
            time.sleep(1)
        else:
            #window close
            pwm.start(7.5)
            time.sleep(1)
            pwm.ChangeDutyCycle(3)
            time.sleep(1)

        pwm.stop() 
        GPIO.cleanup(16)
        time.sleep(1)
    
    elif realfinger == 3 :  
        account_sid = 'AC65c19389ae3ca4db17cca063d2bccb0d'
        auth_token = '71732d24b9ce348f6e5ffbb5e5a1df2c'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to = "+821020265143",
            from_ = "+18562216356",
            body = "I'm in an emergency. \nMy current location is KNU IT5. \nPlease help me."
        )
        print(message.sid)
        
    