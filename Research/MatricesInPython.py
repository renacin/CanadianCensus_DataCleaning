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
def matrix_math():
    # Using A Numpy Array, Create A 3x3 Matrix
    mat_a = np.array([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]], dtype='int16')

    mat_b = np.array([[1, 3, 3],
                      [1, 4, 3],
                      [1, 3, 4]], dtype='int16')

    # Get The Dimensions Of Both Matrices
    print("Dimensions Of Matrix A: {}, Matrix B: {}".format(mat_a.shape, mat_b.shape))

    # Matrix Inverse
    inv_b = np.linalg.inv(mat_b)
    print(inv_b)

    # Matrix Multiplication
    print("\n")
    mul_ab = np.matmul(mat_a, mat_b)
    print(mul_ab)

    # Matrix Division
    print("\n")
    inv_b = np.linalg.inv(mat_b)
    mul_ab = np.matmul(mat_a, inv_b)
    print(mul_ab)

def image_processing():
    # Open Image As Numpy Array | OpenCV Does This Natively
    im = cv2.imread(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Image.jpg")
    print(im.shape)

    # Grab Only Red Channel Values
    red_matrix = im[:, :, 1]
    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Red_Image.jpg",
                red_matrix)

    print(red_matrix)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # matrix_math()
    # image_processing()
