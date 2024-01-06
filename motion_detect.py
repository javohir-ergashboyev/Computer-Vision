import cv2 as cv
video=cv.VideoCapture(2)
first_frame=None
while True:
    _,frame=video.read()
    gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray=cv.GaussianBlur(gray, (11,11),0)

    if first_frame is None:
        first_frame=gray
        continue
    delta_frame=cv.absdiff(first_frame,gray)
    threshold_frame=cv.threshold(delta_frame, 50,255,cv.THRESH_BINARY)[1]
    threshold_frame=cv.dilate(threshold_frame,None, iterations=1)
    cntr, fr=cv.findContours(threshold_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    for contour in cntr:
        if cv.contourArea(contour)<1000:
            continue
        (x,y,w,h)=cv.boundingRect(contour)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


    cv.imshow('Motion Detect', frame)
    if cv.waitKey(10) & 0xFF==ord('d'):
        break
video.release()
cv.destroyAllWindows()