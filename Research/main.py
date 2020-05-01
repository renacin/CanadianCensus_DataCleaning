# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
from Functions_.image_processing import *
from Functions_.data_processing import *
from Functions_.folder_manipulation import *
# ----------------------------------------------------------------------------------------------------------------------


# This Is The Main Function
def main_process():

    # Import The Dashcam Video Into OpenCV
    in_video_path = "/Users/renacinmatadeen/Desktop/Dashcam/RawVideo/V1.mp4"

    # Find Folder Where Dashcam Video Is Stored | Create A Temporary Folder For Individual Frames
    new_temp_folder = create_folder(in_video_path)

    # Process Video
    write_cleaned_frames(in_video_path, new_temp_folder)

    # Keep Only 1st Frame Of 30 FPS
    keep_first_frame(in_video_path, new_temp_folder)

    # Process Images And Write Data To CSV
    process_video(new_temp_folder)

    # Delete Folder With Temp Images
    delete_folder(new_temp_folder)


# ----------------------------------------------------------------------------------------------------------------------
# Entry Point For Main Program
if __name__ == "__main__":

    # Run Main Program
    main_process()