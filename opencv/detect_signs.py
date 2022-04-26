import cv2
import time
import os
import mediapipe as mp
import cv_modulo as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4,8,12,16,20]

def detect_sign(fingers):
    if fingers == [1,0,0,0,0]:
        return 'A'
    if fingers == [0,1,1,1,1]:
        return 'B'
 #   if fingers == [1,1,0,0,1]:
 #       return 'I love you'
    if fingers == [1,1,1,1,1]:
        return 'Oi!'
    if fingers == [0,0,1,1,1]:
        return 'F'


def how_many_fingers(fingers):
    counter = 0
    for i in fingers:
        if i == 1:
            counter += 1
    return counter;


while True:
    s, img = cap.read()

    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #lmList = lista de todos as coordenadas dos dedos, dá p fazer muita coisa com isso
    print(lmList)
    
   

    
    if len(lmList) != 0:
        fingers = []

    
        #dedão
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #4 dedos
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)
        msg = detect_sign(fingers)
        fCounter = how_many_fingers(fingers)
        cv2.putText(img, msg, (300,140), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)
        cv2.putText(img, str(fCounter), (200,140), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)

 

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
