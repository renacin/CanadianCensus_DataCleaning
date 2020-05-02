# Name:                                            Renacin Matadeen
# Date:                                               04/23/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------
import cv2
import os
import shutil
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
def write_cleaned_frames(in_video_path, new_temp_folder):

    # Make Sure The Folder Where Data If being Written To Is Empty
    try:
        shutil.rmtree(new_temp_folder, ignore_errors=True)
        os.mkdir(new_temp_folder)

    except(FileNotFoundError):
        os.mkdir(new_temp_folder)

    # Try Main Parse
    try:
        # Instantiate Video File
        cap = cv2.VideoCapture(in_video_path)
        ret, frame = cap.read()

        # Get Number Of Frames In Video | Loop Through Each
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Loop Through Each Frame
        for frame_num in range(num_frames):  # Number Of Frames

            # Process Image
            ret, frame = cap.read()
            image_ = process_image(frame)

            image_write_path = "{}/Image_{}.jpeg".format(new_temp_folder, frame_num + 1)
            cv2.imwrite(image_write_path, image_, [int(cv2.IMWRITE_JPEG_QUALITY), 15])

            if (frame_num != 0) and (frame_num % 3000 == 0) or (frame_num / num_frames == 1):
                percent_prog = (frame_num/num_frames) * 100
                progress_ = round(percent_prog, 2)
                print("         Progress Writing Frames: {}%, Frames Written: {}/{}".format(progress_,
                                                                                            frame_num, num_frames))

        print("Step #2: Frames Separated - 🎞️")

    # Raise KeyboardInterrupt Exit Program
    except(KeyboardInterrupt, SystemExit):
        cap.release()
        cv2.destroyAllWindows()

    # Raise KeyboardInterrupt Exit Program
    except:
        cap.release()
        cv2.destroyAllWindows()


# Secondary Function, Iterate Through Each Frame Keep Only The FPSth Frame
def keep_first_frame(in_video_path, new_temp_folder):

    # Instantiate Video From Path
    cap = cv2.VideoCapture(in_video_path)

    # Grab Number Of Frames, and Frame Rate Of Video
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Loop Through Files In Directory Remove Images Redundant Images
    for filename in os.listdir(new_temp_folder):

        # Each Image Had A Frame Number Attached, Look At That. Be Careful In The Future Through
        image_frame_num = int(filename[6:-5])

        if (filename.endswith(".jpeg")) and (image_frame_num % num_fps == 0):
            pass
        else:
            try:
                os.remove(new_temp_folder + "/" + filename)
            except:
                pass

    print("Step #3: Unneeded Frames Deleted - 📂")
