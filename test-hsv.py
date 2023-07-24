import cv2
import numpy as np

def on_trackbars_change(pos):
    pass

def main():
    cap = cv2.VideoCapture(1)

    cv2.namedWindow('WebCam HSV Extractor')
    cv2.createTrackbar('H Min', 'WebCam HSV Extractor', 0, 179, on_trackbars_change)
    cv2.createTrackbar('H Max', 'WebCam HSV Extractor', 179, 179, on_trackbars_change)
    cv2.createTrackbar('S Min', 'WebCam HSV Extractor', 0, 255, on_trackbars_change)
    cv2.createTrackbar('S Max', 'WebCam HSV Extractor', 255, 255, on_trackbars_change)
    cv2.createTrackbar('V Min', 'WebCam HSV Extractor', 0, 255, on_trackbars_change)
    cv2.createTrackbar('V Max', 'WebCam HSV Extractor', 255, 255, on_trackbars_change)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos('H Min', 'WebCam HSV Extractor')
        h_max = cv2.getTrackbarPos('H Max', 'WebCam HSV Extractor')
        s_min = cv2.getTrackbarPos('S Min', 'WebCam HSV Extractor')
        s_max = cv2.getTrackbarPos('S Max', 'WebCam HSV Extractor')
        v_min = cv2.getTrackbarPos('V Min', 'WebCam HSV Extractor')
        v_max = cv2.getTrackbarPos('V Max', 'WebCam HSV Extractor')

        lower_bound = np.array([h_min, s_min, v_min])
        upper_bound = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('WebCam HSV Extractor', np.hstack((frame, result)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
