import cv2
import os
import json
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Variables
width, height = 1080, 520  # Original dimensions of the presentation images
folderPath = "Presentation"
annotationsFile = "annotations.json"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Get the list of presentation images
pathImages = os.listdir(folderPath)

# Variables
imgNumber = 0
gestureThreshold = 100  # Reduced the threshold to allow drawing in the upper part
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = 0
annotationStart = False
laserPointerVisible = False  # Flag to show/hide the laser pointer

# Load annotations if available
if os.path.exists(annotationsFile):
    with open(annotationsFile, 'r') as file:
        annotations = json.load(file)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Get screen resolution
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define webcam circle dimensions
circle_radius = int(min(screen_width, screen_height) * 0.2)
circle_center = (screen_width - circle_radius - 10, screen_height - circle_radius - 10)  # Bottom right corner

while True:
    # Import images
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Determine which image to display
    if imgNumber < len(pathImages):
        pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
        imgCurrent = cv2.imread(pathFullImage)
    else:
        imgCurrent = np.zeros((height, width, 3), dtype=np.uint8)  # Blank image

    # Create a copy of the image for hand detection
    imgForDetection = img.copy()
    hands, imgForDetection = detector.findHands(imgForDetection, draw=False)  # Detect hands without drawing

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [50, height - 50], [0, height]))  # Adjusted range for y values
        indexFinger = xVal, yVal

        # Check if thumb is extended (move to previous slide)
        if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
            print("Thumb extended")

            if imgNumber > 0:
                buttonPressed = True
                annotations = [[]]
                annotationNumber = 0
                imgNumber -= 1

        # Check if all fingers are open (move to next slide)
        elif all(f == 1 for f in fingers):
            print("All fingers open")

            if imgNumber < len(pathImages) - 1:
                buttonPressed = True
                annotations = [[]]
                annotationNumber = 0
                imgNumber += 1

        # Gesture 3-Show Pointer (Laser Pointer)
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            laserPointerVisible = True
            annotationStart = False

        # Gesture 4-Draw Pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
            laserPointerVisible = False

        else:
            annotationStart = False

        # Gesture 5- Erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

    else:
        annotationStart = False
        laserPointerVisible = False

    # Button Pressed iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 12)

    # Resize presentation slide to fit the screen
    imgCurrent = cv2.resize(imgCurrent, (screen_width, screen_height))

    # Create a blank image for the combined view
    combined_img = np.zeros((screen_height, screen_width + circle_radius * 2, 3), dtype=np.uint8)

    # Place the presentation slide in the combined image
    combined_img[:screen_height, :screen_width] = imgCurrent

    # Overlay webcam feed in a circle at the bottom right corner
    img_resized = cv2.resize(img, (circle_radius * 2, circle_radius * 2))
    mask = np.zeros((circle_radius * 2, circle_radius * 2, 3), dtype=np.uint8)
    cv2.circle(mask, (circle_radius, circle_radius), circle_radius, (255, 255, 255), -1)
    img_resized = cv2.bitwise_and(img_resized, mask)

    # Calculate the position for webcam overlay
    webcam_x = screen_width - circle_radius * 2
    webcam_y = screen_height - circle_radius * 2

    # Place the webcam feed in the combined image
    combined_img[webcam_y:webcam_y + circle_radius * 2, webcam_x:webcam_x + circle_radius * 2] = img_resized

    # Display the combined image fullscreen
    cv2.imshow("Presentation", combined_img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Save annotations to a file
        with open(annotationsFile, 'w') as file:
            json.dump(annotations, file)
        print("Annotations saved!")

cap.release()
cv2.destroyAllWindows()
