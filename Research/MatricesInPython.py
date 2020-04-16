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

        + What Is Matrix Convolution?
            - Mathematical process on two functions that produces a third
"""
# ----------------------------------------------------------------------------------------------------------------------


def add_pixel_border(img):

    matrix_ = img

    # Grab Extra Left Right Values
    leftside_values = (matrix_[:, 0]).reshape(-1, 1)
    rightside_values = (matrix_[:, -1]).reshape(-1, 1)

    # Append Left & Right Side
    newArr_L = np.append(leftside_values, matrix_ , axis=1)
    newArr_LR = np.append(newArr_L, rightside_values , axis=1)

    # Grab Extra Top Bottom Values
    top_values = newArr_LR[0, :]
    bottom_values = newArr_LR[-1, :]

    # Append Top And Bottom
    newArrLRT = np.vstack((top_values, newArr_LR))
    newArrLRTB = np.vstack((newArrLRT, bottom_values))

    # Debugging
    print(newArrLRTB.shape)


def image_processing():
    # Open Image As Numpy Array | OpenCV Does This Natively
    im = cv2.imread(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Image.jpg")

    # Grab Only Red Channel Values
    matrix_ = im[:, :, 1]
    add_pixel_border(matrix_)

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # matrix_math()
    image_processing()
