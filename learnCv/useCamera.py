import numpy as np4
import cv2 as cv

cap = cv.VideoCapture(1)
print(cap.isOpened())
while(True):

    # Capture frame-by-frameq
    ret, frame = cap.read()
    # Our operations on the frame come here
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    #cv.imshow('frame',gray)
    cv.imshow('frame',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
