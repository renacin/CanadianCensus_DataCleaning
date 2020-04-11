# Name:                                            Renacin Matadeen
# Date:                                               04/07/2020
# Title                                       Random Rounding Research
#
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import random
import math
# ----------------------------------------------------------------------------------------------------------------------
"""
Notes:
    + The larger the roiunding base the larger the effect on the mean, and standard deviation
    + From this experiment we can surmise that randon rounding (with cosideration to rounding bases of 5, or 10) has a
        large influence on smaller census observations
    + Use Numpy Arrays. Much Faster And Designed For This Kind Of Work

"""
# ----------------------------------------------------------------------------------------------------------------------

"""
Create Data For Random Rounding Research
    + Create a dataset, introduce an acceptable amount of noise into both variables
"""
def create_data(num_points):

    # [1.] Create X & Y Variables
    x = np.random.uniform(low=50, high=1000, size=(num_points,))
    y_1 = (6.5 * x) + np.random.uniform(low=0, high=100, size=(1,))

    # [2.] Randomly Round Y Variables
    rounding_var = random.uniform(0, 1)
    rounding_base = 5

    # Process Of Random Rounding
    y_2 = []
    for y_var in y_1:
        if (y_var % rounding_base != 0):
            if rounding_var >= 0.50:
                y_new = math.ceil((y_var / rounding_base)) * rounding_base
            else:
                y_new = math.floor((y_var / rounding_base)) * rounding_base

        y_2.append(y_new)

    y_2 = np.array(y_2)

    y_1 = y_1.reshape(-1, 1)
    y_2 = y_2.reshape(-1, 1)

    return x, y_1, y_2


"""
Predict Original Values Based On Randomly Rounded Data
    + Are Accurate Results Possible?
"""
def predict(x_1, y_2):

    # [1.] Reshape Array
    x_1 = x_1.reshape(-1, 1)

    # [2.] Split Data Into Training And Testing Sets
    X_train, X_test, y_train, y_test = train_test_split(x_1, y_2, test_size = 0.25)

    # [3.] Feed Data Into Linear Regression Model
    regr = LinearRegression()
    regr.fit(X_train, y_train)

    # [4.] Return List Of Predicted Values Based On Coefficients
    m = regr.coef_[0]
    b = regr.intercept_

    y_3 = (x_1 * m) + b

    return y_3


"""
Basic Analysis Of Different Datasets
    + How Do Each Datasets Differ?
    + What Are Appropriate Methodologies To Fix Randomly Rounded Data?
"""
def calc_stats(y_1, y_2, y_3):

    # Calc Difference Between Y_1 & Y_2
    sum_diff_1_2 = sum(abs(y_1 - y_2))
    sum_diff_1_3 = sum(abs(y_1 - y_3))

    # Print General Statistics

    print("---ORIGINAL DATA---")
    print("Average: {}".format(np.average(y_1)))
    print("Standard Deviation: {} \n".format(np.std(y_1)))

    print("---ROUNDED DATA---")
    print("Average: {}".format(np.average(y_2)))
    print("Standard Deviation: {}".format(np.std(y_2)))
    print("Difference B/W Org & RR:{} \n".format(sum_diff_1_2))

    print("---PREDICTED DATA---")
    print("Average: {}".format(np.average(y_3)))
    print("Standard Deviation: {}".format(np.std(y_3)))
    print("Difference B/W Org & Pred:{} \n".format(sum_diff_1_3))


"""
Plot Data
"""
def plot_data(x1, y1, y2, y3):

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


"""
Export Data
"""
def export_data(x1, y1, y2, y3):
    df = pd.DataFrame({'X': x1.tolist(), 'Y_1': y1.tolist(), 'Y_2': y2.tolist(), 'Y_3': y3.tolist()})
    df.to_csv(r"C:\Users\renac\Desktop\RandomRoundingDefeat.csv", index=False)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    x_1, y_1, y_2 = create_data(1000)
    y_3 = predict(x_1, y_2)
    calc_stats(y_1, y_2, y_3)
    plot_data(x_1, y_1, y_2, y_3)
    export_data(x_1, y_1, y_2, y_3)
