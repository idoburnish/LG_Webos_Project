import serial
import numpy as np
import os
import socket
import sys
import socketio
import json
import RPi.GPIO as GPIO
import time

arduino = serial.Serial('/dev/ttyACM0',9600)

Sockio = socketio.Client()
Sockio.connect('http://3.35.107.196:5000')
print('Connected!!  My sid : ', Sockio.sid)

windowCount = 0

#서보모터 제어 함수
def servoMotor(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm=GPIO.PWM(pin, 50)

    pwm.start(3) # 초기 시작값
    
    if windowCount % 2 == 1: # 창문이 열려있으면?
        pwm.ChangeDutyCycle(3)
        time.sleep(1) # 서보모터가 이동할만큼의 시간
    else: # 창문이 닫혀있으면?
        pwm.ChangeDutyCycle(7.5) # 3은 0도, 7.5는 직각, 12는 180도
        time.sleep(1)

    pwm.stop() 
    GPIO.cleanup(pin)

# while(1):
#     c=input()
#     if c=='q':
#         break
#     else:
#         c=c.encode('utf-8')
#         arduino.write(c)



Sockio.on('finger_number', function(data) {
    json_data = json.loads(data)
});


print(json_data['fingerNum'])

realfinger = json_data['fingerNum']

if realfinger == '1':
    realfinger=realfinger.encode('utf-8')
    arduino.write(realfinger)    
    
elif realfinger == '2':
#     realfinger=realfinger.encode('utf-8')
#     arduino.write(realfinger) 
    servoMotor(18)
    count += 1
    
elif realfinger == '3':
    realfinger=realfinger.encode('utf-8')
    arduino.write(realfinger)     
    

    
