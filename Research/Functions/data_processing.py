# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import pandas as pd
import os
import shutil
import pytesseract
# ----------------------------------------------------------------------------------------------------------------------


# Secondary Function, Clean Text Object Orientation
def clean_text(in_text):

    try:
        raw_text = in_text.split(" ")

        # Pull & Clean Inputs
        date_ = raw_text[0]
        time_ = raw_text[1]
        longitude_ = float(raw_text[5].replace("W", ""))
        latitude_ = float(raw_text[6].replace("N", ""))
        longitude_ = longitude_ * -1
        speed_ = float(raw_text[7])

        # Final Error Check
        if (speed_ > 200):
            raise ValueError

    except:
        date_ = "Nan"
        time_ = "Nan"
        latitude_ = "Nan"
        longitude_ = "Nan"
        speed_ = "Nan"

    return date_, time_, latitude_, longitude_, speed_


# Main Function, Process Each Frame And Gather Data
def process_video(in_path):

    # Use Dictionary As Storage Methodology For Data | Convert To Pandas Df & CSV After
    data_dictionary = {'Frame_Num': [], 'Date': [], 'Time': [],
                       'Latitude': [], 'Longitude': [], 'Speed': []}

    # Loop Through Each Frame
    for filename in os.listdir(in_path):

        # Import Image
        im = cv2.imread(in_path + "/" + filename)

        # Frame Number
        image_frame_num = int(filename[6:-5])

        # Gather Data From Frames
        try:
            # Convert Image To Text
            raw_text = pytesseract.image_to_string(im)

            # Pull Information
            date_v, time_v, latitude_v, longitude_v, speed_v = clean_text(raw_text)

            # Append Information To Data_Dictionary
            data_dictionary['Frame_Num'].append(image_frame_num)
            data_dictionary['Date'].append(date_v)
            data_dictionary['Time'].append(time_v)
            data_dictionary['Latitude'].append(latitude_v)
            data_dictionary['Longitude'].append(longitude_v)
            data_dictionary['Speed'].append(speed_v)

            print("Frame Num: {}, Date: {}, Time: {}, Latitude: {}, Longitude: {}, Speed: {}".format(
                image_frame_num, date_v, time_v, latitude_v, longitude_v, speed_v))

        # Raise KeyboardInterrupt Exit Program
        except(KeyboardInterrupt, SystemExit):
            break

    # Write Data To CSV
    df = pd.DataFrame.from_dict(data_dictionary)
    df.to_csv("/Users/renacinmatadeen/Desktop/DashcamDataParse.csv", index=False)
    print("Progress: Data Parsed & Written")


# CREATE A FUNCTION THAT IMPLEMENTS MULTIPROCESSING,
