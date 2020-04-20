# Name:                                            Renacin Matadeen
# Date:                                               04/20/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import pandas as pd
import numpy as np
# ----------------------------------------------------------------------------------------------------------------------
"""
Notes:
    + Resizing Will Destroy Detail, But Can Help With Processing Speed
        - Be careful when resizing images, 1/2x Smaller, 2x Bigger
"""






# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Open Image As Numpy Array | OpenCV Does This Natively
    im = cv2.imread(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Image.jpg")

    # Resize Image, Make 1/32 Version
    im_small = cv2.resize(im, (0,0), fx=0.03125, fy=0.03125)

    # Resize Image, Make 32x Bigger
    im_big = cv2.resize(im_small, (0,0), fx=32, fy=32)

    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Big_Image.jpg", im_big)


    # image_ = im[:, :, 0]
