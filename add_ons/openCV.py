import numpy as np
from cv2 import cv2

# function to open the webcam en get a live feed
def open_webcam():

    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        copyframe = frame.copy()
        result = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([155,25,0])
        upper = np.array([179,255,255])
        mask = cv2.inRange(frame, lower, upper)
        result = cv2.bitwise_and(result, result, mask=mask)
        
        # red color boundaries [B, G, R]
        lower = [86, 31, 4]
        upper = [220, 88, 50]

        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask=mask)

        ret,thresh = cv2.threshold(mask, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(output, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

        # show the images
        cv2.imshow("Result", np.hstack([frame, output]))

        cv2.imshow('Input', frame)
        cv2.imshow('result', result)
        cv2.imshow('default', copyframe)

        c = cv2.waitKey(1)
        if c == 27:
            break


    cap.release()
    cv2.destroyAllWindows()

open_webcam()