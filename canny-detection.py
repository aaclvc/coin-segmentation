'''
-------------------------------
Aida Čolović & Amina Čolović
Allgemeine Informatik M.Sc.
SoSe 2023
Bildverarbeitung
-------------------------------

Detecting coins with canny algortihm and caclulating total amount in EUR

Usage:
-----
python3 canny-detection.py
'''

import cv2
import cvzone
import numpy as np

from cvzone.ColorModule import ColorFinder

def preprocessing(image):
    preprocessed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                  #gray
    preprocessed = cv2.medianBlur(preprocessed, 7)                          #blur

    thresh1 = cv2.getTrackbarPos("Threshold 1", "Trackbars")
    thresh2 = cv2.getTrackbarPos("Threshold 2", "Trackbars")
    preprocessed = cv2.Canny(preprocessed, thresh1, thresh2)                #canny

    kernel = np.ones((3,3), np.uint8)
    preprocessed = cv2.dilate(preprocessed, kernel, iterations=1)           #dilate
    preprocessed = cv2.morphologyEx(preprocessed, cv2.MORPH_CLOSE, kernel)  # morph (schließung kleiner Löcher)

    return preprocessed

def empty (x):
    pass

vid = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Threshold 1", "Trackbars", 100, 255, empty)
cv2.createTrackbar("Threshold 2", "Trackbars", 200, 255, empty)

# Custom Colors
cCopper = {'hmin': 0, 'smin': 0, 'vmin': 33, 'hmax': 14, 'smax': 255, 'vmax': 255}
# cSilver = {'hmin': 17, 'smin': 0, 'vmin': 0, 'hmax': 14, 'smax': 64, 'vmax': 255}
colorFrame = np.zeros((480, 640, 3), dtype=np.uint8)


while(True):
    cFinder = ColorFinder(False)

    ret, frame = vid.read()
    preFrame = preprocessing(frame)

    totalAmount = 0
    imgContours, foundContours = cvzone.findContours(frame, preFrame, minArea=20)

    if foundContours:
        for contour in foundContours:
            peri = cv2.arcLength(contour["cnt"], True)                      # berechnet die Länge der Kontur (true => geschlossene Kontur)
            approx = cv2.approxPolyDP(contour["cnt"], 0.02 * peri, True)    # Approximation auf der Kontur;vereinfachung der Kontur; approx-> anzahl ecken -> Filterung
            if len(approx) > 5:
                area = contour["area"]

                x, y, w, h = contour["bbox"]
                cropedFrame = frame[y:y+h, x:x+w]

                colorFrame, copperMask = cFinder.update(cropedFrame, cCopper)  # maske: weiß -> gefundene farbe; schwarz: -> rest
                whitePixels = cv2.countNonZero(copperMask)                     # anzahl weißer pixel

                # print(area)
                # print(whitePixels)

                # hard coded values with camera (iPhone 13 Pro) distance of 19.5cm

                if whitePixels > 13000:      # copper coins -> 1ct, 2ct, 3ct
                    if area < 14000:
                        totalAmount += 1
                    elif 14000 < area < 19000:
                        totalAmount += 2
                    elif 20000 < area < 23500:
                        totalAmount += 5
                else:
                    if 18000 < area < 20500:
                        totalAmount += 10
                    elif 23000 < area < 25100:
                        totalAmount += 20
                    elif 25500 < area < 27800:
                        totalAmount += 100
                    elif 28000 < area < 30000:
                        totalAmount += 50
                    elif 31500 < area:
                        totalAmount += 200

    imageStack = cvzone.stackImages([frame, preFrame, imgContours], 2, 0.5)
    cvzone.putTextRect(imageStack, f"Total: {totalAmount/100} EUR", (1500,1050), colorR=(255, 0, 0))
    cv2.imshow("video feed", imageStack)

    # cv2.imshow("color image finder", colorFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
