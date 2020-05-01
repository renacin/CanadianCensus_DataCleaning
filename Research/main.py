# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
from Functions_.image_processing import *
from Functions_.data_processing import *
# ----------------------------------------------------------------------------------------------------------------------


# This Is The Main Function
def main_process():

    # Import The Dashcam Video Into OpenCV
    in_video_path = "/Users/renacinmatadeen/Desktop/Dashcam/RawVideo/V1.mp4"
    in_path = "/Users/renacinmatadeen/Desktop/Dashcam/IndividualFrames"

    # # Process Video
    # # write_cleaned_frames(in_video_path, in_path)
    #
    # # Keep Only 1st Frame Of 30 FPS
    # # keep_first_frame(in_video_path, in_path)

    # Process Images And Write Data To CSV
    process_video(in_path)

    # ----------------------------------------------------------------------------------------------------------------------

    # Entry Point For Main Program
if __name__ == "__main__":

    # Run Main Program
    main_process()
