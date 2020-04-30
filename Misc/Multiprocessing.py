# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
from multiprocessing import Process
import os
import math
# ----------------------------------------------------------------------------------------------------------------------


# Def Function To Be Tested
def calc():
    for i in range(0, 1000):
        math.sqrt(i)


def main():

    # Define The Processes For multiprocessing Attempt
    processes = []

    # Number Of Cores On Computer
    print("CPU Cores: {}".format(os.cpu_count()))

    # Register Processes | Match Number Of CPU Cores
    for i in range(os.cpu_count()):
        print("Registering Process ID: {}".format(i + 1))
        processes.append(Process(target=calc))

    for process in processes:
        process.start()

    for process in processes:
        process.join()


# ----------------------------------------------------------------------------------------------------------------------


# Entry Point For Main Program
if __name__ == "__main__":

    # Run Main Program
    main()
