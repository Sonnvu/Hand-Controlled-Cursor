import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

################################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 5
################################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# wScr = 2560
# hScr = 1600
# print(wScr, hScr)


# DEFAULT IMPLEMENTATION WITH INDEX FINGER AND MIDDLE FINGER
# while True:
#     # 1. Find hand Landmarks
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img)
#     # 2. Find the tip of the index and thumb fingers
#     if len(lmList)!=0:
#         x1, y1 = lmList[8][1:]
#         x2, y2 = lmList[4][1:]
#         # print(x1, y1, x2, y2)
#
#         # 3. Check which finger are up
#         fingers = detector.fingersUp()
#         # print(fingers)
#         cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
#                       (255, 0, 255), 2)
#         # 4. Only Index Finger: Moving Mode
#         if fingers[1] == 1 and fingers[0] == 0:
#
#             # 5. Convert Coordinates
#             x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
#             y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
#
#             # 6. Smoothing Values
#             clocX = plocX + (x3 - plocX) / smoothening
#             clocY = plocY + (y3 - plocY) / smoothening
#
#             # 7. Move Mouse
#             autopy.mouse.move(wScr - clocX, clocY)
#             cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#             plocX, plocY = clocX, clocY
#
#         # 8. Both Index and thumb fingers are up: Clicking Mode
#         if fingers[1] == 1 and fingers[0] == 1:
#             # 9. Find distance between two fingers
#             length, img, lineInfo = detector.findDistance(8, 4, img)
#             print(length)
#             # 10. Click mouse if distance short
#             if length < 17:
#                 cv2.circle(img, (lineInfo[4], lineInfo[5]),
#                            15, (0, 255, 0), cv2.FILLED)
#                 autopy.mouse.click()

# ALTERNATE IMPLEMENTATION WITH POINT BETWEEN INDEX FINGER AND THUMB
while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Find the tip of the index and thumb fingers
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[4][1:]
        # print(x1, y1, x2, y2)
        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # 6. Find Point between two finger

        # 3. Check which finger are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. Only Index Finger: Moving Mode
        if fingers[1] == 1 and fingers[0] == 1:

            # 5. Convert Coordinates
            length, img, lineInfo = detector.findDistance(8, 4, img)
            print(length)
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (255, 0, 255), cv2.FILLED)

            # 6. Smoothing Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            fingers = detector.fingersUp()
            # print(fingers)
            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

            if length < 25:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

        # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 255, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)