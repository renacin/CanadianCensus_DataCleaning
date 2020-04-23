# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import pandas as pd
import numpy as np
import time
# ----------------------------------------------------------------------------------------------------------------------
"""
Notes:
    + Resizing Will Destroy Detail, But Can Help With Processing Speed
        - Be careful when resizing images, 1/2x Smaller, 2x Bigger
"""

def process_video(video_path):
    # Import Video
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    # Loop Through Each Frame
    while True:

        # Initialize Individual Frame
        ret, frame = cap.read()

        # Convert To GrayScale | Grab Subsection
        im_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_subsection = im_gray[1000:1080, 0:1200]

        # Apply Threshold Function | Rescale
        retval, threshold = cv2.threshold(frame_subsection, 155, 255, cv2.THRESH_BINARY)
        scale_factor = 2
        im_small = cv2.resize(threshold, (0,0), fx= 1/scale_factor, fy= 1/scale_factor)

        # Display Frames
        cv2.imshow('Original', frame)
        cv2.imshow('Processed', im_small)

        # time.sleep(1/30)

        if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
            cap.release()
            cv2.destroyAllWindows()
            break

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Import The Dashcam Video Into OpenCV
    in_path = r"C:\Users\renac\Desktop\Dashcam\Video_1.mp4"

    # Process Video
    process_video(in_path)
