import cv2 as cv
import mediapipe as mp

face_mesh=mp.solutions.face_mesh.FaceMesh()

capture=cv.VideoCapture(2)

while True:
    _, frame=capture.read()
    if not _:
        print('empty image')
        break
    result=face_mesh.process(frame)
    try:
        for face_landmark in result.multi_face_landmarks:
            for i in range(0,468):
                landmark=face_landmark.landmarks[i]
                x=int(landmark.x*frame.shape[1])
                y=int(landmark.y*frame.shape[0])
                frame=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                cv.circle(frame,(x,y),1,(0,0,255),1)
                cv.imshow('Face detect', frame)        
    except:
         cv.imshow('Face detect', frame)  
    if cv.waitKey(10) & 0xff==ord('q'):
        break
capture.release()
cv.destroyAllWindows()
