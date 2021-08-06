## :checkered_flag: 2021 LG Webos Internship :trophy:

## 🏡 HOUSE IN HAND 🖐️ ##  
  몸이 불편한 이들을 위한 손 동작 인식을 사용한 홈 디바이스 제어 시스템
  
  
  This is Home device control system using hand motion recognition for the elderly and disabled.

## 💡 Topic Selection Background

The elderly and disabled can face many difficult situations when they are home alone. Family may not be able to stay with them 24 hours a day. In the face of an aging society  where the number of elderly people is increasing, welfare environments for the elderly and the disabled should be provided. Therefore, we have developed a system that allows them to operate functionality in their house with simple hand movements and to escape from emergency situations.

## :pushpin: Functionality


Based on the OpenCV library, we will implement a system that recognizes the number of fingers that is registered in advance through webcam footage and operates modules connected to raspberry Pi according to the number of fingers or uses smartphone features via Bluetooth communication.

  ### Hand shape example

  -   **Finger one** : control light (LED module)
    
  -   **Finger two** : close the window (Servomotor module) 
   
  -   **Finger three** : emergency call to family or 119 (Twilio API)
 
 

## :computer: System architecture

![image](https://user-images.githubusercontent.com/69456626/128503155-da33096e-6ef3-4435-8b77-a67710f2f435.png)

1) Recognize the user's finger count with webcam and send it to the AWS server via socket.io.
2) The server sends the number of fingers received to two raspberry Pi via socket.io.
3) The first raspberry Pi controls the house.
    - LED and Servo Motors are controlled through a GPIO pin.
    - Also, Emergency messages are sent to caregiver via Twilio API
4) The second raspberry Pi displays a webOS screen.
    - The webOS screen show the number of fingers recognized and the changing home environment.
    - Additionally, the contents of the screen are printed in TTS(Text-to-Speech)

## ❤️ Component

 - AWS server for Socketio communication
 - RaspberryPi 4 for WebOS installation
 - Web App for Notification of Functionality
 - RaspberryPi 4 for module control
 - Server Motor, LED, breadboard
 - Webcam


## 📁 Usage library

 - OPENCV for finger recognition
 - Twilio API for emergency
 - socket.io for communications

## 🧸 Demo
![손가락 인식 사진](https://user-images.githubusercontent.com/72252806/128503668-fd23a40f-ee4d-4bdc-afa4-1a9dfe065000.png)
![집 내부](https://user-images.githubusercontent.com/72252806/128503724-0b843b7e-e039-4eb9-981a-e8924b66f018.png)

