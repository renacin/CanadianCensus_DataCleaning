# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import pytesseract
# ----------------------------------------------------------------------------------------------------------------------


# Secondary Function, Clean Text Object Orientation Helps With Possible Frame Skipping Implementation
def clean_text(in_text):

    try:
        raw_text = in_text.split(" ")

        # Pull & Clean Inputs
        date_ = raw_text[0]
        time_ = raw_text[1]
        latitude_ = float(raw_text[5].replace("W", ""))
        longitude_ = float(raw_text[6].replace("N", ""))
        speed_ = float(raw_text[7])

    except:
        date_ = "Error"
        time_ = "Error"
        latitude_ = "Error"
        longitude_ = "Error"
        speed_ = "Error"

    return date_, time_, latitude_, longitude_, speed_


# Main Function, Process Each Frame And Gather Data
def process_video(video_path):

    # Import Video
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    # Loop Through Each Frame
    counter = 1
    while True:

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

            # Display Information
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


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # Import The Dashcam Video Into OpenCV
    in_path = "/Users/renacinmatadeen/Desktop/V1.mp4"

    # Process Video
    process_video(in_path)
