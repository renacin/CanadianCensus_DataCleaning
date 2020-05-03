# Name:                                            Renacin Matadeen
# Date:                                               05/03/2020
# Title                                            Open CV Research
#
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# This Is The Main Function
def module_checker():

    list_of_modules = ["os", "shutil", "math", "multiprocessing", "cv2", "pytesseract", "pandas"]

    mismod_count = 0

    # Try To Import Internal Python Modules
    for module_name in list_of_modules:
        try:
            exec("import {}".format(module_name))

        except ImportError as e:
            print("Missing Module: {}".format(module_name))
            mismod_count += 1

    if (mismod_count == 0):
        print("Step 0: Module Precheck: All Modules Accounted For - ✅")

    else:
        raise SystemExit(0)
