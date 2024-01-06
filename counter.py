import cv2 as cv
import mediapipe as mp

mp_drawing=mp.solutions.drawing_utils
mp_draing_style=mp.solutions.drawing_styles
mp_pose=mp.solutions.pose 

count=0
position=None

capture=cv.VideoCapture(2)
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while capture.isOpened():
        _, frame=capture.read()
        if not _:
            print('Empty video')
            break
        rgb=cv.cvtColor(cv.flip(frame, 1), cv.COLOR_BGR2RGB)
        result=pose.process(rgb)
        imlist=[]
        frame=cv.flip(frame, 1)
        cv.putText(frame, 'Count:',(10,20),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)
        cv.putText(frame, str(count),(10,50),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
            for id, im in enumerate(result.pose_landmarks.landmark):
                h,w=rgb.shape[:2]
                X,Y=int(im.x*w),int(im.y*h)
                imlist.append([id,X,Y])
                
            if len(imlist)!=0:
                if imlist[26][2]>imlist[24][2]:
                    position='sat'
                if  imlist[26][2]<imlist[24][2] and position=='sat':
                    position='up'
                    count+=1
                    cv.putText(frame, str(count),(10,10),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)

        cv.imshow('Bb',frame )
        if cv.waitKey(10) & 0xff==ord('q'):
            break

cv.destroyAllWindows()
capture.release()