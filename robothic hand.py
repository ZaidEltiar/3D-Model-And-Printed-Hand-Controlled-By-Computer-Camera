import cv2
import serial
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

arduino = serial.Serial('COM3', 9600)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(maxHands=1)



while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x,y,w,h= hand['bbox']

        #

        d=[0,0,0,0,0]
        tip = [4, 8,12,16,20]

        for i in tip:
            count = (i/4)
            count = count-1
            lmList  = hands[0]['lmList']
            x1,y1,w1 = lmList[0]
            x2,y2,w2 = lmList[i]
            cv2.line(img, (x1,y1),(x2,y2),(255,0,255),4)
            dis = math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))
            cv2.putText(img, f'{int(dis)}cm' , (x+100+int(count*125), y - 27), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            d[int(count)]= dis

        print(d)
        #

        #THUMB
        if d[0]>=190:
            arduino.write(b'2')
        elif d[0]>=130:
            arduino.write(b'1')
        elif d[0]>=0:
            arduino.write(b'0')

        #POINTER
        if d[1]>=230:
            arduino.write(b'5')
        elif d[1]>=180:
            arduino.write(b'4')
        elif d[1]>=130:
            arduino.write(b'l')
        elif d[1]>=0:
            arduino.write(b'3')

        #MIDDLE
        if d[2]>=230:
            arduino.write(b'8')
        elif d[2]>=180:
            arduino.write(b'7')
        elif d[2]>=130:
            arduino.write(b'j')
        elif d[2]>=0:
            arduino.write(b'6')

        #Ring
        if d[3]>=230:
            arduino.write(b'B')
        elif d[3]>=180:
            arduino.write(b'A')
        elif d[3]>=130:
            arduino.write(b'h')
        elif d[3]>=0:
            arduino.write(b'9')

        #Pinky
        if d[4]>=230:
            arduino.write(b'E')
        elif d[4]>=180:
            arduino.write(b'D')
        elif d[4] >= 130:
            arduino.write(b'f')
        elif d[4]>=0:
            arduino.write(b'C')

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)