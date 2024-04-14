import cv2
import os
from HandTracker import HandDetector
import numpy as np
import keyboard

'''
# This app will use your built-in webcam to control your slides presentation.
# For a one-handed presentation, use Gesture 1 (thumbs up) to go to the previous slide 
# and Gesture 2 (whole hand pointing up) to go to the next slide.

'''

# variables
width, height = 350, 250
# gesture Threshold 
ge_thresh_y = 150
ge_thresh_x = 200
# button Pressed
gest_done = False 
gest_counter = 0
delay = 30*1

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# HandDetector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# setup font opencv
font = cv2.FONT_HERSHEY_SIMPLEX   
# position 
org = (20, 30)   
# fontScale 
fontScale = 1   
# Blue color in BGR 
color = (255, 0, 0)   
# Line thickness of 2 px 
thickness = 2

# action name
action_name = ""

while True:
    # Get image frame
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  

    # Find the hand and its landmarks
    hands, frame =  detector.findHands(frame)  

    if hands and gest_done is False:  # If hand is detected

        hand = hands[0]
        cx, cy = hand["center"]
        lm_list = hand["lmList"]  # List of 21 Landmark points
        fingers = detector.fingersUp(hand) # List of which fingers are up  

        if cy < ge_thresh_y and cx > ge_thresh_x :  # If hand is at the height of the face           

            # gest_1 (previous)
            if fingers == [1, 0, 0, 0, 0]:
                # print("Left")
                gest_done = True
                keyboard.press_and_release('left')              
                action_name = "previous"

            # gest_2 (next)
            if fingers == [0, 1, 1, 0, 0]:
                # print("Right") 
                gest_done = True
                keyboard.press_and_release('right')
                action_name = "next"
               

      
    # Gesture Performed Iterations:
    if gest_done:
        gest_counter += 1
        # Using cv2.putText() method 
        frame = cv2.putText(frame, action_name, org, font, fontScale, color, thickness, cv2.LINE_AA)
        if gest_counter > delay:
            gest_counter = 0
            gest_done = False


    cv2.imshow("Slides", frame)
    # cv2.imshow("Image", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break