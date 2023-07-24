'''
-------------------------------
Aida Čolović & Amina Čolović
Allgemeine Informatik M.Sc.
SoSe 2023
Bildverarbeitung
-------------------------------

Takes picutures with webcam and saves them in a folder

Usage:
-----
python3 take-pic.py
'''

import os
import cv2

def take_picture():
    # Create the "pictures" folder if it doesn't exist
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    image_count = 1
    print("Press SPACE to take a picture. Press 'q' or 'esc' to exit.")
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Show the frame in a window
        cv2.imshow("Webcam", frame)

        # Wait for key press
        key = cv2.waitKey(1)

        # Take a picture when the space bar is pressed (ASCII code for space is 32)
        if key == 32:
            # Save the image as a .jpg file in the "dataset" folder
            image_path = os.path.join("dataset", f"{image_count}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image {image_count}.jpg saved successfully.")
            image_count += 1

        # End the program when 'q' or 'esc' is pressed
        if key in [ord('q'), 27]:  # 'q' key or 'esc' key
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    take_picture()
