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


# Tertiary Function, Used In Secondary Function
def process_image(img):

    # Convert To GrayScale | Grab Subsection
    frame_subsection = img[1025:1075, 15:1150, 1]

    # Apply Threshold Function
    retval, threshold = cv2.threshold(frame_subsection, 180, 255, cv2.THRESH_BINARY)

    # Return Simplified Image
    return threshold


# Secondary Function, Iterate Through Each Frame
def write_cleaned_frames(in_video_path, in_path):

    # Make Sure The Folder Where Data If being Written To Is Empty
    try:
        shutil.rmtree(in_path, ignore_errors=True)
        os.mkdir(in_path)

    except(FileNotFoundError):
        os.mkdir(in_path)

    # Try Main Parse
    try:
        # Instantiate Video File
        cap = cv2.VideoCapture(in_video_path)
        ret, frame = cap.read()

        # Get Number Of Frames In Video | Loop Through Each
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Loop Through Each Frame
        for frame_num in range(num_frames):

            # Process Image
            ret, frame = cap.read()
            image_ = process_image(frame)

            image_write_path = "{}/Image_{}.jpeg".format(in_path, frame_num + 1)
            cv2.imwrite(image_write_path, image_, [int(cv2.IMWRITE_JPEG_QUALITY), 15])

            if (frame_num != 0) and (frame_num % 1000 == 0) or (frame_num / num_frames == 1):
                percent_prog = (frame_num/num_frames) * 100
                progress_ = round(percent_prog, 2)
                print("Progress Writing Frames: {}%, Frames Written: {}/{}".format(progress_,
                                                                                   frame_num, num_frames))

            # Raise KeyboardInterrupt Exit Program
    except(KeyboardInterrupt, SystemExit):
        cap.release()
        cv2.destroyAllWindows()

    # Raise KeyboardInterrupt Exit Program
    except:
        cap.release()
        cv2.destroyAllWindows()


# Secondary Function, Iterate Through Each Frame Keep Only The FPSth Frame
def keep_first_frame(in_video_path, in_path):

    # Instantiate Video From Path
    cap = cv2.VideoCapture(in_video_path)

    # Grab Number Of Frames, and Frame Rate Of Video
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Loop Through Files In Directory Remove Images Redundant Images
    for filename in os.listdir(in_path):

        # Each Image Had A Frame Number Attached, Look At That. Be Careful In The Future Through
        image_frame_num = int(filename[6:-5])

        if (filename.endswith(".jpeg")) and (image_frame_num % num_fps == 0):
            pass
        else:
            try:
                os.remove(in_path + "/" + filename)
            except:
                pass

    print("Images Deleted")


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


# This Is The Main Function
def main():

    # Import The Dashcam Video Into OpenCV
    in_video_path = "/Users/renacinmatadeen/Desktop/Dashcam/RawVideo/V1.mp4"
    in_path = "/Users/renacinmatadeen/Desktop/Dashcam/IndividualFrames"

    # Process Video
    # write_cleaned_frames(in_video_path, in_path)

    # Keep Only 1st Frame Of 30 FPS
    # keep_first_frame(in_video_path, in_path)

    # Process Images And Write Data To CSV
    process_video(in_path)


# ----------------------------------------------------------------------------------------------------------------------

# Entry Point For Main Program
if __name__ == "__main__":

    # Run Main Program
    main()
