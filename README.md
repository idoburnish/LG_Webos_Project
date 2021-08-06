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
   
  -   **Finger three** : emergency call to family or 119
 
 
## :computer: Component

 - Socket io 통신을 위한 AWS server
 - WebOS 설치 RaspberryPi 4
 - 기능 작동 여부 알림을 위한 Web App
 - 모듈 제어를 위한 RaspberryPi 4
 - Server Motor, LED, breadboard
 - Webcam


## 📁 Usage library

 - 손가락 인식을 위한 OPENCV 
 - 긴급 연락을 위한 Twilio API 

## ❤️ System explain
![image](https://user-images.githubusercontent.com/69456626/128502212-2fd4ac01-6409-4e11-ac31-d70b6722e447.png)
1) Recognize the user's finger count with webcam and send it to the AWS server via socket.io.
2) The server sends the number of fingers received to two raspberry Pi via socket.io.
3) The first raspberry Pi controls the house.
  - LED and Servo Motors are controlled through a GPIO pin.
  - Also, Emergency messages are sent to caregiver via Twilio API
4) The second raspberry Pi displays a webOS screen.
  - The webOS screen show the number of fingers recognized and the changing home environment.
  - Additionally, the contents of the screen are printed in TTS(Text-to-Speech)

## 🧸 Demo
