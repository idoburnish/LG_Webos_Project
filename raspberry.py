import serial
import numpy as np
import os
import socket
import sys
import socketio
import json

arduino = serial.Serial('/dev/ttyACM0',9600)

Sockio = socketio.Client()
Sockio.connect('http://3.35.107.196:5000')
print('Connected!!  My sid : ', Sockio.sid)


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
    realfinger=realfinger.encode('utf-8')
    arduino.write(realfinger)    
    
elif realfinger == '3':
    realfinger=realfinger.encode('utf-8')
    arduino.write(realfinger)     
    

    