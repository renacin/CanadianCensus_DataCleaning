# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import os
import cv2
import math
import pytesseract
import pandas as pd
import multiprocessing
# ----------------------------------------------------------------------------------------------------------------------


# Secondary Function, Split Index Of Frames By Number Of Cores
def chunks(list_of_frames, list_size):
    for i in range(0, len(list_of_frames), list_size):
        yield list_of_frames[i:i + list_size]


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


# Secondary Function, Create List Of Indices For Each Core/Process
def calc_indices_per_core(new_temp_folder):

    # Get The Frame Numbers In The Folder | Number Of Frames | Equal Size Of Chunk
    list_of_frames_num = [int(filename[6:-5]) for filename in os.listdir(new_temp_folder)]
    list_of_frames_num_sorted = sorted(list_of_frames_num)
    num_images = len(list_of_frames_num_sorted)
    chunk_size = math.ceil(num_images/os.cpu_count())

    # Seperate List By Number Of CPU Cores
    lists_of_indices = chunks(list_of_frames_num_sorted, chunk_size)

    # Return List Of Indices
    return lists_of_indices


# Process Each Frame Per Indices List
def process_frames(new_temp_folder, focus_frames, processor_id):

    # Use Dictionary As Storage Methodology For Data | Convert To Pandas Df & CSV After
    data_dictionary = {'Frame_Num': [], 'Date': [], 'Time': [],
                       'Latitude': [], 'Longitude': [], 'Speed': []}

    processed_images_path = new_temp_folder + "/Image_"

    # Loop Through Each Frame In Focus_Frames List
    for frame_number in focus_frames:
        image_path = processed_images_path + str(frame_number) + ".jpeg"

        # Import Image
        im = cv2.imread(image_path)

        # Frame Number
        image_frame_num = int(frame_number)

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

    # # Write Data To CSV
    # df = pd.DataFrame.from_dict(data_dictionary)
    # df.to_csv("/Users/renacinmatadeen/Desktop/DashcamDataParse.csv", index=False)
    # print("Progress: Data Parsed & Written")

    # Main Function, Process Each Frame And Gather Data | Per Core


def process_frames_multiprocessing(new_temp_folder):

    # List Of Dif Indices
    multiple_chunks_list = calc_indices_per_core(new_temp_folder)

    # Store The Processes In A List | Easier To Iterate
    processes = []

    # Register Processes | Match Number Of CPU Cores
    for i, chunk_index in enumerate(multiple_chunks_list):

        # Utilize Multiprocessing To Process Frames To Data
        processes.append(multiprocessing.Process(target=process_frames,
                                                 args=(new_temp_folder, chunk_index, i + 1,)))

    # Start Processes
    for process in processes:
        process.start()

    # Make Sure Processes Completes Before Moving On
    for process in processes:
        process.join()
