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

def process_image(image):
        # Convert To GrayScale | Resize Image, Make 1/32 Version
        scale_factor = 2
        im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_small = cv2.resize(im, (0,0), fx= 1/scale_factor, fy= 1/scale_factor)

        # Remove Noise From Image | Must Be Bigger Than 3, & Support A Middle Origin Point | Uneven Numbers Only?
        blur_kern_size = 3
        img_blurred = cv2.GaussianBlur(im_small,(blur_kern_size, blur_kern_size), 0)

        # Calculate Edge Detection
        img_edge = cv2.Laplacian(img_blurred, cv2.CV_64F)

        # Resize Image To Original Dimensions
        processed_image = cv2.resize(img_edge, (0,0), fx= scale_factor, fy= scale_factor)

        # Return Image
        return processed_image

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Choose Image To Work On
    in_path = r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Image.jpg"
    im = cv2.imread(in_path)

    # Process Image
    proc_img = process_image(im)

    # Write Image
    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Processed_Image.jpg", proc_img)
