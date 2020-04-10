# Name:                                            Renacin Matadeen
# Date:                                               04/07/2020
# Title                                       Random Rounding Research
#
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import random
import math
import time
# ----------------------------------------------------------------------------------------------------------------------
"""
Notes:
    + The larger the roiunding base the larger the effect on the mean, and standard deviation
    + From this experiment we can surmise that randon rounding (with cosideration to rounding bases of 5, or 10) has a
        large influence on smaller census observations
    +

"""
# ----------------------------------------------------------------------------------------------------------------------

"""
Create Data For Random Rounding Research
    + Create a dataset, introduce an acceptable amount of noise into both variables
"""
def create_data(num_points):
    # [1.] Create X & Y Variables
    x = [random.uniform(50, 1000) for x in range(num_points)]
    y_1 = [((6.5 * x) + random.uniform(0, 1000)) for x in x]

    # [2.] Randomly Round Y Variables
    rounding_var = random.uniform(0, 1)
    rounding_base = 500

    # Process Of Random Rounding
    y_2 = []
    for y_var in y_1:
        if (y_var % rounding_base != 0):
            if rounding_var >= 0.50:
                y_new = math.ceil((y_var / rounding_base)) * rounding_base
            else:
                y_new = math.floor((y_var / rounding_base)) * rounding_base

        y_2.append(y_new)

    return x, y_1, y_2


"""
Basic Analysis Of Different Datasets
    + Create a dataset, introduce an acceptable amount of noise into both variables
"""
def calc_stats(y_1, y_2):

    # Calc Difference Between Points
    sum_diff = 0
    for y1, y2 in zip(y_1, y_2):

        diff = abs(y1 - y2)
        sum_diff += diff


    # Print General Statistics

    print("---ORIGINAL DATA---")
    print("Average: {}".format(np.average(y_1)))
    print("Standard Deviation: {}".format(np.std(y_1)))

    print("---ROUNDED DATA---")
    print("Average: {}".format(np.average(y_2)))
    print("Standard Deviation: {}".format(np.std(y_1)))
    print("Difference B/W Org & RR:{}".format(sum_diff))


"""
Plot Data
"""
def plot_data(x1, y1, y2):

    plt.subplot(1, 2, 1)
    plt.scatter(x1, y1)
    plt.title('Original & Random Rounded Data', loc='center')
    plt.ylabel('Original')


    plt.subplot(1, 2, 2)
    plt.scatter(x1, y2)
    plt.xlabel('X Values')
    plt.ylabel('Random Rounded')

    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    x_1, y_1, y_2 = create_data(100)
    calc_stats(y_1, y_2)
    plot_data(x_1, y_1, y_2)
