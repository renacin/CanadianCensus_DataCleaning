# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import pandas as pd
import pytesseract
# ----------------------------------------------------------------------------------------------------------------------


# Secondary Function, Clean Text Object Orientation
def clean_text(in_text):

    try:
        raw_text = in_text.split(" ")

        # Pull & Clean Inputs
        date_ = raw_text[0]
        time_ = raw_text[1]
        latitude_ = float(raw_text[5].replace("W", ""))
        longitude_ = float(raw_text[6].replace("N", ""))
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
def process_video(video_path):

    # Use Dictionary As Storage Methodology For Data | Convert To Pandas Df & CSV After
    data_dictionary = {'Frame': [], 'Date': [], 'Time': [],
                       'Latitude': [], 'Longitude': [], 'Speed': []}

    # Import Video
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    # Loop Through Each Frame
    counter = 1
    for x in range(300):

        # Try To Gather Data From Frames
        try:
            # Initialize Individual Frame
            ret, frame = cap.read()

            # Convert To GrayScale | Grab Subsection
            frame_subsection = frame[1025:1075, 15:1150, 1]

            # Apply Threshold Function
            retval, threshold = cv2.threshold(frame_subsection, 180, 255, cv2.THRESH_BINARY)

            # Convert Image To Text
            raw_text = pytesseract.image_to_string(threshold)
            date_v, time_v, latitude_v, longitude_v, speed_v = clean_text(raw_text)

            # Append Information To Data_Dictionary
            data_dictionary['Frame'].append(counter)
            data_dictionary['Date'].append(date_v)
            data_dictionary['Time'].append(time_v)
            data_dictionary['Latitude'].append(latitude_v)
            data_dictionary['Longitude'].append(longitude_v)
            data_dictionary['Speed'].append(speed_v)

            # Display Information
            if (counter % 30 == 0):
                print("Frame: {}, Date: {}, Time: {}, Latitude: {}, Longitude: {}, Speed: {}".format(
                    counter, date_v, time_v, latitude_v, longitude_v, speed_v))

        # Raise KeyboardInterrupt Exit Program
        except(KeyboardInterrupt, SystemExit):
            cap.release()
            cv2.destroyAllWindows()
            break

        # Add To Frame Counter
        counter += 1

        if (cv2.waitKey(1) & 0xFF == ord('q')) or (ret == False):
            cap.release()
            cv2.destroyAllWindows()
            break

    # Write Data To CSV
    df = pd.DataFrame.from_dict(data_dictionary)
    df.to_csv("/Users/renacinmatadeen/Desktop/DashcamDataParse.csv", index=False)
    print("Progress: Data Parsed & Written")


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Import The Dashcam Video Into OpenCV
    in_path = "/Users/renacinmatadeen/Desktop/V1.mp4"

    # Process Video
    process_video(in_path)
