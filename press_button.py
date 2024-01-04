import cv2 as cv
import time
import random
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp

mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands
x_enemy=random.randint(50,600)
y_enemy=random.randint(50,400)
score=0

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return int(seconds)
video=cv.VideoCapture(0)
fps = video.get(cv.CAP_PROP_FPS)
start_time=time.time()


def enemy():
    global score, x_enemy,y_enemy
    cv.circle(image, (x_enemy,y_enemy),25,(0,0,255),5)


with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame=video.read()
        image=cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image=cv.flip(image,1)
         # Calculate elapsed time
        elapsed_time = time.time() - start_time
        cv.putText(image, "{}".format(format_time(elapsed_time)), (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv.LINE_AA)
        imageHeight,imageWeight,_=image.shape
        result=hands.process(image)
        image=cv.cvtColor(image, cv.COLOR_BGR2RGB)
        font=cv.FONT_HERSHEY_COMPLEX
        color=(0,255,0)
        cv.putText(image, 'Score',(480,30),font,1,color,4,cv.LINE_AA)
        cv.putText(image, str(score),(590,30),font,1,color,4,cv.LINE_AA)
        enemy()

        if result.multi_hand_landmarks:
            for num,hand in enumerate(result.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(255,44,255), thickness=2, circle_radius=2))

        if result.multi_hand_landmarks!=None:
            for handLandMarks in result.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalizedLandMark=handLandMarks.landmark[point]
                    pixelCoordinatesLandMark=mp_drawing._normalized_to_pixel_coordinates(normalizedLandMark.x, normalizedLandMark.y, imageWeight,imageHeight)
                    
                    if point==8:
                        try:
                            cv.circle(image,(pixelCoordinatesLandMark[0],pixelCoordinatesLandMark[1]),25,(0,255,0),5)
                            if pixelCoordinatesLandMark[0]==x_enemy or pixelCoordinatesLandMark[0]==x_enemy+10 or pixelCoordinatesLandMark[0]==x_enemy-10:
                                print('found')
                                x_enemy=random.randint(50,600)
                                y_enemy=random.randint(50,400)
                                score=score+1
                                font=cv.FONT_HERSHEY_COMPLEX
                                color=(0,255,0)
                                text=cv.putText(image,"score",(100,100),font,1,color,4, cv.LINE_AA)
                                enemy()
                        except:
                            pass
        cv.imshow('Hands Tracking', image)
        if score<10 and format_time(elapsed_time)==20:
            print("You lose")
            print('your score: {}'.format(score))
            break
        elif score>=10 and format_time(elapsed_time)<20:
            print("You win")
            print('your score: {}'.format(score))
            break
        if cv.waitKey(10) & 0xFF==ord('d'):
            break
video.release()
cv.destroyAllWindows()