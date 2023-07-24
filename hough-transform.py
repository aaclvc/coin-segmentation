'''
-------------------------------
Aida Čolović & Amina Čolović
Allgemeine Informatik M.Sc.
SoSe 2023
Bildverarbeitung
-------------------------------
Detecting circles with hough transfrom

Usage:
-----
python3 hough-transform.py
'''

import cv2
import numpy as np

def nothing (x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Param 1", "Trackbars", 20, 255, nothing)
cv2.createTrackbar("Param 2", "Trackbars", 20, 255, nothing)
cv2.createTrackbar("Min Radius", "Trackbars", 0, 100, nothing)
cv2.createTrackbar("Max Radius", "Trackbars", 0, 200, nothing)

while True:
    # load image
    image = cv2.imread('img-2.jpeg')
    # rescale
    height = image.shape[0]
    width = image.shape[1]

    #resize image
    new_width = 720
    ratio = new_width / width # (or new_height / height)
    new_height = int(height * ratio)

    dimensions = (new_width, new_height)
    image = cv2.resize(image, dimensions, interpolation=cv2.INTER_LINEAR)

    original_image = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #gray
    gray = cv2.medianBlur(gray, 7)                  #blur

    # trackbar vars
    param1 = cv2.getTrackbarPos("Param 1", "Trackbars")
    param2 = cv2.getTrackbarPos("Param 2", "Trackbars")
    minRadius = cv2.getTrackbarPos("Min Radius", "Trackbars")
    maxRadius = cv2.getTrackbarPos("Max Radius", "Trackbars")

    # hough-transform (more info -> https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 16, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    # draw circles
    if circles is not None:
        circles = np.uint16(np.around(circles))  # convert numbers

    for i in circles[0, :]:
        center = (i[0], i[1])
        # circle center
        cv2.circle(image, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = i[2]
        cv2.circle(image, center, radius, (255, 0, 255), 3)

    # modify image shape for stacking
    gray = np.stack((gray,) * 3, axis=-1)

    images = [original_image, gray, image]

    image_stack = np.hstack(images)
    cv2.imshow("images", image_stack)

    cv2.waitKey(300)

#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("q"):
#         break

# cv2.destroyAllWindows()
