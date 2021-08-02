import serial
import numpy as np
import os
import socket
import sys
import json
import socketio

arduino = serial.Serial('/dev/ttyACM0',9600)
json_data = 0;
realfinger = 0;

Sockio = socketio.Client()
Sockio.connect('http://3.35.107.196:5000')
print('Connected!!  My sid : ', Sockio.sid)


@Sockio.on('finger_send')
def get_num(data):

    print("finger num : ", data['fingerNum'])
    print("status : " ,data['status'])
    realfinger = data['fingerNum']
    arduino.write(data)


#Sockio.disconnect()
# 
# realfinger = json_data['fingerNum']
# 
# if realfinger == '1':
#     realfinger=realfinger.encode('utf-8')
#     arduino.write(realfinger)    
#     
# # elif realfinger == '2':
#     realfinger=realfinger.encode('utf-8')
#     arduino.write(realfinger)    
#     
# elif realfinger == '3':
#     realfinger=realfinger.encode('utf-8')
#     arduino.write(realfinger)     
#     

    