# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
try:
    import os
    import cv2
    import math
    import pytesseract
    import pandas as pd
    import multiprocessing
except ImportError:
    pass
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

        # Addaptive All Lat/Long Values
        if ("W" in raw_text[5]):
            longitude_ = float(raw_text[5].replace("W", ""))
            longitude_ = longitude_ * -1

        elif ("E" in raw_text[5]):
            longitude_ = float(raw_text[5].replace("E", ""))

        if ("N" in raw_text[6]):
            latitude_ = float(raw_text[6].replace("N", ""))

        elif ("S" in raw_text[6]):
            latitude_ = float(raw_text[6].replace("S", ""))
            latitude_ = latitude_ * -1

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
def process_frames(new_temp_folder, focus_frames, processor_id, return_data):

    # Use Dictionary As Storage Methodology For Data | Convert To Pandas Df & CSV After
    data_dictionary = {'Frame_Num': [], 'Date': [], 'Time': [],
                       'Latitude': [], 'Longitude': [], 'Speed': []}

    processed_images_path = new_temp_folder + "/Image_"

    # Loop Through Each Frame In Focus_Frames List
    for frame_number in focus_frames:

        try:
            image_path = processed_images_path + str(frame_number) + ".jpeg"

            # Import Image
            im = cv2.imread(image_path)

            # Frame Number
            image_frame_num = int(frame_number)

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

            # Raise KeyboardInterrupt Exit Program
        except (KeyboardInterrupt, SystemExit) as e:
            break

    # Write Data To Main Data Storage Unit
    return_data["Processor" + str(processor_id)] = data_dictionary


def process_frames_multiprocessing(new_temp_folder, file_name):

    # Create Main Data Storage Unit
    main_data_container = {'Frame_Num': [], 'Date': [], 'Time': [],
                           'Latitude': [], 'Longitude': [], 'Speed': []}

    # Manager Will Help Store Data Created By Workers
    manager = multiprocessing.Manager()
    return_data = manager.dict()

    # List Of Dif Indices
    multiple_chunks_list = calc_indices_per_core(new_temp_folder)

    # Store The Processes In A List | Easier To Iterate
    processes = []

    # Register Processes | Match Number Of CPU Cores
    for i, chunk_index in enumerate(multiple_chunks_list):

        # Utilize Multiprocessing To Process Frames To Data
        processes.append(multiprocessing.Process(target=process_frames,
                                                 args=(new_temp_folder, chunk_index, i + 1, return_data,)))

    # Start Processes
    for process in processes:
        process.start()

    # Make Sure Processes Completes Before Moving On
    for process in processes:
        process.join()

    print("Step #4: Workers Finished Processing - ⛏️")

    # Print Data Stored By Processors
    for dataset_ in return_data.values():

        # Append Data Parsed By Workers
        main_data_container["Frame_Num"].extend(dataset_["Frame_Num"])
        main_data_container["Date"].extend(dataset_["Date"])
        main_data_container["Time"].extend(dataset_["Time"])
        main_data_container["Latitude"].extend(dataset_["Latitude"])
        main_data_container["Longitude"].extend(dataset_["Longitude"])
        main_data_container["Speed"].extend(dataset_["Speed"])

    # Create A Pandas DF | Write To Folder
    csv_path = new_temp_folder.replace("_TEMP_FLDR_DNT_RMV_", "")
    file_name = file_name.replace(".mp4", "")
    new_path = csv_path + file_name + ".csv"

    df = pd.DataFrame(main_data_container)
    df.to_csv(new_path, index=False)
    print("Step #5: Data Written - 💾")
