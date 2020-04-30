# Name:                                            Renacin Matadeen
# Date:                                               04/07/2020
# Title                                       Random Rounding Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import pandas as pd
import numpy as np
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

    # Return Values
    return newArrLRTB, empty_matrix


def calc_value(data_mat, kernel_choice):

    # Basic Blur
    if kernel_choice == 1:
        kern = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]], dtype="int16")

        elem_mul = (data_mat * kern)
        sum_val = (np.sum(elem_mul)) / 9

    # Gaussian Blur
    if kernel_choice == 2:
        kern = np.array([[1, 2, 1],
                        [2, 4, 2],
                        [1, 2, 1]], dtype="int16")

        elem_mul = (data_mat * kern)
        sum_val = (np.sum(elem_mul)) / 16

    # Identity Matrix
    elif kernel_choice == 3:
        kern = np.array([[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]], dtype="int16")

        elem_mul = (data_mat * kern)
        sum_val = np.sum(elem_mul)

    # Laplacian Operator 1
    elif kernel_choice == 4:
        kern = np.array([[-1, -1, -1],
                        [-1, 8, -1],
                        [-1, -1, -1]], dtype="int16")

        elem_mul = (data_mat * kern)
        sum_val = np.sum(elem_mul)

    # Laplacian Operator 2
    elif kernel_choice == 5:
        kern = np.array([[0, -1, 0],
                        [-1, 4, -1],
                        [0, -1, 0]], dtype="int16")

        elem_mul = (data_mat * kern)
        sum_val = np.sum(elem_mul)




    # Sobel X|Y Edge Detection
    elif kernel_choice == 6:
        kern_1 = np.array([[-1, -1, -1],
                           [0, 0, 0],
                           [1, 1, 1]])

        kern_2 = np.array([[-1, 0, 1],
                           [-1, 0, 1],
                           [-1, 0, 1]])

        # Calculate Seperatly, Then Square Add, Then Root Value
        elem_mul_1 = (data_mat * kern_1)
        # elem_mul_2 = (data_mat * kern_2)
        #
        # # Square Values In Array
        # squared_array = np.square(elem_mul_1) + np.square(elem_mul_2)
        # final_array = np.sqrt(squared_array)
        sum_val = np.sum(elem_mul_1)


    return sum_val


def conv_matrix(empty_matrix, matx, kernel_choice):

    # Dimensions Of Original Image
    org_dim_l = empty_matrix.shape[0]
    org_dim_w = empty_matrix.shape[1]

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
            append_val = calc_value(data_mat, kernel_choice)
            # Append To New Matrix
            empty_matrix[y, x] = append_val

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
    return empty_matrix


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Open Image As Numpy Array | OpenCV Does This Natively
    im = cv2.imread(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Image.jpg")

    # Grab Only Blue Channel Values | Setup Matrix & Convolve With Kernel
    image_ = im[:, :, 2]

    # Setup Matrix
    setup_matrix, empty_matrix = add_pixel_border(image_)

    # Blur Image | Reduce Noise
    for x in range(8):
        if x == 0:
            blurred_image = conv_matrix(empty_matrix, setup_matrix, 2)
        else:
            setup_matrix, empty_matrix = add_pixel_border(blurred_image)
            blurred_image = conv_matrix(empty_matrix, setup_matrix, 2)

    # Edge Detection Image
    processed_image = conv_matrix(empty_matrix, setup_matrix, 4)
    cv2.imwrite(r"C:\Users\renac\Documents\Programming\Python\CanadianCensus_DataCleaning\Research\Images\Processed_Image.jpg", processed_image)
