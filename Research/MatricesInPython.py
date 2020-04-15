# Name:                                            Renacin Matadeen
# Date:                                               04/07/2020
# Title                                       Random Rounding Research
#
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import numpy as np
import math
# ----------------------------------------------------------------------------------------------------------------------
"""
Notes:
    Revisiting Matrices In Python
        + How Can We Manipulate A Matrix?
            - Addition, Subtraction, Division, and Multiplication
            - What is the inverse, determinant of a matrix?
            - What are EigenValues, and EigenVectors? How can we use them?
"""
# ----------------------------------------------------------------------------------------------------------------------

def image_processing():
    # Open Image As Numpy Array | OpenCV Does This Natively
    im = cv2.imread(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Image.jpg")
    print(im.shape)

    # Grab Only Red Channel Values
    red_matrix = im[:, :, 1]
    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Red_Channel_Image.jpg",
                red_matrix)

    print(red_matrix)

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # matrix_math()
    image_processing()
