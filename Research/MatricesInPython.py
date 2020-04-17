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
import time
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

    # Rename As Matrix | Create A Temp That Will Store Data
    matrix_ = img
    empty_matrix = np.full_like(matrix_, 0)

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

    # Write Image
    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\PlusPixel_Image.jpg", newArrLRTB)

    # Debugging
    return newArrLRTB, empty_matrix

def conv_matrix(empty_matrix, matx):

    # Make A Copy Of The Empty Matrix
    emp_mat = empty_matrix.copy()

    # Define Convolution Kernel
    edge_matrix = np.array([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]])

    # Dimensions Of Original Image
    org_dim_l = empty_matrix.shape[0]
    org_dim_w = empty_matrix.shape[1]

    # Dimensions Of Original Image
    set_dim_l = matx.shape[0]
    set_dim_w = matx.shape[1]

    # Define Upper And Lower For Loop
    x_upper = 3
    x_lower = 0

    y_upper = 3
    y_lower = 0

    # For Loop, Do Matrix Convolution
    for y in range(org_dim_l):

        # Iterate Through Each Column For 3 Rows
        for x in range(org_dim_w):
            # Define Subset Matrix
            data_mat = matx[x_lower:x_upper, y_lower:y_upper]

            # Do Calculation
            elem_mul = (data_mat * edge_matrix)
            sum_val = np.sum(elem_mul)

            # Append To New Matrix
            emp_mat[y, x] = sum_val / 9

            # Delete Data_Matrix, Keep Clean
            del data_mat

            # Move Onto Next Column
            y_upper += 1
            y_lower += 1

        # Move Search One Row Down
        x_upper += 1
        x_lower += 1

        # Reset Column Indices
        y_upper = 3
        y_lower = 0

    # Write Image
    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Processed_Image.jpg", emp_mat)







# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Open Image As Numpy Array | OpenCV Does This Natively
    im = cv2.imread(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Image.jpg")

    # Grab Only Blue Channel Values | Setup Matrix & Convolve With Kernel
    image_ = im[:, :, 2]
    setup_matrix, empty_matrix = add_pixel_border(image_)
    conv_matrix(empty_matrix, setup_matrix)
