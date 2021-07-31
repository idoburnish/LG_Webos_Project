import cv2 as cv
import numpy as np
import os
from shapely.geometry import Polygon
import socket
import sys
import socketio
#import requests
import json

# cascade를 사용하여 얼굴검출하여 얼굴부분 제거
# 검출된 얼굴 영역을 기준으로 일정 영역의 픽셀을 검은색으로 바꿈
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects


# return값은 얼굴 영역이 검은색으로 처리된 영상
def removeFaceAra(img, cascade):
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  gray = cv.equalizeHist(gray)
  rects = detect(gray, cascade)

  height,width = img.shape[:2]

  for x1, y1, x2, y2 in rects:
      cv.rectangle(img, (x1-10, 0), (x2+10, height), (0,0,0), -1)

  return img


#영상의 살색 영역을 검출하여 바이너리 이미지 생성(흑백)
def make_mask_image(img_bgr):
    
  img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)

  #img_h,img_s,img_v = cv.split(img_hsv)

  low = (0, 30, 0)
  high = (15, 255, 255)

  img_mask = cv.inRange(img_hsv, low, high)
  return img_mask

  
def distanceBetweenTwoPoints(start, end):

  x1,y1 = start
  x2,y2 = end
 
  return int(np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)))


def calculateAngle(A, B):

  A_norm = np.linalg.norm(A)
  B_norm = np.linalg.norm(B)
  C = np.dot(A,B)

  angle = np.arccos(C/(A_norm*B_norm))*180/np.pi
  return angle

  # 검출된 contour영역에서 가장 큰 영역을 찾음 = 손
def findMaxArea(contours):
  
  max_contour = None
  max_area = -1


  for contour in contours:
    area = cv.contourArea(contour) # 윤곽선 배열로 윤곽선의 면적 계산

    x,y,w,h = cv.boundingRect(contour) # 윤곽선 배열로 최소 크기 사각형 계산 (좌표, 가로폭, 세로폭)

    if (w*h)*0.4 > area:
        continue

    if w > h:
        continue

    if area > max_area:
      max_area = area
      max_contour = contour
  
  if max_area < 10000:
    max_area = -1

  return max_area, max_contour


  # 선의 방향이 바뀌는 지점을 손가락으로 인식
  # convexHull은 꼭짓점끼리 직선으로 연결한 선
def getFingerPosition(max_contour, img_result, debug):
  points1 = []

  # STEP 6-1
  M = cv.moments(max_contour)

  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])


  max_contour = cv.approxPolyDP(max_contour,0.02*cv.arcLength(max_contour,True),True)
  hull = cv.convexHull(max_contour)

  for point in hull:
    if cy > point[0][1]:
      points1.append(tuple(point[0])) 

  if debug:
    cv.drawContours(img_result, [hull], 0, (0,255,0), 2)
    for point in points1:
      cv.circle(img_result, tuple(point), 15, [ 0, 0, 0], -1)



  # STEP 6-2
  # 손가락 사이에 위치한 defect를 이용하여
  # 뾰족한 부분을 손가락 후보로 검출
  # 손가락 하나만 있을 때는 검출할 수 없다는 문제..
  max_contour2 = np.squeeze(max_contour)
  global polygon
  polygon = Polygon(max_contour2)

  if polygon.is_simple == False:
    return -1,None

  hull = cv.convexHull(max_contour, returnPoints=False)
  defects = cv.convexityDefects(max_contour, hull)

  if defects is None:
    return -1,None

  points2=[]
  for i in range(defects.shape[0]):
    s,e,f,d = defects[i, 0]
    start = tuple(max_contour[s][0])
    end = tuple(max_contour[e][0])
    far = tuple(max_contour[f][0])

    angle = calculateAngle( np.array(start) - np.array(far), np.array(end) - np.array(far))

    if angle < 90:
      if start[1] < cy:
        points2.append(start)
      
      if end[1] < cy:
        points2.append(end)

  if debug:
    cv.drawContours(img_result, [max_contour], 0, (255, 0, 255), 2)
    for point in points2:
      cv.circle(img_result, tuple(point), 20, [ 0, 255, 0], 5)


  # STEP 6-3
  # convexHull을 이용하여 검출한 손가락 후보와 defect를 사용하여 검출한 손가락 후보를 합쳐서 사용
  points = points1 + points2
  points = list(set(points))


  # STEP 6-4
  # 검출된 포인트의 좌우에 있는 포인트가 이루는 각이 90도 이하인 경우에만 손가락으로 인식
  # 90도 이상은 구부린 손가락이 잘못 인식된 것이라서 제외함
  new_points = []
  for p0 in points:
    
    i = -1
    for index,c0 in enumerate(max_contour):
      c0 = tuple(c0[0])

      if p0 == c0 or distanceBetweenTwoPoints(p0,c0)<20:
        i = index
        break

    if i >= 0:
      pre = i - 1
      if pre < 0:
        pre = max_contour[len(max_contour)-1][0]
      else:
        pre = max_contour[i-1][0]
      
      next = i + 1
      if next > len(max_contour)-1:
        next = max_contour[0][0]
      else:
        next = max_contour[i+1][0]


      if isinstance(pre, np.ndarray):
            pre = tuple(pre.tolist())
      if isinstance(next, np.ndarray):
        next = tuple(next.tolist())

        
      angle = calculateAngle( np.array(pre) - np.array(p0), np.array(next) - np.array(p0))     

      if angle < 90:
        new_points.append(p0)
  
  return 1,new_points



def process(img_bgr, debug):

  img_result = img_bgr.copy()
  cnt = 0

  # STEP 1 : 얼굴영역 검은색으로 처리
  img_bgr = removeFaceAra(img_bgr, cascade)


  # STEP 2 : 흑백영상 처리
  img_binary = make_mask_image(img_bgr)


  # STEP 3 : 검출된 살색 영역에 검은 구멍이 있는 경우를 없앰
  kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
  img_binary = cv.morphologyEx(img_binary, cv.MORPH_CLOSE, kernel, 1)
  cv.imshow("Binary", img_binary)


  # STEP 4 : 바이너리 이미지에서 contour 검출(바이너리 이미지에서 흰색 영역의 선)
  contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  # 흰색 영역의 index 0에 해당하는 컨투어를 3의 두께로 윤곽선 그리기
  if debug:
    for cnt in contours:
      cv.drawContours(img_result, [cnt], 0, (255, 0, 0), 3)  
    

  # STEP 5 : # 검출된 contour영역에서 가장 큰 영역을 찾음 = 손
  max_area, max_contour = findMaxArea(contours)  

  if max_area == -1:
    return img_result, cnt

  # 손의 index 0에 해당하는 컨투어를 3의 두께로 윤곽선 그리기
  if debug:
    cv.drawContours(img_result, [max_contour], 0, (0, 0, 255), 3)  


  # STEP 6 : 바이너리 이미지 윤곽, 손 윤곽을 같이 보고 손가락 찾기
  ret,points = getFingerPosition(max_contour, img_result, debug)
  

  # STEP 7
  if ret > 0 and len(points) > 0:
    cnt = len(points)
    for point in points:
      cv.circle(img_result, point, 20, [ 255, 0, 255], 5)

  
  return img_result, cnt

current_file_path = os.path.dirname(os.path.realpath(__file__))
cascade = cv.CascadeClassifier(cv.samples.findFile("haarcascade_frontalface_alt.xml"))

cap = cv.VideoCapture(0,cv.CAP_DSHOW)

flag = 0

#URL = "http://3.35.107.196:5000"
# URL = "http://www.naver.com"

Sockio = socketio.Client()
Sockio.connect('http://3.35.107.196:5000')
print('Connected!!  My sid : ', Sockio.sid)


while True:

  ret,img_bgr = cap.read() # 비디오 한 프레임씩 읽기
  
  if ret == False:
    break

  img_result, counts = process(img_bgr, debug=False)
  
  key = cv.waitKey(1) 
  if key== 27:
      break
  
  if (flag != counts) and (counts!=0):
    dataf = {'success':True, 'numbers':counts}
    dataj = json.dumps(dataf)
    print(dataj)

    Sockio.emit('finger_number',dataj)
    
    flag = counts

  cv.imshow("Result", img_result)
  


# cap객체 해제, 생성한 윈도우 제거
cap.release()
cv.destroyAllWindows()

# 소켓 연결 끊기
Sockio.disconnect()

# python opencv.py