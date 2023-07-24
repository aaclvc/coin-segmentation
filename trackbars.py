import cv2
import numpy as np


def nothing (x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Threshold 1", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Threshold 2", "Trackbars", 0, 255, nothing)

while True:
    image = cv2.imread("coins.jpeg")
    original_image = image.copy()

    # trackbar vars
    thresh1 = cv2.getTrackbarPos("Threshold 1", "Trackbars")
    thresh2 = cv2.getTrackbarPos("Threshold 2", "Trackbars")

    # gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur image
    blur = cv2.GaussianBlur(gray, (11,11), 150)

    #canny image
    canny = cv2.Canny(blur, thresh1, thresh2, 3)

    #erode
    # erode = cv2.erode(canny, (1,1), iterations=2)

    #dilate image
    dilate = cv2.dilate(canny, (1,1), iterations=5)

    contours, hierarchy  = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # modify image shape for stacking
    gray = np.stack((gray,) * 3, axis=-1)
    blur = np.stack((blur,) * 3, axis=-1)
    canny = np.stack((canny,) * 3, axis=-1)
    # erode = np.stack((erode,) * 3, axis=-1)
    dilate = np.stack((dilate,) * 3, axis=-1)

    images = [gray, blur, canny, dilate]

    image_stack = np.hstack(images)
    cv2.imshow("images", image_stack)

    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    cv2.imshow("output", image)

    cv2.waitKey(300)
    # cv2.destroyAllWindows()
