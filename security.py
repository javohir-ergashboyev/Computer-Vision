import os
import cv2 as cv
import argparse
from datetime import datetime

video=cv.VideoCapture(0)
face_cascade=cv.CascadeClassifier('haar_cascade.xml')

while True:
    _, frame=video.read()
    if frame is not None:
        gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        face_rect=face_cascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=5)

        for (x, y,w,h) in face_rect:
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),1)
            moment=datetime.now().strftime('"%Y/%m/%d%H:%M:%S"')
            person=frame[x:x+w, y:y+h]
            cv.imwrite(str(moment)+"vv.jpg",person)
            cv.imshow('ss',person)
            print(moment)

        cv.imshow('Safety', frame)
        if cv.waitKey(10) & 0xff==ord('q'):
            break
video.release()
cv.destroyAllWindows()
